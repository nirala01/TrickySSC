import 'dart:async';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../data.dart';
import 'engine.dart';
import 'render.dart';
import 'result_screen.dart';

/// Loads a mock, shows the instructions, runs the test, then opens the result.
class TestFlow extends StatefulWidget {
  final User user;
  final Exam exam;
  final String mockId;
  final String lang;
  final String? partD;
  final bool paid;
  final String title;
  const TestFlow({super.key, required this.user, required this.exam, required this.mockId, required this.lang, this.partD, required this.paid, required this.title});

  @override
  State<TestFlow> createState() => _TestFlowState();
}

class _TestFlowState extends State<TestFlow> {
  Paper? _paper;
  Progress? _saved;
  String? _error;
  bool _starting = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _error = null);
    try {
      final p = await loadPaper(widget.mockId, widget.lang, partD: widget.partD);
      final s = await loadProgress(widget.user.uid, widget.mockId, p.partD);
      if (!mounted) return;
      setState(() {
        _paper = p;
        _saved = (s != null && s.remaining.length == p.units.length) ? s : null;
      });
    } catch (e) {
      if (mounted) setState(() => _error = e is String ? e : 'Could not load this mock. Check your internet and try again.');
    }
  }

  Future<void> _begin(bool resume) async {
    final p = _paper!;
    setState(() => _starting = true);
    if (!resume) {
      final limit = await dailyLimitReached(widget.user, widget.paid);
      if (!mounted) return;
      if (limit != null) {
        setState(() => _starting = false);
        await showDialog<void>(
          context: context,
          builder: (c) => AlertDialog(
            title: const Text('Daily test limit reached'),
            content: Text('${widget.paid ? 'Premium' : 'Free'} accounts can take up to $limit tests a day. Your limit resets at midnight.'),
            actions: [TextButton(onPressed: () => Navigator.pop(c), child: const Text('OK'))],
          ),
        );
        return;
      }
    }
    final pr = resume ? _saved! : (Progress()..remaining = List.filled(p.units.length, p.rules.unitSeconds));
    if (!resume) await clearProgress(widget.user.uid, widget.mockId, p.partD);
    if (!mounted) return;
    await Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => TestScreen(user: widget.user, exam: widget.exam, paper: p, progress: pr, lang: widget.lang, title: widget.title),
    ));
    if (mounted) Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final p = _paper;
    return Scaffold(
      backgroundColor: Color.lerp(Colors.white, exam.c2, 0.10),
      appBar: AppBar(title: Text(widget.title, style: const TextStyle(fontWeight: FontWeight.w800))),
      body: _error != null
          ? Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  const Icon(Icons.wifi_off, size: 44, color: Color(0xFF94A3B8)),
                  const SizedBox(height: 10),
                  Text(_error!, textAlign: TextAlign.center),
                  const SizedBox(height: 12),
                  FilledButton(onPressed: _load, child: const Text('Retry')),
                ]),
              ),
            )
          : p == null
              ? const Center(child: Column(mainAxisSize: MainAxisSize.min, children: [CircularProgressIndicator(), SizedBox(height: 12), Text('Loading the mock…')]))
              : _instructions(p),
    );
  }

  Widget _instructions(Paper p) {
    final exam = widget.exam;
    final mins = p.units.length * p.rules.unitSeconds ~/ 60;
    Widget fact(String v, String l) => Expanded(
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 10),
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
            child: Column(children: [
              Text(v, style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: exam.c1)),
              Text(l, style: const TextStyle(fontSize: 12, color: Color(0xFF64748B))),
            ]),
          ),
        );
    Widget line(IconData i, String t) => Padding(
          padding: const EdgeInsets.only(bottom: 10),
          child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Icon(i, size: 20, color: exam.c1),
            const SizedBox(width: 10),
            Expanded(child: Text(t, style: const TextStyle(fontSize: 14.5, height: 1.4))),
          ]),
        );
    return Column(children: [
      Expanded(
        child: ListView(padding: const EdgeInsets.all(14), children: [
          Row(children: [
            fact('${p.questions.length}', 'Questions'),
            const SizedBox(width: 8),
            fact('$mins', 'Minutes'),
            const SizedBox(width: 8),
            fact('${(p.questions.length * p.rules.pos).round()}', 'Marks'),
          ]),
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14)),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Text('Before you start', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
              const SizedBox(height: 10),
              line(Icons.timer_outlined, p.rules.timingLine(p.units.length)),
              line(Icons.calculate_outlined, p.rules.markingLine()),
              line(Icons.grid_view, 'Use the question palette to jump between questions of the open ${p.units.length > 1 ? (p.rules.mts ? 'session' : 'section') : 'paper'}.'),
              line(Icons.bookmark_outline, 'Mark a question for review to come back to it. A marked question that has an answer is counted.'),
              line(Icons.save_outlined, 'Your answers are saved on the phone as you go. If the app closes, you can resume.'),
              if (p.rules.gd && p.partD.isNotEmpty) line(Icons.translate, 'Part D (Q61–80) is in ${p.partD == 'hi' ? 'Hindi' : 'English'}.'),
            ]),
          ),
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14)),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(p.units.length > 1 ? (p.rules.mts ? 'Sessions' : 'Sections') : 'Paper', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
              const SizedBox(height: 8),
              for (final u in p.units)
                Padding(
                  padding: const EdgeInsets.only(bottom: 6),
                  child: Row(children: [
                    Expanded(child: Text(u.label, style: const TextStyle(fontWeight: FontWeight.w600))),
                    Text('Q${u.from + 1}–${u.to + 1} · ${p.rules.unitSeconds ~/ 60} min', style: const TextStyle(color: Color(0xFF64748B))),
                  ]),
                ),
            ]),
          ),
        ]),
      ),
      SafeArea(
        top: false,
        child: Padding(
          padding: const EdgeInsets.fromLTRB(14, 6, 14, 12),
          child: Row(children: [
            if (_saved != null) ...[
              Expanded(
                child: OutlinedButton(
                  onPressed: _starting ? null : () => _begin(false),
                  style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                  child: const Text('Start again', style: TextStyle(fontWeight: FontWeight.w800)),
                ),
              ),
              const SizedBox(width: 10),
            ],
            Expanded(
              child: FilledButton(
                onPressed: _starting ? null : () => _begin(_saved != null),
                style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                child: _starting
                    ? const SizedBox(width: 22, height: 22, child: CircularProgressIndicator(strokeWidth: 2.5, color: Colors.white))
                    : Text(_saved != null ? 'Resume test' : 'I am ready to begin', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
              ),
            ),
          ]),
        ),
      ),
    ]);
  }
}

// ======================================================================== test

class TestScreen extends StatefulWidget {
  final User user;
  final Exam exam;
  final Paper paper;
  final Progress progress;
  final String lang;
  final String title;
  const TestScreen({super.key, required this.user, required this.exam, required this.paper, required this.progress, required this.lang, required this.title});

  @override
  State<TestScreen> createState() => _TestScreenState();
}

class _TestScreenState extends State<TestScreen> with WidgetsBindingObserver {
  late Progress pr;
  Timer? _timer;
  bool _paused = false;
  bool _submitting = false;
  DateTime _qStart = DateTime.now();
  int _tick = 0;
  bool _showEn = false;
  Map<int, Question>? _en;
  bool _enLoading = false;
  final _scroll = ScrollController();

  Paper get p => widget.paper;
  Unit get unit => p.units[pr.unit];
  Question get q => p.questions[pr.current];

  @override
  void initState() {
    super.initState();
    pr = widget.progress;
    if (pr.current < unit.from || pr.current > unit.to) pr.current = unit.from;
    pr.visited.add(pr.current);
    WidgetsBinding.instance.addObserver(this);
    _start();
  }

  @override
  void dispose() {
    _timer?.cancel();
    WidgetsBinding.instance.removeObserver(this);
    _scroll.dispose();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState s) {
    if (s == AppLifecycleState.paused || s == AppLifecycleState.inactive) {
      _logTime();
      _persist();
    }
  }

  void _start() {
    _timer?.cancel();
    _qStart = DateTime.now();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (_paused || _submitting) return;
      setState(() => pr.remaining[pr.unit] = (pr.remaining[pr.unit] - 1).clamp(0, 1 << 30));
      if (++_tick % 10 == 0) _persist();
      if (pr.remaining[pr.unit] <= 0) _unitTimeUp();
    });
  }

  void _logTime() {
    final now = DateTime.now();
    if (!_paused) pr.qMs[pr.current] = (pr.qMs[pr.current] ?? 0) + now.difference(_qStart).inMilliseconds;
    _qStart = now;
  }

  void _persist() => saveProgress(widget.user.uid, p.rules.mockId, p.partD, pr);

  void _go(int i) {
    if (i < unit.from || i > unit.to) return;
    _logTime();
    setState(() {
      pr.current = i;
      pr.visited.add(i);
      _showEn = false;
    });
    if (_scroll.hasClients) _scroll.jumpTo(0);
    _persist();
  }

  void _pick(String k) {
    setState(() => pr.answers[pr.current] = k);
    _persist();
  }

  void _clear() {
    setState(() => pr.answers.remove(pr.current));
    _persist();
  }

  void _next() {
    if (pr.current < unit.to) {
      _go(pr.current + 1);
    } else {
      _openPalette();
    }
  }

  void _markNext() {
    setState(() {
      if (pr.marked.contains(pr.current)) {
        pr.marked.remove(pr.current);
      } else {
        pr.marked.add(pr.current);
      }
    });
    if (pr.marked.contains(pr.current)) _next();
    _persist();
  }

  void _togglePause() {
    _logTime();
    setState(() => _paused = !_paused);
    _qStart = DateTime.now();
  }

  String get _unitWord => p.rules.ntpc ? 'test' : (p.rules.mts ? 'session' : 'section');
  bool get _lastUnit => pr.unit >= p.units.length - 1;

  void _unitTimeUp() {
    if (_lastUnit) {
      _submit();
    } else {
      _advance();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Time up. ${p.units[pr.unit].label} is open now.')));
      }
    }
  }

  void _advance() {
    _logTime();
    setState(() {
      pr.remaining[pr.unit] = 0;
      pr.unit++;
      pr.current = unit.from;
      pr.visited.add(pr.current);
      _showEn = false;
    });
    _persist();
  }

  Future<void> _confirmSubmitUnit() async {
    final answered = [for (var i = unit.from; i <= unit.to; i++) if (pr.answers[i] != null) i].length;
    final total = unit.to - unit.from + 1;
    final ok = await showDialog<bool>(
      context: context,
      builder: (c) => AlertDialog(
        title: Text(_lastUnit ? 'Submit the test?' : 'Submit ${unit.label}?'),
        content: Text(_lastUnit
            ? 'You answered $answered of $total questions here. This ends the test and you cannot change any answers.'
            : 'You answered $answered of $total questions. You cannot return to this $_unitWord, and its remaining time will be lost.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(c, false), child: const Text('Keep going')),
          FilledButton(onPressed: () => Navigator.pop(c, true), child: Text(_lastUnit ? 'Submit test' : 'Submit $_unitWord')),
        ],
      ),
    );
    if (ok == true) {
      if (_lastUnit) {
        _submit();
      } else {
        _advance();
      }
    }
  }

  Future<void> _submit() async {
    if (_submitting) return;
    _logTime();
    setState(() => _submitting = true);
    _timer?.cancel();
    final r = scorePaper(p, pr);
    if (!mounted) return;
    await Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => ResultScreen(user: widget.user, exam: widget.exam, paper: p, progress: pr, result: r, title: widget.title),
    ));
    if (mounted) Navigator.of(context).pop();
  }

  Future<bool> _confirmLeave() async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('Leave the test?'),
        content: const Text('Your answers and time are saved. You can resume this mock from the mock list.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(c, false), child: const Text('Stay')),
          FilledButton(onPressed: () => Navigator.pop(c, true), child: const Text('Leave')),
        ],
      ),
    );
    if (ok == true) {
      _logTime();
      _persist();
    }
    return ok == true;
  }

  Future<void> _toggleEnglish() async {
    if (_showEn) {
      setState(() => _showEn = false);
      return;
    }
    if (_en == null) {
      setState(() => _enLoading = true);
      _en = await loadEnglishTwin(p.rules.mockId);
      if (!mounted) return;
      setState(() => _enLoading = false);
    }
    if ((_en ?? const {})[q.qNumOr(pr.current + 1)] == null) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('No English version of this question.')));
      return;
    }
    setState(() => _showEn = true);
  }

  // colours of the palette states
  static const _answered = Color(0xFF16A34A);
  static const _notAnswered = Color(0xFFDC2626);
  static const _markedC = Color(0xFF7C3AED);

  Color _stateColor(int i) {
    final a = pr.answers[i] != null, m = pr.marked.contains(i);
    if (m) return _markedC;
    if (a) return _answered;
    if (pr.visited.contains(i)) return _notAnswered;
    return const Color(0xFFE2E8F0);
  }

  void _openPalette() {
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (c) => StatefulBuilder(builder: (c, set) {
        final secs = p.sections.where((s) => s.from >= unit.from && s.to <= unit.to).toList();
        int count(bool Function(int) f) => [for (var i = unit.from; i <= unit.to; i++) if (f(i)) i].length;
        Widget legend(Color col, String t, int n) => Row(mainAxisSize: MainAxisSize.min, children: [
              Container(width: 14, height: 14, decoration: BoxDecoration(color: col, borderRadius: BorderRadius.circular(4))),
              const SizedBox(width: 5),
              Text('$t $n', style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.w600)),
            ]);
        return SafeArea(
          child: ConstrainedBox(
            constraints: BoxConstraints(maxHeight: MediaQuery.of(c).size.height * 0.8),
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
              child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                Center(child: Container(width: 40, height: 4, decoration: BoxDecoration(color: const Color(0xFFCBD5E1), borderRadius: BorderRadius.circular(4)))),
                const SizedBox(height: 10),
                Text(unit.label, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
                const SizedBox(height: 8),
                Wrap(spacing: 12, runSpacing: 6, children: [
                  legend(_answered, 'Answered', count((i) => pr.answers[i] != null && !pr.marked.contains(i))),
                  legend(_notAnswered, 'Not answered', count((i) => pr.answers[i] == null && pr.visited.contains(i) && !pr.marked.contains(i))),
                  legend(_markedC, 'Marked', count((i) => pr.marked.contains(i))),
                  legend(const Color(0xFFE2E8F0), 'Not visited', count((i) => !pr.visited.contains(i))),
                ]),
                const SizedBox(height: 10),
                Flexible(
                  child: SingleChildScrollView(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      for (final s in secs) ...[
                        if (secs.length > 1) Padding(padding: const EdgeInsets.only(top: 6, bottom: 6), child: Text(s.label, style: const TextStyle(fontWeight: FontWeight.w800, color: Color(0xFF475569)))),
                        Wrap(spacing: 8, runSpacing: 8, children: [
                          for (var i = s.from; i <= s.to; i++)
                            InkWell(
                              borderRadius: BorderRadius.circular(10),
                              onTap: () {
                                Navigator.pop(c);
                                _go(i);
                              },
                              child: Container(
                                width: 44,
                                height: 44,
                                alignment: Alignment.center,
                                decoration: BoxDecoration(
                                  color: _stateColor(i),
                                  borderRadius: BorderRadius.circular(10),
                                  border: i == pr.current ? Border.all(color: const Color(0xFF0F172A), width: 2.5) : null,
                                ),
                                child: Stack(clipBehavior: Clip.none, children: [
                                  Text('${i + 1}', style: TextStyle(fontWeight: FontWeight.w800, color: _stateColor(i) == const Color(0xFFE2E8F0) ? const Color(0xFF334155) : Colors.white)),
                                  if (pr.marked.contains(i) && pr.answers[i] != null)
                                    const Positioned(right: -10, top: -10, child: CircleAvatar(radius: 6, backgroundColor: _answered)),
                                ]),
                              ),
                            ),
                        ]),
                      ],
                    ]),
                  ),
                ),
                const SizedBox(height: 12),
                FilledButton(
                  onPressed: () {
                    Navigator.pop(c);
                    _confirmSubmitUnit();
                  },
                  style: FilledButton.styleFrom(backgroundColor: widget.exam.c1, minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                  child: Text(_lastUnit ? 'Submit test' : 'Submit ${unit.label}', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
                ),
              ]),
            ),
          ),
        );
      }),
    );
  }

  String _clock(int s) => '${(s ~/ 60).toString().padLeft(2, '0')}:${(s % 60).toString().padLeft(2, '0')}';

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final secs = p.sections.where((s) => s.from >= unit.from && s.to <= unit.to).toList();
    final shown = _showEn ? (_en?[q.qNumOr(pr.current + 1)] ?? q) : q;
    final left = pr.remaining[pr.unit];
    final neg = p.rules.neg(q, pr.current);
    final low = left <= 60;
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) async {
        if (didPop) return;
        if (await _confirmLeave() && context.mounted) Navigator.of(context).pop();
      },
      child: Scaffold(
        backgroundColor: Color.lerp(Colors.white, exam.c2, 0.08),
        appBar: AppBar(
          titleSpacing: 0,
          toolbarHeight: 54,
          title: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(widget.title, style: const TextStyle(fontSize: 15.5, fontWeight: FontWeight.w800)),
            Text(unit.label, style: TextStyle(fontSize: 12, color: exam.c1, fontWeight: FontWeight.w700)),
          ]),
          actions: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              decoration: BoxDecoration(color: low ? const Color(0xFFFEE2E2) : const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(10)),
              child: Row(children: [
                Icon(Icons.timer_outlined, size: 18, color: low ? const Color(0xFFDC2626) : const Color(0xFF334155)),
                const SizedBox(width: 4),
                Text(_clock(left), style: TextStyle(fontWeight: FontWeight.w800, fontSize: 15, fontFeatures: const [FontFeature.tabularFigures()], color: low ? const Color(0xFFDC2626) : const Color(0xFF0F172A))),
              ]),
            ),
            IconButton(onPressed: _togglePause, icon: Icon(_paused ? Icons.play_arrow : Icons.pause), tooltip: _paused ? 'Resume' : 'Pause'),
            IconButton(onPressed: _openPalette, icon: const Icon(Icons.grid_view_rounded), tooltip: 'Question palette'),
          ],
        ),
        body: _paused
            ? Center(
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  Icon(Icons.pause_circle_outline, size: 64, color: exam.c1),
                  const SizedBox(height: 10),
                  const Text('Test paused', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800)),
                  Text('${_clock(left)} left in ${unit.label}', style: const TextStyle(color: Color(0xFF64748B))),
                  const SizedBox(height: 14),
                  FilledButton.icon(onPressed: _togglePause, style: FilledButton.styleFrom(backgroundColor: exam.c1), icon: const Icon(Icons.play_arrow), label: const Text('Resume')),
                ]),
              )
            : Column(children: [
                if (secs.length > 1)
                  SizedBox(
                    height: 44,
                    child: ListView(
                      scrollDirection: Axis.horizontal,
                      padding: const EdgeInsets.fromLTRB(10, 6, 10, 2),
                      children: [
                        for (final s in secs)
                          Padding(
                            padding: const EdgeInsets.only(right: 8),
                            child: ChoiceChip(
                              label: Text(s.label),
                              selected: pr.current >= s.from && pr.current <= s.to,
                              onSelected: (_) => _go(s.from),
                              selectedColor: Color.lerp(Colors.white, exam.c2, 0.4),
                              visualDensity: VisualDensity.compact,
                            ),
                          ),
                      ],
                    ),
                  ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(14, 8, 10, 4),
                  child: Row(children: [
                    Text('Q ${pr.current + 1}', style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
                    Text(' / ${p.questions.length}', style: const TextStyle(color: Color(0xFF64748B))),
                    const SizedBox(width: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 3),
                      decoration: BoxDecoration(color: const Color(0xFFD1FAE5), borderRadius: BorderRadius.circular(8)),
                      child: Text('+${_n(p.rules.pos)}', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w800, color: Color(0xFF047857))),
                    ),
                    const SizedBox(width: 4),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 3),
                      decoration: BoxDecoration(color: const Color(0xFFFEE2E2), borderRadius: BorderRadius.circular(8)),
                      child: Text(neg == 0 ? '0' : '−${neg == 1 / 3 ? '1/3' : _n(neg)}', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w800, color: Color(0xFFB91C1C))),
                    ),
                    const Spacer(),
                    if (widget.lang == 'hi')
                      TextButton(
                        onPressed: _enLoading ? null : _toggleEnglish,
                        child: _enLoading
                            ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                            : Text(_showEn ? 'हिंदी में देखें' : 'View in English', style: const TextStyle(fontWeight: FontWeight.w700)),
                      ),
                  ]),
                ),
                Expanded(
                  child: ListView(
                    controller: _scroll,
                    padding: const EdgeInsets.fromLTRB(14, 0, 14, 12),
                    children: [
                      Rich(questionHtml(shown.text), size: 16.5),
                      if (shown.imageUrl.isNotEmpty) Figure(shown.imageUrl),
                      const SizedBox(height: 8),
                      for (final k in q.keys) _option(k, shown),
                    ],
                  ),
                ),
                SafeArea(
                  top: false,
                  child: Container(
                    padding: const EdgeInsets.fromLTRB(10, 8, 10, 8),
                    color: Colors.white,
                    child: Row(children: [
                      IconButton.filledTonal(onPressed: pr.current > unit.from ? () => _go(pr.current - 1) : null, icon: const Icon(Icons.chevron_left), tooltip: 'Previous'),
                      const SizedBox(width: 6),
                      Expanded(
                        child: OutlinedButton(
                          onPressed: _markNext,
                          style: OutlinedButton.styleFrom(minimumSize: const Size.fromHeight(46), foregroundColor: _markedC, side: const BorderSide(color: _markedC), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                          child: Text(pr.marked.contains(pr.current) ? 'Unmark' : 'Mark & next', style: const TextStyle(fontWeight: FontWeight.w800)),
                        ),
                      ),
                      const SizedBox(width: 6),
                      TextButton(onPressed: pr.answers[pr.current] == null ? null : _clear, child: const Text('Clear')),
                      const SizedBox(width: 6),
                      Expanded(
                        child: FilledButton(
                          onPressed: _next,
                          style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(46), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                          child: Text(pr.current < unit.to ? 'Save & next' : (_lastUnit ? 'Review & submit' : 'Review'), style: const TextStyle(fontWeight: FontWeight.w800)),
                        ),
                      ),
                    ]),
                  ),
                ),
              ]),
      ),
    );
  }

  String _n(double v) => v == v.roundToDouble() ? '${v.round()}' : v.toStringAsFixed(2).replaceFirst(RegExp(r'0+$'), '');

  Widget _option(String k, Question shown) {
    final sel = pr.answers[pr.current] == k;
    final exam = widget.exam;
    final txt = stripFigRef(shown.option(k));
    final img = shown.optionImage(k).isNotEmpty ? shown.optionImage(k) : q.optionImage(k);
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Material(
        color: sel ? Color.lerp(Colors.white, exam.c2, 0.22) : Colors.white,
        borderRadius: BorderRadius.circular(14),
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: () => _pick(k),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
            decoration: BoxDecoration(borderRadius: BorderRadius.circular(14), border: Border.all(color: sel ? exam.c1 : const Color(0xFFE2E8F0), width: sel ? 2 : 1)),
            child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Container(
                width: 30,
                height: 30,
                alignment: Alignment.center,
                decoration: BoxDecoration(shape: BoxShape.circle, color: sel ? exam.c1 : const Color(0xFFF1F5F9)),
                child: Text(k, style: TextStyle(fontWeight: FontWeight.w800, color: sel ? Colors.white : const Color(0xFF334155))),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.only(top: 4),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    if (txt.isNotEmpty) Rich(contentHtml(txt), size: 15.5),
                    if (img.isNotEmpty) Figure(img, maxHeight: txt.isEmpty ? 170 : 100),
                  ]),
                ),
              ),
            ]),
          ),
        ),
      ),
    );
  }
}
