S = {}
S[1] = dict(raw=r"""Step 1: Study FA → DW
F (6) − 2 = D (4) and A (1) − 4 goes back past A and wraps round to W (23). So the first letter moves 2 back and the second letter moves 4 back.
Step 2: Confirm with PK → NG
P (16) − 2 = N (14) and K (11) − 4 = G (7) ✓ — the same −2, −4 rule.
Step 3: Work back from PA
The missing cluster must give P and A after −2 and −4. So its first letter is P (16) + 2 = R (18), and its second letter is A (1) + 4 = E (5).
Step 4: Answer and check
The missing cluster is RE. Check: R − 2 = P and E − 4 = A ✓. RF gives P and B, PE gives N and A, PC gives N and Y — all fail.""", trick=r"Find the shift from a complete pair, then reverse it on the given cluster.")
S[2] = dict(raw=r"""Step 1: Read the first set (AR, CW, EB)
First letters A → C → E move +2 each time. Second letters R → W → B move +5 each time (W + 5 wraps round to B).
Step 2: Confirm with (GU, IZ, KE)
G → I → K is +2, +2 and U → Z → E is +5, +5 ✓
Step 3: Test the options
(GR, IW, KB): G → I → K is +2, +2 and R → W → B is +5, +5 ✓
(QR, RW, XY) starts Q → R (+1); (GN, FN, NU) starts G → F (−1); (YN, YN, FU) repeats YN — all break the rule.
Step 4: Answer
The set (GR, IW, KB) follows the same +2, +5 rule.""", trick=r"Check the first letters and the second letters separately — here +2 and +5.")
S[3] = dict(raw=r"""Step 1: Know the year
2017 is an ordinary year (not divisible by 4), so we need a later ordinary year that starts on the same day.
Step 2: Count odd days year by year
An ordinary year gives 1 odd day and a leap year 2. 2017, 2018 and 2019 give 1 each, 2020 (leap) gives 2, and 2021 and 2022 give 1 each.
Step 3: Check the total
1 + 1 + 1 + 2 + 1 + 1 = 7 odd days = exactly 1 week. So 1 January 2023 falls on the same day as 1 January 2017, and 2023 is also an ordinary year ✓
Step 4: Answer
The calendar of 2017 is repeated in 2023 (both years begin on a Sunday). 2029 begins on a Monday, 2039 on a Saturday and 2041 on a Tuesday, so none of them matches.""", trick=r"Ordinary year after a leap year (2017 = 2016 + 1) repeats after 6 years: 2017 → 2023.")
S[4] = dict(raw=r"""Step 1: Set up the row
All face north, so their left is our left. There are 5 seats, numbered 1 to 5 from left to right.
Step 2: Place B, A and C
B is immediately left of A, and A is second to the left of C: B, A, _, C. This block needs 4 seats, so it starts at seat 1 or seat 2.
Step 3: Place D and E
D is second to the left of E, so D and E need two seats with one seat between them. If B starts at seat 2, the free seats are 1 and 4 (not two apart) ✗. So B = 1, A = 2, C = 4, and D = 3, E = 5.
Order: B, A, D, C, E.
Step 4: Answer
Between A (seat 2) and E (seat 5) sit D and C — 2 boys.""", trick=r"Fix the longest chain first (B A _ C), then fit the pair that needs a gap.")
S[5] = dict(raw=r"""Step 1: Place A and D
D is fifth to the right of A, and D is not at an end. In a row of 7, A = 1 and D = 6 is the only choice (A = 2 would put D at seat 7, an end).
Step 2: Place F and B
F is exactly in the middle, so F = 4. Two girls sit between F and B, so B is at seat 1 or seat 7; seat 1 is taken by A, so B = 7.
Step 3: Place G, E and C
Free seats: 2, 3, 5. G is third to the left of E, so G = 2 and E = 5. C takes seat 3.
Order (left to right): A, G, C, F, E, D, B.
Step 4: Answer
From the right end: B (1st), D (2nd), E (3rd). So E sits third from the right end.""", trick=r"Start with the clue that fixes two seats at once (A and D), then the middle seat.")
S[6] = dict(raw=r"""Step 1: Count the letters of EXTINCTION
E 1, X 1, T 2, I 2, N 2, C 1, O 1. There is no S in the word.
Step 2: Check NICE and EXIT
NICE needs N, I, C, E ✓. EXIT needs E, X, I, T ✓.
Step 3: Check TENT
TENT needs T twice, E once and N once — the word has two Ts ✓.
Step 4: Check TEXTS
TEXTS needs an S, which EXTINCTION does not have ✗. So TEXTS cannot be formed.""", trick=r"First look for a letter that is missing from the given word — here S.")
S[7] = dict(raw=r"""Step 1: Find the differences
\( 236 - 218 = 18,\; 272 - 236 = 36,\; 326 - 272 = 54 \)
Step 2: Spot the pattern
The differences are 18, 36, 54 — multiples of 18 (18 × 1, 18 × 2, 18 × 3).
Step 3: Next difference
\( 18 \times 4 = 72 \)
Step 4: Missing number
\( 326 + 72 = 398 \)""", trick=r"Differences in a table of 18 → next difference 72.")
S[8] = dict(raw=r"""Step 1: Find the differences
\( 168 - 147 = 21,\; 189 - 168 = 21,\; 210 - 189 = 21 \)
Step 2: Spot the pattern
The difference is constant: +21 each time (all terms are multiples of 21: 7 × 21, 8 × 21, 9 × 21, 10 × 21).
Step 3: Next term
\( 210 + 21 = 231 \)
Step 4: Check
\( 231 = 11 \times 21 \) ✓ — the multiples continue in order.""", trick=r"147 = 7 × 21 → the series is 21 × 7, 8, 9, 10, 11.")
S[9] = dict(raw=r"""Step 1: Test multiplication
\( 6 \times 4 = 24 \), and 24 − 1 = 23. \( 23 \times 5 = 115 \), and 115 − 4 = 111.
Step 2: See the rule
The multiplier goes 4, 5, 6, 7 … and the number subtracted goes 1, 4, 9, 16 … (squares).
Step 3: Confirm
\( 111 \times 6 - 9 = 666 - 9 = 657 \) ✓ and \( 657 \times 7 - 16 = 4599 - 16 = 4583 \) ✓
Step 4: Next term
\( 4583 \times 8 - 25 = 36664 - 25 = 36639 \), written 36,639.""", trick=r"Rule: × 4, × 5, × 6 … then − 1², − 2², − 3² ….")
S[10] = dict(raw=r"""Step 1: Compare the first two figures
First figure: R top-left, 3 top-right, ▲ bottom-right, 8 bottom-left. Second figure: 8 top-left, R top-right, 3 bottom-right, ▲ bottom-left.
Step 2: Find the rule
Every element moves one corner clockwise: top-left → top-right → bottom-right → bottom-left → top-left. The elements themselves do not turn or change.
Step 3: Apply it to the third figure
B (top-left) → top-right; Y (top-right) → bottom-right; Z (bottom-right) → bottom-left; □ (bottom-left) → top-left.
Step 4: Answer
The missing figure has □ and B on top, and Z and Y at the bottom — the first answer figure. The others put B, Y or Z in wrong corners.""", trick=r"Track one element (R) — it moved one corner clockwise; move everything the same way.")
S[11] = dict(raw=r"""Step 1: Compare the first two figures
D top-left → bottom-left, E top-right → top-left, J bottom-right → top-right, G bottom-left → bottom-right. The hollow pentagon in the centre becomes shaded.
Step 2: Find the rule
Every corner element moves one corner anticlockwise, and the central shape changes from unshaded to shaded.
Step 3: Apply it to the third figure
The circle-line (top-left) → bottom-left; the arrow → (top-right) → top-left; the diamond (bottom-right) → top-right; the triangle (bottom-left) → bottom-right; the hollow hexagon becomes a shaded hexagon.
Step 4: Answer
The missing figure has the arrow → and the diamond on top, the circle-line and the triangle at the bottom, and a shaded hexagon — the third answer figure. The others have the arrow pointing left or the triangle and circle-line swapped.""", trick=r"Two changes: corners move one step anticlockwise, centre gets shaded.")
S[12] = dict(raw=r"""Step 1: Study JT310 → WM218 (first to second)
The letters swap and each moves +3: T (20) + 3 = W (23) and J (10) + 3 = M (13). The number: \( 310 - 92 = 218 \).
Step 2: Confirm with AT520 → WD428
T + 3 = W and A + 3 = D (letters swapped) ✓, and \( 520 - 92 = 428 \) ✓
Step 3: Apply to LD620
Swap to D, L, then +3: D (4) + 3 = G (7) and L (12) + 3 = O (15). Number: \( 620 - 92 = 528 \).
Step 4: Answer
The cluster is GO528.""", trick=r"Letters: reverse order and +3; number: − 92.")
S[13] = dict(raw=r"""Step 1: Study SP120 → PY180
First letter S (19) − 3 = P (16); second letter P (16) + 9 = Y (25); number \( 120 \times 1.5 = 180 \).
Step 2: Confirm with EB200 → BK300
E (5) − 3 = B (2); B (2) + 9 = K (11); \( 200 \times 1.5 = 300 \) ✓
Step 3: Work back from KP135
First letter: K (11) + 3 = N (14). Second letter: P (16) − 9 = G (7). Number: \( 135 \div 1.5 = 90 \).
Step 4: Answer
The missing cluster is NG90. Check: N − 3 = K, G + 9 = P, 90 × 1.5 = 135 ✓""", trick=r"Find the rule forward, then reverse every operation for the unknown first term.")
S[14] = dict(raw=r"""Step 1: First pair
\( 2501 - 2458 = 43 \)
Step 2: Second pair
\( 7370 - 7327 = 43 \) ✓ — the rule is "add 43".
Step 3: Apply to 7635
\( 7635 + 43 = 7678 \)
Step 4: Answer
The missing number is 7678.""", trick=r"Same difference in both pairs → just add it.")
S[15] = dict(raw=r"""Step 1: Try a multiplier
\( 13 \times 3 = 39 \), and \( 39 - 5 = 34 \).
Step 2: Confirm with the second pair
\( 587 \times 3 = 1761 \), and \( 1761 - 5 = 1756 \) ✓ — the rule is "× 3, then − 5".
Step 3: Apply to 575
\( 575 \times 3 = 1725 \), and \( 1725 - 5 = 1720 \).
Step 4: Answer
The missing number is 1720.""", trick=r"Second number ≈ 3 × first → check what is left over (here − 5).")
S[16] = dict(raw=r"""Step 1: LOIN → MTHI
L + 1 = M, O + 5 = T, I − 1 = H, N − 5 = I. The pattern is +1, +5, −1, −5.
Step 2: Confirm with NUTS → OZSN
N + 1 = O, U + 5 = Z, T − 1 = S, S − 5 = N ✓
Step 3: Apply to DEAF
D + 1 = E, E + 5 = J, A − 1 = Z (wraps round), F − 5 = A.
Step 4: Answer
DEAF is coded as EJZA.""", trick=r"Write the shift under each letter: +1, +5, −1, −5.")
S[17] = dict(raw=r"""Step 1: Find the code for "flowers"
"flowers" is in sentence 1 (em ta pl rs) and sentence 2 (ta rq zm). The common code is "ta".
Step 2: Find the code for "smell"
"smell" is in sentence 2 (ta rq zm) and sentence 3 (tr rq zi fa). The common code is "rq".
Step 3: Combine
"flowers smell" = ta + rq.
Step 4: Answer
The code is "ta rq". The other options use "zl", "em" or "fa", which belong to other words.""", trick=r"Common word in two sentences ↔ common code in the same two codes.")
S[18] = dict(raw=r"""Step 1: First letters
P → R → ? → V → X: each is +2, so the missing first letter is T.
Step 2: Second and third letters
Second: J → M → ? → S → V is +3, so P. Third: Q → U → ? → C → G is +4 (Y + 4 wraps to C), so Y.
Step 3: Numbers
408 → 639 → ? → 1101 → 1332 increases by 231 each time: \( 639 + 231 = 870 \). Check: \( 870 + 231 = 1101 \) ✓
Step 4: Answer
The missing term is TPY870.""", trick=r"Split the term into three letters and a number; each part has its own steady jump.")
S[19] = dict(raw=r"""Step 1: Starting angle at 2:00
The hour hand is at 60° and the minute hand at 0°, so the minute hand is 60° behind.
Step 2: Relative speed
The minute hand gains \( 6 - 0.5 = 5.5 \) degrees per minute on the hour hand.
Step 3: Angle of 90°
First the minute hand catches up the 60°, then must move 90° ahead: it must gain \( 60 + 90 = 150 \) degrees.
\( t = \dfrac{150}{5.5} = \dfrac{300}{11} \approx 27.27 \) minutes
Step 4: Answer
About 27 minutes after 2:00 PM (at about 2:27).""", trick=r"Gain needed ÷ 5.5 = minutes.")
S[20] = dict(raw=r"""Step 1: Total change
From 3 minutes slow to 7 minutes fast, the clock gains \( 3 + 7 = 10 \) minutes.
Step 2: Time taken
From 9:00 AM to 3:00 PM is 6 hours = 360 minutes. So it gains 10 minutes in 360 minutes.
Step 3: When is it correct?
It shows the correct time when it has gained the first 3 minutes:
\( \dfrac{3}{10} \times 360 = 108 \) minutes after 9:00 AM.
Step 4: Answer
108 minutes = 1 hour 48 minutes, so the time is 10:48 AM.""", trick=r"Correct time = start + (slow minutes ÷ total gain) × time gap.")
