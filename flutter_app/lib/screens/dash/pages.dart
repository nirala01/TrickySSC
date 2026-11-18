// The dashboard's detail pages — one page per card of the website dashboard.
import 'dart:ui' as ui;

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:share_plus/share_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../data.dart';
import '../../test/leaderboard.dart';
import '../../test/result_screen.dart';
import '../../ui/soft.dart';
import '../../ui/soft_list.dart';
import 'logic.dart';
import 'ui.dart';

/// What every page needs: the student, the exam, all their attempts for this exam and the chosen scope.
class DashCtx {
  final User user;
  final Exam exam;
  final List<Att> all; // this exam + chapter tests, newest first
  final String scope;
  final String cat;
  DashCtx(this.user, this.exam, this.all, this.scope, this.cat);
  List<Att> get sc => all.where((a) => scopeOf(a) == scope).toList();
  Att? get latest => sc.isEmpty ? null : sc.first;
}

Future<String> loadCat() async => (await SharedPreferences.getInstance()).getString('tssc_cat') ?? 'GEN';
Future<void> saveCat(String c) async => (await SharedPreferences.getInstance()).setString('tssc_cat', c);

bool canOpenSolutions(Att a) {
  final id = s(a['mockId']).isNotEmpty ? s(a['mockId']) : s(a['paperId']);
  final ok = RegExp(r'_(tier1|tier2|cbt1|paper2|paper3)_mock\d+_(en|hi)$').hasMatch(id) || RegExp(r'^[a-z-]+_\d{4}_tier[12]_.*_(en|hi)$').hasMatch(id);
  return ok && a['answers'] is List;
}

void attemptActions(BuildContext context, DashCtx x, Att a) {
  final exam = x.exam;
  final key = lbKeyOf(a);
  showModalBottomSheet(
    context: context,
    backgroundColor: Colors.white,
    shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
    builder: (c) => SafeArea(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 10),
        child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Text(testName(a), style: baloo(19)),
          Text('${n1(marksOf(a))} / ${n1(maxOf(a))} marks · ${shortDate(tsOf(a))}', style: const TextStyle(color: softMuted, fontWeight: FontWeight.w600)),
          const SizedBox(height: 14),
          if (canOpenSolutions(a))
            FilledButton.icon(
              onPressed: () {
                Navigator.pop(c);
                openAttemptSolutions(context, exam, a);
              },
              style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              icon: const Icon(Icons.menu_book),
              label: const Text('View solutions', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
            ),
          if (key.isNotEmpty) ...[
            const SizedBox(height: 8),
            FilledButton.tonalIcon(
              onPressed: () async {
                Navigator.pop(c);
                await fetchRank(key, x.user.uid, from: a);
                if (!context.mounted) return;
                Navigator.of(context).push(MaterialPageRoute(builder: (_) => LeaderboardScreen(exam: exam, base: key, title: testName(a), uid: x.user.uid)));
              },
              style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              icon: const Icon(Icons.emoji_events_outlined),
              label: const Text('Leaderboard', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
            ),
          ],
          const SizedBox(height: 8),
          FilledButton.tonalIcon(
            onPressed: () {
              Navigator.pop(c);
              Navigator.of(context).push(MaterialPageRoute(builder: (_) => QuestionsPage(x: x, only: a)));
            },
            style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
            icon: const Icon(Icons.fact_check_outlined),
            label: const Text('Question by question', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
          ),
        ]),
      ),
    ),
  );
}

/// "View Result" on a finished mock / PYQ: score, solutions, leaderboard, question-by-question, retake.
void showDoneSheet(BuildContext context, {required User user, required Exam exam, required Att? a, required String title, required VoidCallback onRetake}) {
  showModalBottomSheet(
    context: context,
    backgroundColor: Colors.white,
    shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
    builder: (c) {
      final x = a == null ? null : DashCtx(user, exam, [a], scopeOf(a), 'GEN');
      final key = a == null ? '' : lbKeyOf(a);
      ButtonStyle tonal() => FilledButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)));
      return SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 10),
          child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Text(title, style: baloo(19)),
            if (a != null)
              Padding(
                padding: const EdgeInsets.only(top: 2),
                child: Text('${n1(marksOf(a))} / ${n1(maxOf(a))} marks · ✓${inum(a['correct'])} ✕${inum(a['wrong'])} · ${shortDate(tsOf(a))}', style: const TextStyle(color: softMuted, fontWeight: FontWeight.w700)),
              ),
            const SizedBox(height: 14),
            if (a != null && canOpenSolutions(a))
              FilledButton.icon(
                onPressed: () {
                  Navigator.pop(c);
                  openAttemptSolutions(context, exam, a);
                },
                style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                icon: const Icon(Icons.menu_book),
                label: const Text('View solutions', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
              ),
            if (key.isNotEmpty) ...[
              const SizedBox(height: 8),
              FilledButton.tonalIcon(
                onPressed: () async {
                  Navigator.pop(c);
                  if (a != null) await fetchRank(key, user.uid, from: a);
                  if (!context.mounted) return;
                  Navigator.of(context).push(MaterialPageRoute(builder: (_) => LeaderboardScreen(exam: exam, base: key, title: title, uid: user.uid)));
                },
                style: tonal(),
                icon: const Icon(Icons.emoji_events_outlined),
                label: const Text('Leaderboard', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
              ),
            ],
            if (x != null && answersOf(a!).isNotEmpty) ...[
              const SizedBox(height: 8),
              FilledButton.tonalIcon(
                onPressed: () {
                  Navigator.pop(c);
                  Navigator.of(context).push(MaterialPageRoute(builder: (_) => QuestionsPage(x: x, only: a)));
                },
                style: tonal(),
                icon: const Icon(Icons.fact_check_outlined),
                label: const Text('Question by question', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
              ),
            ],
            const SizedBox(height: 8),
            OutlinedButton.icon(
              onPressed: () {
                Navigator.pop(c);
                onRetake();
              },
              style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              icon: const Icon(Icons.replay_rounded),
              label: const Text('Retake test', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
            ),
          ]),
        ),
      );
    },
  );
}

// ====================================================================== 1. recent attempts

class AttemptsPage extends StatefulWidget {
  final DashCtx x;
  const AttemptsPage({super.key, required this.x});
  @override
  State<AttemptsPage> createState() => _AttemptsPageState();
}

class _AttemptsPageState extends State<AttemptsPage> {
  String _tab = 'all';
  int _show = 25;
  final _ranks = <String, LbInfo?>{};

  String _kind(Att a) => isChapter(a) ? 'chapter' : (isMockAtt(a) ? 'mock' : 'pyq');

  @override
  Widget build(BuildContext context) {
    final x = widget.x, exam = x.exam;
    final all = x.all;
    int cnt(String k) => k == 'all' ? all.length : all.where((a) => _kind(a) == k).length;
    final list = _tab == 'all' ? all : all.where((a) => _kind(a) == _tab).toList();
    final trend = all.where((a) => isFullPaper(a) && s(a['exam']) == exam.id).take(10).toList().reversed.toList();
    return DashPage(exam: exam, title: 'My recent attempts', children: [
      SizedBox(
        height: 44,
        child: ListView(scrollDirection: Axis.horizontal, children: [
          for (final t in const [('all', 'All'), ('pyq', 'PYQ'), ('mock', 'Mocks'), ('chapter', 'Chapter')]) SoftChip('${t.$2} ${cnt(t.$1)}', _tab == t.$1, exam.c1, () => setState(() => _tab = t.$1)),
        ]),
      ),
      const SizedBox(height: 10),
      if (trend.length >= 2 && _tab != 'chapter')
        PCard(title: 'Score trend', sub: 'Full tests, oldest to newest', children: [
          SizedBox(
            height: 130,
            child: Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
              for (final a in trend)
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 3),
                    child: Column(mainAxisAlignment: MainAxisAlignment.end, children: [
                      Text(n1(marksOf(a)), style: TextStyle(fontSize: 11, fontWeight: FontWeight.w800, color: exam.ink)),
                      const SizedBox(height: 2),
                      Container(
                        height: 6 + 96 * (marksOf(a) / maxOf(a)).clamp(0.0, 1.0),
                        decoration: BoxDecoration(borderRadius: BorderRadius.circular(6), gradient: LinearGradient(colors: [exam.c2, exam.c1], begin: Alignment.topCenter, end: Alignment.bottomCenter)),
                      ),
                    ]),
                  ),
                ),
            ]),
          ),
        ]),
      if (list.isEmpty) emptyNote('No tests here yet.'),
      for (final a in list.take(_show)) _row(a),
      if (list.length > _show)
        TextButton(onPressed: () => setState(() => _show += 50), child: Text('Show more (${list.length - _show} left)', style: TextStyle(fontWeight: FontWeight.w800, color: exam.c1))),
    ]);
  }

  Widget _row(Att a) {
    final x = widget.x, exam = x.exam;
    final k = _kind(a);
    final sm = isChapter(a) ? <String, double>{} : subjMarks(a);
    final key = lbKeyOf(a);
    final r = _ranks[key];
    final tag = switch (k) {
      'chapter' => SoftTag(a['type'] == 'pyq-chapter' ? 'PYQ · CHAPTER' : 'CHAPTER', const Color(0xFF0D9488), const Color(0xFFCCFBF1)),
      'mock' => SoftTag(s(a['subjectKey']).isNotEmpty ? 'MOCK · ${s(a['subjectKey']).toUpperCase()}' : 'MOCK', const Color(0xFF7C3AED), const Color(0xFFEDE9FE)),
      _ => const SoftTag('PYQ', Color(0xFFC2410C), Color(0xFFFFEDD5)),
    };
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      decoration: softCard(radius: 18),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(18),
          onTap: () => attemptActions(context, x, a),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(14, 12, 10, 12),
            child: Row(children: [
              Container(
                width: 58,
                height: 58,
                alignment: Alignment.center,
                decoration: softWell(),
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  Text(n1(marksOf(a)), style: baloo(18, color: exam.c1)),
                  Text('/${n1(maxOf(a))}', style: const TextStyle(fontSize: 11, color: softMuted, fontWeight: FontWeight.w700)),
                ]),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(testName(a), maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: softInk)),
                  const SizedBox(height: 3),
                  Wrap(spacing: 6, runSpacing: 4, crossAxisAlignment: WrapCrossAlignment.center, children: [
                    tag,
                    Text('✓${inum(a['correct'])}  ✕${inum(a['wrong'])}  · ${shortDate(tsOf(a))}', style: const TextStyle(fontSize: 12.5, color: softMuted, fontWeight: FontWeight.w700)),
                  ]),
                  if (sm.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(top: 3),
                      child: Text([for (final e in sm.entries) '${e.key} ${n1(e.value)}'].join(' · '), style: const TextStyle(fontSize: 12.5, color: Color(0xFF475569), fontWeight: FontWeight.w600)),
                    ),
                  if (key.isNotEmpty)
                    GestureDetector(
                      onTap: r != null || _ranks.containsKey(key)
                          ? null
                          : () async {
                              setState(() => _ranks[key] = null);
                              final v = await fetchRank(key, x.user.uid, from: a);
                              if (mounted) setState(() => _ranks[key] = v);
                            },
                      child: Padding(
                        padding: const EdgeInsets.only(top: 4),
                        child: Text(
                          r != null
                              ? (r.ok ? 'Rank #${r.rank} of ${r.total}' : 'Not ranked')
                              : (_ranks.containsKey(key) ? 'Loading rank…' : 'Show rank'),
                          style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w800, color: exam.c1, decoration: r == null && !_ranks.containsKey(key) ? TextDecoration.underline : null),
                        ),
                      ),
                    ),
                ]),
              ),
              const Icon(Icons.chevron_right_rounded, color: Color(0xFF94A3B8)),
            ]),
          ),
        ),
      ),
    );
  }
}

// ====================================================================== 2. rank

class RankPage extends StatefulWidget {
  final DashCtx x;
  const RankPage({super.key, required this.x});
  @override
  State<RankPage> createState() => _RankPageState();
}

class _RankPageState extends State<RankPage> {
  LbInfo? _v;
  @override
  void initState() {
    super.initState();
    final a = widget.x.latest;
    if (a != null && lbKeyOf(a).isNotEmpty) fetchRank(lbKeyOf(a), widget.x.user.uid, from: a).then((v) { if (mounted) setState(() => _v = v); });
  }

  @override
  Widget build(BuildContext context) {
    final x = widget.x, exam = x.exam, a = x.latest!;
    final k = lbKeyOf(a);
    final v = _v;
    return DashPage(exam: exam, title: 'Latest test rank', children: [
      PCard(title: testName(a), sub: shortDate(tsOf(a)), children: [
        if (k.isEmpty) ...[
          KV('Your marks', '${n1(marksOf(a))} / ${n1(maxOf(a))}'),
          KV('Accuracy', '${(lostOf(a).acc * 100).round()}%'),
          const Note('This test type has no leaderboard.'),
        ] else if (v == null)
          const Padding(padding: EdgeInsets.all(20), child: Center(child: CircularProgressIndicator()))
        else if (!v.ok)
          Note(v.none ? 'No leaderboard entry for this test yet — it appears after your next submit.' : 'Rank could not be loaded right now. Pull down later.')
        else ...[
          Big('#${v.rank}', 'of ${v.total} candidate${v.total == 1 ? '' : 's'}', exam.c1),
          KV('Percentile', n1(v.pctile)),
          KV('Your marks', '${n1(v.my)}${v.max > 0 ? ' / ${n1(v.max)}' : ''}'),
          KV('Topper${v.topName.isNotEmpty ? ' · ${v.topName}' : ''}', n1(v.top)),
          KV('Average', n1(v.avg)),
          if (v.top > v.my) KV('To reach the topper', '+${n1(v.top - v.my)} marks', color: cWarn),
        ],
      ]),
      if (v != null && v.ok && v.subj.isNotEmpty)
        PCard(title: 'Section rank', children: [
          for (final e in v.subj.entries)
            Builder(builder: (_) {
              final base = e.value.n > 0 ? e.value.n : v.total;
              final pc = base == 0 ? 0.0 : 1 - (e.value.ahead + 1) / base;
              return Bar('${e.key} · ${n1(e.value.my)}  (avg ${n1(e.value.avg)})', pc, '#${e.value.ahead + 1}', pc > .6 ? cGood : (pc > .3 ? cWarn : cBad));
            }),
        ]),
      if (k.isNotEmpty)
        FilledButton.icon(
          onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => LeaderboardScreen(exam: exam, base: k, title: testName(a), uid: x.user.uid))),
          style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16))),
          icon: const Icon(Icons.emoji_events_outlined),
          label: const Text('Full leaderboard', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
        ),
    ]);
  }
}

// ====================================================================== 3. cut-off

List<Att> cutoffTests(List<Att> sc) {
  final f = sc.where((a) => isFullPaper(a) && cutoffs[examTier(a)] != null).toList();
  if (f.isEmpty) return [];
  final t = examTier(f.first);
  return sc.where((a) => isFullPaper(a) && examTier(a) == t).toList();
}

class CutoffPage extends StatefulWidget {
  final DashCtx x;
  const CutoffPage({super.key, required this.x});
  @override
  State<CutoffPage> createState() => _CutoffPageState();
}

class _CutoffPageState extends State<CutoffPage> {
  late String _cat = widget.x.cat;

  @override
  Widget build(BuildContext context) {
    final x = widget.x, exam = x.exam;
    final t1 = cutoffTests(x.sc);
    final a = t1.first;
    final c = cutoffs[examTier(a)]!;
    final m = meritMarks(a), cut = c.cut[_cat]!, mx = c.max;
    final pn = posneg(a);
    final gap = m - cut;
    final qs = (gap.abs() / pn.pos).ceil();
    final l5 = t1.take(5).toList();
    final av = l5.fold(0.0, (t, x) => t + meritMarks(x)) / l5.length;
    final noSubj = c.merit && !subjMarks(a).keys.any((k) => 'QREG'.contains(k));
    return DashPage(exam: exam, title: 'Cut-off gap', children: [
      SizedBox(
        height: 44,
        child: ListView(scrollDirection: Axis.horizontal, children: [
          for (final k in cats)
            SoftChip(k, _cat == k, exam.c1, () {
              setState(() => _cat = k);
              saveCat(k);
            }),
        ]),
      ),
      const SizedBox(height: 10),
      PCard(title: 'vs ${c.label}', sub: testName(a), children: [
        LayoutBuilder(builder: (_, bc) {
          final w = bc.maxWidth;
          double at(double v) => (v.clamp(0, mx) / mx) * w;
          return SizedBox(
            height: 44,
            child: Stack(clipBehavior: Clip.none, children: [
              Positioned(
                left: 0,
                right: 0,
                top: 14,
                child: Container(height: 14, decoration: BoxDecoration(borderRadius: BorderRadius.circular(8), gradient: const LinearGradient(colors: [Color(0xFFFECACA), Color(0xFFFDE68A), Color(0xFFBBF7D0)]))),
              ),
              Positioned(left: at(cut) - 1.5, top: 6, child: Container(width: 3, height: 30, color: softInk)),
              Positioned(
                left: at(m) - 9,
                top: 12,
                child: Container(width: 18, height: 18, decoration: BoxDecoration(shape: BoxShape.circle, color: exam.c1, border: Border.all(color: Colors.white, width: 3))),
              ),
            ]),
          );
        }),
        Row(children: [
          const Text('0', style: TextStyle(color: softMuted, fontWeight: FontWeight.w700)),
          const Spacer(),
          Text('You ${n1(m)}', style: TextStyle(color: exam.c1, fontWeight: FontWeight.w800)),
          const Spacer(),
          Text('$_cat cut-off ${n1(cut)}', style: const TextStyle(color: softInk, fontWeight: FontWeight.w800)),
          const Spacer(),
          Text(n1(mx), style: const TextStyle(color: softMuted, fontWeight: FontWeight.w700)),
        ]),
        const SizedBox(height: 8),
        KV('Gap to $_cat', gap >= 0 ? '+${n1(gap)} · cleared' : '−${n1(-gap)} marks (≈$qs questions)', color: gap >= 0 ? cGood : cBad),
        KV('Your last-${l5.length} average', '${(av / cut * 100).round()}% of the way (${n1(av)})', color: av >= cut ? cGood : cWarn),
      ]),
      PCard(title: 'Other categories', children: [
        for (final k in cats.where((k) => k != _cat))
          Builder(builder: (_) {
            final g = m - c.cut[k]!;
            return KV('$k (${n1(c.cut[k]!)})', '${g >= 0 ? '+' : '−'}${n1(g.abs())}', color: g >= 0 ? cGood : cBad);
          }),
      ]),
      if (c.merit) Note('Tier II merit counts Section I + II only (Computer is qualifying), so this compares your Maths + Reasoning + English + GA marks out of 390.${noSubj ? ' This attempt has no section split, so its total (incl. Computer) is used.' : ''}'),
      if (c.prev != null) Note('${c.prevLabel} cut-off for $_cat was ${n1(c.prev![_cat]!)}. Cut-offs are normalised scores published by SSC; marks here are raw.'),
    ]);
  }
}

// ====================================================================== 4. lost marks

class LostPage extends StatelessWidget {
  final DashCtx x;
  const LostPage({super.key, required this.x});

  @override
  Widget build(BuildContext context) {
    final a = x.latest!;
    final L = lostOf(a);
    final lost = maxOf(a) - marksOf(a);
    final tot = (L.wrongMiss + L.penalty + L.skipped).clamp(1, double.infinity);
    const names = {'concept': 'Concept mistakes', 'calc': 'Calculation mistakes', 'silly': 'Silly / misread', 'guess': 'Guessed', 'time': 'Ran out of time', 'fact': 'Forgot fact / formula'};
    final guess = L.cnt['guess'] ?? 0;
    return DashPage(exam: x.exam, title: 'Where you lost marks', children: [
      PCard(title: 'You lost ${n1(lost)} marks', sub: testName(a), children: [
        Bar('Wrong answers (${L.w})', L.wrongMiss / tot, '−${n1(L.wrongMiss)}', cBad),
        Bar('Negative marking', L.penalty / tot, '−${n1(L.penalty)}', cWarn),
        Bar('Skipped (${L.k})', L.skipped / tot, '−${n1(L.skipped)}', cBlue),
        if (L.tagged > 0) ...[
          const SizedBox(height: 6),
          for (final e in names.entries)
            if ((L.cnt[e.key] ?? 0) > 0) KV(e.value, '${L.cnt[e.key]} question${L.cnt[e.key]! > 1 ? 's' : ''}'),
        ],
        Note('Recoverable: ~${n1(L.recover)} marks ${L.tagged > 0 ? 'by fixing calculation and silly mistakes alone.' : 'if you cut careless errors (estimate).'}'
            '${L.attempted > 0 ? ' You attempted ${L.attempted} of ${L.total} at ${(L.acc * 100).round()}% accuracy${guess > 0 ? '; $guess guess${guess > 1 ? 'es' : ''} cost ${n1(guess * L.neg)} marks' : ''}.' : ''}', color: cGood),
      ]),
    ]);
  }
}

// ====================================================================== 5. question selection

class SelectionPage extends StatelessWidget {
  final DashCtx x;
  const SelectionPage({super.key, required this.x});

  @override
  Widget build(BuildContext context) {
    final a = x.latest!;
    final ans = answersOf(a);
    final pn = posneg(a);
    final L = lostOf(a);
    String dkey(String d) {
      final l = d.toLowerCase();
      if (l.contains('easy')) return 'easy';
      if (RegExp(r'hard|difficult|tough').hasMatch(l)) return 'hard';
      if (RegExp(r'mod|med').hasMatch(l)) return 'moderate';
      return '';
    }

    final by = {for (final k in ['easy', 'moderate', 'hard']) k: [0, 0, 0, 0]}; // n c w k
    var riskyW = 0, easyK = 0, easyW = 0, good = 0;
    for (final q in ans) {
      final d = dkey(s(q['d']));
      final r = s(q['r']);
      if (d.isNotEmpty) {
        by[d]![0]++;
        by[d]![r == 'c' ? 1 : (r == 'w' ? 2 : 3)]++;
      }
      if (d == 'hard' && r == 'w') riskyW++;
      if (d == 'easy' && r == 'k') easyK++;
      if (d == 'easy' && r == 'w') easyW++;
      if (r == 'c' || (d == 'hard' && r == 'k')) good++;
    }
    final known = by.values.fold(0, (t, v) => t + v[0]);
    final e = by['easy']![0] > 0 ? by['easy']![1] / by['easy']![0] : 1.0;
    final m = by['moderate']![0] > 0 ? by['moderate']![1] / by['moderate']![0] : 1.0;
    return DashPage(exam: x.exam, title: 'Question selection', children: [
      PCard(title: 'Exam strategy', sub: testName(a), children: [
        KV('Attempted', '${L.attempted} / ${L.total}'),
        KV('Accuracy on attempted', '${(L.acc * 100).round()}%'),
        if (ans.isEmpty)
          const Note('Difficulty-wise analysis needs a test taken after the dashboard update.')
        else ...[
          KV('Good decisions', '$good', color: cGood),
          KV('Risky attempts on hard questions gone wrong', '$riskyW${riskyW > 0 ? ' — cost ${n1(riskyW * pn.neg)}' : ''}', color: riskyW > 0 ? cBad : cGood),
          KV('Easy questions you skipped', '$easyK${easyK > 0 ? ' — worth ${n1(easyK * pn.pos)}' : ''}', color: easyK > 0 ? cWarn : cGood),
          KV('Easy questions you got wrong', '$easyW', color: easyW > 0 ? cBad : cGood),
        ],
      ]),
      if (known > 0)
        PCard(title: 'Accuracy by difficulty', children: [
          for (final k in const [('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')])
            if (by[k.$1]![0] > 0)
              Builder(builder: (_) {
                final v = by[k.$1]!;
                final acc = v[1] / v[0];
                return Bar('${k.$2} (${v[0]})', acc, '${(acc * 100).round()}%', acc >= .75 ? cGood : (acc >= .5 ? cWarn : cBad));
              }),
          Note(e >= .85 && m < .7
              ? 'You are not losing on easy questions. Your marks are leaking on moderate ones.'
              : e < .85
                  ? 'Easy questions are slipping — those are the cheapest marks to recover.'
                  : 'Solid across difficulty levels; push attempts on moderate questions.'),
        ])
      else if (ans.isNotEmpty)
        emptyNote('Questions in this paper carry no difficulty tag yet.'),
    ]);
  }
}

// ====================================================================== 6. chapters

class ChaptersPage extends StatelessWidget {
  final DashCtx x;
  const ChaptersPage({super.key, required this.x});

  @override
  Widget build(BuildContext context) {
    final sc = x.sc;
    if (sc.isNotEmpty && isChapter(sc.first)) return _sets(context, sc);
    final ch = chapterStats(sc);
    final withData = sc.where((a) => answersOf(a).isNotEmpty).length;
    final tagged = ch.where((c) => c.name != 'Untagged' && c.n >= 3).toList();
    final weak = (tagged.where((c) => c.acc < .7).toList()..sort((a, b) => a.acc != b.acc ? a.acc.compareTo(b.acc) : b.n.compareTo(a.n))).take(8).toList();
    final strong = (tagged.where((c) => c.c > 0 && !weak.contains(c)).toList()..sort((a, b) => a.acc != b.acc ? b.acc.compareTo(a.acc) : b.n.compareTo(a.n))).take(8).toList();
    Widget row(ChStat c) => Bar('${c.name}  · ${c.n}×', c.acc, '${c.c}/${c.n}', accColor(c.acc));
    ChStat? top;
    if (weak.isNotEmpty) top = (weak.toList()..sort((a, b) => ((1 - b.acc) * b.n).compareTo((1 - a.acc) * a.n))).first;
    return DashPage(exam: x.exam, title: 'Chapter-wise accuracy', children: [
      if (ch.isEmpty)
        emptyNote('Chapter analysis covers tests taken after the dashboard update.')
      else ...[
        PCard(title: 'Weakest chapters', sub: '$withData test${withData == 1 ? '' : 's'} analysed', children: [
          if (weak.isEmpty) const Text('Nothing below 70% yet — nice.', style: TextStyle(color: softMuted, fontWeight: FontWeight.w600)),
          for (final c in weak) row(c),
          if (top != null)
            Note('Highest score opportunity: ${top.name} — appeared ${top.n} times in your tests, you get ${(top.acc * 100).round()}% right. '
                'Fixing it alone is worth ~${n1(top.n / (withData == 0 ? 1 : withData) * (1 - top.acc) * posneg(sc.first).pos)} marks per paper.', color: cWarn),
        ]),
        PCard(title: 'Strongest chapters', children: [
          if (strong.isEmpty) const Text('No chapter with a correct answer yet.', style: TextStyle(color: softMuted, fontWeight: FontWeight.w600)),
          for (final c in strong) row(c),
        ]),
      ],
    ]);
  }

  Widget _sets(BuildContext context, List<Att> sc) {
    final rows = sc.take(15).toList();
    double acc(Att a) {
      final n = inum(a['correct']) + inum(a['wrong']) + inum(a['skip']);
      return n == 0 ? 0 : inum(a['correct']) / n;
    }

    final lv = <int, List<int>>{};
    for (final a in sc) {
      final l = inum(a['level']) == 0 ? 1 : inum(a['level']);
      final g = lv.putIfAbsent(l, () => [0, 0, 0]);
      g[0] += inum(a['correct']);
      g[1] += inum(a['correct']) + inum(a['wrong']) + inum(a['skip']);
      g[2]++;
    }
    final best = (rows.toList()..sort((a, b) => acc(b).compareTo(acc(a)))).first;
    final worst = (rows.toList()..sort((a, b) => acc(a).compareTo(acc(b)))).first;
    return DashPage(exam: x.exam, title: 'Test-wise accuracy', children: [
      PCard(title: s(sc.first['chapterName']).isNotEmpty ? s(sc.first['chapterName']) : testName(sc.first), sub: '${sc.length} attempt${sc.length > 1 ? 's' : ''}', children: [
        for (final a in rows)
          Bar('${testName(a).split(' · ').skip(1).join(' · ')}${a['language'] == 'hi' ? ' · हिं' : ''} · ${shortDate(tsOf(a))}', acc(a),
              '${inum(a['correct'])}/${inum(a['correct']) + inum(a['wrong']) + inum(a['skip'])}', accColor(acc(a))),
        if (sc.first['type'] != 'pyq-chapter')
          Note('${(lv.keys.toList()..sort()).map((l) => 'Level $l: ${(lv[l]![0] / (lv[l]![1] == 0 ? 1 : lv[l]![1]) * 100).round()}% right over ${lv[l]![2]} test${lv[l]![2] > 1 ? 's' : ''}').join(' · ')}.'),
        if (rows.length > 1 && best != worst) Note('Best: ${testName(best).split(' · ').skip(1).join(' · ')} (${(acc(best) * 100).round()}%), weakest: ${testName(worst).split(' · ').skip(1).join(' · ')} (${(acc(worst) * 100).round()}%) — retake it.', color: cWarn),
      ]),
    ]);
  }
}

// ====================================================================== 7. readiness

int readiness(List<Att> sc) {
  final last = sc.take(5).toList();
  if (last.isEmpty) return 0;
  return (last.fold(0.0, (t, a) => t + marksOf(a) / maxOf(a)) / last.length * 100).round();
}

class ReadinessPage extends StatelessWidget {
  final DashCtx x;
  const ReadinessPage({super.key, required this.x});

  @override
  Widget build(BuildContext context) {
    final sc = x.sc, exam = x.exam;
    final last = sc.take(5).toList();
    final score = readiness(sc);
    final chScope = isChapter(last.first);
    final subj = subjectAcc(last)..sort((a, b) => b.acc.compareTo(a.acc));
    (String, Color) lab(double v) => v >= .75 ? ('Strong', cGood) : v >= .6 ? ('Good', cGood) : v >= .45 ? ('Improving', cWarn) : ('Weak', cBad);
    final lv = <int, List<int>>{};
    if (chScope) {
      for (final a in sc) {
        final l = inum(a['level']) == 0 ? 1 : inum(a['level']);
        final g = lv.putIfAbsent(l, () => [0, 0]);
        g[0] += inum(a['correct']);
        g[1] += inum(a['correct']) + inum(a['wrong']) + inum(a['skip']);
      }
    }
    String? trend;
    if (sc.length >= 6) {
      final l5 = sc.take(5).fold(0.0, (t, a) => t + marksOf(a)) / 5;
      final p = sc.skip(5).take(5).toList();
      final p5 = p.fold(0.0, (t, a) => t + marksOf(a)) / p.length;
      trend = 'Trend: last 5 avg ${n1(l5)} vs earlier avg ${n1(p5)} — ${l5 > p5 + 2 ? 'improving.' : l5 < p5 - 2 ? 'dipping — revise before the next test.' : 'steady.'}';
    }
    final allSubj = subjectAcc(sc)..sort((a, b) => a.acc.compareTo(b.acc));
    return DashPage(exam: exam, title: chScope ? 'Chapter readiness' : 'Exam readiness', children: [
      PCard(title: 'Last ${last.length} test${last.length > 1 ? 's' : ''}', children: [
        Row(children: [
          SizedBox(
            width: 110,
            height: 110,
            child: Stack(alignment: Alignment.center, children: [
              SizedBox(width: 110, height: 110, child: CircularProgressIndicator(value: score / 100, strokeWidth: 11, color: exam.c1, backgroundColor: const Color(0xFFEEF2FF), strokeCap: StrokeCap.round)),
              Column(mainAxisSize: MainAxisSize.min, children: [Text('$score', style: baloo(32, color: exam.c1)), const Text('/ 100', style: TextStyle(color: softMuted, fontWeight: FontWeight.w700))]),
            ]),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(children: [
              if (chScope) ...[
                for (final l in (lv.keys.toList()..sort())) Builder(builder: (_) {
                  final r = lab(lv[l]![1] == 0 ? 0 : lv[l]![0] / lv[l]![1]);
                  return KV('Level $l', r.$1, color: r.$2);
                }),
                if (!lv.containsKey(2) && last.first['type'] != 'pyq-chapter') const KV('Level 2', 'not attempted', color: softMuted),
              ] else
                for (final x in subj) Builder(builder: (_) {
                  final r = lab(x.acc);
                  return KV(x.name, r.$1, color: r.$2);
                }),
            ]),
          ),
        ]),
        if (trend != null) Note(trend),
        if (chScope)
          Note(score >= 75 ? 'You are ready to move on — try Level 2 sets or the next chapter.' : score >= 55 ? 'Getting there — revise the chapter notes, then retry the weakest set.' : 'Revise this chapter before the next attempt.')
        else if (subj.isNotEmpty)
          Note('Biggest score opportunity: ${subj.last.name}.', color: cWarn),
      ]),
      if (!chScope && allSubj.isNotEmpty)
        PCard(title: 'Subject accuracy', sub: 'All ${sc.length} tests in this group', children: [
          for (final x in allSubj) Bar(x.name, x.acc, '${(x.acc * 100).round()}%', accColor(x.acc)),
        ]),
    ]);
  }
}

// ====================================================================== 8. topper

class TopperPage extends StatefulWidget {
  final DashCtx x;
  const TopperPage({super.key, required this.x});
  @override
  State<TopperPage> createState() => _TopperPageState();
}

class _TopperPageState extends State<TopperPage> {
  LbInfo? _v;
  @override
  void initState() {
    super.initState();
    final a = widget.x.latest!;
    if (lbKeyOf(a).isNotEmpty) fetchRank(lbKeyOf(a), widget.x.user.uid, from: a).then((v) { if (mounted) setState(() => _v = v); });
  }

  @override
  Widget build(BuildContext context) {
    final x = widget.x, a = x.latest!, v = _v;
    Widget row(String l, String me, String tp, bool behind) => Padding(
          padding: const EdgeInsets.symmetric(vertical: 6),
          child: Row(children: [
            Expanded(child: Text(l, style: const TextStyle(fontSize: 14.5, color: Color(0xFF475569), fontWeight: FontWeight.w600))),
            SizedBox(width: 70, child: Text(me, textAlign: TextAlign.right, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: softInk))),
            SizedBox(width: 70, child: Text(tp, textAlign: TextAlign.right, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: behind ? cWarn : cGood))),
          ]),
        );
    final c = inum(a['correct']), w = inum(a['wrong']);
    final meAcc = c + w == 0 ? null : (c / (c + w) * 100).round();
    final nq = inum(a['total']) == 0 ? 100 : inum(a['total']);
    final meT = dnum(a['timeUsed']) > 0 ? (dnum(a['timeUsed']) / nq).round() : null;
    return DashPage(exam: x.exam, title: 'Compare with topper', children: [
      PCard(title: testName(a), children: [
        if (lbKeyOf(a).isEmpty)
          const Note('This test type has no leaderboard.')
        else if (v == null)
          const Padding(padding: EdgeInsets.all(20), child: Center(child: CircularProgressIndicator()))
        else if (!v.ok)
          Note(v.none ? 'Your score for this test is not on the leaderboard yet.' : 'Topper data could not be loaded right now.')
        else ...[
          row('', 'You', v.topName.isNotEmpty ? v.topName.split(' ').first : 'Topper', false),
          const Divider(height: 8),
          row('Score', n1(v.my), n1(v.top), v.top > v.my),
          if (meAcc != null && v.topAcc != null) row('Accuracy', '$meAcc%', '${v.topAcc!.round()}%', v.topAcc! > meAcc),
          if (meT != null && v.topTime > 0) row('Avg time / Q', '$meT s', '${(v.topTime / nq).round()} s', v.topTime / nq < meT),
          for (final e in v.topSubj.entries)
            if ((a['subjectMarks'] is Map) && (a['subjectMarks'] as Map).containsKey(e.key))
              row(e.key, n1(dnum((a['subjectMarks'] as Map)[e.key])), n1(e.value), e.value > dnum((a['subjectMarks'] as Map)[e.key])),
          row('Average student', n1(v.my), n1(v.avg), v.avg > v.my),
          Note(v.top > v.my ? 'You need +${n1(v.top - v.my)} marks to match the topper · you are #${v.rank} of ${v.total}.' : 'You are the topper on this test. 🏆', color: v.top > v.my ? cWarn : cGood),
        ],
      ]),
    ]);
  }
}

// ====================================================================== 9. time

class TimePage extends StatefulWidget {
  final DashCtx x;
  const TimePage({super.key, required this.x});
  @override
  State<TimePage> createState() => _TimePageState();
}

class _TimePageState extends State<TimePage> {
  LbInfo? _v;
  @override
  void initState() {
    super.initState();
    final a = widget.x.latest!;
    if (lbKeyOf(a).isNotEmpty) fetchRank(lbKeyOf(a), widget.x.user.uid, from: a).then((v) { if (mounted) setState(() => _v = v); });
  }

  @override
  Widget build(BuildContext context) {
    final x = widget.x, a = x.latest!;
    final ans = answersOf(a).where((q) => dnum(q['t']) > 0).toList();
    if (ans.isEmpty) return DashPage(exam: x.exam, title: 'Time analysis', children: [emptyNote('Per-question timing is recorded for tests taken after the dashboard update.')]);
    final tot = ans.fold(0.0, (t, q) => t + dnum(q['t']));
    final avg = tot / ans.length;
    final bySub = <String, List<double>>{};
    for (final q in ans) {
      final k = skey(s(q['s']));
      final nm = k == null ? (s(q['s']).isEmpty ? 'Other' : s(q['s'])) : subjName[k]!;
      final g = bySub.putIfAbsent(nm, () => [0, 0]);
      g[0] += dnum(q['t']);
      g[1]++;
    }
    final v = _v;
    final nq = inum(a['total']) == 0 ? 100 : inum(a['total']);
    final lbAvg = v != null && v.ok && v.tAvg > 0 ? v.tAvg / nq : 0.0;
    final slow = (ans.toList()..sort((p, q) => dnum(q['t']).compareTo(dnum(p['t'])))).take(3).toList();
    final st = slow.fold(0.0, (t, q) => t + dnum(q['t']));
    final eq = (st / (avg * .7 < 20 ? 20 : avg * .7)).round().clamp(1, 999);
    final subs = bySub.entries.where((e) => e.key != 'Other').toList()..sort((p, q) => (q.value[0] / q.value[1]).compareTo(p.value[0] / p.value[1]));
    return DashPage(exam: x.exam, title: 'Time analysis', children: [
      PCard(title: testName(a), children: [
        KV('Your avg / question', '${avg.round()} s'),
        if (lbAvg > 0) KV('Other candidates avg', '${lbAvg.round()} s'),
        if (dnum(a['timeUsed']) > 0) KV('Total time', fmtSec(dnum(a['timeUsed']))),
      ]),
      if (subs.isNotEmpty)
        PCard(title: 'By subject', children: [
          for (final e in subs) KV('${e.key} avg', '${(e.value[0] / e.value[1]).round()} s', color: e.value[0] / e.value[1] > avg * 1.3 ? cWarn : null),
        ]),
      PCard(title: 'Slowest questions', children: [
        for (final q in slow) KV('Q${q['q']}', '${dnum(q['t']).round()} s  ${q['r'] == 'c' ? '✓' : q['r'] == 'w' ? '✕' : 'skip'}', color: q['r'] == 'c' ? cGood : (q['r'] == 'w' ? cBad : softMuted)),
        Note('${st ~/ 60} min ${(st % 60).round()} s on your 3 slowest questions — that time is worth ~$eq easy questions (${n1(eq * posneg(a).pos)} marks).', color: cWarn),
      ]),
    ]);
  }
}

// ====================================================================== 10. question by question

class QuestionsPage extends StatefulWidget {
  final DashCtx x;
  final Att? only;
  const QuestionsPage({super.key, required this.x, this.only});
  @override
  State<QuestionsPage> createState() => _QuestionsPageState();
}

class _QuestionsPageState extends State<QuestionsPage> {
  late final List<Att> _tests = widget.only != null ? [widget.only!] : widget.x.sc.where((a) => answersOf(a).isNotEmpty).take(12).toList();
  int _sel = 0;
  Map<String, dynamic>? _qs;
  Map<int, ({String t, String c})>? _qt;
  String _filter = 'all';

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    if (_tests.isEmpty) return;
    setState(() {
      _qs = null;
      _qt = null;
    });
    final a = _tests[_sel];
    final r = await Future.wait([loadQstats(lbKeyOf(a)), loadQtext(a)]);
    if (mounted) {
      setState(() {
        _qs = r[0] as Map<String, dynamic>;
        _qt = r[1] as Map<int, ({String t, String c})>;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final x = widget.x, exam = x.exam;
    if (_tests.isEmpty) return DashPage(exam: exam, title: 'Question by question', children: [emptyNote('Question-wise performance is available for tests taken after the dashboard update.')]);
    final a = _tests[_sel];
    final key = lbKeyOf(a);
    final noStats = key.isEmpty;
    final qs = _qs, qt = _qt;
    final ans = answersOf(a)..sort((p, q) => inum(p['q']).compareTo(inum(q['q'])));
    final shown = ans.where((q) => _filter == 'all' || (_filter == 'wrong' ? q['r'] == 'w' : _filter == 'skip' ? q['r'] == 'k' : q['r'] == 'c')).toList();
    int estimate(Map q) {
      final d = s(q['d']);
      final base = d == 'easy' ? 76 : d == 'hard' ? 34 : d == 'moderate' ? 56 : 42 + (seed01('$key|${q['q']}') * 38).round();
      final jit = ((seed01('$key|${q['q']}j') - .5) * 14).round();
      return (base + jit).clamp(12, 94);
    }

    var e = 0, m = 0, h = 0, fast = 0, slow = 0, timed = 0;
    final rows = <Widget>[];
    for (final q in shown) {
      final st = qs == null ? null : ((qs['q'] as Map?) ?? {})['q${q['q']}'];
      int? pc;
      if (!noStats && qs != null) {
        final att = st is Map ? dnum(st['a']) : 0.0;
        final raw = att > 0 ? dnum(st['c']) * 100 / att : 0.0;
        pc = att >= 20 ? raw.round() : ((estimate(q) * 8 + raw * att) / (8 + att)).round();
      }
      final tn = st is Map ? dnum(st['tn']) : 0.0;
      final avgT = tn > 0 ? dnum(st['ts']) / tn : null;
      final my = dnum(q['t']);
      final lvl = pc != null ? (pc >= 70 ? ('Easy', cGood) : pc >= 40 ? ('Moderate', cWarn) : ('Hard', cBad)) : (s(q['d']).isNotEmpty ? (s(q['d'])[0].toUpperCase() + s(q['d']).substring(1), s(q['d']) == 'easy' ? cGood : s(q['d']) == 'hard' ? cBad : cWarn) : null);
      if (lvl != null) {
        if (lvl.$1 == 'Easy') {
          e++;
        } else if (lvl.$1 == 'Hard') {
          h++;
        } else {
          m++;
        }
      }
      Color? tc;
      if (avgT != null && my > 0 && !(q['r'] == 'k' && my <= 2)) {
        timed++;
        if (avgT.round() < my * .9) {
          slow++;
          tc = cBad;
        } else if (avgT.round() > my * 1.1) {
          fast++;
          tc = cGood;
        } else {
          tc = cWarn;
        }
      }
      final r = s(q['r']);
      final txt = qt?[inum(q['q'])]?.t ?? 'Question ${q['q']}${s(q['s']).isNotEmpty ? ' · ${subjName[skey(s(q['s']))] ?? q['s']}' : ''}';
      final corr = s(q['c']).isNotEmpty ? s(q['c']) : (qt?[inum(q['q'])]?.c ?? '—');
      rows.add(Container(
        margin: const EdgeInsets.only(bottom: 8),
        clipBehavior: Clip.antiAlias,
        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14)),
        child: IntrinsicHeight(
          child: Row(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Container(width: 5, color: r == 'c' ? cGood : (r == 'w' ? cBad : const Color(0xFFCBD5E1))),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(12, 10, 12, 10),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [
            Text('Q${q['q']}', style: baloo(16)),
            const SizedBox(width: 8),
            if (lvl != null) SoftTag(lvl.$1, lvl.$2, lvl.$2.withValues(alpha: .12)),
            const Spacer(),
            if (pc != null) Text('${qs != null && dnum((((qs['q'] as Map?) ?? {})['q${q['q']}'] as Map?)?['a']) < 20 ? '~' : ''}$pc% got it right', style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.w800, color: softMuted)),
          ]),
          const SizedBox(height: 4),
          Text(txt, maxLines: 3, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 14, color: Color(0xFF334155), height: 1.3)),
          const SizedBox(height: 6),
          Wrap(spacing: 14, runSpacing: 4, children: [
            Text('Correct $corr', style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w800, color: cGood)),
            Text(r == 'k' ? 'Skipped' : 'You ${s(q['a'])}', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800, color: r == 'c' ? cGood : (r == 'w' ? cBad : softMuted))),
            Text('Your time ${my > 0 ? fmtSec(my) : '—'}', style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: Color(0xFF475569))),
            if (avgT != null) Text('Avg ${tn < 20 ? '~' : ''}${fmtSec(avgT)}', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800, color: tc ?? softMuted)),
          ]),
        ]),
              ),
            ),
          ]),
        ),
      ));
    }
    return DashPage(exam: exam, title: 'Question by question', onRefresh: _load, children: [
      if (_tests.length > 1)
        SizedBox(
          height: 44,
          child: ListView(scrollDirection: Axis.horizontal, children: [
            for (var i = 0; i < _tests.length; i++)
              SoftChip('${testName(_tests[i]).length > 26 ? '${testName(_tests[i]).substring(0, 26)}…' : testName(_tests[i])} · ${shortDate(tsOf(_tests[i]))}', _sel == i, exam.c1, () {
                setState(() => _sel = i);
                _load();
              }),
          ]),
        ),
      if (_tests.length > 1) const SizedBox(height: 8),
      SizedBox(
        height: 44,
        child: ListView(scrollDirection: Axis.horizontal, children: [
          for (final f in const [('all', 'All'), ('wrong', 'Wrong'), ('skip', 'Skipped'), ('right', 'Correct')]) SoftChip(f.$2, _filter == f.$1, exam.c1, () => setState(() => _filter = f.$1)),
        ]),
      ),
      const SizedBox(height: 10),
      if (canOpenSolutions(a))
        Padding(
          padding: const EdgeInsets.only(bottom: 10),
          child: FilledButton.icon(
            onPressed: () => openAttemptSolutions(context, exam, a),
            style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(48), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
            icon: const Icon(Icons.menu_book),
            label: const Text('Open full solutions', style: TextStyle(fontWeight: FontWeight.w800)),
          ),
        ),
      if (qs == null) const Padding(padding: EdgeInsets.all(24), child: Center(child: CircularProgressIndicator())) else ...rows,
      if (qs != null)
        Note('${noStats ? 'Candidate-wide statistics are not collected for this test type; Level is the question\'s own difficulty tag. ' : '"% got it right" is an estimate (~) until 20 students have answered that question. '}'
            '${e + m + h > 0 ? 'Easy $e · Moderate $m · Hard $h. ' : ''}'
            '${timed > 0 ? 'Avg time is other candidates\' average: red = others were faster, green = you were faster, yellow = about the same. You were faster on $fast and slower on $slow of $timed timed questions.' : ''}'),
    ]);
  }
}

// ====================================================================== 11. report card

class ReportCardPage extends StatefulWidget {
  final DashCtx x;
  final String name;
  const ReportCardPage({super.key, required this.x, required this.name});
  @override
  State<ReportCardPage> createState() => _ReportCardPageState();
}

class _ReportCardPageState extends State<ReportCardPage> {
  final _key = GlobalKey();
  LbInfo? _v;
  bool _busy = false;

  @override
  void initState() {
    super.initState();
    final a = widget.x.latest!;
    if (lbKeyOf(a).isNotEmpty) fetchRank(lbKeyOf(a), widget.x.user.uid, from: a).then((v) { if (mounted) setState(() => _v = v); });
  }

  Future<void> _share() async {
    setState(() => _busy = true);
    try {
      final b = _key.currentContext!.findRenderObject() as RenderRepaintBoundary;
      final img = await b.toImage(pixelRatio: 3);
      final png = await img.toByteData(format: ui.ImageByteFormat.png);
      await Share.shareXFiles([XFile.fromData(png!.buffer.asUint8List(), mimeType: 'image/png', name: 'trickyssc-report-card.png')], text: 'My TrickySSC report card · trickyssc.com');
    } catch (_) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Could not share the card.')));
    }
    if (mounted) setState(() => _busy = false);
  }

  @override
  Widget build(BuildContext context) {
    final x = widget.x, exam = x.exam, sc = x.sc, a = sc.first;
    final marks = sc.map(marksOf).toList();
    final avg = marks.fold(0.0, (t, v) => t + v) / marks.length;
    final best = marks.reduce((p, q) => p > q ? p : q);
    final v = _v;
    final c = isFullPaper(a) ? cutoffs[examTier(a)] : null;
    final ch = chapterStats(sc).where((c) => c.name != 'Untagged' && c.n >= 3).toList();
    final weak = (ch.where((c) => c.acc < .7).toList()..sort((p, q) => p.acc.compareTo(q.acc))).take(4).toList();
    final strong = (ch.where((c) => c.acc >= .7).toList()..sort((p, q) => q.acc.compareTo(p.acc))).take(4).toList();
    final sub = subjectAcc(sc.take(5).toList());
    const w = TextStyle(color: Colors.white, fontWeight: FontWeight.w800);
    const g = TextStyle(color: Color(0xFF94A3B8), fontWeight: FontWeight.w600, fontSize: 12.5);
    Widget box(String v, String l) => Expanded(
          child: Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(color: const Color(0xFF1E293B), borderRadius: BorderRadius.circular(12)),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text(v, style: baloo(24, color: Colors.white)), Text(l, style: g)]),
          ),
        );
    final now = DateTime.now();
    const mo = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    return DashPage(exam: exam, title: 'Report card', children: [
      RepaintBoundary(
        key: _key,
        child: Container(
          padding: const EdgeInsets.fromLTRB(18, 0, 18, 16),
          decoration: BoxDecoration(color: const Color(0xFF0F172A), borderRadius: BorderRadius.circular(18)),
          child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Container(height: 6, margin: const EdgeInsets.only(bottom: 14), decoration: BoxDecoration(gradient: LinearGradient(colors: [exam.c1, exam.c2]))),
            Text('TrickySSC report card', style: baloo(24, color: Colors.white)),
            Text('${widget.name} · ${now.day} ${mo[now.month - 1]} ${now.year}', style: TextStyle(color: exam.c2, fontWeight: FontWeight.w800)),
            const SizedBox(height: 12),
            Row(children: [box('${sc.length}', isChapter(a) ? 'Chapter tests' : 'Tests'), const SizedBox(width: 8), box(n1(avg), 'Average marks'), const SizedBox(width: 8), box(n1(best), 'Best score')]),
            const SizedBox(height: 12),
            Text('Latest: ${testName(a)}', style: w),
            Text('${n1(marksOf(a))} / ${n1(maxOf(a))} marks${v != null && v.ok ? '  ·  Rank #${v.rank} of ${v.total}  ·  ${n1(v.pctile)} percentile' : ''}', style: const TextStyle(color: Color(0xFFCBD5E1), fontWeight: FontWeight.w600)),
            if (c != null)
              Builder(builder: (_) {
                final gap = meritMarks(a) - c.cut[x.cat]!;
                return Padding(
                  padding: const EdgeInsets.only(top: 6),
                  child: Text('${gap >= 0 ? 'Above' : 'Below'} ${x.cat} cut-off (${n1(c.cut[x.cat]!)}) by ${n1(gap.abs())} marks', style: TextStyle(color: gap >= 0 ? const Color(0xFF86EFAC) : const Color(0xFFFCA5A5), fontWeight: FontWeight.w800)),
                );
              }),
            const SizedBox(height: 12),
            Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              for (final col in [('Weak chapters', weak, const Color(0xFFFCA5A5)), ('Strong chapters', strong, const Color(0xFF86EFAC))])
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text(col.$1, style: w),
                    const SizedBox(height: 4),
                    if (col.$2.isEmpty) const Text('— after a few more tests', style: g),
                    for (final i in col.$2) Text('${i.name.length > 20 ? i.name.substring(0, 20) : i.name}  ${(i.acc * 100).round()}%', style: TextStyle(color: col.$3, fontWeight: FontWeight.w700, fontSize: 13)),
                  ]),
                ),
            ]),
            if (sub.isNotEmpty) ...[
              const SizedBox(height: 12),
              const Text('Subjects (last 5 tests)', style: w),
              const SizedBox(height: 6),
              for (final x in sub)
                Padding(
                  padding: const EdgeInsets.only(bottom: 6),
                  child: Stack(children: [
                    Container(height: 24, decoration: BoxDecoration(color: const Color(0xFF1E293B), borderRadius: BorderRadius.circular(6))),
                    FractionallySizedBox(widthFactor: x.acc.clamp(0.02, 1.0), child: Container(height: 24, decoration: BoxDecoration(color: x.acc >= .7 ? const Color(0xFF00A86B) : (x.acc >= .5 ? cWarn : cBad), borderRadius: BorderRadius.circular(6)))),
                    Positioned(left: 8, top: 3, child: Text('${x.name}  ${(x.acc * 100).round()}%', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 13))),
                  ]),
                ),
            ],
            const SizedBox(height: 10),
            const Text('trickyssc.com · free PYQs, mocks and chapter tests', style: g),
          ]),
        ),
      ),
      const SizedBox(height: 14),
      FilledButton.icon(
        onPressed: _busy ? null : _share,
        style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16))),
        icon: const Icon(Icons.share_rounded),
        label: const Text('Share report card', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
      ),
    ]);
  }
}

// ====================================================================== 12. profile

class ProfilePage extends StatefulWidget {
  final DashCtx x;
  const ProfilePage({super.key, required this.x});
  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  Map<String, dynamic>? _doc;
  @override
  void initState() {
    super.initState();
    FirebaseFirestore.instance.collection('users').doc(widget.x.user.uid).get().then<void>((d) { if (mounted) setState(() => _doc = d.data() ?? {}); }).catchError((_) { if (mounted) setState(() => _doc = {}); });
  }

  @override
  Widget build(BuildContext context) {
    final u = widget.x.user, exam = widget.x.exam;
    final name = s(_doc?['name']).isNotEmpty ? s(_doc!['name']) : (u.displayName ?? 'Student');
    final prov = u.providerData.isEmpty ? '' : u.providerData.first.providerId;
    final method = prov == 'google.com' ? '🔵 Google' : (prov == 'phone' ? '📱 Phone OTP' : (prov.isEmpty ? '—' : prov));
    final joined = u.metadata.creationTime;
    const mo = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    final phone = s(_doc?['phone']).isNotEmpty ? s(_doc!['phone']) : (u.phoneNumber ?? '—');
    return DashPage(exam: exam, title: 'My profile', children: [
      PCard(children: [
        Row(children: [
          CircleAvatar(
            radius: 30,
            backgroundColor: exam.c1,
            backgroundImage: u.photoURL != null ? NetworkImage(u.photoURL!) : null,
            child: u.photoURL == null ? Text(name.isEmpty ? 'S' : name[0].toUpperCase(), style: baloo(26, color: Colors.white)) : null,
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(name, style: baloo(21)),
              Text(u.email ?? u.phoneNumber ?? '', style: const TextStyle(color: softMuted, fontWeight: FontWeight.w600)),
            ]),
          ),
        ]),
        const SizedBox(height: 12),
        KV('Email', u.email ?? '—'),
        KV('Phone', _doc == null ? '…' : phone),
        KV('Member since', joined == null ? '—' : '${joined.day} ${mo[joined.month - 1]} ${joined.year}'),
        KV('Login method', method),
      ]),
    ]);
  }
}

// ====================================================================== 13. orders

String planName(String k) {
  final key = k.replaceFirst(RegExp(r'^p-'), '');
  for (final e in exams) {
    if (e.pass == key) return e.passName.isNotEmpty ? e.passName : '${e.name} Mock Test Series';
  }
  return key.replaceAll('-', ' ');
}

int _ms(dynamic v) {
  if (v is Timestamp) return v.millisecondsSinceEpoch;
  if (v is Map && v['seconds'] != null) return inum(v['seconds']) * 1000;
  return DateTime.tryParse(s(v))?.millisecondsSinceEpoch ?? 0;
}

String _longDate(int ms) {
  if (ms == 0) return '—';
  final d = DateTime.fromMillisecondsSinceEpoch(ms);
  const mo = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  return '${d.day} ${mo[d.month - 1]} ${d.year}';
}

/// Active plans from entitlements/{uid}: [(key, expiresMs, live)].
Future<List<(String, int, bool)>> loadPlans(String uid) async {
  try {
    final d = await FirebaseFirestore.instance.collection('entitlements').doc(uid).get();
    final mods = (d.data()?['modules'] as Map?) ?? {};
    final out = <(String, int, bool)>[];
    mods.forEach((k, m) {
      if ('$k'.contains('dashboard') || m is! Map || m['active'] != true) return;
      final t = _ms(m['expiresAt']);
      if (t == 0) return;
      out.add(('$k', t, t > DateTime.now().millisecondsSinceEpoch));
    });
    out.sort((a, b) => a.$3 != b.$3 ? (a.$3 ? -1 : 1) : a.$2.compareTo(b.$2));
    return out;
  } catch (_) {
    return [];
  }
}

class OrdersPage extends StatefulWidget {
  final DashCtx x;
  const OrdersPage({super.key, required this.x});
  @override
  State<OrdersPage> createState() => _OrdersPageState();
}

class _OrdersPageState extends State<OrdersPage> {
  List<(String, int, bool)>? _plans;
  List<Map<String, dynamic>>? _pays;

  @override
  void initState() {
    super.initState();
    loadPlans(widget.x.user.uid).then((p) { if (mounted) setState(() => _plans = p); });
    FirebaseFirestore.instance.collection('payments').where('uid', isEqualTo: widget.x.user.uid).get().then<void>((sn) {
      final l = [for (final d in sn.docs) d.data()]..sort((a, b) => (_ms(b['paidAt']) == 0 ? _ms(b['createdAt']) : _ms(b['paidAt'])).compareTo(_ms(a['paidAt']) == 0 ? _ms(a['createdAt']) : _ms(a['paidAt'])));
      if (mounted) setState(() => _pays = l);
    }).catchError((_) {
      if (mounted) setState(() => _pays = []);
    });
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.x.exam, plans = _plans, pays = _pays;
    return DashPage(exam: exam, title: 'My orders', children: [
      PCard(title: 'My plan', children: [
        if (plans == null)
          const Padding(padding: EdgeInsets.all(12), child: Center(child: CircularProgressIndicator()))
        else if (plans.where((p) => p.$3).isEmpty) ...[
          const Align(alignment: Alignment.centerLeft, child: SoftTag('FREE PLAN', softMuted, Color(0xFFF1F5F9))),
          const SizedBox(height: 6),
          const Text('No active purchase on this account.', style: TextStyle(color: softMuted, fontWeight: FontWeight.w600)),
        ] else
          const Align(alignment: Alignment.centerLeft, child: SoftTag.premium()),
        if (plans != null)
          for (final p in plans) KV(planName(p.$1), p.$3 ? 'till ${_longDate(p.$2)}' : 'expired ${_longDate(p.$2)}', color: p.$3 ? cGood : softMuted),
      ]),
      if (pays == null)
        const Padding(padding: EdgeInsets.all(20), child: Center(child: CircularProgressIndicator()))
      else if (pays.isEmpty)
        emptyNote('No purchases yet.')
      else
        for (final p in pays)
          PCard(title: s(p['productLabel']).isNotEmpty ? s(p['productLabel']) : planName(s(p['courseId'] ?? p['productId'])), trailing: Text('₹${rupees(p['amount'])}', style: baloo(20, color: exam.c1)), children: [
            Align(alignment: Alignment.centerLeft, child: p['status'] == 'paid' ? const SoftTag('PAID', cGood, Color(0xFFDCFCE7)) : const SoftTag('NOT COMPLETED', cWarn, Color(0xFFFEF3C7))),
            const SizedBox(height: 6),
            KV(p['status'] == 'paid' ? 'Paid on' : 'Tried on', _longDate(_ms(p['paidAt']) == 0 ? _ms(p['createdAt']) : _ms(p['paidAt']))),
            KV('Payment ID', s(p['paymentId']).isEmpty ? '—' : s(p['paymentId'])),
            KV('Order ID', s(p['orderId']).isEmpty ? '—' : s(p['orderId'])),
          ]),
      const Note('Keep your Payment ID handy if you ever need to contact us about a purchase. Questions? Write to contact@trickyssc.com.'),
    ]);
  }
}

/// 49.0 -> 49, 49.5 -> 49.50 (app purchases are saved as decimals, website ones as whole numbers).
String rupees(dynamic a) {
  final n = a is num ? a : num.tryParse('${a ?? ''}');
  if (n == null) return '${a ?? ''}';
  return n == n.roundToDouble() ? n.round().toString() : n.toStringAsFixed(2);
}
