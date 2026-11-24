import 'dart:convert';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../data.dart';
import '../test/engine.dart';
import '../test/test_screen.dart';
import '../ui/icons3d.dart';
import '../ui/soft.dart';
import '../ui/soft_list.dart';
import 'dash/logic.dart' show chapterNames, loadPyqChapterMap;
import 'dash/ui.dart';

class ChSubject {
  final String key; // the website's subject key (quant, reasoning, english, gk, computer, finance)
  final String name;
  final String page; // website subject page with the chapter list
  final IconData icon;
  final Color c1, c2;
  const ChSubject(this.key, this.name, this.page, this.icon, this.c1, this.c2);
}

const _subjects = [
  ChSubject('quant', 'Quantitative Aptitude', 'ssc-cgl-quant-chapter-wise-test.html', Icons.calculate, Color(0xFFEA580C), Color(0xFFFDBA74)),
  ChSubject('reasoning', 'Reasoning', 'ssc-cgl-reasoning-chapter-wise-test.html', Icons.psychology, Color(0xFF7C3AED), Color(0xFFC4B5FD)),
  ChSubject('english', 'English', 'ssc-cgl-english-chapter-wise-test.html', Icons.menu_book, Color(0xFF0369A1), Color(0xFF7DD3FC)),
  ChSubject('gk', 'General Awareness', 'ssc-cgl-gk-chapter-wise-test.html', Icons.public, Color(0xFF047857), Color(0xFF6EE7B7)),
  ChSubject('computer', 'Computer', 'ssc-cgl-computer-chapter-wise-test.html', Icons.computer, Color(0xFF334155), Color(0xFF94A3B8)),
  ChSubject('finance', 'Finance & Economics (AAO)', 'ssc-cgl-finance-economics-chapter-wise-test.html', Icons.account_balance, Color(0xFFBE185D), Color(0xFFF9A8D4)),
  ChSubject('statistics', 'Statistics (JSO)', 'ssc-cgl-statistics-chapter-wise-test.html', Icons.bar_chart, Color(0xFF0E7490), Color(0xFF67E8F9)),
];

const _extraSubjects = {'computer', 'finance', 'statistics'};

List<ChSubject> subjectsFor(Exam e) => [
      for (final s in _subjects)
        if (!_extraSubjects.contains(s.key) || e.chExtra.contains(s.key)) s
    ];

class ChChapter {
  final String id, name, icon;
  ChChapter(this.id, this.name, this.icon);
}

/// HTML text -> plain text, including numeric entities (the chapter icons are written as &#128216; on the website).
String _unesc(String s) => s
    .replaceAllMapped(RegExp(r'&#(x[0-9a-fA-F]+|\d+);'), (m) {
      final g = m[1]!;
      final code = g.startsWith('x') ? int.tryParse(g.substring(1), radix: 16) : int.tryParse(g);
      return code == null || code <= 0 || code > 0x10FFFF ? '' : String.fromCharCode(code);
    })
    .replaceAll('&amp;', '&')
    .replaceAll('&quot;', '"')
    .replaceAll('&nbsp;', ' ');

Future<List<ChChapter>> _loadChapters(ChSubject s) async {
  final prefs = await SharedPreferences.getInstance();
  final key = 'tssc_chlist_${s.key}';
  try {
    final c = jsonDecode(prefs.getString(key) ?? '{}') as Map;
    if (DateTime.now().millisecondsSinceEpoch - ((c['at'] as num?) ?? 0) < 24 * 3600 * 1000 && c['l'] is List) {
      return [for (final j in c['l'] as List) ChChapter('${j[0]}', '${j[1]}', _unesc('${j[2]}'))];
    }
  } catch (_) {}
  final r = await http.get(Uri.parse('https://trickyssc.com/${s.page}'));
  if (r.statusCode != 200) throw 'http';
  final html = utf8.decode(r.bodyBytes);
  final out = <ChChapter>[];
  final seen = <String>{};
  final items = RegExp(r'<li class="ch-item[^"]*" data-chapter="([^"]+)"').allMatches(html).toList();
  for (var i = 0; i < items.length; i++) {
    final id = items[i].group(1)!;
    final end = i + 1 < items.length ? items[i + 1].start : html.length;
    final block = html.substring(items[i].start, end);
    final name = _unesc(RegExp(r'class="ch-name">([^<]*)<').firstMatch(block)?.group(1)?.trim() ?? id);
    final ico = _unesc(RegExp(r'class="ch-ico"[^>]*>([^<]*)<').firstMatch(block)?.group(1)?.trim() ?? '');
    if (seen.add(id)) out.add(ChChapter(id, name, ico));
  }
  if (out.isNotEmpty) {
    await prefs.setString(key, jsonEncode({'at': DateTime.now().millisecondsSinceEpoch, 'l': [for (final c in out) [c.id, c.name, c.icon]]}));
  }
  return out;
}

/// Fills chapterNames (dash/logic.dart) with every subject's chapter id -> name, so the dashboard shows
/// chapter names instead of ids. Uses the saved lists; a subject that cannot be loaded is skipped.
Future<void> loadAllChapterNames() async {
  Future<void> one(ChSubject s) async {
    try {
      for (final c in await _loadChapters(s)) {
        if (c.name.isNotEmpty) chapterNames[c.id] = c.name;
      }
    } catch (_) {}
  }

  await Future.wait([loadPyqChapterMap(), for (final s in _subjects) one(s)]);
}

const _chIdPrefix = {'quant': 'quant', 'reasoning': 'reason', 'english': 'eng', 'gk': 'ga', 'computer': 'computer', 'finance': 'fineco', 'statistics': 'statistics'};
const _chShown = {'quant': 'Quant', 'reasoning': 'Reasoning', 'english': 'English', 'gk': 'Gen. Awareness', 'computer': 'Computer', 'finance': 'Finance & Economics', 'statistics': 'Statistics'};

/// Chapter-test subjects of an exam for the chapter analysis: shown name -> its chapter ids, in page order.
Map<String, List<String>> chapterListsFor(Exam e) => {
      for (final s in subjectsFor(e))
        _chShown[s.key] ?? s.name: [
          for (final id in chapterNames.keys)
            if (id.startsWith('${_chIdPrefix[s.key]}.')) id
        ]
    };

/// Opens the tests of one chapter (the "Practice" button of the chapter analysis).
Future<void> openChapterPractice(BuildContext context, User user, Exam exam, String chapterId) async {
  ChSubject? sub;
  for (final s in _subjects) {
    if (chapterId.startsWith('${_chIdPrefix[s.key]}.')) sub = s;
  }
  if (sub == null) return;
  final nav = Navigator.of(context);
  Set<String> owned = <String>{}, attempted = <String>{};
  try {
    final r = await Future.wait([loadOwned(user.uid), loadAttempted(user.uid)]);
    owned = r[0];
    attempted = r[1];
  } catch (_) {}
  final s0 = sub;
  await nav.push(MaterialPageRoute(
    builder: (_) => ChapterTestsScreen(user: user, exam: exam, subject: s0, chapter: ChChapter(chapterId, chapterNames[chapterId] ?? chapterId, ''), paid: owned.isNotEmpty, attempted: attempted, onReturn: () {}),
  ));
}

/// Number of tests in each chapter (English test 1st questions, as the website counts them). Cached 6 h.
Future<Map<String, int>> _loadCounts(List<ChChapter> chs, String subjectKey) async {
  final prefs = await SharedPreferences.getInstance();
  final key = 'tssc_chcount_$subjectKey';
  try {
    final c = jsonDecode(prefs.getString(key) ?? '{}') as Map;
    if (DateTime.now().millisecondsSinceEpoch - ((c['at'] as num?) ?? 0) < 6 * 3600 * 1000 && c['n'] is Map) {
      final m = Map<String, int>.from((c['n'] as Map).map((k, v) => MapEntry('$k', (v as num).toInt())));
      if (chs.every((x) => m.containsKey(x.id))) return m;
    }
  } catch (_) {}
  final col = FirebaseFirestore.instance.collection('questions');
  final out = <String, int>{};
  var failed = false;
  for (var i = 0; i < chs.length; i += 6) {
    await Future.wait([
      for (final c in chs.skip(i).take(6))
        col
            .where('exam', isEqualTo: 'ssc-cgl')
            .where('type', isEqualTo: 'chapterwise')
            .where('chapterId', isEqualTo: c.id)
            .where('language', isEqualTo: 'en')
            .where('qNum', isEqualTo: 1)
            .count()
            .get()
            .then<void>((s) {
          out[c.id] = s.count ?? 0;
        }).catchError((_) {
          failed = true;
          out[c.id] = 0;
        }),
    ]);
  }
  if (!failed) await prefs.setString(key, jsonEncode({'at': DateTime.now().millisecondsSinceEpoch, 'n': out}));
  return out;
}

// ======================================================================= subjects

const _icon3d = {'quant': 'pencil', 'reasoning': 'puzzle', 'english': 'book', 'gk': 'news', 'computer': 'clip', 'finance': 'paper', 'statistics': 'folder'};

class ChapterSubjectsScreen extends StatelessWidget {
  final User user;
  final Exam exam;
  final bool paid;
  final Set<String> attempted;
  final VoidCallback onReturn;
  const ChapterSubjectsScreen({super.key, required this.user, required this.exam, required this.paid, required this.attempted, required this.onReturn});

  @override
  Widget build(BuildContext context) {
    final list = subjectsFor(exam);
    return DashPage(exam: exam, title: 'Chapter Tests', sub: 'Practise Chapter by Chapter · FREE', children: [
      SoftSummary(
        icon: 'book',
        title: 'Practise chapter by chapter',
        progress: 1,
        sub: '25-question tests · Level 1 (exam level) and Level 2 (above exam level) · Hindi & English',
        accent: exam.c1,
      ),
      const SizedBox(height: 12),
      for (final (i, s) in list.indexed)
        SubjectCard(
          icon3d: _icon3d[s.key] ?? 'book',
          title: s.name,
          tone: i,
          line: _SubjectCount(subject: s, color: exam.c1),
          onTap: () => Navigator.of(context).push(MaterialPageRoute(
            builder: (_) => SubjectChaptersScreen(user: user, exam: exam, subject: s, paid: paid, attempted: attempted, onReturn: onReturn),
          )),
        ),
    ]);
  }
}

/// TSSC-LISTUI-V2: "35 chapters · 319 tests · FREE" under a subject, as on the Chapter PYQs screen.
class _SubjectCount extends StatefulWidget {
  final ChSubject subject;
  final Color color;
  const _SubjectCount({required this.subject, required this.color});

  @override
  State<_SubjectCount> createState() => _SubjectCountState();
}

class _SubjectCountState extends State<_SubjectCount> {
  int _ch = 0, _tests = 0;
  bool _failed = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final chs = await _loadChapters(widget.subject);
      final n = await _loadCounts(chs, widget.subject.key);
      final live = chs.where((c) => (n[c.id] ?? 0) > 0).length;
      final tests = n.values.fold<int>(0, (a, b) => a + b);
      if (!mounted) return;
      setState(() {
        if (tests > 0) {
          _ch = live;
          _tests = tests;
        } else {
          _failed = true;
        }
      });
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_tests == 0) {
      return _failed ? const SoftTag.free() : const Text('Counting tests…', style: TextStyle(fontSize: 13, color: softMuted, fontWeight: FontWeight.w700));
    }
    return SubjectCounts(_ch, _tests);
  }
}

// ======================================================================= chapters of a subject

class SubjectChaptersScreen extends StatefulWidget {
  final User user;
  final Exam exam;
  final ChSubject subject;
  final bool paid;
  final Set<String> attempted;
  final VoidCallback onReturn;
  const SubjectChaptersScreen({super.key, required this.user, required this.exam, required this.subject, required this.paid, required this.attempted, required this.onReturn});

  @override
  State<SubjectChaptersScreen> createState() => _SubjectChaptersScreenState();
}

class _SubjectChaptersScreenState extends State<SubjectChaptersScreen> {
  List<ChChapter>? _chs;
  Map<String, int>? _n;
  bool _failed = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _failed = false);
    try {
      final chs = await _loadChapters(widget.subject);
      if (!mounted) return;
      setState(() => _chs = chs);
      final n = await _loadCounts(chs, widget.subject.key);
      if (mounted) setState(() => _n = n);
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam, s = widget.subject;
    final chs = _chs;
    final n = _n ?? const <String, int>{};
    final live = chs == null ? <ChChapter>[] : chs.where((c) => (n[c.id] ?? 0) > 0).toList();
    final soon = chs == null || _n == null ? <ChChapter>[] : chs.where((c) => (n[c.id] ?? 0) == 0).toList();
    return DashPage(exam: exam, title: s.name, sub: 'Chapter-wise Practice Tests', onRefresh: _load, children: [
      if (_failed)
        Padding(
          padding: const EdgeInsets.all(24),
          child: Column(children: [
            const Text('Could not load the chapters. Check your internet.'),
            TextButton(onPressed: _load, child: const Text('Try again')),
          ]),
        )
      else if (chs == null)
        const Padding(padding: EdgeInsets.all(40), child: Center(child: CircularProgressIndicator()))
      else ...[
        if (_n == null) const Padding(padding: EdgeInsets.only(bottom: 10), child: LinearProgressIndicator()),
        for (final (i, c) in (_n == null ? chs : live).indexed) _row(c, n[c.id], i),
        if (soon.isNotEmpty) ...[
          const Padding(padding: EdgeInsets.fromLTRB(4, 8, 4, 8), child: Text('Coming soon', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: softMuted))),
          for (final (i, c) in soon.indexed) _row(c, 0, i),
        ],
      ],
    ]);
  }

  Widget _row(ChChapter c, int? tests, int i) {
    final exam = widget.exam, s = widget.subject;
    final soon = tests == 0;
    final done = tests == null || tests == 0 ? 0 : _attemptedIn(c.id);
    return SoftRow(
      badge: tests == null ? '…' : (soon ? '–' : '$tests'),
      badgeSub: tests == 1 ? 'Test' : 'Tests',
      emoji: c.icon,
      tone: i,
      title: c.name,
      tags: [
        if (!soon) const SoftTag.free(),
        if (done > 0) SoftTag.done(text: '✓ $done DONE'),
      ],
      action: soon ? null : 'Open',
      accent: exam.c1,
      onTap: soon
          ? () {}
          : () => Navigator.of(context).push(MaterialPageRoute(
                builder: (_) => ChapterTestsScreen(user: widget.user, exam: exam, subject: s, chapter: c, paid: widget.paid, attempted: widget.attempted, onReturn: widget.onReturn),
              )),
    );
  }

  int _attemptedIn(String chId) {
    final k = 'cw_${chId.replaceAll(RegExp(r'[^a-zA-Z0-9]'), '')}_L';
    return widget.attempted.where((a) => a.startsWith(k)).length;
  }
}

// ======================================================================= tests of a chapter

class ChapterTestsScreen extends StatefulWidget {
  final User user;
  final Exam exam;
  final ChSubject subject;
  final ChChapter chapter;
  final bool paid;
  final Set<String> attempted;
  final VoidCallback onReturn;
  const ChapterTestsScreen({super.key, required this.user, required this.exam, required this.subject, required this.chapter, required this.paid, required this.attempted, required this.onReturn});

  @override
  State<ChapterTestsScreen> createState() => _ChapterTestsScreenState();
}

class _ChapterTestsScreenState extends State<ChapterTestsScreen> {
  Map<int, Map<int, Set<String>>>? _by; // level -> test -> {en, hi}
  bool _failed = false;
  late Set<String> _attempted = widget.attempted;
  Map<String, List<String>> _paused = {}; // tests left half-way: key -> [lang, partD]
  void _loadPaused() => loadInProgress(widget.user.uid).then((r) {
        if (mounted) setState(() => _paused = r);
      });

  @override
  void initState() {
    super.initState();
    _loadPaused();
    _load();
  }

  Future<void> _load() async {
    setState(() => _failed = false);
    try {
      final snap = await FirebaseFirestore.instance
          .collection('questions')
          .where('exam', isEqualTo: 'ssc-cgl')
          .where('type', isEqualTo: 'chapterwise')
          .where('chapterId', isEqualTo: widget.chapter.id)
          .where('qNum', isEqualTo: 1)
          .get();
      final by = <int, Map<int, Set<String>>>{};
      for (final d in snap.docs) {
        final m = d.data();
        final lv = int.tryParse('${m['level'] ?? ''}') ?? 0, tn = int.tryParse('${m['testNum'] ?? ''}') ?? 0;
        if (lv == 0 || tn == 0) continue;
        by.putIfAbsent(lv, () => {}).putIfAbsent(tn, () => {}).add((m['language'] ?? m['lang']) == 'hi' ? 'hi' : 'en');
      }
      if (mounted) setState(() => _by = by);
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  Future<void> _open(int lv, int tn, Set<String> langs) async {
    final exam = widget.exam;
    var lang = langs.contains('en') ? 'en' : 'hi';
    final saved = _paused[cwLbKey(widget.chapter.id, lv, tn)];
    if (saved != null) {
      lang = saved[0]; // resume in the language it was started in
    } else if (langs.length > 1) {
      final picked = await showModalBottomSheet<String>(
        context: context,
        backgroundColor: Colors.white,
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
        builder: (c) => SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 12),
            child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              Text('${widget.chapter.name} · Test $tn', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: exam.ink)),
              const SizedBox(height: 12),
              Row(children: [
                Expanded(
                  child: FilledButton(
                    onPressed: () => Navigator.pop(c, 'en'),
                    style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50)),
                    child: const Text('English', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: FilledButton(
                    onPressed: () => Navigator.pop(c, 'hi'),
                    style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50)),
                    child: const Text('हिंदी', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
                  ),
                ),
              ]),
            ]),
          ),
        ),
      );
      if (picked == null || !mounted) return;
      lang = picked;
    }
    final ch = widget.chapter;
    await Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => TestFlow(
        user: widget.user,
        exam: exam,
        mockId: '${cwLbKey(ch.id, lv, tn)}_$lang',
        lang: lang,
        paid: widget.paid,
        title: '${ch.name} · Test $tn',
        loader: () => loadChapterTest(chapterId: ch.id, chapterName: ch.name, subject: widget.subject.key, level: lv, testNum: tn, lang: lang),
      ),
    ));
    widget.onReturn();
    final a = await loadAttempted(widget.user.uid);
    if (mounted) setState(() => _attempted = a);
    _loadPaused();
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam, ch = widget.chapter;
    final by = _by;
    const levels = [(1, 'SSC CGL level'), (2, 'Above SSC CGL level')];
    final total = by == null ? 0 : by.values.fold<int>(0, (t, m) => t + m.length);
    var done = 0;
    if (by != null) {
      by.forEach((lv, m) {
        for (final tn in m.keys) {
          if (_attempted.contains(cwLbKey(ch.id, lv, tn))) done++;
        }
      });
    }
    return DashPage(exam: exam, title: ch.name, onRefresh: _load, children: [
      if (_failed)
        Padding(
          padding: const EdgeInsets.all(24),
          child: Column(children: [
            const Text('Could not load the tests. Check your internet.'),
            TextButton(onPressed: _load, child: const Text('Try again')),
          ]),
        )
      else if (by == null)
        const Padding(padding: EdgeInsets.all(40), child: Center(child: CircularProgressIndicator()))
      else ...[
        SoftSummary(icon: 'book', title: '$done of $total done', progress: total == 0 ? 0 : done / total, sub: '25 questions each · 15 min or untimed · FREE', accent: exam.c1),
        const SizedBox(height: 6),
        if (by.isEmpty) const Padding(padding: EdgeInsets.all(30), child: Center(child: Text('No tests in this chapter yet.'))),
        for (final lv in levels)
          if (by[lv.$1] != null) ...[
            Padding(
              padding: const EdgeInsets.fromLTRB(4, 12, 4, 8),
              child: Row(children: [
                SoftTag('LEVEL ${lv.$1}', Colors.white, lv.$1 == 1 ? const Color(0xFF059669) : const Color(0xFFDC2626)),
                const SizedBox(width: 8),
                Expanded(child: Text(lv.$2, style: baloo(17))),
                Text('${by[lv.$1]!.length} tests', style: const TextStyle(fontSize: 13, color: softMuted, fontWeight: FontWeight.w700)),
              ]),
            ),
            GridView.count(
              crossAxisCount: 3,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: 10,
              crossAxisSpacing: 10,
              childAspectRatio: 1.05,
              children: [
                for (final tn in (by[lv.$1]!.keys.toList()..sort()))
                  Builder(builder: (_) {
                    final langs = by[lv.$1]![tn]!;
                    final isDone = _attempted.contains(cwLbKey(ch.id, lv.$1, tn));
                    final isPaused = _paused.containsKey(cwLbKey(ch.id, lv.$1, tn));
                    return Material(
                      color: Colors.transparent,
                      child: Ink(
                        decoration: softCard(radius: 18, glow: isDone ? const Color(0xFF2563EB) : exam.c1),
                        child: InkWell(
                          borderRadius: BorderRadius.circular(18),
                          onTap: () => _open(lv.$1, tn, langs),
                          child: Padding(
                            padding: const EdgeInsets.all(8),
                            child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                              Text('Test $tn', style: baloo(19, color: exam.c1)),
                              const SizedBox(height: 4),
                              isDone ? const SoftTag.done() : const SoftTag.free(),
                              const SizedBox(height: 4),
                              Text(isPaused ? 'Resume ›' : (isDone ? 'Re-attempt ›' : 'Start ›'),
                                  style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w900, color: isPaused ? const Color(0xFFD97706) : exam.c1)),
                              const SizedBox(height: 2),
                              Text(langs.length > 1 ? 'EN · हिंदी' : (langs.contains('hi') ? 'हिंदी' : 'English'), style: const TextStyle(fontSize: 12, color: softMuted, fontWeight: FontWeight.w700)),
                            ]),
                          ),
                        ),
                      ),
                    );
                  }),
              ],
            ),
          ],
      ],
    ]);
  }
}
