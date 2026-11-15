import 'dart:convert';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../data.dart';
import '../test/engine.dart';
import '../test/test_screen.dart';

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

const _pages = {
  'cgl': ['app-ssc-cgl-pyq.html', 'app-ssc-cgl-tier-2-pyq.html'],
  'chsl': ['app-ssc-chsl-pyq.html'],
  'gd': ['app-ssc-gd-pyq.html'],
  'ntpc': ['app-rrb-ntpc-pyq.html'],
  'mts': <String>[],
};

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
  for (final page in _pages[exam.k] ?? const <String>[]) {
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
  final bool paid;
  final VoidCallback onReturn; // refresh DONE / Resume after a test
  const PyqTab({super.key, required this.user, required this.exam, required this.attempted, required this.resume, required this.paid, required this.onReturn});

  @override
  State<PyqTab> createState() => _PyqTabState();
}

class _PyqTabState extends State<PyqTab> {
  List<PyqPaper>? _all;
  bool _failed = false;
  int _tier = 1;
  String _year = '';

  @override
  void initState() {
    super.initState();
    _load();
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

  bool _done(PyqPaper p) => widget.attempted.contains(p.en) || widget.attempted.contains(p.hi);
  bool _paused(PyqPaper p) => widget.resume.containsKey(p.base);

  Future<void> _start(PyqPaper p) async {
    final exam = widget.exam;
    String lang = p.en.isNotEmpty ? 'en' : 'hi';
    String partD = lang;
    final both = p.en.isNotEmpty && p.hi.isNotEmpty;
    final saved = widget.resume[p.base];
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
                  Text(p.title, style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: exam.ink)),
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
                  if (exam.k == 'gd') ...[
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
      builder: (_) => TestFlow(
        user: widget.user,
        exam: exam,
        mockId: id,
        lang: lang,
        partD: exam.k == 'gd' ? partD : null,
        paid: widget.paid,
        title: p.title,
      ),
    ));
    widget.onReturn();
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    if ((_pagesFor(exam)).isEmpty) {
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
    final hasT2 = all.any((p) => p.tier == 2);
    final tierList = all.where((p) => p.tier == _tier).toList();
    final years = <String>{for (final p in tierList) p.year}.where((y) => y.isNotEmpty).toList()..sort((a, b) => b.compareTo(a));
    if (_year.isNotEmpty && !years.contains(_year)) _year = '';
    final list = tierList.where((p) => _year.isEmpty || p.year == _year).toList();
    final done = tierList.where(_done).length;

    Widget chip(String label, bool on, VoidCallback tap) => Padding(
          padding: const EdgeInsets.only(right: 8),
          child: Material(
            color: on ? exam.c1 : Colors.white,
            borderRadius: BorderRadius.circular(20),
            child: InkWell(
              borderRadius: BorderRadius.circular(20),
              onTap: tap,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: Text(label, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: on ? Colors.white : const Color(0xFF334155))),
              ),
            ),
          ),
        );

    return RefreshIndicator(
      onRefresh: () => _load(force: true),
      child: ListView(padding: EdgeInsets.fromLTRB(12, 10, 12, 16 + MediaQuery.of(context).padding.bottom), children: [
        Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(18),
            gradient: const LinearGradient(colors: [Color(0xFF1D4ED8), Color(0xFF60A5FA)], begin: Alignment.topLeft, end: Alignment.bottomRight),
          ),
          child: Row(children: [
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('${exam.name} previous year papers', style: const TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.w800)),
                const SizedBox(height: 2),
                Text('${tierList.length} papers · real exam shifts · Hindi & English', style: const TextStyle(color: Color(0xEEFFFFFF), fontSize: 13.5)),
              ]),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
              child: Column(children: [
                Text('$done', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900, color: Color(0xFF1D4ED8))),
                const Text('Done', style: TextStyle(fontSize: 12, color: Color(0xFF64748B))),
              ]),
            ),
          ]),
        ),
        const SizedBox(height: 10),
        if (hasT2)
          SizedBox(
            height: 40,
            child: ListView(scrollDirection: Axis.horizontal, children: [
              chip('Tier 1', _tier == 1, () => setState(() => _tier = 1)),
              chip('Tier 2', _tier == 2, () => setState(() => _tier = 2)),
            ]),
          ),
        if (hasT2) const SizedBox(height: 8),
        if (years.length > 1)
          SizedBox(
            height: 40,
            child: ListView(scrollDirection: Axis.horizontal, children: [
              chip('All years', _year.isEmpty, () => setState(() => _year = '')),
              for (final y in years) chip(y, _year == y, () => setState(() => _year = y)),
            ]),
          ),
        const SizedBox(height: 8),
        if (list.isEmpty) const Padding(padding: EdgeInsets.all(30), child: Center(child: Text('No papers here yet.'))),
        for (final p in list) _row(p),
      ]),
    );
  }

  List<String> _pagesFor(Exam e) => _pages[e.k] ?? const [];

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

  Widget _row(PyqPaper p) {
    final exam = widget.exam;
    final done = _done(p), paused = _paused(p);
    final langs = [if (p.en.isNotEmpty) 'EN', if (p.hi.isNotEmpty) 'हिंदी'].join(', ');
    Widget tag(String t, Color fg, Color bg) => Container(
          margin: const EdgeInsets.only(left: 6),
          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
          decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(6)),
          child: Text(t, style: TextStyle(color: fg, fontSize: 12, fontWeight: FontWeight.w800)),
        );
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Material(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: () => _start(p),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 10),
            child: Row(children: [
              Container(
                width: 50,
                height: 44,
                alignment: Alignment.center,
                decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), color: const Color(0xFFDBEAFE)),
                child: Text(p.year, style: const TextStyle(color: Color(0xFF1D4ED8), fontWeight: FontWeight.w900, fontSize: 14)),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Row(children: [
                    Flexible(child: Text(p.shift, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800))),
                    if (paused) tag('PAUSED', const Color(0xFFB45309), const Color(0xFFFEF3C7)) else if (done) tag('DONE', const Color(0xFF1D4ED8), const Color(0xFFDBEAFE)),
                  ]),
                  const SizedBox(height: 1),
                  Text([if (p.tier == 1) exam.meta else 'Tier 2 · 135 min', langs].join(' · '), maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 13.5, color: Color(0xFF475569))),
                ]),
              ),
              const SizedBox(width: 6),
              Container(
                width: 88,
                height: 36,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10),
                  gradient: LinearGradient(colors: paused ? const [Color(0xFFD97706), Color(0xFFFBBF24)] : [exam.c1, exam.c2]),
                ),
                child: Text(paused ? 'Resume' : (done ? 'Retake' : 'Start'), style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 15)),
              ),
            ]),
          ),
        ),
      ),
    );
  }
}
