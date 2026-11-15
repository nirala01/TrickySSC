// Dashboard analysis — a port of the website dashboard (dashboard.html, TSSC-DASHPRO-V1 / DASHSCOPE-V1).
// Works on the attempt maps from Firestore `attempts`.
import 'dart:convert';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:shared_preferences/shared_preferences.dart';

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
bool isTier2(Att a) => a['tier'] == 'tier2' || RegExp(r'tier2|tier-2|tier_2', caseSensitive: false).hasMatch(s(a['paperId']) + s(a['mockId']));

({double pos, double neg}) posneg(Att a) {
  final e = s(a['exam']);
  if (e == 'ssc-mts') return (pos: 3.0, neg: 1.0);
  if (e == 'rrb-ntpc') return (pos: 1.0, neg: 1 / 3);
  if (e == 'ssc-gd') return (pos: 2.0, neg: 0.25);
  if (isTier2(a)) return (pos: 3.0, neg: 1.0);
  return (pos: 2.0, neg: 0.5);
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
  final id = s(a['mockId']);
  final m = RegExp(r'^([a-z-]+)_.*_(tier\d|cbt\d)_mock(\d+)_(en|hi)(?:__([a-z]+))?$').firstMatch(id);
  if (m != null) {
    final ex = examById(m.group(1)!)?.name ?? '';
    final sub = s(a['subjectKey']).isNotEmpty ? ' · ${_subjName(s(a['subjectKey']))}' : '';
    return '$ex ${m.group(2) == 'tier2' ? 'Tier 2 ' : ''}Mock ${m.group(3)}$sub';
  }
  final n = s(a['examName']).replaceAll(RegExp(r'\s*—.*$'), '').trim();
  return n.isEmpty ? 'Test' : n;
}

String _subjName(String k) => const {'quant': 'Maths', 'maths': 'Maths', 'reasoning': 'Reasoning', 'english': 'English', 'gk': 'GK', 'ga': 'GK', 'computer': 'Computer'}[k.toLowerCase()] ?? k;

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
  final tier = (p[1] == 'ssc-cgl' || p[1] == 'ssc-chsl') ? (p[2] == 'tier2' ? ' Tier II' : ' Tier I') : '';
  if (p[0] == 'subj') return '$ex$tier · ${_subjName(p[3])} tests';
  return '$ex$tier · Full tests';
}

// ---------------------------------------------------------------- per-attempt analysis

List<Map<String, dynamic>> answersOf(Att a) => [
      if (a['answers'] is List)
        for (final x in a['answers'] as List)
          if (x is Map) Map<String, dynamic>.from(x)
    ];

class ChStat {
  final String name;
  int n = 0, c = 0, w = 0, k = 0;
  ChStat(this.name);
  double get acc => n == 0 ? 0 : c / n;
}

List<ChStat> chapterStats(List<Att> list) {
  final m = <String, ChStat>{};
  for (final a in list) {
    for (final x in answersOf(a)) {
      final raw = s(x['ch']).replaceAll(RegExp(r'<[^>]*>'), ' ').replaceAll(RegExp(r'\s+'), ' ').trim();
      final name = raw.isEmpty ? 'Untagged' : (raw.length > 40 ? raw.substring(0, 40) : raw);
      final st = m.putIfAbsent(name, () => ChStat(name));
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
  return m.values.toList();
}

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
  LbInfo({this.none = false, this.err = false, this.my = 0, this.max = 0, this.avg = 0, this.tAvg = 0, this.top = 0, this.total = 0, this.ahead = 0, this.topName = '', this.topAcc, this.topTime = 0, this.topSubj = const {}, this.subj = const {}});
  int get rank => ahead + 1;
  double get pctile => total == 0 ? 0 : ((1 - ahead / total) * 1000).round() / 10;
  bool get ok => !none && !err;

  Map<String, dynamic> toJson() => {
        'none': none, 'err': err, 'my': my, 'max': max, 'avg': avg, 'tAvg': tAvg, 'top': top, 'total': total, 'ahead': ahead,
        'topName': topName, 'topAcc': topAcc, 'topTime': topTime, 'topSubj': topSubj,
        'subj': {for (final e in subj.entries) e.key: {'my': e.value.my, 'ahead': e.value.ahead, 'avg': e.value.avg, 'n': e.value.n}},
      };
  factory LbInfo.fromJson(Map j) => LbInfo(
        none: j['none'] == true, err: j['err'] == true, my: dnum(j['my']), max: dnum(j['max']), avg: dnum(j['avg']), tAvg: dnum(j['tAvg']), top: dnum(j['top']),
        total: inum(j['total']), ahead: inum(j['ahead']), topName: s(j['topName']), topAcc: j['topAcc'] == null ? null : dnum(j['topAcc']), topTime: dnum(j['topTime']),
        topSubj: {for (final e in ((j['topSubj'] as Map?) ?? {}).entries) '${e.key}': dnum(e.value)},
        subj: {for (final e in ((j['subj'] as Map?) ?? {}).entries) '${e.key}': (my: dnum(e.value['my']), ahead: inum(e.value['ahead']), avg: dnum(e.value['avg']), n: inum(e.value['n']))},
      );
}

final _lbMem = <String, LbInfo>{};

Future<LbInfo> fetchRank(String key, String uid) async {
  if (_lbMem[key] != null) return _lbMem[key]!;
  final prefs = await SharedPreferences.getInstance();
  try {
    final c = jsonDecode(prefs.getString('tssc_dp_lb_$key') ?? 'null');
    if (c is Map && DateTime.now().millisecondsSinceEpoch - inum(c['ts']) < 6 * 3600 * 1000) return _lbMem[key] = LbInfo.fromJson(c['v'] as Map);
  } catch (_) {}
  try {
    final col = FirebaseFirestore.instance.collection('leaderboards').doc(key).collection('scores');
    final res = await Future.wait([col.doc(uid).get(), col.orderBy('marks', descending: true).limit(300).get()]);
    final me = res[0] as DocumentSnapshot<Map<String, dynamic>>;
    final board = res[1] as QuerySnapshot<Map<String, dynamic>>;
    if (!me.exists) return _lbMem[key] = LbInfo(none: true);
    final md = me.data()!;
    final my = dnum(md['marks']);
    final rows = [for (final d in board.docs) d.data()];
    var ahead = rows.where((r) => dnum(r['marks']) > my).length;
    var total = rows.length > ahead + 1 ? rows.length : ahead + 1;
    if (rows.length >= 300) {
      try {
        total = (await col.count().get()).count ?? total;
        ahead = (await col.where('marks', isGreaterThan: my).count().get()).count ?? ahead;
      } catch (_) {}
    }
    final avg = rows.isEmpty ? 0.0 : rows.fold(0.0, (x, r) => x + dnum(r['marks'])) / rows.length;
    final tRows = rows.where((r) => dnum(r['timeUsed']) > 0).toList();
    final tAvg = tRows.isEmpty ? 0.0 : tRows.fold(0.0, (x, r) => x + dnum(r['timeUsed'])) / tRows.length;
    final t = rows.isEmpty ? <String, dynamic>{} : rows.first;
    final sm = (md['subjectMarks'] as Map?) ?? {};
    final subj = <String, ({double my, int ahead, double avg, int n})>{};
    sm.forEach((k, v) {
      final mine = dnum(v);
      final have = rows.where((r) => r['subjectMarks'] is Map && (r['subjectMarks'] as Map).containsKey(k)).toList();
      subj['$k'] = (
        my: mine,
        ahead: have.where((r) => dnum((r['subjectMarks'] as Map)[k]) > mine).length,
        avg: have.isEmpty ? 0.0 : have.fold(0.0, (x, r) => x + dnum((r['subjectMarks'] as Map)[k])) / have.length,
        n: have.length,
      );
    });
    final v = LbInfo(
      my: my, max: dnum(md['maxMarks']), total: total, ahead: ahead, avg: avg, tAvg: tAvg, top: dnum(t['marks']), topName: s(t['name']),
      topAcc: t['accuracy'] == null ? null : dnum(t['accuracy']), topTime: dnum(t['timeUsed']),
      topSubj: {for (final e in ((t['subjectMarks'] as Map?) ?? {}).entries) '${e.key}': dnum(e.value)}, subj: subj,
    );
    _lbMem[key] = v;
    await prefs.setString('tssc_dp_lb_$key', jsonEncode({'ts': DateTime.now().millisecondsSinceEpoch, 'v': v.toJson()}));
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
