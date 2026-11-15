import 'package:flutter/material.dart';

import '../data.dart';

class ChooseExamScreen extends StatelessWidget {
  final void Function(Exam) onPick;
  const ChooseExamScreen({super.key, required this.onPick});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 20, 16, 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Choose your exam', style: TextStyle(fontSize: 26, fontWeight: FontWeight.w800)),
              const SizedBox(height: 4),
              const Text('You can change this any time.', style: TextStyle(color: Color(0xFF64748B))),
              const SizedBox(height: 14),
              Expanded(
                child: Column(
                  children: [
                    for (final e in exams)
                      Expanded(
                        child: Padding(
                          padding: const EdgeInsets.only(bottom: 10),
                          child: _ExamCard(exam: e, onTap: () => onPick(e)),
                        ),
                      ),
                  ],
                ),
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
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(18),
          gradient: LinearGradient(colors: [exam.c1, exam.c2], begin: Alignment.topLeft, end: Alignment.bottomRight),
        ),
        child: InkWell(
          borderRadius: BorderRadius.circular(18),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 18),
            child: Row(
              children: [
                Expanded(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(exam.name, style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.w800)),
                      const SizedBox(height: 2),
                      Text('${exam.sub} · ${exam.mocks}', style: const TextStyle(color: Colors.white, fontSize: 13)),
                    ],
                  ),
                ),
                Text(exam.icon, style: const TextStyle(fontSize: 34)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
