// TSSC-APPISSUE-V2 (2026-11-18): Me tab -> "Report an issue with the app".
// Saved in the existing `question_reports` collection (no new Firestore rules) with
// source 'app-issue'; reply email, phone and device go in the note. The admin sees them on
// trickyssc.com/admin-app-reports.html (reports-admin.html skips them), marks them
// resolved and emails the student.
import 'dart:io' show Platform;

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../data.dart';
import '../profile.dart' show appVersion;
import '../ui/soft.dart';
import '../test/report.dart' show addWithApp;
import 'dash/ui.dart';

const _kinds = [
  ('crash', '💥 App crashes or freezes'),
  ('test', '📝 Test not loading or not saving'),
  ('payment', '💳 Payment or pass access'),
  ('login', '🔑 Sign-in problem'),
  ('content', '❓ Wrong question, answer or solution'),
  ('other', '💬 Something else'),
];

String _kindLabel(String k) => _kinds.firstWhere((e) => e.$1 == k, orElse: () => ('', '💬 Something else')).$2;

class ReportIssuePage extends StatefulWidget {
  final User user;
  final Exam exam;
  const ReportIssuePage({super.key, required this.user, required this.exam});

  @override
  State<ReportIssuePage> createState() => _ReportIssuePageState();
}

class _ReportIssuePageState extends State<ReportIssuePage> {
  final _text = TextEditingController();
  final _email = TextEditingController();
  String _kind = '';
  bool _sending = false;
  String _err = '';
  Map<String, dynamic> _profile = {};

  @override
  void initState() {
    super.initState();
    _email.text = widget.user.email ?? '';
    FirebaseFirestore.instance.collection('users').doc(widget.user.uid).get().then((d) {
      if (!mounted) return;
      _profile = d.data() ?? {};
      final e = '${_profile['email'] ?? ''}'.trim();
      if (_email.text.isEmpty && e.isNotEmpty) setState(() => _email.text = e);
    }).catchError((_) {});
  }

  @override
  void dispose() {
    _text.dispose();
    _email.dispose();
    super.dispose();
  }

  Future<void> _send() async {
    final msg = _text.text.trim(), email = _email.text.trim();
    String bad = '';
    if (_kind.isEmpty) {
      bad = 'Choose what the problem is about.';
    } else if (msg.length < 10) {
      bad = 'Please describe the problem in a few words.';
    } else if (email.isNotEmpty && !RegExp(r'^[^\s@]+@[^\s@]+\.[^\s@]+$').hasMatch(email)) {
      bad = 'Check your email address, or leave it empty.';
    }
    if (bad.isNotEmpty) {
      setState(() => _err = bad);
      return;
    }
    setState(() {
      _sending = true;
      _err = '';
    });
    final u = widget.user;
    final name = '${_profile['name'] ?? ''}'.trim().isNotEmpty ? '${_profile['name']}'.trim() : (u.displayName ?? '');
    final phone = '${_profile['phone'] ?? _profile['mobile'] ?? ''}'.trim().isNotEmpty ? '${_profile['phone'] ?? _profile['mobile']}'.trim() : (u.phoneNumber ?? '');
    String os = '';
    try {
      os = '${Platform.operatingSystem} ${Platform.operatingSystemVersion}';
    } catch (_) {}
    try {
      final body = msg.length > 800 ? msg.substring(0, 800) : msg;
      await addWithApp('question_reports', {
        'source': 'app-issue',
        'target': 'app',
        'mockId': 'app-issue',
        'qNum': '-',
        'position': 0,
        'subject': widget.exam.id,
        'reason': _kindLabel(_kind),
        'note': '$body\n\n— Reply email: ${email.isEmpty ? '-' : email} · Phone: ${phone.isEmpty ? '-' : phone} · Device: ${os.isEmpty ? '-' : os}',
        'uid': u.uid,
        'name': name,
        'testName': 'App issue report',
        'createdAt': FieldValue.serverTimestamp(),
      });
    } catch (_) {
      if (mounted) {
        setState(() {
          _sending = false;
          _err = 'Could not send right now. Check your internet and try again, or write to contact@trickyssc.com.';
        });
      }
      return;
    }
    if (!mounted) return;
    _text.clear();
    setState(() {
      _sending = false;
      _kind = '';
    });
    await showDialog<void>(
      context: context,
      builder: (c) => AlertDialog(
        backgroundColor: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Text('Thank you! 🙏', style: baloo(22)),
        content: Text(
          email.isEmpty ? 'We got your report and will look into it soon.' : 'We got your report. We will email you at $email once it is fixed.',
          style: const TextStyle(fontSize: 15, height: 1.35, color: softInk),
        ),
        actions: [TextButton(onPressed: () => Navigator.pop(c), child: const Text('OK'))],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final exam = widget.exam;
    InputDecoration box(String hint) => InputDecoration(
          hintText: hint,
          filled: true,
          fillColor: const Color(0xFFF8FAFC),
          contentPadding: const EdgeInsets.all(12),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFE2E8F0))),
          enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFE2E8F0))),
        );
    return DashPage(exam: exam, title: 'Report an issue', children: [
      PCard(title: 'What is the problem about?', children: [
        Wrap(spacing: 8, runSpacing: 8, children: [
          for (final k in _kinds)
            ChoiceChip(
              label: Text(k.$2),
              selected: _kind == k.$1,
              onSelected: _sending ? null : (_) => setState(() => _kind = k.$1),
              selectedColor: Color.lerp(Colors.white, exam.c1, .2),
              backgroundColor: Colors.white,
              labelStyle: TextStyle(fontWeight: FontWeight.w700, color: _kind == k.$1 ? exam.ink : softInk, fontSize: 13.5),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: BorderSide(color: _kind == k.$1 ? exam.c1 : const Color(0xFFE2E8F0))),
              showCheckmark: false,
            ),
        ]),
      ]),
      PCard(title: 'Tell us what happened', sub: 'Which screen or test, what you tapped and what went wrong.', children: [
        TextField(controller: _text, minLines: 4, maxLines: 8, maxLength: 800, enabled: !_sending, decoration: box('Example: CGL Mock 12 does not open after I tap Start.')),
        const SizedBox(height: 6),
        const Text('Email for our reply', style: TextStyle(fontWeight: FontWeight.w800, color: softInk)),
        const SizedBox(height: 6),
        TextField(controller: _email, enabled: !_sending, keyboardType: TextInputType.emailAddress, decoration: box('you@gmail.com')),
        if (_err.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 10), child: Text(_err, style: const TextStyle(color: Color(0xFFDC2626), fontWeight: FontWeight.w700))),
        const SizedBox(height: 12),
        FilledButton(
          onPressed: _sending ? null : _send,
          style: FilledButton.styleFrom(backgroundColor: exam.c1, minimumSize: const Size.fromHeight(50), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
          child: Text(_sending ? 'Sending…' : 'Send report', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w900)),
        ),
        const SizedBox(height: 6),
        Text('App version $appVersion and your Android version are sent with the report.', textAlign: TextAlign.center, style: const TextStyle(fontSize: 12, color: softMuted)),
      ]),
    ]);
  }
}
