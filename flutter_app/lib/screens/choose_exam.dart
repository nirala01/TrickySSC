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
              Row(children: [
                Container(
                  decoration: BoxDecoration(shape: BoxShape.circle, boxShadow: [BoxShadow(color: const Color(0xFFFF6B00).withValues(alpha: .3), blurRadius: 14, offset: const Offset(0, 5))]),
                  child: Image.asset('assets/logo.png', width: 40, height: 40),
                ),
                const SizedBox(width: 10),
                Text.rich(TextSpan(children: [TextSpan(text: 'Tricky', style: baloo(24)), TextSpan(text: 'SSC', style: baloo(24, color: const Color(0xFFFF6B00)))])),
              ]),
              const SizedBox(height: 14),
              Text('Choose your exam', style: baloo(34)),
              const SizedBox(height: 4),
              const Text('You can change this any time.', style: TextStyle(color: softMuted, fontSize: 15.5, fontWeight: FontWeight.w600)),
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
