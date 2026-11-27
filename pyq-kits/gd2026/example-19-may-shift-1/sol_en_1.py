S = {}
S[1] = dict(raw=r"""Step 1: Find the differences between consecutive terms
−84 → −95 (−11), −95 → −107 (−12), −107 → −117 (−10), −117 → −128 (−11), −128 → −139 (−11), −139 → −150 (−11), −150 → −161 (−11).
Step 2: Spot the rule
Almost every gap is −11, so the series should fall by 11 at every step.
Step 3: Rebuild the series with −11
−84, −95, −106, −117, −128, −139, −150, −161.
Step 4: Compare
The third term should be −106, but the series shows −107. So −107 is the wrong term.""", trick=r"Constant gap −11; the only term that breaks it is −107 (should be −106).")
S[2] = dict(raw=r"""Step 1: Find the known differences
250 − 243 = 7; then 277 − 267 = 10, 288 − 277 = 11, 300 − 288 = 12, 313 − 300 = 13.
Step 2: Spot the rule
The gaps increase by 1 each time: +7, +8, +9, +10, +11, +12, +13.
Step 3: Fill the missing term
250 + 8 = 258.
Step 4: Check
258 + 9 = 267 ✓, which is the next term of the series. So the missing term is 258.""", trick=r"Gaps +7, +8, +9 … → 250 + 8 = 258.")
S[3] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: ?, E, C, A, Y, W, U, S. Second letters: ?, E, Z, T, M, E, V, L.
Step 2: Rule for the first letters
E (5) → C (3) → A (1) → Y (25) → W (23) → U (21) → S (19): each step is −2. So the missing first letter is E + 2 = G (7).
Step 3: Rule for the second letters
E (5) → Z (26) → T (20) → M (13) → E (5) → V (22) → L (12): the gaps are −5, −6, −7, −8, −9, −10. One step back the gap is −4, so the missing letter is E + 4 = I (9).
Step 4: Answer
The missing term is GI (G − 2 = E ✓ and I − 4 = E ✓).""", trick=r"First letters −2 each; second letters −4, −5, −6 … −10.")
S[4] = dict(raw=r"""Step 1: First letters
K (11) → O (15) → T (20) → ? → C (3) → G (7) → L (12) → P (16): the gaps alternate +4, +5. After T the gap is +4, so the missing first letter is X (24). Check: X + 5 = 29 → 3 = C ✓.
Step 2: Second letters
E (5) → A (1) → V (22) → ? → I (9) → A (1) → R (18) → H (8).
Step 3: Find the rule for the second letters
E → A is −4, A → V is −5 (1 − 5 = −4 → 22). Continue with −6: V (22) − 6 = 16 = P. Check: P − 7 = I ✓, I − 8 = A ✓, A − 9 = R ✓ and R − 10 = H ✓.
Step 4: Answer
The missing term is XP.""", trick=r"First letters +4, +5 alternately; second letters −4, −5, −6 …")
S[5] = dict(raw=r"""Step 1: Study the first set (WL, YN, BR)
First letters W (23) → Y (25) → B (28 → 2): +2, then +3. Second letters L (12) → N (14) → R (18): +2, then +4.
Step 2: Confirm with the second set (TH, VJ, YN)
T (20) → V (22) → Y (25) is +2, +3 and H (8) → J (10) → N (14) is +2, +4 ✓.
Step 3: Test the options
(NO, PQ, SU): N (14) → P (16) → S (19) is +2, +3 and O (15) → Q (17) → U (21) is +2, +4 ✓. In (SV, UW, WZ) and (GO, IU, KY) the first letters move +2, +2; in (GR, FS, KX) they move −1 first ✗.
Step 4: Answer
Only (NO, PQ, SU) follows the same rule.""", trick=r"First letters +2, +3; second letters +2, +4.")
S[6] = dict(raw=r"""Step 1: Study the first set (OG, ME, JB)
First letters O (15) → M (13) → J (10): −2, then −3. Second letters G (7) → E (5) → B (2): −2, then −3.
Step 2: Confirm with the second set (GM, EK, BH)
G (7) → E (5) → B (2) is −2, −3 and M (13) → K (11) → H (8) is −2, −3 ✓.
Step 3: Test the options
(CP, AN, XK): C (3) → A (1) → X (24, since 1 − 3 = −2 → 24) is −2, −3, and P (16) → N (14) → K (11) is −2, −3 ✓. (ZU, WR, VO) starts with −3; (OW, NT, KQ) starts with −1; (WE, RB, SY) starts with −5 ✗.
Step 4: Answer
Only (CP, AN, XK) follows the same rule.""", trick=r"Both letters −2, then −3 (wrap A → Z when needed).")
S[7] = dict(raw=r"""Step 1: Find the differences
−685 − (−771) = 86, −599 − (−685) = 86, −513 − (−599) = 86, and so on.
Step 2: Spot the rule
Each term is 86 more than the term before it.
Step 3: Fill the missing term
−341 + 86 = −255.
Step 4: Check
−255 + 86 = −169 ✓, which is the last term. So the missing term is −255.""", trick=r"Add 86 every time: −341 + 86 = −255.")
S[8] = dict(raw=r"""Step 1: Write the given conditions
C has fewer wickets than E and B, but more than A. D has the fewest wickets of all.
Step 2: Build the order (fewest to most)
D < A < C < (B and E in some order).
Step 3: Use B = 12
C is less than B, so C < 12, and A is less than C, so A must be less than 12 (and A cannot be the lowest, since D is).
Step 4: Check the options
16, 14 and 20 are all more than 12, so they are impossible. Only 8 works (for example D = 5, A = 8, C = 10, B = 12, E = 15).""", trick=r"A < C < B = 12, so A < 12 → only 8 fits.")
S[9] = dict(raw=r"""Step 1: Place S and P
P is lighter than only S, so S is the heaviest (1st) and P is 2nd.
Step 2: Place R
R is heavier than only V and T, so exactly two boys (V and T) are lighter than R. That makes R 4th from the top, with Q in 3rd place.
Step 3: Place T and V
Boys heavier than P = 1 (only S). So the number of boys lighter than T must also be 1, which means T is 5th and V is the lightest (6th).
Step 4: Count the boys heavier than T
Order: S > P > Q > R > T > V. Boys heavier than T are S, P, Q and R, which is 4.""", trick=r"S > P > Q > R > T > V → 4 boys above T.")
S[10] = dict(raw=r"""Step 1: Study KK780 → OO420
Letters: K (11) + 4 = O (15) and K + 4 = O. Number: \( 780 - 360 = 420 \).
Step 2: Confirm with AG510 → EK150
A (1) + 4 = E (5), G (7) + 4 = K (11). Number: \( 510 - 360 = 150 \) ✓.
Step 3: Work backwards to find ?
? is related to TZ130 in the same way, so ? = TZ130 with each letter moved back by 4 and 360 added: T (20) − 4 = P (16), Z (26) − 4 = V (22), \( 130 + 360 = 490 \).
Step 4: Check
PV490 → P + 4 = T, V + 4 = Z, \( 490 - 360 = 130 \), giving TZ130 ✓. So ? = PV490.""", trick=r"Letters +4 each, number −360; reverse it: TZ130 → PV490.")
S[11] = dict(raw=r"""Step 1: Study TU100 → PO150
Letters: T (20) − 4 = P (16) and U (21) − 6 = O (15). Number: \( 100 \times 1.5 = 150 \).
Step 2: Confirm with JK140 → FE210
J (10) − 4 = F (6) and K (11) − 6 = E (5). Number: \( 140 \times 1.5 = 210 \) ✓ (the number is not +50 here, so × 1.5 is the rule).
Step 3: Apply the rule to VW120
V (22) − 4 = R (18), W (23) − 6 = Q (17), \( 120 \times 1.5 = 180 \).
Step 4: Answer
The required cluster is RQ180.""", trick=r"First letter −4, second letter −6, number × 1.5.")
S[12] = dict(raw=r"""Step 1: Study the first pair
\( 9243 - 9198 = 45 \).
Step 2: Confirm with the second pair
\( 7921 - 7876 = 45 \) ✓. So the first number of each pair is 45 more than the second.
Step 3: Apply the rule to the third pair
? is the first number and 7869 the second, so \( ? = 7869 + 45 = 7914 \).
Step 4: Check
\( 7914 - 45 = 7869 \) ✓. So ? = 7914.""", trick=r"First − 45 = second → ? = 7869 + 45 = 7914.")
S[13] = dict(raw=r"""Step 1: Study 469 → 149
\( 469 - 149 = 320 \), so the second number is 320 less than the first.
Step 2: Confirm with 892 → 572
\( 892 - 572 = 320 \) ✓.
Step 3: Apply the rule to 551
\( 551 - 320 = 231 \).
Step 4: Answer
? = 231.""", trick=r"Subtract 320: 551 − 320 = 231.")
S[14] = dict(raw=r"""Step 1: First letters
P (16) → N (14) → ? → J (10) → H (8): −2 each, so the missing letter is L (12).
Step 2: Second letters
O (15) → Q (17) → ? → U (21) → W (23): +2 each, so the missing letter is S (19).
Step 3: Numbers
76 → 152 → ? → 608 → 1216: each number is doubled, so \( 152 \times 2 = 304 \). Check: \( 304 \times 2 = 608 \) ✓.
Step 4: Answer
The missing term is LS304.""", trick=r"Letters −2 and +2, number × 2.")
S[15] = dict(raw=r"""Step 1: First letters
U (21) → ? → Y (25) → A (27 → 1) → C (3): +2 each, so the missing letter is W (23).
Step 2: Second and third letters
Second: R (18) → ? → V (22) → X (24) → Z (26), +2 each → T (20). Third: K (11) → ? → O (15) → Q (17) → S (19), +2 each → M (13).
Step 3: Numbers
984 − 670 = 314 over two steps, and 1141 − 984 = 157, 1298 − 1141 = 157. So each step is +157: \( 670 + 157 = 827 \).
Step 4: Answer
The missing term is WTM827 (check: \( 827 + 157 = 984 \) ✓).""", trick=r"All three letters +2; number +157.")
S[16] = dict(raw=r"""Step 1: Recall the formula
Angle between the hands \( = \left| 30H - \dfrac{11}{2}M \right| \), where H is the hour and M the minutes.
Step 2: Put in the values
At 1:10, H = 1 and M = 10.
Step 3: Calculate
\( 30 \times 1 = 30 \) and \( \dfrac{11}{2} \times 10 = 55 \), so the angle \( = \left| 30 - 55 \right| = 25 \).
Step 4: Answer
The angle between the hands at 1:10 PM is 25°.""", trick=r"θ = |30H − 5.5M| = |30 − 55| = 25°.")
S[17] = dict(raw=r"""Step 1: Find how much time the watch must gain
At 3 PM it is 6 minutes slow, so it must gain 6 minutes \( = 6 \times 60 = 360 \) seconds to show the correct time.
Step 2: Use the rate of gain
It gains 12 seconds every hour.
Step 3: Find the time needed
\( 360 \div 12 = 30 \) hours.
Step 4: Find the clock time
30 hours after 3 PM = 24 hours (3 PM the next day) + 6 hours = 9 PM the next day. So it shows the correct time again at 9:00 PM.""", trick=r"6 min = 360 s; 360 ÷ 12 = 30 h; 3 PM + 30 h = 9 PM (next day).")
S[18] = dict(raw=r"""Step 1: Track the outer stick
The short stick outside the circle points down in the first figure, then bottom-left, then left, then top-left: it moves 45° clockwise each time. So in the fifth figure it points straight up.
Step 2: Track the inner pin
The flat bar of the pin inside the circle points up in the first figure, then top-right, then right, then bottom-right: it also turns 45° clockwise each time. So in the fifth figure the bar points straight down.
Step 3: Write the answer figure
The fifth figure has the stick at the top of the circle and the pin standing with its flat bar at the bottom.
Step 4: Check the options
Only one option has both the stick at the top and the bar at the bottom; the others have the stick at the top-right or the bar pointing to the bottom-left.""", trick=r"Stick and pin both turn 45° clockwise every step.")
S[19] = dict(raw=r"""Step 1: Compare figure 1 with figure 2
Figure 1 rows: (U, V), (Z, R), (Y, X). Figure 2 rows: (Y, X), (U, V), (Z, R). Every row moves one place down, and the bottom row comes to the top.
Step 2: Compare figure 2 with figure 3
Figure 3 rows: (X, Y), (V, U), (R, Z). The rows stay in place, but the two letters of every row swap sides.
Step 3: Confirm the pattern with figure 4
Figure 4 rows: (R, Z), (X, Y), (V, U) — the rows of figure 3 have moved one place down again. So the steps alternate: rows move down, then letters swap sides.
Step 4: Find figure 5
Swap the letters of each row of figure 4: (Z, R), (Y, X), (U, V). Only one option shows Z R / Y X / U V.""", trick=r"Alternate steps: shift rows down, then swap left and right.")
S[20] = dict(raw=r"""Step 1: Count the arrows
The figures have 5, 4, 3 and 2 arrows: one arrow (the leftmost) is removed each time. So the fifth figure has 1 arrow, at the bottom-right.
Step 2: Track the triangle
The triangle is filled at the top-right, then hollow at the top-left, then filled at the top-right, then hollow at the top-left — it alternates.
Step 3: Find the triangle in figure 5
Following the alternation, the fifth figure has a filled triangle at the top-right.
Step 4: Check the options
Only one option has a filled triangle at the top-right and one arrow at the bottom-right; the others have a hollow triangle or the triangle at the top-left.""", trick=r"Arrows 5 → 4 → 3 → 2 → 1; triangle alternates filled right / hollow left.")
