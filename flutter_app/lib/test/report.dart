import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../data.dart';
import 'engine.dart';
import '../profile.dart';

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
          await addWithApp('question_reports', {
            if (paper.chapter != null) 'source': 'chapterwise' else if (isPyqId(paper.rules.mockId)) 'source': 'pyq',
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

/// Adds the doc with platform 'app' (shown on reports-admin.html); if the rules refuse the extra field, sends it without.
Future<void> addWithApp(String col, Map<String, dynamic> body, {String? id}) async {
  final c = FirebaseFirestore.instance.collection(col);
  Future<void> put(Map<String, dynamic> b) async {
    if (id == null) {
      await c.add(b);
    } else {
      await c.doc(id).set(b, SetOptions(merge: true));
    }
  }
  try {
    await put({...body, 'platform': 'app', 'appVersion': appVersion});
  } on FirebaseException catch (e) {
    if (e.code != 'permission-denied') rethrow;
    await put(body);
  }
}

/// Post-test rating, same mock_ratings doc as the website (one per student per test).
class RateCard extends StatefulWidget {
  final Exam exam;
  final Paper paper;
  final String title;
  const RateCard({super.key, required this.exam, required this.paper, required this.title});

  @override
  State<RateCard> createState() => _RateCardState();
}

class _RateCardState extends State<RateCard> {
  int _stars = 0;
  String _diff = '';
  bool _busy = false, _done = false, _hidden = true;
  String _err = '';

  String get _id => '${widget.paper.rules.mockId}_${FirebaseAuth.instance.currentUser?.uid ?? 'anon_${DateTime.now().millisecondsSinceEpoch}'}';

  @override
  void initState() {
    super.initState();
    FirebaseFirestore.instance.collection('mock_ratings').doc(_id).get().then((d) {
      if (mounted) setState(() => _hidden = d.exists);
    }).catchError((_) {
      if (mounted) setState(() => _hidden = false);
    });
  }

  // value saved (same set as the website, which reports-admin.html charts) -> label shown
  static const _diffs = {'Easy': 'Easy', 'Same as CGL': 'Same as real exam', 'Difficult': 'Difficult', 'Very Difficult': 'Very Difficult'};

  Future<void> _send() async {
    if (_stars < 1) return;
    setState(() {
      _busy = true;
      _err = '';
    });
    final u = FirebaseAuth.instance.currentUser;
    try {
      await addWithApp('mock_ratings', {
        'mockId': widget.paper.rules.mockId,
        'uid': u?.uid ?? '',
        'name': u?.displayName ?? '',
        'stars': _stars,
        'difficulty': _diff,
        'testName': widget.paper.title.isNotEmpty ? widget.paper.title : widget.title,
        if (widget.paper.chapter != null) 'source': 'chapterwise' else if (isPyqId(widget.paper.rules.mockId)) 'source': 'pyq',
        'createdAt': FieldValue.serverTimestamp(),
      }, id: _id);
      if (mounted) setState(() => _done = true);
    } catch (_) {
      if (mounted) setState(() => _err = 'Could not send. Please try again.');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_hidden) return const SizedBox.shrink();
    final c1 = widget.exam.c1;
    return Container(
      margin: const EdgeInsets.only(top: 12),
      padding: const EdgeInsets.fromLTRB(14, 12, 14, 12),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(18), border: Border.all(color: const Color(0xFFE2E8F0))),
      child: _done
          ? const Row(mainAxisAlignment: MainAxisAlignment.center, children: [
              Icon(Icons.favorite, color: Color(0xFFE11D48), size: 18),
              SizedBox(width: 6),
              Text('Thanks for rating this test!', style: TextStyle(fontWeight: FontWeight.w800, color: Color(0xFF16A34A))),
            ])
          : Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              const Text('How was this test?', textAlign: TextAlign.center, style: TextStyle(fontSize: 15.5, fontWeight: FontWeight.w900)),
              const SizedBox(height: 4),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                for (var i = 1; i <= 5; i++)
                  IconButton(
                    onPressed: _busy ? null : () => setState(() => _stars = i),
                    icon: Icon(i <= _stars ? Icons.star_rounded : Icons.star_outline_rounded, size: 34, color: i <= _stars ? const Color(0xFFF59E0B) : const Color(0xFF94A3B8)),
                  ),
              ]),
              const Text('Difficulty level', textAlign: TextAlign.center, style: TextStyle(fontSize: 12.5, color: Color(0xFF64748B), fontWeight: FontWeight.w700)),
              const SizedBox(height: 6),
              Wrap(alignment: WrapAlignment.center, spacing: 6, runSpacing: 6, children: [
                for (final d in _diffs.keys)
                  ChoiceChip(
                    label: Text(_diffs[d]!, style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.w700)),
                    selected: _diff == d,
                    selectedColor: c1.withValues(alpha: .18),
                    onSelected: _busy ? null : (_) => setState(() => _diff = d),
                  ),
              ]),
              if (_err.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 6), child: Text(_err, textAlign: TextAlign.center, style: const TextStyle(color: Color(0xFFDC2626), fontWeight: FontWeight.w700))),
              const SizedBox(height: 8),
              FilledButton(
                onPressed: _stars < 1 || _busy ? null : _send,
                style: FilledButton.styleFrom(backgroundColor: c1, minimumSize: const Size.fromHeight(44), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                child: Text(_busy ? 'Sending…' : 'Submit rating', style: const TextStyle(fontWeight: FontWeight.w800)),
              ),
            ]),
    );
  }
}
