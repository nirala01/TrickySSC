S = {}
S[1] = dict(raw=r"""Step 1: Write the differences
385 → 385 → 380 → 373 → 364 → 353 → 340 → 325 gives 0, −5, −7, −9, −11, −13, −15.
Step 2: Spot the pattern
From the second difference on, the gaps are consecutive odd numbers: −5, −7, −9, −11, −13, −15. So the first gap must be −3.
Step 3: Find the correct first term
The second term 385 is right (385 − 5 = 380 ✓), so the first term should be \( 385 + 3 = 388 \).
Step 4: Answer
The first term 385 is the wrong term; the series should start 388, 385, 380, 373 …""", trick=r"Gaps −3, −5, −7 …; the opening 385 breaks the odd-number chain.")
S[2] = dict(raw=r"""Step 1: Write the letter positions
T (20), ?, J (10), E (5), Z (26), U (21), P (16), K (11).
Step 2: Find the gap
J → E is −5, E (5) → Z (26) is −5 with wrap-around (5 − 5 = 0 → 26), Z → U, U → P and P → K are all −5.
Step 3: Fill the blank
T (20) − 5 = 15 = O, and O (15) − 5 = 10 = J ✓.
Step 4: Answer
The missing letter is O.""", trick=r"Every step −5: T, O, J, E, Z, U, P, K.")
S[3] = dict(raw=r"""Step 1: Study JH and OS
J (10) → O (15) is +5. H (8) and S (19) are opposite letters (\( 8 + 19 = 27 \)).
Step 2: Confirm with RC and WX
R (18) → W (23) is +5, and C (3) and X (24) are opposite letters (\( 3 + 24 = 27 \)) ✓.
Step 3: Work backwards to the missing cluster (? → RZ)
First letter: R (18) − 5 = 13 = M. Second letter: the opposite of Z (26) is A (1).
Step 4: Answer
The missing cluster is MA. Check: M + 5 = R ✓ and A ↔ Z are opposites ✓.""", trick=r"First letter +5; second letter jumps to its opposite (sum 27).")
S[4] = dict(raw=r"""Step 1: Write the first letters
T (20), V (22), Y (25), C (29 → 3), ?, N (40 → 14), U (47 → 21), C (55 → 3): the gaps are +2, +3, +4, then +5, +6, +7, +8.
Step 2: Find the first letter
C (29) + 5 = 34 → 34 − 26 = 8 = H, and H (8) + 6 = 14 = N ✓.
Step 3: Find the second letter
Second letters I (9), H (8), F (6), C (3), ?, T (20), N (14), G (7) fall by 1, 2, 3, then 4, 5, 6, 7: C (3) − 4 = −1 → 25 = Y, and Y (25) − 5 = 20 = T ✓.
Step 4: Answer
The missing term is HY.""", trick=r"First letters +2, +3, +4 …; second letters −1, −2, −3 … (wrap past Z/A).")
S[5] = dict(raw=r"""Step 1: Read the pairs the right way round
The second cluster is made from the first: BV → UE, and the sixth from the fifth: XA → QZ.
Step 2: Find the rule from BV → UE
B (2) − 7 = −5 → 21 = U. V (22) and E (5) are opposite letters (\( 22 + 5 = 27 \)).
Step 3: Confirm with XA → QZ
X (24) − 7 = 17 = Q ✓ and A (1) ↔ Z (26) are opposites ✓.
Step 4: Apply to CJ
C (3) − 7 = −4 → 22 = V; the opposite of J (10) is Q (17). The answer is VQ.""", trick=r"First letter −7; second letter → its opposite (sum 27).")
S[6] = dict(raw=r"""Step 1: Study the first set (HS, JU, MX)
First letters H (8) → J (10) → M (13): +2, then +3. Second letters S (19) → U (21) → X (24): +2, then +3.
Step 2: Confirm with (WO, YQ, BT)
W (23) → Y (25) → B (28 → 2) is +2, +3 and O (15) → Q (17) → T (20) is +2, +3 ✓.
Step 3: Test the options
(LZ, NB, QE): L (12) → N (14) → Q (17) is +2, +3 and Z (26) → B (28 → 2) → E (5) is +2, +3 ✓. In (FH, GK, HK) the first letters go +1, +1; in (VP, YS, XW) they go +3, −1; in (JT, MW, RA) they go +3, +5 ✗.
Step 4: Answer
Only (LZ, NB, QE) moves +2, +3 on both letters.""", trick=r"Both letters of each cluster move +2, then +3.")
S[7] = dict(raw=r"""Step 1: Reach the last day of this month
The month has 30 days. From the 8th to the 30th is \( 30 - 8 = 22 \) days = 3 weeks + 1 day.
Step 2: Day on the 30th
Thursday + 1 = Friday, so the 30th (last day of the month) is a Friday.
Step 3: Reach the 15th of the next month
From the 30th of this month to the 15th of the next month is 15 days = 2 weeks + 1 day.
Step 4: Answer
Friday + 1 = Saturday. So the 15th of the next month is a Saturday.""", trick=r"Count odd days: 22 → 1, then 15 → 1; Thursday + 2 = Saturday.")
S[8] = dict(raw=r"""Step 1: Odd days in complete centuries
1600 years give 0 odd days and 100 years give 5 odd days, so the first 1700 years give \( 0 + 5 = 5 \) odd days.
Step 2: Odd days from 1701 to 1754
There are 54 years, of which 13 are leap years (1704, 1708, …, 1752). Odd days \( = 54 + 13 = 67 \), and \( 67 \div 7 \) leaves 4.
Step 3: Total up to 31 December 1754
\( 5 + 4 = 9 \) → 2 odd days, so 31 December 1754 was a Tuesday (0 = Sunday, 1 = Monday, 2 = Tuesday).
Step 4: Answer
1 January 1755 comes one day later: Wednesday.""", trick=r"Odd days till 1754 = 2 (Tuesday), so 1 Jan 1755 = Wednesday.")
S[9] = dict(raw=r"""Step 1: Place P, L and J
L is second to the right of P and J is second to the right of L, so the order is P _ L _ J — this uses all five seats.
Step 2: Fill the two gaps
K is second to the left of Q, so K takes seat 2 and Q takes seat 4.
Step 3: Write the row (left to right)
P, K, L, Q, J.
Step 4: Answer
J sits at the right end of the row.""", trick=r"P _ L _ J fills five seats; K and Q drop into the gaps.")
S[10] = dict(raw=r"""Step 1: Join the fixed blocks
R P (P to the immediate right of R) and S V Q (V right of S and left of Q).
Step 2: Place P and S
One child sits between P and S. Placing S two seats right of P gives R P _ S V Q in seats 1–6.
Step 3: Place U and T
S (seat 4) and U have two children between them, so U is in seat 7. T and Q (seat 6) have two children between them, so T is in seat 3.
Step 4: Answer
The row is R, P, T, S, V, Q, U, so T sits between P and S.""", trick=r"Build R P and S V Q first, then use the counts for T and U.")
S[11] = dict(raw=r"""Step 1: Study the line in the first pair
The vertical line with one arrow-head turns 90° to become a horizontal line, and it now has an arrow-head at BOTH ends.
Step 2: Study the small circle
The circle moves from the top-left corner to the bottom-right corner — it turns 180° about the centre.
Step 3: Apply this to the third figure
The diagonal line (circle at one end, from top-left to bottom-right) turns 90° to run from bottom-left to top-right, with a circle at both ends. The small square below the line moves 180° to the upper-right side above the line.
Step 4: Answer
The figure with a bottom-left to top-right line, circles at both ends and the square above the line near the top-right fits.""", trick=r"Line turns 90° and gets the end mark on both ends; the loose symbol turns 180°.")
S[12] = dict(raw=r"""Step 1: Track every corner in the first pair
C (top-left) → bottom-right; ▲ (top-right) → top-left; × (bottom-left) → top-right; ● (bottom-right) → bottom-left.
Step 2: Write the rule
top-left → bottom-right, top-right → top-left, bottom-left → top-right, bottom-right → bottom-left.
Step 3: Apply it to the third figure (U, ■, ●, T)
U (top-left) → bottom-right; ■ (top-right) → top-left; ● (bottom-left) → top-right; T (bottom-right) → bottom-left.
Step 4: Answer
The answer has ■ at top-left, ● at top-right, T at bottom-left and U at bottom-right.""", trick=r"Copy the corner-to-corner moves of the first pair exactly.")
S[13] = dict(raw=r"""Step 1: Study CP10 → ER38
C (3) → E (5) is +2, P (16) → R (18) is +2, and \( 10 + 28 = 38 \).
Step 2: Confirm with VS40 → XU68
V → X is +2, S → U is +2, and \( 40 + 28 = 68 \) ✓.
Step 3: Work backwards from KO56
K (11) − 2 = 9 = I, O (15) − 2 = 13 = M, and \( 56 - 28 = 28 \).
Step 4: Answer
The missing cluster is IM28.""", trick=r"Letters +2, +2; number +28 — go backwards for the blank.")
S[14] = dict(raw=r"""Step 1: Study AK120 → FD250
A (1) → F (6) is +5, K (11) → D (4) is −7, and \( 120 + 130 = 250 \).
Step 2: Confirm with LL210 → QE340
L (12) → Q (17) is +5, L (12) → E (5) is −7, and \( 210 + 130 = 340 \) ✓.
Step 3: Apply to KM250
K (11) + 5 = 16 = P, M (13) − 7 = 6 = F, and \( 250 + 130 = 380 \).
Step 4: Answer
The missing cluster is PF380.""", trick=r"First letter +5, second letter −7, number +130.")
S[15] = dict(raw=r"""Step 1: Test 540 → 272
\( \dfrac{540}{2} = 270 \) and \( 270 + 2 = 272 \).
Step 2: Confirm with 210 → 107
\( \dfrac{210}{2} = 105 \) and \( 105 + 2 = 107 \) ✓.
Step 3: Apply to 134
\( \dfrac{134}{2} = 67 \) and \( 67 + 2 = 69 \).
Step 4: Answer
The required number is 69.""", trick=r"Halve the number, then add 2.")
S[16] = dict(raw=r"""Step 1: Compare GUFF with HWIJ
G → H (+1), U → W (+2), F → I (+3), F → J (+4).
Step 2: Confirm with MONK → NQQO
M → N (+1), O → Q (+2), N → Q (+3), K → O (+4) ✓.
Step 3: Apply to HINT
H + 1 = I, I + 2 = K, N + 3 = Q, T + 4 = X.
Step 4: Answer
HINT is coded as IKQX.""", trick=r"Add 1, 2, 3, 4 to the letters in order.")
S[17] = dict(raw=r"""Step 1: Find the time passed
From 9 AM to 9 PM is 12 hours = \( 12 \times 60 = 720 \) minutes.
Step 2: Find how much the clock gains
It gains 1 second every 3 minutes, so in 720 minutes it gains \( \dfrac{720}{3} = 240 \) seconds.
Step 3: Convert to minutes
240 seconds = 4 minutes.
Step 4: Answer
A gaining clock runs ahead, so at the true time 9 PM it shows 9:04:00.""", trick=r"Gain = 720 ÷ 3 = 240 s = 4 min ahead.")
S[18] = dict(raw=r"""Step 1: Follow the outer arc
The arc sits at the top, then upper-right, then right, then lower-right: it moves 45° clockwise each time, so it must be at the bottom next.
Step 2: Follow the symbol sets
Figures 1 and 3 hold a triangle, × and square; figures 2 and 4 hold a diamond, + and triangle. The sets alternate, so the fifth figure has a triangle, × and square.
Step 3: Fix the positions
In figures 1 and 3 the square stays on the right, × goes to the bottom, and the triangle turns 90° clockwise each time it appears (pointing up, then right), so next it points down.
Step 4: Answer
The figure with the arc at the bottom, a downward triangle on the left, × at the bottom and the square on the right fits.""", trick=r"Arc +45° clockwise; symbol sets alternate; triangle up → right → down.")
S[19] = dict(raw=r"""Step 1: Follow the arrow
The double arrow turns 45° clockwise each time: vertical, then slanting, then horizontal, then slanting the other way — so it is vertical again next, with the curved head at the top and the arrow-head at the bottom.
Step 2: Follow the dot colours
Figures 1 and 3 have two black dots and one white; figures 2 and 4 have two white and one black. So figure 5 has two black dots and one white.
Step 3: Fix the dot positions
Each step turns the whole figure 45° clockwise, so figure 5 is figure 3 turned 90° clockwise: the black dot above the line goes to the right of it, the black dot at the bottom-right goes to the lower left, and the white dot at the bottom-left goes to the upper left.
Step 4: Answer
The vertical arrow with a white dot at upper left, a black dot at lower left and a black dot on the right fits.""", trick=r"Turn the figure two steps back (figure 3) by 90° clockwise.")
S[20] = dict(raw=r"""Step 1: Use the ratio
Let the ages be 11x and 5x.
Step 2: Use the difference
\( 11x - 5x = 6x = 18 \), so \( x = 3 \). The ages are 33 years and 15 years.
Step 3: Add 5 years
After 5 years: \( 33 + 5 = 38 \) and \( 15 + 5 = 20 \).
Step 4: Answer
The ratio is \( 38 : 20 = 19 : 10 \).""", trick=r"6 parts = 18 → 1 part = 3; then add 5 to both ages.")
