import 'dart:async';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import '../ui/nav.dart';

import '../data.dart';
import 'engine.dart';
import 'render.dart';
import 'report.dart';
import '../ui/soft.dart';
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
  final Future<Paper> Function()? loader; // chapter tests load their own paper
  const TestFlow({super.key, required this.user, required this.exam, required this.mockId, required this.lang, this.partD, required this.paid, required this.title, this.loader});

  @override
  State<TestFlow> createState() => _TestFlowState();
}

class _TestFlowState extends State<TestFlow> {
  Paper? _paper;
  Progress? _saved;
  String? _error;
  bool _starting = false;
  bool _timed = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _error = null);
    try {
      final p = widget.loader != null ? await widget.loader!() : await loadPaper(widget.mockId, widget.lang, partD: widget.partD, title: isPyqId(widget.mockId) ? widget.title : '');
      final s = await loadProgress(widget.user.uid, widget.mockId, p.partD);
      if (!mounted) return;
      setState(() {
        _paper = p;
        _saved = (s != null && s.remaining.length == p.units.length) ? s : null;
      });
    } catch (e) {
      if (mounted) setState(() => _error = e is String ? e : 'Could not load this test. Check your internet and try again.');
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
    final pr = resume
        ? _saved!
        : (Progress()
          ..remaining = [for (var i = 0; i < p.units.length; i++) p.unitSecs(i)]
          ..untimed = p.chapter != null && !_timed);
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
      backgroundColor: const Color(0xFFEEF2FF),
      appBar: AppBar(actions: const [HomeButton()], title: Text(widget.title, style: const TextStyle(fontWeight: FontWeight.w800))),
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
              ? const Center(child: Column(mainAxisSize: MainAxisSize.min, children: [CircularProgressIndicator(), SizedBox(height: 12), Text('Loading the test…')]))
              : _instructions(p),
    );
  }

  Widget _instructions(Paper p) {
    final exam = widget.exam;
    final mins = p.totalSecs ~/ 60;
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
          if (p.chapter != null && _saved == null) ...[
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14)),
              child: Row(children: [
                for (final t in const [(true, 'Timed · 15 min'), (false, 'Untimed practice')])
                  Expanded(
                    child: Material(
                      color: _timed == t.$1 ? exam.c1 : Colors.transparent,
                      borderRadius: BorderRadius.circular(10),
                      child: InkWell(
                        borderRadius: BorderRadius.circular(10),
                        onTap: () => setState(() => _timed = t.$1),
                        child: Container(
                          height: 44,
                          alignment: Alignment.center,
                          child: Text(t.$2, style: TextStyle(fontWeight: FontWeight.w800, color: _timed == t.$1 ? Colors.white : const Color(0xFF334155))),
                        ),
                      ),
                    ),
                  ),
              ]),
            ),
          ],
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
                    Text('Q${u.from + 1}–${u.to + 1} · ${(u.seconds > 0 ? u.seconds : p.rules.unitSeconds) ~/ 60} min', style: const TextStyle(color: Color(0xFF64748B))),
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
      if (pr.untimed) {
        if (++_tick % 10 == 0) _persist();
        return;
      }
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

  void _persist() {
    if (_submitting) return;
    saveProgress(widget.user.uid, p.rules.mockId, p.partD, pr);
  }

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
      _en = p.chapter != null ? p.chapter!.en : await loadEnglishTwin(p.rules.mockId);
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
    final low = !pr.untimed && left <= 60;
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) async {
        if (didPop) return;
        if (await _confirmLeave() && context.mounted) Navigator.of(context).pop();
      },
      child: Container(
        decoration: softBg,
        child: Scaffold(
          backgroundColor: Colors.transparent,
          appBar: AppBar(
            backgroundColor: Colors.transparent,
            surfaceTintColor: Colors.transparent,
            scrolledUnderElevation: 0,
            automaticallyImplyLeading: false,
            toolbarHeight: 66,
            titleSpacing: 12,
            title: Row(children: [
              _sbtn(Icons.chevron_left_rounded, () => Navigator.of(context).maybePop(), 'Leave'),
              const SizedBox(width: 10),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(widget.title, maxLines: 1, overflow: TextOverflow.ellipsis, style: baloo(17.5)),
                  Text(_subtitle, maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(fontSize: 12.5, color: exam.c1, fontWeight: FontWeight.w800)),
                ]),
              ),
            ]),
            actions: [
              Container(
                height: 40,
                padding: const EdgeInsets.symmetric(horizontal: 10),
                decoration: softCard(radius: 14).copyWith(color: low ? const Color(0xFFFEE2E2) : Colors.white),
                child: Row(children: [
                  Icon(Icons.timer_outlined, size: 18, color: low ? const Color(0xFFDC2626) : exam.c1),
                  const SizedBox(width: 4),
                  Text(pr.untimed ? 'Untimed' : _clock(left),
                      style: TextStyle(fontWeight: FontWeight.w900, fontSize: 15, fontFeatures: const [FontFeature.tabularFigures()], color: low ? const Color(0xFFDC2626) : softInk)),
                ]),
              ),
              const SizedBox(width: 6),
              _sbtn(_paused ? Icons.play_arrow_rounded : Icons.pause_rounded, _togglePause, _paused ? 'Resume' : 'Pause'),
              const SizedBox(width: 6),
              _sbtn(Icons.home_rounded, () async {
                if (await _confirmLeave() && context.mounted) goHome(context);
              }, 'Home'),
              const SizedBox(width: 12),
            ],
          ),
          body: _paused
              ? Center(
                  child: Container(
                    margin: const EdgeInsets.all(24),
                    padding: const EdgeInsets.all(24),
                    decoration: softCard(radius: 24),
                    child: Column(mainAxisSize: MainAxisSize.min, children: [
                      Icon(Icons.pause_circle_filled_rounded, size: 64, color: exam.c1),
                      const SizedBox(height: 10),
                      Text('Test paused', style: baloo(22)),
                      Text(pr.untimed ? 'Untimed practice' : '${_clock(left)} left in ${unit.label}', style: const TextStyle(color: softMuted, fontWeight: FontWeight.w600)),
                      const SizedBox(height: 14),
                      FilledButton.icon(onPressed: _togglePause, style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size(160, 48)), icon: const Icon(Icons.play_arrow_rounded), label: const Text('Resume', style: TextStyle(fontWeight: FontWeight.w800))),
                    ]),
                  ),
                )
              : Column(children: [
                  if (p.sections.length > 1) _sectionStrip(),
                  Expanded(
                    child: ListView(
                      controller: _scroll,
                      padding: const EdgeInsets.fromLTRB(14, 10, 14, 16),
                      children: [
                        Container(
                          padding: const EdgeInsets.fromLTRB(16, 14, 16, 8),
                          decoration: softCard(radius: 24, glow: exam.c1),
                          child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                            Row(children: [
                              Text('Q ${pr.current + 1}', style: baloo(21)),
                              Text('  / ${p.questions.length}', style: const TextStyle(color: Color(0xFF8B8FB3), fontWeight: FontWeight.w800)),
                              const Spacer(),
                              if (widget.lang == 'hi')
                                TextButton(
                                  onPressed: _enLoading ? null : _toggleEnglish,
                                  style: TextButton.styleFrom(visualDensity: VisualDensity.compact, foregroundColor: exam.c1),
                                  child: _enLoading
                                      ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                                      : Text(_showEn ? 'हिंदी' : 'English', style: const TextStyle(fontWeight: FontWeight.w800)),
                                ),
                              _pill('+${_n(p.rules.pos)}', const Color(0xFF047857), const Color(0xFFD1FAE5)),
                              const SizedBox(width: 5),
                              _pill(neg == 0 ? '0' : '−${neg == 1 / 3 ? '1/3' : _n(neg)}', const Color(0xFFB91C1C), const Color(0xFFFEE2E2)),
                            ]),
                            if ('${q.raw['_src'] ?? ''}'.isNotEmpty)
                              Padding(
                                padding: const EdgeInsets.only(top: 6),
                                child: Text('📌 Asked in ${q.raw['_src']}${q.raw['_srcQ'] != null ? ' · Q${q.raw['_srcQ']}' : ''}',
                                    style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w700, color: widget.exam.c1)),
                              ),
                            const SizedBox(height: 8),
                            Rich(questionHtml(shown.text), size: 16.5, weight: FontWeight.w600),
                            if (shown.imageUrl.isNotEmpty) Figure(shown.imageUrl),
                            const SizedBox(height: 12),
                            if (_imageOnly(shown))
                              _optionGrid(shown)
                            else
                              for (final k in q.keys) _option(k, shown),
                            Row(children: [
                              if (pr.answers[pr.current] != null)
                                TextButton.icon(
                                  onPressed: _clear,
                                  style: TextButton.styleFrom(foregroundColor: softMuted, visualDensity: VisualDensity.compact),
                                  icon: const Icon(Icons.backspace_outlined, size: 16),
                                  label: const Text('Clear', style: TextStyle(fontWeight: FontWeight.w700)),
                                ),
                              Expanded(child: ReportLink('Report a problem', () => showReport(context, exam: widget.exam, paper: p, index: pr.current, target: 'question'))),
                            ]),
                          ]),
                        ),
                      ],
                    ),
                  ),
                  Container(
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
                      boxShadow: [BoxShadow(color: const Color(0xFF6366F1).withValues(alpha: .10), blurRadius: 24, offset: const Offset(0, -8))],
                    ),
                    child: SafeArea(
                      top: false,
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(12, 12, 12, 10),
                        child: Row(children: [
                          _square(Icons.chevron_left_rounded, pr.current > unit.from ? () => _go(pr.current - 1) : null, 'Previous'),
                          const SizedBox(width: 8),
                          Expanded(
                            flex: 5,
                            child: OutlinedButton(
                              onPressed: _markNext,
                              style: OutlinedButton.styleFrom(
                                minimumSize: const Size.fromHeight(48),
                                padding: const EdgeInsets.symmetric(horizontal: 6),
                                foregroundColor: _markedC,
                                side: const BorderSide(color: Color(0xFFA78BFA), width: 2),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                              ),
                              child: FittedBox(fit: BoxFit.scaleDown, child: Text(pr.marked.contains(pr.current) ? 'Unmark' : 'Mark & next', maxLines: 1, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 14.5))),
                            ),
                          ),
                          const SizedBox(width: 8),
                          _square(Icons.grid_view_rounded, _openPalette, 'Question palette'),
                          const SizedBox(width: 8),
                          Expanded(
                            flex: 6,
                            child: Material(
                              color: Colors.transparent,
                              child: Ink(
                                height: 48,
                                decoration: BoxDecoration(
                                  borderRadius: BorderRadius.circular(15),
                                  gradient: LinearGradient(colors: [Color.lerp(exam.c1, Colors.white, .25)!, exam.c1], begin: Alignment.topCenter, end: Alignment.bottomCenter),
                                  boxShadow: [BoxShadow(color: exam.c1.withValues(alpha: .30), blurRadius: 14, offset: const Offset(0, 6))],
                                ),
                                child: InkWell(
                                  borderRadius: BorderRadius.circular(15),
                                  onTap: _next,
                                  child: Center(
                                    child: FittedBox(fit: BoxFit.scaleDown, child: Text(pr.current < unit.to ? 'Save & next' : (_lastUnit ? 'Submit' : 'Review'),
                                        maxLines: 1, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 15))),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ]),
                      ),
                    ),
                  ),
                ]),
        ),
      ),
    );
  }

  String get _subtitle {
    String sec = unit.label;
    for (final s in p.sections) {
      if (pr.current >= s.from && pr.current <= s.to) sec = s.label;
    }
    if (p.units.length > 1) {
      final w = _unitWord;
      sec += ' · ${w[0].toUpperCase()}${w.substring(1)} ${pr.unit + 1} of ${p.units.length}';
    }
    return sec;
  }

  Widget _sbtn(IconData icon, VoidCallback? onTap, String tip) => Tooltip(
        message: tip,
        child: Material(
          color: Colors.transparent,
          child: Ink(
            decoration: softCard(radius: 14),
            child: InkWell(
              borderRadius: BorderRadius.circular(14),
              onTap: onTap,
              child: SizedBox(width: 40, height: 40, child: Icon(icon, color: widget.exam.c1, size: 24)),
            ),
          ),
        ),
      );

  Widget _square(IconData icon, VoidCallback? onTap, String tip) => Tooltip(
        message: tip,
        child: Material(
          color: Color.lerp(Colors.white, widget.exam.c1, onTap == null ? .05 : .12),
          borderRadius: BorderRadius.circular(15),
          child: InkWell(
            borderRadius: BorderRadius.circular(15),
            onTap: onTap,
            child: SizedBox(width: 48, height: 48, child: Icon(icon, color: onTap == null ? const Color(0xFFCBD5E1) : widget.exam.c1, size: 24)),
          ),
        ),
      );

  Widget _pill(String t, Color fg, Color bg) => Container(
        padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 3),
        decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(999)),
        child: Text(t, style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w900, color: fg)),
      );

  Widget _sectionStrip() {
    final c1 = widget.exam.c1;
    return Padding(
      padding: const EdgeInsets.fromLTRB(14, 2, 14, 0),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        for (var i = 0; i < p.sections.length; i++)
          Builder(builder: (_) {
            final s = p.sections[i];
            final on = pr.current >= s.from && pr.current <= s.to;
            final inUnit = s.from >= unit.from && s.to <= unit.to;
            final done = s.to < unit.from;
            final bar = on ? null : (done ? Color.lerp(Colors.white, c1, .45) : (inUnit ? Color.lerp(Colors.white, c1, .28) : Color.lerp(Colors.white, c1, .10)));
            return Expanded(
              child: GestureDetector(
                onTap: inUnit && !on ? () => _go(s.from) : null,
                child: Padding(
                  padding: EdgeInsets.only(right: i == p.sections.length - 1 ? 0 : 6),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Container(
                      height: 6,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(6),
                        color: bar,
                        gradient: on ? LinearGradient(colors: [Color.lerp(c1, Colors.white, .3)!, c1]) : null,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(s.label, maxLines: 1, overflow: TextOverflow.ellipsis,
                        style: TextStyle(fontSize: 11.5, fontWeight: FontWeight.w800, color: on ? c1 : (inUnit ? softMuted : const Color(0xFFA5A8C8)))),
                  ]),
                ),
              ),
            );
          }),
      ]),
    );
  }

  String _n(double v) => v == v.roundToDouble() ? '${v.round()}' : v.toStringAsFixed(2).replaceFirst(RegExp(r'0+$'), '');

  String _img(String k, Question shown) => shown.optionImage(k).isNotEmpty ? shown.optionImage(k) : q.optionImage(k);

  bool _imageOnly(Question shown) => q.keys.every((k) => stripFigRef(shown.option(k)).isEmpty && _img(k, shown).isNotEmpty);

  Widget _optionGrid(Question shown) {
    final exam = widget.exam;
    final keys = q.keys;
    Widget tile(String k) {
      final sel = pr.answers[pr.current] == k;
      return Expanded(
        child: Material(
          color: sel ? Color.lerp(Colors.white, exam.c1, 0.10) : const Color(0xFFF8FAFF),
          borderRadius: BorderRadius.circular(18),
          child: InkWell(
            borderRadius: BorderRadius.circular(18),
            onTap: () => _pick(k),
            child: Container(
              padding: const EdgeInsets.fromLTRB(8, 8, 8, 4),
              decoration: BoxDecoration(borderRadius: BorderRadius.circular(18), border: Border.all(color: sel ? exam.c1 : Colors.transparent, width: 2)),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                _letter(k, sel),
                SizedBox(height: 124, child: Center(child: Figure(_img(k, shown), maxHeight: 112, tapZoom: false))),
              ]),
            ),
          ),
        ),
      );
    }

    final rows = <Widget>[];
    for (var i = 0; i < keys.length; i += 2) {
      rows.add(Padding(
        padding: const EdgeInsets.only(bottom: 8),
        child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
          tile(keys[i]),
          const SizedBox(width: 8),
          if (i + 1 < keys.length) tile(keys[i + 1]) else const Expanded(child: SizedBox()),
        ]),
      ));
    }
    return Column(children: rows);
  }

  Widget _option(String k, Question shown) {
    final sel = pr.answers[pr.current] == k;
    final c1 = widget.exam.c1;
    final txt = stripFigRef(shown.option(k));
    final img = _img(k, shown);
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Material(
        color: Colors.transparent,
        child: Ink(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(18),
            color: sel ? null : const Color(0xFFF8FAFF),
            gradient: sel ? LinearGradient(colors: [Color.lerp(Colors.white, c1, .06)!, Color.lerp(Colors.white, c1, .14)!], begin: Alignment.topCenter, end: Alignment.bottomCenter) : null,
            border: Border.all(color: sel ? c1 : Colors.transparent, width: 2),
          ),
          child: InkWell(
            borderRadius: BorderRadius.circular(18),
            onTap: () => _pick(k),
            child: Padding(
              padding: const EdgeInsets.all(11),
              child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                _letter(k, sel),
                const SizedBox(width: 12),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.only(top: 5),
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      if (txt.isNotEmpty) Rich(contentHtml(txt), size: 16, weight: FontWeight.w600),
                      if (img.isNotEmpty) Figure(img, maxHeight: txt.isEmpty ? 130 : 100, tapZoom: false),
                    ]),
                  ),
                ),
              ]),
            ),
          ),
        ),
      ),
    );
  }

  Widget _letter(String k, bool sel) {
    final c1 = widget.exam.c1;
    return Container(
      width: 34,
      height: 34,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        color: sel ? null : Colors.white,
        gradient: sel ? LinearGradient(colors: [Color.lerp(c1, Colors.white, .25)!, c1], begin: Alignment.topCenter, end: Alignment.bottomCenter) : null,
        boxShadow: [BoxShadow(color: (sel ? c1 : const Color(0xFF6366F1)).withValues(alpha: sel ? .35 : .12), blurRadius: sel ? 10 : 6, offset: const Offset(0, 3))],
      ),
      child: Text(k, style: TextStyle(fontWeight: FontWeight.w900, fontSize: 15, color: sel ? Colors.white : c1)),
    );
  }
}
