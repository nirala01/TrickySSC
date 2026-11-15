import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';

import '../data.dart';
import '../test/engine.dart';
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
  Map<String, List<String>> _resume = {};
  List<MockItem>? _mocks;
  bool _mocksFailed = false;
  int? _price;

  bool get _hasPass => _owned.contains(widget.exam.pass);

  @override
  void initState() {
    super.initState();
    _loadMocks();
    loadName(widget.user.uid, widget.user.displayName).then((n) {
      if (mounted) setState(() => _name = n);
    });
    loadOwned(widget.user.uid).then((o) {
      if (mounted) setState(() => _owned = o);
    });
    loadAttempted(widget.user.uid).then((a) {
      if (mounted) setState(() => _attempted = a);
    });
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

  void _soon(String what) {
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

  bool _open(MockItem m) => _hasPass || m.n <= widget.exam.free;

  void _loadResume() => loadInProgress(widget.user.uid).then((r) {
        if (mounted) setState(() => _resume = r);
      });

  bool _resuming(MockItem m) => m.tier == 1 && _resume.containsKey(mockBase(widget.exam, m));

  Future<void> _startMock(MockItem m) async {
    final exam = widget.exam;
    if (!_open(m)) {
      _soon('Buying a pass');
      return;
    }
    if (m.tier == 2) {
      _soon('Tier 2 mocks');
      return;
    }
    String lang = m.en ? 'en' : 'hi';
    String partD = lang;
    final both = m.en && m.hi;
    final saved = _resume[mockBase(exam, m)];
    if (saved != null) {
      lang = saved[0];
      partD = saved[1].isEmpty ? lang : saved[1];
    } else if (both || exam.k == 'gd') {
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
                  if (exam.k == 'gd' && both) ...[
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
        partD: exam.k == 'gd' ? partD : null,
        paid: _owned.isNotEmpty,
        title: '${exam.name} Mock ${m.n}',
      ),
    ));
    loadAttempted(widget.user.uid).then((a) {
      if (mounted) setState(() => _attempted = a);
    });
    _loadResume();
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final first = _name.split(' ').first;
    final tint = Color.lerp(Colors.white, exam.c2, 0.10)!;
    final mocks = _mocks ?? const <MockItem>[];
    return Scaffold(
      backgroundColor: tint,
      appBar: AppBar(
        titleSpacing: 14,
        toolbarHeight: 52,
        title: InkWell(
          borderRadius: BorderRadius.circular(20),
          onTap: widget.onChangeExam,
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 4),
            child: Row(mainAxisSize: MainAxisSize.min, children: [
              Text(exam.icon, style: const TextStyle(fontSize: 20)),
              const SizedBox(width: 8),
              Text(exam.name, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
              const Icon(Icons.expand_more, size: 22),
            ]),
          ),
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 14),
            child: Center(child: Text('Hi, $first', style: const TextStyle(fontWeight: FontWeight.w700, color: Color(0xFF047857)))),
          ),
        ],
      ),
      body: IndexedStack(
        index: _tab,
        children: [
          _HomeTab(
            exam: exam,
            hasPass: _hasPass,
            price: _price,
            mocks: mocks,
            loaded: _mocks != null,
            attempted: _attempted,
            isOpen: _open,
            resuming: _resuming,
            onMocks: () => setState(() => _tab = 1),
            onStart: _startMock,
            onSoon: _soon,
          ),
          _MocksTab(
            exam: exam,
            mocks: _mocks,
            failed: _mocksFailed,
            hasPass: _hasPass,
            price: _price,
            tier: _tier,
            attempted: _attempted,
            isOpen: _open,
            resuming: _resuming,
            onTier: (t) => setState(() => _tier = t),
            onStart: _startMock,
            onSoon: _soon,
            onRetry: _loadMocks,
          ),
          const _Placeholder(icon: Icons.description_outlined, title: 'Previous year papers', text: 'Coming in the next build.'),
          _MeTab(name: _name, exam: exam, onChangeExam: widget.onChangeExam, onSignOut: _signOut),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        height: 64,
        backgroundColor: Colors.white,
        surfaceTintColor: Colors.white,
        indicatorColor: Color.lerp(Colors.white, exam.c2, 0.35),
        selectedIndex: _tab,
        onDestinationSelected: (i) => setState(() => _tab = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.track_changes_outlined), selectedIcon: Icon(Icons.track_changes), label: 'Mocks'),
          NavigationDestination(icon: Icon(Icons.description_outlined), selectedIcon: Icon(Icons.description), label: 'PYQs'),
          NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person), label: 'Me'),
        ],
      ),
    );
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
          borderRadius: BorderRadius.circular(16),
          gradient: LinearGradient(colors: [exam.c1, exam.c2], begin: Alignment.topLeft, end: Alignment.bottomRight),
        ),
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            child: Row(children: [
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(title, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.w800)),
                  const SizedBox(height: 2),
                  Text(sub, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(color: Colors.white, fontSize: 12.5)),
                ]),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
                child: Text(hasPass ? '✓ Active' : (price == null ? 'Unlock' : 'Unlock ₹$price'), style: TextStyle(color: exam.c1, fontWeight: FontWeight.w800)),
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
            _Stat('Attempted', num(done), exam),
          ]),
          const SizedBox(height: 8),
          Material(
            color: const Color(0xFFD1FAE5),
            borderRadius: BorderRadius.circular(14),
            child: InkWell(
              borderRadius: BorderRadius.circular(14),
              onTap: next == null ? onMocks : () => onStart(next!),
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                child: Row(children: [
                  Expanded(
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text(
                        next == null
                            ? 'See all mocks'
                            : resumeNext ? 'Resume Mock ${next.n}' : 'Start ${next.tier == 2 ? 'Tier 2 ' : ''}Mock ${next.n}${next.n <= exam.free && !hasPass ? ' · free' : ''}',
                        style: const TextStyle(fontSize: 15.5, fontWeight: FontWeight.w800, color: Color(0xFF064E3B)),
                      ),
                      Text(next != null && next.tier == 1 ? exam.meta : 'Full-length papers with solutions', style: const TextStyle(fontSize: 12, color: Color(0xFF047857))),
                    ]),
                  ),
                  const CircleAvatar(radius: 17, backgroundColor: Color(0xFF059669), child: Icon(Icons.play_arrow, color: Colors.white, size: 22)),
                ]),
              ),
            ),
          ),
          const SizedBox(height: 8),
          Expanded(
            child: Column(children: [
              Expanded(
                child: Row(children: [
                  _Tile(Icons.track_changes, 'Mock tests', exam.mocks, const Color(0xFFFFE9D6), const Color(0xFFC2410C), onMocks),
                  const SizedBox(width: 8),
                  _Tile(Icons.description, 'Year papers', 'Free', const Color(0xFFDBEAFE), const Color(0xFF1D4ED8), () => onSoon('Previous year papers')),
                ]),
              ),
              const SizedBox(height: 8),
              Expanded(
                child: Row(children: [
                  _Tile(Icons.menu_book, 'Chapter tests', '2 levels', const Color(0xFFD1FAE5), const Color(0xFF047857), () => onSoon('Chapter tests')),
                  const SizedBox(width: 8),
                  _Tile(Icons.folder_copy, 'Chapter PYQs', 'By chapter', const Color(0xFFEDE9FE), const Color(0xFF6D28D9), () => onSoon('Chapter PYQs')),
                ]),
              ),
              const SizedBox(height: 8),
              Expanded(
                child: Row(children: [
                  _Tile(Icons.extension, 'Subject mocks', 'Sectional', const Color(0xFFFCE7F3), const Color(0xFFBE185D), () => onSoon('Subject-wise mocks')),
                  const SizedBox(width: 8),
                  _Tile(Icons.newspaper, 'Current affairs', 'Daily', const Color(0xFFCFFAFE), const Color(0xFF0E7490), () => onSoon('Current affairs')),
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
  const _Stat(this.label, this.value, this.exam);

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(value, style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: exam.c1, height: 1.1)),
          Text(label, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 11.5, color: Color(0xFF64748B))),
        ]),
      ),
    );
  }
}

class _Tile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String sub;
  final Color tint;
  final Color ink;
  final VoidCallback onTap;
  const _Tile(this.icon, this.title, this.sub, this.tint, this.ink, this.onTap);

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Material(
        color: tint,
        borderRadius: BorderRadius.circular(16),
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: Row(children: [
              Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
                child: Icon(icon, color: ink, size: 22),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Column(mainAxisAlignment: MainAxisAlignment.center, crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(title, maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w800, height: 1.15, color: Color(0xFF0F172A))),
                  const SizedBox(height: 2),
                  Text(sub, maxLines: 1, overflow: TextOverflow.ellipsis, style: TextStyle(fontSize: 12, color: ink, fontWeight: FontWeight.w600)),
                ]),
              ),
            ]),
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
  final void Function(String) onSoon;
  final VoidCallback onRetry;
  const _MocksTab({
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
        rows.add(_PassCard(
          exam: exam,
          hasPass: false,
          price: price,
          title: 'Unlock all ${exam.mocks}',
          sub: 'One payment · valid 1 year',
          onTap: () => onSoon('Buying a pass'),
        ));
      }
      rows.add(_MockRow(exam: exam, m: m, open: isOpen(m), free: !hasPass && m.n <= exam.free, done: isAttempted(attempted, exam, m), resume: resuming(m), onStart: onStart));
    }
    return Column(children: [
      Padding(
        padding: const EdgeInsets.fromLTRB(12, 10, 12, 2),
        child: Row(children: [
          if (exam.tier2) ...[
            _Chip('Tier 1', tier == 1, exam, () => onTier(1)),
            const SizedBox(width: 8),
            _Chip('Tier 2', tier == 2, exam, () => onTier(2)),
          ] else
            Text('${list.length} mocks live', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w800)),
          const Spacer(),
          Text(hasPass ? 'All ${list.length} unlocked' : '$open free · ${list.length - open} locked', style: const TextStyle(fontSize: 12.5, color: Color(0xFF475569), fontWeight: FontWeight.w600)),
        ]),
      ),
      Expanded(
        child: list.isEmpty
            ? const _Placeholder(icon: Icons.hourglass_empty, title: 'Releasing soon', text: 'These mocks are on the way.')
            : ListView.separated(
                padding: const EdgeInsets.fromLTRB(12, 8, 12, 14),
                itemCount: rows.length,
                separatorBuilder: (_, __) => const SizedBox(height: 7),
                itemBuilder: (_, i) => rows[i],
              ),
      ),
    ]);
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
          child: Text(text, style: TextStyle(fontSize: 13.5, fontWeight: FontWeight.w800, color: on ? Colors.white : const Color(0xFF334155))),
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
  final bool done;
  final bool resume;
  final void Function(MockItem) onStart;
  const _MockRow({required this.exam, required this.m, required this.open, required this.free, required this.done, required this.resume, required this.onStart});

  @override
  Widget build(BuildContext context) {
    final langs = [if (m.en) 'EN', if (m.hi) 'हिंदी'].join(', ');
    final meta = [if (m.tier == 1) exam.meta else 'Tier 2 paper', if (langs.isNotEmpty) langs].join(' · ');
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(14),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: () => onStart(m),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 9),
          child: Row(children: [
            Container(
              width: 40,
              height: 40,
              alignment: Alignment.center,
              decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), color: Color.lerp(Colors.white, exam.c2, open ? 0.30 : 0.14)),
              child: Text('${m.n}', style: TextStyle(color: exam.c1, fontWeight: FontWeight.w800, fontSize: 15)),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Row(children: [
                  Text('Mock ${m.n}', style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800)),
                  if (free) ...[const SizedBox(width: 6), const _Tag('FREE', Color(0xFF047857), Color(0xFFD1FAE5))],
                  if (resume) ...[const SizedBox(width: 6), const _Tag('PAUSED', Color(0xFFB45309), Color(0xFFFEF3C7))]
                  else if (done) ...[const SizedBox(width: 6), const _Tag('DONE', Color(0xFF1D4ED8), Color(0xFFDBEAFE))],
                ]),
                const SizedBox(height: 1),
                Text(meta, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 12, color: Color(0xFF64748B))),
              ]),
            ),
            const SizedBox(width: 6),
            if (open)
              Container(
                width: 88,
                height: 36,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10),
                  gradient: LinearGradient(colors: resume ? const [Color(0xFFD97706), Color(0xFFFBBF24)] : [exam.c1, exam.c2]),
                ),
                child: Text(resume ? 'Resume' : (done ? 'Retake' : 'Start'), style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 13)),
              )
            else
              const SizedBox(width: 88, height: 36, child: Icon(Icons.lock_outline, color: Color(0xFF94A3B8), size: 22)),
          ]),
        ),
      ),
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
      child: Text(text, style: TextStyle(color: fg, fontSize: 11, fontWeight: FontWeight.w800)),
    );
  }
}

class _MeTab extends StatelessWidget {
  final String name;
  final Exam exam;
  final VoidCallback onChangeExam;
  final VoidCallback onSignOut;
  const _MeTab({required this.name, required this.exam, required this.onChangeExam, required this.onSignOut});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(14),
      children: [
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16)),
          child: Row(children: [
            CircleAvatar(
              radius: 24,
              backgroundColor: saffron,
              child: Text(name.isEmpty ? 'S' : name[0].toUpperCase(), style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.w800)),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(name, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w700)),
                const Text('Signed in', style: TextStyle(fontSize: 12.5, color: Color(0xFF64748B))),
              ]),
            ),
          ]),
        ),
        const SizedBox(height: 12),
        Material(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          clipBehavior: Clip.antiAlias,
          child: Column(children: [
            ListTile(leading: const Text('🎓', style: TextStyle(fontSize: 20)), title: const Text('My exam'), subtitle: Text('${exam.name} · tap to change'), trailing: const Icon(Icons.chevron_right), onTap: onChangeExam),
            const Divider(height: 1),
            ListTile(leading: const Icon(Icons.logout), title: const Text('Sign out'), onTap: onSignOut),
          ]),
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
