import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../data.dart';
import 'engine.dart';

const _reasons = {
  'question': ['Wrong answer key', 'Question is incorrect', 'Options wrong or incomplete', 'Typo or formatting', 'Image not visible', 'Other'],
  'solution': ['Solution is wrong', 'Solution contradicts the answer key', 'Steps unclear or incomplete', 'Calculation mistake in solution', 'Typo or formatting', 'Solution image not visible', 'Other'],
};

/// Report a question (test screen) or a solution (solutions screen). Same question_reports doc as the website.
Future<void> showReport(BuildContext context, {required Exam exam, required Paper paper, required int index, required String target}) async {
  final q = paper.questions[index];
  final note = TextEditingController();
  String reason = '';
  bool busy = false, done = false;
  String? err;
  await showModalBottomSheet(
    context: context,
    isScrollControlled: true,
    backgroundColor: Colors.white,
    shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
    builder: (c) => StatefulBuilder(builder: (c, set) {
      Future<void> send() async {
        if (reason.isEmpty) {
          set(() => err = target == 'solution' ? 'Please choose what is wrong with this solution.' : 'Please choose what is wrong with this question.');
          return;
        }
        set(() {
          busy = true;
          err = null;
        });
        final u = FirebaseAuth.instance.currentUser;
        try {
          await FirebaseFirestore.instance.collection('question_reports').add({
            'mockId': paper.rules.mockId,
            'qNum': '${q.qNumOr(index + 1)}',
            'position': index + 1,
            'subject': q.subjectRaw,
            'target': target,
            'reason': reason,
            'note': note.text.length > 1000 ? note.text.substring(0, 1000) : note.text,
            'uid': u?.uid ?? '',
            'name': u?.displayName ?? '',
            'testName': paper.title.isNotEmpty ? paper.title : exam.name,
            'createdAt': FieldValue.serverTimestamp(),
          });
          set(() => done = true);
        } catch (_) {
          set(() {
            busy = false;
            err = 'Could not send the report. Please check your internet and try again.';
          });
        }
      }

      return Padding(
        padding: EdgeInsets.fromLTRB(16, 16, 16, 12 + MediaQuery.of(c).viewInsets.bottom),
        child: SafeArea(
          child: done
              ? Column(mainAxisSize: MainAxisSize.min, children: [
                  const Icon(Icons.check_circle, color: Color(0xFF16A34A), size: 48),
                  const SizedBox(height: 8),
                  Text(target == 'solution' ? 'Thanks! This solution has been sent to our team for review.' : 'Thanks! This question has been sent to our team for review.',
                      textAlign: TextAlign.center, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
                  const SizedBox(height: 12),
                  FilledButton(onPressed: () => Navigator.pop(c), style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(46)), child: const Text('Close')),
                ])
              : Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                  Text(target == 'solution' ? 'Report a problem in the solution' : 'Report a problem', style: TextStyle(fontSize: 19, fontWeight: FontWeight.w800, color: exam.ink)),
                  Text('${target == 'solution' ? 'Solution of ' : ''}Question ${index + 1}${q.subjectRaw.isNotEmpty ? ' · ${q.subjectRaw}' : ''}', style: const TextStyle(color: Color(0xFF64748B))),
                  const SizedBox(height: 12),
                  Wrap(spacing: 8, runSpacing: 8, children: [
                    for (final r in _reasons[target]!)
                      ChoiceChip(
                        label: Text(r),
                        selected: reason == r,
                        onSelected: (_) => set(() {
                          reason = r;
                          err = null;
                        }),
                      ),
                  ]),
                  const SizedBox(height: 12),
                  TextField(
                    controller: note,
                    maxLines: 3,
                    maxLength: 1000,
                    decoration: InputDecoration(hintText: 'Add details (optional)…', border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
                  ),
                  if (err != null) Padding(padding: const EdgeInsets.only(bottom: 8), child: Text(err!, style: const TextStyle(color: Color(0xFFDC2626), fontWeight: FontWeight.w600))),
                  Row(children: [
                    Expanded(child: OutlinedButton(onPressed: () => Navigator.pop(c), style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(46)), child: const Text('Cancel'))),
                    const SizedBox(width: 10),
                    Expanded(
                      child: FilledButton(
                        onPressed: busy ? null : send,
                        style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(46)),
                        child: Text(busy ? 'Sending…' : 'Submit report'),
                      ),
                    ),
                  ]),
                ]),
        ),
      );
    }),
  );

}

class ReportLink extends StatelessWidget {
  final String label;
  final VoidCallback onTap;
  const ReportLink(this.label, this.onTap, {super.key});
  @override
  Widget build(BuildContext context) => Align(
        alignment: Alignment.centerRight,
        child: TextButton.icon(
          onPressed: onTap,
          style: TextButton.styleFrom(foregroundColor: const Color(0xFF94A3B8), visualDensity: VisualDensity.compact),
          icon: const Icon(Icons.flag_outlined, size: 16),
          label: Text(label, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
        ),
      );
}
