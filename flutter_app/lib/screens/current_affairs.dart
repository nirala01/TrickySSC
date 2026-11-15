import 'dart:convert';

import 'package:flutter/material.dart';
import '../ui/nav.dart';
import 'package:flutter_widget_from_html_core/flutter_widget_from_html_core.dart';
import 'package:http/http.dart' as http;

import '../data.dart';

const _base = 'https://trickyssc.com/ca-archive/';
const _months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const _weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

DateTime? _dateOf(String file) {
  final m = RegExp(r'^(\d{2})-(\d{2})-(\d{4})\.html$').firstMatch(file);
  if (m == null) return null;
  return DateTime(int.parse(m[3]!), int.parse(m[2]!), int.parse(m[1]!));
}

// ======================================================================= list

class CurrentAffairsScreen extends StatefulWidget {
  final Exam exam;
  const CurrentAffairsScreen({super.key, required this.exam});

  @override
  State<CurrentAffairsScreen> createState() => _CurrentAffairsScreenState();
}

class _CurrentAffairsScreenState extends State<CurrentAffairsScreen> {
  List<(String, DateTime)>? _days;
  bool _failed = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _failed = false);
    try {
      final r = await http.get(Uri.parse('${_base}index.json?t=${DateTime.now().millisecondsSinceEpoch ~/ 600000}'));
      if (r.statusCode != 200) throw 'http';
      final j = jsonDecode(utf8.decode(r.bodyBytes));
      final files = (j is List ? j : (j['files'] as List? ?? const [])).map((e) => '$e');
      final list = [
        for (final f in files)
          if (_dateOf(f) != null) (f, _dateOf(f)!)
      ]..sort((a, b) => b.$2.compareTo(a.$2));
      if (mounted) setState(() => _days = list);
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final days = _days;
    final groups = <String, List<(String, DateTime)>>{};
    for (final d in days ?? const <(String, DateTime)>[]) {
      groups.putIfAbsent('${_months[d.$2.month - 1]} ${d.$2.year}', () => []).add(d);
    }
    return examTheme(
      context,
      exam,
      Scaffold(
        backgroundColor: const Color(0xFFEEF2FF),
        appBar: AppBar(actions: const [HomeButton()], title: Text('Current affairs', style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: _failed
            ? Center(
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  const Text('Could not load current affairs. Check your internet.'),
                  TextButton(onPressed: _load, child: const Text('Try again')),
                ]),
              )
            : days == null
                ? const Center(child: CircularProgressIndicator())
                : RefreshIndicator(
                    onRefresh: _load,
                    child: ListView(padding: EdgeInsets.fromLTRB(12, 10, 12, 16 + MediaQuery.of(context).padding.bottom), children: [
                      if (days.isNotEmpty) _hero(days.first),
                      for (final g in groups.entries) ...[
                        Padding(
                          padding: const EdgeInsets.fromLTRB(4, 14, 4, 8),
                          child: Text(g.key, style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: exam.ink)),
                        ),
                        for (final d in g.value) _row(d),
                      ],
                    ]),
                  ),
      ),
    );
  }

  void _open((String, DateTime) d) => Navigator.of(context).push(MaterialPageRoute(builder: (_) => CaDayScreen(exam: widget.exam, file: d.$1, date: d.$2)));

  Widget _hero((String, DateTime) d) => Material(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(18),
        child: Ink(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(18),
            gradient: const LinearGradient(colors: [Color(0xFF0E7490), Color(0xFF22D3EE)], begin: Alignment.topLeft, end: Alignment.bottomRight),
          ),
          child: InkWell(
            borderRadius: BorderRadius.circular(18),
            onTap: () => _open(d),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(children: [
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    const Text('Latest · Daily digest', style: TextStyle(color: Color(0xEEFFFFFF), fontSize: 13.5, fontWeight: FontWeight.w600)),
                    const SizedBox(height: 2),
                    Text('${d.$2.day} ${_months[d.$2.month - 1]} ${d.$2.year}', style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.w900)),
                    const Text('Exam-ready news + 8 practice MCQs', style: TextStyle(color: Color(0xEEFFFFFF), fontSize: 13.5)),
                  ]),
                ),
                const CircleAvatar(radius: 20, backgroundColor: Colors.white, child: Icon(Icons.arrow_forward, color: Color(0xFF0E7490))),
              ]),
            ),
          ),
        ),
      );

  Widget _row((String, DateTime) d) => Padding(
        padding: const EdgeInsets.only(bottom: 8),
        child: Material(
          color: Colors.white,
          borderRadius: BorderRadius.circular(14),
          child: InkWell(
            borderRadius: BorderRadius.circular(14),
            onTap: () => _open(d),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              child: Row(children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(color: const Color(0xFFCFFAFE), borderRadius: BorderRadius.circular(12)),
                  child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                    Text('${d.$2.day}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900, color: Color(0xFF0E7490), height: 1)),
                    Text(_months[d.$2.month - 1].substring(0, 3), style: const TextStyle(fontSize: 12, color: Color(0xFF0E7490), fontWeight: FontWeight.w700)),
                  ]),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text(_weekdays[d.$2.weekday - 1], style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
                    const Text('Daily current affairs · quiz', style: TextStyle(fontSize: 13.5, color: Color(0xFF64748B))),
                  ]),
                ),
                const Icon(Icons.chevron_right, color: Color(0xFF0E7490)),
              ]),
            ),
          ),
        ),
      );
}

// ======================================================================= one day

class _Story {
  final String title, body;
  final List<String> tags;
  _Story(this.title, this.body, this.tags);
}

class _Mcq {
  final String q, e;
  final List<String> o;
  final int a;
  _Mcq(this.q, this.o, this.a, this.e);
}

class CaDayScreen extends StatefulWidget {
  final Exam exam;
  final String file;
  final DateTime date;
  const CaDayScreen({super.key, required this.exam, required this.file, required this.date});

  @override
  State<CaDayScreen> createState() => _CaDayScreenState();
}

class _CaDayScreenState extends State<CaDayScreen> {
  List<_Story>? _stories;
  List<_Mcq> _quiz = [];
  final Map<int, int> _picked = {};
  bool _failed = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  String _clean(String s) => s
      .replaceAll(RegExp(r'<span class="omr">.*?</span>', dotAll: true), '')
      .replaceAll(RegExp(r'<div class="scroller">'), '<div>')
      .replaceAll(RegExp(r'\s+'), ' ');

  Future<void> _load() async {
    setState(() => _failed = false);
    try {
      final r = await http.get(Uri.parse('$_base${widget.file}'));
      if (r.statusCode != 200) throw 'http';
      final html = utf8.decode(r.bodyBytes);
      final stories = <_Story>[];
      for (final m in RegExp(r'<article class="story[^"]*"[^>]*>(.*?)</article>', dotAll: true).allMatches(html)) {
        final a = m[1]!;
        final title = RegExp(r'<h2>(.*?)</h2>', dotAll: true).firstMatch(a)?.group(1)?.replaceAll(RegExp(r'<[^>]*>'), '').trim() ?? '';
        final tags = [for (final t in RegExp(r'<span class="tag[^"]*">([^<]*)</span>').allMatches(a)) t[1]!.trim()];
        final bi = a.indexOf('<div class="story-body">');
        var body = bi < 0 ? '' : a.substring(bi + '<div class="story-body">'.length);
        final li = body.lastIndexOf('</div>');
        if (li > 0) body = body.substring(0, li);
        stories.add(_Story(title, _clean(body), tags));
      }
      final quiz = <_Mcq>[];
      final qm = RegExp(r'var QS\s*=\s*(\[.*?\]);', dotAll: true).firstMatch(html);
      if (qm != null) {
        try {
          for (final x in jsonDecode(qm[1]!) as List) {
            quiz.add(_Mcq('${x['q']}', [for (final o in x['o'] as List) '$o'], (x['a'] as num).toInt(), '${x['e'] ?? ''}'));
          }
        } catch (_) {}
      }
      if (mounted) {
        setState(() {
          _stories = stories;
          _quiz = quiz;
        });
      }
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam, d = widget.date;
    final stories = _stories;
    final score = _picked.entries.where((e) => e.key < _quiz.length && _quiz[e.key].a == e.value).length;
    return examTheme(
      context,
      exam,
      Scaffold(
        backgroundColor: const Color(0xFFEEF2FF),
        appBar: AppBar(actions: const [HomeButton()], title: Text('${d.day} ${_months[d.month - 1]} ${d.year}', style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: _failed
            ? Center(
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  const Text('Could not load this day. Check your internet.'),
                  TextButton(onPressed: _load, child: const Text('Try again')),
                ]),
              )
            : stories == null
                ? const Center(child: CircularProgressIndicator())
                : ListView(padding: EdgeInsets.fromLTRB(12, 10, 12, 16 + MediaQuery.of(context).padding.bottom), children: [
                    if (_quiz.isNotEmpty)
                      Padding(
                        padding: const EdgeInsets.only(bottom: 10),
                        child: Row(children: [
                          Expanded(child: Text('${stories.length} topics · ${_quiz.length} MCQs', style: const TextStyle(fontSize: 14, color: Color(0xFF475569), fontWeight: FontWeight.w600))),
                          TextButton.icon(
                            onPressed: () => Scrollable.ensureVisible(_quizKey.currentContext!, duration: const Duration(milliseconds: 400)),
                            icon: const Icon(Icons.quiz_outlined, size: 18),
                            label: const Text('Go to quiz'),
                          ),
                        ]),
                      ),
                    for (final s in stories) _story(s),
                    if (_quiz.isNotEmpty) ...[
                      Container(
                        key: _quizKey,
                        margin: const EdgeInsets.only(top: 6, bottom: 8),
                        padding: const EdgeInsets.all(14),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(16),
                          gradient: const LinearGradient(colors: [Color(0xFF0E7490), Color(0xFF22D3EE)]),
                        ),
                        child: Row(children: [
                          const Expanded(child: Text('Test yourself', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w900))),
                          Text('$score / ${_picked.length}', style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w900)),
                        ]),
                      ),
                      for (var i = 0; i < _quiz.length; i++) _mcq(i),
                      Center(
                        child: TextButton(
                          onPressed: () => setState(_picked.clear),
                          child: const Text('Reset quiz'),
                        ),
                      ),
                    ],
                  ]),
      ),
    );
  }

  final _quizKey = GlobalKey();

  Widget _story(_Story s) => Container(
        margin: const EdgeInsets.only(bottom: 10),
        padding: const EdgeInsets.fromLTRB(14, 12, 14, 10),
        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16), border: const Border(left: BorderSide(color: Color(0xFF0E7490), width: 4))),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Wrap(spacing: 6, runSpacing: 4, children: [
            for (final t in s.tags.take(2))
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(color: const Color(0xFFCFFAFE), borderRadius: BorderRadius.circular(6)),
                child: Text(t, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w800, color: Color(0xFF0E7490))),
              ),
          ]),
          const SizedBox(height: 6),
          Text(s.title, style: TextStyle(fontSize: 18, fontWeight: FontWeight.w900, color: widget.exam.ink, height: 1.25)),
          const SizedBox(height: 4),
          HtmlWidget(
            s.body,
            textStyle: const TextStyle(fontSize: 15, height: 1.45, color: Color(0xFF1E293B)),
            customStylesBuilder: (e) {
              if (e.localName == 'h3') return {'color': '#0E7490', 'font-size': '16px', 'margin': '10px 0 4px 0'};
              if (e.localName == 'h4') return {'color': '#92400E', 'font-size': '15px', 'margin': '6px 0 4px 0'};
              if (e.classes.contains('slip')) return {'background-color': '#FEF3C7', 'padding': '10px', 'margin': '10px 0 0 0', 'border-radius': '10px'};
              if (e.localName == 'td') return {'padding': '5px', 'border': '1px solid #E2E8F0'};
              if (e.localName == 'table') return {'border-collapse': 'collapse'};
              if (e.localName == 'li') return {'margin': '0 0 4px 0'};
              return null;
            },
          ),
        ]),
      );

  Widget _mcq(int i) {
    final m = _quiz[i];
    final p = _picked[i];
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16)),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('Q${i + 1}. ${m.q}', style: const TextStyle(fontSize: 15.5, fontWeight: FontWeight.w700, height: 1.35)),
        const SizedBox(height: 8),
        for (var k = 0; k < m.o.length; k++)
          Padding(
            padding: const EdgeInsets.only(bottom: 6),
            child: Material(
              color: p == null ? const Color(0xFFF8FAFC) : (k == m.a ? const Color(0xFFDCFCE7) : (k == p ? const Color(0xFFFEE2E2) : const Color(0xFFF8FAFC))),
              borderRadius: BorderRadius.circular(10),
              child: InkWell(
                borderRadius: BorderRadius.circular(10),
                onTap: p == null ? () => setState(() => _picked[i] = k) : null,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 9),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: p == null ? const Color(0xFFE2E8F0) : (k == m.a ? const Color(0xFF16A34A) : (k == p ? const Color(0xFFDC2626) : const Color(0xFFE2E8F0)))),
                  ),
                  child: Row(children: [
                    Text('${String.fromCharCode(65 + k)}  ', style: const TextStyle(fontWeight: FontWeight.w800)),
                    Expanded(child: Text(m.o[k], style: const TextStyle(fontSize: 14.5))),
                    if (p != null && k == m.a) const Icon(Icons.check_circle, color: Color(0xFF16A34A), size: 18),
                    if (p != null && k == p && k != m.a) const Icon(Icons.cancel, color: Color(0xFFDC2626), size: 18),
                  ]),
                ),
              ),
            ),
          ),
        if (p != null && m.e.isNotEmpty)
          Container(
            margin: const EdgeInsets.only(top: 4),
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(color: const Color(0xFFEFF6FF), borderRadius: BorderRadius.circular(10)),
            child: Text(m.e, style: const TextStyle(fontSize: 13.5, color: Color(0xFF1E3A8A))),
          ),
      ]),
    );
  }
}
