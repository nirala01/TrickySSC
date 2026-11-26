S = {}
S[1] = dict(raw=r"""Step 1: Write the letters as positions
V = 22, T = 20, N = 14, L = 12, F = 6, ? , X = 24, V = 22.
Step 2: Find the gaps
22 → 20: −2; 20 → 14: −6; 14 → 12: −2; 12 → 6: −6. The gaps alternate −2, −6.
Step 3: Find the missing letter
The next gap is −2: 6 − 2 = 4 = D.
Step 4: Check
D (4) − 6 = −2 → 24 = X ✓ and X (24) − 2 = 22 = V ✓, so the missing letter is D.""", trick=r"Alternate −2, −6; wrap from A back to Z when the count goes below 1.")
S[2] = dict(raw=r"""Step 1: Find the rule in RMZ → PKX
R (18) → P (16): −2; M (13) → K (11): −2; Z (26) → X (24): −2.
Step 2: Confirm with HQT → FOR
H (8) → F (6), Q (17) → O (15), T (20) → R (18): −2 on every letter ✓.
Step 3: Apply the rule to CPI
C (3) − 2 = 1 = A; P (16) − 2 = 14 = N; I (9) − 2 = 7 = G.
Step 4: Answer
CPI is related to ANG.""", trick=r"Every letter moves 2 steps back.")
S[3] = dict(raw=r"""Step 1: Find the rule in AI → YB
A (1) → Y (25): 1 − 2 = −1 → 25, so −2. I (9) → B (2): −7.
Step 2: Confirm with SP → QI
S (19) → Q (17): −2; P (16) → I (9): −7 ✓.
Step 3: Apply the rule to WL
W (23) − 2 = 21 = U; L (12) − 7 = 5 = E.
Step 4: Answer
WL is related to UE.""", trick=r"First letter −2, second letter −7.")
S[4] = dict(raw=r"""Step 1: Pattern of the first letters
Q (17) → N (14) → ? → H (8) → E (5) → B (2) → Y (25) → V (22): −3 each time, so the missing first letter is 14 − 3 = 11 = K.
Step 2: Pattern of the second letters
T (20) → S (19): −1; then ?; N (14) → J (10): −4; J → E (5): −5; E → Y (5 − 6 = −1 → 25): −6; Y → R (18): −7.
Step 3: Find the missing second letter
The gaps are −1, −2, −3, −4 …, so the missing letter is 19 − 2 = 17 = Q; check Q (17) − 3 = 14 = N ✓.
Step 4: Answer
The missing cluster is KQ.""", trick=r"First letter −3 throughout; second letter −1, −2, −3, −4 ….")
S[5] = dict(raw=r"""Step 1: Find the rule in (XG, VC, TY)
First letters X (24) → V (22) → T (20): −2, −2. Second letters G (7) → C (3) → Y (3 − 4 = −1 → 25): −4, −4.
Step 2: Confirm with (RB, PX, NT)
R → P → N: −2, −2 ✓. B (2) → X (2 − 4 = −2 → 24) → T (20): −4, −4 ✓.
Step 3: Test the options
(QM, OI, ME): Q (17) → O (15) → M (13) is −2, −2 ✓; M (13) → I (9) → E (5) is −4, −4 ✓.
Step 4: Reject the rest
(ZP, AM, WH) has Z → A (+1); (TN, OK, KE) has T → O (−5); (IZ, EA, AU) has I → E (−4). Only (QM, OI, ME) follows the rule.""", trick=r"First letters −2, second letters −4 in every set.")
S[6] = dict(raw=r"""Step 1: Check whether 2002 is a leap year
2002 is not divisible by 4, so it is not a leap year and February has 28 days.
Step 2: Count the weeks
28 days = exactly 4 weeks, so every day of the week occurs exactly 4 times.
Step 3: Count Mondays and Wednesdays
Mondays = 4 and Wednesdays = 4.
Step 4: Find the product
\( 4 \times 4 = 16 \).""", trick=r"A 28-day February has every weekday exactly 4 times.")
S[7] = dict(raw=r"""Step 1: Rule for identical calendars
Two years have the same calendar if both are of the same type (both leap or both ordinary) and the odd days between them add up to a multiple of 7.
Step 2: Reject pairs of different types
1972 is a leap year but 1978 is not; 1960 is a leap year but 1967 is not — rejected.
Step 3: Count odd days from 1966 to 1976
11 years with 3 leap years (1968, 1972, 1976): \( 8 \times 1 + 3 \times 2 = 14 \) odd days = 2 weeks, remainder 0 ✓.
Step 4: Check 1965 and 1977
1965 to 1976 is 12 years with 3 leap years: \( 9 + 6 = 15 \) odd days, remainder 1 — not identical. So 1966 and 1977 have identical calendars.""", trick=r"Ordinary year = 1 odd day, leap year = 2; the total must be a multiple of 7.")
S[8] = dict(raw=r"""Step 1: Find the differences
330 → 421: +91; 603 → 694: +91; 694 → 785: +91.
Step 2: Spot the pattern
Every term is 91 more than the one before it.
Step 3: Find the missing term
\( 421 + 91 = 512 \).
Step 4: Check
\( 512 + 91 = 603 \) ✓, so the missing term is 512.""", trick=r"Constant gap +91.")
S[9] = dict(raw=r"""Step 1: Place S
All five face north, so right means towards the right end. Only one girl is to the right of S, so S is 4th from the left.
Step 2: Use the H clue
H is immediately right of R and immediately left of V, so R, H, V sit together in that order.
Step 3: Fit R, H, V
The only three adjacent seats left of S are 1, 2, 3, so R = 1, H = 2, V = 3, and T takes seat 5.
Step 4: Answer
Order from the left: R, H, V, S, T. S is fourth from the left end.""", trick=r"“Only one to the right” fixes the second seat from the right end.")
S[10] = dict(raw=r"""Step 1: Set the directions
Facing the centre, left = clockwise and right = anticlockwise. Number the seats 0 to 6 clockwise and put S at 0.
Step 2: Place Q and V
Going left (clockwise) from S, one student sits between S and Q, so Q = 2. V is fourth to the right (anticlockwise) of Q: 2 − 4 = −2 → V = 5.
Step 3: Place U, P and T
P is fourth to the right of U. If U = 3, P = 6 and T must take 1 or 4 — both next to S or V, not allowed. So U = 1, P = 4, and T goes to 3 (not next to V or S); R = 6.
Step 4: Count between V and U
From U (1) going right (anticlockwise): S (0), R (6), then V (5). So 2 students (S and R) sit between V and U.""", trick=r"Facing the centre: right = anticlockwise. Fix S, then Q and V, and test the two places for U.")
S[11] = dict(raw=r"""Step 1: Compare the first pair
The first figure has 2 unshaded diamonds; the second has 4 shaded (black) diamonds.
Step 2: Write the rule
The number of shapes doubles and the shapes become shaded.
Step 3: Apply the rule to the third figure
The third figure has 1 unshaded arch (half-round shape), so the answer must have 2 shaded arches.
Step 4: Match with the options
Figure 1 has exactly 2 black arches; the others have 4, 5 or 7 arches. So figure 1 is the answer.""", trick=r"Count first (×2), then check shading (open → black).")
S[12] = dict(raw=r"""Step 1: Compare the first pair
The first figure is a square (4 sides) with one vertical line and a half horizontal line on the left. The second is a pentagon (5 sides) with the same two inner lines.
Step 2: Write the rule
The outer shape gets one more side; the inner lines stay exactly the same.
Step 3: Apply the rule to the third figure
The pentagon (5 sides) with a vertical line and a left half-line must become a hexagon (6 sides) with a vertical line and a left half-line.
Step 4: Match with the options
Figure 1 shows a hexagon with a vertical line and only the left half of a horizontal line; figures 2, 3 and 4 have extra lines. So figure 1 is the answer.""", trick=r"Sides +1, inner lines copied as they are.")
S[18] = dict(raw=r"""Step 1: Track the main shape
The cross stands upright in figures 1 and 3 and is turned like an X in figures 2 and 4 — it turns 45° every time. So figure 5 has an upright cross.
Step 2: Track the black dot
The dot moves from top (1) to top-right (2), right (3) and bottom-right (4) — 45° clockwise each time. So in figure 5 it is at the bottom.
Step 3: Track the small circle
The circle is in the left arm (1), the upper-right arm (2), the bottom arm (3) and the upper-left arm (4) — 135° clockwise each time. So in figure 5 it is in the right arm.
Step 4: Match with the options
Figure 2 has an upright cross, the circle in the right arm and the dot at the bottom. So figure 2 is the answer.""", trick=r"Track each element separately: shape turns 45°, dot 45° clockwise, circle 135° clockwise.")
S[19] = dict(raw=r"""Step 1: Count the + signs
The figures have 2, 4, 6 and 8 plus signs.
Step 2: Spot the pattern
The count increases by 2 every time.
Step 3: Find the next count
\( 8 + 2 = 10 \) plus signs.
Step 4: Match with the options
Figure 1 has 12, figure 2 has 9, figure 3 has 11 and figure 4 has 10 (4 + 4 + 2) plus signs. So figure 4 is the answer.""", trick=r"Count the signs row by row: 2, 4, 6, 8, 10.")
S[13] = dict(raw=r"""Step 1: Find the rule in WF851 → UH823
W (23) → U (21): −2; F (6) → H (8): +2; 851 → 823: −28.
Step 2: Confirm with QW270 → OY242
Q (17) → O (15): −2; W (23) → Y (25): +2; 270 → 242: −28 ✓.
Step 3: Apply the rule to XS115
X (24) − 2 = 22 = V; S (19) + 2 = 21 = U; \( 115 - 28 = 87 \).
Step 4: Answer
XS115 is related to VU87.""", trick=r"Letters −2 and +2, number −28.")
S[14] = dict(raw=r"""Step 1: Find the rule in KPS15 → JOR196
K → J, P → O, S → R: each letter −1. And \( 196 = 14^{2} = (15 - 1)^{2} \).
Step 2: Confirm with ZYO17 → YXN256
Z → Y, Y → X, O → N: −1 ✓. \( 256 = 16^{2} = (17 - 1)^{2} \) ✓.
Step 3: Apply the rule to ACD13
A − 1 = Z (wrap-around), C − 1 = B, D − 1 = C; \( (13 - 1)^{2} = 12^{2} = 144 \).
Step 4: Answer
ACD13 is related to ZBC144.""", trick=r"Each letter −1; number → (n − 1)².")
S[15] = dict(raw=r"""Step 1: Find the rule in 16 → 5832
\( 5832 = 18^{3} = (16 + 2)^{3} \).
Step 2: Confirm with 22 → 13824
\( 13824 = 24^{3} = (22 + 2)^{3} \) ✓.
Step 3: Apply the rule to 27
\( (27 + 2)^{3} = 29^{3} = 29 \times 29 \times 29 = 841 \times 29 = 24389 \).
Step 4: Answer
27 is related to 24389.""", trick=r"Add 2, then cube: 18³, 24³, 29³.")
S[16] = dict(raw=r"""Step 1: Compare NANS with SZKN
N (14) → S (19): +5; A (1) → Z (26): −1; N (14) → K (11): −3; S (19) → N (14): −5.
Step 2: Confirm with TARE → YZOZ
T → Y: +5; A → Z: −1; R (18) → O (15): −3; E (5) → Z (0 → 26): −5 ✓.
Step 3: Apply +5, −1, −3, −5 to ITCH
I (9) + 5 = 14 = N; T (20) − 1 = 19 = S; C (3) − 3 = 0 → 26 = Z; H (8) − 5 = 3 = C.
Step 4: Answer
ITCH is coded as NSZC.""", trick=r"Shifts by position: +5, −1, −3, −5.")
S[17] = dict(raw=r"""Step 1: Note the error
At 1 AM the watch is 4 minutes = 240 seconds slow.
Step 2: Find the time to make it up
It gains 8 seconds every hour, so it needs \( 240 \div 8 = 30 \) hours to show the correct time.
Step 3: Add the hours
1 AM + 24 hours = 1 AM the next day; + 6 more hours = 7 AM.
Step 4: Answer
The watch will show the correct time at 7:00 AM.""", trick=r"Hours needed = total error ÷ gain per hour.")
S[20] = dict(raw=r"""Step 1: Write the ages 8 years ago
Let L − 8 = 5k and M − 8 = 6k, so L = 5k + 8 and M = 6k + 8.
Step 2: Use the ratio after 5 years
\( \dfrac{5k + 13}{6k + 13} = \dfrac{6}{7} \Rightarrow 35k + 91 = 36k + 78 \Rightarrow k = 13 \).
Step 3: Find the present ages
L = \( 5 \times 13 + 8 = 73 \) and M = \( 6 \times 13 + 8 = 86 \).
Step 4: Check and answer
8 years ago: 65 and 78 = \( 5 : 6 \) ✓; after 5 years: 78 and 91 = \( 6 : 7 \) ✓. The present ratio is \( 73 : 86 \).""", trick=r"Write both past ages with one multiplier k, then use the second ratio to find k.")
