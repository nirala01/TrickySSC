S = {}
S[1] = dict(raw=r"""Step 1: Study ON → MG
O (15) − 2 = M (13) and N (14) − 7 = G (7). So the first letter moves 2 back and the second letter moves 7 back.
Step 2: Confirm with UC → SV
U (21) − 2 = S (19); C (3) − 7 goes past A and wraps round to V (22) ✓ — the same −2, −7 rule.
Step 3: Work back from WW
The missing cluster must give W and W after −2 and −7. So its first letter is W (23) + 2 = Y (25), and its second letter is W (23) + 7 = 30 − 26 = 4 = D.
Step 4: Answer and check
The missing cluster is YD. Check: Y − 2 = W and D − 7 = W (D → C → B → A → Z → Y → X → W) ✓""", trick=r"Find the shift from a complete pair, then reverse it on the given cluster.")
S[2] = dict(raw=r"""Step 1: Read the first set (SK, WO, AS)
First letters S → W → A move +4 each time (W + 4 wraps to A). Second letters K → O → S also move +4.
Step 2: Confirm with (BG, FK, JO)
B → F → J is +4, +4 and G → K → O is +4, +4 ✓
Step 3: Test the options
(CO, GS, KW): C → G → K is +4, +4 and O → S → W is +4, +4 ✓
(NF, PJ, VN) starts N → P (+2); (WS, CW, EA) starts W → C (+6); (SU, XY, AC) starts S → X (+5) — all break the rule.
Step 4: Answer
The set (CO, GS, KW) follows the same +4 rule.""", trick=r"Check the first letters and the second letters separately — here both jump +4.")
S[3] = dict(raw=r"""Step 1: Know the year
2011 is an ordinary year (not divisible by 4), so we need a later ordinary year that starts on the same day.
Step 2: Count odd days year by year
An ordinary year gives 1 odd day and a leap year 2. From 2011 to 2021 there are 11 years, of which 2012, 2016 and 2020 are leap years: 11 + 3 = 14 odd days.
Step 3: Check the total
14 odd days = 2 complete weeks, so 1 January 2022 falls on the same day as 1 January 2011, and 2022 is also an ordinary year ✓
Step 4: Rule out the others
Up to 2017 the count is 8 (one odd day left over), up to 2023 it is 15 (one left over) and up to 2035 it is 30 (two left over). So 2022 is the answer.""", trick=r"An ordinary year that follows a leap year repeats after 11 years: 2011 → 2022.")
S[4] = dict(raw=r"""Step 1: Set up the row
All face north, so their left is our left. There are 5 seats, numbered 1 to 5 from left to right.
Step 2: Place P, L and J
L is second to the right of P and second to the left of J: P _ L _ J. With only 5 seats, P = 1, L = 3 and J = 5.
Step 3: Place K and Q
Seats 2 and 4 are left. K is second to the left of Q, so K = 2 and Q = 4.
Order: P, K, L, Q, J.
Step 4: Answer
The middle seat (3) belongs to L.""", trick=r"Two 'second to the left/right' clues spanning 4 seats fix the whole row of 5.")
S[5] = dict(raw=r"""Step 1: Fix Q and V
Facing the centre, "right" means anticlockwise. Number the seats clockwise from Q = 0. V is fourth to the right of Q, so V is 4 seats anticlockwise, i.e. seat 3 clockwise.
Step 2: Place S and T
Going left (clockwise) from S there is 1 student between S and Q, so S is 2 seats anticlockwise from Q: seat 5. T must not sit next to V (seats 2, 4) or S (seats 4, 6), so T takes seat 1.
Step 3: Place P, U and R
Seats 2, 4 and 6 remain. P is fourth to the right of U: U = 6 gives P = 2 (U = 2 or 4 would put P on S or Q). So R = 4.
Clockwise: Q, T, P, V, R, S, U.
Step 4: Count from T towards the left
Going left (clockwise) from T: P, V, R and then S. So 3 students sit between T and S.""", trick=r"Facing the centre: left = clockwise, right = anticlockwise. Fix the definite pair first.")
S[6] = dict(raw=r"""Step 1: List the letters of CATASTROPHE
C, A, A, T, T, S, R, O, P, H, E — A and T appear twice, every other letter once. There is no D.
Step 2: Check ATTACHED
It needs A, T, T, A, C, H, E and D. Every letter is available except D.
Step 3: Check the other words
CARPET (C, A, R, P, E, T), CHEAP (C, H, E, A, P) and HORSE (H, O, R, S, E) use only available letters.
Step 4: Answer
ATTACHED cannot be formed because CATASTROPHE has no D.""", trick=r"Look first for a letter that is missing from the given word.")
S[7] = dict(raw=r"""Step 1: List the letters of CONGRATULATIONS
C, O, O, N, N, G, R, A, A, T, T, U, L, I, S — there is no E, F or M.
Step 2: Check GROAN
G, R, O, A and N are all available, so GROAN can be formed.
Step 3: Check the other words
CONSENT and RENT need E; UNIFORM needs F and M — none of these letters is present.
Step 4: Answer
Only GROAN can be formed from CONGRATULATIONS.""", trick=r"Strike out every option containing a letter that is not in the given word.")
S[8] = dict(raw=r"""Step 1: Find the differences
340 − 325 = 15, 355 − 340 = 15, 370 − 355 = 15.
Step 2: Spot the pattern
The series goes up by a constant 15.
Step 3: Next term
370 + 15 = 385.
Step 4: Check
325, 340, 355, 370, 385 — each step +15 ✓""", trick=r"Constant difference series: add the same number again.")
S[9] = dict(raw=r"""Step 1: Find the differences
601 − 597 = 4, 597 − 589 = 8, 589 − 577 = 12.
Step 2: Spot the pattern
The amount subtracted grows by 4 each time: 4, 8, 12, so the next is 16.
Step 3: Next term
577 − 16 = 561.
Step 4: Check
Differences 4, 8, 12, 16 are multiples of 4 ✓""", trick=r"Differences 4, 8, 12, 16 — the table of 4.")
S[10] = dict(raw=r"""Step 1: Test multiply-and-subtract
8 × 3 − 1 = 23 and 23 × 4 − 2 = 90.
Step 2: Confirm the pattern
90 × 5 − 3 = 447 and 447 × 6 − 4 = 2678 ✓ — multiply by 3, 4, 5, 6 and subtract 1, 2, 3, 4.
Step 3: Next term
2678 × 7 − 5 = 18746 − 5 = 18741.
Step 4: Answer
The next number is 18,741.""", trick=r"Big jumps → try × n − k with both n and k increasing.")
S[11] = dict(raw=r"""Step 1: Read the first figure
Left column A, B, C and right column D, E, F (top to bottom).
Step 2: Compare with the second figure
Left column becomes C, A, B and right column F, D, E — in each column the bottom letter moves to the top and the others shift down by one.
Step 3: Apply the rule to the third figure
Left column G, H, I becomes I, G, H; right column J, K, L becomes L, J, K.
Step 4: Match the options
The required figure reads I L / G J / H K (rows). The figure with right column L, K, J, the one with left column L, G, H and the one with J and G swapped do not fit.""", trick=r"Track each column separately — here both rotate one step down.")
S[12] = dict(raw=r"""Step 1: Read the first pair
The plain hexagon gets one arrow on each of its 6 sides: 3 arrows on adjacent sides point inwards and the other 3 point outwards.
Step 2: Find the rule
Half the sides carry inward arrows and half carry outward arrows, each group on adjacent sides.
Step 3: Apply it to the square
A square has 4 sides, so it needs 2 inward arrows on two adjacent sides and 2 outward arrows on the other two.
Step 4: Match the options
The other figures show 3 inward + 1 outward, 1 inward + 3 outward and all 4 outward. Only the figure with top and left arrows outward and right and bottom arrows inward has the 2-in, 2-out split.""", trick=r"Count the arrows in and out: hexagon 3 + 3, so square 2 + 2.")
S[13] = dict(raw=r"""Step 1: Study the first pair (AF150 to ZE270)
A − 1 = Z, F − 1 = E and 150 + 120 = 270.
Step 2: Confirm with the third pair (TL200 to SK320)
T − 1 = S, L − 1 = K and 200 + 120 = 320 ✓
Step 3: Work back from JP190
The missing cluster must give J, P and 190 after −1, −1, +120: J + 1 = K, P + 1 = Q and 190 − 120 = 70.
Step 4: Answer
The missing cluster is KQ70. Check: K − 1 = J, Q − 1 = P, 70 + 120 = 190 ✓""", trick=r"Letters −1, −1 and number +120 — reverse it for the missing term.")
S[14] = dict(raw=r"""Step 1: Study the first pair (LM230 to ER330)
L (12) − 7 = E (5), M (13) + 5 = R (18) and 230 + 100 = 330.
Step 2: Confirm with the third pair (TU310 to MZ410)
T (20) − 7 = M (13), U (21) + 5 = Z (26) and 310 + 100 = 410 ✓
Step 3: Apply to JK420
J (10) − 7 = C (3), K (11) + 5 = P (16) and 420 + 100 = 520.
Step 4: Answer
The missing cluster is CP520.""", trick=r"First letter −7, second letter +5, number +100.")
S[15] = dict(raw=r"""Step 1: Study the second pair (6368 to 6318)
6368 − 50 = 6318.
Step 2: Confirm with the third pair (6850 to 6800)
6850 − 50 = 6800 ✓
Step 3: Apply to 4543
4543 − 50 = 4493.
Step 4: Answer
The missing number is 4493.""", trick=r"Each pair differs by exactly 50.")
S[16] = dict(raw=r"""Step 1: Study the first pair (347 to 685)
347 × 2 = 694 and 694 − 9 = 685.
Step 2: Confirm with the third pair (610 to 1211)
610 × 2 = 1220 and 1220 − 9 = 1211 ✓
Step 3: Reverse the rule for 1903
Missing number × 2 − 9 = 1903, so missing number × 2 = 1912 and the missing number = 956.
Step 4: Check
956 × 2 − 9 = 1912 − 9 = 1903 ✓""", trick=r"Second number = 2 × first − 9; reverse: add 9, then halve.")
S[17] = dict(raw=r"""Step 1: Compare LOLL with MSHG
L → M (+1), O → S (+4), L → H (−4), L → G (−5).
Step 2: Confirm with ULNA to VPJV
U → V (+1), L → P (+4), N → J (−4), A → V (−5, wrapping from A back to V) ✓
Step 3: Apply +1, +4, −4, −5 to YARN
Y + 1 = Z, A + 4 = E, R − 4 = N, N − 5 = I.
Step 4: Answer
YARN is coded as ZENI.""", trick=r"Same position, same shift: +1, +4, −4, −5.")
S[18] = dict(raw=r"""Step 1: Compare ELUTE with FNXXJ
E → F (+1), L → N (+2), U → X (+3), T → X (+4), E → J (+5).
Step 2: Confirm with CRICK to DTLGP
C → D (+1), R → T (+2), I → L (+3), C → G (+4), K → P (+5) ✓
Step 3: Apply +1 to +5 to CLUED
C + 1 = D, L + 2 = N, U + 3 = X, E + 4 = I, D + 5 = I.
Step 4: Answer
CLUED is coded as DNXII.""", trick=r"Shift each letter by its position number: +1, +2, +3, +4, +5.")
S[19] = dict(raw=r"""Step 1: Check the first letters and the numbers
C, D, E, F, G, H move +1 each time, and 12, 24, 36, 48, 60, 72 go up by 12 — both parts are fine.
Step 2: Check the second letters
N (14), R (18), V (22) move +4, so the next should be Z (26), then D (4) and H (8).
Step 3: Find the break
The fourth term has Y instead of Z, while D and H in the next terms still follow the +4 rule.
Step 4: Answer
FY48 is the wrong term; it should be FZ48.""", trick=r"Split each term into parts and check every part separately.")
S[20] = dict(raw=r"""Step 1: Rate of losing time
From 2:20 PM to 8:20 PM (6 hours) the clock goes from 6 minutes slow to 12 minutes slow, so it loses 6 minutes in 6 hours = 1 minute per hour.
Step 2: Go back to zero error
At 2:20 PM it was 6 minutes slow. At 1 minute per hour, it lost those 6 minutes over the previous 6 hours.
Step 3: Find the time
6 hours before 2:20 PM is 8:20 AM, when the clock showed the correct time.
Step 4: Check
8:20 AM → 0 slow, 2:20 PM → 6 slow, 8:20 PM → 12 slow ✓ (it will next be right after losing 12 hours = 720 hours later, again at 8:20 AM).""", trick=r"Error grows 1 minute per hour → go back as many hours as the minutes of error.")
