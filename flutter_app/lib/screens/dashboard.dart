// Dashboard hub — the website dashboard's sections as a list; each opens its own page (lib/screens/dash/pages.dart).
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../data.dart';
import '../ui/soft.dart';
import '../ui/soft_list.dart';
import 'chapters.dart';
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
  List<Att>? _all;
  bool _failed = false;
  String _scope = '';
  String _cat = 'GEN';
  LbInfo? _lb;
  String _lbFor = '';
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
      final mine = a.where((x) => x['exam'] == widget.exam.id || isChapter(x)).toList();
      if (!mounted) return;
      setState(() {
        _all = mine;
        if (_scope.isEmpty || !mine.any((x) => scopeOf(x) == _scope)) _scope = mine.isEmpty ? '' : scopeOf(mine.first);
      });
      _rank();
      final had = chapterNames.length;
      loadAllChapterNames().then((_) {
        if (mounted && chapterNames.length != had) setState(() {});
      });
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  void _rank() {
    final sc = (_all ?? const <Att>[]).where((a) => scopeOf(a) == _scope).toList();
    if (sc.isEmpty) return;
    final k = lbKeyOf(sc.first);
    if (k.isEmpty || k == _lbFor) return;
    _lbFor = k;
    _lb = null;
    fetchRank(k, widget.user.uid, from: sc.first).then((v) {
      if (mounted && _lbFor == k) setState(() => _lb = v);
    });
  }

  DashCtx get _ctx => DashCtx(widget.user, widget.exam, _all!, _scope, _cat);

  Future<void> _open(Widget Function(DashCtx) page) async {
    await Navigator.of(context).push(MaterialPageRoute(builder: (_) => page(_ctx)));
    final c = await loadCat();
    if (mounted && c != _cat) setState(() => _cat = c);
  }

  void _pickScope() {
    final all = _all!;
    final seen = <String, int>{};
    final first = <String, Att>{};
    for (final a in all) {
      final k = scopeOf(a);
      seen[k] = (seen[k] ?? 0) + 1;
      first.putIfAbsent(k, () => a);
    }
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (c) => SafeArea(
        child: ConstrainedBox(
          constraints: BoxConstraints(maxHeight: MediaQuery.of(c).size.height * .7),
          child: ListView(shrinkWrap: true, padding: const EdgeInsets.fromLTRB(8, 14, 8, 8), children: [
            Padding(padding: const EdgeInsets.fromLTRB(12, 0, 12, 8), child: Text('Analyse which tests?', style: baloo(19))),
            for (final k in seen.keys)
              ListTile(
                title: Text(scopeLabel(k, first[k]!), style: TextStyle(fontWeight: FontWeight.w800, color: k == _scope ? widget.exam.c1 : softInk)),
                subtitle: Text('${seen[k]} test${seen[k] == 1 ? '' : 's'} · last ${shortDate(tsOf(first[k]!))}'),
                trailing: k == _scope ? Icon(Icons.check_circle, color: widget.exam.c1) : null,
                onTap: () {
                  Navigator.pop(c);
                  setState(() => _scope = k);
                  _rank();
                },
              ),
          ]),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
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

    if (all.isEmpty) {
      return RefreshIndicator(
        onRefresh: _load,
        child: ListView(padding: const EdgeInsets.all(28), children: [
          const SizedBox(height: 60),
          Icon(Icons.insights, size: 56, color: exam.c1),
          const SizedBox(height: 10),
          Text('No ${exam.name} tests yet', textAlign: TextAlign.center, style: baloo(21)),
          const SizedBox(height: 6),
          const Text('Attempt any test — PYQ, mock, subject-wise or chapter — to see your rank, cut-off gap and weak areas here.',
              textAlign: TextAlign.center, style: TextStyle(fontSize: 15, color: softMuted, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          Center(child: FilledButton(onPressed: widget.onMocks, style: FilledButton.styleFrom(backgroundColor: exam.c1), child: const Text('Go to mocks'))),
        ]),
      );
    }

    final x = _ctx;
    final sc = x.sc;
    final a = sc.first;
    final full = all.where((t) => isFullPaper(t) && s(t['exam']) == exam.id).toList();
    final fullMarks = full.map(marksOf).toList();
    final avg = fullMarks.isEmpty ? null : fullMarks.fold(0.0, (t, v) => t + v) / fullMarks.length;
    final best = fullMarks.isEmpty ? null : fullMarks.reduce((p, q) => p > q ? p : q);
    final maxLabel = full.isEmpty ? '' : '/${n1(maxOf(full.first))}';
    final week = all.where((t) => tsOf(t) >= DateTime.now().millisecondsSinceEpoch - 7 * 86400000).length;
    final streak = streakDays(all);
    final dots = last7(all);
    final scM = sc.map(marksOf).toList();
    final scAvg = scM.fold(0.0, (t, v) => t + v) / scM.length;
    final delta = marksOf(a) - scAvg;
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
    final scCut = cutoffTests(sc);
    String? cutT;
    if (scCut.isNotEmpty) {
      final g = meritMarks(scCut.first) - cutoffs[examTier(scCut.first)]!.cut[_cat]!;
      cutT = g >= 0 ? 'Cleared $_cat by +${n1(g)}' : '${n1(-g)} marks short of $_cat';
    }
    final chScope = isChapter(a);
    final weakN = chapterStats(sc).where((c) => c.name != 'Untagged' && c.n >= 3 && c.acc < .7).length;

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
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.fromLTRB(14, 10, 14, 10),
              decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16)),
              child: Row(children: [
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('Last test · ${testName(a)}', maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 12.5, color: softMuted, fontWeight: FontWeight.w700)),
                    Text(sc.length > 1 ? '${delta >= 0 ? '▲' : '▼'} ${n1(delta.abs())} vs your average in these tests' : 'your first test of this kind',
                        style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w800, color: delta >= 0 ? cGood : cBad)),
                  ]),
                ),
                Text(n1(marksOf(a)), style: baloo(28, color: exam.c1)),
                Text('/${n1(maxOf(a))}', style: const TextStyle(color: softMuted, fontWeight: FontWeight.w800)),
              ]),
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
          stat(best == null ? '—' : n1(best), 'Best marks $maxLabel', exam.name),
          const SizedBox(width: 10),
          stat('$streak', 'Day streak', '',
              extra: Row(children: [
                for (final on in dots)
                  Container(margin: const EdgeInsets.only(right: 4, top: 3), width: 12, height: 12, decoration: BoxDecoration(shape: BoxShape.circle, color: on ? const Color(0xFFF59E0B) : const Color(0xFFE2E8F0))),
              ])),
        ]),
        const SizedBox(height: 12),
        section('📊', 'My recent attempts', '${all.length} tests · tap any for its full analysis', (c) => AttemptsPage(x: c)),
        head('📈 Overall performance'),
        Material(
          color: Colors.transparent,
          child: Ink(
            decoration: BoxDecoration(color: Color.lerp(Colors.white, exam.c2, .18), borderRadius: BorderRadius.circular(16)),
            child: InkWell(
              borderRadius: BorderRadius.circular(16),
              onTap: _pickScope,
              child: Padding(
                padding: const EdgeInsets.fromLTRB(14, 10, 10, 10),
                child: Row(children: [
                  const Text('Showing  ', style: TextStyle(color: softMuted, fontWeight: FontWeight.w700)),
                  Expanded(child: Text('${scopeLabel(_scope, a)} (${sc.length})', maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
                  Icon(Icons.expand_more_rounded, color: exam.c1),
                ]),
              ),
            ),
          ),
        ),
        const SizedBox(height: 10),
        if (cutT != null) section('🎯', 'Cut-off gap', cutT, (c) => CutoffPage(x: c), tc: cutT.startsWith('Cleared') ? cGood : cBad),
        section('📚', chScope ? 'Test-wise accuracy' : 'Chapter-wise accuracy',
            chScope ? '${sc.length} attempt${sc.length == 1 ? '' : 's'} of this chapter' : (weakN > 0 ? '$weakN weak chapter${weakN == 1 ? '' : 's'} found' : 'Your weak and strong chapters'), (c) => ChaptersPage(x: c)),
        section('💪', chScope ? 'Chapter readiness' : 'Exam readiness', '${readiness(sc)} / 100 · last ${sc.length < 5 ? sc.length : 5} tests', (c) => ReadinessPage(x: c)),
        section('🖼️', 'Report card', 'Share an image of your progress', (c) => ReportCardPage(x: c, name: widget.user.displayName ?? 'Student')),
        head('👤 Account'),
        section('👤', 'My profile', widget.user.email ?? widget.user.phoneNumber ?? 'Name, phone, login method', (c) => ProfilePage(x: c)),
        section('🧾', 'My orders', _plans == null ? 'Purchases and access validity' : (live.isNotEmpty ? 'Premium active' : 'Free plan · purchases and payment IDs'), (c) => OrdersPage(x: c)),
      ]),
    );
  }
}
