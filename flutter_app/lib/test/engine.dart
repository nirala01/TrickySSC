// The test engine: the same rules as the website's mock-test.html (Tier 1 mocks of
// SSC CGL, CHSL, GD, MTS and RRB NTPC). Marks, sections, timers, the saved attempt,
// the leaderboard row and the daily limit all follow that page, so a result saved
// from the app looks exactly like one saved from the website.
import 'dart:convert';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../data.dart';

const Map<String, String> subjectShort = {
  'General Intelligence & Reasoning': 'Reasoning',
  'General Intelligence and Reasoning': 'Reasoning',
  'Quantitative Aptitude': 'Quant',
  'General Awareness': 'Gen. Awareness',
  'English Language': 'English',
  'Hindi Language': 'Hindi',
  'Numerical and Mathematical Ability': 'Quant',
  'Reasoning Ability and Problem Solving': 'Reasoning',
  'English Language and Comprehension': 'English',
  'हिंदी भाषा': 'Hindi',
  'English': 'English',
  'reasoning': 'Reasoning',
  'quant': 'Quant',
  'gk': 'Gen. Awareness',
  'english': 'English',
  'सामान्य बुद्धि एवं तर्कशक्ति': 'Reasoning',
  'सामान्य जागरूकता': 'Gen. Awareness',
  'मात्रात्मक योग्यता': 'Quant',
  'अंग्रेजी भाषा': 'English',
  'सामान्य बुद्धि और तर्क शक्ति': 'Reasoning',
  'सामान्य बुद्धि': 'Reasoning',
};

String canonSubject(String? raw) {
  final s = (raw ?? '').replaceAll(RegExp(r'\s+'), ' ').trim();
  if (s.isEmpty) return '';
  final known = subjectShort[s];
  if (known != null) return known;
  final low = s.toLowerCase();
  if (RegExp(r'\benglish\b|comprehension').hasMatch(low)) return 'English';
  if (RegExp(r'quant|aptitude|numerical|\bmath').hasMatch(low)) return 'Quant';
  if (RegExp(r'aware|general studies|\bg\.?k\.?\b|current affairs').hasMatch(low)) return 'Gen. Awareness';
  if (RegExp(r'reason|intelligence|mental ability').hasMatch(low)) return 'Reasoning';
  if (s.contains('अंग्रे')) return 'English';
  if (RegExp(r'मात्रात्मक|संख्यात्मक|गणित|अंकगण').hasMatch(s)) return 'Quant';
  if (RegExp(r'जागरूक|अध्ययन|सामान्य ज्ञान|करंट|समसामयिक').hasMatch(s)) return 'Gen. Awareness';
  if (RegExp(r'बुद्धि|तर्क|रीजनिंग').hasMatch(s)) return 'Reasoning';
  return s;
}

String _str(dynamic v) => v == null ? '' : '$v';

class Question {
  final Map<String, dynamic> raw;
  Question(this.raw);

  int qNumOr(int fallback) => int.tryParse(_str(raw['qNum']).trim()) ?? fallback;
  int get qNum => int.tryParse(_str(raw['qNum']).trim()) ?? 0;
  String get text => _str(raw['text']).isNotEmpty ? _str(raw['text']) : _str(raw['question']);
  String get correct => _str(raw['correct']).trim().toUpperCase();
  String get subjectRaw => _str(raw['subject']).isNotEmpty ? _str(raw['subject']) : _str(raw['section']);
  String get imageUrl => _str(raw['imageUrl']);
  String get explanation => _str(raw['explanation']);
  String get trick => _str(raw['trick']);
  String get concept => _str(raw['concept']);
  String get solutionImage => _str(raw['solutionImage']);
  String get difficulty => _str(raw['difficulty']).trim().toLowerCase();
  String get chapter => _str(raw['chapter']).isNotEmpty ? _str(raw['chapter']) : _str(raw['concept']);

  List<String> get keys {
    final out = <String>[];
    for (final k in const ['A', 'B', 'C', 'D', 'E']) {
      if (k == 'E' && option(k).isEmpty && optionImage(k).isEmpty) continue;
      out.add(k);
    }
    return out;
  }

  String option(String k) {
    final o = raw['options'];
    if (o is Map) {
      final v = o[k] ?? o[k.toLowerCase()];
      if (v != null && '$v'.isNotEmpty) return '$v';
    }
    for (final f in ['option_$k', 'option$k']) {
      if (_str(raw[f]).isNotEmpty) return _str(raw[f]);
    }
    return '';
  }

  String optionImage(String k) {
    final o = raw['optionImages'];
    if (o is Map) return _str(o[k] ?? o[k.toLowerCase()]);
    return '';
  }
}

/// A timed unit: a section (CGL, CHSL, GD: 15 min each), an MTS session (45 min) or
/// the whole NTPC paper (90 min).
class Unit {
  final String label;
  final int from;
  final int to;
  Unit(this.label, this.from, this.to);
}

class Section {
  final String label;
  final int from;
  int to;
  Section(this.label, this.from, this.to);
}

class Rules {
  final String mockId;
  final bool mts;
  final bool ntpc;
  final bool gd;
  Rules(this.mockId)
      : mts = mockId.startsWith('ssc-mts_'),
        ntpc = mockId.startsWith('rrb-ntpc_'),
        gd = mockId.startsWith('ssc-gd_');

  double get pos => ntpc ? 1 : (mts ? 3 : 2);
  double get negBase => ntpc ? 1 / 3 : (mts ? 1 : (gd ? 0.25 : 0.5));
  double neg(Question q, int i) => !mts ? negBase : (q.qNumOr(i + 1) > 40 ? 1 : 0);
  int get unitSeconds => ntpc ? 90 * 60 : (mts ? 45 * 60 : 15 * 60);

  String markingLine() {
    if (mts) return '+3 for a correct answer · −1 in Session II only (no negative in Session I)';
    if (ntpc) return '+1 for a correct answer · −1/3 for a wrong answer';
    if (gd) return '+2 for a correct answer · −0.25 for a wrong answer';
    return '+2 for a correct answer · −0.50 for a wrong answer';
  }

  String timingLine(int units) {
    if (ntpc) return 'One paper on a single 90-minute clock.';
    if (mts) return 'Two sessions of 45 minutes each. Session I (Maths, Reasoning), then Session II (GA, English).';
    return '$units sections of 15 minutes each. When a section ends it is submitted and the next one opens.';
  }

  /// The subject key used for subject-wise stats, as the website computes it.
  String statKey(Question q) {
    if (mts || ntpc) {
      final c = canonSubject(q.subjectRaw);
      return c.isEmpty ? 'General' : c;
    }
    final t = q.subjectRaw.trim();
    return subjectShort[t] ?? (t.isEmpty ? 'General' : t);
  }
}

class Paper {
  final Rules rules;
  final List<Question> questions;
  final List<Section> sections;
  final List<Unit> units;
  final String title;
  final String partD; // GD only: 'en' / 'hi' / ''
  Paper(this.rules, this.questions, this.sections, this.units, this.title, this.partD);
}

/// Previous-year papers are keyed by paperId (ssc-cgl_2026_tier1_shift-1_2026-10-13_en), mocks by mockId.
bool isPyqId(String id) => !RegExp(r'_mock\d+_').hasMatch(id);

Future<List<Question>> _fetch(String mockId) async {
  final snap = await FirebaseFirestore.instance.collection('questions').where(isPyqId(mockId) ? 'paperId' : 'mockId', isEqualTo: mockId).get();
  final list = [for (final d in snap.docs) Question({'id': d.id, ...d.data()})];
  list.sort((a, b) => a.qNum.compareTo(b.qNum));
  return list;
}

String twinId(String mockId, String lang) =>
    mockId.replaceFirstMapped(RegExp(r'([_-])(en|hi|english|hindi)$', caseSensitive: false), (m) {
      final long = m[2]!.length > 2;
      return '${m[1]}${lang == 'hi' ? (long ? 'hindi' : 'hi') : (long ? 'english' : 'en')}';
    });

/// Loads a mock and builds its sections and timed units.
/// [partD] (GD only): take Q61-80 from the other-language paper when it differs from [lang].
Future<Paper> loadPaper(String mockId, String lang, {String? partD, String title = ''}) async {
  final rules = Rules(mockId);
  var qs = await _fetch(mockId);
  if (qs.isEmpty) throw 'This paper has no questions yet.';
  var pd = '';
  if (rules.gd) {
    pd = lang;
    if (partD != null && partD != lang) {
      try {
        final twin = (await _fetch(twinId(mockId, partD))).where((q) => q.qNum >= 61 && q.qNum <= 80).toList();
        if (twin.length == 20) {
          qs = [...qs.where((q) => q.qNum < 61 || q.qNum > 80), ...twin]..sort((a, b) => a.qNum.compareTo(b.qNum));
          pd = partD;
        }
      } catch (_) {}
    }
  }
  if (title.isEmpty && !isPyqId(mockId)) {
    try {
      final meta = await FirebaseFirestore.instance.collection('mock_tests').doc(mockId).get();
      title = _str((meta.data() ?? const {})['title']);
    } catch (_) {}
  }

  // sections: consecutive questions of one subject
  final sections = <Section>[];
  String? prev;
  for (var i = 0; i < qs.length; i++) {
    final subj = canonSubject(qs[i].subjectRaw);
    if (subj != prev) {
      if (sections.isNotEmpty) sections.last.to = i - 1;
      sections.add(Section(subjectShort[subj] ?? (subj.isEmpty ? 'Part ${sections.length + 1}' : subj), i, qs.length - 1));
      prev = subj;
    }
  }
  if (sections.isEmpty) sections.add(Section('All Questions', 0, qs.length - 1));

  final units = <Unit>[];
  if (rules.mts) {
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].label == 'Quant') sections[i] = Section('Maths', sections[i].from, sections[i].to);
    }
    var cut = -1;
    for (var i = 0; i < qs.length; i++) {
      if (qs[i].qNumOr(i + 1) > 40) {
        cut = i;
        break;
      }
    }
    if (cut < 0) cut = qs.length < 40 ? qs.length : 40;
    if (cut > 0) units.add(Unit('Session I', 0, cut - 1));
    if (cut < qs.length) units.add(Unit('Session II', cut, qs.length - 1));
  } else if (rules.ntpc) {
    sections
      ..clear()
      ..add(Section('All Questions', 0, qs.length - 1));
    units.add(Unit('RRB NTPC Paper', 0, qs.length - 1));
  } else {
    for (final s in sections) {
      units.add(Unit(s.label, s.from, s.to));
    }
  }
  return Paper(rules, qs, sections, units, title, pd);
}

/// English version of each question of a Hindi paper, by question number (for "View in English").
Future<Map<int, Question>> loadEnglishTwin(String mockId) async {
  final out = <int, Question>{};
  try {
    for (final q in await _fetch(twinId(mockId, 'en'))) {
      out[q.qNum] = q;
    }
  } catch (_) {}
  return out;
}

// ---------------------------------------------------------------- saved progress

class Progress {
  Map<int, String> answers = {};
  Set<int> marked = {};
  Set<int> visited = {0};
  Map<int, int> qMs = {}; // time spent per question
  int unit = 0;
  int current = 0;
  List<int> remaining = [];

  Map<String, dynamic> toJson() => {
        'a': answers.map((k, v) => MapEntry('$k', v)),
        'm': marked.toList(),
        'v': visited.toList(),
        't': qMs.map((k, v) => MapEntry('$k', v)),
        'u': unit,
        'c': current,
        'r': remaining,
        'at': DateTime.now().millisecondsSinceEpoch,
      };

  static Progress fromJson(Map<String, dynamic> j) {
    final p = Progress();
    (j['a'] as Map? ?? {}).forEach((k, v) => p.answers[int.parse('$k')] = '$v');
    p.marked = {for (final x in (j['m'] as List? ?? [])) (x as num).toInt()};
    p.visited = {for (final x in (j['v'] as List? ?? [0])) (x as num).toInt()};
    (j['t'] as Map? ?? {}).forEach((k, v) => p.qMs[int.parse('$k')] = (v as num).toInt());
    p.unit = (j['u'] as num? ?? 0).toInt();
    p.current = (j['c'] as num? ?? 0).toInt();
    p.remaining = [for (final x in (j['r'] as List? ?? [])) (x as num).toInt()];
    return p;
  }
}

String _progressKey(String uid, String mockId, String partD) => 'tssc_prog_${uid}_${mockId}_$partD';

Future<Progress?> loadProgress(String uid, String mockId, String partD) async {
  try {
    final s = (await SharedPreferences.getInstance()).getString(_progressKey(uid, mockId, partD));
    if (s == null) return null;
    final j = jsonDecode(s) as Map<String, dynamic>;
    final at = (j['at'] as num? ?? 0).toInt();
    if (DateTime.now().millisecondsSinceEpoch - at > 3 * 24 * 3600 * 1000) return null;
    return Progress.fromJson(j);
  } catch (_) {
    return null;
  }
}

Future<void> saveProgress(String uid, String mockId, String partD, Progress p) async {
  try {
    await (await SharedPreferences.getInstance()).setString(_progressKey(uid, mockId, partD), jsonEncode(p.toJson()));
  } catch (_) {}
}

/// Unfinished tests on this phone: base id (no language) → [lang, partD].
Future<Map<String, List<String>>> loadInProgress(String uid) async {
  final out = <String, List<String>>{};
  try {
    final prefs = await SharedPreferences.getInstance();
    final pre = 'tssc_prog_${uid}_';
    final now = DateTime.now().millisecondsSinceEpoch;
    for (final k in prefs.getKeys()) {
      if (!k.startsWith(pre)) continue;
      try {
        final j = jsonDecode(prefs.getString(k) ?? '') as Map<String, dynamic>;
        final at = (j['at'] as num? ?? 0).toInt();
        if (now - at > 3 * 24 * 3600 * 1000) {
          await prefs.remove(k);
          continue;
        }
        final rest = k.substring(pre.length);
        final cut = rest.lastIndexOf('_');
        final mockId = rest.substring(0, cut), partD = rest.substring(cut + 1);
        final lc = mockId.lastIndexOf('_');
        final lang = mockId.substring(lc + 1);
        if (lang != 'en' && lang != 'hi') continue;
        out[mockId.substring(0, lc)] = [lang, partD];
      } catch (_) {}
    }
  } catch (_) {}
  return out;
}

Future<void> clearProgress(String uid, String mockId, String partD) async {
  try {
    await (await SharedPreferences.getInstance()).remove(_progressKey(uid, mockId, partD));
  } catch (_) {}
}

// ---------------------------------------------------------------- daily limit

const int freeLimit = 15;
const int paidLimit = 80;
const List<String> _admins = ['nirala01@gmail.com', 'ashish@trickyssc.com'];

String _todayIst() => DateTime.now().toUtc().add(const Duration(hours: 5, minutes: 30)).toIso8601String().substring(0, 10);

bool _isAdmin(User u) {
  final e = (u.email ?? '').toLowerCase();
  return e.isNotEmpty && (_admins.contains(e) || e.endsWith('@trickyssc.com'));
}

Future<int> _usedToday(String uid) async {
  final s = await FirebaseFirestore.instance.collection('users').doc(uid).get();
  final t = (s.data() ?? const {})['dailyTests'];
  if (t is Map && t['d'] == _todayIst()) return int.tryParse('${t['n']}') ?? 0;
  return 0;
}

/// Null = may start. Otherwise the limit that was reached.
Future<int?> dailyLimitReached(User u, bool paid) async {
  if (_isAdmin(u)) return null;
  try {
    final used = await _usedToday(u.uid).timeout(const Duration(seconds: 4));
    final limit = paid ? paidLimit : freeLimit;
    return used >= limit ? limit : null;
  } catch (_) {
    return null;
  }
}

Future<void> countDailyTest(User u) async {
  if (_isAdmin(u)) return;
  try {
    final n = await _usedToday(u.uid) + 1;
    await FirebaseFirestore.instance.collection('users').doc(u.uid).set({
      'dailyTests': {'d': _todayIst(), 'n': n}
    }, SetOptions(merge: true));
  } catch (_) {}
}

// ---------------------------------------------------------------- result

class SubjectStat {
  int correct = 0, wrong = 0, skip = 0;
  double marks = 0;
}

class Result {
  final int correct, wrong, skip, total;
  final double marks, maxMarks, pct;
  final Map<String, SubjectStat> subjects;
  final int timeUsed;
  String? attemptId;
  bool saved = false;
  int? rank;
  int? candidates;
  Result(this.correct, this.wrong, this.skip, this.total, this.marks, this.maxMarks, this.pct, this.subjects, this.timeUsed);
}

double _r1(double v) => double.parse(v.toStringAsFixed(1));

Result scorePaper(Paper p, Progress pr) {
  final rules = p.rules;
  var correct = 0, wrong = 0, skip = 0;
  var mk = 0.0;
  final subj = <String, SubjectStat>{};
  for (var i = 0; i < p.questions.length; i++) {
    final q = p.questions[i];
    final key = rules.statKey(q);
    final s = subj.putIfAbsent(key, () => SubjectStat());
    final a = pr.answers[i];
    if (a == null || a.isEmpty) {
      skip++;
      s.skip++;
      continue;
    }
    final v = a == q.correct ? rules.pos : -rules.neg(q, i);
    if (a == q.correct) {
      correct++;
      s.correct++;
    } else {
      wrong++;
      s.wrong++;
    }
    mk += v;
    s.marks += v;
  }
  final marks = _r1(mk);
  final maxMarks = p.questions.length * rules.pos;
  final pct = maxMarks > 0 ? _r1(marks / maxMarks * 100) : 0.0;
  final used = (pr.qMs.values.fold<int>(0, (a, b) => a + b) / 1000).round();
  return Result(correct, wrong, skip, p.questions.length, marks, maxMarks, pct, subj, used);
}

String _examName(String id) => const {
      'ssc-cgl': 'SSC CGL',
      'ssc-chsl': 'SSC CHSL',
      'ssc-mts': 'SSC MTS',
      'rrb-ntpc': 'RRB NTPC',
      'ssc-gd': 'SSC GD',
    }[id] ??
    id.toUpperCase().replaceAll('-', ' ');

/// Saves the attempt, the user's totals, the leaderboard row and the per-question tallies,
/// the same documents the website writes.
Future<void> saveResult(User u, Exam exam, Paper p, Progress pr, Result r) async {
  final db = FirebaseFirestore.instance;
  final rules = p.rules;
  final mockId = rules.mockId;
  final label = p.title.isNotEmpty ? p.title : _examName(exam.id);
  final log = <Map<String, dynamic>>[];
  for (var i = 0; i < p.questions.length; i++) {
    final q = p.questions[i];
    final a = pr.answers[i] ?? '';
    log.add({
      'q': q.qNumOr(i + 1),
      's': rules.statKey(q),
      'ch': q.chapter.replaceAll(RegExp(r'<[^>]*>'), ' ').replaceAll('&nbsp;', ' ').replaceAll('&amp;', '&').replaceAll(RegExp(r'\s+'), ' ').trim().characters40(),
      'd': q.difficulty,
      'a': a,
      'c': q.correct,
      'r': a.isEmpty ? 'k' : (a == q.correct ? 'c' : 'w'),
      't': ((pr.qMs[i] ?? 0) / 1000).round(),
    });
  }
  final subjectStats = r.subjects.map((k, v) => MapEntry(k, {'correct': v.correct, 'wrong': v.wrong, 'skip': v.skip}));
  final subjectMarks = r.subjects.map((k, v) => MapEntry(k, _r1(v.marks)));
  final pyq = isPyqId(mockId);
  final year = pyq ? (RegExp(r'^[a-z-]+_(\d{4})_').firstMatch(mockId)?.group(1) ?? '') : '';
  final attemptId = '${u.uid}_${exam.id}_${year.isEmpty ? 'na' : year}_${DateTime.now().millisecondsSinceEpoch}';
  final payload = <String, dynamic>{
    'uid': u.uid,
    'exam': exam.id,
    'year': year,
    'examName': label,
    'paperId': pyq ? mockId : '',
    'mockId': pyq ? '' : mockId,
    'total': r.total,
    'correct': r.correct,
    'wrong': r.wrong,
    'skip': r.skip,
    'marks': r.marks,
    'percentage': r.pct,
    'subjectStats': subjectStats,
    'subjectMarks': subjectMarks,
    'answers': log,
    'timeUsed': r.timeUsed,
    'analyticsV': 1,
    'partD': p.partD,
    'timestamp': FieldValue.serverTimestamp(),
    'clientSubmittedAt': DateTime.now().toUtc().toIso8601String(),
  };
  await db.collection('attempts').doc(attemptId).set(payload, SetOptions(merge: true));
  r.attemptId = attemptId;
  r.saved = true;

  // user totals (same arithmetic as the website)
  try {
    final ref = db.collection('users').doc(u.uid);
    final snap = await ref.get();
    final d = snap.data() ?? const {};
    if (snap.exists) {
      final total = int.tryParse('${d['totalTests'] ?? 0}') ?? 0;
      final avg = double.tryParse('${d['avgScore'] ?? 0}') ?? 0;
      final best = double.tryParse('${d['bestScore'] ?? 0}') ?? 0;
      final nt = total + 1;
      await ref.set({
        'totalTests': nt,
        'avgScore': double.parse(((avg * total + r.pct) / nt).toStringAsFixed(1)),
        'bestScore': r.pct > best ? r.pct : best,
        'lastActive': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true));
    } else {
      await ref.set({'uid': u.uid, 'totalTests': 1, 'avgScore': r.pct, 'bestScore': r.pct, 'lastActive': FieldValue.serverTimestamp()}, SetOptions(merge: true));
    }
  } catch (_) {}

  final base = lbBase(mockId);

  // leaderboard: best score only
  try {
    String name = 'Student';
    try {
      final us = await db.collection('users').doc(u.uid).get();
      final ud = us.data() ?? const {};
      name = '${ud['name'] ?? ud['displayName'] ?? u.displayName ?? ''}'.trim();
      if (name.isEmpty) name = 'Student';
    } catch (_) {}
    final ref = db.collection('leaderboards').doc(base).collection('scores').doc(u.uid);
    await db.runTransaction((tx) async {
      final cur = await tx.get(ref);
      final prev = cur.exists ? ((cur.data() ?? const {})['marks'] as num? ?? 0).toDouble() : double.negativeInfinity;
      if (!cur.exists || r.marks > prev) {
        tx.set(ref, {
          'uid': u.uid,
          'name': name,
          'paperId': base,
          'paperName': label,
          'marks': r.marks,
          'maxMarks': r.maxMarks,
          'accuracy': r.pct,
          'subjectMarks': subjectMarks,
          'timeUsed': r.timeUsed,
          'submittedAt': FieldValue.serverTimestamp(),
        });
      } else if ((cur.data() ?? const {})['name'] != name && name != 'Student') {
        tx.set(ref, {'name': name}, SetOptions(merge: true));
      }
    });
  } catch (_) {}

  // per-question tallies and the topper row
  try {
    final qs = <String, dynamic>{};
    for (final x in log) {
      final t = (x['t'] as int);
      qs['q${x['q']}'] = {
        'a': FieldValue.increment(x['r'] == 'k' ? 0 : 1),
        'c': FieldValue.increment(x['r'] == 'c' ? 1 : 0),
        'ts': FieldValue.increment(t),
        'tn': FieldValue.increment(t > 0 ? 1 : 0),
      };
    }
    await db.collection('qstats').doc(base).set({'n': FieldValue.increment(1), 'total': r.total, 'updatedAt': FieldValue.serverTimestamp(), 'q': qs}, SetOptions(merge: true));
    final sn = await db.collection('qstats').doc(base).get();
    final tp = (sn.data() ?? const {})['top'];
    final beat = !(tp is Map &&
        ((tp['m'] as num? ?? 0) > r.marks || ((tp['m'] as num? ?? 0) == r.marks && (tp['tu'] as num? ?? 0) > 0 && (tp['tu'] as num? ?? 0) <= r.timeUsed)));
    if (beat) {
      final tq = <String, String>{for (final x in log) 'q${x['q']}': '${x['r']}${x['t']}'};
      await db.collection('qstats').doc(base).set({
        'top': {'m': r.marks, 'tu': r.timeUsed, 'q': tq, 'at': FieldValue.serverTimestamp()}
      }, SetOptions(mergeFields: ['top']));
    }
  } catch (_) {}

  // rank among everyone who took this mock
  try {
    final col = db.collection('leaderboards').doc(base).collection('scores');
    final above = await col.where('marks', isGreaterThan: r.marks).count().get();
    final all = await col.count().get();
    r.rank = (above.count ?? 0) + 1;
    r.candidates = all.count;
  } catch (_) {}
}

String lbBase(String mockId) => mockId.replaceFirst(RegExp(r'([_-])(hi|en|hindi|english)$', caseSensitive: false), '');

extension on String {
  String characters40() => length <= 40 ? this : substring(0, 40);
}
