import 'dart:convert';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../profile.dart';
import '../ui/soft.dart';
import 'about.dart';
import 'package:flutter/services.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:http/http.dart' as http;

import '../data.dart';
import '../firebase_options.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _phone = TextEditingController();
  final _otp = TextEditingController();
  bool _otpStep = false;
  bool _busy = false;
  String _msg = '';
  bool _msgOk = false;

  @override
  void dispose() {
    _phone.dispose();
    _otp.dispose();
    super.dispose();
  }

  void _say(String text, {bool ok = false}) {
    if (!mounted) return;
    setState(() {
      _msg = text;
      _msgOk = ok;
    });
  }

  /// Calls the TrickySSC OTP service; returns its JSON or throws its message.
  Future<Map<String, dynamic>> _call(String path, Map<String, dynamic> body) async {
    http.Response res;
    try {
      res = await http
          .post(Uri.parse(otpApi + path), headers: const {'Content-Type': 'application/json', 'Origin': 'https://trickyssc.com', 'Referer': 'https://trickyssc.com/app-login.html'}, body: jsonEncode(body))
          .timeout(const Duration(seconds: 20));
    } catch (_) {
      throw 'Could not reach the OTP service. Check your internet and try again.';
    }
    Map<String, dynamic> data = <String, dynamic>{};
    try {
      final decoded = jsonDecode(res.body);
      if (decoded is Map<String, dynamic>) data = decoded;
    } catch (_) {}
    if (res.statusCode < 200 || res.statusCode >= 300 || data['ok'] != true) {
      final m = data['message'];
      throw (m is String && m.isNotEmpty) ? m : 'OTP service error. Please try again.';
    }
    return data;
  }

  Future<void> _sendOtp() async {
    final phone = _phone.text.replaceAll(RegExp(r'\D'), '');
    if (phone.length != 10) {
      _say('Enter a valid 10-digit mobile number.');
      return;
    }
    setState(() {
      _busy = true;
      _msg = '';
    });
    try {
      await _call('/send', {'phone': phone, 'cf_token': ''});
      if (!mounted) return;
      setState(() => _otpStep = true);
      _say('OTP sent to +91 $phone', ok: true);
    } catch (e) {
      _say('$e');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  Future<void> _verifyOtp() async {
    final phone = _phone.text.replaceAll(RegExp(r'\D'), '');
    final code = _otp.text.trim();
    if (code.length != 6) {
      _say('Enter the 6-digit OTP.');
      return;
    }
    setState(() {
      _busy = true;
      _msg = '';
    });
    try {
      final v = await _call('/verify', {'phone': phone, 'otp': code});
      await rememberLoginPhone('+91$phone');
      final token = v['token'];
      if (token is! String || token.isEmpty) throw 'Could not sign in. Please try again.';
      await FirebaseAuth.instance.signInWithCustomToken(token);
    } on FirebaseAuthException catch (e) {
      _say('Could not sign in (${e.code}). Please try again.');
    } catch (e) {
      _say('$e');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  Future<void> _google() async {
    setState(() {
      _busy = true;
      _msg = '';
    });
    try {
      final g = GoogleSignIn(serverClientId: FbConfig.webClientId.isEmpty ? null : FbConfig.webClientId);
      final acct = await g.signIn();
      if (acct == null) return; // cancelled
      final auth = await acct.authentication;
      final cred = GoogleAuthProvider.credential(idToken: auth.idToken, accessToken: auth.accessToken);
      await FirebaseAuth.instance.signInWithCredential(cred);
    } on FirebaseAuthException catch (e) {
      _say('Google sign-in failed (${e.code}).');
    } catch (e) {
      _say('Google sign-in failed. Please try again or use your mobile number.');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(decoration: softBg, child: Scaffold(
      backgroundColor: Colors.transparent,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(22, 36, 22, 22),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Align(
                alignment: Alignment.centerLeft,
                child: Container(
                  margin: const EdgeInsets.only(bottom: 14),
                  decoration: BoxDecoration(shape: BoxShape.circle, boxShadow: [BoxShadow(color: const Color(0xFFFF6B00).withValues(alpha: .3), blurRadius: 22, offset: const Offset(0, 8))]),
                  child: Image.asset('assets/logo.png', width: 72, height: 72),
                ),
              ),
              Text.rich(TextSpan(children: [
                TextSpan(text: 'Tricky', style: baloo(38)),
                TextSpan(text: 'SSC', style: baloo(38, color: saffron)),
              ])),
              const SizedBox(height: 6),
              const Text('Mock tests and previous year papers for SSC and Railway exams.',
                  style: TextStyle(fontSize: 15, color: Color(0xFF475569), height: 1.35)),
              const SizedBox(height: 18),
              Container(
                padding: const EdgeInsets.fromLTRB(12, 10, 12, 10),
                decoration: BoxDecoration(
                  color: const Color(0xFFFFF7ED),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: const Color(0xFFFED7AA)),
                ),
                child: const Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Icon(Icons.info_outline, size: 18, color: Color(0xFFC2410C)),
                  SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Already a TrickySSC user? Sign in the same way you do on trickyssc.com (same mobile number or same Google account) to see all your passes and saved tests.',
                      style: TextStyle(fontSize: 13, color: Color(0xFF7C2D12), height: 1.35, fontWeight: FontWeight.w600),
                    ),
                  ),
                ]),
              ),
              const SizedBox(height: 22),
              Text(_otpStep ? 'Enter the OTP' : 'Sign in with your mobile number',
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
              const SizedBox(height: 12),
              if (!_otpStep)
                TextField(
                  controller: _phone,
                  keyboardType: TextInputType.phone,
                  maxLength: 10,
                  inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                  decoration: const InputDecoration(
                    filled: true,
                    fillColor: Colors.white,
                    prefixText: '+91  ',
                    hintText: '10-digit mobile number',
                    counterText: '',
                    border: OutlineInputBorder(borderRadius: BorderRadius.all(Radius.circular(14))),
                  ),
                  onSubmitted: (_) => _busy ? null : _sendOtp(),
                )
              else
                TextField(
                  controller: _otp,
                  autofocus: true,
                  keyboardType: TextInputType.number,
                  maxLength: 6,
                  inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                  style: const TextStyle(fontSize: 22, letterSpacing: 8, fontWeight: FontWeight.w700),
                  decoration: const InputDecoration(
                    hintText: '6-digit OTP',
                    counterText: '',
                    border: OutlineInputBorder(borderRadius: BorderRadius.all(Radius.circular(14))),
                  ),
                  onSubmitted: (_) => _busy ? null : _verifyOtp(),
                ),
              const SizedBox(height: 12),
              SizedBox(
                height: 52,
                child: FilledButton(
                  onPressed: _busy ? null : (_otpStep ? _verifyOtp : _sendOtp),
                  style: FilledButton.styleFrom(shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                  child: _busy
                      ? const SizedBox(width: 22, height: 22, child: CircularProgressIndicator(strokeWidth: 2.5, color: Colors.white))
                      : Text(_otpStep ? 'Verify OTP' : 'Send OTP', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
                ),
              ),
              if (_otpStep)
                TextButton(
                  onPressed: _busy
                      ? null
                      : () => setState(() {
                            _otpStep = false;
                            _otp.clear();
                            _msg = '';
                          }),
                  child: const Text('Change number'),
                ),
              if (_msg.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(top: 10),
                  child: Text(_msg,
                      style: TextStyle(color: _msgOk ? const Color(0xFF047857) : const Color(0xFFB91C1C), fontSize: 14, height: 1.35)),
                ),
              const SizedBox(height: 22),
              const Row(children: [
                Expanded(child: Divider()),
                Padding(padding: EdgeInsets.symmetric(horizontal: 10), child: Text('or', style: TextStyle(color: Color(0xFF94A3B8)))),
                Expanded(child: Divider()),
              ]),
              const SizedBox(height: 22),
              SizedBox(
                height: 52,
                child: OutlinedButton(
                  onPressed: _busy ? null : _google,
                  style: OutlinedButton.styleFrom(shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                  child: const Text('Continue with Google', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
                ),
              ),
              const SizedBox(height: 22),
              const GovDisclaimer(),
            ],
          ),
        ),
      ),
    ));
  }
}
