// SSC CGL Tier-2 "All India Challenge Mock": the schedule and the states, in plain Dart
// (no Flutter, no Firebase) so tool/aic_check.dart can run every state with a faked server time.
// The website does the same in /tssc-aic.js.
//
// All times are milliseconds since 1970 (UTC). Round N starts on a Sunday at 9:00 am IST,
// N - 1 weeks after the first round.

const int _min = 60000;
const int _hour = 60 * _min;
const int _week = 7 * 24 * _hour;

/// The "aic" block of catalog.json: on / off, the first Sunday and the last round (0 = no end yet).
class AicConfig {
  final bool on;
  final int firstMs;
  final int lastRound;
  const AicConfig({required this.on, required this.firstMs, required this.lastRound});
}

/// Round 1: Sunday 29 Nov 2026, 9:00 am IST (03:30 UTC). Replaced by catalog.json when it has an "aic" block.
AicConfig aicConfig = AicConfig(on: true, firstMs: DateTime.utc(2026, 11, 29, 3, 30).millisecondsSinceEpoch, lastRound: 0);

/// Reads {"on": true, "first": "2026-11-29T09:00:00+05:30", "lastRound": 0}. Anything unreadable is ignored.
void aicApplyCatalog(dynamic j) {
  if (j is! Map) return;
  final first = DateTime.tryParse('${j['first'] ?? ''}');
  final last = j['lastRound'];
  aicConfig = AicConfig(
    on: j['on'] != false,
    firstMs: first?.millisecondsSinceEpoch ?? aicConfig.firstMs,
    lastRound: last is num ? last.toInt() : aicConfig.lastRound,
  );
}

// ------------------------------------------------------------------ schedule

int aicStart(int n) => aicConfig.firstMs + (n - 1) * _week; // Sunday 9:00 am
int aicRegClose(int n) => aicStart(n) - 9 * _hour; // Saturday midnight
int aicLastEntry(int n) => aicStart(n) + 12 * _hour + 45 * _min; // Sunday 9:45 pm
int aicWindowEnd(int n) => aicStart(n) + 15 * _hour; // Sunday midnight
int aicHardCap(int n) => aicStart(n) + 15 * _hour + 30 * _min; // 12:30 am: nobody is still writing after this
int aicResultAt(int n) => aicStart(n) + 48 * _hour; // Tuesday 9:00 am

/// The live test ends 2 h 25 min after its first start, and never later than 12:30 am.
int aicHardStop(int n, int startedMs) {
  final own = startedMs + 145 * _min;
  return own < aicHardCap(n) ? own : aicHardCap(n);
}

bool aicRoundExists(int n) => n >= 1 && (aicConfig.lastRound <= 0 || n <= aicConfig.lastRound);

/// The round that is coming or is on now: the first one whose Sunday has not ended. 0 = the series is over.
int aicUpRound(int now) {
  var n = 1;
  if (now >= aicWindowEnd(1)) n = ((now - aicWindowEnd(1)) ~/ _week) + 2;
  return aicRoundExists(n) ? n : 0;
}

/// Rounds whose result is out, newest first (at most [limit]).
List<int> aicFinished(int now, {int limit = 8}) {
  final out = <int>[];
  if (now < aicResultAt(1)) return out;
  var n = ((now - aicResultAt(1)) ~/ _week) + 1;
  if (aicConfig.lastRound > 0 && n > aicConfig.lastRound) n = aicConfig.lastRound;
  for (; n >= 1 && out.length < limit; n--) {
    out.add(n);
  }
  return out;
}

/// A student is in round N only when the registration was made before that round's registration closed.
bool aicInRound(int n, int? regAtMs) => regAtMs != null && regAtMs < aicRegClose(n);

// ------------------------------------------------------------------ ids

String aicMockId(int n, String lang) => 'ssc-cgl_aic_mock${n}_$lang';
String aicBoard(int n) => 'ssc-cgl_aic_mock$n';
String aicTitle(int n) => 'SSC CGL Tier-2 All India Challenge Mock $n';
const aicRegBoard = 'aic-registered';

/// The round of an All India Challenge id (mock id, board or leaderboard key); 0 for anything else.
int aicRoundOf(String id) {
  final m = RegExp(r'^ssc-cgl_aic_mock(\d+)(?:_|$)').firstMatch(id);
  return m == null ? 0 : int.parse(m.group(1)!);
}

/// One run of the paper: the live Sunday attempt, or the free mock taken after the result.
class AicRun {
  final int round;
  final bool live;
  const AicRun(this.round, this.live);
  int get resultAt => aicResultAt(round);
  Map<String, dynamic> toAttempt() => live ? {'round': round, 'live': true, 'resultAt': resultAt} : {'round': round, 'live': false};
}

// ------------------------------------------------------------------ hold back

/// When the result of this attempt opens (0 = it is not a live challenge attempt).
int aicAttemptResultAt(Map a) {
  final x = a['aic'];
  if (x is! Map || x['live'] != true) return 0;
  final r = x['resultAt'];
  if (r is num && r > 0) return r.toInt();
  final n = x['round'];
  return n is num && n >= 1 ? aicResultAt(n.toInt()) : 0;
}

/// A live challenge attempt before its result time: hidden everywhere (My Tests, dashboard, analysis, solutions, rank).
bool aicIsHeld(Map a, int now) => now < aicAttemptResultAt(a);

/// The leaderboard of a round is closed until its result time.
bool aicBoardClosed(String key, int now) {
  final n = aicRoundOf(key);
  return n > 0 && now < aicResultAt(n);
}

// ------------------------------------------------------------------ what the student sees

enum AicState {
  off, // switched off, or the series is over
  regOpen, // not registered, registration for the coming Sunday is open
  regNext, // not registered, the coming / running Sunday is closed: registering now is for the Sunday after
  registered, // registered in time for the coming Sunday
  registeredNext, // registered, but after this Sunday's registration closed: in from the next round
  live, // Sunday window, registered in time, not submitted: may start (or resume)
  entryClosed, // Sunday after 9:45 pm, never started
  submitted, // live attempt submitted, the result is not out yet
}

class AicView {
  final AicState state;
  final int round; // the round the state is about (regNext / registeredNext: the round the student will be in)
  final int countdownTo; // ms the countdown runs to (0 = none)
  final int resultsRound; // "Challenge Mock N results are out" (Tuesday 9 am to the next Sunday 9 am); 0 = none
  const AicView(this.state, this.round, {this.countdownTo = 0, this.resultsRound = 0});
  @override
  String toString() => '${state.name} r$round${resultsRound > 0 ? ' results$resultsRound' : ''}';
}

/// [regAt]: when the student registered (null = not registered). [submitted]: rounds with a live attempt.
/// [inProgress]: a live paper of the running round was started on this phone and can still be resumed.
AicView aicView({required int now, int? regAt, Set<int> submitted = const {}, bool inProgress = false}) {
  if (!aicConfig.on) return const AicView(AicState.off, 0);
  final up = aicUpRound(now);
  // the last finished Sunday
  final prev = up > 0 ? up - 1 : (aicConfig.lastRound > 0 ? aicConfig.lastRound : 0);
  var results = 0;
  if (prev >= 1 && now >= aicResultAt(prev) && now < aicStart(prev) + _week) results = prev;

  if (up > 0 && now >= aicStart(up)) {
    // Sunday, 9 am to midnight
    if (aicInRound(up, regAt)) {
      if (submitted.contains(up)) return AicView(AicState.submitted, up, countdownTo: aicResultAt(up));
      if (now <= aicLastEntry(up)) return AicView(AicState.live, up, countdownTo: aicLastEntry(up));
      if (inProgress && now < aicHardCap(up)) return AicView(AicState.live, up, countdownTo: aicHardCap(up));
      return AicView(AicState.entryClosed, up);
    }
    if (!aicRoundExists(up + 1)) return const AicView(AicState.off, 0);
    if (regAt != null) return AicView(AicState.registeredNext, up + 1, countdownTo: aicStart(up + 1));
    return AicView(AicState.regNext, up + 1, countdownTo: aicRegClose(up + 1));
  }

  // a paper still open past midnight (hard stop 12:30 am)
  if (prev >= 1 && inProgress && !submitted.contains(prev) && aicInRound(prev, regAt) && now < aicHardCap(prev)) {
    return AicView(AicState.live, prev, countdownTo: aicHardCap(prev));
  }
  if (prev >= 1 && submitted.contains(prev) && now < aicResultAt(prev)) {
    return AicView(AicState.submitted, prev, countdownTo: aicResultAt(prev));
  }
  if (up == 0) return AicView(AicState.off, 0, resultsRound: results);
  if (regAt == null) {
    if (now < aicRegClose(up)) return AicView(AicState.regOpen, up, countdownTo: aicRegClose(up), resultsRound: results);
    if (!aicRoundExists(up + 1)) return AicView(AicState.off, 0, resultsRound: results);
    return AicView(AicState.regNext, up + 1, countdownTo: aicRegClose(up + 1), resultsRound: results);
  }
  if (aicInRound(up, regAt)) return AicView(AicState.registered, up, countdownTo: aicStart(up), resultsRound: results);
  if (!aicRoundExists(up + 1)) return AicView(AicState.off, 0, resultsRound: results);
  return AicView(AicState.registeredNext, up + 1, countdownTo: aicStart(up + 1), resultsRound: results);
}

// ------------------------------------------------------------------ text

const _wd = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
const _mo = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

DateTime _ist(int ms) => DateTime.fromMillisecondsSinceEpoch(ms, isUtc: true).add(const Duration(hours: 5, minutes: 30));

/// "Sun 6 Dec" (IST).
String aicDay(int ms) {
  final d = _ist(ms);
  return '${_wd[d.weekday - 1]} ${d.day} ${_mo[d.month - 1]}';
}

/// "9 am", "9:45 pm" (IST).
String aicClockText(int ms) {
  final d = _ist(ms);
  final h = d.hour % 12 == 0 ? 12 : d.hour % 12;
  return '$h${d.minute == 0 ? '' : ':${d.minute.toString().padLeft(2, '0')}'} ${d.hour < 12 ? 'am' : 'pm'}';
}

/// "Tue 8 Dec, 9 am" (IST).
String aicWhen(int ms) => '${aicDay(ms)}, ${aicClockText(ms)}';

/// "2d 05h 12m", "05h 12m 09s", "12m 09s".
String aicCountdown(int ms) {
  if (ms <= 0) return '0s';
  final s = ms ~/ 1000;
  final d = s ~/ 86400, h = (s % 86400) ~/ 3600, m = (s % 3600) ~/ 60, x = s % 60;
  String two(int v) => v.toString().padLeft(2, '0');
  if (d > 0) return '${d}d ${two(h)}h ${two(m)}m';
  if (h > 0) return '${two(h)}h ${two(m)}m ${two(x)}s';
  return '${two(m)}m ${two(x)}s';
}
