S = {}
S[1] = dict(raw=r"""Step 1: Find the differences
−405 → −415 → −425 → −435 → −445: each term is 10 less than the one before it.
Step 2: Spot the rule
The series is an arithmetic progression with a common difference of −10.
Step 3: Test the remaining terms
After −445 the next term should be \( -445 - 10 = -455 \), but the series shows −453.
Step 4: Confirm
\( -455 - 10 = -465 \) ✓ and \( -465 - 10 = -475 \) ✓, so only −453 breaks the rule (it should be −455).""", trick=r"Constant −10 series: every term must end in 5; −453 ends in 3.")
S[2] = dict(raw=r"""Step 1: Write the first letters
O (15), P (16), R (18), ?, Y (25), D (4), J (10), Q (17). The gaps are +1, +2, then +3, +4, +5 … (Y + 5 = 30 → 30 − 26 = 4 = D).
Step 2: Find the missing first letter
R (18) + 3 = 21 = U, and U (21) + 4 = 25 = Y ✓.
Step 3: Write the second letters
S (19), M (13), G (7), ?, U (21), O (15), I (9), C (3): each step is −6, so G (7) − 6 = 1 = A (and A − 6 wraps to U ✓).
Step 4: Answer
The missing term is UA.""", trick=r"First letters +1, +2, +3 …; second letters −6 every time.")
S[3] = dict(raw=r"""Step 1: Write the first letters
K, M, O, Q, S, ?, W, Y — each is 2 places after the one before it (+2).
Step 2: Find the missing first letter
S (19) + 2 = 21 = U.
Step 3: Write the second letters
B, Z, X, V, T, ?, P, N — each is 2 places before the one before it (−2; B − 2 wraps to Z). T (20) − 2 = 18 = R.
Step 4: Answer and check
The missing term is UR; then U + 2 = W and R − 2 = P give WP ✓.""", trick=r"First letter +2, second letter −2 in every step.")
S[4] = dict(raw=r"""Step 1: Study the first set (BW, ZR, XM)
First letters B (2) → Z (26) → X (24): −2 each time (2 − 2 = 0 → 26). Second letters W (23) → R (18) → M (13): −5 each time.
Step 2: Confirm with (OE, MZ, KU)
O (15) → M (13) → K (11): −2, −2. E (5) → Z (0 → 26) → U (21): −5, −5 ✓.
Step 3: Test the options
(CN, AI, YD): C (3) → A (1) → Y (25) is −2, −2; N (14) → I (9) → D (4) is −5, −5 ✓. (ZY, WW, VS): Z → W is −3 ✗. (IF, JD, AA): I → J is +1 ✗. (VT, SR, RP): V → S is −3 ✗.
Step 4: Answer
Only (CN, AI, YD) follows −2 on the first letters and −5 on the second letters.""", trick=r"First letters −2, second letters −5 inside each set.")
S[5] = dict(raw=r"""Step 1: Look at the known gaps
−446 → −459 is −13, −459 → −473 is −14, −473 → −488 is −15, −488 → −504 is −16.
Step 2: Spot the rule
The gap grows by 1 each time: −10, −11, −12, −13 …
Step 3: Find the missing term
−413 → −423 is −10, so the next gap is −11: \( -423 - 11 = -434 \).
Step 4: Check
\( -434 - 12 = -446 \) ✓, which is the next given term.""", trick=r"Gaps −10, −11, −12, −13 … — each one bigger by 1.")
S[6] = dict(raw=r"""Step 1: Look at the known gaps
343 → 321 is −22, 321 → 298 is −23, 298 → 274 is −24, 274 → 249 is −25, 249 → 223 is −26.
Step 2: Spot the rule
The gap grows by 1 each time, so going backwards the gaps are −21 and −20.
Step 3: Find the missing term
\( 384 - 20 = 364 \).
Step 4: Check
\( 364 - 21 = 343 \) ✓, which is the third term.""", trick=r"Gaps −20, −21, −22 … — work backwards from the known part.")
S[7] = dict(raw=r"""Step 1: Write the given conditions
C has fewer wickets than E and B, but more than A. D has the fewest wickets of all.
Step 2: Arrange from lowest to highest
D < A < C < (B and E, in some order).
Step 3: Look below A
Only D is below A.
Step 4: Answer
The number of bowlers with fewer wickets than A is 1.""", trick=r"Build the order from the 'least' clue first: D, then A, then C.")
S[8] = dict(raw=r"""Step 1: Place the lowest boys
C has the least marks. A is more than only D and C, so from the bottom the order is C, D, A.
Step 2: Place the remaining boys
B, E and F are all above A. B is more than F but less than E, so F < B < E.
Step 3: Write the full order (lowest to highest)
C < D < A < F < B < E.
Step 4: Answer
E has the highest marks.""", trick=r"'More than only D and C' fixes A in third place from the bottom.")
S[9] = dict(raw=r"""Step 1: Compare the first two figures
The line running from the top-left towards the bottom-right turns through 90° and runs from the bottom-left to the top-right.
Step 2: Look at the end markers
The first figure has a dot at only one end; in the second figure a dot appears at both ends of the line.
Step 3: Look at the small triangle
The triangle moves from the top of the box to the opposite side (the bottom).
Step 4: Apply the same rule to the third figure
The horizontal line with a square at one end becomes a vertical line with squares at both ends, and the triangle moves from the top-right to the bottom-left. Only the figure with a vertical two-square line and the triangle at the bottom-left fits.""", trick=r"Line turns 90°, its end marker doubles, triangle jumps to the opposite corner.")
S[10] = dict(raw=r"""Step 1: Track the corner symbols in the first pair
+ moves from top-left to top-right, − from top-right to bottom-right, ÷ from bottom-right to bottom-left and Λ from bottom-left to top-left.
Step 2: State the rule
Every corner symbol moves one corner clockwise, and the central shape gets a frame around it (the small triangle is placed inside a square).
Step 3: Apply it to the third figure
× (top-left) → top-right, @ (top-right) → bottom-right, # (bottom-right) → bottom-left, © (bottom-left) → top-left; the house shape gets a frame.
Step 4: Answer
The answer figure shows © top-left, × top-right, # bottom-left and @ bottom-right, with the framed house in the centre.""", trick=r"Corner symbols move one step clockwise; the centre shape gets a frame.")
S[11] = dict(raw=r"""Step 1: Study the letters of AJ150 → YH243
A (1) → Y (25) is −2 (1 − 2 = −1 → 25) and J (10) → H (8) is −2.
Step 2: Study the numbers
\( 150 + 93 = 243 \); check with KG300 → IE393: K → I is −2, G → E is −2 and \( 300 + 93 = 393 \) ✓.
Step 3: Apply the rule to SL310
S (19) − 2 = 17 = Q, L (12) − 2 = 10 = J, and \( 310 + 93 = 403 \).
Step 4: Answer
The required cluster is QJ403.""", trick=r"Both letters −2, number +93.")
S[12] = dict(raw=r"""Step 1: Study ZYX160 → VUS320
Z (26) → V (22) is −4, Y (25) → U (21) is −4, X (24) → S (19) is −5, and \( 160 \times 2 = 320 \).
Step 2: Confirm with JLR180 → FHM360
J → F is −4, L → H is −4, R → M is −5 and \( 180 \times 2 = 360 \) ✓.
Step 3: Work backwards from ATK240
Reverse the rule: A (1) + 4 = 5 = E, T (20) + 4 = 24 = X, K (11) + 5 = 16 = P, and \( 240 \div 2 = 120 \).
Step 4: Answer
The missing cluster is EXP120.""", trick=r"Forward rule −4, −4, −5 and ×2; for a blank on the left, reverse it (+4, +4, +5, ÷2).")
S[13] = dict(raw=r"""Step 1: Study the first pair
\( 6276 - 6235 = 41 \).
Step 2: Confirm with the second pair
\( 3592 - 3551 = 41 \) ✓. So the second number of each pair is 41 less than the first.
Step 3: Work backwards for the third pair
The missing number minus 41 must give 7054, so the number is \( 7054 + 41 = 7095 \).
Step 4: Check
\( 7095 - 41 = 7054 \) ✓.""", trick=r"Second number = first number − 41.")
S[14] = dict(raw=r"""Step 1: Study the first pair
Half of 324 is 162, and \( 162 - 3 = 159 \).
Step 2: Confirm with the second pair
Half of 1710 is 855, and \( 855 - 3 = 852 \) ✓.
Step 3: Apply the rule to 680
Half of 680 is 340, and \( 340 - 3 = 337 \).
Step 4: Answer
The missing number is 337.""", trick=r"Second number = first number ÷ 2 − 3.")
S[15] = dict(raw=r"""Step 1: Compare PALL with LWHH
P (16) → L (12) is −4, A (1) → W (23) is −4 (1 − 4 = −3 → 23), L (12) → H (8) is −4.
Step 2: Confirm with GREY → CNAU
G → C, R → N, E → A and Y → U are all −4 ✓.
Step 3: Apply −4 to PULP
P (16) → L (12), U (21) → Q (17), L (12) → H (8), P (16) → L (12).
Step 4: Answer
PULP is coded as LQHL.""", trick=r"Every letter moves 4 places back.")
S[16] = dict(raw=r"""Step 1: Test the plain letter positions
G + R + E + A + T = 7 + 18 + 5 + 1 + 20 = 51, not 84, so the code uses something else.
Step 2: Use the reverse positions (A = 26, B = 25 … Z = 1)
G = 20, R = 9, E = 22, A = 26, T = 7: \( 20 + 9 + 22 + 26 + 7 = 84 \) ✓.
Step 3: Confirm with TEST
T = 7, E = 22, S = 8, T = 7: \( 7 + 22 + 8 + 7 = 44 \) ✓.
Step 4: Code PEAR
P = 11, E = 22, A = 26, R = 9: \( 11 + 22 + 26 + 9 = 68 \).""", trick=r"Reverse position = 27 − position; add them up.")
S[17] = dict(raw=r"""Step 1: First letters
M (13), K (11), I (9), G (7): −2 each time, so the next is E (5).
Step 2: Second letters
Z (26), W (23), T (20), Q (17): −3 each time, so the next is N (14).
Step 3: Numbers
504, 630, 756, 882: +126 each time, so the next is \( 882 + 126 = 1008 \).
Step 4: Answer
The missing term is EN1008.""", trick=r"Three separate patterns: −2, −3 and +126.")
S[18] = dict(raw=r"""Step 1: First and second letters
First letters Q, P, O, N, M, L go −1 each time ✓. Second letters R, N, J, F, B, X go −4 each time (B − 4 wraps to X) ✓.
Step 2: Third letters
From OJE onwards: E (5) → X (24) → Q (17) → J (10) is −7 each time (5 − 7 = −2 → 24). Going back, S (19) − 7 = 12 = L, and L − 7 = E ✓. So the second term should have L, not M.
Step 3: Numbers
1394 → 1341 → 1288 → 1235 is −53 each time. Going back, \( 1394 + 53 = 1447 \) and \( 1447 + 53 = 1500 \) ✓. So the second term should have 1447, not 1445.
Step 4: Answer
The correct second term is PNL1447, so PNM1445 is the wrong term.""", trick=r"Check each part separately; both the letter and the number fail at the same term.")
S[19] = dict(raw=r"""Step 1: Use the formula
Angle \( = \left| 30H - \dfrac{11}{2}M \right| \), where H is the hour and M the minutes.
Step 2: Substitute H = 3, M = 20
\( 30 \times 3 = 90 \) and \( \dfrac{11}{2} \times 20 = 110 \).
Step 3: Find the angle
\( |90 - 110| = 20^{\circ} \).
Step 4: Check directly
The minute hand is at \( 20 \times 6 = 120^{\circ} \); the hour hand is at \( 90 + 20 \times 0.5 = 100^{\circ} \). The difference is \( 20^{\circ} \) ✓.""", trick=r"At 3:20 the hour hand has moved 10° past 3, the minute hand is exactly on 4.")
S[20] = dict(raw=r"""Step 1: Find the time passed
From 7 AM to 7 PM is 12 hours \( = 12 \times 60 = 720 \) minutes.
Step 2: Count the 15-minute blocks
\( 720 \div 15 = 48 \) blocks.
Step 3: Find the total gain
\( 48 \times 5 = 240 \) seconds \( = 4 \) minutes.
Step 4: Find the time shown
The clock is 4 minutes fast, so at 7 PM it shows 7:04:00 PM.""", trick=r"Gain per hour = \( 5 \times 4 = 20 \) s; in 12 hours \( 20 \times 12 = 240 \) s = 4 min.")
