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
  final String meta; // questions and time of a Tier 1 paper
  final bool tier2;
  /// Deep text colour for this exam (headings, labels).
  Color get ink => Color.lerp(c1, const Color(0xFF0F172A), 0.45)!;
  const Exam(this.k, this.id, this.name, this.sub, this.icon, this.pass, this.mocks, this.free, this.c1, this.c2, this.meta, this.tier2);
}

const List<Exam> exams = [
  Exam('cgl', 'ssc-cgl', 'SSC CGL', 'Graduate level', '🎯', 'ssc-cgl-mocks', '100 mocks', 4, Color(0xFFEA580C), Color(0xFFFDA047), '100 Qs · 60 min', true),
  Exam('chsl', 'ssc-chsl', 'SSC CHSL', '10+2 level', '📋', 'ssc-chsl-mocks', '80 mocks', 2, Color(0xFF0369A1), Color(0xFF38BDF8), '100 Qs · 60 min', true),
  Exam('mts', 'ssc-mts', 'SSC MTS', '10th level', '📝', 'ssc-mts-mocks', '60 mocks', 2, Color(0xFF047857), Color(0xFF34D399), '90 Qs · 90 min', false),
  Exam('gd', 'ssc-gd', 'SSC GD', 'Constable', '🛡️', 'ssc-gd-mocks', '60 mocks', 2, Color(0xFF0F766E), Color(0xFF2DD4BF), '80 Qs · 60 min', false),
  Exam('ntpc', 'rrb-ntpc', 'RRB NTPC', 'Railway · Graduate', '🚆', 'rrb-ntpc-mocks', '60 mocks', 3, Color(0xFF1E3FAE), Color(0xFF60A5FA), '100 Qs · 90 min', false),
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
  final int tier;
  bool en = false;
  bool hi = false;
  MockItem(this.n, this.tier);
}

/// Every published mock of the exam, Tier 1 first, in mock order.
Future<List<MockItem>> loadMocks(Exam exam) async {
  final snap = await FirebaseFirestore.instance.collection('mock_tests').where('exam', isEqualTo: exam.id).get();
  final map = <int, MockItem>{};
  for (final doc in snap.docs) {
    final m = doc.data();
    if (m['isPublished'] != true) continue;
    final tier = m['tier'] == 'tier2' ? 2 : 1;
    if (tier == 2 && !exam.tier2) continue;
    final raw = m['seriesNum'] ?? m['mockNum'];
    final n = raw is num ? raw.toInt() : int.tryParse('$raw');
    if (n == null) continue;
    final item = map.putIfAbsent(tier * 10000 + n, () => MockItem(n, tier));
    if ((m['lang'] ?? m['language']) == 'hi') {
      item.hi = true;
    } else {
      item.en = true;
    }
  }
  final keys = map.keys.toList()..sort();
  return [for (final k in keys) map[k]!];
}

/// Ids of the tests this account has attempted (same ids the website uses).
Future<Set<String>> loadAttempted(String uid) async {
  final out = <String>{};
  try {
    final snap = await FirebaseFirestore.instance.collection('attempts').where('uid', isEqualTo: uid).get();
    for (final doc in snap.docs) {
      final a = doc.data();
      for (final key in const ['paperId', 'mockId', 'lbKey']) {
        final v = a[key];
        if (v is String && v.isNotEmpty) out.add(v);
      }
    }
  } catch (_) {}
  return out;
}

/// The mock id the website uses: ssc-cgl_tier1_mock5_en, rrb-ntpc_cbt1_mock5_hi …
String mockBase(Exam exam, MockItem m) => '${exam.id}_${exam.k == 'ntpc' ? 'cbt1' : 'tier${m.tier}'}_mock${m.n}';

bool isAttempted(Set<String> ids, Exam exam, MockItem m) {
  final base = mockBase(exam, m);
  for (final id in ids) {
    if (id == base || id.startsWith('${base}_')) return true;
  }
  return false;
}

/// Lowest live price of a pass for this exam, from config/pricing. Null when it cannot be read.
Future<int?> loadPrice(Exam exam) async {
  try {
    final snap = await FirebaseFirestore.instance.collection('config').doc('pricing').get();
    final products = (snap.data() ?? const {})['products'];
    if (products is! List) return null;
    int? best;
    for (final p in products) {
      if (p is! Map) continue;
      if (p['live'] == false) continue;
      final id = '${p['id'] ?? ''}';
      if (id.startsWith('p-upgrade-')) continue;
      final grants = p['grants'];
      if (grants is! List || !grants.contains(exam.pass)) continue;
      final raw = p['price'];
      final price = raw is num ? raw.toInt() : int.tryParse('$raw');
      if (price == null || price <= 0) continue;
      if (best == null || price < best) best = price;
    }
    return best;
  } catch (_) {
    return null;
  }
}


/// Text in this exam's deep colour instead of plain black.
Widget examTheme(BuildContext context, Exam exam, Widget child) {
  final t = Theme.of(context);
  return Theme(data: t.copyWith(textTheme: t.textTheme.apply(bodyColor: exam.ink, displayColor: exam.ink)), child: child);
}

/// Every attempt of this user (website and app), newest first; each map has 'id'.
Future<List<Map<String, dynamic>>> loadAttempts(String uid) async {
  final snap = await FirebaseFirestore.instance.collection('attempts').where('uid', isEqualTo: uid).get();
  final out = [for (final d in snap.docs) {...d.data(), 'id': d.id}];
  out.sort((a, b) => attemptMs(b).compareTo(attemptMs(a)));
  return out;
}

int attemptMs(Map<String, dynamic> a) {
  final t = a['timestamp'];
  if (t is Timestamp) return t.millisecondsSinceEpoch;
  final c = DateTime.tryParse('${a['clientSubmittedAt'] ?? ''}');
  if (c != null) return c.millisecondsSinceEpoch;
  final m = RegExp(r'_(\d{12,})$').firstMatch('${a['id'] ?? ''}');
  return m == null ? 0 : int.parse(m.group(1)!);
}
