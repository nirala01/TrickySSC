import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

const String otpApi = 'https://trickyssc-otp.nirala01.workers.dev';
const Color saffron = Color(0xFFFF6B00);

class Exam {
  final String k; // short key kept on the phone
  final String id; // "exam" value in the mock_tests collection
  final String name;
  final String sub;
  final String icon;
  final String pass; // entitlement key
  final String mocks;
  final int free; // mocks 1..free are free
  final Color c1;
  final Color c2;
  const Exam(this.k, this.id, this.name, this.sub, this.icon, this.pass, this.mocks, this.free, this.c1, this.c2);
}

const List<Exam> exams = [
  Exam('cgl', 'ssc-cgl', 'SSC CGL', 'Graduate level', '🎯', 'ssc-cgl-mocks', '100 mocks', 4, Color(0xFFEA580C), Color(0xFFFDA047)),
  Exam('chsl', 'ssc-chsl', 'SSC CHSL', '10+2 level', '📋', 'ssc-chsl-mocks', '80 mocks', 2, Color(0xFF0369A1), Color(0xFF38BDF8)),
  Exam('mts', 'ssc-mts', 'SSC MTS', '10th level', '📝', 'ssc-mts-mocks', '60 mocks', 2, Color(0xFF047857), Color(0xFF34D399)),
  Exam('gd', 'ssc-gd', 'SSC GD', 'Constable', '🛡️', 'ssc-gd-mocks', '60 mocks', 2, Color(0xFFB91C1C), Color(0xFFF87171)),
  Exam('ntpc', 'rrb-ntpc', 'RRB NTPC', 'Railway · Graduate', '🚆', 'rrb-ntpc-mocks', '60 mocks', 3, Color(0xFF1E3FAE), Color(0xFF60A5FA)),
];

Exam? examByKey(String? k) {
  for (final e in exams) {
    if (e.k == k) return e;
  }
  return null;
}

class Prefs {
  static const _examKey = 'tssc_app_exam';
  static Future<String?> exam() async => (await SharedPreferences.getInstance()).getString(_examKey);
  static Future<void> setExam(String k) async => (await SharedPreferences.getInstance()).setString(_examKey, k);
}

bool _active(dynamic g) {
  if (g is! Map) return false;
  if (g['active'] != true) return false;
  final e = g['expiresAt'];
  if (e is Timestamp) return e.toDate().isAfter(DateTime.now());
  return true;
}

/// The mock series this account owns (entitlement keys). Empty when nothing is owned or it cannot be read.
Future<Set<String>> loadOwned(String uid) async {
  final out = <String>{};
  try {
    final snap = await FirebaseFirestore.instance.collection('entitlements').doc(uid).get();
    final d = snap.data() ?? <String, dynamic>{};
    final mods = d['modules'];
    final m = mods is Map ? mods : const {};
    final all = _active(d['allAccess']) || _active(m['all-mocks']);
    for (final e in exams) {
      if (all || _active(m[e.pass])) out.add(e.pass);
    }
  } catch (_) {}
  return out;
}

Future<String> loadName(String uid, String? fallback) async {
  try {
    final snap = await FirebaseFirestore.instance.collection('users').doc(uid).get();
    final n = (snap.data() ?? const {})['name'];
    if (n is String && n.trim().isNotEmpty && n != 'Student') return n.trim();
  } catch (_) {}
  if (fallback != null && fallback.trim().isNotEmpty) return fallback.trim();
  return 'Student';
}

class MockItem {
  final int n;
  bool en = false;
  bool hi = false;
  MockItem(this.n);
}

Future<List<MockItem>> loadMocks(Exam exam) async {
  final snap = await FirebaseFirestore.instance.collection('mock_tests').where('exam', isEqualTo: exam.id).get();
  final map = <int, MockItem>{};
  for (final doc in snap.docs) {
    final m = doc.data();
    if (m['isPublished'] != true) continue;
    if (m['tier'] == 'tier2') continue;
    final raw = m['seriesNum'] ?? m['mockNum'];
    final n = raw is num ? raw.toInt() : int.tryParse('$raw');
    if (n == null) continue;
    final item = map.putIfAbsent(n, () => MockItem(n));
    if ((m['lang'] ?? m['language']) == 'hi') {
      item.hi = true;
    } else {
      item.en = true;
    }
  }
  final list = map.values.toList()..sort((a, b) => a.n.compareTo(b.n));
  return list;
}
