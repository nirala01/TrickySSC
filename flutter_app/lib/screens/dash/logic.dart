// Dashboard analysis — a port of the website dashboard (dashboard.html, TSSC-DASHPRO-V1 / DASHSCOPE-V1).
// Works on the attempt maps from Firestore `attempts`.
import 'dart:convert';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:shared_preferences/shared_preferences.dart';

import '../../aic.dart';
import '../../aic_io.dart';
import '../../data.dart';

typedef Att = Map<String, dynamic>;

double dnum(dynamic v) => v is num ? v.toDouble() : double.tryParse('$v') ?? 0;
int inum(dynamic v) => v is num ? v.toInt() : int.tryParse('$v') ?? 0;
String s(dynamic v) => v == null ? '' : '$v';
String n1(num v) {
  final r = (v * 10).round() / 10;
  return r == r.roundToDouble() ? '${r.round()}' : r.toStringAsFixed(1);
}

bool isChapter(Att a) => a['type'] == 'chapterwise' || a['type'] == 'pyq-chapter';
bool isFullPaper(Att a) => !isChapter(a) && a['testKind'] != 'pyq-subject' && a['testKind'] != 'mock-subject';
bool isMockAtt(Att a) => !isChapter(a) && (s(a['mockId']).isNotEmpty || a['type'] == 'mock' || s(a['paperId']).contains('_mock'));
bool isPaper23(Att a) => RegExp(r'_paper[23]_').hasMatch(s(a['paperId']) + s(a['mockId'])); // CGL Paper II / III: +2 / −0.5, not Tier 2 marking
bool isTier2(Att a) => !isPaper23(a) && (a['tier'] == 'tier2' || RegExp(r'tier2|tier-2|tier_2', caseSensitive: false).hasMatch(s(a['paperId']) + s(a['mockId'])));

({double pos, double neg}) posneg(Att a) {
  final e = s(a['exam']);
  final x = examById(e);
  if (isTier2(a) && (x?.tier2 ?? true)) return (pos: 3.0, neg: 1.0);
  return x == null ? (pos: 2.0, neg: 0.5) : (pos: x.pos, neg: x.neg);
}

double maxOf(Att a) {
  final m = dnum(a['maxMarks']);
  if (m > 0) return m;
  final t = inum(a['total']);
  return (t > 0 ? t : 100) * posneg(a).pos;
}

double marksOf(Att a) {
  final m = a['marks'];
  if (m != null && '$m'.isNotEmpty) return dnum(m);
  return (dnum(a['percentage']) / 100 * maxOf(a)).roundToDouble();
}

int tsOf(Att a) => attemptMs(a);

String _strip(String id) => id.replaceAll(RegExp(r'([_\-])(hi|en|hindi|english)$', caseSensitive: false), '');

String cwKey(Att a) {
  final c = s(a['chapterId'] ?? a['chapter']).replaceAll(RegExp(r'[^a-zA-Z0-9]'), '');
  return c.isEmpty ? '' : 'cw_${c}_L${inum(a['level']) == 0 ? 1 : inum(a['level'])}_T${inum(a['testNum']) == 0 ? 1 : inum(a['testNum'])}';
}

String lbKeyOf(Att a) {
  if (isChapter(a)) return s(a['lbKey']).isNotEmpty ? s(a['lbKey']) : cwKey(a);
  if (a['testKind'] == 'pyq-subject') return '';
  if (a['testKind'] == 'mock-subject' && s(a['subjectKey']).isNotEmpty) {
    final b = s(a['baseMockId']).isNotEmpty ? s(a['baseMockId']) : s(a['mockId']).replaceAll(RegExp(r'__[a-z]+$', caseSensitive: false), '');
    return b.isEmpty ? '' : '${_strip(b)}__${a['subjectKey']}';
  }
  final id = s(a['paperId']).isNotEmpty ? s(a['paperId']) : s(a['mockId']);
  return id.isEmpty ? '' : _strip(id);
}

String examTier(Att a) => '${s(a['exam']).isEmpty ? 'ssc-cgl' : a['exam']}|${isTier2(a) ? 'tier2' : 'tier1'}';

String testName(Att a) {
  if (isChapter(a)) {
    final n = s(a['chapterName']).isNotEmpty ? s(a['chapterName']) : s(a['examName']).replaceAll(' (PYQ)', '');
    final tn = inum(a['testNum']) == 0 ? 1 : inum(a['testNum']);
    return a['type'] == 'pyq-chapter' ? '$n · PYQ Test $tn' : '$n · Level ${inum(a['level']) == 0 ? 1 : inum(a['level'])} · Test $tn';
  }
  // All India Challenge: the live Sunday attempt, or the free mock taken after the result
  final ar = aicRoundOf(s(a['mockId']));
  if (ar > 0) return 'All India Challenge Mock $ar${a['aic'] is Map && (a['aic'] as Map)['live'] == true ? '' : ' · Free mock'}';
  final sub = s(a['subjectKey']).isNotEmpty ? ' · ${_subjName(s(a['subjectKey']))}' : '';
  const tiers = {'tier1': 'Tier 1 ', 'tier2': 'Tier 2 ', 'cbt1': 'CBT 1 ', 'cbt2': 'CBT 2 ', 'paper2': 'Statistics ', 'paper3': 'AAO '};
  final ids = [s(a['mockId']), s(a['baseMockId']), s(a['paperId']), s(a['basePaperId'])].where((v) => v.isNotEmpty);
  for (final id in ids) {
    // a mock: ssc-cgl_tier1_mock2_en, ssc-gd_2027_mock12_en
    final m = RegExp(r'^([a-z-]+)_(?:(\d{4})_)?(?:.*?(tier\d|cbt\d|paper\d)_)?(?:.*_)?mock(\d+)_(?:en|hi)').firstMatch(id);
    if (m != null) {
      final e = examById(m.group(1)!);
      final ex = e?.name ?? _idWords(m.group(1)!);
      final tier = (e?.tier2 ?? false) || m.group(3) != 'tier1' ? (tiers[m.group(3)] ?? '') : '';
      return '$ex ${m.group(2) == null ? '' : '${m.group(2)} '}${tier}Mock ${int.parse(m.group(4)!)}$sub';
    }
  }
  for (final id in ids) {
    // a previous-year paper: ssc-cgl_2026_tier1_shift-1_2026-10-13_en
    final m = RegExp(r'^([a-z-]+)_(\d{4})_(?:(tier\d|cbt\d|paper\d)_)?(.*?)_?(\d{4})-(\d{2})-(\d{2})_(?:en|hi)').firstMatch(id);
    if (m != null) {
      final e = examById(m.group(1)!);
      final ex = e?.name ?? _idWords(m.group(1)!);
      final tier = (e?.tier2 ?? false) || (m.group(3) != null && m.group(3) != 'tier1') ? (tiers[m.group(3)] ?? '') : '';
      const mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      final mo = int.parse(m.group(6)!);
      final date = '${int.parse(m.group(7)!)} ${mo >= 1 && mo <= 12 ? mon[mo - 1] : ''} ${m.group(5)}';
      final sh = RegExp(r'shift-?(\d+)').firstMatch(m.group(4)!);
      final shift = sh != null ? ' · Shift ${sh.group(1)}' : (m.group(4)!.isEmpty ? '' : ' · ${_idWords(m.group(4)!)}');
      return '$ex $tier${m.group(2)} · $date$shift$sub';
    }
  }
  final n = s(a['examName']).replaceAll(RegExp(r'\s*—.*$'), '').trim();
  return n.isEmpty ? 'Test' : '$n$sub';
}

String _idWords(String v) => v.split(RegExp(r'[-_]+')).where((w) => w.isNotEmpty).map((w) => w.length <= 4 ? w.toUpperCase() : w[0].toUpperCase() + w.substring(1)).join(' ');

String _subjName(String k) => const {'quant': 'Maths', 'maths': 'Maths', 'reasoning': 'Reasoning', 'english': 'English', 'gk': 'GK', 'ga': 'GK', 'computer': 'Computer', 'scimaths': 'Maths & Science', 'di': 'Data Interpretation', 'logical': 'Logical Capability', 'mental': 'Mental Reasoning'}[k.toLowerCase()] ?? k;

/// Subject key normalisation (website SUBJ_KEY).
String? skey(String k) {
  final l = k.trim().toLowerCase();
  if (l.isEmpty) return null;
  if (RegExp(r'^(quant|maths?|mathematical abilities|quantitative aptitude|mathematics)$').hasMatch(l) || l.contains('quant') || l.contains('math')) return 'Q';
  if (l.contains('reason') || l.contains('intelligence')) return 'R';
  if (l.contains('english')) return 'E';
  if (l.contains('aware') || l == 'ga' || l == 'gk' || l.contains('general studies') || l.contains('science')) return 'G';
  if (l.contains('comput')) return 'C';
  if (l.contains('statist')) return 'S';
  return null;
}

const subjName = {'Q': 'Quant', 'R': 'Reasoning', 'E': 'English', 'G': 'Gen. Awareness', 'C': 'Computer', 'S': 'Statistics'};

Map<String, double> subjMarks(Att a) {
  final out = <String, double>{};
  final pn = posneg(a);
  final sm = a['subjectMarks'];
  if (sm is Map) {
    sm.forEach((k, v) {
      final x = skey('$k');
      if (x != null) out[x] = (out[x] ?? 0) + dnum(v);
    });
    if (out.isNotEmpty) return out;
  }
  final ss = a['subjectStats'];
  if (ss is Map) {
    ss.forEach((k, v) {
      final x = skey('$k');
      if (x != null && v is Map) out[x] = (out[x] ?? 0) + inum(v['correct']) * pn.pos - inum(v['wrong']) * pn.neg;
    });
  }
  return out;
}

// ---------------------------------------------------------------- cut-offs (website CUTOFFS)

class Cutoff {
  final String label;
  final double max;
  final bool merit;
  final Map<String, double> cut;
  final String? prevLabel;
  final Map<String, double>? prev;
  const Cutoff(this.label, this.max, this.cut, {this.merit = false, this.prevLabel, this.prev});
}

const cats = ['GEN', 'OBC', 'EWS', 'SC', 'ST'];

const cutoffs = <String, Cutoff>{
  'ssc-cgl|tier1': Cutoff('SSC CGL 2025 Tier I (all other posts)', 200, {'GEN': 136.83, 'OBC': 130.37, 'EWS': 127.42, 'SC': 114.97, 'ST': 106.37},
      prevLabel: '2024', prev: {'GEN': 153.19, 'OBC': 146.26, 'EWS': 142.02, 'SC': 126.46, 'ST': 111.89}),
  'ssc-chsl|tier1': Cutoff('SSC CHSL 2025 Tier I (LDC/JSA)', 200, {'GEN': 144.26, 'OBC': 143.83, 'EWS': 141.42, 'SC': 125.40, 'ST': 115.25},
      prevLabel: '2024', prev: {'GEN': 157.36, 'OBC': 156.62, 'EWS': 150.52, 'SC': 139.68, 'ST': 129.45}),
  'ssc-cgl|tier2': Cutoff('SSC CGL 2024 Tier II final (lowest post, Sec I+II / 390)', 390, {'GEN': 322.77, 'OBC': 306.28, 'EWS': 300.04, 'SC': 285.46, 'ST': 266.50},
      merit: true, prevLabel: '2025 Inspector (Income Tax)', prev: {'GEN': 342, 'OBC': 334, 'EWS': 334, 'SC': 322, 'ST': 313}),
  'ssc-gd|tier1': Cutoff('SSC GD 2026 CBE (male, overall)', 160, {'GEN': 146.18, 'OBC': 145.56, 'EWS': 144.21, 'SC': 140.95, 'ST': 135.03}),
};

double meritMarks(Att a) {
  final c = cutoffs[examTier(a)];
  if (c == null || !c.merit) return marksOf(a);
  final sm = subjMarks(a);
  final keys = sm.keys.where((k) => 'QREG'.contains(k)).toList();
  return keys.isEmpty ? marksOf(a) : keys.fold(0.0, (t, k) => t + sm[k]!);
}

// ---------------------------------------------------------------- scopes

String scopeOf(Att a) {
  if (isChapter(a)) return 'ch|${s(a['chapterId'] ?? a['chapter'])}|${a['type']}';
  if ((a['testKind'] == 'pyq-subject' || a['testKind'] == 'mock-subject') && s(a['subjectKey']).isNotEmpty) {
    return 'subj|${examTier(a)}|${s(a['subjectKey']).toLowerCase()}';
  }
  return 'full|${examTier(a)}';
}

String scopeLabel(String key, Att a) {
  final p = key.split('|');
  if (p[0] == 'ch') {
    final n = s(a['chapterName']).isNotEmpty ? s(a['chapterName']) : p[1];
    return '$n · ${p.length > 2 && p[2] == 'pyq-chapter' ? 'Chapter PYQs' : 'Chapter tests'}';
  }
  final ex = examById(p[1])?.name ?? p[1];
  final tier = (examById(p[1])?.tier2 ?? false) ? (p[2] == 'tier2' ? ' Tier II' : ' Tier I') : '';
  if (p[0] == 'subj') return '$ex$tier · ${_subjName(p[3])} tests';
  return '$ex$tier · Full tests';
}

// ---------------------------------------------------------------- per-attempt analysis

List<Map<String, dynamic>> answersOf(Att a) => [
      if (a['answers'] is List)
        for (final x in a['answers'] as List)
          if (x is Map) Map<String, dynamic>.from(x)
    ];

/// Chapter id -> chapter name ("fineco.accounting-basics" -> "Accounting Basics"), filled from the website
/// chapter lists by loadAllChapterNames() in chapters.dart.
final Map<String, String> chapterNames = {};

/// The name to show for a question's chapter tag. Tags are chapter ids on most tests; anything that is
/// already a name is returned as it is. Unknown ids are turned into words.
String chapterLabel(String raw) {
  final hit = chapterNames[raw] ?? pyqChapterNames[raw];
  if (hit != null && hit.isNotEmpty) return hit;
  if (!RegExp(r'^[a-z0-9]+[._][a-z0-9._-]+$').hasMatch(raw)) return raw;
  if (raw.length >= 40) {
    // saved tags are cut at 40 characters
    for (final e in chapterNames.entries) {
      if (e.key.startsWith(raw)) return e.value;
    }
  }
  const small = {'and', 'of', 'the', 'in', 'to', 'for', 'on'};
  const caps = {'gst': 'GST', 'gdp': 'GDP', 'rbi': 'RBI', 'lcm': 'LCM', 'hcf': 'HCF', 'si': 'SI', 'ci': 'CI', 'ms': 'MS', 'di': 'DI', 'gk': 'GK', 'pyq': 'PYQ', 'cag': 'CAG', 'it': 'IT'};
  final words = raw.substring(raw.indexOf(RegExp(r'[._]')) + 1).split(RegExp(r'[-._]+')).where((w) => w.isNotEmpty).toList();
  return [
    for (var i = 0; i < words.length; i++)
      caps[words[i]] ?? (i > 0 && small.contains(words[i]) ? words[i] : words[i][0].toUpperCase() + words[i].substring(1))
  ].join(' ');
}

class ChStat {
  final String name;
  final String? id; // the official chapter id, when the row is a real chapter
  int n = 0, c = 0, w = 0, k = 0;
  ChStat(this.name, [this.id]);
  double get acc => n == 0 ? 0 : c / n;
}

/// Chapter name for a saved tag: id -> name, and a paper name stuck after a dash is dropped
/// ("Syllogism — SSC CGL 2025 Sep 25 Shift 1" -> "Syllogism").
String cleanChapter(String raw) {
  var n = chapterLabel(raw.length > 40 ? raw.substring(0, 40) : raw);
  final cutAt = n.indexOf(RegExp(r'\s[—–]\s'));
  if (cutAt > 0) n = n.substring(0, cutAt);
  return n.trim();
}

const _chPrefix = {'hindi': 'Hindi', 'quant': 'Quant', 'math': 'Quant', 'maths': 'Quant', 'reason': 'Reasoning', 'reasoning': 'Reasoning', 'eng': 'English', 'english': 'English', 'ga': 'Gen. Awareness', 'gk': 'Gen. Awareness', 'computer': 'Computer', 'statistics': 'Statistics', 'fineco': 'Finance & Economics'};

const _chSmall = {'and', 'of', 'the', 'in', 'to', 'for', 'on', 'a', 'an', 'by', 'with'};

/// Words of a chapter name or topic note, lower case, without plural "s" and small words.
List<String> _stems(String v) => [
      for (final w in v.toLowerCase().replaceAll('&', ' ').split(RegExp(r'[^a-z0-9]+')))
        if (w.isNotEmpty && !_chSmall.contains(w)) w.length > 3 && w.endsWith('s') ? w.substring(0, w.length - 1) : w
    ];

/// Topic words that point to a chapter whose name does not carry them.
const _chAlias = {
  'quant.number-system': ['number system', 'unit digit', 'factor'],
  'quant.divisibility': ['divisible'],
  'quant.remainder-theorem': ['remainder'],
  'quant.decimal-fraction': ['fraction', 'decimal'],
  'quant.lcm-hcf': ['lcm', 'hcf'],
  'quant.square-cube-root': ['square root', 'cube root'],
  'quant.series-ap-gp': ['progression', 'ap gp'],
  'quant.simplification': ['simplification', 'surd', 'indice', 'bodma'],
  'quant.algebra': ['algebra', 'identity', 'linear equation', 'polynomial'],
  'quant.percentage': ['percent'],
  'quant.profit-loss': ['profit'],
  'quant.discount': ['discount', 'marked price'],
  'quant.simple-interest': ['si'],
  'quant.compound-interest': ['ci', 'installment'],
  'quant.ratio-proportion': ['ratio', 'proportion'],
  'quant.average': ['average', 'mean'],
  'quant.ages': ['age'],
  'quant.mixture-alligation': ['mixture', 'alligation'],
  'quant.time-work': ['work wage', 'work', 'efficiency'],
  'quant.pipe-cistern': ['pipe', 'cistern'],
  'quant.time-speed-distance': ['speed', 'train', 'time distance'],
  'quant.boat-stream': ['boat', 'stream'],
  'quant.race': ['race'],
  'quant.trigonometry': ['trigonometric', 'trigo'],
  'quant.height-distance': ['height', 'elevation'],
  'quant.geometry': ['geometry', 'triangle', 'circle', 'quadrilateral', 'polygon', 'angle', 'chord', 'tangent'],
  'quant.mensuration': ['mensuration', 'area', 'volume', 'cylinder', 'cone', 'sphere', 'cube', 'cuboid', 'prism', 'pyramid', 'perimeter', '2d', '3d'],
  'quant.coordinate-geometry': ['coordinate'],
  'quant.statistics': ['median', 'mode', 'statistic'],
  'quant.data-interpretation': ['di', 'data interpretation', 'bar graph', 'pie chart', 'graph', 'chart', 'table', 'histogram'],
  'reason.analogy-word': ['analogy'],
  'reason.classification-word': ['classification', 'odd one', 'odd man'],
  'reason.series': ['series'],
  'reason.coding-decoding': ['coding', 'decoding'],
  'reason.blood-relation': ['blood', 'relation'],
  'reason.direction-distance': ['direction'],
  'reason.ranking-arrangement': ['ranking', 'order'],
  'reason.seating-arrangement': ['seating', 'arrangement'],
  'reason.statement-conclusion': ['statement', 'inference', 'assumption', 'conclusion', 'course action'],
  'reason.venn-diagram': ['venn'],
  'reason.mathematical-operations': ['operation', 'symbol', 'interchange', 'equation'],
  'reason.word-formation': ['dictionary', 'alphabet', 'word formation', 'jumbled word'],
  'reason.missing-number': ['missing number', 'matrix', 'missing term'],
  'reason.puzzle': ['puzzle'],
  'reason.calendar-clock': ['calendar', 'clock'],
  'reason.mirror-image': ['mirror', 'water image'],
  'reason.paper-folding': ['paper folding', 'paper cutting', 'embedded', 'figure completion', 'completion', 'hidden figure'],
  'reason.figure-series': ['figure series', 'figure counting', 'counting figure', 'figure', 'pattern', 'non verbal'],
  'reason.dice': ['dice', 'cube'],
  'eng.error-spotting': ['error'],
  'eng.sentence-improvement': ['improvement'],
  'eng.fill-blanks': ['fill', 'blank', 'preposition', 'article', 'grammar', 'vocabulary'],
  'eng.active-passive': ['voice', 'active', 'passive'],
  'eng.narration': ['narration', 'speech', 'direct indirect'],
  'eng.para-jumbles': ['jumble', 'rearrangement', 'pqr', 'arrangement'],
  'eng.synonyms': ['synonym'],
  'eng.antonyms': ['antonym'],
  'eng.spelling': ['spelling', 'spelt', 'misspelt', 'misspelled'],
  'eng.idioms-phrases': ['idiom', 'phrase'],
  'eng.one-word': ['one word', 'substitution'],
  'eng.homonyms': ['homonym', 'homophone'],
  'eng.cloze-test': ['cloze'],
  'eng.reading-comprehension': ['comprehension', 'passage'],
  'ga.history-ancient': ['ancient'],
  'ga.history-medieval': ['medieval'],
  'ga.history-modern': ['modern', 'freedom', 'history', 'national movement'],
  'ga.art-culture': ['art', 'culture', 'dance', 'festival', 'music'],
  'ga.geography-india': ['geography', 'river', 'soil', 'agriculture'],
  'ga.geography-world': ['world geography', 'physical geography', 'world'],
  'ga.polity': ['polity', 'constitution', 'parliament', 'article', 'fundamental right'],
  'ga.economics': ['economic', 'economy', 'banking', 'budget'],
  'ga.physics': ['physic'],
  'ga.chemistry': ['chemistry', 'chemical'],
  'ga.biology': ['biology', 'disease', 'botany', 'zoology'],
  'ga.static-books-authors': ['book', 'author'],
  'ga.static-awards': ['award', 'honour'],
  'ga.static-days-events': ['important day'],
  'ga.static-sports': ['sport'],
  'ga.static-schemes': ['scheme', 'yojana'],
  'ga.static-organizations': ['organization', 'organisation', 'headquarter'],
  'ga.static-misc': ['static', 'miscellaneou'],
  'ga.current-affairs': ['current', 'affair'],
  'computer.fundamentals': ['fundamental', 'hardware', 'software', 'generation', 'input', 'output'],
  'computer.memory-storage': ['memory', 'storage'],
  'computer.os-windows': ['operating system', 'window', 'shortcut'],
  'computer.ms-office': ['office', 'word', 'excel', 'powerpoint'],
  'computer.internet-email': ['internet', 'email', 'mail', 'browser', 'web'],
  'computer.networking': ['network'],
  'computer.cyber-security': ['security', 'viru', 'malware', 'cyber'],
};

const _chLetter = {'quant': 'Q', 'reason': 'R', 'eng': 'E', 'ga': 'G', 'computer': 'C', 'statistics': 'S'};

List<({String id, String letter, Set<String> words})>? _chPhrases;
int _chPhrasesN = -1;

/// The chapter of every previous-year question (assets/pyq_chapters.json), filled by loadPyqChapterMap().
final Map<String, List<int>> pyqChapterMap = {};
List<String> pyqChapterIds = const [];
final Map<String, String> pyqChapterNames = {}; // names of the chapters that have no chapter-test list (Hindi)
bool pyqChapterMapLoaded = false;

Future<void> loadPyqChapterMap() async {
  if (pyqChapterMapLoaded) return;
  try {
    final d = jsonDecode(await rootBundle.loadString('assets/pyq_chapters.json')) as Map;
    pyqChapterIds = [for (final c in d['ch'] as List) '$c'];
    final n = d['n'];
    if (n is List) {
      for (var i = 0; i < n.length && i < pyqChapterIds.length; i++) {
        if ('${n[i]}'.isNotEmpty) pyqChapterNames[pyqChapterIds[i]] = '${n[i]}';
      }
    }
    (d['p'] as Map).forEach((k, v) => pyqChapterMap['$k'] = [for (final i in v as List) (i as num).toInt()]);
  } catch (_) {}
  pyqChapterMapLoaded = true;
}

/// The chapter id of one answered question: from the paper's own chapter list when it is a
/// previous-year paper, else from the saved tag.
String? chapterIdFor(Att a, Map<String, dynamic> x, String raw) {
  final pid = s(a['basePaperId']).isNotEmpty ? s(a['basePaperId']) : s(a['paperId']);
  if (pid.isNotEmpty && pyqChapterMap.isNotEmpty) {
    final row = pyqChapterMap[pid.replaceAll(RegExp(r'__.*$'), '').replaceAll(RegExp(r'_(en|hi)$'), '')];
    final q = inum(x['q']);
    if (row != null && q >= 1 && q <= row.length && row[q - 1] >= 0 && row[q - 1] < pyqChapterIds.length) return pyqChapterIds[row[q - 1]];
  }
  return raw.isEmpty ? null : chapterIdOf(raw, skey(s(x['s'])) ?? skey(s(a['subject'])));
}

/// The official chapter (id) for a saved tag, or null. Tags are chapter ids on chapter tests and new
/// papers; older papers and mocks carry a free-text topic ("Heights and Distances — angle of elevation"),
/// matched by its words to the chapter names of the same subject.
String? chapterIdOf(String raw, [String? letter]) {
  if (chapterNames.containsKey(raw)) return raw;
  if (RegExp(r'^[a-z0-9]+[._][a-z0-9._-]+$').hasMatch(raw)) {
    if (raw.length >= 40) {
      for (final k in chapterNames.keys) {
        if (k.startsWith(raw)) return k;
      }
    }
    return RegExp(r'^(quant|reason|eng|ga|computer|statistics|fineco|hindi)\.').hasMatch(raw) ? raw : null;
  }
  if (_chPhrases == null || _chPhrasesN != chapterNames.length) {
    final out = <({String id, String letter, Set<String> words})>[];
    void add(String id, String phrase) {
      final w = _stems(phrase).toSet();
      if (w.isNotEmpty) out.add((id: id, letter: _chLetter[id.split('.').first] ?? '', words: w));
    }

    for (final e in chapterNames.entries) {
      add(e.key, e.value);
      add(e.key, e.value.split(RegExp(r'[(/]')).first);
      if (e.value.contains(':')) add(e.key, e.value.split(':').last.split(RegExp(r'[(/]')).first);
      add(e.key, e.key.substring(e.key.indexOf('.') + 1));
    }
    for (final e in _chAlias.entries) {
      if (!chapterNames.containsKey(e.key)) continue;
      for (final p in e.value) {
        add(e.key, p);
      }
    }
    _chPhrases = out;
    _chPhrasesN = chapterNames.length;
  }
  final tag = _stems(raw).toSet();
  if (tag.isEmpty) return null;
  String? best;
  var score = 0;
  for (final p in _chPhrases!) {
    if (letter != null && p.letter.isNotEmpty && p.letter != letter) continue;
    if (p.words.length > score && tag.containsAll(p.words)) {
      best = p.id;
      score = p.words.length;
    }
  }
  return best;
}

const otherTopics = 'Other topics';

/// Hindi has no chapter-test list, so its chapters are the chapter-wise PYQ ones (hindi.*). A topic note
/// of a Hindi question (from a mock) is matched to them by these words.
const _hindiKeys = {
  'hindi.paryayvachi': ['पर्याय', 'समानार्थ', 'synonym', 'paryay'],
  'hindi.vilom': ['विलोम', 'विपरीत', 'antonym', 'vilom'],
  'hindi.muhavare-lokoktiyan': ['मुहावर', 'लोकोक्ति', 'कहावत', 'idiom', 'proverb', 'muhavar', 'lokokti'],
  'hindi.anek-shabd': ['वाक्यांश', 'एक शब्द', 'one word', 'substitution'],
  'hindi.anekarthi-shabd': ['अनेकार्थ', 'समश्रुत', 'भिन्नार्थ', 'homonym', 'anekarth', 'shrutisam'],
  'hindi.gadyansh': ['गद्यांश', 'अपठित', 'पद्यांश', 'comprehension', 'passage', 'gadyansh'],
  'hindi.rikt-sthan': ['रिक्त', 'fill', 'blank', 'rikt'],
  'hindi.shabd-bhed': ['तत्सम', 'तद्भव', 'देशज', 'विदेशज', 'tatsam', 'tadbhav', 'origin'],
  'hindi.vakya-shuddhi': ['वाक्य', 'अशुद्ध', 'sentence', 'error', 'vakya'],
  'hindi.vartani': ['वर्तनी', 'spelling', 'vartani'],
  'hindi.vyakaran': ['संज्ञा', 'सर्वनाम', 'विशेषण', 'क्रिया', 'लिंग', 'वचन', 'कारक', 'काल', 'संधि', 'समास', 'उपसर्ग', 'प्रत्यय', 'अलंकार', 'रस', 'छंद', 'व्याकरण', 'अव्यय', 'grammar', 'sandhi', 'samas', 'vyakaran', 'noun', 'pronoun', 'verb', 'gender', 'tense'],
};

final _isHindi = RegExp(r'hindi|हिंदी|हिन्दी', caseSensitive: false);

String? _hindiChapter(String raw) {
  final l = raw.toLowerCase();
  for (final e in _hindiKeys.entries) {
    if (!pyqChapterNames.containsKey(e.key)) continue;
    for (final k in e.value) {
      if (l.contains(k)) return e.key;
    }
  }
  return null;
}

/// The Hindi chapters (names), for the full chapter list of the dashboard.
List<String> get hindiChapterNames => [
      for (final e in pyqChapterNames.entries)
        if (e.key.startsWith('hindi.')) e.value
    ];

/// Chapters grouped under their subject: subject name -> chapter stats. Once the chapter lists are
/// loaded, only real chapters are listed; every other topic of a subject is added up as "Other topics".
Map<String, List<ChStat>> chaptersBySubject(List<Att> list) {
  final m = <String, Map<String, ChStat>>{};
  final official = chapterNames.isNotEmpty;
  // subjects that have a chapter list; a topic of any other subject (Hindi, ...) keeps its own name
  final listed = {for (final id in chapterNames.keys) _chPrefix[id.split('.').first]};
  for (final a in list) {
    final own = subjName[skey(s(a['subject']))];
    for (final x in answersOf(a)) {
      final raw = s(x['ch']).replaceAll(RegExp(r'<[^>]*>'), ' ').replaceAll(RegExp(r'\s+'), ' ').trim();
      var id = official ? chapterIdFor(a, x, raw) : null;
      final hindi = _isHindi.hasMatch(s(x['s'])) || (id ?? '').startsWith('hindi.');
      if (id == null && hindi && raw.isNotEmpty) id = _hindiChapter(raw);
      if (raw.isEmpty && id == null) continue;
      final pre = RegExp(r'^([a-z]+)[._]').firstMatch(id ?? raw)?.group(1);
      final sub = (hindi ? 'Hindi' : null) ??
          (id != null ? _chPrefix[pre] : null) ??
          subjName[skey(s(x['s']))] ??
          own ??
          _chPrefix[pre] ??
          (s(x['s']).isEmpty || s(x['s']) == 'General' ? 'Other' : s(x['s']));
      final name = id != null ? (chapterNames[id] ?? chapterLabel(id)) : (official && listed.contains(sub) ? otherTopics : cleanChapter(raw));
      final st = (m[sub] ??= {}).putIfAbsent(name, () => ChStat(name, chapterNames.containsKey(id) ? id : null));
      st.n++;
      if (x['r'] == 'c') {
        st.c++;
      } else if (x['r'] == 'w') {
        st.w++;
      } else {
        st.k++;
      }
    }
  }
  return {for (final e in m.entries) e.key: e.value.values.toList()};
}

/// Every chapter of the attempts in one list (the same chapters as chaptersBySubject).
List<ChStat> chapterStats(List<Att> list) => [
      for (final l in chaptersBySubject(list).values)
        for (final c in l)
          if (c.name != otherTopics) c
    ];

class Lost {
  final int c, w, k, total;
  final double pos, neg, recover;
  final Map<String, int> cnt;
  final int tagged;
  Lost(this.c, this.w, this.k, this.total, this.pos, this.neg, this.cnt, this.tagged, this.recover);
  double get wrongMiss => w * pos;
  double get penalty => w * neg;
  double get skipped => k * pos;
  int get attempted => c + w;
  double get acc => c + w == 0 ? 0 : c / (c + w);
}

Lost lostOf(Att a) {
  final pn = posneg(a);
  final c = inum(a['correct']), w = inum(a['wrong']), k = inum(a['skip']);
  final cnt = {'concept': 0, 'calc': 0, 'silly': 0, 'guess': 0, 'time': 0, 'fact': 0};
  final tags = a['errTags'];
  if (tags is Map) {
    for (final t in tags.values) {
      if (cnt.containsKey('$t')) cnt['$t'] = cnt['$t']! + 1;
    }
  }
  final tagged = cnt.values.fold(0, (x, y) => x + y);
  final recover = tagged > 0 ? (cnt['calc']! + cnt['silly']!) * (pn.pos + pn.neg) + cnt['fact']! * pn.pos : (w * 0.4).round() * (pn.pos + pn.neg);
  return Lost(c, w, k, inum(a['total']) == 0 ? 100 : inum(a['total']), pn.pos, pn.neg, cnt, tagged, recover);
}

class SubAcc {
  final String key, name;
  final int n, c;
  SubAcc(this.key, this.name, this.n, this.c);
  double get acc => n == 0 ? 0 : c / n;
}

List<SubAcc> subjectAcc(List<Att> list) {
  final m = <String, List<int>>{};
  for (final a in list) {
    final ss = a['subjectStats'];
    if (ss is! Map) continue;
    ss.forEach((k, v) {
      final x = skey('$k');
      if (x == null || v is! Map) return;
      final g = m.putIfAbsent(x, () => [0, 0, 0]);
      g[0] += inum(v['correct']);
      g[1] += inum(v['wrong']);
      g[2] += inum(v['skip']);
    });
  }
  return [for (final e in m.entries) SubAcc(e.key, subjName[e.key] ?? e.key, e.value[0] + e.value[1] + e.value[2], e.value[0])];
}

int streakDays(List<Att> all) {
  final days = {for (final a in all) if (tsOf(a) > 0) _day(tsOf(a))};
  var t = DateTime.now();
  t = DateTime(t.year, t.month, t.day);
  if (!days.contains(_day(t.millisecondsSinceEpoch))) t = t.subtract(const Duration(days: 1));
  var n = 0;
  while (days.contains(_day(t.millisecondsSinceEpoch))) {
    n++;
    t = t.subtract(const Duration(days: 1));
  }
  return n;
}

List<bool> last7(List<Att> all) {
  final days = {for (final a in all) if (tsOf(a) > 0) _day(tsOf(a))};
  final now = DateTime.now();
  return [for (var i = 6; i >= 0; i--) days.contains(_day(DateTime(now.year, now.month, now.day - i).millisecondsSinceEpoch))];
}

String _day(int ms) {
  final d = DateTime.fromMillisecondsSinceEpoch(ms);
  return '${d.year}-${d.month}-${d.day}';
}

String shortDate(int ms) {
  if (ms == 0) return '';
  final d = DateTime.fromMillisecondsSinceEpoch(ms);
  const m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  return '${d.day} ${m[d.month - 1]}';
}

String fmtSec(num v) {
  final x = v.round();
  if (x <= 0) return '0s';
  if (x < 60) return '${x}s';
  final m = x ~/ 60, r = x % 60;
  return '${m}m${r > 0 ? ' ${r}s' : ''}';
}

// ---------------------------------------------------------------- leaderboard (website fetchRanks)

class LbInfo {
  final bool none, err;
  final double my, max, avg, tAvg, top;
  final int total, ahead;
  final String topName;
  final double? topAcc;
  final double topTime;
  final Map<String, double> topSubj;
  final Map<String, ({double my, int ahead, double avg, int n})> subj;
  /// Averages of the top 10% and top 25% of the board: label -> marks, time used, subject marks.
  final List<({String label, double marks, double time, Map<String, double> subj})> bands;
  LbInfo({this.bands = const [], this.none = false, this.err = false, this.my = 0, this.max = 0, this.avg = 0, this.tAvg = 0, this.top = 0, this.total = 0, this.ahead = 0, this.topName = '', this.topAcc, this.topTime = 0, this.topSubj = const {}, this.subj = const {}});
  int get rank => ahead + 1;
  double get pctile => total == 0 ? 0 : ((1 - ahead / total) * 1000).round() / 10;
  bool get ok => !none && !err;

  Map<String, dynamic> toJson() => {
        'none': none, 'err': err, 'my': my, 'max': max, 'avg': avg, 'tAvg': tAvg, 'top': top, 'total': total, 'ahead': ahead,
        'topName': topName, 'topAcc': topAcc, 'topTime': topTime, 'topSubj': topSubj,
        'subj': {for (final e in subj.entries) e.key: {'my': e.value.my, 'ahead': e.value.ahead, 'avg': e.value.avg, 'n': e.value.n}},
        'bands': [for (final b in bands) {'label': b.label, 'marks': b.marks, 'time': b.time, 'subj': b.subj}],
      };
  factory LbInfo.fromJson(Map j) => LbInfo(
        none: j['none'] == true, err: j['err'] == true, my: dnum(j['my']), max: dnum(j['max']), avg: dnum(j['avg']), tAvg: dnum(j['tAvg']), top: dnum(j['top']),
        total: inum(j['total']), ahead: inum(j['ahead']), topName: s(j['topName']), topAcc: j['topAcc'] == null ? null : dnum(j['topAcc']), topTime: dnum(j['topTime']),
        topSubj: {for (final e in ((j['topSubj'] as Map?) ?? {}).entries) '${e.key}': dnum(e.value)},
        subj: {for (final e in ((j['subj'] as Map?) ?? {}).entries) '${e.key}': (my: dnum(e.value['my']), ahead: inum(e.value['ahead']), avg: dnum(e.value['avg']), n: inum(e.value['n']))},
        bands: [
          for (final b in ((j['bands'] as List?) ?? const []))
            if (b is Map)
              (label: s(b['label']), marks: dnum(b['marks']), time: dnum(b['time']), subj: {for (final e in ((b['subj'] as Map?) ?? {}).entries) '${e.key}': dnum(e.value)}),
        ],
      );
}

final _lbMem = <String, LbInfo>{};

/// Leaderboard rows read for a rank (the top of the board). Bigger boards use count / average queries for the rest.
const _lbRows = 100;

/// Puts a finished attempt on the leaderboard when its row is missing (a submit whose leaderboard write failed).
Future<bool> _restoreRow(String key, String uid, Att a) async {
  try {
    var name = '';
    try {
      final ud = (await FirebaseFirestore.instance.collection('users').doc(uid).get()).data() ?? {};
      name = s(ud['name'] ?? ud['displayName']).trim();
    } catch (_) {}
    final c = inum(a['correct']), w = inum(a['wrong']);
    await FirebaseFirestore.instance.collection('leaderboards').doc(key).collection('scores').doc(uid).set({
      'uid': uid,
      'name': name.isEmpty ? 'Student' : name,
      'paperId': key,
      'paperName': testName(a),
      'marks': marksOf(a),
      'maxMarks': maxOf(a),
      'accuracy': c + w == 0 ? 0 : (c / (c + w) * 100).round(),
      'subjectMarks': a['subjectMarks'] is Map && !isChapter(a) ? a['subjectMarks'] : <String, dynamic>{},
      'timeUsed': inum(a['timeUsed']),
      'submittedAt': FieldValue.serverTimestamp(),
    });
    return true;
  } catch (_) {
    return false;
  }
}

/// True for an attempt of an All India Challenge paper; [aicLiveAtt]: the live Sunday attempt.
bool isAicAtt(Att a) => aicRoundOf(s(a['mockId'])) > 0;
bool aicLiveAtt(Att a) => a['aic'] is Map && (a['aic'] as Map)['live'] == true;

/// All India Rank of a challenge round. The board holds the live attempts only: a live attempt is ranked by
/// its own row; a free mock is shown where its score would have stood among the live students (no row is written).
/// Rank = students with more marks + 1. Section ranks the same way. Closed until the result time.
Future<LbInfo> _aicRank(String key, String uid, Att? from) async {
  if (aicBoardClosed(key, AicClock.now)) return LbInfo(none: true);
  final live = from == null || aicLiveAtt(from);
  final mk = '$key|${live ? 'live' : s(from!['id'])}';
  if (_lbMem[mk] != null) return _lbMem[mk]!;
  try {
    final col = FirebaseFirestore.instance.collection('leaderboards').doc(key).collection('scores');
    double my;
    double max;
    Map sm;
    if (live) {
      final me = await col.doc(uid).get();
      if (!me.exists && from == null) return LbInfo(none: true);
      final md = me.data() ?? const <String, dynamic>{};
      my = me.exists ? dnum(md['marks']) : marksOf(from!);
      max = me.exists ? dnum(md['maxMarks']) : maxOf(from!);
      sm = (me.exists ? md['subjectMarks'] : from!['subjectMarks']) as Map? ?? {};
    } else {
      my = marksOf(from!);
      max = maxOf(from!);
      sm = (from!['subjectMarks'] as Map?) ?? {};
    }
    final res = await Future.wait([
      col.orderBy('marks', descending: true).limit(_lbRows).get(),
      col.aggregate(count(), average('marks')).get(),
      col.where('marks', isGreaterThan: my).count().get(),
      col.where('timeUsed', isGreaterThan: 0).aggregate(average('timeUsed')).get(),
    ]);
    final rows = [for (final d in (res[0] as QuerySnapshot<Map<String, dynamic>>).docs) d.data()];
    final ag = res[1] as AggregateQuerySnapshot;
    final total = ag.count ?? rows.length;
    final ahead = (res[2] as AggregateQuerySnapshot).count ?? 0;
    final subj = <String, ({double my, int ahead, double avg, int n})>{};
    for (final e in sm.entries) {
      final k = '${e.key}';
      final mine = dnum(e.value);
      final have = rows.where((r) => r['subjectMarks'] is Map && (r['subjectMarks'] as Map).containsKey(k)).toList();
      var sAhead = have.where((r) => dnum((r['subjectMarks'] as Map)[k]) > mine).length;
      if (total > rows.length) {
        // a big board: count the students ahead in this section on the server
        try {
          sAhead = (await col.where(FieldPath(['subjectMarks', k]), isGreaterThan: mine).count().get()).count ?? sAhead;
        } catch (_) {}
      }
      subj[k] = (my: mine, ahead: sAhead, avg: have.isEmpty ? 0.0 : have.fold(0.0, (x, r) => x + dnum((r['subjectMarks'] as Map)[k])) / have.length, n: total);
    }
    final bands = <({String label, double marks, double time, Map<String, double> subj})>[];
    if (total >= 8 && rows.isNotEmpty) {
      for (final b in const [('Top 10%', .10), ('Top 25%', .25)]) {
        final n = (total * b.$2).ceil().clamp(1, rows.length);
        final g = rows.take(n).toList();
        final tg = g.where((r) => dnum(r['timeUsed']) > 0).toList();
        final sj = <String, List<double>>{};
        for (final r in g) {
          if (r['subjectMarks'] is! Map) continue;
          (r['subjectMarks'] as Map).forEach((k, v) => (sj['$k'] ??= [0, 0])..[0] += dnum(v)..[1] += 1);
        }
        bands.add((
          label: b.$1,
          marks: g.fold(0.0, (x, r) => x + dnum(r['marks'])) / g.length,
          time: tg.isEmpty ? 0.0 : tg.fold(0.0, (x, r) => x + dnum(r['timeUsed'])) / tg.length,
          subj: {for (final e in sj.entries) e.key: e.value[0] / e.value[1]},
        ));
      }
    }
    final t = rows.isEmpty ? <String, dynamic>{} : rows.first;
    return _lbMem[mk] = LbInfo(
      bands: bands,
      my: my, max: max, total: total, ahead: ahead, avg: ag.getAverage('marks') ?? 0,
      tAvg: (res[3] as AggregateQuerySnapshot).getAverage('timeUsed') ?? 0,
      top: dnum(t['marks']), topName: s(t['name']), topAcc: t['accuracy'] == null ? null : dnum(t['accuracy']), topTime: dnum(t['timeUsed']),
      topSubj: {for (final e in ((t['subjectMarks'] as Map?) ?? {}).entries) '${e.key}': dnum(e.value)}, subj: subj,
    );
  } catch (_) {
    return LbInfo(err: true);
  }
}

Future<LbInfo> fetchRank(String key, String uid, {Att? from, bool fresh = false}) async {
  if (aicRoundOf(key) > 0) return _aicRank(key, uid, from); // All India Challenge: live attempts only, never restored
  if (!fresh && _lbMem[key] != null) return _lbMem[key]!;
  final prefs = await SharedPreferences.getInstance();
  if (!fresh) try {
    final c = jsonDecode(prefs.getString('tssc_dp_lb2_$key') ?? 'null');
    if (c is Map && DateTime.now().millisecondsSinceEpoch - inum(c['ts']) < 6 * 3600 * 1000) return _lbMem[key] = LbInfo.fromJson(c['v'] as Map);
  } catch (_) {}
  try {
    final col = FirebaseFirestore.instance.collection('leaderboards').doc(key).collection('scores');
    final res = await Future.wait([col.doc(uid).get(), col.orderBy('marks', descending: true).limit(_lbRows).get()]);
    final me = res[0] as DocumentSnapshot<Map<String, dynamic>>;
    final board = res[1] as QuerySnapshot<Map<String, dynamic>>;
    if (!me.exists) {
      if (from != null && lbKeyOf(from) == key && await _restoreRow(key, uid, from)) return fetchRank(key, uid);
      return LbInfo(none: true);
    }
    final md = me.data()!;
    final my = dnum(md['marks']);
    final rows = [for (final d in board.docs) d.data()];
    var ahead = rows.where((r) => dnum(r['marks']) > my).length;
    var total = rows.length > ahead + 1 ? rows.length : ahead + 1;
    var avg = rows.isEmpty ? 0.0 : rows.fold(0.0, (x, r) => x + dnum(r['marks'])) / rows.length;
    final tRows = rows.where((r) => dnum(r['timeUsed']) > 0).toList();
    var tAvg = tRows.isEmpty ? 0.0 : tRows.fold(0.0, (x, r) => x + dnum(r['timeUsed'])) / tRows.length;
    final big = rows.length >= _lbRows; // more students than the rows read: totals come from count / average queries
    if (big) {
      try {
        final ag = await Future.wait([
          col.aggregate(count(), average('marks')).get(),
          col.where('marks', isGreaterThan: my).count().get(),
          col.where('timeUsed', isGreaterThan: 0).aggregate(average('timeUsed')).get(),
        ]);
        total = ag[0].count ?? total;
        avg = ag[0].getAverage('marks') ?? avg;
        ahead = ag[1].count ?? ahead;
        tAvg = ag[2].getAverage('timeUsed') ?? tAvg;
      } catch (_) {}
    }
    final t = rows.isEmpty ? <String, dynamic>{} : rows.first;
    final sm = (md['subjectMarks'] as Map?) ?? {};
    final subj = <String, ({double my, int ahead, double avg, int n})>{};
    if (!big) sm.forEach((k, v) {
      final mine = dnum(v);
      final have = rows.where((r) => r['subjectMarks'] is Map && (r['subjectMarks'] as Map).containsKey(k)).toList();
      subj['$k'] = (
        my: mine,
        ahead: have.where((r) => dnum((r['subjectMarks'] as Map)[k]) > mine).length,
        avg: have.isEmpty ? 0.0 : have.fold(0.0, (x, r) => x + dnum((r['subjectMarks'] as Map)[k])) / have.length,
        n: have.length,
      );
    });
    // top 10% / top 25% averages (the board is read best-first, up to 300 rows)
    final bands = <({String label, double marks, double time, Map<String, double> subj})>[];
    if (total >= 8) {
      for (final b in const [('Top 10%', .10), ('Top 25%', .25)]) {
        final n = (total * b.$2).ceil().clamp(1, rows.length);
        final g = rows.take(n).toList();
        final tg = g.where((r) => dnum(r['timeUsed']) > 0).toList();
        final sj = <String, List<double>>{};
        for (final r in g) {
          if (r['subjectMarks'] is! Map) continue;
          (r['subjectMarks'] as Map).forEach((k, v) => (sj['$k'] ??= [0, 0])..[0] += dnum(v)..[1] += 1);
        }
        bands.add((
          label: b.$1,
          marks: g.fold(0.0, (x, r) => x + dnum(r['marks'])) / g.length,
          time: tg.isEmpty ? 0.0 : tg.fold(0.0, (x, r) => x + dnum(r['timeUsed'])) / tg.length,
          subj: {for (final e in sj.entries) e.key: e.value[0] / e.value[1]},
        ));
      }
    }
    final v = LbInfo(
      bands: bands,
      my: my, max: dnum(md['maxMarks']), total: total, ahead: ahead, avg: avg, tAvg: tAvg, top: dnum(t['marks']), topName: s(t['name']),
      topAcc: t['accuracy'] == null ? null : dnum(t['accuracy']), topTime: dnum(t['timeUsed']),
      topSubj: {for (final e in ((t['subjectMarks'] as Map?) ?? {}).entries) '${e.key}': dnum(e.value)}, subj: subj,
    );
    _lbMem[key] = v;
    await prefs.setString('tssc_dp_lb2_$key', jsonEncode({'ts': DateTime.now().millisecondsSinceEpoch, 'v': v.toJson()}));
    return v;
  } catch (_) {
    return LbInfo(err: true);
  }
}

// ---------------------------------------------------------------- question stats + text

final _qsMem = <String, Map<String, dynamic>>{};
Future<Map<String, dynamic>> loadQstats(String key) async {
  if (key.isEmpty) return {};
  if (_qsMem[key] != null) return _qsMem[key]!;
  try {
    final d = await FirebaseFirestore.instance.collection('qstats').doc(key).get();
    return _qsMem[key] = d.data() ?? {};
  } catch (_) {
    return {};
  }
}

String plainText(String t) {
  var x = t;
  x = x.replaceAll(RegExp(r'\\[\(\)\[\]]'), ' ').replaceAll(RegExp(r'\$\$?'), ' ');
  for (var i = 0; i < 3; i++) {
    x = x.replaceAllMapped(RegExp(r'\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}'), (m) => '${m[1]}/${m[2]}');
  }
  x = x.replaceAllMapped(RegExp(r'\\sqrt\s*\{([^{}]*)\}'), (m) => '√${m[1]}');
  x = x.replaceAllMapped(RegExp(r'\\(?:text|mathrm|mathbf|operatorname)\s*\{([^{}]*)\}'), (m) => m[1]!);
  x = x.replaceAll(RegExp(r'\^\s*\{?\\circ\}?'), '°');
  const sym = {'times': '×', 'div': '÷', 'cdot': '·', 'pm': '±', 'le': '≤', 'leq': '≤', 'ge': '≥', 'geq': '≥', 'ne': '≠', 'theta': 'θ', 'alpha': 'α', 'beta': 'β', 'pi': 'π', 'angle': '∠', 'triangle': '△'};
  x = x.replaceAllMapped(RegExp(r'\\([A-Za-z]+)'), (m) => sym[m[1]] ?? m[1]!);
  x = x.replaceAll(RegExp(r'\[FIGURE-BASED\]\s*', caseSensitive: false), '').replaceAll(RegExp(r'\[BR\]|\|\|'), ' ');
  x = x.replaceAll(RegExp(r'<[^>]*>?'), ' ').replaceAll('&nbsp;', ' ').replaceAll('&amp;', '&').replaceAll(RegExp(r'[{}]'), '');
  return x.replaceAll(RegExp(r'\s+'), ' ').trim();
}

final _qtMem = <String, Map<int, ({String t, String c})>>{};
Future<Map<int, ({String t, String c})>> loadQtext(Att a) async {
  final col = FirebaseFirestore.instance.collection('questions');
  String id;
  Future<QuerySnapshot<Map<String, dynamic>>> Function() q;
  if (a['type'] == 'pyq-chapter') return {};
  if (isChapter(a)) {
    final cid = s(a['chapterId'] ?? a['chapter']);
    final lv = inum(a['level']) == 0 ? 1 : inum(a['level']), tn = inum(a['testNum']) == 0 ? 1 : inum(a['testNum']);
    id = 'cw|$cid|$lv|$tn|${a['language']}';
    q = () async {
      var sn = await col.where('chapterId', isEqualTo: cid).where('level', isEqualTo: lv).where('testNum', isEqualTo: tn).get();
      if (sn.docs.isEmpty) sn = await col.where('chapterId', isEqualTo: cid).where('level', isEqualTo: '$lv').where('testNum', isEqualTo: '$tn').get();
      return sn;
    };
  } else {
    final mid = s(a['mockId']), pid = s(a['paperId']);
    id = pid.isNotEmpty ? pid : mid;
    if (id.isEmpty) return {};
    final base = id.contains('__') ? id.substring(0, id.indexOf('__')) : id;
    final field = pid.isEmpty ? 'mockId' : 'paperId';
    q = () => col.where(field, isEqualTo: s(a['testKind']) == 'mock-subject' ? (s(a['baseMockId']).isNotEmpty ? s(a['baseMockId']) : base) : base).get();
  }
  if (_qtMem[id] != null) return _qtMem[id]!;
  try {
    final sn = await q();
    final lang = a['language'] == 'hi' ? 'hi' : 'en';
    var docs = [for (final d in sn.docs) d.data()];
    if (isChapter(a)) {
      final f = docs.where((d) => (s(d['language'] ?? d['lang']) == 'hi' ? 'hi' : 'en') == lang).toList();
      if (f.isNotEmpty) docs = f;
    }
    final m = <int, ({String t, String c})>{};
    for (final d in docs) {
      final n = int.tryParse(s(d['qNum'] ?? d['number']).replaceAll(RegExp(r'\D'), '')) ?? 0;
      if (n == 0) continue;
      var t = plainText(s(d['text'] ?? d['question'] ?? d['questionText']));
      if (t.length > 110) t = '${t.substring(0, 110)}…';
      m[n] = (t: t, c: s(d['correct']));
    }
    return _qtMem[id] = m;
  } catch (_) {
    return {};
  }
}

/// Stable 0..1 value per key (website TSSC-ESTSEED-V1, FNV-1a + mix).
double seed01(String str) {
  var x = 2166136261;
  for (final c in str.codeUnits) {
    x ^= c;
    x = (x * 16777619) & 0xFFFFFFFF;
  }
  x ^= x >> 13;
  x = (x * 0x5bd1e995) & 0xFFFFFFFF;
  x ^= x >> 15;
  return (x % 10007) / 10007;
}
