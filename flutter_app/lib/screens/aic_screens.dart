// SSC CGL Tier-2 All India Challenge Mock: the Home banner, the Challenge screen, the "submitted" screen
// and the small notes. The rules live in ../aic.dart, the reads and writes in ../aic_io.dart.
import 'dart:async';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../aic.dart';
import '../aic_io.dart';
import '../data.dart';
import '../test/engine.dart';
import '../test/test_screen.dart';
import '../ui/soft.dart';
import 'dash/analysis.dart';
import 'dash/logic.dart';
import 'dash/pages.dart';
import 'dash/ui.dart';

Exam _examOf(AicSeries se, Exam fallback) => examById(se.exam) ?? fallback;

String _commas(int v) => v.toString().replaceAllMapped(RegExp(r'(\d)(?=(\d{3})+$)'), (m) => '${m[1]},');

/// Starts (or resumes) a challenge paper: the live Sunday attempt, or the free mock after the result.
Future<void> startAic(BuildContext context, User user, Exam exam, AicSeries se, int n, {required bool live, String? lang}) async {
  // a paper already started on this phone keeps its language
  for (final l in const ['en', 'hi']) {
    if (await loadProgress(user.uid, se.mockId(n, l), '') != null) lang = l;
  }
  if (!context.mounted) return;
  lang ??= await showModalBottomSheet<String>(
    context: context,
    backgroundColor: Colors.white,
    shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
    builder: (c) => SafeArea(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 12),
        child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Text('${se.short} Challenge Mock $n${live ? '' : ' · Free mock'}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
          const SizedBox(height: 4),
          const Text('Choose the paper language', style: TextStyle(fontWeight: FontWeight.w600, color: Color(0xFF475569))),
          const SizedBox(height: 12),
          Row(children: [
            Expanded(
              child: FilledButton(
                onPressed: () => Navigator.pop(c, 'en'),
                style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                child: const Text('English', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: FilledButton(
                onPressed: () => Navigator.pop(c, 'hi'),
                style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                child: const Text('हिंदी', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
              ),
            ),
          ]),
        ]),
      ),
    ),
  );
  final picked = lang;
  if (picked == null || !context.mounted) return;
  await Navigator.of(context).push(MaterialPageRoute(
    builder: (_) => TestFlow(
      user: user,
      exam: exam,
      mockId: se.mockId(n, picked),
      lang: picked,
      paid: true,
      title: live ? '${se.short} Challenge Mock $n' : '${se.short} Challenge Mock $n · Free mock',
      aic: AicRun(se, n, live),
    ),
  ));
}

// ============================================================ submitted

/// After a live attempt: saves it and shows only "submitted, result on Tuesday". No score, no solutions, no rank.
class AicSubmitScreen extends StatefulWidget {
  final User user;
  final Exam exam;
  final Paper paper;
  final Progress progress;
  final Result result;
  const AicSubmitScreen({super.key, required this.user, required this.exam, required this.paper, required this.progress, required this.result});

  @override
  State<AicSubmitScreen> createState() => _AicSubmitScreenState();
}

class _AicSubmitScreenState extends State<AicSubmitScreen> {
  bool _saving = true, _failed = false;

  int get _n => widget.paper.aic!.round;
  AicSeries get _se => widget.paper.aic!.series;

  @override
  void initState() {
    super.initState();
    _save();
  }

  /// The leaderboard row, written again when the first save could not put it there.
  Future<void> _row() async {
    final r = widget.result, u = widget.user;
    final db = FirebaseFirestore.instance;
    var name = '';
    try {
      final ud = (await db.collection('users').doc(u.uid).get()).data() ?? const {};
      name = '${ud['name'] ?? ud['displayName'] ?? u.displayName ?? ''}'.trim();
    } catch (_) {}
    await db.collection('leaderboards').doc(_se.board(_n)).collection('scores').doc(u.uid).set({
      'uid': u.uid,
      'name': name.isEmpty ? 'Student' : name,
      'paperId': _se.board(_n),
      'paperName': widget.paper.title.isNotEmpty ? widget.paper.title : _se.title(_n),
      'marks': r.marks,
      'maxMarks': r.maxMarks,
      'accuracy': r.pct,
      'subjectMarks': r.subjects.map((k, v) => MapEntry(k, double.parse(v.marks.toStringAsFixed(1)))),
      'timeUsed': r.timeUsed,
      'submittedAt': FieldValue.serverTimestamp(),
    });
    r.lbSaved = true;
  }

  Future<void> _save() async {
    setState(() {
      _saving = true;
      _failed = false;
    });
    final r = widget.result;
    try {
      // a blank paper is saved too
      if (!r.saved) await saveResult(widget.user, widget.exam, widget.paper, widget.progress, r);
      if (!r.lbSaved) await _row();
      await aicMarkSubmitted(_se, widget.user.uid, _n);
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

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    return PopScope(
      canPop: !_saving && !_failed,
      child: Scaffold(
        backgroundColor: const Color(0xFFEEF2FF),
        appBar: AppBar(automaticallyImplyLeading: false, title: Text('${_se.short} Challenge Mock $_n', style: const TextStyle(fontWeight: FontWeight.w800))),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: _saving
                ? const Column(mainAxisSize: MainAxisSize.min, children: [
                    CircularProgressIndicator(),
                    SizedBox(height: 14),
                    Text('Submitting your test…', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
                    SizedBox(height: 6),
                    Text('Keep the app open.', style: TextStyle(color: Color(0xFF64748B))),
                  ])
                : _failed
                    ? Column(mainAxisSize: MainAxisSize.min, children: [
                        const Icon(Icons.wifi_off, size: 48, color: Color(0xFF94A3B8)),
                        const SizedBox(height: 12),
                        const Text('Your test could not be submitted yet.', textAlign: TextAlign.center, style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
                        const SizedBox(height: 6),
                        const Text('Your answers are safe on this phone. Check your internet and try again.', textAlign: TextAlign.center, style: TextStyle(color: Color(0xFF475569))),
                        const SizedBox(height: 16),
                        FilledButton(
                          onPressed: _save,
                          style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size(200, 50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                          child: const Text('Try again', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
                        ),
                      ])
                    : Column(mainAxisSize: MainAxisSize.min, children: [
                        const Icon(Icons.check_circle_rounded, size: 72, color: Color(0xFF16A34A)),
                        const SizedBox(height: 14),
                        Text('Your test has been submitted successfully.', textAlign: TextAlign.center, style: baloo(22)),
                        const SizedBox(height: 10),
                        Text('Result, All India rank and solutions on ${aicWhen(_se.resultAt(_n))}.',
                            textAlign: TextAlign.center, style: const TextStyle(fontSize: 16, height: 1.4, fontWeight: FontWeight.w600, color: Color(0xFF334155))),
                        const SizedBox(height: 22),
                        FilledButton(
                          onPressed: () => Navigator.of(context).pop(),
                          style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size(200, 50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                          child: const Text('Done', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
                        ),
                      ]),
          ),
        ),
      ),
    );
  }
}

// ============================================================ status card (Home banner, top of the Challenge screen)

/// The challenge card with every state the website banner has: registration open, registered, registered from
/// the next round, live now, entry closed, submitted, and "results are out" from Tuesday.
/// [onOpen]: tapping the card opens that series' Challenge screen.
class AicStatusCard extends StatefulWidget {
  final User user;
  final Exam exam;
  final AicSeries series;
  final String? regLabel; // the Register button's text ("Register for CHSL")
  final VoidCallback? onOpen;
  final bool inPopup; // inside the app-open popup: a button press closes nothing, the chevron is hidden
  final VoidCallback? onChanged; // after a registration or a test
  const AicStatusCard({super.key, required this.user, required this.exam, required this.series, this.regLabel, this.onOpen, this.inPopup = false, this.onChanged});

  @override
  State<AicStatusCard> createState() => _AicStatusCardState();
}

class _AicStatusCardState extends State<AicStatusCard> with WidgetsBindingObserver {
  AicMe _me = const AicMe(null, {});
  bool _inProg = false, _busy = false;
  int? _count;
  Timer? _timer;

  String get _uid => widget.user.uid;
  AicSeries get _se => widget.series;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted) setState(() {});
    });
    aicCached(_se, _uid).then((m) {
      if (mounted) setState(() => _me = m);
    });
    _refresh();
  }

  @override
  void dispose() {
    _timer?.cancel();
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState s) {
    if (s == AppLifecycleState.resumed) _refresh(force: true);
  }

  Future<void> _refresh({bool force = false}) async {
    if (!_se.on) return;
    await AicClock.sync(force: force);
    if (!AicClock.synced) return;
    final now = AicClock.now;
    final up = _se.upRound(now);
    final rounds = [if (up > 0) up, if (up > 1) up - 1, if (up == 0 && _se.lastRound > 0) _se.lastRound];
    var prog = false;
    for (final n in rounds) {
      if (now >= _se.hardCap(n)) continue;
      for (final l in const ['en', 'hi']) {
        if (await loadProgress(_uid, _se.mockId(n, l), '') != null) prog = true;
      }
    }
    final me = await aicLoadMe(_se, _uid, rounds);
    final count = _count ?? await aicRegCount(_se);
    if (!mounted) return;
    setState(() {
      _me = me;
      _inProg = prog;
      _count = count;
    });
  }

  void _open() {
    if (widget.onOpen != null) {
      widget.onOpen!();
    } else {
      Navigator.of(context).push(MaterialPageRoute(builder: (_) => ChallengeScreen(user: widget.user, exam: widget.exam, series: _se)));
    }
  }

  void _say(String t) {
    if (!mounted) return;
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(SnackBar(content: Text(t), behavior: SnackBarBehavior.floating));
  }

  Future<void> _register() async {
    if (_busy) return;
    setState(() => _busy = true);
    await AicClock.sync();
    final at = AicClock.synced ? await aicRegister(_se, widget.user) : null;
    if (!mounted) return;
    setState(() {
      _busy = false;
      if (at != null) {
        _me = AicMe(at, _me.submitted);
        if (_count != null) _count = _count! + 1;
      }
    });
    if (at == null) {
      _say('Could not register. Check your internet and try again.');
    } else {
      final up = _se.upRound(AicClock.now);
      final first = up > 0 && _se.inRound(up, at) ? up : up + 1;
      _say(_se.exists(first) ? 'You are registered for ${_se.short}. Your first Challenge Mock is on ${aicDay(_se.start(first))}.' : 'You are registered for ${_se.short}.');
      widget.onChanged?.call();
    }
  }

  Future<void> _start(int n) async {
    await startAic(context, widget.user, widget.exam, _se, n, live: true);
    await _refresh(force: true);
    widget.onChanged?.call();
  }

  @override
  Widget build(BuildContext context) {
    if (!_se.on) return const SizedBox.shrink();
    final exam = widget.exam;
    final se = _se;
    final now = AicClock.now;
    final v = se.view(now: now, regAt: _me.regAt, submitted: _me.submitted, inProgress: _inProg);
    if (v.state == AicState.off && v.resultsRound == 0) return const SizedBox.shrink();
    final left = v.countdownTo > 0 ? aicCountdown(v.countdownTo - now) : '';
    final n = v.round;
    String head = 'All India Challenge Mock';
    String body = '';
    final actions = <Widget>[];

    Widget btn(String label, VoidCallback? tap, {bool solid = true}) => Padding(
          padding: const EdgeInsets.only(right: 8, top: 8),
          child: solid
              ? FilledButton(
                  onPressed: tap,
                  style: FilledButton.styleFrom(backgroundColor: Colors.white, foregroundColor: exam.c1, padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                  child: Text(label, style: const TextStyle(fontWeight: FontWeight.w800)),
                )
              : OutlinedButton(
                  onPressed: tap,
                  style: OutlinedButton.styleFrom(foregroundColor: Colors.white, side: const BorderSide(color: Colors.white70), padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                  child: Text(label, style: const TextStyle(fontWeight: FontWeight.w800)),
                ),
        );

    final reg = widget.regLabel ?? 'Register free';
    final lastE = n > 0 ? aicClockText(se.lastEntry(n)) : '';
    switch (v.state) {
      case AicState.regOpen:
        head = 'Challenge Mock $n · ${aicDay(se.start(n))}';
        body = 'Free ${se.name} mock with All India rank. ${se.day} 9 am to $lastE. Registration closes in $left.';
        actions.add(btn(_busy ? 'Registering…' : reg, _busy ? null : _register));
      case AicState.regNext:
        head = 'Challenge Mock $n · ${aicDay(se.start(n))}';
        body = 'Registration for this ${se.day} is closed. Register now for the next one; it closes in $left.';
        actions.add(btn(_busy ? 'Registering…' : reg, _busy ? null : _register));
      case AicState.registered:
        head = 'You are registered ✓';
        body = 'Challenge Mock $n starts in $left (${aicWhen(se.start(n))}). Start any time until $lastE.';
      case AicState.registeredNext:
        head = 'You are registered ✓';
        body = 'You are in from Challenge Mock $n on ${aicDay(se.start(n))}. Registration for the ${se.day} before it had already closed.';
      case AicState.live:
        head = 'Challenge Mock $n is LIVE';
        if (_inProg) {
          body = 'Your test is running. It ends ${se.hardStopMin} minutes after you started, 12:30 am at the latest.';
          actions.add(btn('Resume test', () => _start(n)));
        } else {
          body = 'Start before $lastE ($left left). One attempt.';
          actions.add(btn('Start in English', () => startAic(context, widget.user, exam, se, n, live: true, lang: 'en').then((_) => _refresh(force: true))));
          actions.add(btn('हिंदी में शुरू करें', () => startAic(context, widget.user, exam, se, n, live: true, lang: 'hi').then((_) => _refresh(force: true)), solid: false));
        }
      case AicState.entryClosed:
        head = 'Challenge Mock $n: entry closed';
        body = 'Entry closed at $lastE.${se.exists(n + 1) ? ' You are in for Challenge Mock ${n + 1} on ${aicDay(se.start(n + 1))}.' : ''}';
      case AicState.submitted:
        head = 'Challenge Mock $n submitted ✓';
        body = 'Result, All India rank and solutions on ${aicWhen(se.resultAt(n))} (in $left).';
      case AicState.off:
        head = 'All India Challenge Mock';
        body = '';
    }
    if (!AicClock.synced) {
      // never from the phone's clock: nothing is offered until the server time is read
      head = 'All India Challenge Mock';
      body = 'Every ${se.day}, free, with All India rank. Connect to the internet to see this week\'s status.';
      actions.clear();
    }
    final showCount = _count != null && _count! > 0 && (v.state == AicState.regOpen || v.state == AicState.regNext || v.state == AicState.registered || v.state == AicState.registeredNext);

    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(20),
          onTap: widget.onOpen,
          child: Ink(
            padding: const EdgeInsets.fromLTRB(16, 14, 12, 14),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(20),
              gradient: LinearGradient(colors: se.key == 'chsl' ? const [Color(0xFF7C2D12), Color(0xFFEA580C)] : const [Color(0xFF312E81), Color(0xFF6D28D9)], begin: Alignment.topLeft, end: Alignment.bottomRight),
              boxShadow: [BoxShadow(color: (se.key == 'chsl' ? const Color(0xFFEA580C) : const Color(0xFF6D28D9)).withValues(alpha: .25), blurRadius: 18, offset: const Offset(0, 8))],
            ),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                const Text('🏆', style: TextStyle(fontSize: 20)),
                const SizedBox(width: 8),
                Expanded(
                  child: Text('${se.name.toUpperCase()} · ALL INDIA CHALLENGE', maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Color(0xFFFDE68A), fontSize: 11.5, letterSpacing: .4, fontWeight: FontWeight.w800)),
                ),
                if (widget.onOpen != null && !widget.inPopup) const Icon(Icons.chevron_right_rounded, color: Colors.white70),
              ]),
              if (AicClock.synced && v.resultsRound > 0) ...[
                const SizedBox(height: 8),
                GestureDetector(
                  onTap: widget.onOpen == null ? null : _open,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(color: const Color(0xFFFDE68A), borderRadius: BorderRadius.circular(12)),
                    child: Row(children: [
                      Expanded(child: Text('Challenge Mock ${v.resultsRound} results are out', style: const TextStyle(color: Color(0xFF312E81), fontWeight: FontWeight.w800))),
                      if (widget.onOpen != null) const Text('View ›', style: TextStyle(color: Color(0xFF312E81), fontWeight: FontWeight.w800)),
                    ]),
                  ),
                ),
              ],
              if (body.isNotEmpty) ...[
                const SizedBox(height: 8),
                Text(head, style: baloo(20, color: Colors.white)),
                const SizedBox(height: 2),
                Text(body, style: const TextStyle(color: Color(0xF2FFFFFF), fontSize: 13.5, height: 1.35, fontWeight: FontWeight.w600)),
              ],
              if (actions.isNotEmpty) Wrap(children: actions),
              if (showCount)
                Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: Text('${_commas(_count!)} students registered', style: const TextStyle(color: Color(0xFFFDE68A), fontSize: 12.5, fontWeight: FontWeight.w800)),
                ),
            ]),
          ),
        ),
      ),
    );
  }
}

/// The All India Challenge popup, shown when the app opens: once a day, and again whenever a state changes
/// (registration open, live, submitted, results out). Both challenges are on it (CHSL Tier 1 and CGL Tier 2),
/// each with its own Register button, and "Register for both" while neither is registered.
Future<void> maybeShowAicPopup(BuildContext context, User user, Exam exam) async {
  if (!aicAnyOn) return;
  try {
    if (!await AicClock.sync() || !AicClock.synced) return;
    final now = AicClock.now;
    final shown = <AicSeries>[];
    final marks = <String>[];
    final open = <AicSeries>[]; // not registered yet, registration possible
    for (final se in aicAll) {
      if (!se.on) continue;
      final up = se.upRound(now);
      final me = await aicLoadMe(se, user.uid, [if (up > 0) up, if (up > 1) up - 1]);
      final v = se.view(now: now, regAt: me.regAt, submitted: me.submitted);
      if (v.state == AicState.off && v.resultsRound == 0) continue;
      shown.add(se);
      marks.add('${se.key}:${v.state.name}:${v.round}:${v.resultsRound}');
      if (v.state == AicState.regOpen || v.state == AicState.regNext) open.add(se);
    }
    if (shown.isEmpty) return;
    // once a day for the same states; a new state (or a new day) shows it again
    final p = await SharedPreferences.getInstance();
    final day = DateTime.fromMillisecondsSinceEpoch(now, isUtc: true).add(const Duration(hours: 5, minutes: 30)).toIso8601String().substring(0, 10);
    final mark = '$day|${marks.join('|')}';
    final key = 'tssc_aic_popup_${user.uid}';
    if (p.getString(key) == mark) return;
    await p.setString(key, mark);
    if (!context.mounted) return;
    await showDialog<void>(
      context: context,
      builder: (c) => _AicPopup(user: user, exam: exam, shown: shown, canBoth: open.length >= 2, host: context),
    );
  } catch (_) {}
}

class _AicPopup extends StatefulWidget {
  final User user;
  final Exam exam;
  final List<AicSeries> shown;
  final bool canBoth; // both series are open for registration and neither is registered
  final BuildContext host; // the screen under the popup (to open the Challenge screen from)
  const _AicPopup({required this.user, required this.exam, required this.shown, required this.canBoth, required this.host});

  @override
  State<_AicPopup> createState() => _AicPopupState();
}

class _AicPopupState extends State<_AicPopup> {
  int _v = 0;
  bool _busy = false;
  late bool _both = widget.canBoth;

  void _open(AicSeries se) {
    Navigator.of(context).pop();
    Navigator.of(widget.host).push(MaterialPageRoute(builder: (_) => ChallengeScreen(user: widget.user, exam: _examOf(se, widget.exam), series: se)));
  }

  Future<void> _registerBoth() async {
    if (_busy) return;
    setState(() => _busy = true);
    await AicClock.sync();
    var ok = 0;
    if (AicClock.synced) {
      for (final se in widget.shown) {
        if (await aicRegister(se, widget.user) != null) ok++;
      }
    }
    if (!mounted) return;
    setState(() {
      _busy = false;
      if (ok > 0) {
        _both = false;
        _v++; // the cards read the registration again
      }
    });
    ScaffoldMessenger.of(widget.host)
      ..hideCurrentSnackBar()
      ..showSnackBar(SnackBar(
        behavior: SnackBarBehavior.floating,
        content: Text(ok == widget.shown.length ? 'You are registered for both challenges.' : (ok == 0 ? 'Could not register. Check your internet and try again.' : 'Registered for one challenge; try the other again.')),
      ));
  }

  @override
  Widget build(BuildContext context) {
    final shown = widget.shown;
    return Dialog(
      backgroundColor: Colors.white,
      insetPadding: const EdgeInsets.symmetric(horizontal: 18, vertical: 24),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
      child: SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(14, 6, 14, 12),
        child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Row(children: [
            const SizedBox(width: 6),
            Expanded(child: Text(shown.length > 1 ? '🏆 All India Challenges' : '🏆 All India Challenge', style: baloo(20))),
            IconButton(onPressed: () => Navigator.pop(context), icon: const Icon(Icons.close, color: softMuted)),
          ]),
          const Padding(
            padding: EdgeInsets.fromLTRB(6, 0, 6, 8),
            child: Text('Free mock, All India rank and full analysis. Register once for each.', style: TextStyle(fontSize: 13, height: 1.35, color: softMuted, fontWeight: FontWeight.w600)),
          ),
          for (final se in shown)
            AicStatusCard(
              key: ValueKey('aic-pop-${se.key}-$_v'),
              user: widget.user,
              exam: _examOf(se, widget.exam),
              series: se,
              regLabel: shown.length > 1 ? 'Register for ${se.key == 'chsl' ? 'CHSL' : 'CGL'}' : null,
              inPopup: true,
              onOpen: () => _open(se),
              onChanged: () {
                if (mounted && _both) setState(() => _both = false);
              },
            ),
          if (_both)
            FilledButton(
              onPressed: _busy ? null : _registerBoth,
              style: FilledButton.styleFrom(backgroundColor: const Color(0xFF16A34A), minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              child: Text(_busy ? 'Registering…' : 'Register for both', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
            ),
          const Padding(
            padding: EdgeInsets.only(top: 6),
            child: Text('Tap a card for how it works and past results.', textAlign: TextAlign.center, style: TextStyle(fontSize: 12.5, color: softMuted, fontWeight: FontWeight.w600)),
          ),
        ]),
      ),
    );
  }
}

/// Mocks tab: the entry that opens a series' Challenge screen (SSC CGL > Tier 2, SSC CHSL > Tier 1).
class AicEntryCard extends StatelessWidget {
  final User user;
  final Exam exam;
  final AicSeries series;
  const AicEntryCard({super.key, required this.user, required this.exam, required this.series});

  @override
  Widget build(BuildContext context) {
    if (!series.on) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Material(
        color: Colors.transparent,
        child: Ink(
          decoration: softCard(radius: 18),
          child: InkWell(
            borderRadius: BorderRadius.circular(18),
            onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => ChallengeScreen(user: user, exam: _examOf(series, exam), series: series))),
            child: Padding(
              padding: const EdgeInsets.fromLTRB(12, 11, 8, 11),
              child: Row(children: [
                Container(width: 48, height: 48, alignment: Alignment.center, decoration: softWell(), child: const Text('🏆', style: TextStyle(fontSize: 24))),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('All India Challenge Mock', style: baloo(17.5)),
                    Text('Every ${series.day} · free · All India rank', maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(fontSize: 13.5, color: exam.c1, fontWeight: FontWeight.w800)),
                  ]),
                ),
                Icon(Icons.chevron_right_rounded, color: exam.c1),
              ]),
            ),
          ),
        ),
      ),
    );
  }
}

/// My Tests / Dashboard: live challenge attempts are held back until the result; this says when it comes.
class AicHeldNote extends StatelessWidget {
  const AicHeldNote({super.key});

  @override
  Widget build(BuildContext context) {
    if (aicHeld.isEmpty) return const SizedBox.shrink();
    final seen = <String>{};
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      for (final a in aicHeld)
        if (a['aic'] is Map && seen.add('${aicSeriesOfAttempt(a).key}${(a['aic'] as Map)['round']}'))
          Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: Note(
              '🏆 ${aicSeriesOfAttempt(a).short} All India Challenge Mock ${((a['aic'] as Map)['round'] as num? ?? 0).toInt()} is submitted. Its result, All India rank and solutions open on ${aicWhen(aicAttemptResultAt(a))}.',
              color: const Color(0xFF6D28D9),
            ),
          ),
    ]);
  }
}

// ============================================================ Challenge screen

class ChallengeScreen extends StatefulWidget {
  final User user;
  final Exam exam;
  final AicSeries series;
  const ChallengeScreen({super.key, required this.user, required this.exam, required this.series});

  @override
  State<ChallengeScreen> createState() => _ChallengeScreenState();
}

class _ChallengeScreenState extends State<ChallengeScreen> {
  List<Map<String, dynamic>> _atts = const [];
  AicMe _me = const AicMe(null, {});
  int _v = 0;

  AicSeries get _se => widget.series;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    await AicClock.sync();
    try {
      final a = await loadAttempts(widget.user.uid);
      final me = await aicCached(_se, widget.user.uid);
      if (mounted) {
        setState(() {
          _atts = a;
          _me = me;
          _v++;
        });
      }
    } catch (_) {}
  }

  /// This student's attempt of round [n] whose result may be shown: the live one first, else the latest free mock.
  Map<String, dynamic>? _attempt(int n) {
    Map<String, dynamic>? free;
    for (final a in _atts) {
      final x = a['aic'];
      if (x is! Map || (x['round'] as num? ?? 0).toInt() != n || aicSeriesOfAttempt(a).key != _se.key) continue;
      if (x['live'] == true) return a;
      free ??= a;
    }
    return free;
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam, se = _se;
    final now = AicClock.now;
    final synced = AicClock.synced;
    final up = synced ? se.upRound(now) : 0;
    final done = synced ? se.finished(now) : const <int>[];
    final lastE = aicClockText(se.lastEntry(1));
    Widget how(String t) => Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Padding(padding: const EdgeInsets.only(top: 2), child: Icon(Icons.check_circle_rounded, size: 18, color: exam.c1)),
            const SizedBox(width: 8),
            Expanded(child: Text(t, style: const TextStyle(fontSize: 14, height: 1.4, color: softInk, fontWeight: FontWeight.w600))),
          ]),
        );
    return DashPage(exam: exam, title: '${se.short} Challenge', onRefresh: _load, children: [
      AicStatusCard(key: ValueKey('aic-card-${se.key}-$_v'), user: widget.user, exam: exam, series: se, onChanged: _load),
      if (!synced) emptyNote('Connect to the internet to see the schedule and the results.'),
      if (up > 0)
        PCard(title: 'Next ${se.day}s', sub: 'Every ${se.day}, 9 am to $lastE', children: [
          for (var n = up; n < up + 4 && se.exists(n); n++)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 6),
              child: Row(children: [
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('Challenge Mock $n', style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: softInk)),
                    Text('${aicDay(se.start(n))} · result ${aicDay(se.resultAt(n))}', style: const TextStyle(fontSize: 12.5, color: softMuted, fontWeight: FontWeight.w600)),
                  ]),
                ),
                Builder(builder: (_) {
                  final inIt = se.inRound(n, _me.regAt);
                  final closed = now >= se.regClose(n);
                  final label = _me.submitted.contains(n) ? 'Submitted' : (inIt ? 'You are in' : (closed ? 'Closed' : 'Register by ${aicDay(se.regClose(n) - 60000).split(' ').first}'));
                  final c = inIt || _me.submitted.contains(n) ? cGood : (closed ? softMuted : exam.c1);
                  return Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                    decoration: BoxDecoration(color: c.withValues(alpha: .1), borderRadius: BorderRadius.circular(20)),
                    child: Text(label, style: TextStyle(fontSize: 12, fontWeight: FontWeight.w800, color: c)),
                  );
                }),
              ]),
            ),
        ]),
      PCard(title: 'How it works', children: [
        how('Free for everyone. Register once and you are in for every ${se.day} after that. This registration is only for ${se.short}.'),
        how('Registration for a ${se.day} closes at midnight the day before. Register later and you are in from the next ${se.day}.'),
        how('The test is open on ${se.day} from 9 am. Start any time until $lastE. One attempt only.'),
        how(se.paperLine),
        how(se.parts ? 'No pause and no going back to a finished part.' : 'No pause. The test ends ${se.hardStopMin} minutes after you start.'),
        how('Result, All India rank and solutions two days later at 9 am.'),
        how('From then the same paper is open to everyone as a free mock. A free mock is not counted in the All India rank.'),
        if (se.lastRound > 0) how('Last round: Challenge Mock ${se.lastRound} on ${aicDay(se.start(se.lastRound))}.'),
      ]),
      for (final n in done)
        _RoundCard(
          key: ValueKey('aic-round-${se.key}-$n-$_v'),
          user: widget.user,
          exam: exam,
          series: se,
          round: n,
          auto: n == done.first,
          attempt: _attempt(n),
          onReturn: _load,
        ),
    ]);
  }
}

/// A finished round: top 10, "My result" and "Attempt as free mock".
class _RoundCard extends StatefulWidget {
  final User user;
  final Exam exam;
  final AicSeries series;
  final int round;
  final bool auto; // load the top 10 at once (the latest round); older rounds on tap
  final Map<String, dynamic>? attempt;
  final VoidCallback onReturn;
  const _RoundCard({super.key, required this.user, required this.exam, required this.series, required this.round, required this.auto, required this.attempt, required this.onReturn});

  @override
  State<_RoundCard> createState() => _RoundCardState();
}

class _RoundCardState extends State<_RoundCard> {
  List<AicTop>? _top;
  int _total = 0;
  bool _loading = false, _failed = false;

  @override
  void initState() {
    super.initState();
    if (widget.auto) _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _failed = false;
    });
    try {
      final r = await aicTop10(widget.series, widget.round);
      if (mounted) {
        setState(() {
          _top = r.$1;
          _total = r.$2;
          _loading = false;
        });
      }
    } catch (_) {
      if (mounted) {
        setState(() {
          _loading = false;
          _failed = true;
        });
      }
    }
  }

  String _time(int s) => s <= 0 ? '' : '${s ~/ 60} min';

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam, n = widget.round, a = widget.attempt, se = widget.series;
    final top = _top;
    return PCard(
      title: 'Challenge Mock $n',
      sub: '${aicDay(se.start(n))}${_total > 0 ? ' · ${_commas(_total)} took it live' : ''}',
      children: [
        if (_loading) const Padding(padding: EdgeInsets.all(12), child: Center(child: CircularProgressIndicator())),
        if (_failed) emptyNote('Could not load the top 10. Pull down to try again.'),
        if (top == null && !_loading && !_failed)
          Align(
            alignment: Alignment.centerLeft,
            child: TextButton(onPressed: _load, child: Text('Show top 10', style: TextStyle(fontWeight: FontWeight.w800, color: exam.c1))),
          ),
        if (top != null && top.isEmpty) emptyNote('No live attempts on this round.'),
        if (top != null && top.isNotEmpty) ...[
          for (var i = 0; i < top.length; i++)
            Container(
              margin: const EdgeInsets.only(bottom: 4),
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 7),
              decoration: BoxDecoration(color: top[i].uid == widget.user.uid ? exam.c1.withValues(alpha: .1) : const Color(0xFFF8FAFC), borderRadius: BorderRadius.circular(10)),
              child: Row(children: [
                SizedBox(width: 30, child: Text('#${i + 1}', style: TextStyle(fontWeight: FontWeight.w800, color: exam.c1))),
                Expanded(child: Text(top[i].uid == widget.user.uid ? '${top[i].name} (you)' : top[i].name, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontWeight: FontWeight.w700, color: softInk))),
                if (_time(top[i].timeUsed).isNotEmpty) Text('${_time(top[i].timeUsed)}  ', style: const TextStyle(fontSize: 12, color: softMuted, fontWeight: FontWeight.w600)),
                Text(n1(top[i].marks), style: const TextStyle(fontWeight: FontWeight.w800, color: softInk)),
              ]),
            ),
        ],
        const SizedBox(height: 8),
        Row(children: [
          if (a != null) ...[
            Expanded(
              child: FilledButton(
                onPressed: () => Navigator.of(context).push(MaterialPageRoute(
                  builder: (_) => TestAnalysisPage(x: DashCtx(widget.user, exam, [a], scopeOf(a), 'GEN'), a: a),
                )),
                style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(46), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                child: const Text('My result', style: TextStyle(fontWeight: FontWeight.w800)),
              ),
            ),
            const SizedBox(width: 8),
          ],
          Expanded(
            child: OutlinedButton(
              onPressed: () async {
                await startAic(context, widget.user, exam, se, n, live: false);
                widget.onReturn();
              },
              style: OutlinedButton.styleFrom(foregroundColor: exam.c1, minimumSize: const Size.fromHeight(46), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
              child: Text(a != null && !aicLiveAtt(a) ? 'Attempt again' : 'Attempt as free mock', style: const TextStyle(fontWeight: FontWeight.w800)),
            ),
          ),
        ]),
      ],
    );
  }
}
