import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import '../ui/soft.dart';
import '../ui/nav.dart';
import 'package:scrollable_positioned_list/scrollable_positioned_list.dart';

import '../data.dart';
import 'engine.dart';
import '../screens/dashboard.dart';
import 'compare.dart';
import 'leaderboard.dart';
import 'report.dart';
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
  Compare? _cmp;

  void _loadCompare() => Compare.load(widget.paper, widget.progress).then((c) {
        if (mounted && c != null) setState(() => _cmp = c);
      });

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
      _loadCompare();
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

  Widget _vsTopper(Exam exam) {
    final t = _cmp!.topperTotals();
    final lb = _cmp!.lbTop ?? const {};
    final tTime = (lb['timeUsed'] as num? ?? 0).toInt();
    final sm = lb['subjectMarks'] is Map ? lb['subjectMarks'] as Map : const {};
    final rows = <List<String>>[
      ['Marks', _n(r.marks), _n(t.$1)],
      ['✓ Correct', '${r.correct}', '${t.$2}'],
      ['✕ Wrong', '${r.wrong}', '${t.$3}'],
      ['– Skipped', '${r.skip}', '${t.$4}'],
      if (tTime > 0) ['⏱ Time', _time(r.timeUsed), _time(tTime)],
      for (final e in r.subjects.entries)
        if (sm[e.key] is num) [e.key, _n(e.value.marks), _n((sm[e.key] as num).toDouble())],
    ];
    final pct = r.rank != null && (r.candidates ?? 0) > 1 ? ((r.candidates! - r.rank!) * 100 / (r.candidates! - 1)).round() : null;
    TextStyle hs(Color c) => TextStyle(fontWeight: FontWeight.w800, color: c, fontSize: 14);
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(18)),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('You vs Topper', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: exam.ink)),
        if (pct != null) Text('You did better than $pct% of students', style: const TextStyle(fontSize: 13.5, color: Color(0xFF475569))),
        const SizedBox(height: 8),
        Row(children: [
          const Expanded(child: SizedBox()),
          SizedBox(width: 76, child: Text('🙋 You', textAlign: TextAlign.center, style: hs(exam.c1))),
          SizedBox(width: 86, child: Text('👑 Topper', textAlign: TextAlign.center, style: hs(const Color(0xFFB45309)))),
        ]),
        const Divider(),
        for (final row in rows)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 4),
            child: Row(children: [
              Expanded(child: Text(row[0], style: const TextStyle(fontSize: 14.5))),
              SizedBox(width: 76, child: Text(row[1], textAlign: TextAlign.center, style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w700))),
              SizedBox(width: 86, child: Text(row[2], textAlign: TextAlign.center, style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w700, color: Color(0xFFB45309)))),
            ]),
          ),
      ]),
    );
  }
  String _time(int s) => s >= 3600 ? '${s ~/ 3600}h ${(s % 3600) ~/ 60}m' : '${s ~/ 60}m ${s % 60}s';

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final attempted = r.correct + r.wrong;
    final acc = attempted == 0 ? 0 : (r.correct * 100 / attempted).round();
    Widget stat(String v, String l, Color c) => Expanded(
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 10),
            decoration: softCard(radius: 16, glow: c),
            child: Column(children: [
              Text(v, style: baloo(22, color: c)),
              Text(l, style: const TextStyle(fontSize: 12.5, color: softMuted, fontWeight: FontWeight.w700)),
            ]),
          ),
        );
    void board() => Navigator.of(context).push(MaterialPageRoute(
          builder: (_) => LeaderboardScreen(exam: exam, base: lbBase(widget.paper.rules.mockId), title: widget.title, uid: widget.user.uid),
        ));
    return examTheme(context, exam, Container(decoration: softBg, child: Scaffold(
      backgroundColor: Colors.transparent,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        surfaceTintColor: Colors.transparent,
        scrolledUnderElevation: 0,
        actions: const [HomeButton()],
        title: Text(widget.title, maxLines: 1, overflow: TextOverflow.ellipsis, style: baloo(20)),
      ),
      body: ListView(padding: EdgeInsets.fromLTRB(14, 8, 14, 16 + MediaQuery.of(context).padding.bottom), children: [
        Container(
          padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(22),
            gradient: LinearGradient(colors: [exam.c1, Color.lerp(exam.c1, exam.c2, .55)!], begin: Alignment.topLeft, end: Alignment.bottomRight),
            boxShadow: [BoxShadow(color: exam.c1.withValues(alpha: .3), blurRadius: 18, offset: const Offset(0, 8))],
          ),
          child: Row(children: [
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                const Text('Your score', style: TextStyle(color: Color(0xEEFFFFFF), fontSize: 14, fontWeight: FontWeight.w700)),
                Text('${_n(r.marks)} / ${_n(r.maxMarks)}', style: baloo(34, color: Colors.white)),
                Text('${r.pct}% · ${_time(r.timeUsed)} used', style: const TextStyle(color: Color(0xEEFFFFFF), fontSize: 13.5, fontWeight: FontWeight.w600)),
              ]),
            ),
            if (r.rank != null)
              GestureDetector(onTap: board, child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16)),
                child: Column(children: [
                  Text('#${r.rank}', style: baloo(26, color: exam.c1)),
                  Text(r.candidates == null ? 'Rank' : 'of ${r.candidates}', style: const TextStyle(fontSize: 12, color: Color(0xFF64748B))),
                ]),
              )),
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
          padding: const EdgeInsets.all(16),
          decoration: softCard(radius: 20),
          child: Column(children: [
            Row(children: [
              Expanded(child: Text('Subject-wise', style: baloo(17))),
              const SizedBox(width: 40, child: Text('✓', textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.w800, color: Color(0xFF16A34A)))),
              const SizedBox(width: 40, child: Text('✕', textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.w800, color: Color(0xFFDC2626)))),
              const SizedBox(width: 56, child: Text('Marks', textAlign: TextAlign.right, style: TextStyle(fontWeight: FontWeight.w800))),
            ]),
            const Divider(),
            for (final e in r.subjects.entries)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Row(children: [
                  Expanded(child: Text(e.key, style: const TextStyle(fontWeight: FontWeight.w700, color: softInk))),
                  SizedBox(width: 40, child: Text('${e.value.correct}', textAlign: TextAlign.center)),
                  SizedBox(width: 40, child: Text('${e.value.wrong}', textAlign: TextAlign.center)),
                  SizedBox(width: 56, child: Text(_n(e.value.marks), textAlign: TextAlign.right, style: const TextStyle(fontWeight: FontWeight.w700))),
                ]),
              ),
          ]),
        ),
        if (_cmp != null)
          Padding(
            padding: const EdgeInsets.only(top: 10),
            child: Material(
              color: const Color(0xFFFEF3C7),
              borderRadius: BorderRadius.circular(14),
              child: InkWell(
                borderRadius: BorderRadius.circular(14),
                onTap: () => showModalBottomSheet(
                  context: context,
                  isScrollControlled: true,
                  backgroundColor: Colors.transparent,
                  builder: (c) => SafeArea(
                    child: Padding(
                      padding: const EdgeInsets.all(10),
                      child: SingleChildScrollView(child: examTheme(c, exam, _vsTopper(exam))),
                    ),
                  ),
                ),
                child: const Padding(
                  padding: EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  child: Row(children: [
                    Text('👑', style: TextStyle(fontSize: 20)),
                    SizedBox(width: 10),
                    Expanded(child: Text('You vs Topper', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: Color(0xFF92400E)))),
                    Icon(Icons.chevron_right, color: Color(0xFF92400E)),
                  ]),
                ),
              ),
            ),
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
        if (!_saving && !_failed && attempted > 0) RateCard(exam: exam, paper: widget.paper, title: widget.title),
        const SizedBox(height: 12),
        FilledButton.icon(
          onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => SolutionsScreen(exam: exam, paper: widget.paper, progress: widget.progress))),
          style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
          icon: const Icon(Icons.menu_book),
          label: const Text('View solutions', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
        ),
        const SizedBox(height: 8),
        Row(children: [
          Expanded(
            child: FilledButton.tonalIcon(
              onPressed: _saving || _failed ? null : board,
              style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              icon: const Icon(Icons.emoji_events_outlined),
              label: const Text('Leaderboard', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800)),
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: FilledButton.tonalIcon(
              onPressed: _saving
                  ? null
                  : () => Navigator.of(context).push(MaterialPageRoute(
                        builder: (c) => examTheme(
                          c,
                          exam,
                          Container(
                            decoration: softBg,
                            child: Scaffold(
                              backgroundColor: Colors.transparent,
                              appBar: AppBar(backgroundColor: Colors.transparent, surfaceTintColor: Colors.transparent, actions: const [HomeButton()], title: Text('My dashboard', style: baloo(21))),
                              body: DashboardTab(user: widget.user, exam: exam, version: 0, onMocks: () => Navigator.of(c).pop()),
                            ),
                          ),
                        ),
                      )),
              style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              icon: const Icon(Icons.insights),
              label: const Text('Dashboard', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800)),
            ),
          ),
        ]),
        const SizedBox(height: 8),
        OutlinedButton(
          onPressed: _saving ? null : () => Navigator.of(context).pop(true),
          style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
          child: const Text('Back to mocks', style: TextStyle(fontWeight: FontWeight.w800)),
        ),
      ]),
    )));
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
  bool _scrollMode = true;
  int _sec = -1; // section filter, -1 = all
  Compare? _cmp;

  @override
  void initState() {
    super.initState();
    Compare.load(widget.paper, widget.progress).then((c) {
      if (mounted && c != null) setState(() => _cmp = c);
    });
  }
  final _items = ItemScrollController();
  final _strip = ScrollController();

  Paper get p => widget.paper;
  Progress get pr => widget.progress;

  List<int> get _list => [
        for (var i = 0; i < p.questions.length; i++)
          if ((_filter == 'all' || _status(i) == _filter) && (_sec < 0 || (i >= p.sections[_sec].from && i <= p.sections[_sec].to))) i
      ];

  String _status(int i) {
    final a = pr.answers[i];
    if (a == null) return 'skip';
    return a == p.questions[i].correct ? 'right' : 'wrong';
  }

  int _count(String f) => f == 'all' ? p.questions.length : [for (var i = 0; i < p.questions.length; i++) if (_status(i) == f) i].length;

  static const _col = {'right': Color(0xFF16A34A), 'wrong': Color(0xFFDC2626), 'skip': Color(0xFF94A3B8)};
  static const _label = {'right': 'Correct', 'wrong': 'Wrong', 'skip': 'Not answered'};

  String _section(int i) {
    for (final s in p.sections) {
      if (i >= s.from && i <= s.to) return s.label;
    }
    return '';
  }

  void _jump(int i) {
    setState(() => _i = i);
    if (_scrollMode) {
      final k = _list.indexOf(i);
      if (k >= 0 && _items.isAttached) _items.jumpTo(index: k);
    }
  }

  Widget _panel(String title, IconData icon, Color c, String html, [String img = '']) => Container(
        margin: const EdgeInsets.only(top: 8),
        padding: const EdgeInsets.fromLTRB(10, 8, 10, 8),
        decoration: BoxDecoration(
          color: Color.lerp(Colors.white, c, 0.06),
          borderRadius: BorderRadius.circular(10),
          border: Border(left: BorderSide(color: c, width: 3)),
        ),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [Icon(icon, size: 16, color: c), const SizedBox(width: 5), Text(title, style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800, color: c))]),
          const SizedBox(height: 4),
          if (html.isNotEmpty) Rich(contentHtml(html), size: 14.5),
          if (img.isNotEmpty) Figure(img),
        ]),
      );

  Color _optBg(String k, Question q, String? a) => k == q.correct ? const Color(0xFFDCFCE7) : (k == a ? const Color(0xFFFEE2E2) : Colors.white);
  Color _optBorder(String k, Question q, String? a) => k == q.correct ? const Color(0xFF16A34A) : (k == a ? const Color(0xFFDC2626) : const Color(0xFFE2E8F0));

  Widget _mark(String k, Question q, String? a) => k == q.correct
      ? const Icon(Icons.check_circle, color: Color(0xFF16A34A), size: 18)
      : (k == a ? const Icon(Icons.cancel, color: Color(0xFFDC2626), size: 18) : const SizedBox(width: 18));

  Widget _options(Question q, String? a) {
    final imageOnly = q.keys.every((k) => stripFigRef(q.option(k)).isEmpty && q.optionImage(k).isNotEmpty);
    if (imageOnly) {
      Widget tile(String k) => Expanded(
            child: Container(
              padding: const EdgeInsets.fromLTRB(6, 6, 6, 4),
              decoration: BoxDecoration(color: _optBg(k, q, a), borderRadius: BorderRadius.circular(10), border: Border.all(color: _optBorder(k, q, a), width: k == q.correct || k == a ? 1.6 : 1)),
              child: Column(children: [
                Row(children: [Text(k, style: const TextStyle(fontWeight: FontWeight.w800)), const Spacer(), _mark(k, q, a)]),
                SizedBox(height: 104, child: Center(child: Figure(q.optionImage(k), maxHeight: 96))),
              ]),
            ),
          );
      return Column(children: [
        for (var i = 0; i < q.keys.length; i += 2)
          Padding(
            padding: const EdgeInsets.only(bottom: 6),
            child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              tile(q.keys[i]),
              const SizedBox(width: 6),
              if (i + 1 < q.keys.length) tile(q.keys[i + 1]) else const Expanded(child: SizedBox()),
            ]),
          ),
      ]);
    }
    return Column(children: [
      for (final k in q.keys)
        Container(
          margin: const EdgeInsets.only(bottom: 6),
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7),
          decoration: BoxDecoration(color: _optBg(k, q, a), borderRadius: BorderRadius.circular(10), border: Border.all(color: _optBorder(k, q, a), width: k == q.correct || k == a ? 1.6 : 1)),
          child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            SizedBox(width: 22, child: Text(k, style: const TextStyle(fontWeight: FontWeight.w800))),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                if (stripFigRef(q.option(k)).isNotEmpty) Rich(contentHtml(stripFigRef(q.option(k))), size: 14.5),
                if (q.optionImage(k).isNotEmpty) Figure(q.optionImage(k), maxHeight: 100),
              ]),
            ),
            _mark(k, q, a),
          ]),
        ),
    ]);
  }

  Widget _card(int i) {
    final q = p.questions[i];
    final a = pr.answers[i];
    final st = _status(i);
    final secs = (pr.qMs[i] ?? 0) ~/ 1000;
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.fromLTRB(12, 10, 12, 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border(left: BorderSide(color: _col[st]!, width: 4)),
        boxShadow: const [BoxShadow(color: Color(0x0F000000), blurRadius: 6, offset: Offset(0, 2))],
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Text('Q${i + 1}', style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w900)),
          const SizedBox(width: 6),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
            decoration: BoxDecoration(color: _col[st], borderRadius: BorderRadius.circular(6)),
            child: Text(_label[st]!, style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w800)),
          ),
          const SizedBox(width: 6),
          Expanded(child: Text(_section(i), overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 12, color: Color(0xFF64748B)))),
          if (secs > 0) Text('⏱ ${secs ~/ 60}:${(secs % 60).toString().padLeft(2, '0')}', style: const TextStyle(fontSize: 12, color: Color(0xFF64748B))),
        ]),
        if (_cmp != null)
          Builder(builder: (_) {
            final row = _cmp!.row(i);
            return Padding(
              padding: const EdgeInsets.only(top: 6),
              child: Material(
                color: const Color(0xFFFEF3C7),
                borderRadius: BorderRadius.circular(10),
                child: InkWell(
                  borderRadius: BorderRadius.circular(10),
                  onTap: () => showModalBottomSheet(
                    context: context,
                    backgroundColor: Colors.transparent,
                    builder: (c) => SafeArea(
                      child: Container(
                        margin: const EdgeInsets.all(10),
                        padding: const EdgeInsets.all(6),
                        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(18)),
                        child: examTheme(c, widget.exam, CompareStrip(row)),
                      ),
                    ),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7),
                    child: Row(children: [
                      const Text('👑 You vs Topper', style: TextStyle(fontSize: 13.5, fontWeight: FontWeight.w800, color: Color(0xFF92400E))),
                      const Spacer(),
                      Text('${row.pc}% got it right', style: const TextStyle(fontSize: 12.5, color: Color(0xFF92400E))),
                      const Icon(Icons.chevron_right, size: 18, color: Color(0xFF92400E)),
                    ]),
                  ),
                ),
              ),
            );
          }),
        if ('${q.raw['_src'] ?? ''}'.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(top: 6),
            child: Text('📌 Asked in ${q.raw['_src']}${q.raw['_srcQ'] != null ? ' · Q${q.raw['_srcQ']}' : ''}',
                style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w700, color: widget.exam.c1)),
          ),
        const SizedBox(height: 6),
        Rich(questionHtml(q.text), size: 15.5),
        if (q.imageUrl.isNotEmpty) Figure(q.imageUrl),
        const SizedBox(height: 6),
        _options(q, a),
        if (q.explanation.isNotEmpty || q.solutionImage.isNotEmpty) _panel('Solution', Icons.lightbulb_outline, const Color(0xFF2563EB), q.explanation, q.solutionImage),
        if (q.trick.isNotEmpty) _panel('Quick trick', Icons.bolt, const Color(0xFFD97706), q.trick),
        if (q.concept.isNotEmpty) _panel('Concept', Icons.psychology_outlined, const Color(0xFF7C3AED), q.concept),
        ReportLink('Report a problem in the solution', () => showReport(context, exam: widget.exam, paper: p, index: i, target: 'solution')),
      ]),
    );
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final list = _list;
    if (list.isNotEmpty && !list.contains(_i)) _i = list.first;
    final pos = list.indexOf(_i);
    Widget chip(String key, String label) => Padding(
          padding: const EdgeInsets.only(right: 6),
          child: ChoiceChip(
            label: Text('$label ${_count(key)}'),
            selected: _filter == key,
            onSelected: (_) => setState(() => _filter = key),
            visualDensity: VisualDensity.compact,
            labelStyle: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700),
          ),
        );
    return examTheme(context, exam, Scaffold(
      backgroundColor: const Color(0xFFEEF2FF),
      appBar: AppBar(
        titleSpacing: 0,
        title: Text('Solutions', style: TextStyle(fontWeight: FontWeight.w800, color: exam.ink)),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 0),
            child: SegmentedButton<bool>(
              showSelectedIcon: false,
              style: const ButtonStyle(visualDensity: VisualDensity.compact),
              segments: const [
                ButtonSegment(value: true, icon: Icon(Icons.view_agenda_outlined, size: 18), label: Text('Scroll')),
                ButtonSegment(value: false, icon: Icon(Icons.crop_square, size: 18), label: Text('One')),
              ],
              selected: {_scrollMode},
              onSelectionChanged: (v) => setState(() => _scrollMode = v.first),
            ),
          ),
          const HomeButton(),
        ],
      ),
      body: Column(children: [
        SizedBox(
          height: 44,
          child: ListView(scrollDirection: Axis.horizontal, padding: const EdgeInsets.fromLTRB(10, 4, 10, 2), children: [
            chip('all', 'All'),
            chip('wrong', 'Wrong'),
            chip('skip', 'Skipped'),
            chip('right', 'Correct'),
          ]),
        ),
        if (p.sections.length > 1)
          SizedBox(
            height: 40,
            child: ListView(scrollDirection: Axis.horizontal, padding: const EdgeInsets.fromLTRB(10, 2, 10, 2), children: [
              for (var s = -1; s < p.sections.length; s++)
                Padding(
                  padding: const EdgeInsets.only(right: 6),
                  child: ChoiceChip(
                    label: Text(s < 0 ? 'All sections' : p.sections[s].label),
                    selected: _sec == s,
                    onSelected: (_) => setState(() => _sec = s),
                    visualDensity: VisualDensity.compact,
                    selectedColor: Color.lerp(Colors.white, exam.c2, 0.35),
                    labelStyle: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: exam.ink),
                  ),
                ),
            ]),
          ),
        if (_cmp != null)
          Builder(builder: (_) {
            final t = _cmp!.topperTotals();
            String n(double v) => v == v.roundToDouble() ? '${v.round()}' : '$v';
            return Container(
              margin: const EdgeInsets.fromLTRB(10, 2, 10, 2),
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              decoration: BoxDecoration(color: const Color(0xFFFEF3C7), borderRadius: BorderRadius.circular(10)),
              child: Text('👑 Topper: ${n(t.$1)} marks · ✓ ${t.$2} · ✕ ${t.$3} · – ${t.$4}',
                  style: const TextStyle(fontSize: 13.5, fontWeight: FontWeight.w700, color: Color(0xFF92400E))),
            );
          }),
        SizedBox(
          height: 42,
          child: ListView.builder(
            controller: _strip,
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            itemCount: list.length,
            itemBuilder: (_, k) {
              final i = list[k];
              return Padding(
                padding: const EdgeInsets.only(right: 5),
                child: InkWell(
                  onTap: () => _jump(i),
                  borderRadius: BorderRadius.circular(8),
                  child: Container(
                    width: 36,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(color: _col[_status(i)], borderRadius: BorderRadius.circular(8), border: i == _i ? Border.all(color: const Color(0xFF0F172A), width: 2.5) : null),
                    child: Text('${i + 1}', style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w800)),
                  ),
                ),
              );
            },
          ),
        ),
        Expanded(
          child: list.isEmpty
              ? const Center(child: Text('No questions here.'))
              : _scrollMode
                  ? ScrollablePositionedList.builder(
                      key: ValueKey('scroll_$_filter'),
                      itemScrollController: _items,
                      padding: EdgeInsets.fromLTRB(10, 4, 10, 16 + MediaQuery.of(context).padding.bottom),
                      itemCount: list.length,
                      minCacheExtent: 600,
                      itemBuilder: (_, k) => _card(list[k]),
                    )
                  : ListView(key: ValueKey('one_$_i'), padding: const EdgeInsets.fromLTRB(10, 4, 10, 10), children: [_card(_i)]),
        ),
        if (!_scrollMode && list.isNotEmpty)
          SafeArea(
            top: false,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(10, 4, 10, 8),
              child: Row(children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: pos > 0 ? () => setState(() => _i = list[pos - 1]) : null,
                    style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(46), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                    icon: const Icon(Icons.chevron_left),
                    label: const Text('Previous', style: TextStyle(fontWeight: FontWeight.w800)),
                  ),
                ),
                Padding(padding: const EdgeInsets.symmetric(horizontal: 10), child: Text('${pos + 1}/${list.length}', style: const TextStyle(fontWeight: FontWeight.w800))),
                Expanded(
                  child: FilledButton.icon(
                    onPressed: pos >= 0 && pos < list.length - 1 ? () => setState(() => _i = list[pos + 1]) : null,
                    style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(46), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                    icon: const Icon(Icons.chevron_right),
                    label: const Text('Next', style: TextStyle(fontWeight: FontWeight.w800)),
                  ),
                ),
              ]),
            ),
          ),
      ]),
    ));
  }
}


/// Open the solutions of a saved attempt (from the dashboard).
Future<void> openAttemptSolutions(BuildContext context, Exam exam, Map<String, dynamic> a) async {
  final mockId = '${a['mockId'] ?? ''}'.isNotEmpty ? '${a['mockId']}' : '${a['paperId'] ?? ''}';
  final lang = mockId.endsWith('_hi') ? 'hi' : 'en';
  final pd = '${a['partD'] ?? ''}';
  final nav = Navigator.of(context);
  final msg = ScaffoldMessenger.of(context);
  showDialog(context: context, barrierDismissible: false, builder: (_) => const Center(child: CircularProgressIndicator()));
  try {
    final p = await loadPaper(mockId, lang, partD: pd.isEmpty ? null : pd, title: '${a['examName'] ?? ''}');
    final pr = Progress();
    final byQ = <String, Map>{};
    for (final x in (a['answers'] as List? ?? const [])) {
      if (x is Map) byQ['${x['q']}'] = x;
    }
    for (var i = 0; i < p.questions.length; i++) {
      final x = byQ['${p.questions[i].qNumOr(i + 1)}'];
      if (x == null) continue;
      final ans = '${x['a'] ?? ''}';
      if (ans.isNotEmpty) pr.answers[i] = ans;
      final t = (x['t'] as num? ?? 0).toInt();
      if (t > 0) pr.qMs[i] = t * 1000;
    }
    nav.pop();
    nav.push(MaterialPageRoute(builder: (_) => SolutionsScreen(exam: exam, paper: p, progress: pr)));
  } catch (_) {
    nav.pop();
    msg.showSnackBar(const SnackBar(content: Text('Could not open the solutions. Check your internet and try again.')));
  }
}
