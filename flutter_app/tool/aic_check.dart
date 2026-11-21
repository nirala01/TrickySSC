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

void main() {
  aicApplyCatalog({'on': true, 'first': '2026-11-29T09:00:00+05:30', 'lastRound': 0});

  // ---- schedule (round 2 = Sunday 6 Dec 2026)
  eq(aicStart(1), ist(2026, 11, 29, 9), 'round 1 start');
  eq(aicStart(2), ist(2026, 12, 6, 9), 'round 2 start');
  eq(aicRegClose(2), ist(2026, 12, 6, 0), 'round 2 registration closes Saturday midnight');
  eq(aicLastEntry(2), ist(2026, 12, 6, 21, 45), 'round 2 last entry 9:45 pm');
  eq(aicWindowEnd(2), ist(2026, 12, 7, 0), 'round 2 window ends Sunday midnight');
  eq(aicHardCap(2), ist(2026, 12, 7, 0, 30), 'round 2 hard cap 12:30 am');
  eq(aicResultAt(2), ist(2026, 12, 8, 9), 'round 2 result Tuesday 9 am');
  eq(aicWhen(aicResultAt(2)), 'Tue 8 Dec, 9 am', 'result date text');
  eq(aicWhen(aicLastEntry(2)), 'Sun 6 Dec, 9:45 pm', 'last entry text');

  // ---- hard stop: 2 h 25 min after the first start, never after 12:30 am
  eq(aicHardStop(2, ist(2026, 12, 6, 9)), ist(2026, 12, 6, 11, 25), 'hard stop, started 9:00 am');
  eq(aicHardStop(2, ist(2026, 12, 6, 21, 45)), ist(2026, 12, 7, 0, 10), 'hard stop, started 9:45 pm');
  eq(aicHardStop(2, ist(2026, 12, 6, 22, 30)), ist(2026, 12, 7, 0, 30), 'hard stop is capped at 12:30 am');

  // ---- which round
  eq(aicUpRound(ist(2026, 11, 25)), 1, 'before round 1');
  eq(aicUpRound(ist(2026, 11, 29, 23, 59)), 1, 'Sunday 11:59 pm is still round 1');
  eq(aicUpRound(ist(2026, 11, 30, 0, 0)), 2, 'Monday 0:00 moves to round 2');
  eq(aicUpRound(ist(2026, 12, 6, 12)), 2, 'Sunday noon, round 2');
  eq(aicFinished(ist(2026, 12, 1, 8, 59)), <int>[], 'no result before Tuesday 9 am');
  eq(aicFinished(ist(2026, 12, 1, 9)), [1], 'round 1 result out Tuesday 9 am');
  eq(aicFinished(ist(2026, 12, 8, 9)), [2, 1], 'round 2 result out');

  final early = ist(2026, 11, 20); // registered long ago
  final sat11 = ist(2026, 12, 5, 23, 59); // one minute before round 2 registration closes
  final late = ist(2026, 12, 6, 0, 0); // exactly at close: too late for round 2
  eq(aicInRound(2, sat11), true, 'registered Saturday 11:59 pm is in round 2');
  eq(aicInRound(2, late), false, 'registered Sunday 0:00 is not in round 2');
  eq(aicInRound(3, late), true, '... but is in round 3');
  eq(aicInRound(2, null), false, 'not registered');

  // ---- states, Wednesday 2 Dec (round 1 results are out, round 2 coming)
  var now = ist(2026, 12, 2, 10);
  eq(st(aicView(now: now)), 'regOpen r2 results1', 'Wed, not registered');
  eq(aicView(now: now).countdownTo, aicRegClose(2), 'Wed, countdown to registration close');
  eq(st(aicView(now: now, regAt: early)), 'registered r2 results1', 'Wed, registered');
  eq(aicView(now: now, regAt: early).countdownTo, aicStart(2), 'Wed, countdown to Sunday 9 am');

  // ---- Sunday 6 Dec, 2 am (registration for round 2 closed, test not started)
  now = ist(2026, 12, 6, 2);
  eq(st(aicView(now: now)), 'regNext r3 results1', 'Sun 2 am, not registered: next round');
  eq(st(aicView(now: now, regAt: early)), 'registered r2 results1', 'Sun 2 am, registered in time');
  eq(st(aicView(now: now, regAt: late)), 'registeredNext r3 results1', 'Sun 2 am, registered late');

  // ---- Sunday 6 Dec, live window
  now = ist(2026, 12, 6, 9);
  eq(st(aicView(now: now, regAt: early)), 'live r2', 'Sun 9:00 am, live');
  eq(st(aicView(now: now)), 'regNext r3', 'Sun 9 am, not registered');
  eq(st(aicView(now: now, regAt: late)), 'registeredNext r3', 'Sun 9 am, registered late');
  now = ist(2026, 12, 6, 21, 45);
  eq(st(aicView(now: now, regAt: early)), 'live r2', 'Sun 9:45 pm, last entry');
  now = ist(2026, 12, 6, 21, 46);
  eq(st(aicView(now: now, regAt: early)), 'entryClosed r2', 'Sun 9:46 pm, entry closed');
  eq(st(aicView(now: now, regAt: early, inProgress: true)), 'live r2', 'Sun 9:46 pm, already started: may resume');
  eq(st(aicView(now: now, regAt: early, submitted: {2})), 'submitted r2', 'Sun, submitted');
  eq(aicView(now: now, regAt: early, submitted: {2}).countdownTo, aicResultAt(2), 'submitted, countdown to result');

  // ---- after midnight
  now = ist(2026, 12, 7, 0, 10);
  eq(st(aicView(now: now, regAt: early, inProgress: true)), 'live r2', 'Mon 0:10 am, paper still open');
  now = ist(2026, 12, 7, 0, 31);
  eq(st(aicView(now: now, regAt: early, inProgress: true)), 'registered r3', 'Mon 0:31 am, past the hard cap');
  now = ist(2026, 12, 7, 12);
  eq(st(aicView(now: now, regAt: early, submitted: {2})), 'submitted r2', 'Mon, submitted, result pending');
  eq(st(aicView(now: now, regAt: early)), 'registered r3', 'Mon, did not take round 2');
  eq(st(aicView(now: now)), 'regOpen r3', 'Mon, not registered');

  // ---- Tuesday 8 Dec 9 am: results out, until the next Sunday 9 am
  now = ist(2026, 12, 8, 8, 59);
  eq(st(aicView(now: now, regAt: early, submitted: {2})), 'submitted r2', 'Tue 8:59 am, still held');
  now = ist(2026, 12, 8, 9);
  eq(st(aicView(now: now, regAt: early, submitted: {2})), 'registered r3 results2', 'Tue 9 am, results out');
  eq(st(aicView(now: now)), 'regOpen r3 results2', 'Tue 9 am, results out, not registered');
  now = ist(2026, 12, 13, 8, 59);
  eq(aicView(now: now, regAt: early).resultsRound, 2, 'Sun 8:59 am, results still shown');
  now = ist(2026, 12, 13, 9);
  eq(aicView(now: now, regAt: early).resultsRound, 0, 'Sun 9 am, results note ends');
  eq(st(aicView(now: now, regAt: early)), 'live r3', 'Sun 9 am, round 3 live');

  // ---- hold back
  final liveAtt = {'aic': {'round': 2, 'live': true, 'resultAt': aicResultAt(2)}};
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
  eq(aicMockId(2, 'hi'), 'ssc-cgl_aic_mock2_hi', 'mock id');
  eq(aicRoundOf('ssc-cgl_aic_mock12_en'), 12, 'round of a mock id');
  eq(aicRoundOf('ssc-cgl_aic_mock3'), 3, 'round of a board');
  eq(aicRoundOf('ssc-cgl_tier2_mock3_en'), 0, 'not a challenge id');
  eq(const AicRun(2, true).toAttempt(), {'round': 2, 'live': true, 'resultAt': aicResultAt(2)}, 'live attempt block');
  eq(const AicRun(2, false).toAttempt(), {'round': 2, 'live': false}, 'free mock attempt block');

  // ---- a last round, and the switch
  aicApplyCatalog({'on': true, 'first': '2026-11-29T09:00:00+05:30', 'lastRound': 2});
  eq(aicUpRound(ist(2026, 12, 7, 12)), 0, 'series over after the last round');
  eq(st(aicView(now: ist(2026, 12, 6, 12))), 'off r0', 'last Sunday, not registered: no next round');
  eq(st(aicView(now: ist(2026, 12, 9), regAt: early)), 'off r0 results2', 'after the last round: only its result');
  eq(st(aicView(now: ist(2026, 12, 14), regAt: early)), 'off r0', 'a week later: nothing');
  eq(aicFinished(ist(2027, 1, 1)), [2, 1], 'finished rounds stop at the last round');
  aicApplyCatalog({'on': false});
  eq(st(aicView(now: ist(2026, 12, 2), regAt: early)), 'off r0', 'switched off');

  stdout.writeln(_fails == 0 ? 'All India Challenge: $_n checks passed.' : 'All India Challenge: $_fails of $_n checks FAILED.');
  if (_fails > 0) exit(1);
}
