// SSC CGL Tier-2 All India Challenge Mock: the Home banner, the Challenge screen, the "submitted" screen
// and the small notes. The rules live in ../aic.dart, the reads and writes in ../aic_io.dart.
import 'dart:async';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

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

Exam _cgl(Exam fallback) => examById('ssc-cgl') ?? fallback;

String _commas(int v) => v.toString().replaceAllMapped(RegExp(r'(\d)(?=(\d{3})+$)'), (m) => '${m[1]},');

/// Starts (or resumes) a challenge paper: the live Sunday attempt, or the free mock after the result.
Future<void> startAic(BuildContext context, User user, Exam exam, int n, {required bool live, String? lang}) async {
  // a paper already started on this phone keeps its language
  for (final l in const ['en', 'hi']) {
    if (await loadProgress(user.uid, aicMockId(n, l), '') != null) lang = l;
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
          Text('Challenge Mock $n${live ? '' : ' · Free mock'}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
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
      mockId: aicMockId(n, picked),
      lang: picked,
      paid: true,
      title: live ? 'Challenge Mock $n' : 'Challenge Mock $n · Free mock',
      aic: AicRun(n, live),
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
    await db.collection('leaderboards').doc(aicBoard(_n)).collection('scores').doc(u.uid).set({
      'uid': u.uid,
      'name': name.isEmpty ? 'Student' : name,
      'paperId': aicBoard(_n),
      'paperName': widget.paper.title.isNotEmpty ? widget.paper.title : aicTitle(_n),
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
      await aicMarkSubmitted(widget.user.uid, _n);
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
        appBar: AppBar(automaticallyImplyLeading: false, title: Text('Challenge Mock $_n', style: const TextStyle(fontWeight: FontWeight.w800))),
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
                        Text('Result, All India rank and solutions on ${aicWhen(aicResultAt(_n))}.',
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
/// [onOpen]: tapping the card opens the Challenge screen (Home). [popup]: also raise the "results out" pop-up once a day.
class AicStatusCard extends StatefulWidget {
  final User user;
  final Exam exam;
  final VoidCallback? onOpen;
  final bool popup;
  final bool compact; // Home: a short card (the Home screen does not scroll)
  final VoidCallback? onChanged; // after a registration or a test
  const AicStatusCard({super.key, required this.user, required this.exam, this.onOpen, this.popup = false, this.compact = false, this.onChanged});

  @override
  State<AicStatusCard> createState() => _AicStatusCardState();
}

class _AicStatusCardState extends State<AicStatusCard> with WidgetsBindingObserver {
  AicMe _me = const AicMe(null, {});
  bool _inProg = false, _busy = false, _popped = false;
  int? _count;
  Timer? _timer;

  String get _uid => widget.user.uid;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (mounted) setState(() {});
    });
    aicCached(_uid).then((m) {
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
    if (!aicConfig.on) return;
    await AicClock.sync(force: force);
    if (!AicClock.synced) return;
    final now = AicClock.now;
    final up = aicUpRound(now);
    final rounds = [if (up > 0) up, if (up > 1) up - 1, if (up == 0 && aicConfig.lastRound > 0) aicConfig.lastRound];
    var prog = false;
    for (final n in rounds) {
      if (now >= aicHardCap(n)) continue;
      for (final l in const ['en', 'hi']) {
        if (await loadProgress(_uid, aicMockId(n, l), '') != null) prog = true;
      }
    }
    final me = await aicLoadMe(_uid, rounds);
    final count = _count ?? await aicRegCount();
    if (!mounted) return;
    setState(() {
      _me = me;
      _inProg = prog;
      _count = count;
    });
    final v = aicView(now: AicClock.now, regAt: me.regAt, submitted: me.submitted, inProgress: prog);
    if (widget.popup && !_popped && v.resultsRound > 0 && await aicPopupDue(_uid, v.resultsRound)) {
      _popped = true;
      if (mounted) _resultsPopup(v.resultsRound);
    }
  }

  void _resultsPopup(int n) {
    final exam = widget.exam;
    showDialog<void>(
      context: context,
      builder: (c) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Text('🏆 Challenge Mock $n results are out', style: baloo(20)),
        content: const Text('See your All India rank, the top 10 and the solutions. The paper is now open to everyone as a free mock.', style: TextStyle(height: 1.4)),
        actions: [
          TextButton(onPressed: () => Navigator.pop(c), child: const Text('Later')),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: exam.c1),
            onPressed: () {
              Navigator.pop(c);
              _open();
            },
            child: const Text('See results'),
          ),
        ],
      ),
    );
  }

  void _open() {
    if (widget.onOpen != null) {
      widget.onOpen!();
    } else {
      Navigator.of(context).push(MaterialPageRoute(builder: (_) => ChallengeScreen(user: widget.user, exam: widget.exam)));
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
    final at = AicClock.synced ? await aicRegister(widget.user) : null;
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
      final up = aicUpRound(AicClock.now);
      final first = up > 0 && aicInRound(up, at) ? up : up + 1;
      _say('You are registered. Your first Challenge Mock is on ${aicDay(aicStart(first))}.');
      widget.onChanged?.call();
    }
  }

  Future<void> _start(int n) async {
    await startAic(context, widget.user, widget.exam, n, live: true);
    await _refresh(force: true);
    widget.onChanged?.call();
  }

  @override
  Widget build(BuildContext context) {
    if (!aicConfig.on) return const SizedBox.shrink();
    final exam = widget.exam;
    final now = AicClock.now;
    final v = aicView(now: now, regAt: _me.regAt, submitted: _me.submitted, inProgress: _inProg);
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

    switch (v.state) {
      case AicState.regOpen:
        head = 'Challenge Mock $n · ${aicDay(aicStart(n))}';
        body = 'Free SSC CGL Tier-2 mock with All India rank. Sunday 9 am to 9:45 pm. Registration closes in $left.';
        actions.add(btn(_busy ? 'Registering…' : 'Register free', _busy ? null : _register));
      case AicState.regNext:
        head = 'Challenge Mock $n · ${aicDay(aicStart(n))}';
        body = 'Registration for this Sunday is closed. Register now for the next one; it closes in $left.';
        actions.add(btn(_busy ? 'Registering…' : 'Register free', _busy ? null : _register));
      case AicState.registered:
        head = 'You are registered ✓';
        body = 'Challenge Mock $n starts in $left (${aicWhen(aicStart(n))}). Start any time until 9:45 pm.';
      case AicState.registeredNext:
        head = 'You are registered ✓';
        body = 'You are in from Challenge Mock $n on ${aicDay(aicStart(n))}. Registration for the Sunday before it had already closed.';
      case AicState.live:
        head = 'Challenge Mock $n is LIVE';
        if (_inProg) {
          body = 'Your test is running. It ends 2 h 25 min after you started, 12:30 am at the latest.';
          actions.add(btn('Resume test', () => _start(n)));
        } else {
          body = 'Start before 9:45 pm ($left left). 150 questions, five timed parts, one attempt.';
          actions.add(btn('Start in English', () => startAic(context, widget.user, exam, n, live: true, lang: 'en').then((_) => _refresh(force: true))));
          actions.add(btn('हिंदी में शुरू करें', () => startAic(context, widget.user, exam, n, live: true, lang: 'hi').then((_) => _refresh(force: true)), solid: false));
        }
      case AicState.entryClosed:
        head = 'Challenge Mock $n: entry closed';
        body = 'Entry closed at 9:45 pm.${aicRoundExists(n + 1) ? ' You are in for Challenge Mock ${n + 1} on ${aicDay(aicStart(n + 1))}.' : ''}';
      case AicState.submitted:
        head = 'Challenge Mock $n submitted ✓';
        body = 'Result, All India rank and solutions on ${aicWhen(aicResultAt(n))} (in $left).';
      case AicState.off:
        head = 'All India Challenge Mock';
        body = '';
    }
    if (!AicClock.synced) {
      // never from the phone's clock: nothing is offered until the server time is read
      head = 'All India Challenge Mock';
      body = 'Every Sunday, free, with All India rank. Connect to the internet to see this week\'s status.';
      actions.clear();
    }
    final showCount = _count != null && _count! > 0 && (v.state == AicState.regOpen || v.state == AicState.regNext || v.state == AicState.registered || v.state == AicState.registeredNext);

    if (widget.compact) {
      // Home: one short card. Head, two lines of status and one button; everything else is on the Challenge screen.
      final results = AicClock.synced && v.resultsRound > 0;
      String? act;
      VoidCallback? tap;
      if (AicClock.synced) {
        if (v.state == AicState.regOpen || v.state == AicState.regNext) {
          act = _busy ? '…' : 'Register';
          tap = _busy ? null : _register;
        } else if (v.state == AicState.live) {
          act = _inProg ? 'Resume' : 'Start';
          tap = () => _start(n);
        } else if (results) {
          act = 'Results';
          tap = _open;
        }
      }
      final line = body.isEmpty ? 'Challenge Mock ${v.resultsRound} results are out.' : (results && act != 'Results' ? 'Mock ${v.resultsRound} results are out. $body' : body);
      return Padding(
        padding: const EdgeInsets.only(bottom: 8),
        child: Material(
          color: Colors.transparent,
          child: InkWell(
            borderRadius: BorderRadius.circular(18),
            onTap: widget.onOpen,
            child: Ink(
              padding: const EdgeInsets.fromLTRB(12, 9, 10, 9),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(18),
                gradient: const LinearGradient(colors: [Color(0xFF312E81), Color(0xFF6D28D9)], begin: Alignment.topLeft, end: Alignment.bottomRight),
              ),
              child: Row(children: [
                const Text('🏆', style: TextStyle(fontSize: 22)),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisSize: MainAxisSize.min, children: [
                    Text(body.isEmpty ? 'All India Challenge Mock' : (v.state == AicState.registered || v.state == AicState.registeredNext ? 'All India Challenge · registered ✓' : head),
                        maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.w800)),
                    Text(line, maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Color(0xF2FFFFFF), fontSize: 12, height: 1.25, fontWeight: FontWeight.w600)),
                  ]),
                ),
                const SizedBox(width: 8),
                if (act != null)
                  FilledButton(
                    onPressed: tap,
                    style: FilledButton.styleFrom(backgroundColor: Colors.white, foregroundColor: exam.c1, minimumSize: const Size(0, 38), padding: const EdgeInsets.symmetric(horizontal: 14), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                    child: Text(act, style: const TextStyle(fontWeight: FontWeight.w800)),
                  )
                else
                  const Icon(Icons.chevron_right_rounded, color: Colors.white70),
              ]),
            ),
          ),
        ),
      );
    }

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
              gradient: const LinearGradient(colors: [Color(0xFF312E81), Color(0xFF6D28D9)], begin: Alignment.topLeft, end: Alignment.bottomRight),
              boxShadow: [BoxShadow(color: const Color(0xFF6D28D9).withValues(alpha: .25), blurRadius: 18, offset: const Offset(0, 8))],
            ),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Row(children: [
                const Text('🏆', style: TextStyle(fontSize: 20)),
                const SizedBox(width: 8),
                const Expanded(
                  child: Text('SSC CGL TIER-2 · ALL INDIA CHALLENGE', maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(color: Color(0xFFFDE68A), fontSize: 11.5, letterSpacing: .4, fontWeight: FontWeight.w800)),
                ),
                if (widget.onOpen != null) const Icon(Icons.chevron_right_rounded, color: Colors.white70),
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

/// Home: the challenge banner. Tapping it opens the Challenge screen.
class AicBanner extends StatelessWidget {
  final User user;
  final Exam exam;
  const AicBanner({super.key, required this.user, required this.exam});

  @override
  Widget build(BuildContext context) {
    final cgl = _cgl(exam);
    return AicStatusCard(
      user: user,
      exam: cgl,
      popup: true,
      compact: true,
      onOpen: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => ChallengeScreen(user: user, exam: cgl))),
    );
  }
}

/// SSC CGL > Mocks > Tier 2: the entry that opens the Challenge screen.
class AicEntryCard extends StatelessWidget {
  final User user;
  final Exam exam;
  const AicEntryCard({super.key, required this.user, required this.exam});

  @override
  Widget build(BuildContext context) {
    if (!aicConfig.on) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Material(
        color: Colors.transparent,
        child: Ink(
          decoration: softCard(radius: 18),
          child: InkWell(
            borderRadius: BorderRadius.circular(18),
            onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => ChallengeScreen(user: user, exam: _cgl(exam)))),
            child: Padding(
              padding: const EdgeInsets.fromLTRB(12, 11, 8, 11),
              child: Row(children: [
                Container(width: 48, height: 48, alignment: Alignment.center, decoration: softWell(), child: const Text('🏆', style: TextStyle(fontSize: 24))),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('All India Challenge Mock', style: baloo(17.5)),
                    Text('Every Sunday · free · All India rank', maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(fontSize: 13.5, color: exam.c1, fontWeight: FontWeight.w800)),
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
    final seen = <int>{};
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      for (final a in aicHeld)
        if (a['aic'] is Map && seen.add(((a['aic'] as Map)['round'] as num? ?? 0).toInt()))
          Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: Note(
              '🏆 All India Challenge Mock ${((a['aic'] as Map)['round'] as num? ?? 0).toInt()} is submitted. Its result, All India rank and solutions open on ${aicWhen(aicAttemptResultAt(a))}.',
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
  const ChallengeScreen({super.key, required this.user, required this.exam});

  @override
  State<ChallengeScreen> createState() => _ChallengeScreenState();
}

class _ChallengeScreenState extends State<ChallengeScreen> {
  List<Map<String, dynamic>> _atts = const [];
  AicMe _me = const AicMe(null, {});
  int _v = 0;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    await AicClock.sync();
    try {
      final a = await loadAttempts(widget.user.uid);
      final me = await aicCached(widget.user.uid);
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
      if (x is! Map || (x['round'] as num? ?? 0).toInt() != n) continue;
      if (x['live'] == true) return a;
      free ??= a;
    }
    return free;
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final now = AicClock.now;
    final synced = AicClock.synced;
    final up = synced ? aicUpRound(now) : 0;
    final done = synced ? aicFinished(now) : const <int>[];
    Widget how(String t) => Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Padding(padding: const EdgeInsets.only(top: 2), child: Icon(Icons.check_circle_rounded, size: 18, color: exam.c1)),
            const SizedBox(width: 8),
            Expanded(child: Text(t, style: const TextStyle(fontSize: 14, height: 1.4, color: softInk, fontWeight: FontWeight.w600))),
          ]),
        );
    return DashPage(exam: exam, title: 'All India Challenge', onRefresh: _load, children: [
      AicStatusCard(key: ValueKey('aic-card-$_v'), user: widget.user, exam: exam, onChanged: _load),
      if (!synced) emptyNote('Connect to the internet to see the schedule and the results.'),
      if (up > 0)
        PCard(title: 'Next Sundays', sub: 'Every Sunday, 9 am to 9:45 pm', children: [
          for (var n = up; n < up + 4 && aicRoundExists(n); n++)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 6),
              child: Row(children: [
                Expanded(
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('Challenge Mock $n', style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: softInk)),
                    Text('${aicDay(aicStart(n))} · result ${aicDay(aicResultAt(n))}', style: const TextStyle(fontSize: 12.5, color: softMuted, fontWeight: FontWeight.w600)),
                  ]),
                ),
                Builder(builder: (_) {
                  final inIt = aicInRound(n, _me.regAt);
                  final closed = now >= aicRegClose(n);
                  final label = _me.submitted.contains(n) ? 'Submitted' : (inIt ? 'You are in' : (closed ? 'Closed' : 'Register by Sat'));
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
        how('Free for everyone. Register once and you are in for every Sunday after that.'),
        how('Registration for a Sunday closes on Saturday midnight. Register later and you are in from the next Sunday.'),
        how('The test is open on Sunday from 9 am. Start any time until 9:45 pm. One attempt only.'),
        how('150 questions, +3 for a correct answer, −1 for a wrong one.'),
        how('Five separately timed parts, in order: Maths 30 min, Reasoning 30, English 40, General Awareness 20, Computer 15. No pause and no going back to a finished part.'),
        how('Result, All India rank and solutions on Tuesday at 9 am.'),
        how('From Tuesday the same paper is open to everyone as a free mock. A free mock is not counted in the All India rank.'),
      ]),
      for (final n in done)
        _RoundCard(
          key: ValueKey('aic-round-$n-$_v'),
          user: widget.user,
          exam: exam,
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
  final int round;
  final bool auto; // load the top 10 at once (the latest round); older rounds on tap
  final Map<String, dynamic>? attempt;
  final VoidCallback onReturn;
  const _RoundCard({super.key, required this.user, required this.exam, required this.round, required this.auto, required this.attempt, required this.onReturn});

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
      final r = await aicTop10(widget.round);
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
    final exam = widget.exam, n = widget.round, a = widget.attempt;
    final top = _top;
    return PCard(
      title: 'Challenge Mock $n',
      sub: '${aicDay(aicStart(n))}${_total > 0 ? ' · ${_commas(_total)} took it live' : ''}',
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
                await startAic(context, widget.user, exam, n, live: false);
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
