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
              Text('TrickySSC', style: baloo(21, color: softIndigo)),
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
                  Text('${exam.sub} · ${exam.mocks}', style: const TextStyle(color: softMuted, fontSize: 14.5, fontWeight: FontWeight.w600)),
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
