import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'ui/soft.dart';
import 'package:google_fonts/google_fonts.dart';

import 'data.dart';
import 'firebase_options.dart';
import 'profile.dart';
import 'screens/choose_exam.dart';
import 'screens/login.dart';
import 'screens/shell.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  if (FbConfig.ready) {
    await Firebase.initializeApp(
      options: const FirebaseOptions(
        apiKey: FbConfig.apiKey,
        appId: FbConfig.appId,
        messagingSenderId: FbConfig.senderId,
        projectId: FbConfig.projectId,
        storageBucket: FbConfig.storageBucket,
      ),
    );
  }
  await Catalog.init();
  runApp(const TrickyApp());
}

class TrickyApp extends StatelessWidget {
  const TrickyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TrickySSC',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        textTheme: GoogleFonts.nunitoTextTheme(),
        colorScheme: ColorScheme.fromSeed(seedColor: saffron, primary: saffron),
        scaffoldBackgroundColor: const Color(0xFFEEF2FF),
        appBarTheme: const AppBarTheme(backgroundColor: Color(0xFFEEF2FF), surfaceTintColor: Color(0xFFEEF2FF), elevation: 0, scrolledUnderElevation: 0),
      ),
      builder: (context, child) => LargeScreen(child: child ?? const SizedBox.shrink()),
      home: FbConfig.ready ? const AuthGate() : const _SetupMissing(),
    );
  }
}

/// TSSC-TABLET-V1: tablets and unfolded foldables.
/// The app is drawn for a phone-sized canvas; on a large screen that canvas is scaled up to fill the whole
/// display, so text, buttons and cards grow with the screen and nothing sits small in one corner.
/// Phones (shortest side under 600) are untouched.
class LargeScreen extends StatelessWidget {
  final Widget child;
  const LargeScreen({super.key, required this.child});

  static double scaleFor(Size z) {
    if (z.shortestSide < 600) return 1;
    final s = z.height >= z.width ? z.width / 480 : z.height / 640;
    return s < 1 ? 1 : (s > 1.8 ? 1.8 : s);
  }

  @override
  Widget build(BuildContext context) {
    final mq = MediaQuery.of(context);
    final s = scaleFor(mq.size);
    if (s <= 1.02) return child;
    return SizedBox.expand(
      child: FittedBox(
        fit: BoxFit.fill,
        alignment: Alignment.topLeft,
        child: SizedBox(
          width: mq.size.width / s,
          height: mq.size.height / s,
          child: MediaQuery(
            data: mq.copyWith(
              size: mq.size / s,
              padding: mq.padding / s,
              viewPadding: mq.viewPadding / s,
              viewInsets: mq.viewInsets / s,
              devicePixelRatio: mq.devicePixelRatio * s,
            ),
            child: child,
          ),
        ),
      ),
    );
  }
}

class _SetupMissing extends StatelessWidget {
  const _SetupMissing();

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Padding(
          padding: EdgeInsets.all(28),
          child: Text(
            'App setup is not finished.\n\ngoogle-services.json has not been added to flutter_app/config yet.',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 16, height: 1.4),
          ),
        ),
      ),
    );
  }
}

/// Sign in first, then choose an exam, then the app.
class AuthGate extends StatelessWidget {
  const AuthGate({super.key});

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: FirebaseAuth.instance.authStateChanges(),
      builder: (context, snap) {
        if (snap.connectionState == ConnectionState.waiting) {
          return const BrandSplash();
        }
        final user = snap.data;
        if (user == null) return const LoginScreen();
        return ProfileGate(key: ValueKey(user.uid), user: user, child: ExamGate(user: user));
      },
    );
  }
}

class ExamGate extends StatefulWidget {
  final User user;
  const ExamGate({super.key, required this.user});

  @override
  State<ExamGate> createState() => _ExamGateState();
}

class _ExamGateState extends State<ExamGate> {
  bool _loaded = false;
  Exam? _exam, _last;

  @override
  void initState() {
    super.initState();
    Prefs.exam().then((k) {
      if (!mounted) return;
      setState(() {
        _exam = examByKey(k);
        _loaded = true;
      });
    });
  }

  void _pick(Exam e) {
    Prefs.setExam(e.k);
    setState(() => _exam = e);
  }

  @override
  Widget build(BuildContext context) {
    if (!_loaded) return const BrandSplash();
    final exam = _exam;
    if (exam == null) {
      final last = _last;
      return PopScope(
        canPop: last == null,
        onPopInvokedWithResult: (didPop, _) {
          if (!didPop && last != null) setState(() => _exam = last);
        },
        child: ValueListenableBuilder<int>(valueListenable: catalogVersion, builder: (_, __, ___) => ChooseExamScreen(onPick: _pick)),
      );
    }
    return AppShell(
        key: ValueKey(exam.k),
        user: widget.user,
        exam: exam,
        onChangeExam: () => setState(() {
              _last = exam;
              _exam = null;
            }));
  }
}

/// Shown while the app starts: the same look as the Android splash, then the soft theme.
class BrandSplash extends StatelessWidget {
  const BrandSplash({super.key});

  @override
  Widget build(BuildContext context) => Container(
        decoration: softBg,
        child: Scaffold(
          backgroundColor: Colors.transparent,
          body: Center(
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              Container(
                decoration: BoxDecoration(shape: BoxShape.circle, boxShadow: [BoxShadow(color: const Color(0xFFFF6B00).withValues(alpha: .35), blurRadius: 30, offset: const Offset(0, 12))]),
                child: Image.asset('assets/logo.png', width: 110, height: 110),
              ),
              const SizedBox(height: 18),
              Text.rich(TextSpan(children: [
                TextSpan(text: 'Tricky', style: baloo(34)),
                TextSpan(text: 'SSC', style: baloo(34, color: const Color(0xFFFF6B00))),
              ])),
              const SizedBox(height: 2),
              const Text('Mocks · PYQs · Chapter tests', style: TextStyle(color: softMuted, fontWeight: FontWeight.w700)),
              const SizedBox(height: 26),
              const SizedBox(width: 26, height: 26, child: CircularProgressIndicator(strokeWidth: 3, color: Color(0xFFFF6B00))),
            ]),
          ),
        ),
      );
}
