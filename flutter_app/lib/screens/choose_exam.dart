import 'package:flutter/material.dart';

import '../data.dart';
import '../ui/icons3d.dart';
import '../ui/soft.dart';

class ChooseExamScreen extends StatelessWidget {
  final void Function(Exam) onPick;
  const ChooseExamScreen({super.key, required this.onPick});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: softBg,
        child: SafeArea(
          child: ListView(
            padding: const EdgeInsets.fromLTRB(20, 18, 20, 20),
            children: [
              const _HeroCard(),
              const SizedBox(height: 18),
              for (final e in exams)
                Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: _ExamCard(exam: e, onTap: () => onPick(e)),
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
  final Exam exam;
  final VoidCallback onTap;
  const _ExamCard({required this.exam, required this.onTap});

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
                child: Icon3D(exam.icon3d, size: 46),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(exam.name, style: baloo(21)),
                  const SizedBox(height: 2),
                  Text(exam.sub, style: const TextStyle(color: softMuted, fontSize: 14.5, fontWeight: FontWeight.w600)),
                ]),
              ),
              Icon(Icons.chevron_right, color: exam.c1, size: 26),
            ]),
          ),
        ),
      ),
    );
  }
}
