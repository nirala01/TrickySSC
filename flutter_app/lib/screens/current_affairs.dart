import 'dart:convert';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import '../ui/nav.dart';
import '../test/engine.dart';
import '../test/test_screen.dart';
import '../ui/soft.dart';
import '../ui/soft_list.dart';
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

Future<List<(String, DateTime)>> _loadDays() async {
  final r = await http.get(Uri.parse('${_base}index.json?t=${DateTime.now().millisecondsSinceEpoch ~/ 600000}'));
  if (r.statusCode != 200) throw 'http';
  final j = jsonDecode(utf8.decode(r.bodyBytes));
  final files = (j is List ? j : (j['files'] as List? ?? const [])).map((e) => '$e');
  return [
    for (final f in files)
      if (_dateOf(f) != null) (f, _dateOf(f)!)
  ]..sort((a, b) => b.$2.compareTo(a.$2));
}

Map<String, String>? _caStyles(dynamic e) {
  if (e.localName == 'h2') return {'color': '#0F172A', 'font-size': '17px', 'margin': '12px 0 4px 0'};
  if (e.localName == 'h3') return {'color': '#0E7490', 'font-size': '16px', 'margin': '10px 0 4px 0'};
  if (e.localName == 'h4') return {'color': '#92400E', 'font-size': '15px', 'margin': '6px 0 4px 0'};
  if (e.classes.contains('slip')) return {'background-color': '#FEF3C7', 'padding': '10px', 'margin': '10px 0 0 0', 'border-radius': '10px'};
  if (e.localName == 'td' || e.localName == 'th') return {'padding': '5px', 'border': '1px solid #E2E8F0'};
  if (e.localName == 'table') return {'border-collapse': 'collapse'};
  if (e.localName == 'li') return {'margin': '0 0 4px 0'};
  return null;
}

// ======================================================================= hub: daily + topic-wise
//
// Topic-wise current affairs:
//   trickyssc.com/ca-topics/index.json        {months: ['2026-01', ... '2026-10'], period: '...', topics: [{id, name}]}   (optional; the list below is used without it)
//                                             months = the rolling window: it sets the heading and which months' questions are asked
//   trickyssc.com/ca-topics/<topic id>.json   {parts: [{title: 'January 2026', html: '...'}]}   the notes; the website landing page reads the same file
//   questions (Firestore)                     the topic's questions: chapter-test rows with chapterId = <topic id> and year = YYYY-MM (see loadCaPool)
// Fallbacks kept for notes typed into admin-ca-notes.html: config/ca_topics and the ca_notes collection.

const _topicBase = 'https://trickyssc.com/ca-topics/';

Future<Map<String, dynamic>?> _topicJson(String name) async {
  try {
    final r = await http.get(Uri.parse('$_topicBase$name.json?t=${DateTime.now().millisecondsSinceEpoch ~/ 600000}')).timeout(const Duration(seconds: 12));
    if (r.statusCode != 200) return null;
    final j = jsonDecode(utf8.decode(r.bodyBytes));
    return j is Map<String, dynamic> ? j : null;
  } catch (_) {
    return null;
  }
}

class CaTopic {
  final String id, name;
  const CaTopic(this.id, this.name);
}

const _defaultPeriod = 'Jan 2026 to Oct 2026';
const _defaultTopics = [
  CaTopic('ca.international', 'International'),
  CaTopic('ca.national', 'National'),
  CaTopic('ca.economic', 'Economic'),
  CaTopic('ca.science-tech', 'Science and Technology'),
  CaTopic('ca.sports', 'Sports Affairs'),
  CaTopic('ca.awards', 'Awards and Honours'),
  CaTopic('ca.conferences', 'Conferences, Meetings, Fairs, Festivals and Exhibitions'),
  CaTopic('ca.appointments', 'Election and Appointments'),
  CaTopic('ca.military', 'Campaigns, Operations and Military Exercises'),
  CaTopic('ca.important-days', 'Important Days'),
  CaTopic('ca.economic-survey', 'Economic Survey'),
  CaTopic('ca.budget', 'Budget 2026'),
];

const _topicColors = [Color(0xFF4F46E5), Color(0xFFEA580C), Color(0xFF047857), Color(0xFF7C3AED), Color(0xFF0369A1), Color(0xFFBE185D)];

IconData _topicIcon(CaTopic t) {
  final k = '${t.id} ${t.name}'.toLowerCase();
  if (k.contains('budget')) return Icons.account_balance_wallet;
  if (k.contains('survey')) return Icons.insights;
  if (k.contains('international')) return Icons.public;
  if (k.contains('national')) return Icons.flag;
  if (k.contains('econom')) return Icons.trending_up;
  if (k.contains('science')) return Icons.science;
  if (k.contains('sport')) return Icons.sports_cricket;
  if (k.contains('award')) return Icons.emoji_events;
  if (k.contains('conference')) return Icons.groups;
  if (k.contains('appoint') || k.contains('election')) return Icons.how_to_vote;
  if (k.contains('military') || k.contains('campaign')) return Icons.military_tech;
  if (k.contains('days')) return Icons.event;
  return Icons.article;
}

class CurrentAffairsScreen extends StatefulWidget {
  final User user;
  final Exam exam;
  final bool paid;
  final Set<String> attempted;
  final VoidCallback onReturn;
  const CurrentAffairsScreen({super.key, required this.user, required this.exam, required this.paid, required this.attempted, required this.onReturn});

  @override
  State<CurrentAffairsScreen> createState() => _CurrentAffairsScreenState();
}

class _CurrentAffairsScreenState extends State<CurrentAffairsScreen> {
  (String, DateTime)? _latest;
  List<CaTopic> _topics = _defaultTopics;
  String _period = _defaultPeriod;
  List<String> _window = const []; // months asked in the tests; empty = all

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    await Future.wait([_loadLatest(), _loadTopics()]);
  }

  Future<void> _loadLatest() async {
    try {
      final days = await _loadDays();
      if (mounted && days.isNotEmpty) setState(() => _latest = days.first);
    } catch (_) {}
  }

  Future<void> _loadTopics() async {
    Map<String, dynamic>? m = await _topicJson('index');
    if (m == null) {
      try {
        m = (await FirebaseFirestore.instance.collection('config').doc('ca_topics').get().timeout(const Duration(seconds: 8))).data();
      } catch (_) {}
    }
    if (m == null || !mounted) return;
    final list = <CaTopic>[];
    for (final t in (m['topics'] as List? ?? const [])) {
      if (t is Map && '${t['id'] ?? ''}'.isNotEmpty) list.add(CaTopic('${t['id']}', '${t['name'] ?? t['id']}'));
    }
    final win = [for (final x in (m['months'] as List? ?? const [])) caMonthKey(x)].where((x) => x.isNotEmpty).toList()..sort();
    var p = '${m['period'] ?? ''}';
    if (p.isEmpty && win.isNotEmpty) p = '${caMonthLabel(win.first, short: true)} to ${caMonthLabel(win.last, short: true)}';
    setState(() {
      if (list.isNotEmpty) _topics = list;
      if (p.isNotEmpty) _period = p;
      _window = win;
    });
  }

  void _daily() => Navigator.of(context).push(MaterialPageRoute(builder: (_) => CaDailyScreen(exam: widget.exam)));

  void _today() {
    final d = _latest;
    if (d == null) return _daily();
    Navigator.of(context).push(MaterialPageRoute(builder: (_) => CaDayScreen(exam: widget.exam, file: d.$1, date: d.$2)));
  }

  void _read(CaTopic t) => Navigator.of(context).push(MaterialPageRoute(builder: (_) => CaTopicNotesScreen(exam: widget.exam, topic: t, period: _period)));

  void _test(CaTopic t) => Navigator.of(context).push(MaterialPageRoute(
        builder: (_) => CaTopicTestsScreen(user: widget.user, exam: widget.exam, topic: t, period: _period, window: _window, paid: widget.paid, attempted: widget.attempted, onReturn: widget.onReturn),
      ));

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    return examTheme(
      context,
      exam,
      Scaffold(
        appBar: AppBar(actions: const [HomeButton()], title: Text('Current affairs', style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: Container(
          decoration: softBg,
          child: RefreshIndicator(
            onRefresh: _load,
            child: ListView(padding: EdgeInsets.fromLTRB(14, 10, 14, 18 + MediaQuery.of(context).padding.bottom), children: [
              _dailyCard(),
              Padding(
                padding: const EdgeInsets.fromLTRB(4, 20, 4, 2),
                child: Text('Topic-wise current affairs', style: baloo(21)),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(4, 0, 4, 10),
                child: Row(children: [
                  const Icon(Icons.date_range, size: 16, color: softMuted),
                  const SizedBox(width: 5),
                  Text(_period, style: const TextStyle(fontSize: 14.5, color: softMuted, fontWeight: FontWeight.w700)),
                ]),
              ),
              for (var i = 0; i < _topics.length; i++) _topicCard(i, _topics[i]),
            ]),
          ),
        ),
      ),
    );
  }

  Widget _dailyCard() {
    final d = _latest;
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(22),
        gradient: const LinearGradient(colors: [Color(0xFF0E7490), Color(0xFF22D3EE)], begin: Alignment.topLeft, end: Alignment.bottomRight),
        boxShadow: [BoxShadow(color: const Color(0xFF0E7490).withValues(alpha: .28), blurRadius: 20, offset: const Offset(0, 9))],
      ),
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          const Icon(Icons.today, color: Colors.white, size: 20),
          const SizedBox(width: 6),
          Text('Daily current affairs', style: baloo(20, color: Colors.white)),
        ]),
        const SizedBox(height: 4),
        Text(
          d == null ? 'Exam-ready news + practice MCQs, every day' : 'Latest: ${d.$2.day} ${_months[d.$2.month - 1]} ${d.$2.year} · news + 8 MCQs',
          style: const TextStyle(color: Color(0xF2FFFFFF), fontSize: 14, fontWeight: FontWeight.w600),
        ),
        const SizedBox(height: 12),
        Row(children: [
          Expanded(
            child: FilledButton.icon(
              onPressed: _today,
              style: FilledButton.styleFrom(backgroundColor: Colors.white, foregroundColor: const Color(0xFF0E7490), minimumSize: const Size.fromHeight(44)),
              icon: const Icon(Icons.menu_book, size: 18),
              label: const Text('Read today', style: TextStyle(fontWeight: FontWeight.w800)),
            ),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: OutlinedButton.icon(
              onPressed: _daily,
              style: OutlinedButton.styleFrom(foregroundColor: Colors.white, side: const BorderSide(color: Colors.white, width: 1.4), minimumSize: const Size.fromHeight(44)),
              icon: const Icon(Icons.calendar_month, size: 18),
              label: const Text('All days', style: TextStyle(fontWeight: FontWeight.w800)),
            ),
          ),
        ]),
      ]),
    );
  }

  Widget _topicCard(int i, CaTopic t) {
    final c = _topicColors[i % _topicColors.length];
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.fromLTRB(14, 14, 14, 12),
      decoration: softCard(glow: c),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Container(
            width: 46,
            height: 46,
            decoration: BoxDecoration(color: c.withValues(alpha: .12), borderRadius: BorderRadius.circular(14)),
            child: Icon(_topicIcon(t), color: c, size: 25),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(t.name, style: baloo(18, height: 1.2)),
              const SizedBox(height: 2),
              Text(_period, style: const TextStyle(fontSize: 13, color: softMuted, fontWeight: FontWeight.w600)),
            ]),
          ),
        ]),
        const SizedBox(height: 12),
        Row(children: [
          Expanded(
            child: OutlinedButton.icon(
              onPressed: () => _read(t),
              style: OutlinedButton.styleFrom(foregroundColor: c, side: BorderSide(color: c, width: 1.4), minimumSize: const Size.fromHeight(42)),
              icon: const Icon(Icons.menu_book, size: 18),
              label: const Text('Read here', style: TextStyle(fontWeight: FontWeight.w800)),
            ),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: FilledButton.icon(
              onPressed: () => _test(t),
              style: FilledButton.styleFrom(backgroundColor: c, foregroundColor: Colors.white, minimumSize: const Size.fromHeight(42)),
              icon: const Icon(Icons.quiz, size: 18),
              label: const Text('Attempt test', style: TextStyle(fontWeight: FontWeight.w800)),
            ),
          ),
        ]),
      ]),
    );
  }
}

// ======================================================================= one topic's tests

class CaTopicTestsScreen extends StatefulWidget {
  final User user;
  final Exam exam;
  final CaTopic topic;
  final String period;
  final List<String> window;
  final bool paid;
  final Set<String> attempted;
  final VoidCallback onReturn;
  const CaTopicTestsScreen({super.key, required this.user, required this.exam, required this.topic, required this.period, required this.window, required this.paid, required this.attempted, required this.onReturn});

  @override
  State<CaTopicTestsScreen> createState() => _CaTopicTestsScreenState();
}

class _CaTopicTestsScreenState extends State<CaTopicTestsScreen> {
  CaPool? _pool;
  bool _failed = false;
  late Set<String> _attempted = widget.attempted;
  Map<String, List<String>> _paused = {};
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
      final p = await loadCaPool(widget.topic.id, widget.window);
      if (mounted) setState(() => _pool = p);
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  Future<void> _open(CaTest t) async {
    final exam = widget.exam, pool = _pool!;
    var lang = t.en.isNotEmpty ? 'en' : 'hi';
    final saved = _paused[cwLbKey(pool.keyId, 1, t.num)];
    if (saved != null) {
      lang = saved[0];
    } else if (t.en.isNotEmpty && t.hi.isNotEmpty) {
      final picked = await showModalBottomSheet<String>(
        context: context,
        backgroundColor: Colors.white,
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
        builder: (c) => SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 12),
            child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              Text('${widget.topic.name} · Test ${t.num}', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: exam.ink)),
              const SizedBox(height: 12),
              Row(children: [
                for (final l in const [('en', 'English'), ('hi', 'हिंदी')]) ...[
                  if (l.$1 == 'hi') const SizedBox(width: 10),
                  Expanded(
                    child: FilledButton(
                      onPressed: () => Navigator.pop(c, l.$1),
                      style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50)),
                      child: Text(l.$2, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
                    ),
                  ),
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
        mockId: '${cwLbKey(pool.keyId, 1, t.num)}_$lang',
        lang: lang,
        paid: widget.paid,
        title: '${widget.topic.name} · Test ${t.num}',
        loader: () async => caTestPaper(pool, t, widget.topic.name, lang),
      ),
    ));
    widget.onReturn();
    final a = await loadAttempted(widget.user.uid);
    if (mounted) setState(() => _attempted = a);
    _loadPaused();
  }

  String _span(CaTest t) {
    if (t.newest.isEmpty) return '';
    final a = caMonthLabel(t.newest, short: true), b = caMonthLabel(t.oldest, short: true);
    return a == b ? a : '$a to $b';
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam, pool = _pool;
    return examTheme(
      context,
      exam,
      Scaffold(
        appBar: AppBar(actions: const [HomeButton()], title: Text(widget.topic.name, style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: Container(
          decoration: softBg,
          child: _failed
              ? Center(
                  child: Column(mainAxisSize: MainAxisSize.min, children: [
                    const Text('Could not load the tests. Check your internet.'),
                    TextButton(onPressed: _load, child: const Text('Try again')),
                  ]),
                )
              : pool == null
                  ? const Center(child: CircularProgressIndicator())
                  : RefreshIndicator(
                      onRefresh: _load,
                      child: ListView(padding: EdgeInsets.fromLTRB(14, 10, 14, 18 + MediaQuery.of(context).padding.bottom), children: [
                        Padding(
                          padding: const EdgeInsets.fromLTRB(4, 0, 4, 12),
                          child: Text('Current affairs tests · ${widget.period}\nNewest questions first · 25 questions · 15 min or untimed · FREE',
                              style: const TextStyle(fontSize: 13.5, height: 1.45, color: softMuted, fontWeight: FontWeight.w700)),
                        ),
                        if (pool.tests.isEmpty)
                          const Padding(
                            padding: EdgeInsets.all(36),
                            child: Center(child: Text('Tests for this topic are being added. Please check again soon.', textAlign: TextAlign.center, style: TextStyle(fontSize: 15, color: softMuted))),
                          ),
                        for (final t in pool.tests)
                          Builder(builder: (_) {
                            final done = _attempted.contains(cwLbKey(pool.keyId, 1, t.num));
                            final span = _span(t);
                            return SoftRow(
                              badge: '${t.num}',
                              title: 'Test ${t.num}',
                              tags: [done ? const SoftTag.done() : const SoftTag.free()],
                              meta: '${span.isEmpty ? '' : '$span · '}${t.count} Qs${t.hi.isNotEmpty && t.en.isNotEmpty ? ' · EN · हिंदी' : ''}',
                              action: _paused.containsKey(cwLbKey(pool.keyId, 1, t.num)) ? 'Resume' : (done ? 'Re-attempt' : 'Start'),
                              resume: _paused.containsKey(cwLbKey(pool.keyId, 1, t.num)),
                              accent: exam.c1,
                              onTap: () => _open(t),
                            );
                          }),
                      ]),
                    ),
        ),
      ),
    );
  }
}

// ======================================================================= one topic's notes

class CaTopicNotesScreen extends StatefulWidget {
  final Exam exam;
  final CaTopic topic;
  final String period;
  const CaTopicNotesScreen({super.key, required this.exam, required this.topic, required this.period});

  @override
  State<CaTopicNotesScreen> createState() => _CaTopicNotesScreenState();
}

class _CaTopicNotesScreenState extends State<CaTopicNotesScreen> {
  List<(String, String)>? _parts; // title, html
  bool _failed = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _failed = false);
    try {
      final j = await _topicJson(widget.topic.id);
      final fromSite = <(String, String)>[];
      for (final x in (j?['parts'] as List? ?? const [])) {
        if (x is Map && '${x['html'] ?? ''}'.isNotEmpty) fromSite.add(('${x['title'] ?? ''}', '${x['html']}'));
      }
      if (fromSite.isNotEmpty) {
        if (mounted) setState(() => _parts = fromSite);
        return;
      }
      var docs = <Map<String, dynamic>>[];
      try {
        final snap = await FirebaseFirestore.instance.collection('ca_notes').where('topic', isEqualTo: widget.topic.id).get();
        docs = [for (final d in snap.docs) d.data()]..sort((a, b) => ((a['order'] as num?) ?? 0).compareTo((b['order'] as num?) ?? 0));
      } catch (_) {}
      if (mounted) setState(() => _parts = [for (final m in docs) ('${m['title'] ?? ''}', '${m['html'] ?? ''}')]);
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam, parts = _parts;
    return examTheme(
      context,
      exam,
      Scaffold(
        backgroundColor: const Color(0xFFEEF2FF),
        appBar: AppBar(actions: const [HomeButton()], title: Text(widget.topic.name, style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: _failed
            ? Center(
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  const Text('Could not load these notes. Check your internet.'),
                  TextButton(onPressed: _load, child: const Text('Try again')),
                ]),
              )
            : parts == null
                ? const Center(child: CircularProgressIndicator())
                : ListView(padding: EdgeInsets.fromLTRB(12, 10, 12, 16 + MediaQuery.of(context).padding.bottom), children: [
                    Padding(
                      padding: const EdgeInsets.fromLTRB(4, 0, 4, 10),
                      child: Text('Current affairs · ${widget.period}', style: const TextStyle(fontSize: 14, color: Color(0xFF475569), fontWeight: FontWeight.w700)),
                    ),
                    if (parts.isEmpty)
                      const Padding(
                        padding: EdgeInsets.all(36),
                        child: Center(child: Text('Notes for this topic are being added. Please check again soon.', textAlign: TextAlign.center, style: TextStyle(fontSize: 15, color: Color(0xFF475569)))),
                      ),
                    for (final p in parts)
                      Container(
                        margin: const EdgeInsets.only(bottom: 10),
                        padding: const EdgeInsets.fromLTRB(14, 12, 14, 10),
                        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16), border: const Border(left: BorderSide(color: Color(0xFF0E7490), width: 4))),
                        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                          if (p.$1.isNotEmpty) ...[
                            Text(p.$1, style: TextStyle(fontSize: 18, fontWeight: FontWeight.w900, color: exam.ink, height: 1.25)),
                            const SizedBox(height: 4),
                          ],
                          HtmlWidget(p.$2, textStyle: const TextStyle(fontSize: 15, height: 1.45, color: Color(0xFF1E293B)), customStylesBuilder: _caStyles),
                        ]),
                      ),
                  ]),
      ),
    );
  }
}

// ======================================================================= daily list

class CaDailyScreen extends StatefulWidget {
  final Exam exam;
  const CaDailyScreen({super.key, required this.exam});

  @override
  State<CaDailyScreen> createState() => _CaDailyScreenState();
}

class _CaDailyScreenState extends State<CaDailyScreen> {
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
      final list = await _loadDays();
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
        appBar: AppBar(actions: const [HomeButton()], title: Text('Daily current affairs', style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
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
            customStylesBuilder: _caStyles,
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
