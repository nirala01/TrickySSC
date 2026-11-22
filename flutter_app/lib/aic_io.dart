// All India Challenge: the server clock, registration and the few Firestore reads and writes.
// No new collections: users/{uid}.aic, leaderboards/aic-registered and leaderboards/ssc-cgl_aic_mockN,
// the same documents the website uses.
import 'dart:io' show HttpDate;

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import 'aic.dart';

/// The time of a server, never the phone's own clock: the Date header of trickyssc.com/robots.txt.
/// Between two readings the phone only counts how much time has passed.
class AicClock {
  static const _urls = ['https://trickyssc.com/robots.txt', 'https://raw.githubusercontent.com/nirala01/TrickySSC/main/robots.txt'];
  // a build made with --dart-define=AIC_FAKE_NOW=2026-12-06T09:05:00+05:30 runs on that time (testing only)
  static const _fake = String.fromEnvironment('AIC_FAKE_NOW');
  static int? _base;
  static final Stopwatch _sw = Stopwatch();
  static Future<bool>? _busy;

  /// Server time now, or null when it has not been read yet.
  static int? get nowOrNull => _base == null ? null : _base! + _sw.elapsedMilliseconds;

  /// Server time when it is known; the phone's clock only until the first reading arrives.
  static int get now => nowOrNull ?? DateTime.now().millisecondsSinceEpoch;

  static bool get synced => _base != null;

  /// Reads the server time. [force]: read it again even if it was read a moment ago (app came back, test starts).
  static Future<bool> sync({bool force = false}) {
    if (!force && _base != null && _sw.elapsedMilliseconds < 3 * 60000) return Future.value(true);
    return _busy ??= _read().whenComplete(() => _busy = null);
  }

  static Future<bool> _read() async {
    if (_fake.isNotEmpty) {
      final f = DateTime.tryParse(_fake);
      if (f != null) {
        if (_base == null) {
          _base = f.millisecondsSinceEpoch;
          _sw
            ..reset()
            ..start();
        }
        return true;
      }
    }
    for (final u in _urls) {
      try {
        final t0 = DateTime.now();
        final r = await http.head(Uri.parse('$u?t=${t0.millisecondsSinceEpoch}')).timeout(const Duration(seconds: 8));
        final d = r.headers['date'];
        if (d == null || d.isEmpty) continue;
        final ms = HttpDate.parse(d).millisecondsSinceEpoch;
        // the header has whole seconds; add half the round trip
        _base = ms + DateTime.now().difference(t0).inMilliseconds ~/ 2;
        _sw
          ..reset()
          ..start();
        return true;
      } catch (_) {}
    }
    return _base != null;
  }
}

/// What the app knows about this student and one series.
class AicMe {
  final int? regAt; // when registered (ms), null = not registered
  final Set<int> submitted; // rounds with a live attempt
  const AicMe(this.regAt, this.submitted);
}

/// Live challenge attempts still held back (result not out): filled by loadAttempts, shown as a small note.
List<Map<String, dynamic>> aicHeld = [];

/// Rounds this student has a live attempt for, per series key (from the attempts last loaded).
final Map<String, Set<int>> aicLiveRounds = {};

/// Called by loadAttempts with every attempt of the student: returns the list without the held ones.
List<Map<String, dynamic>> aicFilterAttempts(List<Map<String, dynamic>> all) {
  final now = AicClock.now;
  final held = <Map<String, dynamic>>[];
  final out = <Map<String, dynamic>>[];
  for (final a in all) {
    final x = a['aic'];
    if (x is Map && x['live'] == true && x['round'] is num) (aicLiveRounds[aicSeriesOfAttempt(a).key] ??= {}).add((x['round'] as num).toInt());
    (aicIsHeld(a, now) ? held : out).add(a);
  }
  aicHeld = held;
  return out;
}

String _regKey(AicSeries s, String uid) => 'tssc_aic_reg_${s.tag}$uid';
String _subKey(AicSeries s, String uid) => 'tssc_aic_sub_${s.tag}$uid';

int? _ms(dynamic v) {
  if (v is Timestamp) return v.millisecondsSinceEpoch;
  if (v is num && v > 0) return v.toInt();
  if (v is String) return DateTime.tryParse(v)?.millisecondsSinceEpoch;
  return null;
}

/// Registration and submitted rounds as saved on this phone (instant, may be a little old).
Future<AicMe> aicCached(AicSeries se, String uid) async {
  final liveR = aicLiveRounds[se.key] ?? const <int>{};
  try {
    final p = await SharedPreferences.getInstance();
    final r = p.getInt(_regKey(se, uid));
    final s = {for (final x in (p.getStringList(_subKey(se, uid)) ?? const <String>[])) int.tryParse(x) ?? 0}..remove(0);
    return AicMe(r, {...s, ...liveR});
  } catch (_) {
    return AicMe(null, {...liveR});
  }
}

/// Reads the registration (users/{uid}.<regField>) and whether rounds [rounds] were submitted (their leaderboard rows).
Future<AicMe> aicLoadMe(AicSeries se, String uid, List<int> rounds) async {
  final db = FirebaseFirestore.instance;
  final cached = await aicCached(se, uid);
  int? reg = cached.regAt;
  final sub = {...cached.submitted};
  try {
    final u = await db.collection('users').doc(uid).get();
    final x = (u.data() ?? const {})[se.regField];
    if (x is Map && x['reg'] == true) {
      // a registration whose time is not on the server yet counts from now
      reg = _ms(x['at']) ?? reg ?? AicClock.now;
    } else if (u.exists) {
      reg = null;
    }
  } catch (_) {}
  for (final n in rounds) {
    if (n < 1 || sub.contains(n)) continue;
    try {
      final d = await db.collection('leaderboards').doc(se.board(n)).collection('scores').doc(uid).get();
      if (d.exists) sub.add(n);
    } catch (_) {}
  }
  try {
    final p = await SharedPreferences.getInstance();
    if (reg == null) {
      await p.remove(_regKey(se, uid));
    } else {
      await p.setInt(_regKey(se, uid), reg);
    }
    await p.setStringList(_subKey(se, uid), [for (final n in sub) '$n']);
  } catch (_) {}
  return AicMe(reg, sub);
}

/// Marks a round as submitted on this phone at once (the leaderboard row is the proof for other devices).
Future<void> aicMarkSubmitted(AicSeries se, String uid, int round) async {
  (aicLiveRounds[se.key] ??= {}).add(round);
  try {
    final p = await SharedPreferences.getInstance();
    final s = {...(p.getStringList(_subKey(se, uid)) ?? const <String>[]), '$round'};
    await p.setStringList(_subKey(se, uid), s.toList());
  } catch (_) {}
}

/// One-time registration for one series; it covers every later round of that series.
/// Returns the registration time, or null when it failed.
Future<int?> aicRegister(AicSeries se, User u) async {
  final db = FirebaseFirestore.instance;
  try {
    await db.collection('users').doc(u.uid).set({
      se.regField: {'reg': true, 'at': FieldValue.serverTimestamp(), 'src': 'app'}
    }, SetOptions(merge: true));
  } catch (_) {
    return null;
  }
  // the row that makes the "students registered" count
  try {
    var name = '';
    try {
      final us = await db.collection('users').doc(u.uid).get();
      final ud = us.data() ?? const {};
      name = '${ud['name'] ?? ud['displayName'] ?? u.displayName ?? ''}'.trim();
    } catch (_) {}
    await db.collection('leaderboards').doc(se.regBoard).collection('scores').doc(u.uid).set({
      'uid': u.uid,
      'name': name.isEmpty ? 'Student' : name,
      'paperId': se.regBoard,
      'paperName': 'All India Challenge registration',
      'marks': 0,
      'maxMarks': 0,
      'accuracy': null,
      'subjectMarks': <String, dynamic>{},
      'timeUsed': null,
      'submittedAt': FieldValue.serverTimestamp(),
    });
  } catch (_) {}
  int? at;
  try {
    final us = await db.collection('users').doc(u.uid).get(const GetOptions(source: Source.server));
    final x = (us.data() ?? const {})[se.regField];
    if (x is Map) at = _ms(x['at']);
  } catch (_) {}
  at ??= AicClock.now;
  try {
    await (await SharedPreferences.getInstance()).setInt(_regKey(se, u.uid), at);
  } catch (_) {}
  return at;
}

/// "Students registered": the number of rows on the registration board. Null when it cannot be read.
Future<int?> aicRegCount(AicSeries se) async {
  try {
    final c = await FirebaseFirestore.instance.collection('leaderboards').doc(se.regBoard).collection('scores').count().get();
    return c.count;
  } catch (_) {
    return null;
  }
}

/// True when this student's live row of round [n] is on the board.
Future<bool> aicHasRow(AicSeries se, String uid, int n) async {
  final d = await FirebaseFirestore.instance.collection('leaderboards').doc(se.board(n)).collection('scores').doc(uid).get();
  return d.exists;
}

class AicTop {
  final String uid, name;
  final double marks;
  final int timeUsed;
  AicTop(this.uid, this.name, this.marks, this.timeUsed);
}

final _topMem = <String, (List<AicTop>, int)>{};

/// The top 10 of a finished round and how many students took it live. Closed until the result time.
Future<(List<AicTop>, int)> aicTop10(AicSeries se, int n) async {
  final key = se.board(n);
  if (aicBoardClosed(key, AicClock.now)) return (<AicTop>[], 0);
  if (_topMem[key] != null) return _topMem[key]!;
  final col = FirebaseFirestore.instance.collection('leaderboards').doc(key).collection('scores');
  final snap = await col.orderBy('marks', descending: true).limit(10).get();
  var total = snap.docs.length;
  if (total >= 10) {
    try {
      total = (await col.count().get()).count ?? total;
    } catch (_) {}
  }
  final rows = [
    for (final d in snap.docs)
      AicTop(d.id, '${d.data()['name'] ?? 'Student'}', (d.data()['marks'] as num? ?? 0).toDouble(), (d.data()['timeUsed'] as num? ?? 0).toInt())
  ];
  return _topMem[key] = (rows, total);
}
