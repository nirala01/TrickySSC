// One test, all of its analysis on one screen: score and rank, subject-wise, you vs topper,
// where marks were lost, question selection, time, weak topics and the wrong questions.
// Opened by tapping an attempt (Dashboard > My recent attempts) or "View Result" on a test list.
import 'package:flutter/material.dart';

import '../../test/leaderboard.dart';
import '../../test/result_screen.dart';
import '../../ui/soft.dart';
import 'logic.dart';
import 'pages.dart';
import 'ui.dart';

class TestAnalysisPage extends StatefulWidget {
  final DashCtx x;
  final Att a;
  final VoidCallback? onRetake;
  const TestAnalysisPage({super.key, required this.x, required this.a, this.onRetake});
  @override
  State<TestAnalysisPage> createState() => _TestAnalysisPageState();
}

class _TestAnalysisPageState extends State<TestAnalysisPage> {
  LbInfo? _v;
  bool _lbDone = false;

  Att get a => widget.a;

  @override
  void initState() {
    super.initState();
    final k = lbKeyOf(a);
    if (k.isEmpty) {
      _lbDone = true;
    } else {
      fetchRank(k, widget.x.user.uid, from: a).then((v) {
        if (mounted) {
          setState(() {
            _v = v;
            _lbDone = true;
          });
        }
      });
    }
  }

  String _dkey(String d) {
    final l = d.toLowerCase();
    if (l.contains('easy')) return 'easy';
    if (RegExp(r'hard|difficult|tough').hasMatch(l)) return 'hard';
    if (RegExp(r'mod|med').hasMatch(l)) return 'moderate';
    return '';
  }

  void _solutions({int? q}) => openAttemptSolutions(context, widget.x.exam, a, openQ: q);

  @override
  Widget build(BuildContext context) {
    final x = widget.x, exam = x.exam;
    final ok = _v != null && _v!.ok;
    final v = _v ?? LbInfo(err: true);
    final key = lbKeyOf(a);
    final canSol = canOpenSolutions(a);
    final ans = answersOf(a)..sort((p, q) => inum(p['q']).compareTo(inum(q['q'])));
    final L = lostOf(a);
    final pn = posneg(a);
    final marks = marksOf(a), max = maxOf(a);
    final t = dnum(a['timeUsed']);
    final nq = L.total;

    // ---- subject-wise
    final ss = a['subjectStats'] is Map ? a['subjectStats'] as Map : const {};
    final sm = a['subjectMarks'] is Map ? a['subjectMarks'] as Map : const {};

    // ---- question selection
    final by = {for (final k in ['easy', 'moderate', 'hard']) k: [0, 0]}; // n, correct
    var riskyW = 0, easyK = 0, easyW = 0;
    for (final q in ans) {
      final d = _dkey(s(q['d']));
      final r = s(q['r']);
      if (d.isNotEmpty) {
        by[d]![0]++;
        if (r == 'c') by[d]![1]++;
      }
      if (d == 'hard' && r == 'w') riskyW++;
      if (d == 'easy' && r == 'k') easyK++;
      if (d == 'easy' && r == 'w') easyW++;
    }
    final knownDiff = by.values.fold(0, (s, v) => s + v[0]);

    // ---- time
    final timed = ans.where((q) => dnum(q['t']) > 0).toList();
    final avgT = timed.isEmpty ? 0.0 : timed.fold(0.0, (s, q) => s + dnum(q['t'])) / timed.length;
    final bySub = <String, List<double>>{};
    for (final q in timed) {
      final k = skey(s(q['s']));
      if (k == null) continue;
      final g = bySub.putIfAbsent(subjName[k]!, () => [0, 0]);
      g[0] += dnum(q['t']);
      g[1]++;
    }
    final slow = (timed.toList()..sort((p, q) => dnum(q['t']).compareTo(dnum(p['t'])))).take(3).toList();
    final othersAvg = ok && v.tAvg > 0 ? v.tAvg : 0.0;

    // ---- weak topics (this test only)
    final ch = chapterStats([a]).where((c) => c.name != 'Untagged' && c.n >= 2).toList();
    final weak = (ch.where((c) => c.acc < .7).toList()..sort((p, q) => p.acc != q.acc ? p.acc.compareTo(q.acc) : q.n.compareTo(p.n))).take(6).toList();
    final strong = (ch.where((c) => c.acc >= .8).toList()..sort((p, q) => q.n.compareTo(p.n))).take(3).toList();

    // ---- wrong / skipped questions
    final wrong = ans.where((q) => q['r'] == 'w').toList();
    final skipped = ans.where((q) => q['r'] == 'k').toList();

    Widget chipQ(Map q, Color c) => Material(
          color: c.withValues(alpha: .12),
          borderRadius: BorderRadius.circular(10),
          child: InkWell(
            borderRadius: BorderRadius.circular(10),
            onTap: canSol ? () => _solutions(q: inum(q['q'])) : null,
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              child: Text('Q${q['q']}', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w800, color: Color.lerp(c, Colors.black, .2))),
            ),
          ),
        );

    Widget cmpRow(String l, String me, String tp, {bool behind = false, bool head = false}) => Padding(
          padding: const EdgeInsets.symmetric(vertical: 5),
          child: Row(children: [
            Expanded(child: Text(l, style: TextStyle(fontSize: 14.5, color: const Color(0xFF475569), fontWeight: head ? FontWeight.w800 : FontWeight.w600))),
            SizedBox(width: 72, child: Text(me, textAlign: TextAlign.right, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: head ? exam.c1 : softInk))),
            SizedBox(width: 78, child: Text(tp, textAlign: TextAlign.right, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: head ? const Color(0xFFB45309) : (behind ? cWarn : cGood)))),
          ]),
        );

    Widget stat(String val, String lab, Color c) => Expanded(
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 10),
            decoration: softCard(radius: 16, glow: c),
            child: Column(children: [
              Text(val, style: baloo(21, color: c)),
              Text(lab, style: const TextStyle(fontSize: 12.5, color: softMuted, fontWeight: FontWeight.w700)),
            ]),
          ),
        );

    final lost = (max - marks).clamp(0, double.infinity);
    final lostTot = (L.wrongMiss + L.penalty + L.skipped).clamp(1, double.infinity);

    return DashPage(exam: exam, title: 'Test analysis', children: [
      // ================================================= score + rank
      Container(
        padding: const EdgeInsets.all(18),
        margin: const EdgeInsets.only(bottom: 10),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(22),
          gradient: LinearGradient(colors: [exam.c1, Color.lerp(exam.c1, exam.c2, .55)!], begin: Alignment.topLeft, end: Alignment.bottomRight),
        ),
        child: Row(children: [
          Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(testName(a), maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Color(0xEEFFFFFF), fontSize: 13.5, fontWeight: FontWeight.w700)),
              const SizedBox(height: 2),
              Text('${n1(marks)} / ${n1(max)}', style: baloo(32, color: Colors.white)),
              Text('${max == 0 ? 0 : (marks * 100 / max).round()}%${t > 0 ? ' · ${fmtSec(t)} used' : ''} · ${shortDate(tsOf(a))}',
                  style: const TextStyle(color: Color(0xEEFFFFFF), fontSize: 13, fontWeight: FontWeight.w600)),
            ]),
          ),
          if (ok)
            GestureDetector(
              onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => LeaderboardScreen(exam: exam, base: key, title: testName(a), uid: x.user.uid))),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 9),
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16)),
                child: Column(children: [
                  Text('#${v.rank}', style: baloo(24, color: exam.c1)),
                  Text('of ${v.total}', style: const TextStyle(fontSize: 12, color: Color(0xFF64748B), fontWeight: FontWeight.w700)),
                ]),
              ),
            )
          else if (!_lbDone)
            const SizedBox(width: 22, height: 22, child: CircularProgressIndicator(strokeWidth: 2.4, color: Colors.white)),
        ]),
      ),
      Row(children: [
        stat('${L.c}', 'Correct', cGood),
        const SizedBox(width: 8),
        stat('${L.w}', 'Wrong', cBad),
        const SizedBox(width: 8),
        stat('${L.k}', 'Skipped', softMuted),
        const SizedBox(width: 8),
        stat('${(L.acc * 100).round()}%', 'Accuracy', exam.c1),
      ]),
      const SizedBox(height: 12),
      if (canSol)
        Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: FilledButton.icon(
            onPressed: _solutions,
            style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
            icon: const Icon(Icons.menu_book),
            label: const Text('View solutions', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
          ),
        ),

      // ================================================= subject-wise
      if (ss.isNotEmpty)
        PCard(title: 'Subject-wise', children: [
          Row(children: [
            const Expanded(child: SizedBox()),
            const SizedBox(width: 34, child: Text('✓', textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.w800, color: cGood))),
            const SizedBox(width: 34, child: Text('✕', textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.w800, color: cBad))),
            const SizedBox(width: 52, child: Text('Marks', textAlign: TextAlign.right, style: TextStyle(fontWeight: FontWeight.w800))),
            if (ok && v.subj.isNotEmpty) const SizedBox(width: 50, child: Text('Rank', textAlign: TextAlign.right, style: TextStyle(fontWeight: FontWeight.w800))),
          ]),
          const Divider(),
          for (final e in ss.entries)
            if (e.value is Map)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Row(children: [
                  Expanded(child: Text('${e.key}', style: const TextStyle(fontWeight: FontWeight.w700, color: softInk))),
                  SizedBox(width: 34, child: Text('${inum((e.value as Map)['correct'])}', textAlign: TextAlign.center)),
                  SizedBox(width: 34, child: Text('${inum((e.value as Map)['wrong'])}', textAlign: TextAlign.center)),
                  SizedBox(
                      width: 52,
                      child: Text(sm.containsKey(e.key) ? n1(dnum(sm[e.key])) : n1(inum((e.value as Map)['correct']) * pn.pos - inum((e.value as Map)['wrong']) * pn.neg),
                          textAlign: TextAlign.right, style: const TextStyle(fontWeight: FontWeight.w800))),
                  if (ok && v.subj.isNotEmpty)
                    SizedBox(width: 50, child: Text(v.subj['${e.key}'] == null ? '—' : '#${v.subj['${e.key}']!.ahead + 1}', textAlign: TextAlign.right, style: TextStyle(fontWeight: FontWeight.w800, color: exam.c1))),
                ]),
              ),
        ]),

      // ================================================= you vs topper
      if (ok)
        PCard(title: 'You vs topper', sub: v.total > 1 ? 'You did better than ${v.pctile.round()}% of ${v.total} students' : null, children: [
          cmpRow('', 'You', v.topName.isNotEmpty ? v.topName.split(' ').first : 'Topper', head: true),
          const Divider(height: 8),
          cmpRow('Marks', n1(v.my), n1(v.top), behind: v.top > v.my),
          if (L.attempted > 0 && v.topAcc != null) cmpRow('Accuracy', '${(L.acc * 100).round()}%', '${v.topAcc!.round()}%', behind: v.topAcc! > L.acc * 100),
          if (t > 0 && v.topTime > 0) cmpRow('Avg time / Q', '${(t / nq).round()} s', '${(v.topTime / nq).round()} s', behind: v.topTime / nq < t / nq),
          for (final e in v.topSubj.entries)
            if (sm.containsKey(e.key)) cmpRow(e.key, n1(dnum(sm[e.key])), n1(e.value), behind: e.value > dnum(sm[e.key])),
          cmpRow('Average student', n1(v.my), n1(v.avg), behind: v.avg > v.my),
          Note(v.top > v.my ? 'You need +${n1(v.top - v.my)} marks to match the topper.' : 'You are the topper on this test. 🏆', color: v.top > v.my ? cWarn : cGood),
        ]),

      // ================================================= where marks were lost
      if (lost > 0)
        PCard(title: 'Where you lost ${n1(lost)} marks', children: [
          Bar('Wrong answers (${L.w})', L.wrongMiss / lostTot, '−${n1(L.wrongMiss)}', cBad),
          Bar('Negative marking', L.penalty / lostTot, '−${n1(L.penalty)}', cWarn),
          Bar('Skipped (${L.k})', L.skipped / lostTot, '−${n1(L.skipped)}', cBlue),
          if (L.w > 0) Note('Recoverable: ~${n1(L.recover)} marks if you cut careless mistakes.', color: cGood),
        ]),

      // ================================================= question selection
      if (ans.isNotEmpty && knownDiff > 0)
        PCard(title: 'Question selection', sub: 'Attempted ${L.attempted} of ${L.total}', children: [
          for (final k in const [('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')])
            if (by[k.$1]![0] > 0)
              Builder(builder: (_) {
                final acc = by[k.$1]![1] / by[k.$1]![0];
                return Bar('${k.$2} questions (${by[k.$1]![0]})', acc, '${(acc * 100).round()}% right', accColor(acc));
              }),
          if (easyK > 0) KV('Easy questions you skipped', '$easyK · worth ${n1(easyK * pn.pos)}', color: cWarn),
          if (easyW > 0) KV('Easy questions you got wrong', '$easyW', color: cBad),
          if (riskyW > 0) KV('Hard questions gone wrong', '$riskyW · cost ${n1(riskyW * pn.neg)}', color: cBad),
        ]),

      // ================================================= time
      if (timed.isNotEmpty)
        PCard(title: 'Time', children: [
          if (t > 0) KV('Your total time', fmtSec(t)),
          if (othersAvg > 0) KV('Other students\' average', fmtSec(othersAvg)),
          KV('Your average per question', '${avgT.round()} s'),
          if (bySub.length > 1)
            for (final e in bySub.entries) KV('${e.key} · per question', '${(e.value[0] / e.value[1]).round()} s', color: e.value[0] / e.value[1] > avgT * 1.3 ? cWarn : null),
          if (slow.isNotEmpty) ...[
            const SizedBox(height: 4),
            const Text('Slowest questions', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w800, color: Color(0xFF334155))),
            const SizedBox(height: 6),
            Wrap(spacing: 8, runSpacing: 8, children: [
              for (final q in slow)
                Material(
                  color: const Color(0xFFF1F5F9),
                  borderRadius: BorderRadius.circular(10),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(10),
                    onTap: canSol ? () => _solutions(q: inum(q['q'])) : null,
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7),
                      child: Text('Q${q['q']} · ${fmtSec(dnum(q['t']))} ${q['r'] == 'c' ? '✓' : q['r'] == 'w' ? '✕' : '–'}',
                          style: TextStyle(fontSize: 13.5, fontWeight: FontWeight.w800, color: q['r'] == 'c' ? cGood : (q['r'] == 'w' ? cBad : softMuted))),
                    ),
                  ),
                ),
            ]),
          ],
        ]),

      // ================================================= weak topics
      if (weak.isNotEmpty || strong.isNotEmpty)
        PCard(title: 'Topics in this test', children: [
          for (final c in weak) Bar('${c.name} · ${c.n} Qs', c.acc, '${c.c}/${c.n}', accColor(c.acc)),
          for (final c in strong) Bar('${c.name} · ${c.n} Qs', c.acc, '${c.c}/${c.n}', accColor(c.acc)),
          if (weak.isNotEmpty) Note('Revise ${weak.first.name} first — it cost you the most in this test.', color: cWarn),
        ]),

      // ================================================= wrong + skipped questions
      if (wrong.isNotEmpty || skipped.isNotEmpty)
        PCard(title: 'Questions to review', sub: canSol ? 'Tap a question to open its solution' : null, children: [
          if (wrong.isNotEmpty) ...[
            Text('Wrong (${wrong.length})', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w800, color: cBad)),
            const SizedBox(height: 6),
            Wrap(spacing: 8, runSpacing: 8, children: [for (final q in wrong) chipQ(q, cBad)]),
          ],
          if (skipped.isNotEmpty) ...[
            const SizedBox(height: 12),
            Text('Skipped (${skipped.length})', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w800, color: softMuted)),
            const SizedBox(height: 6),
            Wrap(spacing: 8, runSpacing: 8, children: [for (final q in skipped.take(40)) chipQ(q, const Color(0xFF64748B))]),
          ],
        ]),

      if (ans.isEmpty) emptyNote('Detailed analysis is available for tests taken after the dashboard update.'),

      // ================================================= actions
      Row(children: [
        if (ok)
          Expanded(
            child: FilledButton.tonalIcon(
              onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => LeaderboardScreen(exam: exam, base: key, title: testName(a), uid: x.user.uid))),
              style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              icon: const Icon(Icons.emoji_events_outlined),
              label: const Text('Leaderboard', style: TextStyle(fontWeight: FontWeight.w800)),
            ),
          ),
        if (ok && ans.isNotEmpty) const SizedBox(width: 8),
        if (ans.isNotEmpty)
          Expanded(
            child: FilledButton.tonalIcon(
              onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => QuestionsPage(x: x, only: a))),
              style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              icon: const Icon(Icons.fact_check_outlined),
              label: const Text('Each question', style: TextStyle(fontWeight: FontWeight.w800)),
            ),
          ),
      ]),
      if (widget.onRetake != null) ...[
        const SizedBox(height: 8),
        OutlinedButton.icon(
          onPressed: () {
            Navigator.of(context).pop();
            widget.onRetake!();
          },
          style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
          icon: const Icon(Icons.replay_rounded),
          label: const Text('Retake test', style: TextStyle(fontWeight: FontWeight.w800)),
        ),
      ],
    ]);
  }
}
