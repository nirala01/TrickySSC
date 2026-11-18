import 'package:flutter/material.dart';

import '../data.dart';
import '../ui/icons3d.dart';
import '../ui/soft.dart';

/// TSSC-RRB-GROUP-V1: railway exams (id "rrb-…") sit behind one "RRB" card once there are two or more;
/// tapping it opens a page listing them. A new rrb-* exam in catalog.json joins the group by itself.
bool _isRrb(Exam e) => e.id.startsWith('rrb-');

class ChooseExamScreen extends StatelessWidget {
  final void Function(Exam) onPick;
  const ChooseExamScreen({super.key, required this.onPick});

  @override
  Widget build(BuildContext context) {
    final rrb = exams.where(_isRrb).toList();
    final group = rrb.length >= 2;
    final cards = <Widget>[];
    var placed = false;
    for (final e in exams) {
      if (group && _isRrb(e)) {
        if (placed) continue;
        placed = true;
        cards.add(_ExamCard(
          name: 'RRB',
          sub: 'Railway · ${rrb.map((x) => x.name.replaceFirst('RRB ', '')).join(', ')}',
          icon3d: e.icon3d,
          c1: e.c1,
          onTap: () => Navigator.of(context).push(MaterialPageRoute<void>(
              builder: (c) => _GroupScreen(
                  title: 'RRB exams',
                  list: rrb,
                  onPick: (x) {
                    Navigator.of(c).pop();
                    onPick(x);
                  }))),
        ));
      } else {
        cards.add(_ExamCard(name: e.name, sub: e.sub, icon3d: e.icon3d, c1: e.c1, onTap: () => onPick(e)));
      }
    }
    return Scaffold(
      body: Container(
        decoration: softBg,
        child: SafeArea(
          child: ListView(
            padding: const EdgeInsets.fromLTRB(20, 18, 20, 20),
            children: [
              const _HeroCard(),
              const SizedBox(height: 18),
              for (final w in cards) Padding(padding: const EdgeInsets.only(bottom: 12), child: w),
            ],
          ),
        ),
      ),
    );
  }
}

class _GroupScreen extends StatelessWidget {
  final String title;
  final List<Exam> list;
  final void Function(Exam) onPick;
  const _GroupScreen({required this.title, required this.list, required this.onPick});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: softBg,
        child: SafeArea(
          child: ListView(
            padding: const EdgeInsets.fromLTRB(20, 10, 20, 20),
            children: [
              Row(children: [
                IconButton(onPressed: () => Navigator.of(context).pop(), icon: const Icon(Icons.arrow_back)),
                const SizedBox(width: 4),
                Text(title, style: baloo(26)),
              ]),
              const Padding(
                padding: EdgeInsets.fromLTRB(8, 0, 8, 14),
                child: Text('Choose your course', style: TextStyle(color: softMuted, fontSize: 15, fontWeight: FontWeight.w600)),
              ),
              for (final e in list)
                Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: _ExamCard(name: e.name, sub: e.sub, icon3d: e.icon3d, c1: e.c1, onTap: () => onPick(e)),
                ),
            ],
          ),
        ),
      ),
    );
  }
}

class _HeroCard extends StatelessWidget {
  const _HeroCard();

  @override
  Widget build(BuildContext context) {
    Widget bubble(double size, double alpha) => Container(width: size, height: size, decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.white.withValues(alpha: alpha)));
    return Container(
      clipBehavior: Clip.antiAlias,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(26),
        gradient: const LinearGradient(colors: [Color(0xFF1E1B4B), Color(0xFF4338CA), Color(0xFF6366F1)], begin: Alignment.topLeft, end: Alignment.bottomRight),
        boxShadow: [BoxShadow(color: const Color(0xFF4338CA).withValues(alpha: .35), blurRadius: 26, offset: const Offset(0, 12))],
      ),
      child: Stack(children: [
        Positioned(right: -34, top: -40, child: bubble(140, .08)),
        Positioned(right: 36, bottom: -50, child: bubble(110, .07)),
        Positioned(left: -30, bottom: -36, child: bubble(90, .05)),
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 20, 20, 22),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              Container(
                padding: const EdgeInsets.all(3),
                decoration: BoxDecoration(shape: BoxShape.circle, color: Colors.white, boxShadow: [BoxShadow(color: const Color(0xFFFF6B00).withValues(alpha: .45), blurRadius: 14, offset: const Offset(0, 5))]),
                child: Image.asset('assets/logo.png', width: 42, height: 42),
              ),
              const SizedBox(width: 10),
              Text.rich(TextSpan(children: [TextSpan(text: 'Tricky', style: baloo(26, color: Colors.white)), TextSpan(text: 'SSC', style: baloo(26, color: const Color(0xFFFFA24D)))])),
            ]),
            const SizedBox(height: 16),
            Text('Choose your exam', style: baloo(32, color: Colors.white)),
            const SizedBox(height: 4),
            const Text('You can change this any time.', style: TextStyle(color: Color(0xE6FFFFFF), fontSize: 15, fontWeight: FontWeight.w600)),
          ]),
        ),
      ]),
    );
  }
}

class _ExamCard extends StatelessWidget {
  final String name, sub, icon3d;
  final Color c1;
  final VoidCallback onTap;
  const _ExamCard({required this.name, required this.sub, required this.icon3d, required this.c1, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: Ink(
        decoration: softCard(),
        child: InkWell(
          borderRadius: BorderRadius.circular(22),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
            child: Row(children: [
              Container(
                width: 64,
                height: 64,
                alignment: Alignment.center,
                decoration: softWell(radius: 18),
                child: Icon3D(icon3d, size: 46),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(name, style: baloo(21)),
                  const SizedBox(height: 2),
                  Text(sub, maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(color: softMuted, fontSize: 14.5, fontWeight: FontWeight.w600)),
                ]),
              ),
              Icon(Icons.chevron_right, color: c1, size: 26),
            ]),
          ),
        ),
      ),
    );
  }
}
