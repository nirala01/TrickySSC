// The test engine: the same rules as the website's mock-test.html (Tier 1 mocks of
// SSC CGL, CHSL, GD, MTS and RRB NTPC). Marks, sections, timers, the saved attempt,
// the leaderboard row and the daily limit all follow that page, so a result saved
// from the app looks exactly like one saved from the website.
import 'dart:convert';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../aic.dart';
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
  'Computer Knowledge': 'Computer',
  'Computer Knowledge Test': 'Computer',
  'Computer': 'Computer',
  'computer': 'Computer',
  'कंप्यूटर ज्ञान': 'Computer',
  'कंप्यूटर': 'Computer',
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
  if (low.contains('comput') || s.contains('कंप्यूटर')) return 'Computer';
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
  final int seconds; // 0 = the exam's usual unit length
  Unit(this.label, this.from, this.to, [this.seconds = 0]);
}

class Section {
  final String label;
  final int from;
  int to;
  Section(this.label, this.from, this.to);
}

class Rules {
  final String mockId;
  final Exam? ex; // the exam of this paper (null: chapter tests)
  final bool mts; // two sessions (SSC MTS)
  final bool ntpc; // one clock for the whole paper (RRB NTPC)
  final bool gd; // Part D in English or Hindi (SSC GD)
  final bool tier2; // CGL / CHSL Tier 2 (mock-test-tier2.html, test-tier2.html)
  final bool paper; // CGL Tier II Paper II (Statistics) / Paper III (Finance & Economics): 100 Qs, +2 / −0.5, one 2-hour clock
  final bool aic; // SSC CGL Tier-2 All India Challenge Mock: Tier 2 marking, five separately timed parts
  Rules(String mockId) : this._(mockId, examOfPaper(mockId));
  Rules._(this.mockId, this.ex)
      : mts = ex?.timing == 'sessions',
        ntpc = ex?.timing == 'single',
        gd = ex?.partD ?? false,
        tier2 = mockId.contains('_tier2_') || mockId.contains('_aic_'),
        aic = mockId.contains('_aic_'),
        paper = mockId.contains('_paper2_') || mockId.contains('_paper3_');

  static String _n(double v) => v == v.roundToDouble() ? '${v.round()}' : ((v * 3 - 1).abs() < 1e-9 ? '1/3' : v.toStringAsFixed(2));

  double get pos => tier2 ? 3 : (ex?.pos ?? 2);
  double get negBase => tier2 ? 1 : (ex?.neg ?? 0.5);
  double neg(Question q, int i) => !(ex?.negS2 ?? false) ? negBase : (q.qNumOr(i + 1) > ex!.split ? negBase : 0);
  int get unitSeconds => (ex?.unitMin ?? 15) * 60;

  String markingLine() {
    if (tier2) return '+3 for a correct answer · −1 for a wrong answer';
    if (ex?.negS2 ?? false) return '+${_n(pos)} for a correct answer · −${_n(negBase)} in Session II only (no negative in Session I)';
    return '+${_n(pos)} for a correct answer · −${_n(negBase)} for a wrong answer';
  }

  String timingLine(int units) {
    if (mockId.contains('__') && isPyqId(mockId)) return 'One subject section of the paper on its own clock. Submit when you are done or when time runs out.';
    if (mockId.contains('__')) return 'One subject section of the mock on its own clock. Submit when you are done or when time runs out.';
    if (mockId.startsWith('cw_') || mockId.startsWith('cwp_')) return 'One chapter test of 25 questions. Choose a 15-minute clock or untimed practice below.';
    if (paper) return 'One paper on a single 2-hour clock. Move freely between the parts.';
    if (aic) return 'Five separately timed parts, in order: Maths 30 min, Reasoning 30, English 40, General Awareness 20, Computer 15. You cannot go back to a finished part.';
    if (tier2) return 'Section I (Maths + Reasoning) 60 min, Section II (English + GA) 60 min, Section III (Computer) 15 min. Move freely inside the open section.';
    final note = (ex?.timingNote ?? '').isEmpty ? '' : ' ${ex!.timingNote}';
    final min = ex?.unitMin ?? 15;
    if (ntpc) return 'One paper on a single $min-minute clock.$note';
    if (mts) return 'Two sessions of $min minutes each.$note';
    return '$units sections of $min minutes each. When a section ends it is submitted and the next one opens.$note';
  }

  /// The subject key used for subject-wise stats, as the website computes it.
  String statKey(Question q) {
    if (ex?.canonStats ?? false) {
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
  ChapterInfo? chapter; // set for chapter tests
  AicRun? aic; // set for an All India Challenge paper: the live Sunday attempt or the free mock
  Paper(this.rules, this.questions, this.sections, this.units, this.title, this.partD);

  int unitSecs(int i) => units[i].seconds > 0 ? units[i].seconds : rules.unitSeconds;
  int get totalSecs => [for (var i = 0; i < units.length; i++) unitSecs(i)].fold(0, (a, b) => a + b);
}

/// A chapter test (website: chapterwise-test.html): 25 questions, +2 / −0.5, 15 minutes or untimed.
class ChapterInfo {
  final String chapterId, chapterName, subject, lang;
  final int level, testNum;
  final Map<int, Question> en; // English questions by qNum, for "View in English"
  final bool pyq; // chapter-wise PYQ test (website: pyq-chapter-test.html)
  // TSSC-EXAMUI-V1: Hindi questions by qNum, for "हिंदी में देखें" on an English test. [hiLoader] fetches them
  // on the first tap when they were not loaded with the test (chapter-wise PYQ tests).
  final Map<int, Question> hi;
  final Future<Map<int, Question>> Function()? hiLoader;
  ChapterInfo(this.chapterId, this.chapterName, this.subject, this.level, this.testNum, this.lang, this.en, {this.pyq = false, this.hi = const {}, this.hiLoader});
  String get _key => chapterId.replaceAll(RegExp(r'[^a-zA-Z0-9]'), '');
  String get lbKey => pyq ? 'cwp_ssc_all_${_key}_T$testNum' : cwLbKey(chapterId, level, testNum);
  String get lbName => pyq ? '$chapterName · SSC PYQ · Test $testNum' : '$chapterName · Level $level · Test $testNum';
}

/// One question of a chapter-wise PYQ test: its EN / HI document ids and the paper it came from.
class PyqRef {
  final String en, hi, paper;
  final int q;
  PyqRef(this.en, this.hi, this.paper, this.q);
}

Future<Paper> loadChapterPyqTest({required String chapterId, required String chapterName, required String subject, required int testNum, required List<PyqRef> refs, required String lang}) async {
  final col = FirebaseFirestore.instance.collection('questions');
  Future<Map<String, dynamic>?> get(String id) async {
    if (id.isEmpty) return null;
    try {
      final d = await col.doc(id).get();
      return d.exists ? {'id': d.id, ...d.data()!} : null;
    } catch (_) {
      return null;
    }
  }

  final enDocs = await Future.wait([for (final r in refs) get(r.en)]);
  final hiDocs = lang == 'hi' ? await Future.wait([for (final r in refs) get(r.hi)]) : List<Map<String, dynamic>?>.filled(refs.length, null);
  Question make(Map<String, dynamic> d, int k) => Question({...d, 'qNum': k + 1, '_src': refs[k].paper, '_srcQ': refs[k].q});
  final en = <Question>[], hi = <Question>[];
  for (var k = 0; k < refs.length; k++) {
    if (enDocs[k] != null) en.add(make(enDocs[k]!, k));
    if (hiDocs[k] != null) hi.add(make(hiDocs[k]!, k));
  }
  final useLang = lang == 'hi' && hi.isNotEmpty ? 'hi' : 'en';
  final qs = useLang == 'hi' ? hi : en;
  if (qs.isEmpty) throw 'This test could not be loaded just now.';
  final info = ChapterInfo(chapterId, chapterName, subject, 1, testNum, useLang, {for (final q in en) q.qNumOr(0): q},
      pyq: true,
      hi: {for (final q in hi) q.qNumOr(0): q},
      hiLoader: () async {
        final docs = await Future.wait([for (final r in refs) get(r.hi)]);
        return {for (var k = 0; k < refs.length; k++) if (docs[k] != null) k + 1: make(docs[k]!, k)};
      });
  final rules = Rules('${info.lbKey}_$useLang');
  final p = Paper(rules, qs, [Section(chapterName, 0, qs.length - 1)], [Unit(chapterName, 0, qs.length - 1, 15 * 60)], '$chapterName · PYQ Test $testNum', '');
  p.chapter = info;
  return p;
}

String cwLbKey(String chapterId, int level, int testNum) => 'cw_${chapterId.replaceAll(RegExp(r'[^a-zA-Z0-9]'), '')}_L${level}_T$testNum';

Future<Paper> loadChapterTest({required String chapterId, required String chapterName, required String subject, required int level, required int testNum, required String lang}) async {
  final col = FirebaseFirestore.instance.collection('questions');
  var snap = await col.where('chapterId', isEqualTo: chapterId).where('level', isEqualTo: level).where('testNum', isEqualTo: testNum).get();
  if (snap.docs.isEmpty) {
    snap = await col.where('chapterId', isEqualTo: chapterId).where('level', isEqualTo: '$level').where('testNum', isEqualTo: '$testNum').get();
  }
  final en = <Question>[], hi = <Question>[];
  for (final d in snap.docs) {
    final m = d.data();
    if (m['type'] != 'chapterwise' || m['exam'] != 'ssc-cgl') continue;
    ((m['language'] ?? m['lang']) == 'hi' ? hi : en).add(Question({'id': d.id, ...m}));
  }
  en.sort((a, b) => a.qNum.compareTo(b.qNum));
  hi.sort((a, b) => a.qNum.compareTo(b.qNum));
  final useLang = (lang == 'hi' && hi.isNotEmpty) || en.isEmpty ? 'hi' : 'en';
  final qs = useLang == 'hi' ? hi : en;
  if (qs.isEmpty) throw 'This test has no questions yet.';
  final id = '${cwLbKey(chapterId, level, testNum)}_$useLang';
  final rules = Rules(id);
  final p = Paper(rules, qs, [Section(chapterName, 0, qs.length - 1)], [Unit(chapterName, 0, qs.length - 1, 15 * 60)], '$chapterName · Level $level · Test $testNum', '');
  p.chapter = ChapterInfo(chapterId, chapterName, subject, level, testNum, useLang, {for (final q in en) q.qNumOr(0): q}, hi: {for (final q in hi) q.qNumOr(0): q});
  return p;
}

// ---- topic-wise current affairs tests (a rolling window of months)
//
// The questions are ordinary chapter-test rows (type chapterwise, exam ssc-cgl) with chapterId = the topic id
// and the month in the CSV's "year" column as YYYY-MM. The app keeps the months of the current window
// (ca-topics/index.json "months"), orders the questions newest month first and cuts them into tests of 25.
// So a month is dropped or added by changing the window: nothing is deleted from the database.

const caMonthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

/// '2026-10', '2026-1', '202610' -> '2026-10'; anything else -> ''.
String caMonthKey(dynamic v) {
  final m = RegExp(r'^\s*(\d{4})\D?(\d{1,2})\s*$').firstMatch(_str(v));
  if (m == null) return '';
  final mo = int.parse(m[2]!);
  return mo < 1 || mo > 12 ? '' : '${m[1]}-${mo.toString().padLeft(2, '0')}';
}

/// '2026-10' -> 'October 2026' (short: 'Oct 2026').
String caMonthLabel(String key, {bool short = false}) {
  if (key.length != 7) return '';
  final n = caMonthNames[int.parse(key.substring(5)) - 1];
  return '${short ? n.substring(0, 3) : n} ${key.substring(0, 4)}';
}

class CaTest {
  final int num; // 1 = the newest questions
  final List<Question> en, hi; // hi is empty, or has the same questions in the same order
  final String newest, oldest; // month keys ('' = undated)
  CaTest(this.num, this.en, this.hi, this.newest, this.oldest);
  int get count => en.isNotEmpty ? en.length : hi.length;
}

class CaPool {
  final String keyId; // topic id + the months covered: results reset cleanly when the window moves
  final List<CaTest> tests;
  CaPool(this.keyId, this.tests);
}

Future<CaPool> loadCaPool(String topicId, List<String> window) async {
  final snap = await FirebaseFirestore.instance.collection('questions').where('chapterId', isEqualTo: topicId).get();
  final keep = {for (final w in window) caMonthKey(w)}..remove('');
  final en = <String, Question>{}, hi = <String, Question>{};
  for (final d in snap.docs) {
    final m = d.data();
    if (m['type'] != 'chapterwise' || m['exam'] != 'ssc-cgl') continue;
    final month = caMonthKey(m['year']);
    if (month.isNotEmpty && keep.isNotEmpty && !keep.contains(month)) continue;
    final q = Question({'id': d.id, ...m, '_mk': month});
    // newest month first; undated questions (Budget, Economic Survey) keep their upload order
    final inv = month.isEmpty ? '999999' : (999999 - int.parse(month.replaceAll('-', ''))).toString();
    final key = '$inv|${_str(m['level']).padLeft(3, '0')}|${_str(m['testNum']).padLeft(4, '0')}|${q.qNum.toString().padLeft(4, '0')}';
    ((m['language'] ?? m['lang']) == 'hi' ? hi : en)[key] = q;
  }
  final base = en.isNotEmpty ? en : hi;
  final keys = base.keys.toList()..sort();
  final tests = <CaTest>[];
  var chunks = <List<String>>[for (var i = 0; i < keys.length; i += 25) keys.sublist(i, i + 25 > keys.length ? keys.length : i + 25)];
  if (chunks.length > 1 && chunks.last.length < 8) {
    final tail = chunks.removeLast();
    chunks.last.addAll(tail);
  }
  for (var n = 0; n < chunks.length; n++) {
    final c = chunks[n];
    final e = en.isEmpty ? <Question>[] : [for (final k in c) en[k]!];
    final h = c.every(hi.containsKey) ? [for (final k in c) hi[k]!] : <Question>[];
    final months = [for (final k in c) '${base[k]!.raw['_mk']}'].where((x) => x.isNotEmpty).toList()..sort();
    tests.add(CaTest(n + 1, e, h, months.isEmpty ? '' : months.last, months.isEmpty ? '' : months.first));
  }
  final all = [for (final q in base.values) '${q.raw['_mk']}'].where((x) => x.isNotEmpty).toList()..sort();
  final tag = all.isEmpty ? '' : '.${all.first.replaceAll('-', '').substring(2)}${all.last.replaceAll('-', '').substring(2)}';
  return CaPool('$topicId$tag', tests);
}

Paper caTestPaper(CaPool pool, CaTest t, String topicName, String lang) {
  final useLang = (lang == 'hi' && t.hi.isNotEmpty) || t.en.isEmpty ? 'hi' : 'en';
  Question make(Question q, int k) => Question({...q.raw, 'qNum': k + 1, '_month': caMonthLabel('${q.raw['_mk']}')});
  final en = [for (var k = 0; k < t.en.length; k++) make(t.en[k], k)];
  final hi = [for (var k = 0; k < t.hi.length; k++) make(t.hi[k], k)];
  final qs = useLang == 'hi' ? hi : en;
  final rules = Rules('${cwLbKey(pool.keyId, 1, t.num)}_$useLang');
  final p = Paper(rules, qs, [Section(topicName, 0, qs.length - 1)], [Unit(topicName, 0, qs.length - 1, 15 * 60)], '$topicName · Test ${t.num}', '');
  p.chapter = ChapterInfo(pool.keyId, topicName, 'gk', 1, t.num, useLang, {for (final q in en) q.qNumOr(0): q}, hi: {for (final q in hi) q.qNumOr(0): q});
  return p;
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
/// Subject mocks (website: mock-test-subject.html): one subject's band of a Tier 1 mock.
const subjectMockShort = {'quant': 'Quant', 'reasoning': 'Reasoning', 'gk': 'Gen. Awareness', 'english': 'English'};

List<int> _subjectBand(String mockId, String subject) => examOfPaper(mockId)?.bands[subject] ?? const [0, 0];

int subjectMockMinutes(String mockId, String subject) => examOfPaper(mockId)?.secTest(subject)?.min ?? examOfPaper(mockId)?.subjMin[subject] ?? 15;

Future<Paper> loadPaper(String mockId, String lang, {String? partD, String title = '', String? subject}) async {
  final rules = Rules(subject == null ? mockId : '${mockId}__$subject');
  var qs = await _fetch(mockId);
  if (qs.isEmpty) throw 'This paper has no questions yet.';
  final sec = subject == null ? null : examOfPaper(mockId)?.secTest(subject);
  if (sec != null) {
    // TSSC-SM-SECTEST-V1: a section test picked by the questions' own subject names (website SM_SUBJ_SETS)
    final picked = qs.where((q) => sec.match.contains(SecTest.norm(q.subjectRaw))).toList();
    if (picked.isEmpty) throw 'This mock has no ${sec.name} questions yet.';
    if (title.isEmpty) {
      try {
        final meta = await FirebaseFirestore.instance.collection('mock_tests').doc(mockId).get();
        title = _str((meta.data() ?? const {})['title']);
      } catch (_) {}
    }
    return Paper(rules, picked, [Section(sec.name, 0, picked.length - 1)], [Unit('${sec.name} section', 0, picked.length - 1, sec.min * 60)],
        title.isEmpty ? '' : '$title · ${sec.name}', '');
  }
  if (subject != null) {
    final short = subjectMockShort[subject] ?? 'Quant';
    var picked = qs.where((q) => canonSubject(q.subjectRaw) == short || (rules.gd && subject == 'english' && RegExp(r'hindi|हिंदी|हिन्दी', caseSensitive: false).hasMatch(q.subjectRaw))).toList();
    if (picked.length < 5) {
      final band = _subjectBand(mockId, subject);
      picked = qs.where((q) => q.qNum >= band[0] && q.qNum <= band[1]).toList();
    }
    if (picked.isEmpty) throw 'This ${isPyqId(mockId) ? 'paper' : 'mock'} has no ${short == 'Quant' ? 'Maths' : short} questions yet.';
    if (title.isEmpty) {
      try {
        final meta = await FirebaseFirestore.instance.collection('mock_tests').doc(mockId).get();
        title = _str((meta.data() ?? const {})['title']);
      } catch (_) {}
    }
    final label = rules.mts && short == 'Quant' ? 'Maths' : short;
    return Paper(rules, picked, [Section(label, 0, picked.length - 1)], [Unit('$label section', 0, picked.length - 1, subjectMockMinutes(mockId, subject) * 60)],
        title.isEmpty ? '' : '$title · ${short == 'Gen. Awareness' ? 'Gen. Awareness' : short}', '');
  }
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

  if (title.isEmpty && rules.aic) title = aicTitle(aicRoundOf(mockId));

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
  if (rules.aic) {
    // All India Challenge: every part on its own clock, in paper order, no going back
    const mins = {'Quant': 30, 'Reasoning': 30, 'English': 40, 'Gen. Awareness': 20, 'Computer': 15};
    for (var i = 0; i < sections.length; i++) {
      final c = canonSubject(sections[i].label);
      if (c == 'Quant') sections[i] = Section('Maths', sections[i].from, sections[i].to);
      units.add(Unit('Part ${i + 1} · ${sections[i].label}', sections[i].from, sections[i].to, (mins[c] ?? 30) * 60));
    }
  } else if (rules.tier2) {
    const phaseOf = {'Quant': 0, 'Reasoning': 0, 'English': 1, 'Gen. Awareness': 1, 'Computer': 2};
    const meta = [('Section I', 60 * 60), ('Section II', 60 * 60), ('Section III', 15 * 60)];
    int? curPhase;
    for (final s in sections) {
      final ph = phaseOf[canonSubject(s.label)] ?? curPhase ?? units.length;
      if (curPhase != ph || units.isEmpty) {
        final m = ph < meta.length ? meta[ph] : ('Section ${units.length + 1}', 60 * 60);
        units.add(Unit(m.$1, s.from, s.to, m.$2));
        curPhase = ph;
      } else {
        final last = units.removeLast();
        units.add(Unit(last.label, last.from, s.to, last.seconds));
      }
    }
    if (units.isEmpty) units.add(Unit('Full Test', 0, qs.length - 1, 135 * 60));
    for (var k = 0; k < units.length; k++) {
      final u = units[k];
      final names = [for (final s in sections) if (s.from >= u.from && s.to <= u.to) s.label];
      units[k] = Unit('${u.label} · ${names.join(' + ')}', u.from, u.to, u.seconds);
    }
  } else if (rules.paper) {
    units.add(Unit('Full paper', 0, qs.length - 1, 120 * 60));
  } else if (rules.mts) {
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].label == 'Quant') sections[i] = Section('Maths', sections[i].from, sections[i].to);
    }
    final split = rules.ex!.split > 0 ? rules.ex!.split : qs.length ~/ 2;
    var cut = -1;
    for (var i = 0; i < qs.length; i++) {
      if (qs[i].qNumOr(i + 1) > split) {
        cut = i;
        break;
      }
    }
    if (cut < 0) cut = qs.length < split ? qs.length : split;
    if (cut > 0) units.add(Unit('Session I', 0, cut - 1));
    if (cut < qs.length) units.add(Unit('Session II', cut, qs.length - 1));
  } else if (rules.ntpc) {
    sections
      ..clear()
      ..add(Section('All Questions', 0, qs.length - 1));
    units.add(Unit('${rules.ex!.name} Paper', 0, qs.length - 1));
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
    for (final q in await _fetch(twinId(mockId.replaceFirst(RegExp(r'__[a-z]+$'), ''), 'en'))) {
      out[q.qNum] = q;
    }
  } catch (_) {}
  return out;
}

/// TSSC-EXAMUI-V1: Hindi version of each question of an English paper, by question number (for "हिंदी में देखें").
/// An empty map = this test has no Hindi version; null = it could not be loaded (network).
Future<Map<int, Question>?> loadHindiTwin(String mockId) async {
  final base = mockId.replaceFirst(RegExp(r'__[a-z]+$'), '');
  final id = twinId(base, 'hi');
  if (id == base) return {};
  try {
    final out = <int, Question>{};
    for (final q in await _fetch(id)) {
      final l = '${q.raw['language'] ?? q.raw['lang'] ?? ''}'.trim().toLowerCase();
      if (l == 'en' || l == 'eng' || l == 'english') continue;
      out[q.qNum] = q;
    }
    return out;
  } catch (_) {
    return null;
  }
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
  bool untimed = false; // chapter tests can be taken without a clock
  int startedAt = 0; // All India Challenge, live: server time of the first start (the 2 h 25 min hard stop runs from it)

  Map<String, dynamic> toJson() => {
        'a': answers.map((k, v) => MapEntry('$k', v)),
        'm': marked.toList(),
        'v': visited.toList(),
        't': qMs.map((k, v) => MapEntry('$k', v)),
        'u': unit,
        'c': current,
        'r': remaining,
        'ut': untimed,
        if (startedAt > 0) 'st': startedAt,
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
    p.untimed = j['ut'] == true;
    p.startedAt = (j['st'] as num? ?? 0).toInt();
    return p;
  }
}

String _progressKey(String uid, String mockId, String partD) => 'tssc_prog_${uid}_${mockId}_$partD';

Future<Progress?> loadProgress(String uid, String mockId, String partD) async {
  try {
    final s = (await SharedPreferences.getInstance()).getString(_progressKey(uid, mockId, partD));
    if (s == null) return null;
    final j = jsonDecode(s) as Map<String, dynamic>;
    // a test left half-way stays resumable until it is submitted or restarted (no expiry, 2026-11-19)
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
    for (final k in prefs.getKeys()) {
      if (!k.startsWith(pre)) continue;
      try {
        final j = jsonDecode(prefs.getString(k) ?? '') as Map<String, dynamic>;
        final rest = k.substring(pre.length);
        final cut = rest.lastIndexOf('_');
        var mockId = rest.substring(0, cut);
        final partD = rest.substring(cut + 1);
        // one subject section ("<base>_<lang>__<subject>") is listed as "<base>__<subject>"
        var tail = '';
        final ss = mockId.indexOf('__');
        if (ss > 0) {
          tail = mockId.substring(ss);
          mockId = mockId.substring(0, ss);
        }
        final lc = mockId.lastIndexOf('_');
        final lang = mockId.substring(lc + 1);
        if (lang != 'en' && lang != 'hi') continue;
        out[mockId.substring(0, lc) + tail] = [lang, partD];
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
  bool lbSaved = true; // false: the leaderboard row could not be written (matters for a live challenge attempt)
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

String _examName(String id) => examById(id)?.name ?? id.toUpperCase().replaceAll('-', ' ');

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
      'ch': (_str(q.raw['chapterId']).isNotEmpty ? _str(q.raw['chapterId']) : q.chapter).replaceAll(RegExp(r'<[^>]*>'), ' ').replaceAll('&nbsp;', ' ').replaceAll('&amp;', '&').replaceAll(RegExp(r'\s+'), ' ').trim().characters40(),
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
  final ch = p.chapter;
  final attemptId = ch != null
      ? (ch.pyq
          ? 'cwp_${u.uid}_ssc_all_${ch.chapterId.replaceAll(RegExp(r'[^a-zA-Z0-9]'), '')}_T${ch.testNum}_${ch.lang}'
          : 'cw_${u.uid}_${ch.chapterId.replaceAll(RegExp(r'[^a-zA-Z0-9]'), '')}_L${ch.level}_T${ch.testNum}_${ch.lang}')
      : '${u.uid}_${exam.id}_${year.isEmpty ? 'na' : year}_${DateTime.now().millisecondsSinceEpoch}';
  final payload = ch != null
      ? <String, dynamic>{
          'uid': u.uid,
          'type': ch.pyq ? 'pyq-chapter' : 'chapterwise',
          if (ch.pyq) 'src': 'pyq',
          if (ch.pyq) 'tier': 'all',
          'exam': ch.pyq ? 'ssc' : 'ssc-cgl',
          'examName': ch.pyq ? '${ch.chapterName} (PYQ)' : ch.chapterName,
          'subject': ch.subject,
          'chapter': ch.chapterId,
          'chapterId': ch.chapterId,
          'chapterName': ch.chapterName,
          'level': ch.level,
          'testNum': ch.testNum,
          'language': ch.lang,
          'correct': r.correct,
          'wrong': r.wrong,
          'skip': r.skip,
          'total': r.total,
          'marks': r.marks,
          'percentage': r.pct,
          'name': u.displayName ?? '',
          'email': u.email ?? '',
          'phone': u.phoneNumber ?? '',
          'answers': log,
          'timeUsed': r.timeUsed,
          'analyticsV': 1,
          'lbKey': ch.lbKey,
          'timestamp': FieldValue.serverTimestamp(),
          'clientSubmittedAt': DateTime.now().toUtc().toIso8601String(),
        }
      : <String, dynamic>{
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
    if (rules.tier2 || rules.paper) 'tier': 'tier2', // the website files Paper II / III attempts under tier2 too
    if (p.aic != null) 'aic': p.aic!.toAttempt(), // All India Challenge: {round, live, resultAt}
    // one subject section on its own: a mock's, or a previous-year paper's (same fields as the website)
    if (mockId.contains('__')) (pyq ? 'basePaperId' : 'baseMockId'): mockId.substring(0, mockId.indexOf('__')),
    if (mockId.contains('__')) 'subjectKey': mockId.substring(mockId.indexOf('__') + 2),
    if (mockId.contains('__')) 'testKind': pyq ? 'pyq-subject' : 'mock-subject',
    'timestamp': FieldValue.serverTimestamp(),
    'clientSubmittedAt': DateTime.now().toUtc().toIso8601String(),
  };
  await db.collection('attempts').doc(attemptId).set(payload, SetOptions(merge: ch == null));
  r.attemptId = attemptId;
  r.saved = true;

  // app usage, for the testers page (admin-testers.html)
  db.collection('users').doc(u.uid).set({
    'appTests': FieldValue.increment(1),
    'lastAppTest': FieldValue.serverTimestamp(),
    'appDays': FieldValue.arrayUnion([_todayIst()]),
  }, SetOptions(merge: true)).catchError((_) {});

  // user totals (same arithmetic as the website; chapter tests do not count here)
  if (ch == null) try {
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

  // leaderboard: best score only. All India Challenge: the board is live attempts only, so the free mock
  // taken after the result writes no row; a live attempt tries three times, because that row is the proof of "submitted".
  final aicFree = p.aic != null && !p.aic!.live;
  if (!aicFree) {
    String name = 'Student';
    try {
      final us = await db.collection('users').doc(u.uid).get();
      final ud = us.data() ?? const {};
      name = '${ud['name'] ?? ud['displayName'] ?? u.displayName ?? ''}'.trim();
      if (name.isEmpty) name = 'Student';
    } catch (_) {}
    final ref = db.collection('leaderboards').doc(base).collection('scores').doc(u.uid);
    var ok = false;
    for (var tries = 0; tries < (p.aic != null ? 3 : 1) && !ok; tries++) {
      try {
        await db.runTransaction((tx) async {
          final cur = await tx.get(ref);
          final prev = cur.exists ? ((cur.data() ?? const {})['marks'] as num? ?? 0).toDouble() : double.negativeInfinity;
          if (!cur.exists || r.marks > prev) {
            tx.set(ref, {
              'uid': u.uid,
              'name': name,
              'paperId': base,
              'paperName': ch != null ? ch.lbName : label,
              'marks': r.marks,
              'maxMarks': r.maxMarks,
              'accuracy': r.pct,
              'subjectMarks': ch != null ? <String, dynamic>{} : subjectMarks,
              'timeUsed': r.timeUsed,
              'submittedAt': FieldValue.serverTimestamp(),
            });
          } else if ((cur.data() ?? const {})['name'] != name && name != 'Student') {
            tx.set(ref, {'name': name}, SetOptions(merge: true));
          }
        });
        ok = true;
      } catch (_) {}
    }
    r.lbSaved = ok;
  }

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
    if (beat && !aicFree) {
      final tq = <String, String>{for (final x in log) 'q${x['q']}': '${x['r']}${x['t']}'};
      await db.collection('qstats').doc(base).set({
        'top': {'m': r.marks, 'tu': r.timeUsed, 'q': tq, 'at': FieldValue.serverTimestamp()}
      }, SetOptions(mergeFields: ['top']));
    }
  } catch (_) {}

  // rank among everyone who took this mock (a challenge paper shows its rank only from the result time)
  if (p.aic == null) try {
    final col = db.collection('leaderboards').doc(base).collection('scores');
    final above = await col.where('marks', isGreaterThan: r.marks).count().get();
    final all = await col.count().get();
    r.rank = (above.count ?? 0) + 1;
    r.candidates = all.count;
  } catch (_) {}
}

String lbBase(String mockId) => mockId.replaceFirstMapped(RegExp(r'([_-])(hi|en|hindi|english)(__[a-z]+)?$', caseSensitive: false), (m) => m[3] ?? '');

extension on String {
  String characters40() => length <= 40 ? this : substring(0, 40);
}
