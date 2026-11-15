import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';

import '../data.dart';

class LbRow {
  final String uid, name;
  final double marks, maxMarks;
  final int timeUsed;
  int rank = 0;
  LbRow(this.uid, this.name, this.marks, this.maxMarks, this.timeUsed);

  factory LbRow.from(String id, Map<String, dynamic> d) => LbRow(
        '${d['uid'] ?? id}',
        '${d['name'] ?? 'Student'}'.trim().isEmpty ? 'Student' : '${d['name']}'.trim(),
        (d['marks'] as num? ?? 0).toDouble(),
        (d['maxMarks'] as num? ?? 0).toDouble(),
        (d['timeUsed'] as num? ?? 0).toInt(),
      );
}

class LeaderboardScreen extends StatefulWidget {
  final Exam exam;
  final String base; // mock id without the language
  final String title;
  final String uid;
  const LeaderboardScreen({super.key, required this.exam, required this.base, required this.title, required this.uid});

  @override
  State<LeaderboardScreen> createState() => _LeaderboardScreenState();
}

class _LeaderboardScreenState extends State<LeaderboardScreen> {
  List<LbRow>? _rows;
  LbRow? _me;
  int? _total;
  bool _failed = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _failed = false);
    try {
      final col = FirebaseFirestore.instance.collection('leaderboards').doc(widget.base).collection('scores');
      final snap = await col.orderBy('marks', descending: true).limit(100).get();
      final rows = [for (final d in snap.docs) LbRow.from(d.id, d.data())];
      for (var i = 0; i < rows.length; i++) {
        rows[i].rank = (i > 0 && rows[i].marks == rows[i - 1].marks) ? rows[i - 1].rank : i + 1;
      }
      LbRow? me;
      for (final r in rows) {
        if (r.uid == widget.uid) me = r;
      }
      if (me == null) {
        final d = await col.doc(widget.uid).get();
        if (d.exists) {
          me = LbRow.from(d.id, d.data()!);
          final above = await col.where('marks', isGreaterThan: me.marks).count().get();
          me.rank = (above.count ?? 0) + 1;
        }
      }
      int? total;
      try {
        total = (await col.count().get()).count;
      } catch (_) {}
      if (mounted) {
        setState(() {
          _rows = rows;
          _me = me;
          _total = total ?? rows.length;
        });
      }
    } catch (_) {
      if (mounted) setState(() => _failed = true);
    }
  }

  String _n(double v) => v == v.roundToDouble() ? '${v.round()}' : v.toStringAsFixed(2).replaceFirst(RegExp(r'0+$'), '');
  String _t(int s) => s <= 0 ? '' : '${s ~/ 60}m ${s % 60}s';

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final rows = _rows;
    return examTheme(
      context,
      exam,
      Scaffold(
        backgroundColor: Color.lerp(Colors.white, exam.c2, 0.10),
        appBar: AppBar(title: Text('Leaderboard', style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: _failed
            ? Center(
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  const Text('Could not load the leaderboard.'),
                  TextButton(onPressed: _load, child: const Text('Try again')),
                ]),
              )
            : rows == null
                ? const Center(child: CircularProgressIndicator())
                : RefreshIndicator(
                    onRefresh: _load,
                    child: ListView(
                      padding: EdgeInsets.fromLTRB(12, 10, 12, 16 + MediaQuery.of(context).padding.bottom),
                      children: [
                        Container(
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(18),
                            gradient: LinearGradient(colors: [exam.c1, exam.c2], begin: Alignment.topLeft, end: Alignment.bottomRight),
                          ),
                          child: Row(children: [
                            Expanded(
                              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                                Text(widget.title, style: const TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.w800)),
                                const SizedBox(height: 4),
                                Text('${_total ?? rows.length} students took this mock', style: const TextStyle(color: Colors.white, fontSize: 14)),
                                if (_me != null)
                                  Text('Your best: ${_n(_me!.marks)}${_me!.maxMarks > 0 ? ' / ${_n(_me!.maxMarks)}' : ''}',
                                      style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.w700)),
                              ]),
                            ),
                            if (_me != null)
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14)),
                                child: Column(children: [
                                  Text('#${_me!.rank}', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900, color: exam.c1)),
                                  const Text('Your rank', style: TextStyle(fontSize: 12, color: Color(0xFF64748B))),
                                ]),
                              ),
                          ]),
                        ),
                        const SizedBox(height: 12),
                        if (rows.isEmpty) const Padding(padding: EdgeInsets.all(30), child: Center(child: Text('No scores yet. Be the first!'))),
                        if (rows.length >= 3) _podium(rows),
                        for (final r in rows.length >= 3 ? rows.skip(3) : rows) _row(r),
                        if (_me != null && !rows.any((r) => r.uid == widget.uid)) ...[
                          const Padding(padding: EdgeInsets.symmetric(vertical: 4), child: Center(child: Text('⋯', style: TextStyle(fontSize: 20)))),
                          _row(_me!),
                        ],
                      ],
                    ),
                  ),
      ),
    );
  }

  Widget _podium(List<LbRow> rows) {
    final exam = widget.exam;
    Widget spot(LbRow r, double h, String medal, Color c) => Expanded(
          child: Column(children: [
            Text(medal, style: const TextStyle(fontSize: 28)),
            CircleAvatar(
              radius: 22,
              backgroundColor: c,
              child: Text(r.name[0].toUpperCase(), style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w800)),
            ),
            const SizedBox(height: 4),
            Text(r.uid == widget.uid ? 'You' : r.name, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 14)),
            Text(_n(r.marks), style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16, color: exam.c1)),
            const SizedBox(height: 4),
            Container(
              height: h,
              decoration: BoxDecoration(
                color: Color.lerp(Colors.white, c, 0.35),
                borderRadius: const BorderRadius.vertical(top: Radius.circular(12)),
              ),
              alignment: Alignment.center,
              child: Text('${r.rank}', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: Color.lerp(c, Colors.black, 0.3))),
            ),
          ]),
        );
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.fromLTRB(10, 10, 10, 0),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16)),
      child: Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
        spot(rows[1], 56, '🥈', const Color(0xFF94A3B8)),
        const SizedBox(width: 8),
        spot(rows[0], 80, '🥇', const Color(0xFFF59E0B)),
        const SizedBox(width: 8),
        spot(rows[2], 40, '🥉', const Color(0xFFB45309)),
      ]),
    );
  }

  Widget _row(LbRow r) {
    final exam = widget.exam;
    final me = r.uid == widget.uid;
    return Container(
      margin: const EdgeInsets.only(bottom: 6),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: me ? Color.lerp(Colors.white, exam.c2, 0.25) : Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: me ? Border.all(color: exam.c1, width: 1.5) : null,
      ),
      child: Row(children: [
        SizedBox(width: 40, child: Text('#${r.rank}', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 15, color: exam.c1))),
        CircleAvatar(
          radius: 16,
          backgroundColor: Color.lerp(Colors.white, exam.c2, 0.4),
          child: Text(r.name[0].toUpperCase(), style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink)),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(me ? '${r.name} (You)' : r.name, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 15)),
            if (r.timeUsed > 0) Text(_t(r.timeUsed), style: const TextStyle(fontSize: 12.5, color: Color(0xFF64748B))),
          ]),
        ),
        Text(_n(r.marks), style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16, color: exam.ink)),
        if (r.maxMarks > 0) Text(' / ${_n(r.maxMarks)}', style: const TextStyle(fontSize: 12.5, color: Color(0xFF64748B))),
      ]),
    );
  }
}
