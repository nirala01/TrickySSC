// Chapter-wise PYQs: previous-year questions of SSC CGL, CHSL, GD, MTS and RRB NTPC grouped by chapter.
// Reads the lists the website's nightly "Build chapter-wise PYQ tests" Action publishes in /pyq-chapters/.
import 'dart:convert';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../data.dart';
import '../test/engine.dart';
import '../test/test_screen.dart';
import '../ui/icons3d.dart';
import '../ui/nav.dart';
import '../ui/soft.dart';
import '../ui/soft_list.dart';

const _base = 'https://trickyssc.com/pyq-chapters/';

const _subjects = [
  ('quant', 'Quantitative Aptitude', 'pencil'),
  ('reasoning', 'Reasoning', 'puzzle'),
  ('english', 'English', 'book'),
  ('ga', 'General Awareness', 'news'),
  ('computer', 'Computer', 'clip'),
  ('hindi', 'Hindi', 'paper'),
];

const _examShort = {'ssc-cgl': 'CGL', 'ssc-chsl': 'CHSL', 'ssc-gd': 'GD', 'ssc-mts': 'MTS', 'ssc-rrb-ntpc': 'NTPC', 'rrb-ntpc': 'NTPC'};

class _Ch {
  final String id, name, subject;
  final int count, tests;
  final bool hi;
  final Map<String, int> exams;
  _Ch(this.id, this.name, this.subject, this.count, this.tests, this.hi, this.exams);
}

Future<Map<String, List<_Ch>>> _loadIndex({bool force = false}) async {
  final prefs = await SharedPreferences.getInstance();
  const key = 'tssc_pyqch_index';
  String? body;
  if (!force) {
    try {
      final c = jsonDecode(prefs.getString(key) ?? '{}') as Map;
      if (DateTime.now().millisecondsSinceEpoch - ((c['at'] as num?) ?? 0) < 6 * 3600 * 1000) body = c['b'] as String?;
    } catch (_) {}
  }
  if (body == null) {
    final r = await http.get(Uri.parse('${_base}index.json?t=${DateTime.now().millisecondsSinceEpoch ~/ 600000}'));
    if (r.statusCode != 200) throw 'http';
    body = utf8.decode(r.bodyBytes);
    await prefs.setString(key, jsonEncode({'at': DateTime.now().millisecondsSinceEpoch, 'b': body}));
  }
  final j = jsonDecode(body) as Map;
  final out = <String, List<_Ch>>{};
  (j['subjects'] as Map? ?? {}).forEach((k, v) {
    out['$k'] = [
      for (final c in (v as List))
        _Ch('${c['id']}', '${c['name']}', '$k', (c['count'] as num? ?? 0).toInt(), (c['tests'] as num? ?? 0).toInt(), c['hi'] == true,
            Map<String, int>.from(((c['exams'] as Map?) ?? {}).map((a, b) => MapEntry('$a', (b as num).toInt()))))
    ];
  });
  return out;
}

// ======================================================================= subjects

class ChapterPyqScreen extends StatefulWidget {
  final User user;
  final Exam exam;
  final bool paid;
  final Set<String> attempted;
  final VoidCallback onReturn;
  const ChapterPyqScreen({super.key, required this.user, required this.exam, required this.paid, required this.attempted, required this.onReturn});

  @override
  State<ChapterPyqScreen> createState() => _ChapterPyqScreenState();
}

class _ChapterPyqScreenState extends State<ChapterPyqScreen> {
  Map<String, List<_Ch>>? _idx;
  bool _failed = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load({bool force = false}) async {
    setState(() => _failed = false);
    try {
      final i = await _loadIndex(force: force);
      if (mounted) setState(() => _idx = i);
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final idx = _idx;
    return examTheme(
      context,
      exam,
      Scaffold(
        appBar: AppBar(actions: const [HomeButton()], title: Text('Chapter PYQs', style: baloo(22))),
        body: _failed
            ? Center(
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  const Text('Could not load the chapters. Check your internet.'),
                  TextButton(onPressed: () => _load(force: true), child: const Text('Try again')),
                ]),
              )
            : idx == null
                ? const Center(child: CircularProgressIndicator())
                : RefreshIndicator(
                    onRefresh: () => _load(force: true),
                    child: ListView(padding: EdgeInsets.fromLTRB(16, 8, 16, 16 + MediaQuery.of(context).padding.bottom), children: [
                      Builder(builder: (_) {
                        var tests = 0, qs = 0;
                        for (final l in idx.values) {
                          for (final c in l) {
                            tests += c.tests;
                            qs += c.count;
                          }
                        }
                        return SoftSummary(
                          icon: 'folder',
                          title: '$tests tests · $qs questions',
                          progress: 1,
                          sub: 'Real questions from CGL, CHSL, GD, MTS and NTPC, chapter by chapter',
                          accent: exam.c1,
                        );
                      }),
                      const SizedBox(height: 12),
                      for (final s in _subjects)
                        if ((idx[s.$1] ?? const []).isNotEmpty)
                          Builder(builder: (_) {
                            final list = idx[s.$1]!;
                            final tests = list.fold<int>(0, (a, c) => a + c.tests);
                            return Padding(
                              padding: const EdgeInsets.only(bottom: 10),
                              child: Material(
                                color: Colors.transparent,
                                child: Ink(
                                  decoration: softCard(radius: 20),
                                  child: InkWell(
                                    borderRadius: BorderRadius.circular(20),
                                    onTap: () => Navigator.of(context).push(MaterialPageRoute(
                                      builder: (_) => _ChaptersScreen(user: widget.user, exam: exam, title: s.$2, chapters: list, paid: widget.paid, attempted: widget.attempted, onReturn: widget.onReturn),
                                    )),
                                    child: Padding(
                                      padding: const EdgeInsets.all(12),
                                      child: Row(children: [
                                        Container(width: 54, height: 54, alignment: Alignment.center, decoration: softWell(), child: Icon3D(s.$3, size: 40)),
                                        const SizedBox(width: 12),
                                        Expanded(
                                          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                                            Text(s.$2, style: baloo(18)),
                                            Text('${list.length} chapters · $tests tests', style: TextStyle(fontSize: 13.5, color: exam.c1, fontWeight: FontWeight.w800)),
                                          ]),
                                        ),
                                        Icon(Icons.chevron_right_rounded, color: exam.c1),
                                      ]),
                                    ),
                                  ),
                                ),
                              ),
                            );
                          }),
                    ]),
                  ),
      ),
    );
  }
}

// ======================================================================= chapters of a subject

class _ChaptersScreen extends StatelessWidget {
  final User user;
  final Exam exam;
  final String title;
  final List<_Ch> chapters;
  final bool paid;
  final Set<String> attempted;
  final VoidCallback onReturn;
  const _ChaptersScreen({required this.user, required this.exam, required this.title, required this.chapters, required this.paid, required this.attempted, required this.onReturn});

  @override
  Widget build(BuildContext context) {
    final live = chapters.where((c) => c.tests > 0).toList();
    final soon = chapters.where((c) => c.tests == 0).toList();
    Widget row(_Ch c, int i) => SoftRow(
          badge: c.tests > 0 ? '${c.tests}' : '–',
          title: c.name,
          tags: [
            for (final e in (c.exams.entries.toList()..sort((a, b) => b.value.compareTo(a.value))).take(3))
              SoftTag('${_examShort[e.key] ?? e.key} ${e.value}', exam.c1, Color.lerp(Colors.white, exam.c1, .12)!),
          ],
          meta: '${c.count} questions · ${c.tests} test${c.tests == 1 ? '' : 's'}${c.hi ? ' · EN, हिंदी' : ''}',
          action: c.tests > 0 ? 'Open' : null,
          accent: exam.c1,
          onTap: c.tests == 0
              ? () {}
              : () => Navigator.of(context).push(MaterialPageRoute(
                    builder: (_) => _TestsScreen(user: user, exam: exam, ch: c, paid: paid, attempted: attempted, onReturn: onReturn),
                  )),
        );
    return examTheme(
      context,
      exam,
      Scaffold(
        appBar: AppBar(actions: const [HomeButton()], title: Text(title, style: baloo(21))),
        body: ListView(padding: EdgeInsets.fromLTRB(16, 8, 16, 16 + MediaQuery.of(context).padding.bottom), children: [
          for (var i = 0; i < live.length; i++) row(live[i], i),
          if (soon.isNotEmpty) ...[
            const Padding(padding: EdgeInsets.fromLTRB(4, 8, 4, 8), child: Text('Collecting questions', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: softMuted))),
            for (var i = 0; i < soon.length; i++) row(soon[i], i),
          ],
        ]),
      ),
    );
  }
}

// ======================================================================= tests of a chapter

class _TestsScreen extends StatefulWidget {
  final User user;
  final Exam exam;
  final _Ch ch;
  final bool paid;
  final Set<String> attempted;
  final VoidCallback onReturn;
  const _TestsScreen({required this.user, required this.exam, required this.ch, required this.paid, required this.attempted, required this.onReturn});

  @override
  State<_TestsScreen> createState() => _TestsScreenState();
}

class _TestsScreenState extends State<_TestsScreen> {
  List<(int, List<PyqRef>)>? _sets;
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
      final r = await http.get(Uri.parse('${_base}all/${Uri.encodeComponent(widget.ch.id)}.json?t=${DateTime.now().millisecondsSinceEpoch ~/ 600000}'));
      if (r.statusCode != 200) throw 'http';
      final j = jsonDecode(utf8.decode(r.bodyBytes)) as Map;
      final sets = <(int, List<PyqRef>)>[
        for (final s in (j['sets'] as List? ?? const []))
          ((s['n'] as num).toInt(), [for (final x in (s['qs'] as List)) PyqRef('${x['en'] ?? ''}', '${x['hi'] ?? ''}', '${x['p'] ?? ''}', (x['q'] as num? ?? 0).toInt())]),
      ];
      if (mounted) setState(() => _sets = sets);
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  String _key(int n) => 'cwp_ssc_all_${widget.ch.id.replaceAll(RegExp(r'[^a-zA-Z0-9]'), '')}_T$n';

  Future<void> _open(int n, List<PyqRef> refs) async {
    final exam = widget.exam, ch = widget.ch;
    var lang = 'en';
    if (ch.hi && refs.any((r) => r.hi.isNotEmpty)) {
      final picked = await showModalBottomSheet<String>(
        context: context,
        backgroundColor: Colors.white,
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
        builder: (c) => SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 12),
            child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              Text('${ch.name} · Test $n', style: baloo(18)),
              const SizedBox(height: 12),
              Row(children: [
                for (final l in const [('en', 'English'), ('hi', 'हिंदी')]) ...[
                  Expanded(
                    child: FilledButton(
                      onPressed: () => Navigator.pop(c, l.$1),
                      style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50)),
                      child: Text(l.$2, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
                    ),
                  ),
                  if (l.$1 == 'en') const SizedBox(width: 10),
                ],
              ]),
            ]),
          ),
        ),
      );
      if (picked == null || !mounted) return;
      lang = picked;
    }
    await Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => TestFlow(
        user: widget.user,
        exam: exam,
        mockId: '${_key(n)}_$lang',
        lang: lang,
        paid: widget.paid,
        title: '${ch.name} · PYQ Test $n',
        loader: () => loadChapterPyqTest(chapterId: ch.id, chapterName: ch.name, subject: ch.subject, testNum: n, refs: refs, lang: lang),
      ),
    ));
    widget.onReturn();
    final a = await loadAttempted(widget.user.uid);
    if (mounted) setState(() => _attempted = a);
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam, ch = widget.ch;
    final sets = _sets;
    final done = sets == null ? 0 : sets.where((s) => _attempted.contains(_key(s.$1))).length;
    return examTheme(
      context,
      exam,
      Scaffold(
        appBar: AppBar(actions: const [HomeButton()], title: Text(ch.name, maxLines: 1, overflow: TextOverflow.ellipsis, style: baloo(20))),
        body: _failed
            ? Center(
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  const Text('Could not load the tests. Check your internet.'),
                  TextButton(onPressed: _load, child: const Text('Try again')),
                ]),
              )
            : sets == null
                ? const Center(child: CircularProgressIndicator())
                : ListView(padding: EdgeInsets.fromLTRB(16, 8, 16, 16 + MediaQuery.of(context).padding.bottom), children: [
                    SoftSummary(
                      icon: 'folder',
                      title: '$done of ${sets.length} done',
                      progress: sets.isEmpty ? 0 : done / sets.length,
                      sub: '${ch.count} real exam questions · oldest papers first',
                      accent: exam.c1,
                    ),
                    const SizedBox(height: 12),
                    if (sets.isEmpty) const Padding(padding: EdgeInsets.all(30), child: Center(child: Text('No tests in this chapter yet.'))),
                    for (final s in sets)
                      Builder(builder: (_) {
                        final isDone = _attempted.contains(_key(s.$1));
                        final first = s.$2.isEmpty ? '' : s.$2.first.paper.split('·').first.trim();
                        final last = s.$2.isEmpty ? '' : s.$2.last.paper.split('·').first.trim();
                        return SoftRow(
                          badge: '${s.$1}',
                          title: 'Test ${s.$1}',
                          tags: [if (isDone) const SoftTag.done()],
                          meta: '${s.$2.length} Qs · ${first == last ? first : '$first → $last'}',
                          action: isDone ? 'Retake' : 'Start',
                          accent: exam.c1,
                          onTap: () => _open(s.$1, s.$2),
                        );
                      }),
                  ]),
      ),
    );
  }
}
