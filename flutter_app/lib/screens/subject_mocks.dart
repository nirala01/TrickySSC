import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../data.dart';
import '../test/engine.dart';
import '../test/test_screen.dart';

/// Subject-wise mocks: one subject section of each Tier 1 mock (website: mock-test-subject.html).
class SubjectMocksScreen extends StatefulWidget {
  final User user;
  final Exam exam;
  final List<MockItem> mocks;
  final bool hasPass;
  final bool paid;
  final Set<String> attempted;
  final VoidCallback onReturn;
  final VoidCallback onBuy;
  const SubjectMocksScreen({super.key, required this.user, required this.exam, required this.mocks, required this.hasPass, required this.paid, required this.attempted, required this.onReturn, required this.onBuy});

  @override
  State<SubjectMocksScreen> createState() => _SubjectMocksScreenState();
}

class _SubjectMocksScreenState extends State<SubjectMocksScreen> {
  late String _subject = _subjects.first.$1;
  late Set<String> _attempted = widget.attempted;

  List<(String, String, IconData, Color)> get _subjects {
    final e = widget.exam;
    return [
      ('quant', e.k == 'mts' || e.k == 'gd' || e.k == 'ntpc' ? 'Maths' : 'Quant', Icons.calculate, const Color(0xFFEA580C)),
      ('reasoning', 'Reasoning', Icons.psychology, const Color(0xFF7C3AED)),
      ('gk', 'Gen. Awareness', Icons.public, const Color(0xFF047857)),
      if (e.k != 'ntpc') ('english', e.k == 'gd' ? 'English / Hindi' : 'English', Icons.menu_book, const Color(0xFF0369A1)),
    ];
  }

  bool _open(MockItem m) => widget.hasPass || m.n <= widget.exam.free;

  bool _done(MockItem m) {
    final base = mockBase(widget.exam, m);
    return _attempted.contains('${base}_en__$_subject') || _attempted.contains('${base}_hi__$_subject');
  }

  Future<void> _start(MockItem m) async {
    final exam = widget.exam;
    if (!_open(m)) {
      widget.onBuy();
      return;
    }
    var lang = m.en ? 'en' : 'hi';
    if (m.en && m.hi) {
      final picked = await showModalBottomSheet<String>(
        context: context,
        backgroundColor: Colors.white,
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
        builder: (c) => SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 12),
            child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              Text('Mock ${m.n} · ${_label()}', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: exam.ink)),
              const SizedBox(height: 12),
              Row(children: [
                for (final l in const [('en', 'English'), ('hi', 'हिंदी')]) ...[
                  Expanded(
                    child: FilledButton(
                      onPressed: () => Navigator.pop(c, l.$1),
                      style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50)),
                      child: Text(l.$2, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
                    ),
                  ),
                  if (l.$1 == 'en') const SizedBox(width: 10),
                ],
              ]),
            ]),
          ),
        ),
      );
      if (picked == null || !mounted) return;
      lang = picked;
    }
    final full = '${mockBase(exam, m)}_$lang';
    await Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => TestFlow(
        user: widget.user,
        exam: exam,
        mockId: '${full}__$_subject',
        lang: lang,
        paid: widget.paid,
        title: '${exam.name} Mock ${m.n} · ${_label()}',
        loader: () => loadPaper(full, lang, subject: _subject, title: '${exam.name} Mock ${m.n}'),
      ),
    ));
    widget.onReturn();
    final a = await loadAttempted(widget.user.uid);
    if (mounted) setState(() => _attempted = a);
  }

  String _label() => _subjects.firstWhere((s) => s.$1 == _subject).$2;

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final mocks = widget.mocks.where((m) => m.tier == 1).toList();
    final subj = _subjects.firstWhere((s) => s.$1 == _subject);
    final mins = mocks.isEmpty ? 15 : subjectMockMinutes('${exam.id}_', _subject);
    final done = mocks.where(_done).length;
    return examTheme(
      context,
      exam,
      Scaffold(
        backgroundColor: Color.lerp(Colors.white, exam.c2, 0.10),
        appBar: AppBar(title: Text('Subject mocks', style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: ListView(padding: EdgeInsets.fromLTRB(12, 10, 12, 16 + MediaQuery.of(context).padding.bottom), children: [
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(18),
              gradient: LinearGradient(colors: [subj.$4, Color.lerp(subj.$4, Colors.white, 0.42)!], begin: Alignment.topLeft, end: Alignment.bottomRight),
            ),
            child: Row(children: [
              Container(
                width: 46,
                height: 46,
                decoration: BoxDecoration(color: const Color(0x33FFFFFF), borderRadius: BorderRadius.circular(12)),
                child: Icon(subj.$3, color: Colors.white, size: 26),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('${subj.$2} sectional mocks', style: const TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.w800)),
                  Text('The ${subj.$2} section of each full mock · $mins min · $done done', style: const TextStyle(color: Color(0xEEFFFFFF), fontSize: 13.5)),
                ]),
              ),
            ]),
          ),
          const SizedBox(height: 10),
          SizedBox(
            height: 42,
            child: ListView(scrollDirection: Axis.horizontal, children: [
              for (final s in _subjects)
                Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: Material(
                    color: _subject == s.$1 ? s.$4 : Colors.white,
                    borderRadius: BorderRadius.circular(20),
                    child: InkWell(
                      borderRadius: BorderRadius.circular(20),
                      onTap: () => setState(() => _subject = s.$1),
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 9),
                        child: Text(s.$2, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: _subject == s.$1 ? Colors.white : const Color(0xFF334155))),
                      ),
                    ),
                  ),
                ),
            ]),
          ),
          const SizedBox(height: 10),
          if (mocks.isEmpty) const Padding(padding: EdgeInsets.all(30), child: Center(child: Text('Mocks are loading or not released yet.'))),
          for (final m in mocks) _row(m, subj.$4),
        ]),
      ),
    );
  }

  Widget _row(MockItem m, Color c) {
    final exam = widget.exam;
    final open = _open(m), done = _done(m), free = m.n <= exam.free;
    Widget tag(String t, Color fg, Color bg) => Container(
          margin: const EdgeInsets.only(left: 6),
          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
          decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(6)),
          child: Text(t, style: TextStyle(color: fg, fontSize: 12, fontWeight: FontWeight.w800)),
        );
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Material(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: () => _start(m),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 9),
            child: Row(children: [
              Container(
                width: 40,
                height: 40,
                alignment: Alignment.center,
                decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), color: Color.lerp(Colors.white, c, open ? 0.2 : 0.08)),
                child: Text('${m.n}', style: TextStyle(color: c, fontWeight: FontWeight.w800, fontSize: 15)),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Wrap(crossAxisAlignment: WrapCrossAlignment.center, runSpacing: 2, children: [
                    Text('Mock ${m.n} · ${_label()}', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
                    if (free) tag('FREE', const Color(0xFF047857), const Color(0xFFD1FAE5)),
                    if (!free && widget.hasPass) tag('PREMIUM', const Color(0xFF92400E), const Color(0xFFFEF3C7)),
                    if (done) tag('DONE', const Color(0xFF1D4ED8), const Color(0xFFDBEAFE)),
                  ]),
                  Text([if (m.en) 'EN', if (m.hi) 'हिंदी'].join(', '), style: const TextStyle(fontSize: 13.5, color: Color(0xFF475569))),
                ]),
              ),
              const SizedBox(width: 6),
              if (open)
                Container(
                  width: 88,
                  height: 36,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(borderRadius: BorderRadius.circular(10), gradient: LinearGradient(colors: [exam.c1, exam.c2])),
                  child: Text(done ? 'Retake' : 'Start', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 15)),
                )
              else
                const SizedBox(width: 88, height: 36, child: Icon(Icons.lock_outline, color: Color(0xFF94A3B8), size: 22)),
            ]),
          ),
        ),
      ),
    );
  }
}
