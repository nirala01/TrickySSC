// All India Challenge Mocks (SSC CGL Tier 2 on Sundays, SSC CHSL Tier 1 on Saturdays): the schedule and
// the states, in plain Dart (no Flutter, no Firebase) so tool/aic_check.dart can run every state with a
// faked server time. The website does the same in /tssc-aic.js.
//
// All times are milliseconds since 1970 (UTC).

const int _min = 60000;
const int _hour = 60 * _min;
const int _week = 7 * 24 * _hour;

/// One challenge series. Two run side by side, as on the website (tssc-aic.js):
///   cgl   SSC CGL Tier 2    every Sunday    from 29 Nov 2026, no end yet
///   chsl  SSC CHSL Tier 1   every Saturday  from 28 Nov 2026 to round 5 (26 Dec 2026)
/// Round N starts at 9:00 am IST, N - 1 weeks after the first round. The dates, the last round and the
/// on / off switch come from catalog.json ("aic" and "aicChsl" blocks), so they change without an app update.
class AicSeries {
  final String key; // 'cgl' | 'chsl'
  final String exam; // 'ssc-cgl' | 'ssc-chsl'
  final String name; // 'SSC CGL Tier 2'
  final String short; // 'CGL Tier 2'
  final String day; // 'Sunday'
  final String regField; // users/{uid}.<regField>
  final String regBoard; // leaderboards/<regBoard>: the "students registered" count
  final String tag; // part of the keys saved on the phone
  final int paperMin; // length of the paper; the last entry is midnight minus this
  final int hardStopMin; // the live test ends this long after its first start
  final bool parts; // separately timed parts (CGL Tier 2: five, CHSL Tier 1: four); false = one clock
  final String paperLine;
  bool on;
  int firstMs;
  int lastRound; // 0 = no end yet

  AicSeries({
    required this.key,
    required this.exam,
    required this.name,
    required this.short,
    required this.day,
    required this.regField,
    required this.regBoard,
    required this.tag,
    required this.paperMin,
    required this.hardStopMin,
    required this.parts,
    required this.paperLine,
    required this.firstMs,
    required this.lastRound,
    this.on = true,
  });

  /// Reads {"on": true, "first": "2026-11-29T09:00:00+05:30", "lastRound": 0}. Anything unreadable is ignored.
  void apply(dynamic j) {
    if (j is! Map) return;
    final first = DateTime.tryParse('${j['first'] ?? ''}');
    final last = j['lastRound'];
    on = j['on'] != false;
    if (first != null) firstMs = first.millisecondsSinceEpoch;
    if (last is num) lastRound = last.toInt();
  }

  // ---------------------------------------------------------------- schedule
  int start(int n) => firstMs + (n - 1) * _week; // challenge day, 9:00 am
  int regClose(int n) => start(n) - 9 * _hour; // midnight before the challenge day
  int windowEnd(int n) => start(n) + 15 * _hour; // midnight of the challenge day
  int lastEntry(int n) => windowEnd(n) - paperMin * _min; // CGL 9:45 pm, CHSL 11 pm
  int hardCap(int n) => windowEnd(n) + 30 * _min; // 12:30 am: nobody is still writing after this
  int resultAt(int n) => start(n) + 48 * _hour; // two days later, 9:00 am

  /// The live test ends [hardStopMin] after its first start, and never later than 12:30 am.
  int hardStop(int n, int startedMs) {
    final own = startedMs + hardStopMin * _min;
    return own < hardCap(n) ? own : hardCap(n);
  }

  bool exists(int n) => n >= 1 && (lastRound <= 0 || n <= lastRound);

  /// The round that is coming or is on now: the first one whose day has not ended. 0 = the series is over.
  int upRound(int now) {
    var n = 1;
    if (now >= windowEnd(1)) n = ((now - windowEnd(1)) ~/ _week) + 2;
    return exists(n) ? n : 0;
  }

  /// Rounds whose result is out, newest first (at most [limit]).
  List<int> finished(int now, {int limit = 8}) {
    final out = <int>[];
    if (now < resultAt(1)) return out;
    var n = ((now - resultAt(1)) ~/ _week) + 1;
    if (lastRound > 0 && n > lastRound) n = lastRound;
    for (; n >= 1 && out.length < limit; n--) {
      out.add(n);
    }
    return out;
  }

  /// A student is in round N only when the registration was made before that round's registration closed.
  bool inRound(int n, int? regAtMs) => regAtMs != null && regAtMs < regClose(n);

  // ---------------------------------------------------------------- ids
  String mockId(int n, String lang) => '${exam}_aic_mock${n}_$lang';
  String board(int n) => '${exam}_aic_mock$n';
  String title(int n) => '$name All India Challenge Mock $n';

  /// [regAt]: when the student registered for this series (null = not registered). [submitted]: rounds with a
  /// live attempt. [inProgress]: a live paper of the running round was started on this phone and can be resumed.
  AicView view({required int now, int? regAt, Set<int> submitted = const {}, bool inProgress = false}) {
    if (!on) return const AicView(AicState.off, 0);
    final up = upRound(now);
    // the last finished challenge day
    final prev = up > 0 ? up - 1 : (lastRound > 0 ? lastRound : 0);
    var results = 0;
    if (prev >= 1 && now >= resultAt(prev) && now < start(prev) + _week) results = prev;

    if (up > 0 && now >= start(up)) {
      // challenge day, 9 am to midnight
      if (inRound(up, regAt)) {
        if (submitted.contains(up)) return AicView(AicState.submitted, up, countdownTo: resultAt(up));
        if (now <= lastEntry(up)) return AicView(AicState.live, up, countdownTo: lastEntry(up));
        if (inProgress && now < hardCap(up)) return AicView(AicState.live, up, countdownTo: hardCap(up));
        return AicView(AicState.entryClosed, up);
      }
      if (!exists(up + 1)) return const AicView(AicState.off, 0);
      if (regAt != null) return AicView(AicState.registeredNext, up + 1, countdownTo: start(up + 1));
      return AicView(AicState.regNext, up + 1, countdownTo: regClose(up + 1));
    }

    // a paper still open past midnight (hard stop 12:30 am)
    if (prev >= 1 && inProgress && !submitted.contains(prev) && inRound(prev, regAt) && now < hardCap(prev)) {
      return AicView(AicState.live, prev, countdownTo: hardCap(prev));
    }
    if (prev >= 1 && submitted.contains(prev) && now < resultAt(prev)) {
      return AicView(AicState.submitted, prev, countdownTo: resultAt(prev));
    }
    if (up == 0) return AicView(AicState.off, 0, resultsRound: results);
    if (regAt == null) {
      if (now < regClose(up)) return AicView(AicState.regOpen, up, countdownTo: regClose(up), resultsRound: results);
      if (!exists(up + 1)) return AicView(AicState.off, 0, resultsRound: results);
      return AicView(AicState.regNext, up + 1, countdownTo: regClose(up + 1), resultsRound: results);
    }
    if (inRound(up, regAt)) return AicView(AicState.registered, up, countdownTo: start(up), resultsRound: results);
    if (!exists(up + 1)) return AicView(AicState.off, 0, resultsRound: results);
    return AicView(AicState.registeredNext, up + 1, countdownTo: start(up + 1), resultsRound: results);
  }
}

final AicSeries aicCgl = AicSeries(
  key: 'cgl',
  exam: 'ssc-cgl',
  name: 'SSC CGL Tier 2',
  short: 'CGL Tier 2',
  day: 'Sunday',
  regField: 'aic',
  regBoard: 'aic-registered',
  tag: '',
  paperMin: 135,
  hardStopMin: 145,
  parts: true,
  paperLine: '150 questions, +3 / −1, five timed parts (Maths 30 min, Reasoning 30, English 40, General Awareness 20, Computer 15).',
  firstMs: DateTime.utc(2026, 11, 29, 3, 30).millisecondsSinceEpoch, // Sunday 29 Nov 2026, 9:00 am IST
  lastRound: 0,
);

final AicSeries aicChsl = AicSeries(
  key: 'chsl',
  exam: 'ssc-chsl',
  name: 'SSC CHSL Tier 1',
  short: 'CHSL Tier 1',
  day: 'Saturday',
  regField: 'aicChsl',
  regBoard: 'aic-chsl-registered',
  tag: 'chsl_',
  paperMin: 60,
  hardStopMin: 70,
  parts: true,
  paperLine: '100 questions, +2 / −0.5, four timed parts of 15 minutes (English, Reasoning, Maths, General Awareness).',
  firstMs: DateTime.utc(2026, 11, 28, 3, 30).millisecondsSinceEpoch, // Saturday 28 Nov 2026, 9:00 am IST
  lastRound: 5, // 28 Nov, 5, 12, 19 and 26 Dec 2026
);

final List<AicSeries> aicAll = [aicChsl, aicCgl];

/// True when at least one series is switched on.
bool get aicAnyOn => aicAll.any((s) => s.on);

/// catalog.json: "aic" is the CGL Tier 2 series, "aicChsl" the CHSL Tier 1 one.
void aicApplyCatalog(dynamic j) {
  if (j is! Map) return;
  aicCgl.apply(j['aic']);
  aicChsl.apply(j['aicChsl']);
}

final _idRe = RegExp(r'^(ssc-cgl|ssc-chsl)_aic_mock(\d+)(?:_|$)');

/// The series of an All India Challenge id (mock id, board or leaderboard key); null for anything else.
AicSeries? aicSeriesOf(String id) {
  final m = _idRe.firstMatch(id);
  return m == null ? null : (m.group(1) == 'ssc-chsl' ? aicChsl : aicCgl);
}

/// The round of an All India Challenge id; 0 for anything else.
int aicRoundOf(String id) {
  final m = _idRe.firstMatch(id);
  return m == null ? 0 : int.parse(m.group(2)!);
}

/// One run of a paper: the live attempt of the challenge day, or the free mock taken after the result.
class AicRun {
  final AicSeries series;
  final int round;
  final bool live;
  const AicRun(this.series, this.round, this.live);
  int get resultAt => series.resultAt(round);
  Map<String, dynamic> toAttempt() => live ? {'round': round, 'live': true, 'resultAt': resultAt, if (aicPreviewOn) 'preview': true} : {'round': round, 'live': false};
}

// ------------------------------------------------------------------ the owner's test clock
// TSSC-AICADMIN-V1 (same as the website): the owner's login may move the challenge clock on this phone to walk
// through a round. A test taken with the clock moved is a preview: no leaderboard row, no statistics, no rating row.
const aicAdminEmails = {'nirala01@gmail.com'};

/// Milliseconds added to the server time (0 = the real date). Set only by AicClock, only for the owner's login.
int aicAdminShift = 0;
bool get aicPreviewOn => aicAdminShift != 0;

// ------------------------------------------------------------------ hold back

/// The series an attempt belongs to (by its paper id, else by its exam).
AicSeries aicSeriesOfAttempt(Map a) => aicSeriesOf('${a['mockId'] ?? ''}') ?? ('${a['exam'] ?? ''}' == 'ssc-chsl' ? aicChsl : aicCgl);

/// When the result of this attempt opens (0 = it is not a live challenge attempt).
int aicAttemptResultAt(Map a) {
  final x = a['aic'];
  if (x is! Map || x['live'] != true) return 0;
  final r = x['resultAt'];
  if (r is num && r > 0) return r.toInt();
  final n = x['round'];
  return n is num && n >= 1 ? aicSeriesOfAttempt(a).resultAt(n.toInt()) : 0;
}

/// A live challenge attempt before its result time: hidden everywhere (My Tests, dashboard, analysis, solutions, rank).
bool aicIsHeld(Map a, int now) => now < aicAttemptResultAt(a);

/// The leaderboard of a round is closed until its result time.
bool aicBoardClosed(String key, int now) {
  final s = aicSeriesOf(key);
  return s != null && now < s.resultAt(aicRoundOf(key));
}

// ------------------------------------------------------------------ what the student sees

enum AicState {
  off, // switched off, or the series is over
  regOpen, // not registered, registration for the coming round is open
  regNext, // not registered, the coming / running round is closed: registering now is for the round after
  registered, // registered in time for the coming round
  registeredNext, // registered, but after this round's registration closed: in from the next round
  live, // challenge day, registered in time, not submitted: may start (or resume)
  entryClosed, // challenge day after the last entry, never started
  submitted, // live attempt submitted, the result is not out yet
}

class AicView {
  final AicState state;
  final int round; // the round the state is about (regNext / registeredNext: the round the student will be in)
  final int countdownTo; // ms the countdown runs to (0 = none)
  final int resultsRound; // "Challenge Mock N results are out" (result time to the next round's start); 0 = none
  const AicView(this.state, this.round, {this.countdownTo = 0, this.resultsRound = 0});
  @override
  String toString() => '${state.name} r$round${resultsRound > 0 ? ' results$resultsRound' : ''}';
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
