import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import 'data.dart';
import 'firebase_options.dart';
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
      home: FbConfig.ready ? const AuthGate() : const _SetupMissing(),
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
          return const Scaffold(body: Center(child: CircularProgressIndicator()));
        }
        final user = snap.data;
        if (user == null) return const LoginScreen();
        return ExamGate(user: user);
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
    if (!_loaded) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    final exam = _exam;
    if (exam == null) {
      final last = _last;
      return PopScope(
        canPop: last == null,
        onPopInvokedWithResult: (didPop, _) {
          if (!didPop && last != null) setState(() => _exam = last);
        },
        child: ChooseExamScreen(onPick: _pick),
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
