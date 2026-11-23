// TSSC-APPRATING-V1: "Rate the app" popup - stars and a suggestion, both optional.
// Asked on Home after a finished test (from the 2nd test, at most once in 7 days, never after a
// submit), and any time from the Me tab. Saved like an app issue report (question_reports, source
// 'app-issue'), so it shows on admin-app-reports.html. 4-5 stars then open Google Play's rating sheet.
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:in_app_review/in_app_review.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'test/report.dart' show addWithApp;

class AppRating {
  static const _kTests = 'tssc_rate_tests', _kDone = 'tssc_rate_done', _kAsked = 'tssc_rate_asked';
  static bool _pending = false;

  /// A test was finished and saved (called from the result screen).
  static Future<void> testFinished() async {
    try {
      final p = await SharedPreferences.getInstance();
      await p.setInt(_kTests, (p.getInt(_kTests) ?? 0) + 1);
      _pending = true;
    } catch (_) {}
  }

  /// Back on Home after a test: ask, if it is time to.
  static Future<void> maybeAsk(BuildContext context, String examId) async {
    if (!_pending) return;
    _pending = false;
    try {
      final p = await SharedPreferences.getInstance();
      if (p.getBool(_kDone) == true) return;
      if ((p.getInt(_kTests) ?? 0) < 2) return;
      final now = DateTime.now().millisecondsSinceEpoch;
      if (now - (p.getInt(_kAsked) ?? 0) < 7 * 24 * 3600 * 1000) return;
      await Future.delayed(const Duration(milliseconds: 700));
      if (!context.mounted) return;
      await p.setInt(_kAsked, now);
      await show(context, examId, auto: true);
    } catch (_) {}
  }

  static Future<void> show(BuildContext context, String examId, {bool auto = false}) async {
    final u = FirebaseAuth.instance.currentUser;
    if (u == null) return;
    int stars = 0;
    bool busy = false;
    String err = '';
    final ctl = TextEditingController();

    final sent = await showDialog<int>(
      context: context,
      builder: (c) => StatefulBuilder(builder: (c, setS) {
        Future<void> submit() async {
          final text = ctl.text.trim();
          if (stars < 1 && text.isEmpty) return;
          setS(() {
            busy = true;
            err = '';
          });
          try {
            await addWithApp('question_reports', {
              'source': 'app-issue',
              'target': 'app',
              'mockId': 'app-issue',
              'qNum': '-',
              'position': 0,
              'subject': examId,
              'reason': stars > 0 ? '⭐ App rating: $stars★' : '💡 App suggestion',
              'note': '${text.isEmpty ? '(no suggestion written)' : text}\n\n— Reply email: ${(u.email ?? '').isEmpty ? '-' : u.email} · Phone: ${(u.phoneNumber ?? '').isEmpty ? '-' : u.phoneNumber} · Device: -',
              'uid': u.uid,
              'name': u.displayName ?? '',
              'testName': 'App rating',
              'createdAt': FieldValue.serverTimestamp(),
            });
            try {
              (await SharedPreferences.getInstance()).setBool(_kDone, true);
            } catch (_) {}
            if (c.mounted) Navigator.of(c).pop(stars);
          } catch (_) {
            setS(() {
              busy = false;
              err = 'Could not send right now. Check your internet and try again.';
            });
          }
        }

        return Dialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
          insetPadding: const EdgeInsets.symmetric(horizontal: 28, vertical: 24),
          child: SingleChildScrollView(
            padding: const EdgeInsets.fromLTRB(20, 22, 20, 14),
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              Container(
                width: 52,
                height: 52,
                decoration: const BoxDecoration(color: Color(0xFFEDE9FE), shape: BoxShape.circle),
                child: const Icon(Icons.star_rounded, color: Color(0xFF6D28D9), size: 30),
              ),
              const SizedBox(height: 10),
              const Text('Enjoying TrickySSC?', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
              const SizedBox(height: 4),
              const Text('Rate the app. Both are optional.', style: TextStyle(fontSize: 13, color: Color(0xFF64748B))),
              const SizedBox(height: 12),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                for (int i = 1; i <= 5; i++)
                  InkWell(
                    borderRadius: BorderRadius.circular(20),
                    onTap: busy ? null : () => setS(() => stars = i),
                    child: Padding(
                      padding: const EdgeInsets.all(4),
                      child: Icon(i <= stars ? Icons.star_rounded : Icons.star_outline_rounded, size: 36, color: i <= stars ? const Color(0xFFF59E0B) : const Color(0xFF94A3B8)),
                    ),
                  ),
              ]),
              const SizedBox(height: 12),
              TextField(
                controller: ctl,
                enabled: !busy,
                minLines: 3,
                maxLines: 5,
                maxLength: 500,
                textCapitalization: TextCapitalization.sentences,
                onChanged: (_) => setS(() {}),
                style: const TextStyle(fontSize: 14),
                decoration: InputDecoration(
                  hintText: 'Any suggestion to make the app better',
                  hintStyle: const TextStyle(fontSize: 13.5, color: Color(0xFF94A3B8)),
                  counterText: '',
                  filled: true,
                  fillColor: const Color(0xFFF8FAFC),
                  contentPadding: const EdgeInsets.all(12),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFE2E8F0))),
                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFE2E8F0))),
                ),
              ),
              if (err.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 8), child: Text(err, textAlign: TextAlign.center, style: const TextStyle(fontSize: 12.5, color: Color(0xFFDC2626)))),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                child: FilledButton(
                  style: FilledButton.styleFrom(backgroundColor: const Color(0xFF6D28D9), padding: const EdgeInsets.symmetric(vertical: 13), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                  onPressed: busy || (stars < 1 && ctl.text.trim().isEmpty) ? null : submit,
                  child: Text(busy ? 'Sending…' : 'Submit', style: const TextStyle(fontWeight: FontWeight.w800)),
                ),
              ),
              TextButton(
                onPressed: busy ? null : () => Navigator.of(c).pop(),
                child: const Text('Not now', style: TextStyle(color: Color(0xFF64748B), fontWeight: FontWeight.w700)),
              ),
            ]),
          ),
        );
      }),
    );
    if (sent == null) return;
    if (context.mounted) {
      ScaffoldMessenger.maybeOf(context)?.showSnackBar(const SnackBar(content: Text('Thank you! Your feedback has reached us.')));
    }
    if (sent >= 4) {
      try {
        final r = InAppReview.instance;
        if (auto && await r.isAvailable()) {
          await r.requestReview();
        } else {
          await r.openStoreListing();
        }
      } catch (_) {}
    }
  }
}
