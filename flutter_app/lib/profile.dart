// The student's profile in users/{uid}, kept the same as the website's login does,
// so app sign-ups show on candidates.html with name, mobile / email, login method and join date.
// Also stamps the app version and last app open, so the admin pages can tell app users apart.
import 'dart:async';
import 'dart:io';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'ui/soft.dart';

/// Set by the build: --dart-define=APP_VERSION=2.0.<run>
const String appVersion = String.fromEnvironment('APP_VERSION', defaultValue: 'dev');

const _phoneKey = 'tssc_app_login_phone';

/// Remember the mobile number used for the OTP (the custom-token account has no phone of its own).
Future<void> rememberLoginPhone(String phone) async => (await SharedPreferences.getInstance()).setString(_phoneKey, phone);
Future<String> _loginPhone() async => (await SharedPreferences.getInstance()).getString(_phoneKey) ?? '';

String _method(User u) {
  for (final p in u.providerData) {
    if (p.providerId == 'google.com') return 'google';
  }
  return u.email != null && u.email!.isNotEmpty ? 'google' : 'phone';
}

class ProfileGate extends StatefulWidget {
  final User user;
  final Widget child;
  const ProfileGate({super.key, required this.user, required this.child});

  @override
  State<ProfileGate> createState() => _ProfileGateState();
}

class _ProfileGateState extends State<ProfileGate> with WidgetsBindingObserver {
  bool _loading = true, _needName = false, _busy = false;
  String _msg = '';
  final _name = TextEditingController();

  DocumentReference<Map<String, dynamic>> get _ref => FirebaseFirestore.instance.collection('users').doc(widget.user.uid);

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    // "live on the app" for the testers page: a small stamp every 5 minutes while the app is on screen
    _beat = Timer.periodic(const Duration(minutes: 5), (_) {
      if (_front) _seen();
    });
    _check();
  }

  Timer? _beat;
  bool _front = true;

  void _seen() {
    _ref.set({'lastAppSeen': FieldValue.serverTimestamp()}, SetOptions(merge: true)).catchError((_) {});
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    final now = state == AppLifecycleState.resumed;
    if (now && !_front) _seen();
    _front = now;
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _beat?.cancel();
    _name.dispose();
    super.dispose();
  }

  Future<void> _check() async {
    final u = widget.user;
    try {
      final snap = await _ref.get();
      final d = snap.data() ?? const <String, dynamic>{};
      final name = '${d['name'] ?? ''}'.trim();
      final method = _method(u);
      final gName = (u.displayName ?? '').trim();
      if (!snap.exists || name.isEmpty || name == 'Student') {
        if (method == 'google' && gName.isNotEmpty) {
          await _write(gName, created: snap.exists);
        } else {
          _name.text = gName == 'Student' ? '' : gName;
          if (mounted) setState(() => _needName = true);
        }
      } else if ((u.displayName ?? '').isEmpty) {
        try {
          await u.updateDisplayName(name);
        } catch (_) {}
      }
    } catch (_) {
      // offline or unreadable: let the student in, try again next open
    }
    _stampApp();
    if (mounted) setState(() => _loading = false);
  }

  /// Same fields as the website's login (login-modal.js). [created]: the doc already exists.
  Future<void> _write(String name, {required bool created}) async {
    final u = widget.user;
    final method = _method(u);
    final phone = method == 'phone' ? ((u.phoneNumber ?? '').isNotEmpty ? u.phoneNumber! : await _loginPhone()) : (u.phoneNumber ?? '');
    final body = <String, dynamic>{
      'uid': u.uid,
      'name': name,
      'email': u.email ?? '',
      'photoURL': u.photoURL ?? '',
      'loginMethod': method,
      if (phone.isNotEmpty) 'phone': phone,
      if (!created) 'createdAt': FieldValue.serverTimestamp(),
      if (!created) 'totalTests': 0,
      if (!created) 'avgScore': 0,
      if (!created) 'bestScore': 0,
      if (!created) 'signupVia': 'android-app',
    };
    await _ref.set(body, SetOptions(merge: true));
    try {
      await u.updateDisplayName(name);
    } catch (_) {}
  }

  /// App marker for the admin pages. Kept separate so a rules change can never block the profile.
  void _stampApp() {
    String dev = '';
    try {
      dev = '${Platform.operatingSystem} ${Platform.operatingSystemVersion}';
    } catch (_) {}
    // Google's review / pre-launch devices are emulators with debug builds of Android
    final review = RegExp(r'sdk_gphone|emulator|generic_x86|userdebug|dev-keys|test-keys', caseSensitive: false).hasMatch(dev);
    _ref.set({
      'appUser': true,
      'appDevice': dev,
      'appReview': review, // this open only: the same account can later be used on a real phone
      'appVersion': appVersion,
      'lastAppOpen': FieldValue.serverTimestamp(),
      'lastAppSeen': FieldValue.serverTimestamp(),
      'appOpens': FieldValue.increment(1),
      'appDays': FieldValue.arrayUnion([DateTime.now().toUtc().add(const Duration(hours: 5, minutes: 30)).toIso8601String().substring(0, 10)]),
    }, SetOptions(merge: true)).catchError((_) {});
  }

  Future<void> _save() async {
    final n = _name.text.trim();
    if (n.length < 2) {
      setState(() => _msg = 'Please enter your full name.');
      return;
    }
    setState(() {
      _busy = true;
      _msg = '';
    });
    try {
      final exists = (await _ref.get()).exists;
      await _write(n, created: exists);
      _stampApp();
      if (mounted) setState(() => _needName = false);
    } catch (_) {
      if (mounted) setState(() => _msg = 'Could not save. Please check your internet and try again.');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return Container(
        decoration: softBg,
        child: const Scaffold(backgroundColor: Colors.transparent, body: Center(child: CircularProgressIndicator(color: Color(0xFFFF6B00)))),
      );
    }
    if (!_needName) return widget.child;
    return Container(
      decoration: softBg,
      child: Scaffold(
        backgroundColor: Colors.transparent,
        body: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(22),
              child: Container(
                padding: const EdgeInsets.fromLTRB(20, 22, 20, 18),
                decoration: softCard(radius: 22, glow: const Color(0xFFFF6B00)),
                child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                  Image.asset('assets/logo.png', width: 64, height: 64),
                  const SizedBox(height: 12),
                  Text('One last step', textAlign: TextAlign.center, style: baloo(24)),
                  const SizedBox(height: 4),
                  const Text('Your name appears on leaderboards and your dashboard.', textAlign: TextAlign.center, style: TextStyle(color: softMuted, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _name,
                    textCapitalization: TextCapitalization.words,
                    textInputAction: TextInputAction.done,
                    onSubmitted: (_) => _busy ? null : _save(),
                    decoration: InputDecoration(
                      labelText: 'Full name',
                      filled: true,
                      fillColor: Colors.white,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(14)),
                    ),
                  ),
                  if (_msg.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 8), child: Text(_msg, style: const TextStyle(color: Color(0xFFDC2626), fontWeight: FontWeight.w700))),
                  const SizedBox(height: 14),
                  FilledButton(
                    onPressed: _busy ? null : _save,
                    style: FilledButton.styleFrom(backgroundColor: const Color(0xFFFF6B00), minimumSize: const Size.fromHeight(52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                    child: Text(_busy ? 'Saving…' : 'Start learning →', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
                  ),
                  TextButton(onPressed: _busy ? null : () => FirebaseAuth.instance.signOut(), child: const Text('Use another account')),
                ]),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
