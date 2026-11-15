import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../data.dart';
import '../test/engine.dart';
import '../test/leaderboard.dart';
import '../test/result_screen.dart';

class DashboardTab extends StatefulWidget {
  final User user;
  final Exam exam;
  final int version; // bumped by the shell after a test, to reload
  final VoidCallback onMocks;
  const DashboardTab({super.key, required this.user, required this.exam, required this.version, required this.onMocks});

  @override
  State<DashboardTab> createState() => _DashboardTabState();
}

class _SubAgg {
  int c = 0, w = 0, k = 0;
}

class _DashboardTabState extends State<DashboardTab> {
  List<Map<String, dynamic>>? _all;
  bool _failed = false;

  @override
  void initState() {
    super.initState();
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
      if (mounted) setState(() => _all = a);
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  String _n(num v) => v == v.roundToDouble() ? '${v.round()}' : v.toStringAsFixed(1);
  double _d(dynamic v) => v is num ? v.toDouble() : double.tryParse('$v') ?? 0;

  String _date(int ms) {
    if (ms == 0) return '';
    final d = DateTime.fromMillisecondsSinceEpoch(ms);
    const m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    final h = d.hour % 12 == 0 ? 12 : d.hour % 12;
    return '${d.day} ${m[d.month - 1]} · $h:${d.minute.toString().padLeft(2, '0')} ${d.hour < 12 ? 'am' : 'pm'}';
  }

  String _id(Map<String, dynamic> a) => '${a['mockId'] ?? ''}'.isNotEmpty ? '${a['mockId']}' : '${a['paperId'] ?? ''}';

  String _title(Map<String, dynamic> a) {
    final id = '${a['mockId'] ?? ''}';
    final m = RegExp(r'_(tier\d|cbt\d)_mock(\d+)_(en|hi)$').firstMatch(id);
    if (m != null) {
      final t2 = m.group(1) == 'tier2' ? 'Tier 2 ' : '';
      return '${widget.exam.name} ${t2}Mock ${m.group(2)}${m.group(3) == 'hi' ? ' · हिंदी' : ''}';
    }
    final n = '${a['examName'] ?? ''}'.trim();
    final hi = _id(a).endsWith('_hi') ? ' · हिंदी' : '';
    return n.isEmpty ? 'Test' : '$n$hi';
  }

  bool _canOpen(Map<String, dynamic> a) {
    final id = _id(a);
    final ok = RegExp(r'_(tier1|cbt1)_mock\d+_(en|hi)$').hasMatch(id) || RegExp(r'^[a-z-]+_\d{4}_tier1_.*_(en|hi)$').hasMatch(id);
    return ok && (a['answers'] is List);
  }

  void _actions(Map<String, dynamic> a) {
    final exam = widget.exam;
    final id = _id(a);
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (c) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 10),
          child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            Text(_title(a), style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: exam.ink)),
            Text('${_n(_d(a['marks']))} marks · ${_n(_d(a['percentage']))}% · ${_date(attemptMs(a))}', style: const TextStyle(color: Color(0xFF64748B))),
            const SizedBox(height: 14),
            if (_canOpen(a))
              FilledButton.icon(
                onPressed: () {
                  Navigator.pop(c);
                  openAttemptSolutions(context, exam, a);
                },
                style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                icon: const Icon(Icons.menu_book),
                label: const Text('View solutions', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
              ),
            if (id.isNotEmpty) ...[
              const SizedBox(height: 8),
              FilledButton.tonalIcon(
                onPressed: () {
                  Navigator.pop(c);
                  Navigator.of(context).push(MaterialPageRoute(
                    builder: (_) => LeaderboardScreen(exam: exam, base: lbBase(id), title: _title(a).replaceAll(' · हिंदी', ''), uid: widget.user.uid),
                  ));
                },
                style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                icon: const Icon(Icons.emoji_events_outlined),
                label: const Text('Leaderboard', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
              ),
            ],
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
    final mine = all.where((a) => a['exam'] == exam.id).toList();

    if (mine.isEmpty) {
      return RefreshIndicator(
        onRefresh: _load,
        child: ListView(padding: const EdgeInsets.all(28), children: [
          const SizedBox(height: 60),
          Icon(Icons.insights, size: 56, color: exam.c1),
          const SizedBox(height: 10),
          Text('No ${exam.name} tests yet', textAlign: TextAlign.center, style: TextStyle(fontSize: 19, fontWeight: FontWeight.w800, color: exam.ink)),
          const SizedBox(height: 6),
          const Text('Take a mock and your scores, ranks and weak areas will show here.', textAlign: TextAlign.center, style: TextStyle(fontSize: 15, color: Color(0xFF64748B))),
          const SizedBox(height: 16),
          Center(child: FilledButton(onPressed: widget.onMocks, style: FilledButton.styleFrom(backgroundColor: exam.c1), child: const Text('Go to mocks'))),
        ]),
      );
    }

    // numbers
    var sumPct = 0.0, best = double.negativeInfinity, timeSec = 0, c = 0, w = 0;
    final subs = <String, _SubAgg>{};
    for (final a in mine) {
      sumPct += _d(a['percentage']);
      final mk = _d(a['marks']);
      if (mk > best) best = mk;
      timeSec += _d(a['timeUsed']).toInt();
      c += _d(a['correct']).toInt();
      w += _d(a['wrong']).toInt();
      final ss = a['subjectStats'];
      if (ss is Map) {
        ss.forEach((k, v) {
          if (v is! Map) return;
          final g = subs.putIfAbsent('$k', () => _SubAgg());
          g.c += _d(v['correct']).toInt();
          g.w += _d(v['wrong']).toInt();
          g.k += _d(v['skip']).toInt();
        });
      }
    }
    final avg = sumPct / mine.length;
    final acc = c + w == 0 ? 0 : (c * 100 / (c + w)).round();
    final trend = mine.take(10).toList().reversed.toList();
    final subList = subs.entries.where((e) => e.value.c + e.value.w > 0).toList()
      ..sort((a, b) => (a.value.c / (a.value.c + a.value.w)).compareTo(b.value.c / (b.value.c + b.value.w)));
    final hrs = timeSec ~/ 3600, mins = (timeSec % 3600) ~/ 60;

    Widget card({required Widget child, EdgeInsets pad = const EdgeInsets.all(14)}) => Container(
          margin: const EdgeInsets.only(bottom: 10),
          padding: pad,
          decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16)),
          child: child,
        );
    Widget head(String t) => Padding(padding: const EdgeInsets.only(bottom: 10), child: Text(t, style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: exam.ink)));
    Widget mini(String v, String l) => Expanded(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 10),
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(v, style: TextStyle(fontSize: 21, fontWeight: FontWeight.w800, color: exam.c1, height: 1.1)),
              Text(l, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 13, color: Color(0xFF475569), fontWeight: FontWeight.w600)),
            ]),
          ),
        );

    return RefreshIndicator(
      onRefresh: _load,
      child: ListView(padding: const EdgeInsets.fromLTRB(12, 12, 12, 16), children: [
        Container(
          margin: const EdgeInsets.only(bottom: 10),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(18),
            gradient: LinearGradient(colors: [exam.c1, exam.c2], begin: Alignment.topLeft, end: Alignment.bottomRight),
          ),
          child: Row(children: [
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('My ${exam.name} progress', style: const TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.w600)),
                const SizedBox(height: 2),
                Text('${mine.length} test${mine.length == 1 ? '' : 's'} taken', style: const TextStyle(color: Colors.white, fontSize: 26, fontWeight: FontWeight.w900)),
                Text('${all.length} across all exams', style: const TextStyle(color: Colors.white, fontSize: 13.5)),
              ]),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14)),
              child: Column(children: [
                Text(_n(best), style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900, color: exam.c1)),
                const Text('Best marks', style: TextStyle(fontSize: 12, color: Color(0xFF64748B))),
              ]),
            ),
          ]),
        ),
        Row(children: [
          mini('${_n(avg)}%', 'Avg score'),
          const SizedBox(width: 8),
          mini('$acc%', 'Accuracy'),
          const SizedBox(width: 8),
          mini(hrs > 0 ? '${hrs}h ${mins}m' : '${mins}m', 'Time spent'),
        ]),
        const SizedBox(height: 10),
        if (trend.length >= 2)
          card(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              head('Score trend · last ${trend.length}'),
              SizedBox(
                height: 130,
                child: Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
                  for (final a in trend)
                    Expanded(
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 3),
                        child: Column(mainAxisAlignment: MainAxisAlignment.end, children: [
                          Text(_n(_d(a['percentage']).clamp(0, 100)), style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: exam.ink)),
                          const SizedBox(height: 2),
                          Container(
                            height: 6 + 100 * (_d(a['percentage']).clamp(0, 100) / 100),
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(6),
                              gradient: LinearGradient(colors: [exam.c2, exam.c1], begin: Alignment.topCenter, end: Alignment.bottomCenter),
                            ),
                          ),
                        ]),
                      ),
                    ),
                ]),
              ),
              const SizedBox(height: 4),
              const Text('Score % of each test, oldest to newest', style: TextStyle(fontSize: 12, color: Color(0xFF64748B))),
            ]),
          ),
        if (subList.isNotEmpty)
          card(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              head('Subject accuracy'),
              for (final e in subList) ...[
                Builder(builder: (_) {
                  final g = e.value;
                  final p = g.c / (g.c + g.w);
                  final col = p >= 0.75 ? const Color(0xFF16A34A) : (p >= 0.5 ? const Color(0xFFD97706) : const Color(0xFFDC2626));
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 10),
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Row(children: [
                        Expanded(child: Text(e.key, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700))),
                        Text('${(p * 100).round()}%', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: col)),
                        Text('  ${g.c}✓ ${g.w}✕', style: const TextStyle(fontSize: 12.5, color: Color(0xFF64748B))),
                      ]),
                      const SizedBox(height: 4),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(6),
                        child: LinearProgressIndicator(value: p, minHeight: 8, color: col, backgroundColor: const Color(0xFFF1F5F9)),
                      ),
                    ]),
                  );
                }),
              ],
              if (subList.length > 1)
                Text('Weakest: ${subList.first.key} — practise it first.', style: const TextStyle(fontSize: 13, color: Color(0xFF64748B))),
            ]),
          ),
        card(
          pad: const EdgeInsets.fromLTRB(14, 14, 14, 4),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            head('Recent tests'),
            for (final a in mine.take(30))
              InkWell(
                onTap: () => _actions(a),
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 9),
                  child: Row(children: [
                    Container(
                      width: 46,
                      height: 46,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(color: Color.lerp(Colors.white, exam.c2, 0.25), borderRadius: BorderRadius.circular(12)),
                      child: Text('${_n(_d(a['percentage']))}%', style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w800, color: exam.ink)),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text(_title(a), maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 15.5, fontWeight: FontWeight.w700)),
                        Text('${_n(_d(a['marks']))} marks · ${_d(a['correct']).toInt()}✓ ${_d(a['wrong']).toInt()}✕ · ${_date(attemptMs(a))}',
                            maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 13, color: Color(0xFF64748B))),
                      ]),
                    ),
                    const Icon(Icons.chevron_right, color: Color(0xFF94A3B8)),
                  ]),
                ),
              ),
          ]),
        ),
      ]),
    );
  }
}
