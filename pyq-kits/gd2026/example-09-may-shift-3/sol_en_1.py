S = {}
S[1] = dict(raw=r"""Step 1: Write the letter positions
W (23), D (4), L (12), S (19), ?, H (8), P (16), W (23), E (5).
Step 2: Find the gaps
W → D is +7 (23 + 7 = 30 → 30 − 26 = 4), D → L is +8, L → S is +7. The gaps alternate +7, +8.
Step 3: Find the missing term
S (19) + 8 = 27 → 27 − 26 = 1 = A.
Step 4: Check the rest
A (1) + 7 = 8 = H ✓, H + 8 = P ✓, P + 7 = W ✓, W + 8 = 31 − 26 = 5 = E ✓.""", trick=r"Alternate +7, +8 — after S comes +8, wrapping Z back to A.")
S[2] = dict(raw=r"""Step 1: Study the first pair EIS → JNX
E (5) → J (10), I (9) → N (14), S (19) → X (24): every letter moves +5.
Step 2: Confirm with KZL → PEQ
K (11) → P (16), Z (26) → E (31 − 26 = 5), L (12) → Q (17): +5 each ✓.
Step 3: Work backwards from VSR
The fifth cluster becomes VSR, so subtract 5 from each letter: V (22) → Q (17), S (19) → N (14), R (18) → M (13).
Step 4: Answer and check
The missing cluster is QNM; Q + 5 = V, N + 5 = S, M + 5 = R ✓.""", trick=r"Every letter +5 — reverse it (−5) to find the fifth cluster.")
S[3] = dict(raw=r"""Step 1: Write the first letters
V (22), S (19), P (16), ?, J (10), G (7), D (4), A (1): each step is −3, so the missing first letter is P (16) − 3 = 13 = M.
Step 2: Write the second letters
L (12), J (10), G (7), ?, X (24), R (18), K (11), C (3).
Step 3: Find the gaps of the second letters
−2, −3, then −4, −5, −6, −7, −8: G (7) − 4 = 3 = C, and C (3) − 5 = −2 → 24 = X ✓.
Step 4: Answer
The missing term is MC.""", trick=r"First letters −3; second letters −2, −3, −4, −5 … (wrap past A to Z).")
S[4] = dict(raw=r"""Step 1: Study NS → JM
N (14) → J (10) is −4 and S (19) → M (13) is −6.
Step 2: Confirm with RY → NS
R (18) → N (14) is −4 and Y (25) → S (19) is −6 ✓.
Step 3: Work backwards from HO
The fifth cluster becomes HO, so add 4 to the first letter and 6 to the second: H (8) + 4 = 12 = L, O (15) + 6 = 21 = U.
Step 4: Answer and check
The missing cluster is LU; L − 4 = H and U − 6 = O ✓. MR, MU and LT do not give HO.""", trick=r"First letter −4, second letter −6; reverse it to go back from HO.")
S[5] = dict(raw=r"""Step 1: Study the first set (SY, UA, YE)
First letters S (19) → U (21) → Y (25): +2, then +4. Second letters Y (25) → A (27 → 1) → E (5): +2, then +4.
Step 2: Confirm with (RV, TX, XB)
R → T → X is +2, +4 and V → X → B (28 → 2) is +2, +4 ✓. So both letters move +2 and then +4 across the set.
Step 3: Test the options
(PM, RO, VS): P → R → V is +2, +4 and M → O → S is +2, +4 ✓. (NV, PX, RG): N → P → R is +2, +2 ✗. (EI, GO, IN): E → G → I is +2, +2 ✗. (NE, PJ, RP): N → P → R is +2, +2 ✗.
Step 4: Answer
Only (PM, RO, VS) follows the +2, +4 pattern on both letters.""", trick=r"Read each set column-wise: +2 then +4 on the first and on the second letters.")
S[6] = dict(raw=r"""Step 1: Find the number of days
2008 is divisible by 4, so it is a leap year and February 2008 has 29 days = 4 weeks + 1 extra day.
Step 2: Find the extra day
1 February 2008 was a Friday, so the extra (29th) day is also a Friday.
Step 3: Count each day
In 4 full weeks every weekday occurs 4 times; the extra day adds one more Friday. Wednesday = 4, Thursday = 4, Friday = 5.
Step 4: Add
\( 4 + 4 + 5 = 13 \).""", trick=r"29-day February: the weekday of 1 February occurs 5 times, every other day 4 times.")
S[7] = dict(raw=r"""Step 1: Find the day on 1 January 1914
1 January 1900 was a Monday. From 1900 to 1913 there are 14 years with 3 leap years (1904, 1908, 1912), so the odd days are \( 14 + 3 = 17 \) → 3. Monday + 3 = Thursday.
Step 2: Check January 1914
A 31-day month has its first 3 weekdays 5 times: Thursday, Friday and Saturday. Monday occurs only 4 times.
Step 3: Find the day on 1 April 1914
January (31) gives 3 odd days → 1 February is a Sunday; February 1914 (28 days) gives 0 → 1 March is a Sunday; March (31) gives 3 → 1 April is a Wednesday.
Step 4: Check April 1914
A 30-day month has its first 2 weekdays 5 times: Wednesday and Thursday. Monday occurs only 4 times, so neither month had 5 Mondays.""", trick=r"A month has 5 Mondays only if Monday is among its first 3 (31 days) or 2 (30 days) dates.")
S[8] = dict(raw=r"""Step 1: Find the differences
−496 → −371 is +125, −371 → −246 is +125, −246 → −121 is +125.
Step 2: Spot the rule
Each term is 125 more than the one before it.
Step 3: Find the missing term
\( -121 + 125 = 4 \).
Step 4: Check
\( 4 + 125 = 129 \) ✓, \( 129 + 125 = 254 \) ✓, \( 254 + 125 = 379 \) ✓.""", trick=r"Constant difference +125 all through the series.")
S[9] = dict(raw=r"""Step 1: Place P
Three girls are to the right of P, so P is 2nd from the left.
Step 2: Place J
Four girls are to the left of J, so J is 5th (the right end).
Step 3: Place K and L
The free places are 1, 3 and 4. K must be immediately left of L, so K is 3rd and L is 4th, leaving Q in 1st place. Row: Q, P, K, L, J.
Step 4: Count between Q and L
Between Q (1st) and L (4th) sit P and K, so 2 girls.""", trick=r"Fix the girls with exact counts (P, J) first, then fit the pair K-L.")
S[10] = dict(raw=r"""Step 1: Join the linked clues
V is immediately right of S and immediately left of Q, so S, V, Q sit together in that order. P is immediately right of R, so R, P sit together.
Step 2: Use "one child between P and S"
P cannot be right of S (that place is V's), so the order is R, P, _, S, V, Q.
Step 3: Fit U and T
Two children between S and U: U is three places from S. Taking R at the left end gives R, P, _, S, V, Q with U at the right end (7th). The gap is T, and T (3rd) and Q (6th) have two children between them ✓.
Step 4: Answer
Row: R, P, T, S, V, Q, U — R is at the left end.""", trick=r"Build the blocks S-V-Q and R-P first; the remaining clues fix the gaps.")
S[11] = dict(raw=r"""Step 1: Compare the first pair
The first figure shows three symbols in a horizontal row (circle, cross, plus).
Step 2: Find the change
In the second figure the same three symbols stand in a vertical column, in the same order from top to bottom: circle, cross, plus.
Step 3: Apply the rule to the third figure
The third figure has &, @ and # in a horizontal row, so the answer must show &, @, # in a column from top to bottom.
Step 4: Check the options
Only the figure with & at the top, @ in the middle and # at the bottom keeps the order; the others mix it up.""", trick=r"Row turns into a column; the left-to-right order becomes top-to-bottom.")
S[12] = dict(raw=r"""Step 1: Track each corner element of the first figure
Dot-line (top-left) goes to the bottom-right, the "T" (top-right) goes to the top-left, the square-line (bottom-left) goes to the top-right, and the arrow (bottom-right) goes to the bottom-left.
Step 2: Write the rule
Top-left → bottom-right, top-right → top-left, bottom-left → top-right, bottom-right → bottom-left.
Step 3: Apply it to R, T, H, C
R (top-left) → bottom-right, T (top-right) → top-left, H (bottom-left) → top-right, C (bottom-right) → bottom-left.
Step 4: Answer
The new figure has T and H on top and C and R at the bottom (T H / C R).""", trick=r"Track every corner separately — the same moves apply to the letters R, T, H, C.")
S[18] = dict(raw=r"""Step 1: Follow the circle
The circle moves from the left side to the top-left, then to the top and then to the top-right — 45° clockwise each time.
Step 2: Follow the line
The line moves from the top-right corner to the top, then to the top-left and then to the left — 45° anticlockwise each time.
Step 3: Follow the shape
The inner shape alternates square, diamond, square, diamond, so the fifth figure has a square.
Step 4: Predict the fifth figure
Circle on the right side (one more 45° clockwise), line at the bottom-left corner (one more 45° anticlockwise), square shape — the first option fits.""", trick=r"Circle 45° clockwise, line 45° anticlockwise, shape alternates.")
S[19] = dict(raw=r"""Step 1: Count the triangles
1, 1, 2, 2 — each count appears twice, so the fifth figure has 3 triangles.
Step 2: Look at the corner arrows
Figures 1 and 3 have ↓ ↑ on top and ↑ ↓ at the bottom; figures 2 and 4 have them reversed. The arrow pattern alternates.
Step 3: Predict the fifth figure
It follows figure 1 and 3: ↓ ↑ on top, ↑ ↓ at the bottom, with 3 triangles.
Step 4: Check the options
The first option has 3 triangles but the wrong arrows; the last two have 4 triangles. Only the second option fits.""", trick=r"Triangles 1, 1, 2, 2, 3 and the arrow set alternates.")
S[13] = dict(raw=r"""Step 1: Study AF14 → EB196
Swap the letters (AF → FA), then the first goes back 1 (F → E) and the second goes forward 1 (A → B). The number is squared: \( 14^{2} = 196 \).
Step 2: Confirm with LT17 → SM289
Swap (TL), T − 1 = S, L + 1 = M; \( 17^{2} = 289 \) ✓.
Step 3: Apply to KO15
Swap (OK), O − 1 = N, K + 1 = L; \( 15^{2} = 225 \).
Step 4: Answer
KO15 → NL225.""", trick=r"Swap the letters, −1 / +1, and square the number.")
S[14] = dict(raw=r"""Step 1: Study KAR220 → LBS340
Each letter moves +1 (K → L, A → B, R → S) and the number increases by 120 (220 + 120 = 340).
Step 2: Confirm with RSV200 → STW320
R → S, S → T, V → W and 200 + 120 = 320 ✓.
Step 3: Apply to CRT280
C → D, R → S, T → U and 280 + 120 = 400.
Step 4: Answer
CRT280 → DSU400.""", trick=r"Each letter +1 and the number +120.")
S[15] = dict(raw=r"""Step 1: Find the rule in the first pair
\( 877 - 416 = 461 \).
Step 2: Confirm with the third pair
\( 1235 - 774 = 461 \) ✓, so the rule is "add 461".
Step 3: Apply the rule
\( 639 + 461 = 1100 \).
Step 4: Check the options
Only 1100 gives a difference of 461.""", trick=r"Same difference (+461) in every pair.")
S[16] = dict(raw=r"""Step 1: Compare CAME with EEJZ
C (3) → E (5) is +2, A (1) → E (5) is +4, M (13) → J (10) is −3, E (5) → Z (0 → 26) is −5.
Step 2: Confirm with ACRE → CGOZ
A → C (+2), C → G (+4), R (18) → O (15) (−3), E → Z (−5) ✓.
Step 3: Apply +2, +4, −3, −5 to GULL
G (7) + 2 = I, U (21) + 4 = Y, L (12) − 3 = I, L (12) − 5 = G.
Step 4: Answer
GULL is coded as IYIG.""", trick=r"Positions 1 to 4 move +2, +4, −3, −5.")
S[17] = dict(raw=r"""Step 1: Find the time passed
From 12 PM to 6 PM is 6 hours = 360 minutes.
Step 2: Count the 10-minute blocks
\( 360 \div 10 = 36 \) blocks.
Step 3: Find the total gain
\( 36 \times 5 = 180 \) seconds = 3 minutes.
Step 4: Add the gain
The fast clock shows 6:03:00 PM.""", trick=r"Gain = (minutes passed ÷ 10) × 5 seconds.")
S[20] = dict(raw=r"""Step 1: Write the first condition
Five years ago: \( \dfrac{L - 5}{M - 5} = \dfrac{1}{3} \), so \( M - 5 = 3L - 15 \), i.e. \( M = 3L - 10 \).
Step 2: Write the second condition
After three years: \( \dfrac{L + 3}{M + 3} = \dfrac{2}{5} \), so \( 5L + 15 = 2M + 6 \).
Step 3: Solve
\( 5L + 15 = 2(3L - 10) + 6 = 6L - 14 \), so L = 29 and \( M = 3 \times 29 - 10 = 77 \).
Step 4: Check and answer
\( 24 : 72 = 1 : 3 \) ✓ and \( 32 : 80 = 2 : 5 \) ✓. The present ages are in the ratio \( 29 : 77 \).""", trick=r"Write both ratios as equations in L and M, then substitute.")
