// One test, all of its analysis on one screen: score and rank, subject-wise, you vs topper,
// you vs top students, quality of attempt and of time, lost marks, difficulty, time, painful questions
// and a table of every question.
// Opened by tapping an attempt (Dashboard > My recent attempts) or "View Result" on a test list.
import 'package:flutter/material.dart';

import '../../data.dart';
import '../../test/engine.dart' show subjectMockMinutes;
import '../../test/leaderboard.dart';
import '../../test/result_screen.dart';
import '../../ui/soft.dart';
import '../../ui/soft_list.dart';
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
  String _dSub = ''; // difficulty table: subject ('' = all)
  String _qf = 'all'; // question table filter
  int _qShow = 30;

  /// Seconds one question gets in this test (exam time / questions).
  double _limit(Exam exam) {
    final id = s(a['mockId']).isNotEmpty ? s(a['mockId']) : s(a['paperId']);
    final n = inum(a['total']) == 0 ? 100 : inum(a['total']);
    if (isChapter(a)) return 15 * 60 / n;
    if (id.contains('__')) return subjectMockMinutes(id.substring(0, id.indexOf('__')), id.substring(id.indexOf('__') + 2)) * 60 / n;
    if (RegExp(r'_paper[23]_').hasMatch(id)) return 120 * 60 / n;
    if (isTier2(a)) return 135 * 60 / n;
    final ex = examById(s(a['exam'])) ?? exam;
    final m = RegExp(r'(\d+)\s*Qs.*?(\d+)\s*min').firstMatch(ex.meta);
    if (m != null) return int.parse(m.group(2)!) * 60 / int.parse(m.group(1)!);
    return 36;
  }

  /// perfect | overtime | wasted | confused | '' for one saved answer.
  String _quality(Map q, double lim) {
    final t = dnum(q['t']);
    final r = s(q['r']);
    if (t <= 0) return '';
    if (r == 'k') return t > lim ? 'confused' : '';
    if (t > lim) return 'overtime';
    if (r == 'c') return 'perfect';
    return t < lim / 3 ? 'wasted' : '';
  }

  static const _qName = {'perfect': 'Perfect', 'overtime': 'Overtime', 'wasted': 'Wasted', 'confused': 'Confused'};
  static const _qCol = {'perfect': cGood, 'overtime': cWarn, 'wasted': cBad, 'confused': Color(0xFF64748B)};

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

    // ---- subject-wise
    final ss = a['subjectStats'] is Map ? a['subjectStats'] as Map : const {};
    final sm = a['subjectMarks'] is Map ? a['subjectMarks'] as Map : const {};

    // ---- question selection
    final lim = _limit(exam);
    String subOf(Map q) => subjName[skey(s(q['s']))] ?? '';
    final dSubs = {for (final q in ans) if (subOf(q).isNotEmpty) subOf(q)}.toList();
    if (!dSubs.contains(_dSub)) _dSub = '';
    final by = {for (final k in ['easy', 'moderate', 'hard']) k: [0, 0, 0, 0]}; // n, correct, wrong, skipped
    var riskyW = 0, easyK = 0, easyW = 0;
    for (final q in ans) {
      final d = _dkey(s(q['d']));
      final r = s(q['r']);
      if (d.isNotEmpty && (_dSub.isEmpty || subOf(q) == _dSub)) {
        by[d]![0]++;
        by[d]![r == 'c' ? 1 : (r == 'w' ? 2 : 3)]++;
      }
      if (d == 'hard' && r == 'w') riskyW++;
      if (d == 'easy' && r == 'k') easyK++;
      if (d == 'easy' && r == 'w') easyW++;
    }
    final knownDiff = ans.where((q) => _dkey(s(q['d'])).isNotEmpty).length;

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

    // ---- quality of attempt + of time
    final qual = <String, int>{'perfect': 0, 'overtime': 0, 'wasted': 0, 'confused': 0};
    final qualSub = <String, Map<String, int>>{};
    var tC = 0.0, tW = 0.0, tK = 0.0;
    for (final q in ans) {
      final k = _quality(q, lim);
      if (k.isNotEmpty) {
        qual[k] = qual[k]! + 1;
        final sb = subOf(q);
        if (sb.isNotEmpty) (qualSub[sb] ??= {'perfect': 0, 'overtime': 0, 'wasted': 0, 'confused': 0})[k] = qualSub[sb]![k]! + 1;
      }
      final tt = dnum(q['t']);
      if (q['r'] == 'c') {
        tC += tt;
      } else if (q['r'] == 'w') {
        tW += tt;
      } else {
        tK += tt;
      }
    }
    final tAll = tC + tW + tK;

    // ---- painful questions: wrong, or took too long — by chapter
    final pain = <String, List<Map<String, dynamic>>>{};
    for (final q in ans) {
      if (q['r'] != 'w' && _quality(q, lim) != 'overtime') continue;
      final raw = s(q['ch']).replaceAll(RegExp(r'<[^>]*>'), ' ').replaceAll(RegExp(r'\s+'), ' ').trim();
      (pain[raw.isEmpty ? (subOf(q).isEmpty ? 'Other' : subOf(q)) : chapterLabel(raw)] ??= []).add(q);
    }
    final painKeys = pain.keys.toList()..sort((p, q) => pain[q]!.length.compareTo(pain[p]!.length));

    // ---- question table
    final rowsQ = ans.where((q) => _qf == 'all' || (_qf == 'wrong' ? q['r'] == 'w' : _qf == 'skip' ? q['r'] == 'k' : _quality(q, lim) == 'overtime')).toList();

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

      // ================================================= you vs top students
      if (ok)
        PCard(title: 'You vs top students', sub: v.total > 1 ? 'You did better than ${v.pctile.round()}% of ${v.total} students' : null, children: [
          Builder(builder: (_) {
            final hasT = t > 0 && (v.topTime > 0 || v.bands.any((b) => b.time > 0));
            Widget row(String l, String sc, String tm, {Color? c, bool head = false}) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 5),
                  child: Row(children: [
                    Expanded(child: Text(l, maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(fontSize: 14.5, color: c ?? const Color(0xFF475569), fontWeight: c != null ? FontWeight.w800 : FontWeight.w600))),
                    SizedBox(width: 70, child: Text(sc, textAlign: TextAlign.right, style: TextStyle(fontSize: head ? 13 : 15, fontWeight: FontWeight.w800, color: head ? softMuted : (c ?? softInk)))),
                    if (hasT) SizedBox(width: 84, child: Text(tm, textAlign: TextAlign.right, style: TextStyle(fontSize: head ? 13 : 15, fontWeight: FontWeight.w800, color: head ? softMuted : (c ?? softInk)))),
                  ]),
                );
            String tm(double x) => x > 0 ? fmtSec(x) : '—';
            final target = v.bands.where((b) => b.marks > v.my).toList();
            return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              row('', 'Score', 'Time', head: true),
              const Divider(height: 8),
              row('You', n1(v.my), tm(t), c: exam.c1),
              for (final b in v.bands) row(b.label, n1(b.marks), tm(b.time)),
              row('Topper${v.topName.isNotEmpty ? ' · ${v.topName.split(' ').first}' : ''}', n1(v.top), tm(v.topTime), c: const Color(0xFFB45309)),
              row('Average student', n1(v.avg), tm(v.tAvg)),
              for (final e in v.topSubj.entries)
                if (sm.containsKey(e.key))
                  KV('${e.key} · you / ${v.bands.isNotEmpty && v.bands.first.subj[e.key] != null ? 'top 10% / ' : ''}topper',
                      '${n1(dnum(sm[e.key]))} / ${v.bands.isNotEmpty && v.bands.first.subj[e.key] != null ? '${n1(v.bands.first.subj[e.key]!)} / ' : ''}${n1(e.value)}'),
              Note(
                  v.top <= v.my
                      ? 'You are the topper on this test. 🏆'
                      : target.isNotEmpty
                          ? '+${n1(target.last.marks - v.my)} marks to reach the ${target.last.label.toLowerCase()} · +${n1(v.top - v.my)} to match the topper.'
                          : 'You are in the top group. +${n1(v.top - v.my)} marks to match the topper.',
                  color: v.top > v.my ? cWarn : cGood),
            ]);
          }),
        ]),

      // ================================================= quality of attempt + time
      if (tAll > 0)
        PCard(title: 'Quality of attempt', sub: 'Time per question in this test: ${lim.round()} s', children: [
          Row(children: [
            for (final k in const ['perfect', 'overtime', 'wasted', 'confused']) ...[
              if (k != 'perfect') const SizedBox(width: 6),
              Expanded(
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  decoration: BoxDecoration(color: _qCol[k]!.withValues(alpha: .1), borderRadius: BorderRadius.circular(12)),
                  child: Column(children: [
                    Text('${qual[k]}', style: baloo(20, color: _qCol[k]!)),
                    Text(_qName[k]!, style: TextStyle(fontSize: 12, fontWeight: FontWeight.w800, color: Color.lerp(_qCol[k]!, Colors.black, .25))),
                  ]),
                ),
              ),
            ],
          ]),
          if (qualSub.length > 1) ...[
            const SizedBox(height: 6),
            for (final e in qualSub.entries) KV(e.key, '${e.value['perfect']} perfect · ${e.value['overtime']} overtime · ${e.value['wasted']} wasted · ${e.value['confused']} confused'),
          ],
          const Note('Perfect: correct within the time. Overtime: took longer than the time. Wasted: wrong and answered very fast (a guess). Confused: spent the time, then skipped.'),
          const SizedBox(height: 12),
          const Text('Quality of time spent', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: softInk)),
          const SizedBox(height: 8),
          ClipRRect(
            borderRadius: BorderRadius.circular(7),
            child: SizedBox(
              height: 14,
              child: Row(children: [
                if (tC > 0) Expanded(flex: (tC * 1000 / tAll).round().clamp(1, 1000), child: Container(color: cGood)),
                if (tW > 0) Expanded(flex: (tW * 1000 / tAll).round().clamp(1, 1000), child: Container(color: cBad)),
                if (tK > 0) Expanded(flex: (tK * 1000 / tAll).round().clamp(1, 1000), child: Container(color: const Color(0xFFCBD5E1))),
              ]),
            ),
          ),
          KV('On correct answers', '${fmtSec(tC)} · ${(tC * 100 / tAll).round()}%', color: cGood),
          KV('On wrong answers', '${fmtSec(tW)} · ${(tW * 100 / tAll).round()}%', color: cBad),
          KV('On skipped questions', '${fmtSec(tK)} · ${(tK * 100 / tAll).round()}%', color: softMuted),
        ]),

      // ================================================= where marks were lost
      if (lost > 0)
        PCard(title: 'Where you lost ${n1(lost)} marks', children: [
          Bar('Wrong answers (${L.w})', L.wrongMiss / lostTot, '−${n1(L.wrongMiss)}', cBad),
          Bar('Negative marking', L.penalty / lostTot, '−${n1(L.penalty)}', cWarn),
          Bar('Skipped (${L.k})', L.skipped / lostTot, '−${n1(L.skipped)}', cBlue),
          if (L.w > 0) Note('Recoverable: ~${n1(L.recover)} marks if you cut careless mistakes.', color: cGood),
        ]),

      // ================================================= difficulty
      if (ans.isNotEmpty && knownDiff > 0)
        PCard(title: 'Difficulty', sub: 'Attempted ${L.attempted} of ${L.total}', children: [
          if (dSubs.length > 1)
            SizedBox(
              height: 44,
              child: ListView(scrollDirection: Axis.horizontal, children: [
                SoftChip('All', _dSub.isEmpty, exam.c1, () => setState(() => _dSub = '')),
                for (final sb in dSubs) SoftChip(sb, _dSub == sb, exam.c1, () => setState(() => _dSub = sb)),
              ]),
            ),
          Row(children: const [
            Expanded(child: SizedBox()),
            SizedBox(width: 64, child: Text('✓', textAlign: TextAlign.right, style: TextStyle(fontWeight: FontWeight.w800, color: cGood))),
            SizedBox(width: 48, child: Text('✕', textAlign: TextAlign.right, style: TextStyle(fontWeight: FontWeight.w800, color: cBad))),
            SizedBox(width: 48, child: Text('–', textAlign: TextAlign.right, style: TextStyle(fontWeight: FontWeight.w800, color: softMuted))),
          ]),
          const Divider(height: 10),
          for (final k in const [('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Tough')])
            if (by[k.$1]![0] > 0)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 5),
                child: Row(children: [
                  Expanded(child: Text(k.$2, style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w700, color: softInk))),
                  SizedBox(width: 64, child: Text('${by[k.$1]![1]}/${by[k.$1]![0]}', textAlign: TextAlign.right, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: cGood))),
                  SizedBox(width: 48, child: Text('${by[k.$1]![2]}', textAlign: TextAlign.right, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: cBad))),
                  SizedBox(width: 48, child: Text('${by[k.$1]![3]}', textAlign: TextAlign.right, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: softMuted))),
                ]),
              ),
          if (easyK > 0) KV('Easy questions you skipped', '$easyK · worth ${n1(easyK * pn.pos)}', color: cWarn),
          if (easyW > 0) KV('Easy questions you got wrong', '$easyW', color: cBad),
          if (riskyW > 0) KV('Tough questions gone wrong', '$riskyW · cost ${n1(riskyW * pn.neg)}', color: cBad),
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

      // ================================================= painful questions
      if (painKeys.isNotEmpty)
        PCard(title: 'Painful questions', sub: 'Wrong, or took too long — by chapter${canSol ? '. Tap to open the solution' : ''}', children: [
          for (final k in painKeys.take(12)) ...[
            Padding(
              padding: const EdgeInsets.only(top: 6, bottom: 6),
              child: Text('$k (${pain[k]!.length})', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w800, color: Color(0xFF334155))),
            ),
            Wrap(spacing: 8, runSpacing: 8, children: [for (final q in pain[k]!) chipQ(q, q['r'] == 'w' ? cBad : cWarn)]),
          ],
          const Note('Red: wrong answer. Orange: right, but over the time.', color: softMuted),
        ]),

      // ================================================= all questions
      if (ans.isNotEmpty)
        PCard(title: 'All questions', children: [
          SizedBox(
            height: 44,
            child: ListView(scrollDirection: Axis.horizontal, children: [
              for (final f in const [('all', 'All'), ('wrong', 'Wrong'), ('over', 'Overtime'), ('skip', 'Skipped')])
                SoftChip(f.$2, _qf == f.$1, exam.c1, () => setState(() {
                      _qf = f.$1;
                      _qShow = 30;
                    })),
            ]),
          ),
          if (rowsQ.isEmpty) const Padding(padding: EdgeInsets.all(8), child: Text('No questions here.', style: TextStyle(color: softMuted, fontWeight: FontWeight.w600))),
          for (final q in rowsQ.take(_qShow))
            Builder(builder: (_) {
              final r = s(q['r']);
              final k = _quality(q, lim);
              final rawCh = s(q['ch']).trim();
              final d = _dkey(s(q['d']));
              final lab = k.isNotEmpty ? _qName[k]! : (r == 'c' ? 'Correct' : r == 'w' ? 'Wrong' : 'Skipped');
              final col = k.isNotEmpty ? _qCol[k]! : (r == 'c' ? cGood : r == 'w' ? cBad : softMuted);
              return InkWell(
                onTap: canSol ? () => _solutions(q: inum(q['q'])) : null,
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  decoration: const BoxDecoration(border: Border(top: BorderSide(color: Color(0xFFEEF2FF)))),
                  child: Row(children: [
                    Container(width: 4, height: 34, margin: const EdgeInsets.only(right: 8), decoration: BoxDecoration(color: r == 'c' ? cGood : (r == 'w' ? cBad : const Color(0xFFCBD5E1)), borderRadius: BorderRadius.circular(2))),
                    SizedBox(width: 40, child: Text('Q${q['q']}', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w800, color: softInk))),
                    Expanded(
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text(rawCh.isEmpty ? (subOf(q).isEmpty ? '—' : subOf(q)) : chapterLabel(rawCh), maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 13.5, fontWeight: FontWeight.w700, color: Color(0xFF334155))),
                        Text('${d.isEmpty ? '' : '${d == 'hard' ? 'Tough' : d[0].toUpperCase() + d.substring(1)} · '}${dnum(q['t']) > 0 ? fmtSec(dnum(q['t'])) : 'no time'}', style: const TextStyle(fontSize: 12.5, color: softMuted, fontWeight: FontWeight.w600)),
                      ]),
                    ),
                    const SizedBox(width: 8),
                    Text(lab, style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800, color: col)),
                    if (canSol) const Icon(Icons.chevron_right_rounded, size: 18, color: Color(0xFF94A3B8)),
                  ]),
                ),
              );
            }),
          if (rowsQ.length > _qShow)
            TextButton(onPressed: () => setState(() => _qShow += 100), child: Text('Show all ${rowsQ.length} questions', style: TextStyle(fontWeight: FontWeight.w800, color: exam.c1))),
        ]),

      if (ans.isEmpty) emptyNote('Detailed analysis is available for tests taken after the dashboard update.'),

      // ================================================= actions
      if (ok)
        FilledButton.tonalIcon(
          onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => LeaderboardScreen(exam: exam, base: key, title: testName(a), uid: x.user.uid))),
          style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
          icon: const Icon(Icons.emoji_events_outlined),
          label: const Text('Leaderboard', style: TextStyle(fontWeight: FontWeight.w800)),
        ),
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
