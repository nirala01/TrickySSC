import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_sign_in/google_sign_in.dart';

import '../app_rating.dart';
import '../billing.dart';
import '../data.dart';
import '../test/engine.dart';
import 'dashboard.dart';
import 'pyq.dart';
import 'chapter_pyq.dart';
import 'dash/logic.dart';
import 'dash/pages.dart';
import 'chapters.dart';
import 'plans.dart';
import 'subject_mocks.dart';
import 'current_affairs.dart';
import 'report_issue.dart';
import 'about.dart';
import 'aic_screens.dart';
import '../aic.dart';
import '../app_update.dart';
import '../profile.dart' show appVersion;
import '../ui/icons3d.dart';
import '../ui/soft.dart';
import '../ui/soft_list.dart';
import '../ui/nav.dart';
import '../test/test_screen.dart';

/// The app after sign-in: Home, Mocks, PYQs and Me. Tabs stay loaded, so switching is instant.
class AppShell extends StatefulWidget {
  final User user;
  final Exam exam;
  final VoidCallback onChangeExam;
  const AppShell({super.key, required this.user, required this.exam, required this.onChangeExam});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int _tab = 0;
  int _tier = 1;
  String _mockSub = ''; // Mocks tab: the subject picked ('' = full mocks)
  String _name = 'Student';
  Set<String> _owned = <String>{};
  Set<String> _attempted = <String>{};
  Map<String, Map<String, dynamic>> _last = {};
  Map<String, List<String>> _resume = {};
  int _version = 0;
  List<MockItem>? _mocks;
  bool _mocksFailed = false;
  int? _price;
  // until the name and the passes are loaded, a "please wait" screen covers the app, so a paid student on a
  // slow connection never sees "Student" or a locked course first (2026-11-18)
  bool _nameReady = false, _ownedReady = false;
  bool get _ready => _nameReady && _ownedReady;
  // what was loaded last for this student in this app run: shown at once when the exam is changed,
  // so the wait screen appears only when the app is opened
  static String? _cUid;
  static String? _cName;
  static Set<String>? _cOwned;

  bool get _hasPass => _owned.contains(widget.exam.pass);

  /// Payment confirmed and pass opened: say so clearly, and offer to go straight to the mocks.
  void _onUnlocked() {
    final name = Billing.I.unlocked.value;
    if (name == null || !mounted) return;
    Billing.I.unlocked.value = null;
    showDialog<void>(
      context: context,
      builder: (c) => AlertDialog(
        icon: const Icon(Icons.check_circle_rounded, color: Color(0xFF16A34A), size: 48),
        title: const Text('Payment successful', textAlign: TextAlign.center),
        content: Text('Your $name is unlocked. All the best!', textAlign: TextAlign.center, style: const TextStyle(fontSize: 15.5, height: 1.4)),
        actionsAlignment: MainAxisAlignment.center,
        actions: [
          TextButton(onPressed: () => Navigator.pop(c), child: const Text('OK')),
          FilledButton(
            onPressed: () {
              Navigator.pop(c);
              setState(() {
                _mockSub = '';
                _tab = 2;
              });
            },
            child: const Text('Start practising'),
          ),
        ],
      ),
    );
  }

  @override
  void _toHome() {
    if (mounted && _tab != 0) setState(() => _tab = 0);
  }

  @override
  void dispose() {
    homeRequest.removeListener(_toHome);
    Billing.I.unlocked.removeListener(_onUnlocked);
    AppUpdater.available.removeListener(_onUpdate);
    _life?.dispose();
    Billing.I
      ..onMessage = null
      ..onGranted = null;
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    homeRequest.addListener(_toHome);
    Billing.I.unlocked.addListener(_onUnlocked);
    Billing.I
      ..onMessage = _say
      ..onGranted = () {
        loadOwned(widget.user.uid).then((o) {
          _cOwned = o;
          if (mounted) setState(() => _owned = o);
        });
      }
      ..start();
    _loadMocks();
    if (_cUid == widget.user.uid) {
      if (_cName != null) { _name = _cName!; _nameReady = true; }
      if (_cOwned != null) { _owned = _cOwned!; _ownedReady = true; }
    } else {
      _cUid = widget.user.uid;
      _cName = null;
      _cOwned = null;
    }
    loadName(widget.user.uid, widget.user.displayName).then((n) {
      _cName = n;
      if (mounted) setState(() { _name = n; _nameReady = true; });
    }).catchError((_) {
      if (mounted) setState(() => _nameReady = true);
    });
    loadOwnedOrNull(widget.user.uid).then((o) {
      if (o != null) _cOwned = o;
      if (!mounted) return;
      setState(() { _owned = o ?? <String>{}; _ownedReady = true; });
      if (o != null) _welcome(o);
    }).catchError((_) {
      if (mounted) setState(() => _ownedReady = true);
    });
    // never hold the app for long: after 12 seconds it opens with whatever has loaded
    Future.delayed(const Duration(seconds: 12), () {
      if (mounted && !_ready) setState(() { _nameReady = true; _ownedReady = true; });
    });
    _loadAtt();
    _loadResume();
    // TSSC-INAPPUPDATE-V3: the update popup no longer waits for the account to load; it shows as soon as
    // Play says a newer version exists, and the check runs again each time the app comes back to the front
    AppUpdater.available.addListener(_onUpdate);
    _life = AppLifecycleListener(onResume: () => AppUpdater.check());
    AppUpdater.check();
    loadPrice(widget.exam).then((p) {
      if (mounted) setState(() => _price = p);
    });
  }

  void _loadMocks() {
    setState(() => _mocksFailed = false);
    loadMocks(widget.exam).then((list) {
      if (mounted) setState(() => _mocks = list);
    }).catchError((_) {
      if (mounted) setState(() => _mocksFailed = true);
    });
  }

  static String? _welcomed; // once per app open, per student

  AppLifecycleListener? _life;

  void _onUpdate() {
    if (AppUpdater.available.value == null) return;
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) showUpdatePopup(context);
    });
  }

  /// On entering the app: a student with no pass sees Full Access (with a link to every other pass);
  /// a paid student sees only their upgrade; full access sees nothing.
  Future<void> _welcome(Set<String> owned) async {
    if (_welcomed == widget.user.uid) return;
    _welcomed = widget.user.uid;
    // TSSC-INAPPUPDATE-V2: a waiting app update comes first, as a popup
    final upd = await AppUpdater.check().timeout(const Duration(seconds: 6), onTimeout: () => false);
    if (upd && mounted) await showUpdatePopup(context);
    if (!mounted) return;
    if (owned.isEmpty) {
      await Billing.I.showFullAccessPopup(context, onExplore: () {
        if (mounted) setState(() => _tab = 1);
      });
    } else if (!exams.every((e) => owned.contains(e.pass))) {
      final q = await Billing.I.quote();
      if (mounted && q != null && q.offer) await Billing.I.showUpgradeSheet(context, widget.exam, q);
    }
    // then the All India Challenge popup (once a day, and again when its state changes)
    if (mounted) await maybeShowAicPopup(context, widget.user, widget.exam);
  }

  void _buy() => Billing.I.showBuySheet(context, widget.exam);

  void _say(String t) {
    if (!mounted) return;
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(SnackBar(content: Text(t), duration: const Duration(seconds: 4)));
  }

  void _soon(String what) {
    if (what == 'Buying a pass') return _buy();
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(SnackBar(content: Text('$what comes in the next build.'), duration: const Duration(seconds: 2)));
  }

  Future<void> _signOut() async {
    try {
      await GoogleSignIn().signOut();
    } catch (_) {}
    await FirebaseAuth.instance.signOut();
  }

  void _loadAtt() => loadAttemptInfo(widget.user.uid).then((r) {
        if (mounted) {
          setState(() {
            _attempted = r.$1;
            _last = r.$2;
          });
        }
      });

  void _mockTap(MockItem m) {
    final exam = widget.exam;
    if (_open(m) && !_resuming(m) && isAttempted(_attempted, exam, m)) {
      showDoneSheet(context, user: widget.user, exam: exam, a: _last[mockBase(exam, m)], title: '${exam.name} ${tierWord(m.tier)}Mock ${m.n}', onRetake: () => _startMock(m));
    } else {
      _startMock(m);
    }
  }

  bool _open(MockItem m) => _hasPass || m.n <= freeMocks(widget.exam, m);

  void _loadResume() => loadInProgress(widget.user.uid).then((r) {
        if (mounted) setState(() => _resume = r);
      });

  bool _resuming(MockItem m) => _resume.containsKey(mockBase(widget.exam, m));

  Future<void> _startMock(MockItem m) async {
    final exam = widget.exam;
    if (!_open(m)) {
      _buy();
      return;
    }
    String lang = m.en ? 'en' : 'hi';
    String partD = lang;
    final both = m.en && m.hi;
    final saved = _resume[mockBase(exam, m)];
    if (saved != null) {
      lang = saved[0];
      partD = saved[1].isEmpty ? lang : saved[1];
    } else if (both || exam.partD) {
      final picked = await showModalBottomSheet<List<String>>(
        context: context,
        backgroundColor: Colors.white,
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
        builder: (c) {
          var l = lang, d = partD;
          return StatefulBuilder(builder: (c, set) {
            Widget opt(String label, bool on, VoidCallback tap) => Expanded(
                  child: Material(
                    color: on ? Color.lerp(Colors.white, exam.c2, 0.3) : const Color(0xFFF1F5F9),
                    borderRadius: BorderRadius.circular(12),
                    child: InkWell(
                      borderRadius: BorderRadius.circular(12),
                      onTap: tap,
                      child: Container(
                        height: 48,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), border: Border.all(color: on ? exam.c1 : Colors.transparent, width: 2)),
                        child: Text(label, style: TextStyle(fontWeight: FontWeight.w800, color: on ? exam.c1 : const Color(0xFF334155))),
                      ),
                    ),
                  ),
                );
            return SafeArea(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 12),
                child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                  Text('${exam.name} Mock ${m.n}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
                  const SizedBox(height: 12),
                  if (both) ...[
                    const Text('Paper language', style: TextStyle(fontWeight: FontWeight.w700, color: Color(0xFF475569))),
                    const SizedBox(height: 6),
                    Row(children: [
                      opt('English', l == 'en', () => set(() { if (d == l) d = 'en'; l = 'en'; })),
                      const SizedBox(width: 8),
                      opt('हिंदी', l == 'hi', () => set(() { if (d == l) d = 'hi'; l = 'hi'; })),
                    ]),
                    const SizedBox(height: 12),
                  ],
                  if (exam.partD && both) ...[
                    const Text('Part D (Q61–80)', style: TextStyle(fontWeight: FontWeight.w700, color: Color(0xFF475569))),
                    const SizedBox(height: 6),
                    Row(children: [
                      opt('English', d == 'en', () => set(() => d = 'en')),
                      const SizedBox(width: 8),
                      opt('Hindi', d == 'hi', () => set(() => d = 'hi')),
                    ]),
                    const SizedBox(height: 12),
                  ],
                  FilledButton(
                    onPressed: () => Navigator.pop(c, [l, d]),
                    style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                    child: const Text('Continue', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
                  ),
                ]),
              ),
            );
          });
        },
      );
      if (picked == null || !mounted) return;
      lang = picked[0];
      partD = picked[1];
    }
    final mockId = '${mockBase(exam, m)}_$lang';
    await Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => TestFlow(
        user: widget.user,
        exam: exam,
        mockId: mockId,
        lang: lang,
        partD: exam.partD ? partD : null,
        paid: _owned.isNotEmpty,
        title: '${exam.name} Mock ${m.n}',
      ),
    ));
    _afterTest();
  }

  void _afterTest() {
    _loadAtt();
    if (mounted) AppRating.maybeAsk(context, widget.exam.id); // TSSC-APPRATING-V1
    _loadResume();
    if (mounted) setState(() => _version++);
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final first = _name.split(' ').first;
    final mocks = _mocks ?? const <MockItem>[];
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) {
        if (didPop) return;
        if (_tab == 0) {
          widget.onChangeExam();
        } else {
          setState(() => _tab = 0);
        }
      },
      child: Stack(children: [examTheme(context, exam, Container(decoration: softBg, child: Scaffold(
      backgroundColor: Colors.transparent,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        surfaceTintColor: Colors.transparent,
        scrolledUnderElevation: 0,
        automaticallyImplyLeading: false,
        // TSSC-HOME-TILES-V1: purple header on the Home tab
        foregroundColor: _tab == 0 ? Colors.white : null,
        iconTheme: _tab == 0 ? const IconThemeData(color: Colors.white) : null,
        systemOverlayStyle: _tab == 0 ? SystemUiOverlayStyle.light : null,
        flexibleSpace: _tab == 0
            ? Container(
                decoration: const BoxDecoration(
                  gradient: LinearGradient(colors: [Color(0xFF6D28D9), Color(0xFF4C1D95)], begin: Alignment.topLeft, end: Alignment.bottomRight),
                  borderRadius: BorderRadius.vertical(bottom: Radius.circular(22)),
                ),
              )
            : null,
        leading: IconButton(
          tooltip: _tab == 0 ? 'Change exam' : 'Back',
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: () => _tab == 0 ? widget.onChangeExam() : setState(() => _tab = 0),
        ),
        titleSpacing: 0,
        toolbarHeight: 58,
        title: InkWell(
          borderRadius: BorderRadius.circular(20),
          onTap: widget.onChangeExam,
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 4),
            child: Row(mainAxisSize: MainAxisSize.min, children: [
              Icon3D(exam.icon3d, size: 32),
              const SizedBox(width: 8),
              Flexible(child: Text(exam.name, maxLines: 1, overflow: TextOverflow.ellipsis, style: _tab == 0 ? baloo(21, color: Colors.white) : baloo(24))),
              const SizedBox(width: 2),
              Icon(Icons.expand_more, size: 24, color: _tab == 0 ? Colors.white : exam.c1),
            ]),
          ),
        ),
        actions: [
          if (_tab != 1)
            Padding(
              padding: const EdgeInsets.only(right: 6),
              child: Center(
                child: Tooltip(
                  message: 'Plans',
                  child: InkWell(
                    borderRadius: BorderRadius.circular(14),
                    onTap: () => setState(() => _tab = 1),
                    child: Container(
                      width: 38,
                      height: 38,
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(colors: [Color(0xFFFDE68A), Color(0xFFF59E0B)], begin: Alignment.topLeft, end: Alignment.bottomRight),
                        borderRadius: BorderRadius.circular(14),
                        boxShadow: const [BoxShadow(color: Color(0x40F59E0B), blurRadius: 10, offset: Offset(0, 4))],
                      ),
                      child: const Icon(Icons.workspace_premium, color: Colors.white, size: 22),
                    ),
                  ),
                ),
              ),
            ),
          if (_tab == 0)
            Padding(
              padding: const EdgeInsets.only(right: 12),
              child: Center(child: NameCard(name: first, color: exam.c1, onTap: () => setState(() => _tab = 5))),
            )
          else
            IconButton(tooltip: 'Home', icon: const Icon(Icons.home_rounded), onPressed: () => setState(() => _tab = 0)),
        ],
      ),
      body: IndexedStack(
        index: _tab,
        children: [
          _HomeTab(
            user: widget.user,
            exam: exam,
            hasPass: _hasPass,
            price: _owned.isNotEmpty ? null : _price, // paid students see only the Full Access upgrade
            mocks: mocks,
            loaded: _mocks != null,
            attempted: _attempted,
            isOpen: _open,
            resuming: _resuming,
            onMocks: () => setState(() => _tab = 2),
            onDashboard: () => setState(() => _tab = 3),
            onPyq: () => setState(() => _tab = 4),
            onSubjects: () => Navigator.of(context).push(MaterialPageRoute(
              builder: (_) => SubjectMocksScreen(
                user: widget.user,
                exam: exam,
                mocks: _mocks ?? const [],
                hasPass: _hasPass,
                paid: _owned.isNotEmpty,
                attempted: _attempted,
                onReturn: _afterTest,
                onBuy: () => _buy(),
              ),
            )),
            onCa: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => CurrentAffairsScreen(user: widget.user, exam: exam, paid: _owned.isNotEmpty, attempted: _attempted, onReturn: _afterTest))),
            onChapterPyq: () => Navigator.of(context).push(MaterialPageRoute(
              builder: (_) => ChapterPyqScreen(user: widget.user, exam: exam, paid: _owned.isNotEmpty, attempted: _attempted, onReturn: _afterTest),
            )),
            onChapters: () => Navigator.of(context).push(MaterialPageRoute(
              builder: (_) => ChapterSubjectsScreen(user: widget.user, exam: exam, paid: _owned.isNotEmpty, attempted: _attempted, onReturn: _afterTest),
            )),
            onStart: _startMock,
            onSoon: _soon,
          ),
          PlansTab(exam: exam, owned: _owned),
          if (_mockSub.isNotEmpty && _tier == 1 && _mocks != null)
            // Mocks tab, one subject picked: the subject-wise list, with a "Full mock" chip to come back
            SubjectMocksScreen(
              key: ValueKey('mock-sub-${exam.id}'),
              embedded: true,
              initialSubject: _mockSub,
              onFull: () => setState(() => _mockSub = ''),
              user: widget.user,
              exam: exam,
              mocks: _mocks ?? const [],
              hasPass: _hasPass,
              paid: _owned.isNotEmpty,
              attempted: _attempted,
              onReturn: _afterTest,
              onBuy: () => _buy(),
            )
          else
          _MocksTab(
            top2: exam.id == 'ssc-cgl' && aicCgl.on ? AicEntryCard(user: widget.user, exam: exam, series: aicCgl) : null,
            top1: exam.id == 'ssc-chsl' && aicChsl.on ? AicEntryCard(user: widget.user, exam: exam, series: aicChsl) : null,
            onSubject: (k) => setState(() => _mockSub = k),
            exam: exam,
            mocks: _mocks,
            failed: _mocksFailed,
            hasPass: _hasPass,
            price: _owned.isNotEmpty ? null : _price, // paid students see only the Full Access upgrade
            tier: _tier,
            attempted: _attempted,
            isOpen: _open,
            resuming: _resuming,
            onTier: (t) => setState(() => _tier = t),
            onStart: _mockTap,
            onRetake: _startMock,
            last: _last,
            onSoon: _soon,
            onRetry: _loadMocks,
          ),
          DashboardTab(user: widget.user, exam: exam, version: _version, onMocks: () => setState(() => _tab = 2)),
          PyqTab(
            user: widget.user,
            exam: exam,
            attempted: _attempted,
            resume: _resume,
            last: _last,
            paid: _owned.isNotEmpty,
            onReturn: _afterTest,
          ),
          _MeTab(name: _name, exam: exam, onChangeExam: widget.onChangeExam, onSignOut: _signOut, onDashboard: () => setState(() => _tab = 3)),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        height: 64,
        backgroundColor: Colors.white,
        surfaceTintColor: Colors.white,
        indicatorColor: Color.lerp(Colors.white, exam.c1, 0.16),
        selectedIndex: _tab,
        onDestinationSelected: (i) => setState(() => _tab = i),
        destinations: [
          const NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
          const NavigationDestination(icon: Icon(Icons.workspace_premium_outlined), selectedIcon: Icon(Icons.workspace_premium), label: 'Plans'),
          const NavigationDestination(icon: Icon(Icons.track_changes_outlined), selectedIcon: Icon(Icons.track_changes), label: 'Mocks'),
          const NavigationDestination(icon: Icon(Icons.insights_outlined), selectedIcon: Icon(Icons.insights), label: 'Dashboard'),
          const NavigationDestination(icon: Icon(Icons.description_outlined), selectedIcon: Icon(Icons.description), label: 'PYQs'),
          NavigationDestination(
            icon: ValueListenableBuilder<int?>(
              valueListenable: AppUpdater.available,
              builder: (_, v, __) => Badge(isLabelVisible: v != null, child: const Icon(Icons.person_outline)),
            ),
            selectedIcon: ValueListenableBuilder<int?>(
              valueListenable: AppUpdater.available,
              builder: (_, v, __) => Badge(isLabelVisible: v != null, child: const Icon(Icons.person)),
            ),
            label: 'Me',
          ),
        ],
      ),
    ))),
        if (!_ready) _wait('Please wait while we load your account…', opaque: true),
        // Google Play has the payment but the bank has not confirmed it yet (UPI, net banking)
        ValueListenableBuilder<String?>(
          valueListenable: Billing.I.waiting,
          builder: (_, w, __) => w == null
              ? const SizedBox.shrink()
              : Positioned(
                  left: 12,
                  right: 12,
                  bottom: 86 + MediaQuery.of(context).padding.bottom,
                  child: Material(
                    elevation: 8,
                    color: const Color(0xFFFFFBEB),
                    borderRadius: BorderRadius.circular(18),
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(16, 14, 12, 12),
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisSize: MainAxisSize.min, children: [
                        const Row(children: [
                          SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2.6, color: Color(0xFFD97706))),
                          SizedBox(width: 12),
                          Expanded(child: Text('Waiting for Google Play to confirm your payment', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 15, color: softInk))),
                        ]),
                        const SizedBox(height: 8),
                        const Text('UPI and net banking payments can take a few minutes. You can keep using the app: your pass opens by itself as soon as it is confirmed. Please do not pay again.',
                            style: TextStyle(fontSize: 13.5, height: 1.4, color: softInk)),
                        Align(
                          alignment: Alignment.centerRight,
                          child: TextButton(onPressed: Billing.I.recheck, child: const Text('Check now')),
                        ),
                      ]),
                    ),
                  ),
                ),
        ),
        ValueListenableBuilder<bool>(
          valueListenable: Billing.I.busy,
          builder: (_, b, __) => b ? _wait('Confirming your payment…\nPlease wait, do not close the app.') : const SizedBox.shrink(),
        ),
      ]),
    );
  }

  /// A "please wait" layer over the whole screen. [opaque]: nothing behind it shows.
  Widget _wait(String text, {bool opaque = false}) => Positioned.fill(
        child: Material(
          color: opaque ? softBgMid : Colors.black.withValues(alpha: .45),
          child: Center(
            child: Container(
              margin: const EdgeInsets.all(32),
              padding: const EdgeInsets.fromLTRB(22, 24, 22, 22),
              decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(20)),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                SizedBox(width: 34, height: 34, child: CircularProgressIndicator(strokeWidth: 3.2, color: widget.exam.c1)),
                const SizedBox(height: 16),
                Text(text, textAlign: TextAlign.center, style: const TextStyle(fontSize: 15.5, fontWeight: FontWeight.w700, color: softInk, height: 1.4)),
              ]),
            ),
          ),
        ),
      );
}

/// The pass banner: price and Unlock for non-owners, "Pass active" for owners.
class _PassCard extends StatelessWidget {
  final Exam exam;
  final bool hasPass;
  final int? price;
  final String title;
  final String sub;
  final VoidCallback onTap;
  final bool plain;
  const _PassCard({required this.exam, required this.hasPass, required this.price, required this.title, required this.sub, required this.onTap, this.plain = false});

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: Ink(
        decoration: plain
            ? softCard(radius: 20, glow: const Color(0xFF6D28D9))
            : BoxDecoration(
                borderRadius: BorderRadius.circular(24),
                gradient: LinearGradient(colors: [Color.lerp(exam.c1, Colors.white, 0.22)!, exam.c1], begin: Alignment.topLeft, end: Alignment.bottomRight),
                boxShadow: [BoxShadow(color: exam.c1.withValues(alpha: .28), blurRadius: 22, offset: const Offset(0, 10))],
              ),
        child: InkWell(
          borderRadius: BorderRadius.circular(24),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 15),
            child: Row(children: [
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(title, maxLines: 1, overflow: TextOverflow.ellipsis, style: plain ? baloo(19) : baloo(20, color: Colors.white)),
                  const SizedBox(height: 2),
                  Text(sub, maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(color: plain ? softMuted : const Color(0xEEFFFFFF), fontSize: 14, fontWeight: FontWeight.w600)),
                ]),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 9),
                decoration: BoxDecoration(color: !plain ? Colors.white : (hasPass ? const Color(0xFFDDF5EA) : const Color(0xFF6D28D9)), borderRadius: BorderRadius.circular(plain ? 999 : 14)),
                child: Text(hasPass ? '✓ Active' : (price == null ? 'Unlock' : 'Unlock ₹$price'), style: TextStyle(color: !plain ? exam.c1 : (hasPass ? const Color(0xFF0B6B49) : Colors.white), fontWeight: FontWeight.w900, fontSize: 14.5)),
              ),
            ]),
          ),
        ),
      ),
    );
  }
}

class _HomeTab extends StatelessWidget {
  final User user;
  final Exam exam;
  final bool hasPass;
  final int? price;
  final List<MockItem> mocks;
  final bool loaded;
  final Set<String> attempted;
  final bool Function(MockItem) isOpen;
  final bool Function(MockItem) resuming;
  final VoidCallback onMocks;
  final VoidCallback onDashboard;
  final VoidCallback onPyq;
  final VoidCallback onChapters;
  final VoidCallback onChapterPyq;
  final VoidCallback onSubjects;
  final VoidCallback onCa;
  final void Function(MockItem) onStart;
  final void Function(String) onSoon;
  const _HomeTab({
    required this.user,
    required this.exam,
    required this.hasPass,
    required this.price,
    required this.mocks,
    required this.loaded,
    required this.attempted,
    required this.isOpen,
    required this.resuming,
    required this.onMocks,
    required this.onDashboard,
    required this.onPyq,
    required this.onChapters,
    required this.onChapterPyq,
    required this.onSubjects,
    required this.onCa,
    required this.onStart,
    required this.onSoon,
  });

  @override
  Widget build(BuildContext context) {
    final live = mocks.length;
    final open = mocks.where(isOpen).length;
    final done = mocks.where((m) => isAttempted(attempted, exam, m)).length;
    MockItem? next;
    for (final m in mocks) {
      if (isOpen(m) && resuming(m)) {
        next = m;
        break;
      }
    }
    if (next == null) {
      for (final m in mocks) {
        if (isOpen(m) && !isAttempted(attempted, exam, m)) {
          next = m;
          break;
        }
      }
    }
    final resumeNext = next != null && resuming(next);
    final hasAic = (exam.id == 'ssc-cgl' && aicCgl.on) || (exam.id == 'ssc-chsl' && aicChsl.on);
    String num(int v) => loaded ? '$v' : '–';
    // "View details" on each card: what is inside, in plain words
    final passLine = hasPass ? 'Your pass is active, so every one of them is open for you.' : 'Mocks 1 to ${exam.free} are free. The ${exam.name} pass opens all of them for 1 year.';
    final subj = subjectChoices(exam).map((x) => x.$2).join(', ');
    // TSSC-LISTUI-V2: the exact number of mocks in each part, counted from the live list
    int tc(int t) => mocks.where((m) => m.tier == t).length;
    final tierParts = [
      if (tc(1) > 0) '${tc(1)} Tier 1',
      if (tc(2) > 0) '${tc(2)} Tier 2',
      if (tc(3) > 0) '${tc(3)} Statistics (JSO)',
      if (tc(4) > 0) '${tc(4)} Finance (AAO)',
    ];
    final split = loaded && exam.tier2 && tierParts.length > 1;
    final mocksSub = split ? '${tc(1)} Tier 1 + ${tc(2)} Tier 2' : exam.mocks;
    final dMocks = [
      if (split) '$live mocks in all: ${tierParts.join(' + ')}.' else '${exam.mocks}, full length, on the latest ${exam.name} pattern.',
      if (split) 'Full length, on the latest ${exam.name} pattern.',
      if (exam.meta.isNotEmpty) 'Each ${split ? 'Tier 1 ' : ''}mock: ${exam.meta}, the same as the real exam.',
      if (loaded && !split) '$live mocks are live now; new ones keep being added.',
      passLine,
      'Hindi and English, with a solution for every question.',
      'After each test: your score, accuracy, time taken and section-wise analysis.',
      'Leave a test half-way and resume it later from the same question.',
    ];
    final dPyq = [
      'Real question papers from previous ${exam.name} exams, exactly as asked.',
      'Attempt the full paper on the real exam clock.',
      if (exam.secTests.isEmpty && subj.isNotEmpty) 'Or attempt just one subject of a paper: $subj.',
      'Hindi and English, with solutions.',
      'Free for everyone.',
    ];
    final dChap = [
      'Short practice tests for every chapter of every subject.',
      'Two levels: Level 1 to build the basics, Level 2 at real exam level.',
      'Solutions after every test, so you learn the method.',
      'Best for fixing weak topics you find in mocks.',
      'Free for everyone.',
    ];
    final dChapPyq = [
      'Previous year questions sorted chapter by chapter.',
      'See exactly what the exam asks from each topic, and how often.',
      'Solutions with every question.',
      'Free for everyone.',
    ];
    final dSub = [
      'One section of a full mock on its own shorter timer.',
      if (subj.isNotEmpty) 'Sections: $subj.',
      'Good for daily practice when you do not have time for a full mock.',
      'Your score is saved separately from the full mock.',
      hasPass ? 'Your pass is active, so every section of every mock is open.' : 'Free for Mocks 1 to ${exam.free}; the pass opens the rest.',
    ];
    final dCa = [
      'Daily current affairs, updated every day.',
      'Topic-wise collections: read a topic, then attempt a short test on it.',
      'Covers the questions asked in the GK section of the exam.',
      'Free for everyone.',
    ];
    // TSSC-TABLET-V1: the six tiles, laid out 2 per row on phones and 3 per row on wide screens
    final tiles = <Widget>[
          _Tile('target', 'Mock tests', mocksSub, const Color(0xFF1552C4), onMocks, details: dMocks, glyph: Icons.track_changes_rounded, g1: const Color(0xFF2F7BEA), g2: const Color(0xFF1552C4), tag: hasPass ? const SoftTag('PREMIUM', Color(0xFF6B4A00), Color(0xFFFDE68A)) : SoftTag('${exam.free} FREE', const Color(0xFF0B5E3F), const Color(0xFFC9F5DC))),
          _Tile('paper', 'PYQs', 'Real exam papers', const Color(0xFF5B2BD1), onPyq, details: dPyq, glyph: Icons.description_outlined, g1: const Color(0xFF8B5CF6), g2: const Color(0xFF5B2BD1), tag: const SoftTag('FREE', Color(0xFF0B5E3F), Color(0xFFC9F5DC))),
          _Tile('book', 'Chapter tests', '2 levels', const Color(0xFFD2560A), onChapters, details: dChap, glyph: Icons.layers_outlined, g1: const Color(0xFFF58A1F), g2: const Color(0xFFD2560A), tag: const SoftTag('FREE', Color(0xFF0B5E3F), Color(0xFFC9F5DC))),
          _Tile('folder', 'Chapter PYQs', 'Real questions', const Color(0xFF0B7A55), onChapterPyq, details: dChapPyq, glyph: Icons.menu_book_rounded, g1: const Color(0xFF19A974), g2: const Color(0xFF0B7A55), tag: const SoftTag('FREE', Color(0xFF0B5E3F), Color(0xFFC9F5DC))),
          if (exam.hasSubjectMocks)
            _Tile('puzzle', 'Subject mocks', 'Sectional', const Color(0xFFC21A55), onSubjects, details: dSub, glyph: Icons.dashboard_customize_outlined, g1: const Color(0xFFF0477B), g2: const Color(0xFFC21A55), tag: hasPass ? const SoftTag('PREMIUM', Color(0xFF6B4A00), Color(0xFFFDE68A)) : SoftTag('${exam.free} FREE', const Color(0xFF0B5E3F), const Color(0xFFC9F5DC))),
          _Tile('news', 'Current affairs', 'Daily · Topic-wise', const Color(0xFF4A22B3), onCa, details: dCa, glyph: Icons.emoji_events_outlined, g1: const Color(0xFF7C4DE8), g2: const Color(0xFF4A22B3), tag: const SoftTag('FREE', Color(0xFF0B5E3F), Color(0xFFC9F5DC))),
    ];
    return LayoutBuilder(builder: (context, bc) {
      final cols = bc.maxWidth >= 840 ? 3 : 2;
      final rows = <List<Widget>>[];
      for (var i = 0; i < tiles.length; i += cols) {
        rows.add(tiles.sublist(i, i + cols > tiles.length ? tiles.length : i + cols));
      }
      Widget row(List<Widget> r) => Row(children: [
            for (var i = 0; i < r.length; i++) ...[if (i > 0) const SizedBox(width: 8), r[i]],
          ]);
      // a short screen (a phone or tablet held sideways) cannot fit everything: it scrolls
      final scroll = bc.maxHeight < 300 + rows.length * 112;
      final top = <Widget>[
          const UpdateStrip(),
          _PassCard(
            exam: exam,
            hasPass: hasPass,
            price: price,
            title: '${exam.name} Mock Pass',
            sub: '${exam.mocks} · Hindi & English · valid 1 year',
            onTap: () => hasPass ? onMocks() : onSoon('Buying a pass'),
            plain: true,
          ),
          const SizedBox(height: 8),
          Row(children: [
            _Stat('Mocks live', num(live), exam, color: const Color(0xFF1552C4)),
            const SizedBox(width: 8),
            _Stat(hasPass ? 'Unlocked' : 'Free for you', num(open), exam, color: const Color(0xFF0B7A55)),
            const SizedBox(width: 8),
            _Stat('Attempted ›', num(done), exam, onTap: onDashboard, color: const Color(0xFFC21A55)),
          ]),
          // TSSC-AIC-HOME-V2: the Challenge Mock card takes the place of the "Start Mock" card
          if (!hasAic) const SizedBox(height: 8),
          if (!hasAic)
          Material(
            color: Colors.transparent,
            child: Ink(
              decoration: softCard(radius: 20, glow: exam.c1),
              child: InkWell(
                borderRadius: BorderRadius.circular(20),
                onTap: next == null ? onMocks : () => onStart(next!),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 11),
                  child: Row(children: [
                    Expanded(
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text(
                          next == null
                              ? 'See all mocks'
                              : resumeNext ? 'Resume Mock ${next.n}' : 'Start ${tierWord(next.tier)}Mock ${next.n}${next.n <= freeMocks(exam, next) ? ' · free' : ''}',
                          style: baloo(19),
                        ),
                        Text(next != null && next.tier == 1 ? exam.meta : 'Full-length papers with solutions', style: const TextStyle(fontSize: 14, color: softMuted, fontWeight: FontWeight.w600)),
                      ]),
                    ),
                    Container(
                      width: 44,
                      height: 44,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        gradient: const LinearGradient(colors: [Color(0xFF34D399), Color(0xFF059669)], begin: Alignment.topCenter, end: Alignment.bottomCenter),
                        boxShadow: [BoxShadow(color: const Color(0xFF059669).withValues(alpha: .35), blurRadius: 12, offset: const Offset(0, 5))],
                      ),
                      child: const Icon(Icons.play_arrow_rounded, color: Colors.white, size: 28),
                    ),
                  ]),
                ),
              ),
            ),
          ),
          // TSSC-AIC-HOME-V1: Challenge Mock card on SSC CGL and SSC CHSL
          if (exam.id == 'ssc-cgl' && aicCgl.on) ...[const SizedBox(height: 8), AicHomeCard(user: user, exam: exam, series: aicCgl)],
          if (exam.id == 'ssc-chsl' && aicChsl.on) ...[const SizedBox(height: 8), AicHomeCard(user: user, exam: exam, series: aicChsl)],
          const SizedBox(height: 8),
      ];
      final body = Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        mainAxisSize: scroll ? MainAxisSize.min : MainAxisSize.max,
        children: [
          ...top,
          if (scroll)
            for (var i = 0; i < rows.length; i++) ...[if (i > 0) const SizedBox(height: 8), SizedBox(height: 150, child: row(rows[i]))]
          else
            Expanded(
              child: Column(children: [
                for (var i = 0; i < rows.length; i++) ...[if (i > 0) const SizedBox(height: 8), Expanded(child: row(rows[i]))],
              ]),
            ),
        ],
      );
      return scroll
          ? SingleChildScrollView(padding: const EdgeInsets.fromLTRB(12, 10, 12, 10), child: body)
          : Padding(padding: const EdgeInsets.fromLTRB(12, 10, 12, 10), child: body);
    });
  }
}

class _Stat extends StatelessWidget {
  final String label;
  final String value;
  final Exam exam;
  final VoidCallback? onTap;
  final Color? color;
  const _Stat(this.label, this.value, this.exam, {this.onTap, this.color});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: GestureDetector(onTap: onTap, child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
        decoration: softCard(radius: 18),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(value, style: baloo(25, color: color ?? exam.c1)),
          Text(label, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 13.5, color: softMuted, fontWeight: FontWeight.w700)),
        ]),
      )),
    );
  }
}

class _Tile extends StatelessWidget {
  final String icon;
  final String title;
  final String sub;
  final Color accent;
  final VoidCallback onTap;
  final Widget? tag;
  final List<String>? details;
  final IconData glyph;
  final Color g1, g2;
  const _Tile(this.icon, this.title, this.sub, this.accent, this.onTap, {this.tag, this.details, required this.glyph, required this.g1, required this.g2});

  void _showDetails(BuildContext context) {
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (c) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 14, 20, 16),
          child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
            Center(child: Container(width: 40, height: 4, decoration: BoxDecoration(color: const Color(0xFFE2E8F0), borderRadius: BorderRadius.circular(4)))),
            const SizedBox(height: 14),
            Row(children: [
              Container(width: 48, height: 48, alignment: Alignment.center, decoration: BoxDecoration(borderRadius: BorderRadius.circular(14), gradient: LinearGradient(colors: [g1, g2], begin: Alignment.topLeft, end: Alignment.bottomRight)), child: Icon(glyph, color: Colors.white, size: 28)),
              const SizedBox(width: 12),
              Expanded(child: Text(title, style: baloo(21))),
              if (tag != null) tag!,
            ]),
            const SizedBox(height: 12),
            for (final l in details!)
              Padding(
                padding: const EdgeInsets.only(bottom: 9),
                child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Padding(padding: const EdgeInsets.only(top: 2), child: Icon(Icons.check_circle_rounded, size: 18, color: accent)),
                  const SizedBox(width: 10),
                  Expanded(child: Text(l, style: const TextStyle(fontSize: 15, height: 1.4, color: softInk))),
                ]),
              ),
            const SizedBox(height: 8),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                style: FilledButton.styleFrom(backgroundColor: accent, padding: const EdgeInsets.symmetric(vertical: 14), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                onPressed: () {
                  Navigator.pop(c);
                  onTap();
                },
                child: Text('Open $title', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
              ),
            ),
          ]),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // TSSC-HOME-TILES-V1: colour tile, white icon in a soft box, white text
    return Expanded(
      child: Material(
        color: Colors.transparent,
        child: Ink(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(22),
            gradient: LinearGradient(colors: [g1, g2], begin: Alignment.topLeft, end: Alignment.bottomRight),
            boxShadow: [BoxShadow(color: g2.withValues(alpha: .28), blurRadius: 14, offset: const Offset(0, 6))],
          ),
          child: InkWell(
            borderRadius: BorderRadius.circular(22),
            onTap: onTap,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(22),
              child: Stack(children: [
                Positioned(
                  right: -28,
                  bottom: -28,
                  child: Container(width: 100, height: 100, decoration: const BoxDecoration(shape: BoxShape.circle, color: Color(0x1FFFFFFF))),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(14, 12, 12, 10),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Container(
                        width: 48,
                        height: 48,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(color: const Color(0x3DFFFFFF), borderRadius: BorderRadius.circular(14)),
                        child: Icon(glyph, color: Colors.white, size: 28),
                      ),
                      const Spacer(),
                      if (tag != null) tag!,
                    ]),
                    const Spacer(),
                    Text(title, maxLines: 1, overflow: TextOverflow.ellipsis, style: baloo(18, color: Colors.white)),
                    Text(sub, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 13.5, color: Colors.white, fontWeight: FontWeight.w700)),
                    if (details != null)
                      InkWell(
                        borderRadius: BorderRadius.circular(8),
                        onTap: () => _showDetails(context),
                        child: const Padding(
                          padding: EdgeInsets.fromLTRB(0, 3, 8, 2),
                          child: Text('View details ›', style: TextStyle(fontSize: 12.5, color: Colors.white, fontWeight: FontWeight.w800)),
                        ),
                      ),
                  ]),
                ),
              ]),
            ),
          ),
        ),
      ),
    );
  }
}

class _MocksTab extends StatelessWidget {
  final Exam exam;
  final List<MockItem>? mocks;
  final bool failed;
  final bool hasPass;
  final int? price;
  final int tier;
  final Set<String> attempted;
  final bool Function(MockItem) isOpen;
  final bool Function(MockItem) resuming;
  final void Function(int) onTier;
  final void Function(String) onSubject;
  final void Function(MockItem) onStart;
  final void Function(MockItem) onRetake;
  final void Function(String) onSoon;
  final VoidCallback onRetry;
  final Map<String, Map<String, dynamic>> last;
  final Widget? top2; // shown on top of the Tier 2 list (SSC CGL: the All India Challenge entry)
  final Widget? top1; // shown on top of the Tier 1 list (SSC CHSL: the All India Challenge entry)
  const _MocksTab({
    this.top2,
    this.top1,
    required this.onSubject,
    required this.last,
    required this.onRetake,
    required this.exam,
    required this.mocks,
    required this.failed,
    required this.hasPass,
    required this.price,
    required this.tier,
    required this.attempted,
    required this.isOpen,
    required this.resuming,
    required this.onTier,
    required this.onStart,
    required this.onSoon,
    required this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    if (failed) {
      return _Placeholder(icon: Icons.wifi_off, title: 'Could not load the mocks', text: 'Check your internet and try again.', action: 'Retry', onAction: onRetry);
    }
    final all = mocks;
    if (all == null) return const Center(child: CircularProgressIndicator());
    final list = all.where((m) => m.tier == tier).toList();
    final open = list.where(isOpen).length;
    final rows = <Widget>[];
    var offered = hasPass;
    var ri = 0;
    for (final m in list) {
      if (!offered && !isOpen(m)) {
        offered = true;
        rows.add(Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: _PassCard(
            exam: exam,
            hasPass: false,
            price: price,
            title: 'Unlock all ${exam.mocks}',
            sub: 'One payment · valid 1 year',
            onTap: () => onSoon('Buying a pass'),
          ),
        ));
      }
      rows.add(_MockRow(exam: exam, m: m, open: isOpen(m), free: m.n <= freeMocks(exam, m), premium: hasPass && m.n > freeMocks(exam, m), done: isAttempted(attempted, exam, m), resume: resuming(m), last: last[mockBase(exam, m)], onStart: onStart, onRetake: onRetake, bar: rowBar(ri++)));
    }
    final doneN = list.where((m) => isAttempted(attempted, exam, m)).length;
    final head = <Widget>[
      SoftSummary(
        icon: exam.icon3d,
        title: '$doneN of ${list.length} done',
        progress: list.isEmpty ? 0 : doneN / list.length,
        sub: hasPass ? 'All ${list.length} unlocked · Hindi & English' : '$open free · ${list.length - open} locked',
        accent: exam.c1,
        pct: true,
      ),
      const SizedBox(height: 12),
      // TSSC-LISTUI-V2: big tier buttons with the number of mocks in each
      if (exam.tier2)
        Builder(builder: (_) {
          int cnt(int t) => all.where((m) => m.tier == t).length;
          final tiers = [1, 2, if (cnt(3) > 0) 3, if (cnt(4) > 0) 4];
          const names = {1: 'Tier 1', 2: 'Tier 2', 3: 'Statistics (JSO)', 4: 'Finance (AAO)'};
          const icons = {1: Icons.emoji_events_outlined, 2: Icons.layers_outlined, 3: Icons.bar_chart_rounded, 4: Icons.account_balance_outlined};
          return Padding(
            padding: EdgeInsets.only(bottom: tiers.length <= 2 ? 12 : 0),
            child: SoftTabs(
              items: [for (final t in tiers) ('${names[t]} (${cnt(t)})', icons[t]!)],
              index: tiers.indexOf(tier) < 0 ? 0 : tiers.indexOf(tier),
              accent: exam.c1,
              onTap: (i) => onTier(tiers[i]),
            ),
          );
        }),
      if (tier == 2 && top2 != null) top2!,
      if (tier != 2 && top1 != null) top1!,
      // subject-wise mocks: the same chips as the PYQ tab (Tier 1 only)
      if (tier == 1 && list.isNotEmpty && subjectChoices(exam).isNotEmpty)
        SubjectTiles(
          items: [('', 'Full Mock'), for (final s in subjectChoices(exam)) (s.$1, s.$2)],
          selected: '',
          accent: exam.c1,
          onTap: (k) {
            if (k.isNotEmpty) onSubject(k);
          },
        ),
    ];
    if (list.isEmpty) {
      return ListView(padding: const EdgeInsets.fromLTRB(16, 8, 16, 14), children: [
        ...head,
        const SizedBox(height: 260, child: _Placeholder(icon: Icons.hourglass_empty, title: 'Releasing soon', text: 'These mocks are on the way.')),
      ]);
    }
    return ListView.builder(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 14),
      itemCount: head.length + rows.length,
      itemBuilder: (_, i) => i < head.length ? head[i] : rows[i - head.length],
    );
  }
}

class _Chip extends StatelessWidget {
  final String text;
  final bool on;
  final Exam exam;
  final VoidCallback onTap;
  const _Chip(this.text, this.on, this.exam, this.onTap);

  @override
  Widget build(BuildContext context) {
    return Material(
      color: on ? exam.c1 : Colors.white,
      borderRadius: BorderRadius.circular(20),
      child: InkWell(
        borderRadius: BorderRadius.circular(20),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Text(text, style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: on ? Colors.white : const Color(0xFF334155))),
        ),
      ),
    );
  }
}

class _MockRow extends StatelessWidget {
  final Exam exam;
  final MockItem m;
  final bool open;
  final bool free;
  final bool premium;
  final bool done;
  final bool resume;
  final Map<String, dynamic>? last;
  final void Function(MockItem) onStart;
  final void Function(MockItem) onRetake;
  final Color? bar;
  const _MockRow({this.bar, required this.onRetake, required this.exam, required this.m, required this.open, required this.free, required this.premium, required this.done, required this.resume, required this.last, required this.onStart});

  @override
  Widget build(BuildContext context) {
    final langs = [if (m.en) 'EN', if (m.hi) 'हिंदी'].join(', ');
    final parts = exam.meta.split(' · ');
    final state = !open ? RowState.locked : (resume ? RowState.progress : (done ? RowState.done : RowState.todo));
    final a = last;
    final meta = <(IconData, String)>[
      if (state == RowState.done && a != null) (Icons.calendar_today_outlined, shortDate(attemptMs(a))) else if (m.tier == 1 && parts.isNotEmpty) (Icons.help_outline_rounded, parts.first) else (Icons.help_outline_rounded, m.tier >= 3 ? '100 Qs' : 'Tier 2'),
      (Icons.schedule_rounded, m.tier == 1 && parts.length > 1 ? parts[1] : (m.tier >= 3 ? '120 min' : '135 min')),
    ];
    return TestRow(
      tags: [
        if (free) const SoftTag.free(),
        if (!free) const SoftTag.premium(),
      ],
      title: '${exam.name.replaceFirst('SSC ', '')} ${tierWord(m.tier)}Mock ${m.n.toString().padLeft(2, '0')}',
      sub: '${m.tier == 3 ? 'Paper II · Statistics' : m.tier == 4 ? 'Paper III · Finance & Economics' : 'Mixed (All Subjects)'}${langs.isNotEmpty ? ' · $langs' : ''}',
      meta: meta,
      state: state,
      score: state == RowState.done && a != null ? '${n1(marksOf(a))} / ${n1(maxOf(a))}' : null,
      accent: exam.c1,
      bar: bar,
      onTap: () => onStart(m),
      onAction: state == RowState.done ? () => onRetake(m) : null,
      // TSSC-T2TIMING-V1: SSC CGL Tier 2 mocks run on the 2026 timing (five timed parts)
      note: exam.id == 'ssc-cgl' && m.tier == 2 ? const TimingNote() : null,
    );
  }
}

class _Tag extends StatelessWidget {
  final String text;
  final Color fg;
  final Color bg;
  const _Tag(this.text, this.fg, this.bg);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(8)),
      child: Text(text, style: TextStyle(color: fg, fontSize: 12, fontWeight: FontWeight.w800)),
    );
  }
}

class _MeTab extends StatelessWidget {
  final String name;
  final Exam exam;
  final VoidCallback onChangeExam;
  final VoidCallback onSignOut;
  final VoidCallback onDashboard;
  const _MeTab({required this.name, required this.exam, required this.onChangeExam, required this.onSignOut, required this.onDashboard});

  @override
  Widget build(BuildContext context) {
    final u = FirebaseAuth.instance.currentUser;
    final prov = u == null || u.providerData.isEmpty ? '' : u.providerData.first.providerId;
    final method = prov == 'google.com' ? 'Google' : (prov == 'phone' ? 'Phone OTP' : (prov == 'password' ? 'Email' : 'TrickySSC account'));
    final joined = u?.metadata.creationTime;
    const mo = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    Widget row(Widget icon, String title, String sub, VoidCallback onTap, {Color? color}) => Padding(
          padding: const EdgeInsets.only(bottom: 10),
          child: Material(
            color: Colors.transparent,
            child: Ink(
              decoration: softCard(radius: 18),
              child: InkWell(
                borderRadius: BorderRadius.circular(18),
                onTap: onTap,
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(12, 10, 8, 10),
                  child: Row(children: [
                    Container(width: 46, height: 46, alignment: Alignment.center, decoration: softWell(), child: icon),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text(title, style: baloo(17, color: color ?? softInk)),
                        if (sub.isNotEmpty) Text(sub, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 13, color: softMuted, fontWeight: FontWeight.w600)),
                      ]),
                    ),
                    Icon(Icons.chevron_right_rounded, color: color ?? exam.c1),
                  ]),
                ),
              ),
            ),
          ),
        );
    return ListView(
      padding: EdgeInsets.fromLTRB(14, 8, 14, 20 + MediaQuery.of(context).padding.bottom),
      children: [
        Container(
          padding: const EdgeInsets.all(16),
          margin: const EdgeInsets.only(bottom: 12),
          decoration: softCard(radius: 22, glow: exam.c1),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              CircleAvatar(
                radius: 30,
                backgroundColor: exam.c1,
                backgroundImage: u?.photoURL != null ? NetworkImage(u!.photoURL!) : null,
                child: u?.photoURL == null ? Text(name.isEmpty ? 'S' : name[0].toUpperCase(), style: baloo(26, color: Colors.white)) : null,
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(name, maxLines: 1, overflow: TextOverflow.ellipsis, style: baloo(21)),
                  Text(u?.email ?? u?.phoneNumber ?? '', maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: softMuted, fontWeight: FontWeight.w600)),
                ]),
              ),
            ]),
            const SizedBox(height: 12),
            Wrap(spacing: 8, runSpacing: 6, children: [
              SoftTag('${prov == 'google.com' ? '🔵' : '📱'} Signed in with $method', const Color(0xFF1D4ED8), const Color(0xFFDBEAFE)),
              if (joined != null) SoftTag('Member since ${mo[joined.month - 1]} ${joined.year}', const Color(0xFF475569), const Color(0xFFF1F5F9)),
            ]),
          ]),
        ),
        row(const Text('📈', style: TextStyle(fontSize: 22)), 'My dashboard', 'Scores, ranks, cut-off gap and weak areas', onDashboard),
        row(Icon3D(exam.icon3d, size: 34), 'My exam', '${exam.name} · tap to change', onChangeExam),
        if (u != null)
          row(const Text('🧾', style: TextStyle(fontSize: 22)), 'My orders', 'Your plan, purchases and payment IDs',
              () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => OrdersPage(x: DashCtx(u, exam, const [], '', 'GEN'))))),
        if (u != null)
          row(const Text('👤', style: TextStyle(fontSize: 22)), 'My profile', 'Name, phone and login method',
              () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => ProfilePage(x: DashCtx(u, exam, const [], '', 'GEN'))))),
        if (u != null)
          row(const Text('🐞', style: TextStyle(fontSize: 22)), 'Report an issue', 'Something not working in the app? Tell us',
              () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => ReportIssuePage(user: u, exam: exam)))),
        if (u != null)
          row(const Text('⭐', style: TextStyle(fontSize: 22)), 'Rate this app', 'Stars and a suggestion, both optional', () => AppRating.show(context, exam.id)),
        // TSSC-INAPPUPDATE-V1: App updates, with a red dot while a newer version is waiting
        ValueListenableBuilder<int?>(
          valueListenable: AppUpdater.available,
          builder: (_, v, __) => row(
            Badge(isLabelVisible: v != null, child: const Icon(Icons.system_update_rounded, color: Color(0xFF16A34A), size: 26)),
            v != null ? 'Update available' : 'App updates',
            v != null ? 'Tap to install the new version' : 'Version $appVersion · tap to check',
            () => v != null ? AppUpdater.update(context) : AppUpdater.checkNow(context),
            color: v != null ? const Color(0xFF15803D) : null,
          ),
        ),
        row(const Text('🏛️', style: TextStyle(fontSize: 22)), 'Disclaimer & official sources', 'Not a government app · ssc.gov.in, rrbapply.gov.in',
            () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => AboutPage(color: exam.c1)))),
        row(const Text('✉️', style: TextStyle(fontSize: 22)), 'Help', 'Write to contact@trickyssc.com', () {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Write to contact@trickyssc.com — we reply within 24 hours.')));
        }),
        row(const Icon(Icons.logout_rounded, color: Color(0xFFDC2626)), 'Sign out', '', onSignOut, color: const Color(0xFFDC2626)),
        const Padding(
          padding: EdgeInsets.fromLTRB(6, 10, 6, 0),
          child: Text('TrickySSC is a private practice app, not affiliated with SSC, RRB or any government body. Official information: ssc.gov.in, rrbapply.gov.in.',
              textAlign: TextAlign.center, style: TextStyle(fontSize: 12, color: softMuted, height: 1.35)),
        ),
      ],
    );
  }
}

class _Placeholder extends StatelessWidget {
  final IconData icon;
  final String title;
  final String text;
  final String? action;
  final VoidCallback? onAction;
  const _Placeholder({required this.icon, required this.title, required this.text, this.action, this.onAction});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(28),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Icon(icon, size: 46, color: const Color(0xFF94A3B8)),
          const SizedBox(height: 12),
          Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
          const SizedBox(height: 4),
          Text(text, textAlign: TextAlign.center, style: const TextStyle(color: Color(0xFF64748B))),
          if (action != null) ...[const SizedBox(height: 14), FilledButton(onPressed: onAction, child: Text(action!))],
        ]),
      ),
    );
  }
}

/// The student's name in a small card (top bar and wherever the name is shown).
class NameCard extends StatelessWidget {
  final String name;
  final Color color;
  final VoidCallback? onTap;
  const NameCard({super.key, required this.name, required this.color, this.onTap});

  @override
  Widget build(BuildContext context) {
    final n = name.trim().isEmpty ? 'Student' : name.trim();
    return InkWell(
      borderRadius: BorderRadius.circular(999),
      onTap: onTap,
      child: Container(
        constraints: const BoxConstraints(maxWidth: 118),
        padding: const EdgeInsets.fromLTRB(4, 4, 11, 4),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(999),
          border: Border.all(color: color.withValues(alpha: .25)),
          boxShadow: [BoxShadow(color: color.withValues(alpha: .16), blurRadius: 10, offset: const Offset(0, 4))],
        ),
        child: Row(mainAxisSize: MainAxisSize.min, children: [
          Container(
            width: 28,
            height: 28,
            alignment: Alignment.center,
            decoration: BoxDecoration(shape: BoxShape.circle, gradient: LinearGradient(colors: [Color.lerp(color, Colors.white, .3)!, color])),
            child: Text(n[0].toUpperCase(), style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 14)),
          ),
          const SizedBox(width: 6),
          Flexible(child: Text(n, maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(fontWeight: FontWeight.w800, fontSize: 14, color: color))),
        ]),
      ),
    );
  }
}
