import 'dart:convert';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../data.dart';
import '../test/engine.dart';
import '../test/test_screen.dart';
import '../ui/soft_list.dart';
import 'dash/logic.dart' show shortDate, n1, marksOf, maxOf;
import 'dash/pages.dart' show showDoneSheet;

/// One previous-year paper, read from the website's own PYQ list page.
class PyqPaper {
  final String en, hi; // paperIds
  final String title; // "SSC CGL Tier I 2026 · Shift-1 · 13 October 2026"
  final int tier; // 1 or 2
  PyqPaper(this.en, this.hi, this.title, this.tier);

  String get base => lbBase(en.isNotEmpty ? en : hi);
  String get year => RegExp(r'^[a-z-]+_(\d{4})_').firstMatch(base)?.group(1) ?? '';
  String get shift {
    final parts = title.split('·').map((e) => e.trim()).toList();
    return parts.length >= 3 ? '${parts[1]} · ${parts[2]}' : title;
  }

  Map<String, dynamic> toJson() => {'en': en, 'hi': hi, 't': title, 'tier': tier};
  factory PyqPaper.fromJson(Map j) => PyqPaper('${j['en'] ?? ''}', '${j['hi'] ?? ''}', '${j['t'] ?? ''}', (j['tier'] as num? ?? 1).toInt());
}

String _unesc(String s) => s.replaceAll('&amp;', '&').replaceAll('&quot;', '"').replaceAll('&#39;', "'").replaceAll('&middot;', '·');

List<PyqPaper> _parse(String html) {
  final out = <PyqPaper>[];
  final seen = <String>{};
  for (final m in RegExp(r'<(?:button|a)\b[^>]*data-pid-en="[^>]*>').allMatches(html)) {
    final tag = m.group(0)!;
    String attr(String n) => _unesc(RegExp('$n="([^"]*)"').firstMatch(tag)?.group(1) ?? '');
    final en = attr('data-pid-en'), hi = attr('data-pid-hi'), title = attr('data-title'), url = attr('data-en');
    if (en.isEmpty && hi.isEmpty) continue;
    final key = en.isNotEmpty ? en : hi;
    if (!seen.add(key)) continue;
    out.add(PyqPaper(en, hi, title, (url.contains('tier2') || key.contains('_tier2_')) ? 2 : 1));
  }
  return out;
}

const _months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

/// For an exam with no static PYQ list page (catalog `pyqFs`). SSC MTS used this until its list was
/// baked into ssc-mts.html (Nov 2026); kept for a future exam whose page is not built yet.
/// Reads the `papers` cards the batch uploader writes, plus Q1 of each paper in `questions` as a fallback.
Future<List<PyqPaper>> _loadFirestore(String examId, String label) async {
  final db = FirebaseFirestore.instance;
  final rows = <Map<String, dynamic>>[];
  try {
    final a = await db.collection('papers').where('exam', isEqualTo: examId).get();
    rows.addAll(a.docs.map((d) => {'paperId': d.id, ...d.data()}));
  } catch (_) {}
  for (final q in [1, '1']) {
    try {
      final b = await db.collection('questions').where('exam', isEqualTo: examId).where('qNum', isEqualTo: q).get();
      rows.addAll(b.docs.map((d) => d.data()));
    } catch (_) {}
  }
  String str(dynamic v) => v == null ? '' : '$v'.trim();
  final map = <String, Map<String, String>>{};
  for (final r in rows) {
    if (str(r['type']).toLowerCase() == 'mock' || str(r['mockId']).isNotEmpty) continue;
    final pid = str(r['paperId']);
    if (pid.isEmpty) continue;
    final hi = RegExp(r'^(hi|hindi)$', caseSensitive: false).hasMatch(str(r['language'])) || pid.endsWith('_hi');
    final key = [str(r['year']), str(r['shift']), str(r['heldOn']), str(r['tier'])].join('|');
    final m = map.putIfAbsent(key, () => {'year': str(r['year']), 'shift': str(r['shift']), 'heldOn': str(r['heldOn']), 'en': '', 'hi': ''});
    if (hi) {
      m['hi'] = m['hi']!.isEmpty ? pid : m['hi']!;
    } else {
      m['en'] = m['en']!.isEmpty ? pid : m['en']!;
    }
  }
  String date(String d) {
    final p = d.split('-');
    if (p.length != 3) return d;
    final mo = int.tryParse(p[1]) ?? 0;
    return mo >= 1 && mo <= 12 ? '${int.tryParse(p[2]) ?? p[2]} ${_months[mo - 1]} ${p[0]}' : d;
  }

  final list = map.values.toList()
    ..sort((a, b) {
      final y = (int.tryParse(b['year']!) ?? 0).compareTo(int.tryParse(a['year']!) ?? 0);
      if (y != 0) return y;
      final h = b['heldOn']!.compareTo(a['heldOn']!);
      return h != 0 ? h : a['shift']!.compareTo(b['shift']!);
    });
  return [
    for (final m in list)
      PyqPaper(m['en']!, m['hi']!, '$label ${m['year']} · ${m['shift']!.isEmpty ? 'Full Paper' : m['shift']} · ${date(m['heldOn']!)}', 1),
  ];
}

Future<List<PyqPaper>> loadPyqs(Exam exam, {bool force = false}) async {
  final prefs = await SharedPreferences.getInstance();
  final key = 'tssc_pyq_${exam.k}';
  if (!force) {
    try {
      final c = jsonDecode(prefs.getString(key) ?? '{}') as Map;
      final at = (c['at'] as num? ?? 0).toInt();
      if (DateTime.now().millisecondsSinceEpoch - at < 6 * 3600 * 1000 && c['p'] is List) {
        return [for (final j in c['p'] as List) PyqPaper.fromJson(j as Map)];
      }
    } catch (_) {}
  }
  final list = <PyqPaper>[];
  if (exam.pyqFs) list.addAll(await _loadFirestore(exam.id, exam.name));
  for (final page in exam.pyqPages) {
    final r = await http.get(Uri.parse('https://trickyssc.com/$page'));
    if (r.statusCode == 200) list.addAll(_parse(utf8.decode(r.bodyBytes)));
  }
  if (list.isNotEmpty) {
    await prefs.setString(key, jsonEncode({'at': DateTime.now().millisecondsSinceEpoch, 'p': [for (final p in list) p.toJson()]}));
  }
  return list;
}

class PyqTab extends StatefulWidget {
  final User user;
  final Exam exam;
  final Set<String> attempted;
  final Map<String, List<String>> resume;
  final Map<String, Map<String, dynamic>> last;
  final bool paid;
  final VoidCallback onReturn; // refresh DONE / Resume after a test
  const PyqTab({super.key, required this.user, required this.exam, required this.attempted, required this.resume, this.last = const {}, required this.paid, required this.onReturn});

  @override
  State<PyqTab> createState() => _PyqTabState();
}

class _PyqTabState extends State<PyqTab> {
  List<PyqPaper>? _all;
  bool _failed = false;
  int _tier = 1;
  String _year = '';
  // subject-wise PYQ: one section of each paper on its own clock ('' = the full paper). Tier 1 only.
  String _subject = '';
  Set<String> _subDone = <String>{};
  Map<String, Map<String, dynamic>> _subLast = {};

  @override
  void initState() {
    super.initState();
    _load();
    _loadSub();
    _loadSubPaused();
  }

  List<(String, String)> get _subjects {
    final e = widget.exam;
    if (e.secTests.isNotEmpty) return const [];
    const all = ['quant', 'reasoning', 'gk', 'english'];
    return [
      for (final k in all)
        if (e.subjects.contains(k)) (k, k == 'quant' ? (e.maths ? 'Maths' : 'Quant') : k == 'reasoning' ? 'Reasoning' : k == 'gk' ? 'Gen. Awareness' : (e.partD ? 'English / Hindi' : 'English')),
    ];
  }

  String get _subLabel => _subjects.firstWhere((s) => s.$1 == _subject, orElse: () => ('', '')).$2;

  Future<void> _loadSub() async {
    try {
      final list = await loadAttempts(widget.user.uid);
      final done = <String>{};
      final m = <String, Map<String, dynamic>>{};
      for (final a in list) {
        final id = '${a['paperId'] ?? ''}';
        if (!id.contains('__')) continue;
        final key = id.replaceAll(RegExp(r'_(en|hi)__'), '__');
        done.add(key);
        m.putIfAbsent(key, () => a);
      }
      if (mounted) setState(() { _subDone = done; _subLast = m; });
    } catch (_) {}
  }

  Future<void> _load({bool force = false}) async {
    setState(() => _failed = false);
    try {
      final l = await loadPyqs(widget.exam, force: force);
      if (mounted) setState(() => _all = l);
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  bool get _sub => _subject.isNotEmpty && _tier == 1;
  bool _done(PyqPaper p) => _sub ? _subDone.contains('${p.base}__$_subject') : (widget.attempted.contains(p.en) || widget.attempted.contains(p.hi));
  Map<String, List<String>> _subPaused = {};
  void _loadSubPaused() => loadInProgress(widget.user.uid).then((r) {
        if (mounted) setState(() => _subPaused = r);
      });
  bool _paused(PyqPaper p) => _sub ? _subPaused.containsKey('${p.base}__$_subject') : widget.resume.containsKey(p.base);

  Future<void> _start(PyqPaper p) async {
    final exam = widget.exam;
    String lang = p.en.isNotEmpty ? 'en' : 'hi';
    String partD = lang;
    final both = p.en.isNotEmpty && p.hi.isNotEmpty;
    final sub = _sub ? _subject : '';
    final saved = sub.isEmpty ? widget.resume[p.base] : _subPaused['${p.base}__$sub'];
    if (saved != null) {
      lang = saved[0];
      partD = saved[1].isEmpty ? lang : saved[1];
    } else if (both) {
      final picked = await showModalBottomSheet<List<String>>(
        context: context,
        backgroundColor: Colors.white,
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
        builder: (c) {
          var l = lang, d = partD;
          return StatefulBuilder(builder: (c, set) {
            Widget opt(String label, bool on, VoidCallback tap) => Expanded(
                  child: Material(
                    color: on ? Color.lerp(Colors.white, exam.c2, 0.3) : const Color(0xFFF1F5F9),
                    borderRadius: BorderRadius.circular(12),
                    child: InkWell(
                      borderRadius: BorderRadius.circular(12),
                      onTap: tap,
                      child: Container(
                        height: 48,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), border: Border.all(color: on ? exam.c1 : Colors.transparent, width: 2)),
                        child: Text(label, style: TextStyle(fontWeight: FontWeight.w800, color: on ? exam.c1 : const Color(0xFF334155))),
                      ),
                    ),
                  ),
                );
            return SafeArea(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 12),
                child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                  Text(sub.isEmpty ? p.title : '${p.title} · $_subLabel', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: exam.ink)),
                  const SizedBox(height: 12),
                  const Text('Paper language', style: TextStyle(fontWeight: FontWeight.w700, color: Color(0xFF475569))),
                  const SizedBox(height: 6),
                  Row(children: [
                    opt('English', l == 'en', () => set(() {
                          if (d == l) d = 'en';
                          l = 'en';
                        })),
                    const SizedBox(width: 8),
                    opt('हिंदी', l == 'hi', () => set(() {
                          if (d == l) d = 'hi';
                          l = 'hi';
                        })),
                  ]),
                  if (exam.partD && sub.isEmpty) ...[
                    const SizedBox(height: 12),
                    const Text('Part D (Q61–80)', style: TextStyle(fontWeight: FontWeight.w700, color: Color(0xFF475569))),
                    const SizedBox(height: 6),
                    Row(children: [
                      opt('English', d == 'en', () => set(() => d = 'en')),
                      const SizedBox(width: 8),
                      opt('Hindi', d == 'hi', () => set(() => d = 'hi')),
                    ]),
                  ],
                  const SizedBox(height: 14),
                  FilledButton(
                    onPressed: () => Navigator.pop(c, [l, d]),
                    style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                    child: const Text('Continue', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
                  ),
                ]),
              ),
            );
          });
        },
      );
      if (picked == null || !mounted) return;
      lang = picked[0];
      partD = picked[1];
    }
    final id = lang == 'hi' ? p.hi : p.en;
    await Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => sub.isEmpty
          ? TestFlow(
              user: widget.user,
              exam: exam,
              mockId: id,
              lang: lang,
              partD: exam.partD ? partD : null,
              paid: widget.paid,
              title: p.title,
            )
          : TestFlow(
              user: widget.user,
              exam: exam,
              mockId: '${id}__$sub',
              lang: lang,
              paid: widget.paid,
              title: '${p.title} · $_subLabel',
              loader: () => loadPaper(id, lang, subject: sub, title: p.title),
            ),
    ));
    widget.onReturn();
    if (sub.isNotEmpty) _loadSub();
    _loadSubPaused();
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    if (exam.pyqPages.isEmpty && !exam.pyqFs) {
      return _empty(Icons.description_outlined, '${exam.name} previous year papers', 'Coming soon. Meanwhile, practise with the full mocks.');
    }
    if (_failed) {
      return Center(
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          const Text('Could not load the papers. Check your internet.'),
          TextButton(onPressed: () => _load(force: true), child: const Text('Try again')),
        ]),
      );
    }
    final all = _all;
    if (all == null) return const Center(child: CircularProgressIndicator());
    if (all.isEmpty) {
      return RefreshIndicator(
        onRefresh: () => _load(force: true),
        child: ListView(physics: const AlwaysScrollableScrollPhysics(), children: [
          const SizedBox(height: 120),
          _empty(Icons.description_outlined, '${exam.name} previous year papers', 'No papers yet. Pull down to refresh.'),
        ]),
      );
    }
    final hasT2 = all.any((p) => p.tier == 2);
    final tierList = all.where((p) => p.tier == _tier).toList();
    final years = <String>{for (final p in tierList) p.year}.where((y) => y.isNotEmpty).toList()..sort((a, b) => b.compareTo(a));
    if (_year.isNotEmpty && !years.contains(_year)) _year = '';
    final list = tierList.where((p) => _year.isEmpty || p.year == _year).toList();
    final done = tierList.where(_done).length;

    return RefreshIndicator(
      onRefresh: () => _load(force: true),
      child: ListView(padding: EdgeInsets.fromLTRB(16, 8, 16, 16 + MediaQuery.of(context).padding.bottom), children: [
        SoftSummary(
          icon: 'paper',
          title: _sub ? '$_subLabel · $done of ${tierList.length} done' : '$done of ${tierList.length} done',
          progress: tierList.isEmpty ? 0 : done / tierList.length,
          sub: _sub ? 'Only the $_subLabel section of each paper · ${subjectMockMinutes('${exam.id}_', _subject)} min' : 'Real exam shifts · Hindi & English',
          accent: exam.c1,
          pct: true,
        ),
        const SizedBox(height: 12),
        // TSSC-LISTUI-V2
        if (hasT2) ...[
          SoftTabs(
            items: [('Tier 1 (${all.where((p) => p.tier == 1).length})', Icons.emoji_events_outlined), ('Tier 2 (${all.where((p) => p.tier == 2).length})', Icons.layers_outlined)],
            index: _tier == 2 ? 1 : 0,
            accent: exam.c1,
            onTap: (i) => setState(() => _tier = i + 1),
          ),
          const SizedBox(height: 12),
        ],
        if (_tier == 1 && _subjects.isNotEmpty)
          SubjectTiles(
            items: [('', 'Full Paper'), for (final s in _subjects) (s.$1, s.$2)],
            selected: _subject,
            accent: exam.c1,
            onTap: (k) => setState(() => _subject = k),
          ),
        if (years.length > 1)
          SizedBox(
            height: 46,
            child: ListView(scrollDirection: Axis.horizontal, children: [
              SoftChip('All Years (${tierList.length})', _year.isEmpty, exam.c1, () => setState(() => _year = ''), icon: Icons.calendar_month_outlined),
              for (final y in years) SoftChip('$y (${tierList.where((p) => p.year == y).length})', _year == y, exam.c1, () => setState(() => _year = y), icon: Icons.calendar_today_outlined),
            ]),
          ),
        const SizedBox(height: 8),
        if (list.isEmpty) const Padding(padding: EdgeInsets.all(30), child: Center(child: Text('No papers here yet.'))),
        for (var i = 0; i < list.length; i++) _row(list[i], i),
      ]),
    );
  }


  Widget _empty(IconData icon, String title, String text) => Center(
        child: Padding(
          padding: const EdgeInsets.all(28),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            Icon(icon, size: 46, color: widget.exam.c1),
            const SizedBox(height: 10),
            Text(title, textAlign: TextAlign.center, style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: widget.exam.ink)),
            const SizedBox(height: 6),
            Text(text, textAlign: TextAlign.center, style: const TextStyle(fontSize: 15, color: Color(0xFF64748B))),
          ]),
        ),
      );

  Widget _row(PyqPaper p, int i) {
    final exam = widget.exam;
    final done = _done(p), paused = _paused(p);
    final langs = [if (p.en.isNotEmpty) 'EN', if (p.hi.isNotEmpty) 'हिंदी'].join(', ');
    final parts = p.title.split('·').map((e) => e.trim()).where((e) => e.isNotEmpty).toList();
    String shortMonths(String t) => t.replaceAllMapped(RegExp(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b'), (m) => m[1]!.substring(0, 3) == 'Sep' ? 'Sept' : m[1]!.substring(0, 3));
    final title = parts.isEmpty ? p.year : parts.first.replaceFirst(RegExp(r'^SSC\s+'), '');
    final sub = shortMonths(parts.length > 1 ? parts.sublist(1).reversed.join(' · ') : p.shift);
    final a = _sub ? _subLast['${p.base}__$_subject'] : widget.last[p.base];
    final state = paused ? RowState.progress : (done ? RowState.done : RowState.todo);
    final em = exam.meta.split(' · ');
    return TestRow(
      tags: const [SoftTag('ORIGINAL PYQ', Color(0xFF1D4ED8), Color(0xFFDBEAFE)), SoftTag.free()],
      title: _sub ? '$title · $_subLabel' : title,
      sub: '$sub${langs.isNotEmpty ? ' · $langs' : ''}',
      meta: [
        if (state == RowState.done && a != null) (Icons.calendar_today_outlined, shortDate(attemptMs(a))) else (Icons.help_outline_rounded, _sub ? 'Sectional' : (p.tier == 1 ? em.first : 'Tier 2')),
        (Icons.schedule_rounded, _sub ? '${subjectMockMinutes('${exam.id}_', _subject)} min' : (p.tier == 1 && em.length > 1 ? em[1] : '135 min')),
      ],
      state: state,
      score: state == RowState.done && a != null ? '${n1(marksOf(a))} / ${n1(maxOf(a))}' : null,
      accent: exam.c1,
      bar: rowBar(i),
      onTap: () => state == RowState.done ? showDoneSheet(context, user: widget.user, exam: exam, a: a, title: _sub ? '${p.title} · $_subLabel' : p.title, onRetake: () => _start(p)) : _start(p),
      onAction: state == RowState.done ? () => _start(p) : null,
    );
  }

}
