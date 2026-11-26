S = {}
S[1] = dict(raw=r"""Step 1: Compare neighbouring terms
1920 → 960 is ÷2, 960 → 240 is ÷4, 240 → 120 is ÷2, 120 → 30 is ÷4, 30 → 15 is ÷2.
Step 2: Spot the rule
The divisors alternate: ÷2, ÷4, ÷2, ÷4, ÷2 …
Step 3: Find the missing term
The next step is ÷4: \( 15 \div 4 = 3.75 \).
Step 4: Check with the last term
\( 3.75 \div 2 = 1.875 \) ✓, which is the last term of the series.""", trick=r"Alternate ÷2, ÷4 — check the last given term to confirm.")
S[2] = dict(raw=r"""Step 1: Write the letter positions
N = 14, P = 16, R = 18, T = 20, V = 22.
Step 2: Spot the rule
Each letter is 2 places after the one before it (skip one letter each time).
Step 3: Find the missing term
\( 22 + 2 = 24 \) = X.
Step 4: Check the rest
X (24) + 2 = 26 = Z ✓, and Z + 2 wraps round to B (2) ✓. The missing term is X.""", trick=r"Skip one letter each time; after Z the series wraps to A, B.")
S[3] = dict(raw=r"""Step 1: Study the first pair (AI → GO)
A (1) → G (7) is +6 and I (9) → O (15) is +6.
Step 2: Confirm with the second pair (RG → XM)
R (18) → X (24) is +6 and G (7) → M (13) is +6 ✓.
Step 3: Apply +6 to FP
F (6) + 6 = 12 = L and P (16) + 6 = 22 = V.
Step 4: Answer
The missing cluster is LV.""", trick=r"Both letters move forward by 6 in every pair.")
S[4] = dict(raw=r"""Step 1: Write the first letters
A (1), X (24), U (21), R (18), ?, L (12), I (9), F (6): each step is −3 (1 − 3 = −2 → 24). So R (18) − 3 = 15 = O.
Step 2: Write the second letters
I (9), F (6), B (2), W (23), ?, J (10), B (2), S (19).
Step 3: Find the gaps
I → F is −3, F → B is −4, B → W is −5 (2 − 5 = −3 → 23), so the next gap is −6: W (23) − 6 = 17 = Q.
Step 4: Check and answer
Q (17) − 7 = 10 = J ✓, J (10) − 8 = 2 = B ✓, B (2) − 9 = −7 → 19 = S ✓. The missing term is OQ.""", trick=r"First letters −3 always; second letters −3, −4, −5, −6 … (wrap past A).")
S[5] = dict(raw=r"""Step 1: Study the first pair (HO → CH)
H (8) → C (3) is −5 and O (15) → H (8) is −7.
Step 2: Confirm with the second pair (MZ → HS)
M (13) → H (8) is −5 and Z (26) → S (19) is −7 ✓.
Step 3: Apply −5 and −7 to GS
G (7) − 5 = 2 = B and S (19) − 7 = 12 = L.
Step 4: Answer
The missing cluster is BL.""", trick=r"First letter −5, second letter −7 in every pair.")
S[6] = dict(raw=r"""Step 1: Study the first set (TN, OI, IC)
First letters T (20) → O (15) → I (9): −5, then −6. Second letters N (14) → I (9) → C (3): −5, then −6.
Step 2: Confirm with (GW, BR, VL)
G (7) → B (2) → V (2 − 6 = −4 → 22): −5, −6. W (23) → R (18) → L (12): −5, −6 ✓.
Step 3: Test the options
(UX, PS, JM): U (21) → P (16) → J (10) is −5, −6; X (24) → S (19) → M (13) is −5, −6 ✓. (KM, FG, ZA): M → G is −6 at the first step ✗. (WB, RV, LP): B (2) → V (22) is −6 at the first step ✗. (JX, ER, CL): E → C is only −2 ✗.
Step 4: Answer
Only (UX, PS, JM) follows −5 and then −6 on both letters.""", trick=r"Both letters: −5 then −6 inside each set.")
S[7] = dict(raw=r"""Step 1: Note the leap year
2020 is divisible by 4 (and is not a century year), so it is a leap year: February has 29 days.
Step 2: Count the days in January
From 10 January to 31 January, both inclusive: \( 31 - 10 + 1 = 22 \) days.
Step 3: Add the full months February to August
\( 29 + 31 + 30 + 31 + 30 + 31 + 31 = 213 \) days.
Step 4: Add September and total
1 to 25 September = 25 days. Total \( = 22 + 213 + 25 = 260 \) days.""", trick=r"'Both inclusive' — count the first day too: 31 − 10 + 1.")
S[8] = dict(raw=r"""Step 1: Know the rule
Two years have the same calendar when both are of the same type (leap or ordinary) and the odd days between them add up to a multiple of 7. An ordinary year gives 1 odd day, a leap year 2.
Step 2: Test 2011 and 2022
Years 2011 to 2021 = 11 years, of which 2012, 2016 and 2020 are leap years. Odd days \( = 11 + 3 = 14 \), a multiple of 7, and both 2011 and 2022 are ordinary years ✓.
Step 3: Test the other pairs
2017 → 2027: 10 years + 2 leap years (2020, 2024) = 12 odd days ✗. 2003 → 2007: 4 years + 1 leap year (2004) = 5 odd days ✗. 2014 and 2020: 2020 is a leap year and 2014 is not ✗.
Step 4: Answer
2011 and 2022 have identical calendars (both begin on a Saturday).""", trick=r"An ordinary year usually repeats after 6 or 11 years — add up the odd days to be sure.")
S[9] = dict(raw=r"""Step 1: Place A
A is at one end. D is to the right of A, so A cannot be at the right end — A sits at the left end (seat 1).
Step 2: Place E and C
E is third to the left of C, so (E, C) can be (seat 1, seat 4) or (seat 2, seat 5). Seat 1 is taken by A, so E is in seat 2 and C in seat 5.
Step 3: Place D and B
D is to the right of A and to the left of B, so D takes seat 3 and B seat 4.
Step 4: Count
Order (left to right): A, E, D, B, C. To the right of E sit D, B and C — 3 persons.""", trick=r"Fix the end person first; 'third to the left' means two seats in between.")
S[10] = dict(raw=r"""Step 1: Fix P and S
Facing the centre, moving to one's right means moving anticlockwise. Put P at a seat; S is second to the right of P.
Step 2: Place C
S is fifth to the right of C, which on a 7-seat table is the same as second to the left of C. So C is second to the right of S: going round to the right from P, S is 2nd and C is 4th — that is, C is third to the left of P.
Step 3: Place Q, A, B and R
Q is not next to P or S, so Q takes the only seat left that touches neither of them (between C and P's left side). Of the three remaining seats, B is fourth to the right of A only when A is P's immediate left neighbour; then B is S's immediate neighbour and R takes the last seat, next to P on the right.
Step 4: Answer
Going round to the left of P: A (1st), Q (2nd), C (3rd). So C sits third to the left of P.""", trick=r"On a 7-seat table, 5th to the right = 2nd to the left.")
S[11] = dict(raw=r"""Step 1: Look at the first pair
In the first figure a hexagon is outside and a dome (semicircle-like shape) is inside. In the second figure the dome is outside and the hexagon is inside.
Step 2: Find the rule
The outer shape and the inner shape swap places; the square frame around each figure does not change.
Step 3: Apply the rule to the third figure
The third figure has a square outside and a circle inside. After the swap, the circle must be outside and the square inside.
Step 4: Check the options
Every option keeps the frame and a large circle; only the figure with a square inside the circle completes the swap. The other options put a pentagon, a circle or a triangle inside.""", trick=r"Outer ↔ inner: square-in-circle answers circle-in-square.")
S[12] = dict(raw=r"""Step 1: Track the four corner shapes in the first pair
Triangle: top-left → top-right. Square: top-right → bottom-right. Circle: bottom-right → bottom-left. Rectangle: bottom-left → top-left.
Step 2: Find the rule
Every corner shape moves one corner clockwise. The letter in the middle is the same in all four options, so it does not decide the answer.
Step 3: Apply the rule to the third figure
Pentagon (top-left) → top-right; square (top-right) → bottom-right; hexagon (bottom-right) → bottom-left; triangle (bottom-left) → top-left.
Step 4: Check the options
The answer must show triangle top-left, pentagon top-right, hexagon bottom-left and square bottom-right — only one option has exactly this.""", trick=r"Follow one shape (the triangle): it goes one corner clockwise.")
S[13] = dict(raw=r"""Step 1: Study AZ205 → CB112
A (1) + 2 = C, Z (26) + 2 = 28 → B (2), and \( 205 - 93 = 112 \).
Step 2: Confirm with CB200 → ED107
C + 2 = E, B + 2 = D, and \( 200 - 93 = 107 \) ✓.
Step 3: Apply the rule to XM999
X (24) + 2 = 26 = Z, M (13) + 2 = 15 = O, \( 999 - 93 = 906 \).
Step 4: Answer
The missing cluster is ZO906.""", trick=r"Letters +2 each, number −93.")
S[14] = dict(raw=r"""Step 1: Study DI30 → HC75 (first to second)
D (4) + 4 = H (8), I (9) − 6 = C (3), \( 30 \times 2.5 = 75 \).
Step 2: Confirm with KR40 → OL100
K (11) + 4 = O (15), R (18) − 6 = L (12), \( 40 \times 2.5 = 100 \) ✓.
Step 3: Work backwards from HL150
The missing cluster is the FIRST of its pair, so reverse each step: H (8) − 4 = D (4), L (12) + 6 = R (18), \( 150 \div 2.5 = 60 \).
Step 4: Answer
The missing cluster is DR60.""", trick=r"When the '?' is the first term, undo the rule: −4, +6, ÷2.5.")
S[15] = dict(raw=r"""Step 1: Study 11 → 729
\( 729 = 9^{3} \) and \( 9 = 11 - 2 \).
Step 2: Confirm with 15 → 2197
\( 2197 = 13^{3} \) and \( 13 = 15 - 2 \) ✓.
Step 3: Apply the rule to 23
\( 23 - 2 = 21 \), and \( 21^{3} = 9261 \).
Step 4: Answer
The missing number is 9261.""", trick=r"Know cubes up to 25: 9³ = 729, 13³ = 2197, 21³ = 9261.")
S[16] = dict(raw=r"""Step 1: Study LORD → OPSE
L (12) → O (15): O is the opposite letter of L (12 + 15 = 27). O → P, R → S, D → E: each +1.
Step 2: Confirm with WAST → DBTU
W (23) → D (4): opposite letter (23 + 4 = 27). A → B, S → T, T → U: each +1 ✓.
Step 3: Apply the rule to NORM
N (14) → opposite letter M (13); O → P, R → S, M → N.
Step 4: Answer
NORM is coded as MPSN.""", trick=r"First letter → its opposite (pairs add to 27); the other letters +1.")
S[17] = dict(raw=r"""Step 1: Find how much time the watch must make up
It is 12 minutes slow, so it must gain 12 minutes \( = 12 \times 60 = 720 \) seconds.
Step 2: Find the time needed
It gains 48 seconds every hour, so it needs \( 720 \div 48 = 15 \) hours.
Step 3: Add to the starting time
4 AM + 15 hours = 7 PM.
Step 4: Answer
The watch will show the correct time at 7:00 PM.""", trick=r"Time needed = total lag ÷ gain per hour.")
S[18] = dict(raw=r"""Step 1: Count the curls in each figure
The diamond has 1 curl in the first figure, 2 in the second, 3 in the third and 4 in the fourth.
Step 2: Find the rule
One curl is added at each step, and the curls already drawn stay at their corners.
Step 3: Predict the next figure
The fifth figure must have 5 curls: the four curls of the fourth figure in the same positions and directions, plus a new one at the top corner.
Step 4: Check the options
All four options have 5 curls, so compare the old curls one by one with the fourth figure — only one option keeps every one of them facing the same way.""", trick=r"Count first (1, 2, 3, 4 → 5), then match the curl directions with the last figure.")
S[19] = dict(raw=r"""Step 1: Track where each new line appears
Figure 1: a line at the top-left corner. Figure 2: a line added at the bottom-left. Figure 3: a line added at the bottom-right. Figure 4: a line added at the top-right.
Step 2: Find the rule
One line is added in each step, moving anticlockwise: top-left → bottom-left → bottom-right → top-right.
Step 3: Predict the next figure
All four corners now have one line, so the cycle starts again at the top-left: the top-left corner gets a second (double) line and the other three corners keep a single line.
Step 4: Check the options
Only one option has a double line at the top-left and single lines at the other three corners; the others put the double line at a different corner or have two double lines.""", trick=r"Lines are added anticlockwise; after one round, the first corner gets doubled.")
S[20] = dict(raw=r"""Step 1: Write the ages using the ratio
Let the present ages be 2x and 5x.
Step 2: Use the sum
\( 2x + 5x = 21 \Rightarrow 7x = 21 \Rightarrow x = 3 \). The ages are 6 and 15 years.
Step 3: Find the ages after 7 years
\( 6 + 7 = 13 \) and \( 15 + 7 = 22 \).
Step 4: Answer
The new ratio is \( 13 : 22 \).""", trick=r"Ratio \( 2 : 5 \) with sum 21 → one part = 3.")
