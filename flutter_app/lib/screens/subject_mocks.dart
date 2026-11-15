import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import '../ui/nav.dart';

import '../data.dart';
import '../test/engine.dart';
import '../test/test_screen.dart';
import '../ui/soft.dart';
import '../ui/soft_list.dart';

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
        backgroundColor: softBgTop,
        appBar: AppBar(backgroundColor: softBgTop, surfaceTintColor: softBgTop, actions: const [HomeButton()], title: Text('Subject mocks', style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: ListView(padding: EdgeInsets.fromLTRB(12, 10, 12, 16 + MediaQuery.of(context).padding.bottom), children: [
          SoftSummary(
            icon: 'puzzle',
            title: '${subj.$2} · $done of ${mocks.length} done',
            progress: mocks.isEmpty ? 0 : done / mocks.length,
            sub: 'The ${subj.$2} section of each mock · $mins min',
            accent: exam.c1,
          ),
          const SizedBox(height: 10),
          SizedBox(
            height: 46,
            child: ListView(scrollDirection: Axis.horizontal, children: [
              for (final s in _subjects) SoftChip(s.$2, _subject == s.$1, exam.c1, () => setState(() => _subject = s.$1)),
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
    return SoftRow(
      badge: '${m.n}',
      title: 'Mock ${m.n} · ${_label()}',
      tags: [
        if (free) const SoftTag.free(),
        if (!free && widget.hasPass) const SoftTag.premium(),
        if (done) const SoftTag.done(),
      ],
      meta: [if (m.en) 'EN', if (m.hi) 'हिंदी'].join(', '),
      action: open ? (done ? 'Retake' : 'Start') : null,
      accent: exam.c1,
      onTap: () => _start(m),
    );
  }
}
