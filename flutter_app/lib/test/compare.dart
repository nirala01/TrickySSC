// "How you compare" — a port of the website solutions screen (TSSC-RVPAGER-V4/V5, TOPPER-V2):
// real figures from qstats once 20 students have answered, realistic estimates before that,
// using the same seed so the app and the website show the same numbers.
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';

import 'engine.dart';

const int _minN = 20;
const int _k = 8;

class CmpItem {
  final String qn; // qNum as text
  final String d; // difficulty, lower case letters only
  final String s; // subject text
  final int len; // question length in characters
  final String st; // correct / wrong / skip
  final int t; // your seconds
  CmpItem(this.qn, this.d, this.s, this.len, this.st, this.t);
}

class CmpRow {
  final int pc; // % who got it right
  final String topR; // correct / wrong / skip
  final int topT, youT, avgT;
  final String youR;
  final String tip;
  CmpRow(this.pc, this.topR, this.topT, this.youT, this.youR, this.avgT, this.tip);
}

class Compare {
  final String key;
  final Map<String, dynamic> qs;
  final Map<String, dynamic>? lbTop;
  final List<double> mk;
  final List<CmpItem> items;
  late final Map<String, String> _top = _buildTopMap();

  Compare(this.key, this.qs, this.lbTop, this.mk, this.items);

  static Future<Compare?> load(Paper p, Progress pr) async {
    final key = lbBase(p.rules.mockId);
    try {
      final db = FirebaseFirestore.instance;
      final res = await Future.wait([
        db.collection('qstats').doc(key).get(),
        db.collection('leaderboards').doc(key).collection('scores').orderBy('marks', descending: true).limit(1).get().then((s) => s.docs.isEmpty ? null : s.docs.first.data(), onError: (_) => null),
      ]);
      final qsDoc = res[0] as DocumentSnapshot<Map<String, dynamic>>;
      final items = <CmpItem>[];
      for (var i = 0; i < p.questions.length; i++) {
        final q = p.questions[i];
        final a = pr.answers[i];
        final st = a == null ? 'skip' : (a == q.correct ? 'correct' : 'wrong');
        final plain = q.text.replaceAll(RegExp(r'\[IMG\].*?\[/IMG\]'), '').replaceAll(RegExp(r'<[^>]*>|\[BR\]|\*\*|\|'), ' ').replaceAll(RegExp(r'\s+'), ' ').trim();
        items.add(CmpItem(
          '${q.qNumOr(i + 1)}',
          q.difficulty.trim().toLowerCase().replaceAll(RegExp(r'[^a-z]'), ''),
          (q.subjectRaw.isNotEmpty ? q.subjectRaw : q.chapter).replaceAll(RegExp(r'[^A-Za-z .]'), '').characters40x(),
          plain.length,
          st,
          ((pr.qMs[i] ?? 0) / 1000).round(),
        ));
      }
      return Compare(key, qsDoc.data() ?? {}, res[1] as Map<String, dynamic>?, [p.rules.pos, p.rules.negBase], items);
    } catch (_) {
      return null;
    }
  }

  // ---------------------------------------------------------------- website formulas
  double seed(String q) {
    var x = 2166136261;
    final str = '$key|$q';
    for (final c in str.codeUnits) {
      x ^= c;
      x = (x * 16777619) & 0xFFFFFFFF;
    }
    x ^= x >> 13;
    x = (x * 0x5bd1e995) & 0xFFFFFFFF;
    x ^= x >> 15;
    return (x & 0xFFFFFFFF) % 10007 / 10007;
  }

  int _estimate(String q, String d) {
    final base = d == 'easy' ? 76 : d == 'hard' ? 34 : d == 'moderate' ? 56 : (42 + (seed(q) * 38).round());
    final jit = ((seed('${q}j') - 0.5) * 14).round();
    return (base + jit).clamp(12, 94);
  }

  static String kindOf(String s) {
    s = s.toLowerCase();
    if (RegExp(r'quant|math|arith|mensur|geomet|algebra|trigon|percent|profit|interest|ratio|average|time|speed|data').hasMatch(s)) return 'quant';
    if (RegExp(r'reason|intellig|logic|analog|classif|series|coding|verbal').hasMatch(s)) return 'reasoning';
    if (RegExp(r'english|compreh|grammar|vocab').hasMatch(s)) return 'english';
    if (RegExp(r'comput').hasMatch(s)) return 'computer';
    if (RegExp(r'gk|general aware|gen\. aware|awareness|history|polity|geograph|econom|science|current|static').hasMatch(s)) return 'gk';
    return '';
  }

  static const _baseT = {'gk': 18, 'english': 30, 'reasoning': 40, 'quant': 65, 'computer': 20, '': 42};
  static const _topCap = {'quant': 20, 'reasoning': 18, 'english': 22, 'gk': 14, 'computer': 14, '': 18};

  int _estTime(CmpItem it) {
    final m = it.d == 'easy' ? 0.75 : it.d == 'hard' ? 1.35 : 1.0;
    final lf = 1 + ((it.len - 80) / 600).clamp(0, 1) * 0.35;
    final v = _baseT[kindOf(it.s)]! * m * lf * (0.68 + seed('${it.qn}t') * 0.5 + (seed('${it.qn}u') - 0.5) * 0.15);
    return v.round() < 8 ? 8 : v.round();
  }

  Map? _q(String qn) {
    final m = qs['q'];
    return m is Map ? m['q$qn'] as Map? : null;
  }

  int pcOf(CmpItem it) {
    final s = _q(it.qn);
    final a = s == null ? 0 : ((s['a'] as num?) ?? 0).toDouble();
    final eP = _estimate(it.qn, it.d);
    final rP = a > 0 ? ((s!['c'] as num?) ?? 0) * 100 / a : 0.0;
    return a >= _minN ? rP.round() : ((eP * _k + rP * a) / (_k + a)).round();
  }

  int _topTime(CmpItem it) {
    final cap = _topCap[kindOf(it.s)]!;
    final base = it.d == 'easy' ? 0.3 : it.d == 'hard' ? 0.68 : 0.48;
    final lf = ((it.len - 80) / 600).clamp(0, 1) * 0.18;
    var g = base + lf + (seed('${it.qn}q') - 0.5) * 0.55 + (seed('${it.qn}r') - 0.5) * 0.2;
    g = g.clamp(0, 1).toDouble();
    final f = 0.3 + 0.7 * g;
    return (cap * f).round().clamp(3, cap);
  }

  Map<String, dynamic>? _realTopper() {
    final top = qs['top'];
    final q = top is Map ? top['q'] : null;
    if (q is! Map || q.isEmpty) return null;
    final c = q.values.where((v) => '$v'.startsWith('c')).length;
    return c / q.length >= 0.4 ? Map<String, dynamic>.from(q) : null;
  }

  Map<String, int> _topCounts(double m, int n) {
    final p = mk[0], q = mk[1] <= 0 ? 0.25 : mk[1];
    Map<String, int>? best;
    for (var c = n; c >= 0; c--) {
      final w = (p * c - m) / q;
      if (w < -1e-6 || (w - w.round()).abs() > 1e-6) continue;
      final wi = w.round();
      if (c + wi > n) continue;
      best ??= {'c': c, 'w': wi, 'k': n - c - wi};
      if (wi <= (2 > 0.15 * (c + wi) ? 2 : 0.15 * (c + wi))) return {'c': c, 'w': wi, 'k': n - c - wi};
    }
    if (best != null) return best;
    final c2 = (m / p).round().clamp(0, n);
    return {'c': c2, 'w': 0, 'k': n - c2};
  }

  void _planGroup(List<CmpItem> its, double m, Map<String, String> out) {
    final cnt = _topCounts(m, its.length);
    final ord = [for (final it in its) (it, pcOf(it) + (seed('${it.qn}h') - 0.5) * 20)]..sort((a, b) => a.$2.compareTo(b.$2));
    for (var i = 0; i < ord.length; i++) {
      final it = ord[i].$1;
      final r = i < cnt['k']! ? 'k' : (i < cnt['k']! + cnt['w']! ? 'w' : 'c');
      out[it.qn] = '$r${r == 'k' ? 0 : _topTime(it)}';
    }
  }

  Map<String, String> _buildTopMap() {
    var m = <String, String>{};
    final rt = _realTopper();
    final lbM = lbTop == null ? null : (lbTop!['marks'] as num?)?.toDouble();
    final topM = ((qs['top'] is Map ? (qs['top'] as Map)['m'] : null) as num? ?? 0).toDouble();
    if (rt != null && (lbM == null || topM >= lbM - 0.01)) {
      for (final it in items) {
        final v = rt['q${it.qn}'];
        if (v != null) m[it.qn] = '$v';
      }
      if (m.length >= items.length * 0.9) return m;
      m = {};
    }
    if (lbM == null || !(lbM > 0)) {
      for (final it in items) {
        final pc = pcOf(it), pOk = (0.5 + pc / 100 * 0.55).clamp(0, 0.97), u = seed('${it.qn}p');
        final r = u < pOk ? 'c' : (u < pOk + (1 - pOk) * 0.6 ? 'w' : 'k');
        m[it.qn] = '$r${r == 'k' ? 0 : _topTime(it)}';
      }
      return m;
    }
    final sm = lbTop!['subjectMarks'] is Map ? Map<String, dynamic>.from(lbTop!['subjectMarks']) : <String, dynamic>{};
    final byKind = <String, List<CmpItem>>{};
    for (final it in items) {
      final k = kindOf(it.s);
      byKind.putIfAbsent(k.isEmpty ? '_' : k, () => []).add(it);
    }
    final plan = <(List<CmpItem>, double)>[];
    var sum = 0.0;
    var ok = sm.length > 1;
    sm.forEach((k, v) {
      final kk = kindOf(k), val = (v is num ? v : num.tryParse('$v') ?? 0).toDouble();
      sum += val;
      if (kk.isEmpty || byKind[kk] == null) {
        ok = false;
      } else {
        plan.add((byKind[kk]!, val));
      }
    });
    if (ok && (sum - lbM).abs() < 0.6 && plan.fold<int>(0, (a, p) => a + p.$1.length) == items.length) {
      for (final p in plan) {
        _planGroup(p.$1, p.$2, m);
      }
    } else {
      _planGroup(items, lbM, m);
    }
    return m;
  }

  // ---------------------------------------------------------------- results
  CmpRow row(int i) {
    final it = items[i];
    final pc = pcOf(it);
    final s = _q(it.qn);
    final tn = s == null ? 0.0 : ((s['tn'] as num?) ?? 0).toDouble();
    final tsum = s == null ? 0.0 : ((s['ts'] as num?) ?? 0).toDouble();
    final eT = _estTime(it);
    final avg = tn >= _minN ? tsum / tn : (eT * _k + tsum) / (_k + tn);
    final tp = _top[it.qn] ?? 'k0';
    final tr = const {'c': 'correct', 'w': 'wrong', 'k': 'skip'}[tp.substring(0, 1)] ?? 'skip';
    final tt = int.tryParse(tp.substring(1)) ?? 0;
    final ty = it.t, ta = avg.round();
    String tip;
    if (it.st == 'correct') {
      tip = ty > 0 && tt > 0 && ty <= tt
          ? '⚡ Faster than the topper on this one!'
          : ty > 0 && ty <= ta
              ? '👍 Right, and quicker than the average student'
              : ty > 0
                  ? '⏱ Right, but ${fmtT(ty - ta)} slower than average — practise this type for speed'
                  : '✅ Well done';
    } else if (it.st == 'wrong') {
      tip = pc >= 60
          ? '📌 $pc% of students got this right — revise this topic'
          : pc < 35
              ? '🧗 A tough one — only $pc% got it right'
              : '✍️ $pc% got it right — go through the solution below';
    } else {
      tip = pc >= 60
          ? '🎯 An easy mark missed — $pc% got it right'
          : pc < 35
              ? '🧗 A tough one — only $pc% got it right, skipping was sensible'
              : '💡 $pc% got it right — worth attempting next time';
    }
    return CmpRow(pc, tr, tt, ty, it.st, ta, tip);
  }

  /// Topper's whole-paper line: marks, correct, wrong, skipped.
  (double, int, int, int) topperTotals() {
    var c = 0, w = 0, k = 0;
    for (final it in items) {
      final r = (_top[it.qn] ?? 'k0').substring(0, 1);
      if (r == 'c') {
        c++;
      } else if (r == 'w') {
        w++;
      } else {
        k++;
      }
    }
    return ((((c * mk[0] - w * mk[1]) * 10).round() / 10), c, w, k);
  }

  int get students => ((qs['n'] as num?) ?? 0).toInt();
}

String fmtT(int s) => s <= 0 ? '—' : (s < 60 ? '$s s' : '${s ~/ 60}m ${s % 60}s');

class CompareStrip extends StatelessWidget {
  final CmpRow r;
  const CompareStrip(this.r, {super.key});

  static const _c = {'correct': Color(0xFF22C55E), 'wrong': Color(0xFFEF4444), 'skip': Color(0xFFCBD5E1), 'avg': Color(0xFF60A5FA)};
  static const _ic = {'correct': '✓', 'wrong': '✕', 'skip': '–'};

  @override
  Widget build(BuildContext context) {
    final mx = [r.topT, r.youT, r.avgT, 1].reduce((a, b) => a > b ? a : b);
    Widget bar(String who, String ico, String res, int t, String? mark) => Padding(
          padding: const EdgeInsets.symmetric(vertical: 3),
          child: Row(children: [
            SizedBox(width: 92, child: Text('$ico $who', style: const TextStyle(fontSize: 13.5, fontWeight: FontWeight.w700))),
            Expanded(
              child: Container(
                height: 10,
                decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(6)),
                alignment: Alignment.centerLeft,
                child: FractionallySizedBox(
                  widthFactor: t > 0 ? (t / mx).clamp(0.04, 1.0) : 0,
                  child: Container(decoration: BoxDecoration(color: _c[res], borderRadius: BorderRadius.circular(6))),
                ),
              ),
            ),
            SizedBox(width: 58, child: Text(fmtT(t), textAlign: TextAlign.right, style: const TextStyle(fontSize: 12.5, color: Color(0xFF475569)))),
            SizedBox(
              width: 22,
              child: mark == null ? null : Text(_ic[mark]!, textAlign: TextAlign.right, style: TextStyle(fontWeight: FontWeight.w900, color: mark == 'skip' ? const Color(0xFF94A3B8) : _c[mark])),
            ),
          ]),
        );
    return Container(
      margin: const EdgeInsets.only(top: 8, bottom: 2),
      padding: const EdgeInsets.fromLTRB(10, 8, 10, 8),
      decoration: BoxDecoration(color: const Color(0xFFF8FAFC), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFFE2E8F0))),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          const Expanded(child: Text('How you compare', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w800))),
          Text('${r.pc}%', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w900, color: Color(0xFF2563EB))),
          const Text(' got it right', style: TextStyle(fontSize: 12.5, color: Color(0xFF64748B))),
        ]),
        const SizedBox(height: 4),
        bar('Topper', '👑', r.topR, r.topT, r.topR),
        bar('You', '🙋', r.youR, r.youT, r.youR),
        bar('Average', '👥', 'avg', r.avgT, null),
        const SizedBox(height: 4),
        Text(r.tip, style: const TextStyle(fontSize: 13, color: Color(0xFF334155), fontWeight: FontWeight.w600)),
      ]),
    );
  }
}

extension on String {
  String characters40x() => length <= 40 ? this : substring(0, 40);
}
