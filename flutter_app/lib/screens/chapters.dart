import 'dart:convert';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../data.dart';
import '../test/engine.dart';
import '../test/test_screen.dart';

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
];

List<ChSubject> subjectsFor(Exam e) => [
      for (final s in _subjects)
        if ((s.key != 'computer' || e.k == 'cgl' || e.k == 'chsl') && (s.key != 'finance' || e.k == 'cgl')) s
    ];

class ChChapter {
  final String id, name, icon;
  ChChapter(this.id, this.name, this.icon);
}

String _unesc(String s) => s.replaceAll('&amp;', '&').replaceAll('&quot;', '"').replaceAll('&#39;', "'").replaceAll('&nbsp;', ' ');

Future<List<ChChapter>> _loadChapters(ChSubject s) async {
  final prefs = await SharedPreferences.getInstance();
  final key = 'tssc_chlist_${s.key}';
  try {
    final c = jsonDecode(prefs.getString(key) ?? '{}') as Map;
    if (DateTime.now().millisecondsSinceEpoch - ((c['at'] as num?) ?? 0) < 24 * 3600 * 1000 && c['l'] is List) {
      return [for (final j in c['l'] as List) ChChapter('${j[0]}', '${j[1]}', '${j[2]}')];
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
    final ico = RegExp(r'class="ch-ico"[^>]*>([^<]*)<').firstMatch(block)?.group(1)?.trim() ?? '';
    if (seen.add(id)) out.add(ChChapter(id, name, ico));
  }
  if (out.isNotEmpty) {
    await prefs.setString(key, jsonEncode({'at': DateTime.now().millisecondsSinceEpoch, 'l': [for (final c in out) [c.id, c.name, c.icon]]}));
  }
  return out;
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
    return examTheme(
      context,
      exam,
      Scaffold(
        backgroundColor: Color.lerp(Colors.white, exam.c2, 0.10),
        appBar: AppBar(title: Text('Chapter tests', style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: ListView(padding: const EdgeInsets.all(12), children: [
          Container(
            padding: const EdgeInsets.all(14),
            margin: const EdgeInsets.only(bottom: 10),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(18),
              gradient: const LinearGradient(colors: [Color(0xFF047857), Color(0xFF34D399)], begin: Alignment.topLeft, end: Alignment.bottomRight),
            ),
            child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Practise chapter by chapter', style: TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.w800)),
              SizedBox(height: 2),
              Text('25-question tests · Level 1 (exam level) and Level 2 (above exam level) · Hindi & English', style: TextStyle(color: Color(0xEEFFFFFF), fontSize: 13.5)),
            ]),
          ),
          for (var i = 0; i < list.length; i += 2)
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Row(children: [
                Expanded(child: _tile(context, list[i])),
                const SizedBox(width: 8),
                Expanded(child: i + 1 < list.length ? _tile(context, list[i + 1]) : const SizedBox()),
              ]),
            ),
        ]),
      ),
    );
  }

  Widget _tile(BuildContext context, ChSubject s) => SizedBox(
        height: 130,
        child: Material(
          color: Colors.transparent,
          borderRadius: BorderRadius.circular(18),
          child: Ink(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(18),
              gradient: LinearGradient(colors: [s.c1, Color.lerp(s.c1, s.c2, 0.6)!], begin: Alignment.topLeft, end: Alignment.bottomRight),
            ),
            child: InkWell(
              borderRadius: BorderRadius.circular(18),
              onTap: () => Navigator.of(context).push(MaterialPageRoute(
                builder: (_) => SubjectChaptersScreen(user: user, exam: exam, subject: s, paid: paid, attempted: attempted, onReturn: onReturn),
              )),
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(color: const Color(0x33FFFFFF), borderRadius: BorderRadius.circular(12)),
                    child: Icon(s.icon, color: Colors.white, size: 26),
                  ),
                  const Spacer(),
                  Text(s.name, maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Colors.white, fontSize: 16.5, fontWeight: FontWeight.w900, height: 1.15)),
                ]),
              ),
            ),
          ),
        ),
      );
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
    return examTheme(
      context,
      exam,
      Scaffold(
        backgroundColor: Color.lerp(Colors.white, exam.c2, 0.10),
        appBar: AppBar(title: Text(s.name, style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: _failed
            ? Center(
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  const Text('Could not load the chapters. Check your internet.'),
                  TextButton(onPressed: _load, child: const Text('Try again')),
                ]),
              )
            : chs == null
                ? const Center(child: CircularProgressIndicator())
                : ListView(padding: EdgeInsets.fromLTRB(12, 10, 12, 16 + MediaQuery.of(context).padding.bottom), children: [
                    if (_n == null)
                      const Padding(padding: EdgeInsets.only(bottom: 10), child: LinearProgressIndicator()),
                    for (final c in (_n == null ? chs : live)) _row(c, n[c.id]),
                    if (soon.isNotEmpty) ...[
                      const Padding(
                        padding: EdgeInsets.fromLTRB(4, 12, 4, 6),
                        child: Text('Coming soon', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: Color(0xFF64748B))),
                      ),
                      for (final c in soon) _row(c, 0),
                    ],
                  ]),
      ),
    );
  }

  Widget _row(ChChapter c, int? tests) {
    final s = widget.subject;
    final soon = tests == 0;
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Material(
        color: soon ? const Color(0xFFF8FAFC) : Colors.white,
        borderRadius: BorderRadius.circular(14),
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: soon
              ? null
              : () => Navigator.of(context).push(MaterialPageRoute(
                    builder: (_) => ChapterTestsScreen(user: widget.user, exam: widget.exam, subject: s, chapter: c, paid: widget.paid, attempted: widget.attempted, onReturn: widget.onReturn),
                  )),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 11),
            child: Row(children: [
              Container(
                width: 42,
                height: 42,
                alignment: Alignment.center,
                decoration: BoxDecoration(color: Color.lerp(Colors.white, s.c2, soon ? 0.2 : 0.45), borderRadius: BorderRadius.circular(12)),
                child: c.icon.isNotEmpty ? Text(c.icon, style: const TextStyle(fontSize: 20)) : Icon(s.icon, color: s.c1),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(c.name, maxLines: 2, overflow: TextOverflow.ellipsis, style: TextStyle(fontSize: 15.5, fontWeight: FontWeight.w700, color: soon ? const Color(0xFF94A3B8) : null)),
              ),
              const SizedBox(width: 8),
              if (tests == null)
                const SizedBox()
              else if (soon)
                const Text('Soon', style: TextStyle(fontSize: 13, color: Color(0xFF94A3B8), fontWeight: FontWeight.w700))
              else
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 4),
                  decoration: BoxDecoration(color: Color.lerp(Colors.white, s.c2, 0.4), borderRadius: BorderRadius.circular(8)),
                  child: Text('$tests test${tests == 1 ? '' : 's'}', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800, color: s.c1)),
                ),
              if (!soon) Icon(Icons.chevron_right, color: s.c1),
            ]),
          ),
        ),
      ),
    );
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

  @override
  void initState() {
    super.initState();
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
    if (langs.length > 1) {
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
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam, s = widget.subject, ch = widget.chapter;
    final by = _by;
    const levels = [(1, 'SSC CGL Level', Color(0xFF00A86B)), (2, 'Above SSC CGL Level', Color(0xFFEF4444))];
    return examTheme(
      context,
      exam,
      Scaffold(
        backgroundColor: Color.lerp(Colors.white, exam.c2, 0.10),
        appBar: AppBar(title: Text(ch.name, maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: _failed
            ? Center(
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  const Text('Could not load the tests. Check your internet.'),
                  TextButton(onPressed: _load, child: const Text('Try again')),
                ]),
              )
            : by == null
                ? const Center(child: CircularProgressIndicator())
                : ListView(padding: EdgeInsets.fromLTRB(12, 10, 12, 16 + MediaQuery.of(context).padding.bottom), children: [
                    if (by.isEmpty) const Padding(padding: EdgeInsets.all(30), child: Center(child: Text('No tests in this chapter yet.'))),
                    for (final lv in levels)
                      if (by[lv.$1] != null) ...[
                        Padding(
                          padding: const EdgeInsets.fromLTRB(2, 8, 2, 8),
                          child: Row(children: [
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 4),
                              decoration: BoxDecoration(color: lv.$3, borderRadius: BorderRadius.circular(8)),
                              child: Text('Level ${lv.$1}', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 13)),
                            ),
                            const SizedBox(width: 8),
                            Expanded(child: Text(lv.$2, style: const TextStyle(fontSize: 15.5, fontWeight: FontWeight.w800))),
                            Text('${by[lv.$1]!.length} tests', style: const TextStyle(fontSize: 13, color: Color(0xFF64748B))),
                          ]),
                        ),
                        GridView.count(
                          crossAxisCount: 3,
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          mainAxisSpacing: 8,
                          crossAxisSpacing: 8,
                          childAspectRatio: 1.15,
                          children: [
                            for (final tn in (by[lv.$1]!.keys.toList()..sort()))
                              Builder(builder: (_) {
                                final langs = by[lv.$1]![tn]!;
                                final done = _attempted.contains(cwLbKey(ch.id, lv.$1, tn));
                                return Material(
                                  color: Colors.white,
                                  borderRadius: BorderRadius.circular(14),
                                  child: InkWell(
                                    borderRadius: BorderRadius.circular(14),
                                    onTap: () => _open(lv.$1, tn, langs),
                                    child: Container(
                                      decoration: BoxDecoration(borderRadius: BorderRadius.circular(14), border: Border.all(color: done ? s.c1 : const Color(0xFFE2E8F0), width: done ? 1.6 : 1)),
                                      padding: const EdgeInsets.all(8),
                                      child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                                        Text('Test $tn', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w900, color: s.c1)),
                                        const SizedBox(height: 2),
                                        Text(done ? '✓ Done' : '25 Qs', style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w700, color: done ? const Color(0xFF16A34A) : const Color(0xFF64748B))),
                                        Text(langs.length > 1 ? 'EN · हिंदी' : (langs.contains('hi') ? 'हिंदी' : 'English'), style: const TextStyle(fontSize: 12, color: Color(0xFF94A3B8))),
                                      ]),
                                    ),
                                  ),
                                );
                              }),
                          ],
                        ),
                        const SizedBox(height: 8),
                      ],
                  ]),
      ),
    );
  }
}
