import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';

import '../data.dart';

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
  String _name = 'Student';
  Set<String> _owned = <String>{};
  late Future<List<MockItem>> _mocks;

  bool get _hasPass => _owned.contains(widget.exam.pass);

  @override
  void initState() {
    super.initState();
    _mocks = loadMocks(widget.exam);
    loadName(widget.user.uid, widget.user.displayName).then((n) {
      if (mounted) setState(() => _name = n);
    });
    loadOwned(widget.user.uid).then((o) {
      if (mounted) setState(() => _owned = o);
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

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    final first = _name.split(' ').first;
    return Scaffold(
      appBar: AppBar(
        titleSpacing: 14,
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
          _HomeTab(exam: exam, hasPass: _hasPass, onMocks: () => setState(() => _tab = 1), onSoon: _soon),
          _MocksTab(exam: exam, future: _mocks, hasPass: _hasPass, onSoon: _soon, onRetry: () => setState(() => _mocks = loadMocks(exam))),
          const _Placeholder(icon: Icons.description_outlined, title: 'Previous year papers', text: 'Coming in the next build.'),
          _MeTab(name: _name, exam: exam, onChangeExam: widget.onChangeExam, onSignOut: _signOut),
        ],
      ),
      bottomNavigationBar: NavigationBar(
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

class _HomeTab extends StatelessWidget {
  final Exam exam;
  final bool hasPass;
  final VoidCallback onMocks;
  final void Function(String) onSoon;
  const _HomeTab({required this.exam, required this.hasPass, required this.onMocks, required this.onSoon});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(14, 12, 14, 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(18),
              gradient: LinearGradient(colors: [exam.c1, exam.c2], begin: Alignment.topLeft, end: Alignment.bottomRight),
            ),
            child: Row(children: [
              Expanded(
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('${exam.name} Mock Pass', style: const TextStyle(color: Colors.white, fontSize: 19, fontWeight: FontWeight.w800)),
                  const SizedBox(height: 3),
                  Text('${exam.mocks} · Mock 1–${exam.free} free · Hindi & English', style: const TextStyle(color: Colors.white, fontSize: 12.5)),
                ]),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
                child: Text(hasPass ? '✓ Active' : 'View pass', style: TextStyle(color: exam.c1, fontWeight: FontWeight.w800)),
              ),
            ]),
          ),
          const SizedBox(height: 14),
          const Text('START PRACTISING', style: TextStyle(fontSize: 12.5, letterSpacing: .8, fontWeight: FontWeight.w800, color: Color(0xFF64748B))),
          const SizedBox(height: 8),
          Expanded(
            child: Column(children: [
              Expanded(
                child: Row(children: [
                  _Tile('🎯', 'Mock tests', exam.mocks, const Color(0xFFFFE9D6), onMocks),
                  const SizedBox(width: 10),
                  _Tile('📄', 'Previous year papers', 'Free', const Color(0xFFDBEAFE), () => onSoon('Previous year papers')),
                ]),
              ),
              const SizedBox(height: 10),
              Expanded(
                child: Row(children: [
                  _Tile('📚', 'Chapter tests', 'New questions · 2 levels', const Color(0xFFD1FAE5), () => onSoon('Chapter tests')),
                  const SizedBox(width: 10),
                  _Tile('🗂️', 'Chapter PYQs', 'Real questions by chapter', const Color(0xFFEDE9FE), () => onSoon('Chapter PYQs')),
                ]),
              ),
              const SizedBox(height: 10),
              Expanded(
                child: Row(children: [
                  _Tile('🧩', 'Subject-wise mocks', 'Sectional', const Color(0xFFFCE7F3), () => onSoon('Subject-wise mocks')),
                  const SizedBox(width: 10),
                  _Tile('📰', 'Current affairs', 'Daily', const Color(0xFFCFFAFE), () => onSoon('Current affairs')),
                ]),
              ),
            ]),
          ),
        ],
      ),
    );
  }
}

class _Tile extends StatelessWidget {
  final String icon;
  final String title;
  final String sub;
  final Color tint;
  final VoidCallback onTap;
  const _Tile(this.icon, this.title, this.sub, this.tint, this.onTap);

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Material(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        child: InkWell(
          borderRadius: BorderRadius.circular(18),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Container(
                width: 42,
                height: 42,
                alignment: Alignment.center,
                decoration: BoxDecoration(color: tint, borderRadius: BorderRadius.circular(13)),
                child: Text(icon, style: const TextStyle(fontSize: 20)),
              ),
              const Spacer(),
              Text(title, maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800, height: 1.15)),
              const SizedBox(height: 3),
              Text(sub, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 12, color: Color(0xFF64748B))),
            ]),
          ),
        ),
      ),
    );
  }
}

class _MocksTab extends StatelessWidget {
  final Exam exam;
  final Future<List<MockItem>> future;
  final bool hasPass;
  final void Function(String) onSoon;
  final VoidCallback onRetry;
  const _MocksTab({required this.exam, required this.future, required this.hasPass, required this.onSoon, required this.onRetry});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<MockItem>>(
      future: future,
      builder: (context, snap) {
        if (snap.connectionState != ConnectionState.done) return const Center(child: CircularProgressIndicator());
        if (snap.hasError) {
          return _Placeholder(icon: Icons.wifi_off, title: 'Could not load the mocks', text: 'Check your internet and try again.', action: 'Retry', onAction: onRetry);
        }
        final list = snap.data ?? const <MockItem>[];
        if (list.isEmpty) return const _Placeholder(icon: Icons.hourglass_empty, title: 'Releasing soon', text: 'Mocks for this exam are on the way.');
        return ListView.separated(
          padding: const EdgeInsets.fromLTRB(14, 12, 14, 16),
          itemCount: list.length,
          separatorBuilder: (_, __) => const SizedBox(height: 8),
          itemBuilder: (context, i) {
            final m = list[i];
            final free = m.n <= exam.free;
            final open = free || hasPass;
            return Material(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              child: InkWell(
                borderRadius: BorderRadius.circular(16),
                onTap: () => onSoon(open ? 'The test screen' : 'Buying a pass'),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  child: Row(children: [
                    Container(
                      width: 44,
                      height: 44,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(13),
                        gradient: LinearGradient(colors: [exam.c1, exam.c2]),
                      ),
                      child: Text('${m.n}', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 16)),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text('${exam.name} Mock ${m.n}', style: const TextStyle(fontSize: 15.5, fontWeight: FontWeight.w700)),
                        const SizedBox(height: 2),
                        Text([if (m.en) 'English', if (m.hi) 'हिंदी'].join(' · '), style: const TextStyle(fontSize: 12.5, color: Color(0xFF64748B))),
                      ]),
                    ),
                    if (free)
                      const _Tag('FREE', Color(0xFF047857), Color(0xFFD1FAE5))
                    else if (!hasPass)
                      const Icon(Icons.lock_outline, color: Color(0xFF94A3B8)),
                    const SizedBox(width: 6),
                    const Icon(Icons.chevron_right, color: Color(0xFFCBD5E1)),
                  ]),
                ),
              ),
            );
          },
        );
      },
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
