// Dashboard hub — the website dashboard's sections as a list; each opens its own page (lib/screens/dash/pages.dart).
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../data.dart';
import '../ui/soft.dart';
import '../ui/soft_list.dart';
import 'chapters.dart';
import 'aic_screens.dart';
import 'dash/analysis.dart';
import 'dash/logic.dart';
import 'dash/pages.dart';
import 'dash/ui.dart';

class DashboardTab extends StatefulWidget {
  final User user;
  final Exam exam;
  final int version; // bumped by the shell after a test, to reload
  final VoidCallback onMocks;
  const DashboardTab({super.key, required this.user, required this.exam, required this.version, required this.onMocks});

  @override
  State<DashboardTab> createState() => _DashboardTabState();
}

class _DashboardTabState extends State<DashboardTab> {
  List<Att>? _raw; // every attempt of this student
  String _grp = ''; // the exam chosen in the dropdown: "<exam id>|tier1|tier2|paper2|paper3"
  bool _failed = false;

  String _gkey(Att a) {
    final id = s(a['paperId']) + s(a['mockId']);
    final t = id.contains('_paper2_') ? 'paper2' : (id.contains('_paper3_') ? 'paper3' : (isTier2(a) ? 'tier2' : 'tier1'));
    return '${s(a['exam'])}|$t';
  }

  /// Attempts of the chosen exam. Chapter tests are common practice, so they count under Tier 1.
  List<Att>? get _all => _raw?.where((a) => isChapter(a) ? _grp.endsWith('|tier1') : _gkey(a) == _grp).toList();

  Exam get _exam => examById(_grp.split('|').first) ?? widget.exam;

  bool _holds(Exam e) => (_plans ?? const []).any((p) => p.$3 && (p.$1.replaceFirst(RegExp(r'^p-'), '') == e.pass || p.$1.contains('all')));

  /// Dropdown choices: the exam open in the app, exams whose pass the student holds, and exams already attempted.
  List<String> get _groups {
    final out = <String>['${widget.exam.id}|tier1'];
    void add(String g) {
      if (!out.contains(g) && examById(g.split('|').first) != null) out.add(g);
    }

    if (widget.exam.tier2 && _holds(widget.exam)) add('${widget.exam.id}|tier2');
    for (final e in exams) {
      if (!_holds(e)) continue;
      add('${e.id}|tier1');
      if (e.tier2) add('${e.id}|tier2');
    }
    for (final a in _raw ?? const <Att>[]) {
      if (!isChapter(a)) add(_gkey(a));
    }
    return out;
  }

  String _label(String g) {
    final p = g.split('|');
    final e = examById(p[0]);
    final n = e?.name ?? p[0];
    return switch (p.length > 1 ? p[1] : 'tier1') {
      'tier2' => '$n Tier 2',
      'paper2' => '$n Statistics (Paper II)',
      'paper3' => '$n AAO (Paper III)',
      _ => (e?.tier2 ?? false) ? '$n Tier 1' : n,
    };
  }

  void _pickExam() {
    final gs = _groups;
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (c) => SafeArea(
        child: ConstrainedBox(
          constraints: BoxConstraints(maxHeight: MediaQuery.of(c).size.height * .7),
          child: ListView(shrinkWrap: true, padding: const EdgeInsets.fromLTRB(8, 14, 8, 8), children: [
            Padding(padding: const EdgeInsets.fromLTRB(12, 0, 12, 8), child: Text('Show performance for', style: baloo(19))),
            for (final g in gs)
              Builder(builder: (_) {
                final n = (_raw ?? const <Att>[]).where((a) => !isChapter(a) && _gkey(a) == g).length;
                return ListTile(
                  title: Text(_label(g), style: TextStyle(fontWeight: FontWeight.w800, color: g == _grp ? _exam.c1 : softInk)),
                  subtitle: Text(n == 0 ? 'No tests yet' : '$n test${n == 1 ? '' : 's'} taken'),
                  trailing: g == _grp ? Icon(Icons.check_circle, color: _exam.c1) : null,
                  onTap: () {
                    Navigator.pop(c);
                    setState(() => _grp = g);
                  },
                );
              }),
          ]),
        ),
      ),
    );
  }
  String _scope = '';
  String _cat = 'GEN';
  List<(String, int, bool)>? _plans;

  @override
  void initState() {
    super.initState();
    loadCat().then((c) {
      if (mounted) setState(() => _cat = c);
    });
    loadPlans(widget.user.uid).then((p) {
      if (mounted) setState(() => _plans = p);
    });
    _load();
  }

  @override
  void didUpdateWidget(DashboardTab old) {
    super.didUpdateWidget(old);
    if (old.version != widget.version) _load();
  }

  Future<void> _load() async {
    setState(() => _failed = false);
    try {
      final a = await loadAttempts(widget.user.uid);
      if (!mounted) return;
      setState(() {
        _raw = a;
        if (_grp.isEmpty) {
          final mine = a.where((x) => !isChapter(x) && x['exam'] == widget.exam.id).toList();
          _grp = mine.isEmpty ? '${widget.exam.id}|tier1' : _gkey(mine.first);
        }
      });
      final had = chapterNames.length;
      loadAllChapterNames().then((_) {
        if (mounted && chapterNames.length != had) setState(() {});
      });
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  DashCtx get _ctx => DashCtx(widget.user, _exam, _all!, _scope, _cat, overall: true);

  Future<void> _open(Widget Function(DashCtx) page) async {
    await Navigator.of(context).push(MaterialPageRoute(builder: (_) => page(_ctx)));
    final c = await loadCat();
    if (mounted && c != _cat) setState(() => _cat = c);
  }

  @override
  Widget build(BuildContext context) {
    final exam = _exam;
    if (_failed) {
      return Center(
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          const Text('Could not load your dashboard.'),
          TextButton(onPressed: _load, child: const Text('Try again')),
        ]),
      );
    }
    final all = _all;
    if (all == null) return const Center(child: CircularProgressIndicator());
    final first = (widget.user.displayName ?? 'Student').split(' ').first;

    final picker = Material(
      color: Colors.transparent,
      child: Ink(
        decoration: BoxDecoration(color: Color.lerp(Colors.white, exam.c2, .18), borderRadius: BorderRadius.circular(16)),
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: _pickExam,
          child: Padding(
            padding: const EdgeInsets.fromLTRB(14, 12, 10, 12),
            child: Row(children: [
              const Text('Exam  ', style: TextStyle(color: softMuted, fontWeight: FontWeight.w700)),
              Expanded(child: Text(_label(_grp), maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(fontSize: 15.5, fontWeight: FontWeight.w800, color: exam.ink))),
              Icon(Icons.expand_more_rounded, color: exam.c1),
            ]),
          ),
        ),
      ),
    );

    if (all.isEmpty) {
      return RefreshIndicator(
        onRefresh: _load,
        child: ListView(padding: const EdgeInsets.fromLTRB(14, 8, 14, 28), children: [
          picker,
          const SizedBox(height: 10),
          const AicHeldNote(),
          const SizedBox(height: 40),
          Icon(Icons.insights, size: 56, color: exam.c1),
          const SizedBox(height: 10),
          Text('No ${_label(_grp)} tests yet', textAlign: TextAlign.center, style: baloo(21)),
          const SizedBox(height: 6),
          const Text('Attempt any test — PYQ, mock, subject-wise or chapter — to see your overall performance here.',
              textAlign: TextAlign.center, style: TextStyle(fontSize: 15, color: softMuted, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          Center(child: FilledButton(onPressed: widget.onMocks, style: FilledButton.styleFrom(backgroundColor: exam.c1), child: const Text('Go to mocks'))),
        ]),
      );
    }

    final full = all.where((t) => isFullPaper(t)).toList();
    final fullMarks = full.map(marksOf).toList();
    final avg = fullMarks.isEmpty ? null : fullMarks.fold(0.0, (t, v) => t + v) / fullMarks.length;
    final best = fullMarks.isEmpty ? null : fullMarks.reduce((p, q) => p > q ? p : q);
    final maxLabel = full.isEmpty ? '' : '/${n1(maxOf(full.first))}';
    final week = all.where((t) => tsOf(t) >= DateTime.now().millisecondsSinceEpoch - 7 * 86400000).length;
    final streak = streakDays(all);
    final dots = last7(all);
    final ct = cutoffTests(full);
    String? goal;
    if (ct.isNotEmpty) {
      final c = cutoffs[examTier(ct.first)]!;
      final l5 = ct.take(5).toList();
      final av = l5.fold(0.0, (t, v) => t + meritMarks(v)) / l5.length;
      goal = '🎯 ${(av / c.cut[_cat]! * 100).round().clamp(0, 100)}% of the way to last year\'s $_cat cut-off';
    }
    final live = (_plans ?? const []).where((p) => p.$3).toList();

    // teasers
    final weakN = chapterStats(all).where((c) => c.name != 'Untagged' && c.n >= 3 && c.acc < .7).length;

    Widget stat(String v, String l, String d, {Widget? extra}) => Expanded(
          child: Container(
            padding: const EdgeInsets.fromLTRB(14, 12, 12, 12),
            decoration: softCard(radius: 18),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(v, style: baloo(26, color: exam.c1)),
              Text(l, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 13.5, color: softInk, fontWeight: FontWeight.w800)),
              const SizedBox(height: 2),
              extra ?? Text(d, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 12, color: softMuted, fontWeight: FontWeight.w600)),
            ]),
          ),
        );

    Widget section(String emoji, String title, String teaser, Widget Function(DashCtx) page, {Color? tc}) => Padding(
          padding: const EdgeInsets.only(bottom: 10),
          child: Material(
            color: Colors.transparent,
            child: Ink(
              decoration: softCard(radius: 18),
              child: InkWell(
                borderRadius: BorderRadius.circular(18),
                onTap: () => _open(page),
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(12, 11, 8, 11),
                  child: Row(children: [
                    Container(width: 48, height: 48, alignment: Alignment.center, decoration: softWell(), child: Text(emoji, style: const TextStyle(fontSize: 24))),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text(title, style: baloo(17.5)),
                        Text(teaser, maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(fontSize: 13.5, color: tc ?? exam.c1, fontWeight: FontWeight.w800)),
                      ]),
                    ),
                    Icon(Icons.chevron_right_rounded, color: exam.c1),
                  ]),
                ),
              ),
            ),
          ),
        );

    Widget head(String t) => Padding(padding: const EdgeInsets.fromLTRB(4, 8, 4, 8), child: Text(t, style: baloo(19)));

    return RefreshIndicator(
      onRefresh: _load,
      child: ListView(padding: EdgeInsets.fromLTRB(14, 8, 14, 20 + MediaQuery.of(context).padding.bottom), children: [
        picker,
        const SizedBox(height: 10),
        const AicHeldNote(), // a live All India Challenge attempt is held back until its result
        // welcome
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(22),
            gradient: LinearGradient(colors: [exam.c1, Color.lerp(exam.c1, exam.c2, .55)!], begin: Alignment.topLeft, end: Alignment.bottomRight),
            boxShadow: [BoxShadow(color: exam.c1.withValues(alpha: .3), blurRadius: 18, offset: const Offset(0, 8))],
          ),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              Expanded(child: Text('Welcome back, $first! 👋', style: baloo(21, color: Colors.white))),
              if (_plans != null) live.isNotEmpty ? const SoftTag('⭐ PREMIUM', Color(0xFF92400E), Color(0xFFFEF3C7)) : const SoftTag('FREE PLAN', Color(0xFF475569), Colors.white),
            ]),
            if (live.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 2),
                child: Text(live.map((p) => '${planName(p.$1).replaceAll(' Mock Test Series', ' mocks')} till ${shortDate(p.$2)}').join(' · '), style: const TextStyle(color: Color(0xEEFFFFFF), fontSize: 12.5, fontWeight: FontWeight.w600)),
              ),
            if (goal != null) Padding(padding: const EdgeInsets.only(top: 8), child: Text(goal, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 13.5))),
          ]),
        ),
        const SizedBox(height: 12),
        Row(children: [
          stat('${all.length}', 'Tests taken', week > 0 ? '+$week this week' : 'none this week'),
          const SizedBox(width: 10),
          stat(avg == null ? '—' : n1(avg), 'Avg marks $maxLabel', '${full.length} full test${full.length == 1 ? '' : 's'}'),
        ]),
        const SizedBox(height: 10),
        Row(children: [
          stat(best == null ? '—' : n1(best), 'Best marks $maxLabel', _label(_grp)),
          const SizedBox(width: 10),
          stat('$streak', 'Day streak', '',
              extra: Row(children: [
                for (final on in dots)
                  Container(margin: const EdgeInsets.only(right: 4, top: 3), width: 12, height: 12, decoration: BoxDecoration(shape: BoxShape.circle, color: on ? const Color(0xFFF59E0B) : const Color(0xFFE2E8F0))),
              ])),
        ]),
        const SizedBox(height: 12),
        head('📈 Overall performance'),
        section('📊', 'My tests', '${all.length} tests · tap any for its full analysis', (c) => AttemptsPage(x: c)),
        section('💪', 'Exam readiness', '${readiness(all)} / 100 · last ${all.length < 5 ? all.length : 5} tests', (c) => ReadinessPage(x: c)),
        section('📚', 'Chapter analysis', weakN > 0 ? '$weakN weak chapter${weakN == 1 ? '' : 's'} · subject-wise' : 'Subject-wise, weakest first', (c) => ChapterAnalysisPage(x: c)),
      ]),
    );
  }
}
