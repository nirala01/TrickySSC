import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';

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
  String _name = 'Student';
  Set<String> _owned = <String>{};
  Set<String> _attempted = <String>{};
  Map<String, Map<String, dynamic>> _last = {};
  Map<String, List<String>> _resume = {};
  int _version = 0;
  List<MockItem>? _mocks;
  bool _mocksFailed = false;
  int? _price;

  bool get _hasPass => _owned.contains(widget.exam.pass);

  @override
  void _toHome() {
    if (mounted && _tab != 0) setState(() => _tab = 0);
  }

  @override
  void dispose() {
    homeRequest.removeListener(_toHome);
    Billing.I
      ..onMessage = null
      ..onGranted = null;
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    homeRequest.addListener(_toHome);
    Billing.I
      ..onMessage = _say
      ..onGranted = () {
        loadOwned(widget.user.uid).then((o) {
          if (mounted) setState(() => _owned = o);
        });
      }
      ..start();
    _loadMocks();
    loadName(widget.user.uid, widget.user.displayName).then((n) {
      if (mounted) setState(() => _name = n);
    });
    loadOwnedOrNull(widget.user.uid).then((o) {
      if (!mounted) return;
      setState(() => _owned = o ?? <String>{});
      if (o != null) _welcome(o);
    });
    _loadAtt();
    _loadResume();
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

  /// On entering the app: a student with no pass sees Full Access (with a link to every other pass);
  /// a paid student sees only their upgrade; full access sees nothing.
  Future<void> _welcome(Set<String> owned) async {
    if (_welcomed == widget.user.uid) return;
    _welcomed = widget.user.uid;
    if (owned.isEmpty) {
      await Billing.I.showFullAccessPopup(context, onExplore: () {
        if (mounted) setState(() => _tab = 1);
      });
    } else if (!exams.every((e) => owned.contains(e.pass))) {
      final q = await Billing.I.quote();
      if (mounted && q != null && q.offer) await Billing.I.showUpgradeSheet(context, widget.exam, q);
    }
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
      child: examTheme(context, exam, Container(decoration: softBg, child: Scaffold(
      backgroundColor: Colors.transparent,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        surfaceTintColor: Colors.transparent,
        scrolledUnderElevation: 0,
        automaticallyImplyLeading: false,
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
              Flexible(child: Text(exam.name, maxLines: 1, overflow: TextOverflow.ellipsis, style: baloo(_tab == 0 ? 21 : 24))),
              const SizedBox(width: 2),
              Icon(Icons.expand_more, size: 24, color: exam.c1),
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
          _MocksTab(
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
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.workspace_premium_outlined), selectedIcon: Icon(Icons.workspace_premium), label: 'Plans'),
          NavigationDestination(icon: Icon(Icons.track_changes_outlined), selectedIcon: Icon(Icons.track_changes), label: 'Mocks'),
          NavigationDestination(icon: Icon(Icons.insights_outlined), selectedIcon: Icon(Icons.insights), label: 'Dashboard'),
          NavigationDestination(icon: Icon(Icons.description_outlined), selectedIcon: Icon(Icons.description), label: 'PYQs'),
          NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person), label: 'Me'),
        ],
      ),
    ))));
  }
}

/// The pass banner: price and Unlock for non-owners, "Pass active" for owners.
class _PassCard extends StatelessWidget {
  final Exam exam;
  final bool hasPass;
  final int? price;
  final String title;
  final String sub;
  final VoidCallback onTap;
  const _PassCard({required this.exam, required this.hasPass, required this.price, required this.title, required this.sub, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: Ink(
        decoration: BoxDecoration(
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
                  Text(title, maxLines: 1, overflow: TextOverflow.ellipsis, style: baloo(20, color: Colors.white)),
                  const SizedBox(height: 2),
                  Text(sub, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Color(0xEEFFFFFF), fontSize: 14, fontWeight: FontWeight.w600)),
                ]),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 9),
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14)),
                child: Text(hasPass ? '✓ Active' : (price == null ? 'Unlock' : 'Unlock ₹$price'), style: TextStyle(color: exam.c1, fontWeight: FontWeight.w900, fontSize: 14.5)),
              ),
            ]),
          ),
        ),
      ),
    );
  }
}

class _HomeTab extends StatelessWidget {
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
    String num(int v) => loaded ? '$v' : '–';
    return Padding(
      padding: const EdgeInsets.fromLTRB(12, 10, 12, 10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _PassCard(
            exam: exam,
            hasPass: hasPass,
            price: price,
            title: '${exam.name} Mock Pass',
            sub: '${exam.mocks} · Hindi & English · valid 1 year',
            onTap: () => hasPass ? onMocks() : onSoon('Buying a pass'),
          ),
          const SizedBox(height: 8),
          Row(children: [
            _Stat('Mocks live', num(live), exam),
            const SizedBox(width: 8),
            _Stat(hasPass ? 'Unlocked' : 'Free for you', num(open), exam),
            const SizedBox(width: 8),
            _Stat('Attempted ›', num(done), exam, onTap: onDashboard),
          ]),
          const SizedBox(height: 8),
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
          const SizedBox(height: 8),
          Expanded(
            child: Column(children: [
              Expanded(
                child: Row(children: [
                  _Tile('target', 'Mock tests', exam.mocks, exam.c1, onMocks, tag: hasPass ? const SoftTag.premium() : SoftTag('${exam.free} FREE', const Color(0xFF047857), const Color(0xFFD1FAE5))),
                  const SizedBox(width: 8),
                  _Tile('paper', 'Previous year papers', 'Real exam papers', exam.c1, onPyq, tag: const SoftTag.free()),
                ]),
              ),
              const SizedBox(height: 8),
              Expanded(
                child: Row(children: [
                  _Tile('book', 'Chapter tests', '2 levels', exam.c1, onChapters, tag: const SoftTag.free()),
                  const SizedBox(width: 8),
                  _Tile('folder', 'Chapter PYQs', 'Real questions', exam.c1, onChapterPyq, tag: const SoftTag.free()),
                ]),
              ),
              const SizedBox(height: 8),
              Expanded(
                child: Row(children: [
                  // TSSC-SM-APP-V1: an exam with no subject mocks (RRB Station Master) shows no Subject mocks tile
                  if (exam.hasSubjectMocks) ...[
                    _Tile('puzzle', 'Subject mocks', 'Sectional', exam.c1, onSubjects, tag: hasPass ? const SoftTag.premium() : SoftTag('${exam.free} FREE', const Color(0xFF047857), const Color(0xFFD1FAE5))),
                    const SizedBox(width: 8),
                  ],
                  _Tile('news', 'Current affairs', 'Daily · Topic-wise', exam.c1, onCa, tag: const SoftTag.free()),
                ]),
              ),
            ]),
          ),
        ],
      ),
    );
  }
}

class _Stat extends StatelessWidget {
  final String label;
  final String value;
  final Exam exam;
  final VoidCallback? onTap;
  const _Stat(this.label, this.value, this.exam, {this.onTap});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: GestureDetector(onTap: onTap, child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
        decoration: softCard(radius: 18),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(value, style: baloo(25, color: exam.c1)),
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
  const _Tile(this.icon, this.title, this.sub, this.accent, this.onTap, {this.tag});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Material(
        color: Colors.transparent,
        child: Ink(
          decoration: softCard(radius: 22),
          child: InkWell(
            borderRadius: BorderRadius.circular(22),
            onTap: onTap,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(14, 12, 12, 12),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Container(width: 56, height: 56, alignment: Alignment.center, decoration: softWell(), child: Icon3D(icon, size: 42)),
                  const Spacer(),
                  if (tag != null) tag!,
                ]),
                const Spacer(),
                Text(title, maxLines: 2, overflow: TextOverflow.ellipsis, style: baloo(18)),
                const SizedBox(height: 2),
                Text(sub, maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(fontSize: 14, color: accent, fontWeight: FontWeight.w800)),
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
  final void Function(MockItem) onStart;
  final void Function(MockItem) onRetake;
  final void Function(String) onSoon;
  final VoidCallback onRetry;
  final Map<String, Map<String, dynamic>> last;
  const _MocksTab({
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
      rows.add(_MockRow(exam: exam, m: m, open: isOpen(m), free: m.n <= freeMocks(exam, m), premium: hasPass && m.n > freeMocks(exam, m), done: isAttempted(attempted, exam, m), resume: resuming(m), last: last[mockBase(exam, m)], onStart: onStart, onRetake: onRetake));
    }
    final doneN = list.where((m) => isAttempted(attempted, exam, m)).length;
    final head = <Widget>[
      SoftSummary(
        icon: exam.icon3d,
        title: '$doneN of ${list.length} done',
        progress: list.isEmpty ? 0 : doneN / list.length,
        sub: hasPass ? 'All ${list.length} unlocked · Hindi & English' : '$open free · ${list.length - open} locked',
        accent: exam.c1,
      ),
      const SizedBox(height: 12),
      if (exam.tier2)
        Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: Row(children: [
            Expanded(
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                clipBehavior: Clip.none,
                child: Row(children: [
                  SoftChip('Tier 1', tier == 1, exam.c1, () => onTier(1)),
                  SoftChip('Tier 2', tier == 2, exam.c1, () => onTier(2)),
                  if (all.any((m) => m.tier == 3)) SoftChip('Statistics (JSO)', tier == 3, exam.c1, () => onTier(3)),
                  if (all.any((m) => m.tier == 4)) SoftChip('Finance (AAO)', tier == 4, exam.c1, () => onTier(4)),
                ]),
              ),
            ),
          ]),
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
  const _MockRow({required this.onRetake, required this.exam, required this.m, required this.open, required this.free, required this.premium, required this.done, required this.resume, required this.last, required this.onStart});

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
      onTap: () => onStart(m),
      onAction: state == RowState.done ? () => onRetake(m) : null,
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
