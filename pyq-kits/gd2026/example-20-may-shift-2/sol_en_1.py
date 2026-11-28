S = {}
S[1] = dict(raw=r"""Step 1: Find the gap between neighbouring terms
357 → 352 is −5, 352 → 347 is −5, 347 → 339 is −8, 339 → 337 is −2, 337 → 332 is −5, 332 → 327 is −5, 327 → 322 is −5.
Step 2: Spot the rule
Almost every gap is −5, so the series should fall by 5 at each step: 357, 352, 347, 342, 337, 332, 327, 322.
Step 3: Compare with the given series
The fourth term should be 347 − 5 = 342, but the series shows 339. All the other terms already follow the rule.
Step 4: Check
With 342 in place, 342 − 5 = 337 ✓, so the series is consistent again. The wrong term is 339.""", trick=r"Same gap of 5 everywhere except one place → the term at the odd gap (339, should be 342) is wrong.")
S[2] = dict(raw=r"""Step 1: Find the gaps that are known
240 → 251 is +11, 251 → 263 is +12, 263 → 276 is +13 and 276 → 290 is +14.
Step 2: Spot the rule
The gaps grow by 1 each time. Going backwards the gaps must be +10 (before 240), +9 and +8: 213 → 221 is +8 ✓.
Step 3: Find the missing term
The gap after 221 is +9, so the missing term is 221 + 9 = 230.
Step 4: Check
230 + 10 = 240 ✓, so the gaps 8, 9, 10, 11, 12, 13, 14 run without a break.""", trick=r"Gaps 8, 9, 10, 11 … rise by 1 → 221 + 9 = 230.")
S[3] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: F, H, J, L, N, P, ?, T. Second letters: W, C, I, O, U, A, ?, M.
Step 2: Rule for the first letters
F (6) → H (8) → J (10) → L (12) → N (14) → P (16) is +2 each time, so the missing first letter is P + 2 = R (18), and R + 2 = T ✓.
Step 3: Rule for the second letters
W (23) → C (23 + 6 − 26 = 3) → I (9) → O (15) → U (21) → A (21 + 6 − 26 = 1) is +6 each time. So the missing second letter is A + 6 = G (7), and G + 6 = M (13) ✓.
Step 4: Answer
The missing term is RG. PG and QI have the wrong first letter, and RD has the wrong second letter.""", trick=r"First letters +2, second letters +6 → R and G.")
S[4] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: Y, B, E, ?, K, N, Q, T. Second letters: Y, D, I, ?, S, X, C, H.
Step 2: Rule for the first letters
Y (25) → B (25 + 3 − 26 = 2) → E (5) is +3 each time. So the missing first letter is E + 3 = H (8), and H + 3 = K (11) ✓.
Step 3: Rule for the second letters
Y (25) → D (25 + 5 − 26 = 4) → I (9) is +5 each time. So the missing second letter is I + 5 = N (14), and N + 5 = S (19) ✓.
Step 4: Answer
The missing term is HN. The tail of the series also agrees: K → N → Q → T is +3 and S → X → C → H is +5.""", trick=r"First letters +3, second letters +5 → H and N.")
S[5] = dict(raw=r"""Step 1: Study the first set (VD, SX, PR)
First letters: V (22) → S (19) → P (16), a fall of 3 each time. Second letters: D (4) → X (4 − 6 + 26 = 24) → R (18), a fall of 6 each time.
Step 2: Confirm with the second set (MW, JQ, GK)
M (13) → J (10) → G (7) is −3 again, and W (23) → Q (17) → K (11) is −6 again. So the rule is: first letter −3, second letter −6.
Step 3: Test the group that fits
(AU, XO, UI): A (1) → X (1 − 3 + 26 = 24) → U (21) is −3, −3; U (21) → O (15) → I (9) is −6, −6. Both rules hold.
Step 4: Reject the others
(MJ, LE, DA): M → L is only −1. (EP, YJ, VG): E → Y is −6, not −3. (UR, UM, LI): U → U is 0. So only (AU, XO, UI) follows the rule.""", trick=r"First letter −3, second letter −6 in every step → (AU, XO, UI).")
S[6] = dict(raw=r"""Step 1: Study the first set (UI, SC, QW)
First letters: U (21) → S (19) → Q (17), a fall of 2 each time. Second letters: I (9) → C (3) → W (3 − 6 + 26 = 23), a fall of 6 each time.
Step 2: Confirm with the second set (BL, ZF, XZ)
B (2) → Z (2 − 2 + 26 = 26) → X (24) is −2 again, and L (12) → F (6) → Z (6 − 6 + 26 = 26) is −6 again. So the rule is: first letter −2, second letter −6.
Step 3: Test the group that fits
(KE, IY, GS): K (11) → I (9) → G (7) is −2, −2; E (5) → Y (5 − 6 + 26 = 25) → S (19) is −6, −6. Both rules hold.
Step 4: Reject the others
(BQ, BO, VF) and (RO, RM, LJ) keep the first letter unchanged from the first to the second cluster. (ZK, AI, UA) has Z → A, which is +1. So only (KE, IY, GS) follows the rule.""", trick=r"First letter −2, second letter −6 in every step → (KE, IY, GS).")
S[7] = dict(raw=r"""Step 1: Find the gaps that are known
911 → 895 is −16, 895 → 877 is −18, 877 → 857 is −20, 857 → 835 is −22, 835 → 811 is −24.
Step 2: Spot the rule
The gaps grow by 2 each time: −16, −18, −20, −22, −24, so the next gap is −26.
Step 3: Find the missing term
811 − 26 = 785.
Step 4: Check
The following gap should be −28, and 785 − 28 = 757 ✓, which is the last term given.""", trick=r"Gaps −16, −18, −20 … grow by 2 → 811 − 26 = 785.")
S[8] = dict(raw=r"""Step 1: Place C and A first
Number the seats 1 to 5 from left to right. A is fourth to the right of C, which is possible only if C is in seat 1 and A in seat 5.
Step 2: Place B
B is second to the right of C, so B sits in seat 3.
Step 3: Place D and E
D is to the immediate left of B, so D sits in seat 2. The only seat left is seat 4, which belongs to E. The row is C, D, B, E, A.
Step 4: Count and check
Persons to the left of E are C, D and B, which is 3. All three conditions fit the row C, D, B, E, A.""", trick=r"Fourth to the right of C in a row of five → C is first, A is last; fill B, D, then E.")
S[9] = dict(raw=r"""Step 1: Use the first clues
C has the least marks. A has more than only D and C, so exactly two boys are below A, and they are C and D. So C < D < A.
Step 2: Bring in the other boys
All the others (B, E, F) are above A, because A beats only D and C.
Step 3: Order B, E and F
B is more than F but less than E, so F < B < E. The full order from lowest to highest is C < D < A < F < B < E.
Step 4: Count
E is the top scorer, so the marks of all the other five boys (C, D, A, F, B) are less than E.""", trick=r"Order low → high: C, D, A, F, B, E → five boys are below E.")
S[10] = dict(raw=r"""Step 1: Find the rule for the letters
KT → QH: reverse the letters (TK), then move each letter 3 back: T → Q and K → H. SU → RP: reverse (US), then U → R and S → P. So the rule is: reverse, then −3 on each letter.
Step 2: Find the rule for the numbers
222 → 336 and 302 → 416 are both a rise of \( 114 \).
Step 3: Apply to ZW432
Reverse ZW to WZ, then W (23) − 3 = T (20) and Z (26) − 3 = W (23), giving TW. The number is \( 432 + 114 = 546 \).
Step 4: Answer
The required cluster is TW546.""", trick=r"Reverse the letters and go 3 back on each; add 114 to the number.")
S[11] = dict(raw=r"""Step 1: Find the rule for the letters
ZKX → UHW: reverse the letters (XKZ), then move each letter 3 back: X → U, K → H, Z → W. LST → QPI: reverse (TSL), then T → Q, S → P, L → I. So the rule is: reverse, then −3 on each letter.
Step 2: Find the rule for the numbers
\( 102 \times 2 = 204 \) and \( 305 \times 2 = 610 \), so the number is doubled.
Step 3: Apply to XYR126
Reverse XYR to RYX, then R (18) − 3 = O (15), Y (25) − 3 = V (22), X (24) − 3 = U (21), giving OVU. The number is \( 126 \times 2 = 252 \).
Step 4: Answer
The required cluster is OVU252.""", trick=r"Reverse the letters, −3 on each, double the number → OVU252.")
S[12] = dict(raw=r"""Step 1: Find the relation in the first pair
\( 2838 - 2793 = 45 \), so the second number is 45 more than the first.
Step 2: Confirm with the last pair
\( 8225 - 8180 = 45 \) ✓, so the same rule holds.
Step 3: Apply to the third number
The missing number is \( 6270 + 45 = 6315 \).
Step 4: Check
\( 6315 - 6270 = 45 \) ✓, and no other option is 45 more than 6270.""", trick=r"Each second number is first + 45 → \( 6270 + 45 = 6315 \).")
S[13] = dict(raw=r"""Step 1: Test a simple rule on the first pair
\( 479 \times 2 = 958 \) and \( 958 + 2 = 960 \), so the rule looks like “double and add 2”.
Step 2: Confirm with the second pair
\( 25 \times 2 + 2 = 52 \) ✓, so the rule holds for both pairs.
Step 3: Work backwards for the missing number
The missing number multiplied by 2, plus 2, gives 728. So \( 728 - 2 = 726 \) and \( 726 \div 2 = 363 \).
Step 4: Check
\( 363 \times 2 + 2 = 728 \) ✓.""", trick=r"Rule: ×2 + 2; undo it on 728 → \( (728 - 2) \div 2 = 363 \).")
S[14] = dict(raw=r"""Step 1: Split each term into letters and number
Letters: BZ, ZB, XD, ?, TH. Numbers: 200, 400, 800, ?, 3200.
Step 2: Rule for the numbers
Each number is doubled: 200 → 400 → 800 → 1600 → 3200. So the missing number is 1600.
Step 3: Rule for the letters
First letters: B (2) → Z (26) → X (24) fall by 2 each time, so the missing one is X − 2 = V (22), and V − 2 = T ✓. Second letters: Z → B → D rise by 2 each time, so the missing one is D + 2 = F, and F + 2 = H ✓.
Step 4: Answer
The missing term is VF1600.""", trick=r"Number ×2, first letter −2, second letter +2 → VF1600.")
S[15] = dict(raw=r"""Step 1: Split each term into letters and number
Numbers: 20, 40, 88, 160, 320, 640. Letters: FFE, EGD, DHD, CIB, BJA, AKZ.
Step 2: Rule for the numbers
Each number is double the one before it: 20, 40, 80, 160, 320, 640. The third number should be 80, but the series shows 88.
Step 3: Rule for the letters
First letters fall by 1 (F, E, D, C, B, A), second letters rise by 1 (F, G, H, I, J, K), and third letters fall by 1 (E, D, C, B, A, Z). In DHD the third letter should be C, but it is D.
Step 4: Answer
Every other term follows both rules fully, so the wrong term is DHD88.""", trick=r"Numbers must double (20, 40, 80 …) → 88 breaks it, so DHD88 is wrong.")
S[16] = dict(raw=r"""Step 1: Set up the positions of the hands
At m minutes past 6, the hour hand is at \( 180 + 0.5m \) degrees and the minute hand is at \( 6m \) degrees, both measured from 12.
Step 2: First time (minute hand behind the hour hand)
Angle \( = (180 + 0.5m) - 6m = 180 - 5.5m = 30 \), so \( m = \dfrac{150}{5.5} \approx 27.27 \), which is about 6:27 — not in the options.
Step 3: Second time (minute hand ahead of the hour hand)
Angle \( = 6m - (180 + 0.5m) = 5.5m - 180 = 30 \), so \( m = \dfrac{210}{5.5} \approx 38.18 \), which is about 6:38.
Step 4: Choose from the options
Only 6:38 is available among the given times, so the required approximate time is 6:38.""", trick=r"Angle between the hands m minutes past 6 is \( |180 - 5.5m| \); set it to 30 → 6:27 or about 6:38.")
S[17] = dict(raw=r"""Step 1: Find the real time that passes
From 8 AM to 8 PM is 12 hours \( = 12 \times 60 = 720 \) minutes.
Step 2: Count the 6-minute blocks
\( 720 \div 6 = 120 \) blocks, and the clock gains 2 seconds in each block.
Step 3: Find the total gain
\( 120 \times 2 = 240 \) seconds \( = 4 \) minutes.
Step 4: Find the time shown
When the real time is 8 PM, the fast clock shows 8 PM + 4 minutes = 8:04:00 PM.""", trick=r"720 minutes ÷ 6 = 120 gains of 2 seconds = 240 seconds = 4 minutes fast.")
S[18] = dict(raw=r"""Step 1: Note the parts of each figure
Every box has an eight-ray star, one arrow at the end of a ray and one small solid shape at the end of another ray.
Step 2: Track the arrow
The arrow sits at the top-right ray, then the right ray, then the bottom-right ray, then the bottom ray. It moves 45° clockwise each step, so in the fifth figure it is at the bottom-left ray.
Step 3: Track the solid shape
The shape sits at the bottom-right ray, bottom ray, bottom-left ray, then the left ray: it also moves 45° clockwise each step, so in the fifth figure it is at the top-left ray. Its type alternates diamond, square, diamond, square, so the fifth is a diamond.
Step 4: Pick the matching figure
The correct figure has the arrow at the bottom-left ray and a solid diamond at the top-left ray. The figure that repeats the first figure (arrow top-right, diamond bottom-right) is wrong, the one with a square at the left ray has the wrong shape and position, and the one with the arrow at the right ray and a diamond at the bottom-left ray is out of sequence.""", trick=r"Arrow and shape each move 45° clockwise; the shape alternates diamond, square → diamond at the top-left.")
S[19] = dict(raw=r"""Step 1: Spot the change from figure to figure
Each figure has one long line with a short cross-bar near one end, an arrow at the other end, a solid shape on a short stem and a small side arrow. The whole figure keeps turning.
Step 2: Find the angle of turning
The line is upright in the first figure, slants like “/” in the second, lies flat in the third and slants like “\” in the fourth. So the figure turns 45° clockwise each step.
Step 3: Verify with two steps
First to third is a 90° clockwise turn: the top arrow goes to the right end, the right-pointing side arrow points down, and the solid square moves from the bottom-left to the top-left ✓.
Step 4: Build the fifth figure
Five steps need a total turn of 180° from the first figure: the line is upright again with its arrowhead at the bottom, the side arrow points left and the solid square is at the top-right. Only one option shows this; the vertical figure with the arrow pointing right and the square at the top-left is a mirror image, and the two slanting figures are turns of other angles.""", trick=r"The whole figure turns 45° clockwise each step → the fifth is the first turned upside down.")
S[20] = dict(raw=r"""Step 1: Note the shapes
Each box is divided into four parts holding a triangle, a square, a circle and a solid house-shaped pentagon, one in each part.
Step 2: Track the triangle
The triangle is in the top-left part, then the top-right, then the bottom-right, then the bottom-left: one part clockwise each step.
Step 3: Check the other shapes
The circle goes bottom-left → top-left → top-right → bottom-right, the square goes top-right → bottom-right → bottom-left → top-left and the house goes bottom-right → bottom-left → top-left → top-right. All four shapes move one part clockwise each step.
Step 4: Build the fifth figure
One more step puts the triangle at the top-left, the square at the top-right, the house at the bottom-right and the circle at the bottom-left. That is the same as the first figure, since the pattern repeats after four steps.""", trick=r"All four shapes move one part clockwise per step; the pattern repeats every 4 steps → the fifth equals the first.")
