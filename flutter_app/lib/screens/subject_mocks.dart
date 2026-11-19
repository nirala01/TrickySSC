import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import '../ui/nav.dart';

import '../data.dart';
import '../test/engine.dart';
import '../test/test_screen.dart';
import '../ui/soft.dart';
import '../ui/soft_list.dart';
import 'dash/logic.dart' show shortDate, n1, marksOf, maxOf;
import 'dash/pages.dart' show showDoneSheet;

/// The subject (or section) choices of an exam's mocks: key, label, icon, colour.
List<(String, String, IconData, Color)> subjectChoices(Exam e) {
  // TSSC-SM-SECTEST-V1: an exam with its own section tests (RRB Station Master) lists those
  if (e.secTests.isNotEmpty) {
    const look = [(Icons.calculate, Color(0xFFEA580C)), (Icons.bar_chart, Color(0xFF0369A1)), (Icons.psychology, Color(0xFF7C3AED)), (Icons.extension, Color(0xFF047857))];
    return [for (var i = 0; i < e.secTests.length; i++) (e.secTests[i].key, e.secTests[i].name, look[i % look.length].$1, look[i % look.length].$2)];
  }
  final all = [
    ('quant', e.maths ? 'Maths' : 'Quant', Icons.calculate, const Color(0xFFEA580C)),
    ('reasoning', 'Reasoning', Icons.psychology, const Color(0xFF7C3AED)),
    ('gk', 'Gen. Awareness', Icons.public, const Color(0xFF047857)),
    ('english', e.partD ? 'English / Hindi' : 'English', Icons.menu_book, const Color(0xFF0369A1)),
  ];
  return [for (final s in all) if (e.subjects.contains(s.$1)) s];
}

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
  /// Shown inside the Mocks tab (no page of its own): [onFull] is the "Full mock" chip.
  final bool embedded;
  final String initialSubject;
  final VoidCallback? onFull;
  const SubjectMocksScreen({super.key, this.embedded = false, this.initialSubject = '', this.onFull, required this.user, required this.exam, required this.mocks, required this.hasPass, required this.paid, required this.attempted, required this.onReturn, required this.onBuy});

  @override
  State<SubjectMocksScreen> createState() => _SubjectMocksScreenState();
}

class _SubjectMocksScreenState extends State<SubjectMocksScreen> {
  late String _subject = _subjects.any((s) => s.$1 == widget.initialSubject) ? widget.initialSubject : (_subjects.isEmpty ? '' : _subjects.first.$1); // TSSC-SM-APP-V1: no subjects, no crash
  late Set<String> _attempted = widget.attempted;
  Map<String, Map<String, dynamic>> _last = {};

  @override
  void initState() {
    super.initState();
    _loadLast();
  }

  Future<void> _loadLast() async {
    try {
      final list = await loadAttempts(widget.user.uid);
      final m = <String, Map<String, dynamic>>{};
      for (final a in list) {
        final id = '${a['mockId'] ?? ''}';
        if (id.contains('__')) m.putIfAbsent(id.replaceAll(RegExp(r'_(en|hi)__'), '__'), () => a);
      }
      if (mounted) setState(() => _last = m);
    } catch (_) {}
  }

  List<(String, String, IconData, Color)> get _subjects => subjectChoices(widget.exam);

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
    _loadLast();
  }

  String _label() => _subjects.firstWhere((s) => s.$1 == _subject).$2;

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final mocks = widget.mocks.where((m) => m.tier == 1).toList();
    final subj = _subjects.firstWhere((s) => s.$1 == _subject);
    final mins = mocks.isEmpty ? 15 : subjectMockMinutes('${exam.id}_', _subject);
    final done = mocks.where(_done).length;
    final list = ListView(padding: widget.embedded ? const EdgeInsets.fromLTRB(16, 8, 16, 14) : EdgeInsets.fromLTRB(12, 10, 12, 16 + MediaQuery.of(context).padding.bottom), children: [
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
              if (widget.embedded) SoftChip('Full mock', false, exam.c1, () => widget.onFull?.call()),
              for (final s in _subjects) SoftChip(s.$2, _subject == s.$1, exam.c1, () => setState(() => _subject = s.$1)),
            ]),
          ),
          const SizedBox(height: 10),
          if (mocks.isEmpty) const Padding(padding: EdgeInsets.all(30), child: Center(child: Text('Mocks are loading or not released yet.'))),
          for (final m in mocks) _row(m, subj.$4),
        ]);
    if (widget.embedded) return list;
    return examTheme(
      context,
      exam,
      Scaffold(
        backgroundColor: softBgTop,
        appBar: AppBar(backgroundColor: softBgTop, surfaceTintColor: softBgTop, actions: const [HomeButton()], title: Text('Subject mocks', style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink))),
        body: list,
      ),
    );
  }

  Widget _row(MockItem m, Color c) {
    final exam = widget.exam;
    final open = _open(m), done = _done(m), free = m.n <= exam.free;
    final a = _last['${mockBase(exam, m)}__$_subject'];
    final state = !open ? RowState.locked : (done ? RowState.done : RowState.todo);
    final mins = subjectMockMinutes('${exam.id}_', _subject);
    final langs = [if (m.en) 'EN', if (m.hi) 'हिंदी'].join(', ');
    final title = 'Mock ${m.n.toString().padLeft(2, '0')} · ${_label()}';
    return TestRow(
      tags: [if (free) const SoftTag.free() else const SoftTag.premium()],
      title: title,
      sub: 'From full Mock ${m.n}${langs.isNotEmpty ? ' · $langs' : ''}',
      meta: [
        if (state == RowState.done && a != null) (Icons.calendar_today_outlined, shortDate(attemptMs(a))) else (Icons.help_outline_rounded, 'Sectional'),
        (Icons.schedule_rounded, '$mins min'),
      ],
      state: state,
      score: state == RowState.done && a != null ? '${n1(marksOf(a))} / ${n1(maxOf(a))}' : null,
      accent: exam.c1,
      onTap: () => state == RowState.done ? showDoneSheet(context, user: widget.user, exam: exam, a: a, title: '${exam.name} $title', onRetake: () => _start(m)) : _start(m),
      onAction: state == RowState.done ? () => _start(m) : null,
    );
  }

}
