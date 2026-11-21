// Run by .github/workflows/build-flutter.yml before the build (never by hand):
//     dart run tool/aic_check.dart
// Walks the All India Challenge through every state with a faked server time. Any wrong state fails the build.
import 'dart:io';

import 'package:trickyssc/aic.dart';

var _fails = 0, _n = 0;

void eq(Object? got, Object? want, String what) {
  _n++;
  if ('$got' != '$want') {
    _fails++;
    stdout.writeln('FAIL  $what: got $got, want $want');
  }
}

/// IST wall time -> ms.
int ist(int y, int mo, int d, [int h = 0, int mi = 0]) => DateTime.utc(y, mo, d, h, mi).millisecondsSinceEpoch - (5 * 60 + 30) * 60000;

String st(AicView v) => v.toString();

final C = aicCgl; // SSC CGL Tier 2, Sundays
final H = aicChsl; // SSC CHSL Tier 1, Saturdays

void main() {
  C.apply({'on': true, 'first': '2026-11-29T09:00:00+05:30', 'lastRound': 0});

  // ---- schedule (round 2 = Sunday 6 Dec 2026)
  eq(C.start(1), ist(2026, 11, 29, 9), 'round 1 start');
  eq(C.start(2), ist(2026, 12, 6, 9), 'round 2 start');
  eq(C.regClose(2), ist(2026, 12, 6, 0), 'round 2 registration closes Saturday midnight');
  eq(C.lastEntry(2), ist(2026, 12, 6, 21, 45), 'round 2 last entry 9:45 pm');
  eq(C.windowEnd(2), ist(2026, 12, 7, 0), 'round 2 window ends Sunday midnight');
  eq(C.hardCap(2), ist(2026, 12, 7, 0, 30), 'round 2 hard cap 12:30 am');
  eq(C.resultAt(2), ist(2026, 12, 8, 9), 'round 2 result Tuesday 9 am');
  eq(aicWhen(C.resultAt(2)), 'Tue 8 Dec, 9 am', 'result date text');
  eq(aicWhen(C.lastEntry(2)), 'Sun 6 Dec, 9:45 pm', 'last entry text');

  // ---- hard stop: 2 h 25 min after the first start, never after 12:30 am
  eq(C.hardStop(2, ist(2026, 12, 6, 9)), ist(2026, 12, 6, 11, 25), 'hard stop, started 9:00 am');
  eq(C.hardStop(2, ist(2026, 12, 6, 21, 45)), ist(2026, 12, 7, 0, 10), 'hard stop, started 9:45 pm');
  eq(C.hardStop(2, ist(2026, 12, 6, 22, 30)), ist(2026, 12, 7, 0, 30), 'hard stop is capped at 12:30 am');

  // ---- which round
  eq(C.upRound(ist(2026, 11, 25)), 1, 'before round 1');
  eq(C.upRound(ist(2026, 11, 29, 23, 59)), 1, 'Sunday 11:59 pm is still round 1');
  eq(C.upRound(ist(2026, 11, 30, 0, 0)), 2, 'Monday 0:00 moves to round 2');
  eq(C.upRound(ist(2026, 12, 6, 12)), 2, 'Sunday noon, round 2');
  eq(C.finished(ist(2026, 12, 1, 8, 59)), <int>[], 'no result before Tuesday 9 am');
  eq(C.finished(ist(2026, 12, 1, 9)), [1], 'round 1 result out Tuesday 9 am');
  eq(C.finished(ist(2026, 12, 8, 9)), [2, 1], 'round 2 result out');

  final early = ist(2026, 11, 20); // registered long ago
  final sat11 = ist(2026, 12, 5, 23, 59); // one minute before round 2 registration closes
  final late = ist(2026, 12, 6, 0, 0); // exactly at close: too late for round 2
  eq(C.inRound(2, sat11), true, 'registered Saturday 11:59 pm is in round 2');
  eq(C.inRound(2, late), false, 'registered Sunday 0:00 is not in round 2');
  eq(C.inRound(3, late), true, '... but is in round 3');
  eq(C.inRound(2, null), false, 'not registered');

  // ---- states, Wednesday 2 Dec (round 1 results are out, round 2 coming)
  var now = ist(2026, 12, 2, 10);
  eq(st(C.view(now: now)), 'regOpen r2 results1', 'Wed, not registered');
  eq(C.view(now: now).countdownTo, C.regClose(2), 'Wed, countdown to registration close');
  eq(st(C.view(now: now, regAt: early)), 'registered r2 results1', 'Wed, registered');
  eq(C.view(now: now, regAt: early).countdownTo, C.start(2), 'Wed, countdown to Sunday 9 am');

  // ---- Sunday 6 Dec, 2 am (registration for round 2 closed, test not started)
  now = ist(2026, 12, 6, 2);
  eq(st(C.view(now: now)), 'regNext r3 results1', 'Sun 2 am, not registered: next round');
  eq(st(C.view(now: now, regAt: early)), 'registered r2 results1', 'Sun 2 am, registered in time');
  eq(st(C.view(now: now, regAt: late)), 'registeredNext r3 results1', 'Sun 2 am, registered late');

  // ---- Sunday 6 Dec, live window
  now = ist(2026, 12, 6, 9);
  eq(st(C.view(now: now, regAt: early)), 'live r2', 'Sun 9:00 am, live');
  eq(st(C.view(now: now)), 'regNext r3', 'Sun 9 am, not registered');
  eq(st(C.view(now: now, regAt: late)), 'registeredNext r3', 'Sun 9 am, registered late');
  now = ist(2026, 12, 6, 21, 45);
  eq(st(C.view(now: now, regAt: early)), 'live r2', 'Sun 9:45 pm, last entry');
  now = ist(2026, 12, 6, 21, 46);
  eq(st(C.view(now: now, regAt: early)), 'entryClosed r2', 'Sun 9:46 pm, entry closed');
  eq(st(C.view(now: now, regAt: early, inProgress: true)), 'live r2', 'Sun 9:46 pm, already started: may resume');
  eq(st(C.view(now: now, regAt: early, submitted: {2})), 'submitted r2', 'Sun, submitted');
  eq(C.view(now: now, regAt: early, submitted: {2}).countdownTo, C.resultAt(2), 'submitted, countdown to result');

  // ---- after midnight
  now = ist(2026, 12, 7, 0, 10);
  eq(st(C.view(now: now, regAt: early, inProgress: true)), 'live r2', 'Mon 0:10 am, paper still open');
  now = ist(2026, 12, 7, 0, 31);
  eq(st(C.view(now: now, regAt: early, inProgress: true)), 'registered r3', 'Mon 0:31 am, past the hard cap');
  now = ist(2026, 12, 7, 12);
  eq(st(C.view(now: now, regAt: early, submitted: {2})), 'submitted r2', 'Mon, submitted, result pending');
  eq(st(C.view(now: now, regAt: early)), 'registered r3', 'Mon, did not take round 2');
  eq(st(C.view(now: now)), 'regOpen r3', 'Mon, not registered');

  // ---- Tuesday 8 Dec 9 am: results out, until the next Sunday 9 am
  now = ist(2026, 12, 8, 8, 59);
  eq(st(C.view(now: now, regAt: early, submitted: {2})), 'submitted r2', 'Tue 8:59 am, still held');
  now = ist(2026, 12, 8, 9);
  eq(st(C.view(now: now, regAt: early, submitted: {2})), 'registered r3 results2', 'Tue 9 am, results out');
  eq(st(C.view(now: now)), 'regOpen r3 results2', 'Tue 9 am, results out, not registered');
  now = ist(2026, 12, 13, 8, 59);
  eq(C.view(now: now, regAt: early).resultsRound, 2, 'Sun 8:59 am, results still shown');
  now = ist(2026, 12, 13, 9);
  eq(C.view(now: now, regAt: early).resultsRound, 0, 'Sun 9 am, results note ends');
  eq(st(C.view(now: now, regAt: early)), 'live r3', 'Sun 9 am, round 3 live');

  // ---- hold back
  final liveAtt = {'aic': {'round': 2, 'live': true, 'resultAt': C.resultAt(2)}};
  final webAtt = {'aic': {'round': 2, 'live': true}}; // no resultAt: worked out from the round
  final freeAtt = {'aic': {'round': 2, 'live': false}};
  eq(aicIsHeld(liveAtt, ist(2026, 12, 8, 8, 59)), true, 'live attempt hidden before Tuesday 9 am');
  eq(aicIsHeld(liveAtt, ist(2026, 12, 8, 9)), false, 'live attempt shown from Tuesday 9 am');
  eq(aicIsHeld(webAtt, ist(2026, 12, 7)), true, 'attempt without resultAt hidden by its round');
  eq(aicIsHeld(freeAtt, ist(2026, 12, 7)), false, 'free mock is never hidden');
  eq(aicIsHeld({'mockId': 'ssc-cgl_tier2_mock1_en'}, ist(2026, 12, 7)), false, 'an ordinary mock is never hidden');
  eq(aicBoardClosed('ssc-cgl_aic_mock2', ist(2026, 12, 8, 8, 59)), true, 'board closed before the result');
  eq(aicBoardClosed('ssc-cgl_aic_mock2', ist(2026, 12, 8, 9)), false, 'board open from the result');
  eq(aicBoardClosed('ssc-cgl_tier2_mock2', ist(2026, 12, 7)), false, 'ordinary board is never closed');

  // ---- ids
  eq(C.mockId(2, 'hi'), 'ssc-cgl_aic_mock2_hi', 'mock id');
  eq(aicRoundOf('ssc-cgl_aic_mock12_en'), 12, 'round of a mock id');
  eq(aicRoundOf('ssc-cgl_aic_mock3'), 3, 'round of a board');
  eq(aicRoundOf('ssc-cgl_tier2_mock3_en'), 0, 'not a challenge id');
  eq(AicRun(C, 2, true).toAttempt(), {'round': 2, 'live': true, 'resultAt': C.resultAt(2)}, 'live attempt block');
  eq(AicRun(C, 2, false).toAttempt(), {'round': 2, 'live': false}, 'free mock attempt block');

  // ================= SSC CHSL Tier 1: Saturdays, 28 Nov to 26 Dec 2026 (5 rounds), one 60-minute clock
  aicApplyCatalog({
    'aic': {'on': true, 'first': '2026-11-29T09:00:00+05:30', 'lastRound': 0},
    'aicChsl': {'on': true, 'first': '2026-11-28T09:00:00+05:30', 'lastRound': 5},
  });
  eq(H.start(1), ist(2026, 11, 28, 9), 'CHSL round 1 start, Saturday 9 am');
  eq(H.start(5), ist(2026, 12, 26, 9), 'CHSL round 5 is 26 Dec');
  eq(H.regClose(2), ist(2026, 12, 5, 0), 'CHSL registration closes Friday midnight');
  eq(H.lastEntry(2), ist(2026, 12, 5, 23, 0), 'CHSL last entry 11 pm');
  eq(H.windowEnd(2), ist(2026, 12, 6, 0), 'CHSL window ends Saturday midnight');
  eq(H.resultAt(2), ist(2026, 12, 7, 9), 'CHSL result Monday 9 am');
  eq(aicWhen(H.resultAt(2)), 'Mon 7 Dec, 9 am', 'CHSL result date text');
  eq(H.hardStop(2, ist(2026, 12, 5, 9)), ist(2026, 12, 5, 10, 10), 'CHSL hard stop 70 minutes after the start');
  eq(H.hardStop(2, ist(2026, 12, 5, 23, 0)), ist(2026, 12, 6, 0, 10), 'CHSL hard stop, started 11 pm');
  eq(H.hardStop(2, ist(2026, 12, 5, 23, 40)), ist(2026, 12, 6, 0, 30), 'CHSL hard stop capped at 12:30 am');
  eq(H.exists(5), true, 'CHSL round 5 exists');
  eq(H.exists(6), false, 'CHSL has no round 6');
  eq(H.upRound(ist(2026, 12, 26, 12)), 5, 'CHSL last Saturday');
  eq(H.upRound(ist(2026, 12, 27, 0, 0)), 0, 'CHSL series over after 26 Dec');
  eq(H.mockId(3, 'hi'), 'ssc-chsl_aic_mock3_hi', 'CHSL mock id');
  eq(H.board(3), 'ssc-chsl_aic_mock3', 'CHSL board');
  eq(aicSeriesOf('ssc-chsl_aic_mock3_en')?.key, 'chsl', 'series of a CHSL id');
  eq(aicSeriesOf('ssc-cgl_aic_mock3')?.key, 'cgl', 'series of a CGL id');
  eq(aicSeriesOf('ssc-chsl_tier1_mock3_en'), null, 'an ordinary CHSL mock is no challenge');
  eq(aicRoundOf('ssc-chsl_aic_mock4_en'), 4, 'round of a CHSL id');
  eq(H.regField, 'aicChsl', 'CHSL registration field');
  eq(H.regBoard, 'aic-chsl-registered', 'CHSL registration board');
  eq(C.regField, 'aic', 'CGL registration field');
  eq(C.regBoard, 'aic-registered', 'CGL registration board');

  final hEarly = ist(2026, 11, 20);
  var t = ist(2026, 12, 2, 10); // Wednesday: round 1 result out (Mon 30 Nov), round 2 coming
  eq(st(H.view(now: t)), 'regOpen r2 results1', 'CHSL Wed, not registered');
  eq(st(H.view(now: t, regAt: hEarly)), 'registered r2 results1', 'CHSL Wed, registered');
  t = ist(2026, 12, 5, 9);
  eq(st(H.view(now: t, regAt: hEarly)), 'live r2', 'CHSL Sat 9 am, live');
  eq(st(H.view(now: t, regAt: ist(2026, 12, 5, 0, 0))), 'registeredNext r3', 'CHSL registered after Friday midnight');
  eq(st(H.view(now: t)), 'regNext r3', 'CHSL Sat, not registered');
  t = ist(2026, 12, 5, 23, 0);
  eq(st(H.view(now: t, regAt: hEarly)), 'live r2', 'CHSL Sat 11:00 pm, last entry');
  t = ist(2026, 12, 5, 23, 1);
  eq(st(H.view(now: t, regAt: hEarly)), 'entryClosed r2', 'CHSL Sat 11:01 pm, entry closed');
  eq(st(H.view(now: t, regAt: hEarly, inProgress: true)), 'live r2', 'CHSL 11:01 pm, started: may resume');
  eq(st(H.view(now: t, regAt: hEarly, submitted: {2})), 'submitted r2', 'CHSL submitted');
  t = ist(2026, 12, 7, 8, 59);
  eq(st(H.view(now: t, regAt: hEarly, submitted: {2})), 'submitted r2', 'CHSL Mon 8:59 am, still held');
  t = ist(2026, 12, 7, 9);
  eq(st(H.view(now: t, regAt: hEarly, submitted: {2})), 'registered r3 results2', 'CHSL Mon 9 am, results out');
  // the last round and after it
  t = ist(2026, 12, 26, 12);
  eq(st(H.view(now: t, regAt: hEarly)), 'live r5', 'CHSL last Saturday, live');
  eq(st(H.view(now: t)), 'off r0', 'CHSL last Saturday, not registered: nothing left to register for');
  t = ist(2026, 12, 28, 10);
  eq(st(H.view(now: t, regAt: hEarly)), 'off r0 results5', 'CHSL after the last round: its result');
  t = ist(2027, 1, 2, 9);
  eq(st(H.view(now: t, regAt: hEarly)), 'off r0', 'CHSL a week after the last round: nothing');
  eq(H.finished(ist(2027, 2, 1)), [5, 4, 3, 2, 1], 'CHSL finished rounds');

  // hold back and board of a CHSL attempt; the two series do not mix
  final chAtt = {'exam': 'ssc-chsl', 'mockId': 'ssc-chsl_aic_mock2_en', 'aic': {'round': 2, 'live': true}};
  eq(aicIsHeld(chAtt, ist(2026, 12, 7, 8, 59)), true, 'CHSL live attempt hidden before Monday 9 am');
  eq(aicIsHeld(chAtt, ist(2026, 12, 7, 9)), false, 'CHSL live attempt shown from Monday 9 am');
  eq(aicBoardClosed('ssc-chsl_aic_mock2', ist(2026, 12, 7, 8, 59)), true, 'CHSL board closed before the result');
  eq(aicBoardClosed('ssc-chsl_aic_mock2', ist(2026, 12, 7, 9)), false, 'CHSL board open from the result');
  eq(aicBoardClosed('ssc-cgl_aic_mock2', ist(2026, 12, 7, 9)), true, 'CGL board of the same weekend still closed on Monday');
  eq(AicRun(H, 2, true).toAttempt(), {'round': 2, 'live': true, 'resultAt': H.resultAt(2)}, 'CHSL live attempt block');
  eq(st(C.view(now: ist(2026, 12, 2, 10))), 'regOpen r2 results1', 'CGL is unchanged by the CHSL series');


  // ---- a last round, and the switch
  C.apply({'on': true, 'first': '2026-11-29T09:00:00+05:30', 'lastRound': 2});
  eq(C.upRound(ist(2026, 12, 7, 12)), 0, 'series over after the last round');
  eq(st(C.view(now: ist(2026, 12, 6, 12))), 'off r0', 'last Sunday, not registered: no next round');
  eq(st(C.view(now: ist(2026, 12, 9), regAt: early)), 'off r0 results2', 'after the last round: only its result');
  eq(st(C.view(now: ist(2026, 12, 14), regAt: early)), 'off r0', 'a week later: nothing');
  eq(C.finished(ist(2027, 1, 1)), [2, 1], 'finished rounds stop at the last round');
  C.apply({'on': false});
  eq(st(C.view(now: ist(2026, 12, 2), regAt: early)), 'off r0', 'switched off');

  stdout.writeln(_fails == 0 ? 'All India Challenge: $_n checks passed.' : 'All India Challenge: $_fails of $_n checks FAILED.');
  if (_fails > 0) exit(1);
}
