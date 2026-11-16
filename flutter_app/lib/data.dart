import 'dart:convert';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:http/http.dart' as http;
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
  // ---- how this exam's papers work (all of it can come from catalog.json, so a new course needs no app update)
  final String icon3dName;
  final String tierTag; // middle part of the mock id; '' = tier1 / tier2, NTPC = cbt1
  final double pos; // marks for a correct answer (Tier 1)
  final double neg; // marks cut for a wrong answer (Tier 1)
  final String timing; // sections (one clock per subject) | sessions (two halves) | single (one clock)
  final int unitMin; // minutes of one section / session / the whole paper
  final int split; // sessions: Session II starts after this question number
  final bool negS2; // sessions: negative marking in Session II only
  final String timingNote; // extra words after the timing line
  final bool maths; // the Quant section is called Maths
  final bool partD; // Part D (Q61-80) can be taken in English or Hindi
  final bool canonStats; // subject stats by canonical subject name
  final List<String> subjects; // subject mocks offered
  final Map<String, List<int>> bands; // subject -> question range in the full mock (fallback)
  final Map<String, int> subjMin; // subject mock minutes (default 15)
  final List<String> pyqPages; // app PYQ list pages on trickyssc.com
  final bool pyqFs; // PYQ list comes from Firestore
  final List<String> chExtra; // extra chapter-test subjects: computer, finance, statistics
  final String passName; // name of the pass in My orders
  final String play; // Play product id of the pass ('' = made from the pass key)
  String get icon3d => icon3dName.isNotEmpty ? icon3dName : (const {'cgl': 'target', 'chsl': 'clip', 'mts': 'pencil', 'gd': 'shield', 'ntpc': 'train'}[k] ?? 'book');
  /// Short name: CGL, CHSL, NTPC.
  String get short => name.replaceFirst('SSC ', '').replaceFirst('RRB ', '');
  /// Deep text colour for this exam (headings, labels).
  Color get ink => Color.lerp(c1, const Color(0xFF0F172A), 0.45)!;
  const Exam(this.k, this.id, this.name, this.sub, this.icon, this.pass, this.mocks, this.free, this.c1, this.c2, this.meta, this.tier2,
      {this.icon3dName = '',
      this.tierTag = '',
      this.pos = 2,
      this.neg = 0.5,
      this.timing = 'sections',
      this.unitMin = 15,
      this.split = 0,
      this.negS2 = false,
      this.timingNote = '',
      this.maths = false,
      this.partD = false,
      this.canonStats = false,
      this.subjects = const ['quant', 'reasoning', 'gk', 'english'],
      this.bands = const {},
      this.subjMin = const {},
      this.pyqPages = const [],
      this.pyqFs = false,
      this.chExtra = const [],
      this.passName = '',
      this.play = ''});

  /// One exam of catalog.json. Anything the file leaves out comes from [base] (the same exam built into this app) or the usual default.
  static Exam? fromJson(Map j, Exam? base) {
    String str(String key, String d) => j[key] == null ? d : '${j[key]}';
    bool flag(String key, bool d) => j[key] is bool ? j[key] as bool : d;
    int whole(String key, int d) => j[key] is num ? (j[key] as num).toInt() : d;
    double dec(String key, double d) => j[key] is num ? (j[key] as num).toDouble() : d;
    Color col(String key, Color d) {
      final v = int.tryParse('${j[key] ?? ''}'.replaceFirst('#', ''), radix: 16);
      return v == null ? d : Color(0xFF000000 | v);
    }

    List<String> strs(String key, List<String> d) => j[key] is List ? [for (final x in j[key] as List) '$x'] : d;
    final k = str('k', ''), id = str('id', ''), pass = str('pass', '');
    if (k.isEmpty || id.isEmpty || pass.isEmpty) return null;
    final b = base;
    var bands = b?.bands ?? const <String, List<int>>{};
    if (j['bands'] is Map) {
      bands = {
        for (final e in (j['bands'] as Map).entries)
          if (e.value is List && (e.value as List).length == 2) '${e.key}': [for (final x in e.value as List) x is num ? x.toInt() : 0]
      };
    }
    var subjMin = b?.subjMin ?? const <String, int>{};
    if (j['subjMin'] is Map) subjMin = {for (final e in (j['subjMin'] as Map).entries) if (e.value is num) '${e.key}': (e.value as num).toInt()};
    return Exam(
      k,
      id,
      str('name', b?.name ?? id.toUpperCase().replaceAll('-', ' ')),
      str('sub', b?.sub ?? ''),
      str('icon', b?.icon ?? '📘'),
      pass,
      str('mocks', b?.mocks ?? 'Mocks'),
      whole('free', b?.free ?? 2),
      col('c1', b?.c1 ?? const Color(0xFF4F46E5)),
      col('c2', b?.c2 ?? const Color(0xFFA5B4FC)),
      str('meta', b?.meta ?? ''),
      flag('tier2', b?.tier2 ?? false),
      icon3dName: str('icon3d', b?.icon3dName ?? ''),
      tierTag: str('tierTag', b?.tierTag ?? ''),
      pos: dec('pos', b?.pos ?? 2),
      neg: dec('neg', b?.neg ?? 0.5),
      timing: str('timing', b?.timing ?? 'sections'),
      unitMin: whole('unitMin', b?.unitMin ?? 15),
      split: whole('split', b?.split ?? 0),
      negS2: flag('negS2', b?.negS2 ?? false),
      timingNote: str('timingNote', b?.timingNote ?? ''),
      maths: flag('maths', b?.maths ?? false),
      partD: flag('partD', b?.partD ?? false),
      canonStats: flag('canonStats', b?.canonStats ?? true),
      subjects: strs('subjects', b?.subjects ?? const ['quant', 'reasoning', 'gk', 'english']),
      bands: bands,
      subjMin: subjMin,
      pyqPages: strs('pyqPages', b?.pyqPages ?? const []),
      pyqFs: flag('pyqFs', b?.pyqFs ?? false),
      chExtra: strs('chExtra', b?.chExtra ?? const []),
      passName: str('passName', b?.passName ?? ''),
      play: str('play', b?.play ?? ''),
    );
  }
}

/// The exams built into this build. [exams] starts as this list and is replaced by catalog.json (see [Catalog]).
const List<Exam> _builtIn = [
  Exam('cgl', 'ssc-cgl', 'SSC CGL', 'Graduate level', '🎯', 'ssc-cgl-mocks', '100 mocks', 4, Color(0xFFEA580C), Color(0xFFFDA047), '100 Qs · 60 min', true,
      bands: {'reasoning': [1, 25], 'gk': [26, 50], 'quant': [51, 75], 'english': [76, 100]},
      pyqPages: ['app-ssc-cgl-pyq.html', 'app-ssc-cgl-tier-2-pyq.html'],
      chExtra: ['computer', 'finance', 'statistics'],
      passName: 'SSC CGL Mock Test Series'),
  Exam('chsl', 'ssc-chsl', 'SSC CHSL', '10+2 level', '📋', 'ssc-chsl-mocks', '80 mocks', 2, Color(0xFF0369A1), Color(0xFF38BDF8), '100 Qs · 60 min', true,
      bands: {'english': [1, 25], 'reasoning': [26, 50], 'quant': [51, 75], 'gk': [76, 100]},
      pyqPages: ['app-ssc-chsl-pyq.html'],
      chExtra: ['computer'],
      passName: 'SSC CHSL Mock Test Series'),
  Exam('mts', 'ssc-mts', 'SSC MTS', '10th level', '📝', 'ssc-mts-mocks', '60 mocks', 2, Color(0xFF047857), Color(0xFF34D399), '90 Qs · 90 min', false,
      pos: 3,
      neg: 1,
      timing: 'sessions',
      unitMin: 45,
      split: 40,
      negS2: true,
      timingNote: 'Session I (Maths, Reasoning), then Session II (GA, English).',
      maths: true,
      canonStats: true,
      bands: {'quant': [1, 20], 'reasoning': [21, 40], 'gk': [41, 65], 'english': [66, 90]},
      subjMin: {'quant': 25, 'reasoning': 20, 'gk': 20, 'english': 25},
      pyqFs: true,
      passName: 'SSC MTS Mock Test Series'),
  Exam('gd', 'ssc-gd', 'SSC GD', 'Constable', '🛡️', 'ssc-gd-mocks', '60 mocks', 2, Color(0xFF0F766E), Color(0xFF2DD4BF), '80 Qs · 60 min', false,
      neg: 0.25,
      maths: true,
      partD: true,
      bands: {'reasoning': [1, 20], 'gk': [21, 40], 'quant': [41, 60], 'english': [61, 80]},
      pyqPages: ['app-ssc-gd-pyq.html'],
      passName: 'SSC GD Constable Mock Test Series'),
  Exam('ntpc', 'rrb-ntpc', 'RRB NTPC', 'Railway · Graduate', '🚆', 'rrb-ntpc-mocks', '60 mocks', 3, Color(0xFF1E3FAE), Color(0xFF60A5FA), '100 Qs · 90 min', false,
      tierTag: 'cbt1',
      pos: 1,
      neg: 1 / 3,
      timing: 'single',
      unitMin: 90,
      maths: true,
      canonStats: true,
      subjects: ['quant', 'reasoning', 'gk'],
      subjMin: {'quant': 27, 'reasoning': 27, 'gk': 36},
      pyqPages: ['app-rrb-ntpc-pyq.html'],
      passName: 'RRB NTPC Mock Test Series'),
];

/// Every course the app offers, in display order. Read from catalog.json at start, so a course added
/// on the website shows up without an app update.
List<Exam> exams = List.of(_builtIn);

/// Goes up each time [exams] is replaced, so open screens can rebuild.
final ValueNotifier<int> catalogVersion = ValueNotifier(0);

/// catalog.json (flutter_app/catalog.json in the repo) is the list of courses. The app reads the copy bundled
/// into the build, then the copy saved on the phone, then the live one; the newest ("v") wins.
class Catalog {
  static const _urls = [
    'https://trickyssc.com/flutter_app/catalog.json',
    'https://raw.githubusercontent.com/nirala01/TrickySSC/main/flutter_app/catalog.json',
  ];
  static const _key = 'tssc_catalog';
  static const _app = String.fromEnvironment('APP_VERSION');
  static int _v = -1;

  /// True when this build is older than [min] ("2.0.50"); an unknown build number is never too old.
  static bool _tooOld(String min) {
    List<int> parts(String s) => [for (final x in s.split('.')) int.tryParse(x.replaceAll(RegExp(r'[^0-9]'), '')) ?? 0];
    if (min.isEmpty || _app.isEmpty) return false;
    final a = parts(_app), b = parts(min);
    for (var i = 0; i < b.length; i++) {
      final x = i < a.length ? a[i] : 0;
      if (x != b[i]) return x < b[i];
    }
    return false;
  }

  static bool _apply(String body) {
    try {
      final j = jsonDecode(body);
      if (j is! Map || j['exams'] is! List) return false;
      final v = j['v'] is num ? (j['v'] as num).toInt() : 0;
      if (v < _v) return false;
      final list = <Exam>[];
      for (final x in j['exams'] as List) {
        if (x is! Map || x['live'] == false || _tooOld('${x['minApp'] ?? ''}')) continue;
        Exam? base;
        for (final b in _builtIn) {
          if (b.k == x['k']) base = b;
        }
        final e = Exam.fromJson(x, base);
        if (e != null && !list.any((o) => o.k == e.k || o.pass == e.pass)) list.add(e);
      }
      if (list.isEmpty) return false;
      _v = v;
      exams = list;
      catalogVersion.value++;
      return true;
    } catch (_) {
      return false;
    }
  }

  /// Before the first screen: the bundled copy and the copy saved on the phone (no network). The live copy follows.
  static Future<void> init() async {
    try {
      _apply(await rootBundle.loadString('catalog.json'));
    } catch (_) {}
    try {
      final saved = (await SharedPreferences.getInstance()).getString(_key);
      if (saved != null) _apply(saved);
    } catch (_) {}
    refresh();
  }

  static Future<void> refresh() async {
    for (final u in _urls) {
      try {
        final r = await http.get(Uri.parse('$u?t=${DateTime.now().millisecondsSinceEpoch ~/ 300000}')).timeout(const Duration(seconds: 8));
        if (r.statusCode != 200) continue;
        final body = utf8.decode(r.bodyBytes);
        if (!_apply(body)) continue;
        (await SharedPreferences.getInstance()).setString(_key, body);
        return;
      } catch (_) {}
    }
  }
}

/// The exam a mock / paper id belongs to (ssc-cgl_tier1_mock5_en -> SSC CGL).
Exam? examOfPaper(String id) {
  for (final e in exams) {
    if (id.startsWith('${e.id}_')) return e;
  }
  return null;
}

Exam? examById(String id) {
  for (final e in exams) {
    if (e.id == id) return e;
  }
  return null;
}

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
/// Null when the entitlements could not be read (offline), so nothing is assumed about the student.
Future<Set<String>?> loadOwnedOrNull(String uid) async {
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
  } catch (_) {
    return null;
  }
  return out;
}

Future<Set<String>> loadOwned(String uid) async => (await loadOwnedOrNull(uid)) ?? <String>{};

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

/// Attempted ids (as [loadAttempted]) plus the latest attempt of each mock / PYQ, keyed by its id without the language.
Future<(Set<String>, Map<String, Map<String, dynamic>>)> loadAttemptInfo(String uid) async {
  final ids = <String>{};
  final last = <String, Map<String, dynamic>>{};
  try {
    final list = await loadAttempts(uid);
    for (final a in list) {
      for (final key in const ['paperId', 'mockId', 'lbKey']) {
        final v = a[key];
        if (v is String && v.isNotEmpty) ids.add(v);
      }
      final id = '${a['mockId'] ?? ''}'.isNotEmpty ? '${a['mockId']}' : '${a['paperId'] ?? ''}';
      if (id.isEmpty || id.contains('__')) continue;
      last.putIfAbsent(id.replaceAll(RegExp(r'_(en|hi)$'), ''), () => a);
    }
  } catch (_) {}
  return (ids, last);
}

/// The mock id the website uses: ssc-cgl_tier1_mock5_en, rrb-ntpc_cbt1_mock5_hi …
String mockBase(Exam exam, MockItem m) => '${exam.id}_${exam.tierTag.isNotEmpty ? exam.tierTag : 'tier${m.tier}'}_mock${m.n}';

bool isAttempted(Set<String> ids, Exam exam, MockItem m) {
  final base = mockBase(exam, m);
  for (final id in ids) {
    if (id.contains('__')) continue; // subject mocks never mark the full mock as done
    if (id == base || id.startsWith('${base}_')) return true;
  }
  return false;
}

/// Products from admin-pricing (config/pricing). If Firestore cannot be read, the copy bundled
/// into this build (assets/pricing.json, refreshed by every GitHub build) is used.
Future<List<dynamic>> pricingProducts() async {
  try {
    final snap = await FirebaseFirestore.instance.collection('config').doc('pricing').get().timeout(const Duration(seconds: 8));
    final p = (snap.data() ?? const {})['products'];
    if (p is List && p.isNotEmpty) return p;
  } catch (_) {}
  try {
    final j = jsonDecode(await rootBundle.loadString('assets/pricing.json'));
    final p = j is Map ? j['products'] : null;
    if (p is List) return p;
  } catch (_) {}
  return const [];
}

/// Lowest live price of a pass for this exam, from config/pricing. Null when it cannot be read.
Future<int?> loadPrice(Exam exam) async {
  try {
    final products = await pricingProducts();
    if (products.isEmpty) return null;
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
