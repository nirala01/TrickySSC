import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../data.dart';
import 'engine.dart';
import 'render.dart';

class ResultScreen extends StatefulWidget {
  final User user;
  final Exam exam;
  final Paper paper;
  final Progress progress;
  final Result result;
  final String title;
  const ResultScreen({super.key, required this.user, required this.exam, required this.paper, required this.progress, required this.result, required this.title});

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  bool _saving = true;
  bool _failed = false;

  Result get r => widget.result;

  @override
  void initState() {
    super.initState();
    _save(first: true);
  }

  Future<void> _save({bool first = false}) async {
    setState(() {
      _saving = true;
      _failed = false;
    });
    if (r.correct + r.wrong == 0) {
      await clearProgress(widget.user.uid, widget.paper.rules.mockId, widget.paper.partD);
      if (mounted) setState(() => _saving = false);
      return;
    }
    try {
      await saveResult(widget.user, widget.exam, widget.paper, widget.progress, r);
      if (first) await countDailyTest(widget.user);
      await clearProgress(widget.user.uid, widget.paper.rules.mockId, widget.paper.partD);
      if (mounted) setState(() => _saving = false);
    } catch (_) {
      if (mounted) {
        setState(() {
          _saving = false;
          _failed = true;
        });
      }
    }
  }

  String _n(double v) => v == v.roundToDouble() ? '${v.round()}' : v.toStringAsFixed(1);
  String _time(int s) => s >= 3600 ? '${s ~/ 3600}h ${(s % 3600) ~/ 60}m' : '${s ~/ 60}m ${s % 60}s';

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final attempted = r.correct + r.wrong;
    final acc = attempted == 0 ? 0 : (r.correct * 100 / attempted).round();
    Widget stat(String v, String l, Color c) => Expanded(
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 10),
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
            child: Column(children: [
              Text(v, style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: c)),
              Text(l, style: const TextStyle(fontSize: 12, color: Color(0xFF64748B))),
            ]),
          ),
        );
    return Scaffold(
      backgroundColor: Color.lerp(Colors.white, exam.c2, 0.10),
      appBar: AppBar(title: Text(widget.title, style: const TextStyle(fontWeight: FontWeight.w800))),
      body: ListView(padding: const EdgeInsets.all(14), children: [
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(18),
            gradient: LinearGradient(colors: [exam.c1, exam.c2], begin: Alignment.topLeft, end: Alignment.bottomRight),
          ),
          child: Row(children: [
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                const Text('Your score', style: TextStyle(color: Colors.white, fontSize: 13)),
                Text('${_n(r.marks)} / ${_n(r.maxMarks)}', style: const TextStyle(color: Colors.white, fontSize: 30, fontWeight: FontWeight.w900)),
                Text('${r.pct}% · ${_time(r.timeUsed)} used', style: const TextStyle(color: Colors.white, fontSize: 13)),
              ]),
            ),
            if (r.rank != null)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14)),
                child: Column(children: [
                  Text('#${r.rank}', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: exam.c1)),
                  Text(r.candidates == null ? 'Rank' : 'of ${r.candidates}', style: const TextStyle(fontSize: 12, color: Color(0xFF64748B))),
                ]),
              ),
          ]),
        ),
        const SizedBox(height: 10),
        Row(children: [
          stat('${r.correct}', 'Correct', const Color(0xFF16A34A)),
          const SizedBox(width: 8),
          stat('${r.wrong}', 'Wrong', const Color(0xFFDC2626)),
          const SizedBox(width: 8),
          stat('${r.skip}', 'Skipped', const Color(0xFF64748B)),
          const SizedBox(width: 8),
          stat('$acc%', 'Accuracy', exam.c1),
        ]),
        const SizedBox(height: 10),
        Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14)),
          child: Column(children: [
            const Row(children: [
              Expanded(child: Text('Subject', style: TextStyle(fontWeight: FontWeight.w800))),
              SizedBox(width: 40, child: Text('✓', textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.w800, color: Color(0xFF16A34A)))),
              SizedBox(width: 40, child: Text('✕', textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.w800, color: Color(0xFFDC2626)))),
              SizedBox(width: 56, child: Text('Marks', textAlign: TextAlign.right, style: TextStyle(fontWeight: FontWeight.w800))),
            ]),
            const Divider(),
            for (final e in r.subjects.entries)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Row(children: [
                  Expanded(child: Text(e.key)),
                  SizedBox(width: 40, child: Text('${e.value.correct}', textAlign: TextAlign.center)),
                  SizedBox(width: 40, child: Text('${e.value.wrong}', textAlign: TextAlign.center)),
                  SizedBox(width: 56, child: Text(_n(e.value.marks), textAlign: TextAlign.right, style: const TextStyle(fontWeight: FontWeight.w700))),
                ]),
              ),
          ]),
        ),
        const SizedBox(height: 10),
        if (_saving)
          const Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2)),
            SizedBox(width: 8),
            Text('Saving your result…'),
          ])
        else if (_failed)
          Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            const Text('Result not saved.', style: TextStyle(color: Color(0xFFDC2626), fontWeight: FontWeight.w700)),
            TextButton(onPressed: _save, child: const Text('Try again')),
          ])
        else
          Text(attempted == 0 ? 'No question was answered, so this result is not saved.' : '✓ Result saved to your dashboard',
              textAlign: TextAlign.center, style: TextStyle(color: attempted == 0 ? const Color(0xFF64748B) : const Color(0xFF16A34A), fontWeight: FontWeight.w700)),
        const SizedBox(height: 12),
        FilledButton.icon(
          onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => SolutionsScreen(exam: exam, paper: widget.paper, progress: widget.progress))),
          style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
          icon: const Icon(Icons.menu_book),
          label: const Text('View solutions', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
        ),
        const SizedBox(height: 8),
        OutlinedButton(
          onPressed: _saving ? null : () => Navigator.of(context).pop(true),
          style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
          child: const Text('Back to mocks', style: TextStyle(fontWeight: FontWeight.w800)),
        ),
      ]),
    );
  }
}

// ======================================================================= solutions

class SolutionsScreen extends StatefulWidget {
  final Exam exam;
  final Paper paper;
  final Progress progress;
  const SolutionsScreen({super.key, required this.exam, required this.paper, required this.progress});

  @override
  State<SolutionsScreen> createState() => _SolutionsScreenState();
}

class _SolutionsScreenState extends State<SolutionsScreen> {
  int _i = 0;
  String _filter = 'all';

  List<int> get _list {
    final p = widget.paper, pr = widget.progress;
    return [
      for (var i = 0; i < p.questions.length; i++)
        if (_filter == 'all' ||
            (_filter == 'wrong' && pr.answers[i] != null && pr.answers[i] != p.questions[i].correct) ||
            (_filter == 'skip' && pr.answers[i] == null) ||
            (_filter == 'right' && pr.answers[i] == p.questions[i].correct))
          i
    ];
  }

  String _status(int i) {
    final a = widget.progress.answers[i];
    if (a == null) return 'skip';
    return a == widget.paper.questions[i].correct ? 'right' : 'wrong';
  }

  static const _col = {'right': Color(0xFF16A34A), 'wrong': Color(0xFFDC2626), 'skip': Color(0xFF94A3B8)};

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final list = _list;
    if (list.isNotEmpty && !list.contains(_i)) _i = list.first;
    final q = widget.paper.questions[_i];
    final a = widget.progress.answers[_i];
    final pos = list.indexOf(_i);
    Widget chip(String key, String label) => Padding(
          padding: const EdgeInsets.only(right: 8),
          child: ChoiceChip(label: Text(label), selected: _filter == key, onSelected: (_) => setState(() => _filter = key), visualDensity: VisualDensity.compact),
        );
    Widget panel(String title, IconData icon, Color c, String html, [String img = '']) => Container(
          margin: const EdgeInsets.only(top: 10),
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: Color.lerp(Colors.white, c, 0.08), borderRadius: BorderRadius.circular(12), border: Border.all(color: Color.lerp(Colors.white, c, 0.35)!)),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [Icon(icon, size: 18, color: c), const SizedBox(width: 6), Text(title, style: TextStyle(fontWeight: FontWeight.w800, color: c))]),
            const SizedBox(height: 6),
            if (html.isNotEmpty) Rich(contentHtml(html), size: 15),
            if (img.isNotEmpty) Figure(img),
          ]),
        );
    return Scaffold(
      backgroundColor: Color.lerp(Colors.white, exam.c2, 0.08),
      appBar: AppBar(title: const Text('Solutions', style: TextStyle(fontWeight: FontWeight.w800))),
      body: Column(children: [
        SizedBox(
          height: 46,
          child: ListView(scrollDirection: Axis.horizontal, padding: const EdgeInsets.fromLTRB(10, 6, 10, 2), children: [
            chip('all', 'All'),
            chip('wrong', 'Wrong'),
            chip('skip', 'Skipped'),
            chip('right', 'Correct'),
          ]),
        ),
        SizedBox(
          height: 48,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            itemCount: list.length,
            itemBuilder: (_, k) {
              final i = list[k];
              return Padding(
                padding: const EdgeInsets.only(right: 6),
                child: InkWell(
                  onTap: () => setState(() => _i = i),
                  borderRadius: BorderRadius.circular(10),
                  child: Container(
                    width: 40,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(color: _col[_status(i)], borderRadius: BorderRadius.circular(10), border: i == _i ? Border.all(color: const Color(0xFF0F172A), width: 2.5) : null),
                    child: Text('${i + 1}', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800)),
                  ),
                ),
              );
            },
          ),
        ),
        Expanded(
          child: list.isEmpty
              ? const Center(child: Text('No questions here.'))
              : ListView(padding: const EdgeInsets.fromLTRB(14, 6, 14, 14), children: [
                  Row(children: [
                    Text('Q ${_i + 1}', style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
                    const SizedBox(width: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(color: _col[_status(_i)], borderRadius: BorderRadius.circular(8)),
                      child: Text({'right': 'Correct', 'wrong': 'Wrong', 'skip': 'Not answered'}[_status(_i)]!, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w800)),
                    ),
                  ]),
                  const SizedBox(height: 8),
                  Rich(questionHtml(q.text), size: 16),
                  if (q.imageUrl.isNotEmpty) Figure(q.imageUrl),
                  const SizedBox(height: 8),
                  for (final k in q.keys)
                    Container(
                      margin: const EdgeInsets.only(bottom: 8),
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                      decoration: BoxDecoration(
                        color: k == q.correct ? const Color(0xFFDCFCE7) : (k == a ? const Color(0xFFFEE2E2) : Colors.white),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: k == q.correct ? const Color(0xFF16A34A) : (k == a ? const Color(0xFFDC2626) : const Color(0xFFE2E8F0))),
                      ),
                      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text('$k  ', style: const TextStyle(fontWeight: FontWeight.w800)),
                        Expanded(
                          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                            if (stripFigRef(q.option(k)).isNotEmpty) Rich(contentHtml(stripFigRef(q.option(k))), size: 15),
                            if (q.optionImage(k).isNotEmpty) Figure(q.optionImage(k), maxHeight: 100),
                          ]),
                        ),
                        if (k == q.correct) const Icon(Icons.check_circle, color: Color(0xFF16A34A), size: 20),
                        if (k == a && k != q.correct) const Icon(Icons.cancel, color: Color(0xFFDC2626), size: 20),
                      ]),
                    ),
                  if (q.explanation.isNotEmpty || q.solutionImage.isNotEmpty) panel('Step-by-step solution', Icons.lightbulb_outline, const Color(0xFF2563EB), q.explanation, q.solutionImage),
                  if (q.trick.isNotEmpty) panel('Quick trick', Icons.bolt, const Color(0xFFD97706), q.trick),
                  if (q.concept.isNotEmpty) panel('Concept', Icons.psychology_outlined, const Color(0xFF7C3AED), q.concept),
                ]),
        ),
        SafeArea(
          top: false,
          child: Padding(
            padding: const EdgeInsets.fromLTRB(10, 6, 10, 8),
            child: Row(children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: pos > 0 ? () => setState(() => _i = list[pos - 1]) : null,
                  style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(46)),
                  child: const Text('Previous'),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: FilledButton(
                  onPressed: pos >= 0 && pos < list.length - 1 ? () => setState(() => _i = list[pos + 1]) : null,
                  style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(46)),
                  child: const Text('Next'),
                ),
              ),
            ]),
          ),
        ),
      ]),
    );
  }
}
