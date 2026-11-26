S = {}
S[1] = dict(raw=r"""Step 1: Find the differences
−598 → −607 is −9, −607 → −616 is −9, −616 → −625 is −9, −625 → −634 is −9.
Step 2: Spot the rule
Each term is 9 less than the one before it.
Step 3: Check the next terms
\( -634 - 9 = -643 \), but the series shows −644. The term after it, −652, is \( -643 - 9 \).
Step 4: Confirm
−652 − 9 = −661 ✓. So −644 is the wrong term; it should be −643.""", trick=r"Constant difference series: the one term that breaks the −9 pattern is wrong.")
S[2] = dict(raw=r"""Step 1: Find the differences
−16 → −12 is +4, −12 → −7 is +5, −7 → −1 is +6, −1 → 6 is +7, 6 → 14 is +8, 14 → 23 is +9.
Step 2: Spot the rule
The differences grow by 1 each time.
Step 3: Find the missing term
The next difference is +10: \( 23 + 10 = 33 \).
Step 4: Answer
The missing term is 33.""", trick=r"Differences +4, +5, +6 … — add one more each step.")
S[3] = dict(raw=r"""Step 1: Write the first letters
E (5), G (7), J (10), L (12), ?, Q (17), T (20), V (22): the gaps go +2, +3, +2, +3 …, so after L (12) comes \( 12 + 3 = 15 \) = O, and O + 2 = Q ✓.
Step 2: Write the second letters
F (6), D (4), A (1), W (23), ?, L (12), E (5), W (23).
Step 3: Find the gaps
F → D is −2, D → A is −3, A → W is −4 (1 − 4 = −3 → 23), so the next gap is −5: W (23) − 5 = 18 = R.
Step 4: Check and answer
R (18) − 6 = 12 = L ✓, L (12) − 7 = 5 = E ✓, E (5) − 8 = −3 → 23 = W ✓. The missing term is OR.""", trick=r"First letters +2, +3 alternately; second letters −2, −3, −4, −5 …")
S[4] = dict(raw=r"""Step 1: Write the first letters
R (18), T (20), X (24), Z (26), D (4 = 30), F (6 = 32), ?, L (12 = 38): the gaps go +2, +4, +2, +4, +2, so the next is +4: F (6) + 4 = 10 = J.
Step 2: Check the first letters
J (10) + 2 = 12 = L ✓, which is the last term.
Step 3: Write the second letters
D (4), X (24), R (18), L (12), F (6), Z (26), ?, N (14): each step is −6 (4 − 6 = −2 → 24, 6 − 6 = 0 → 26). So Z (26) − 6 = 20 = T.
Step 4: Answer
T (20) − 6 = 14 = N ✓. The missing term is JT.""", trick=r"First letters +2, +4 alternately; second letters always −6 (wrap past A).")
S[5] = dict(raw=r"""Step 1: Study the first set (GW, ES, CO)
First letters G (7) → E (5) → C (3): −2 each. Second letters W (23) → S (19) → O (15): −4 each.
Step 2: Confirm with (AR, YN, WJ)
A (1) → Y (25) → W (23): −2 each (1 − 2 = −1 → 25). R (18) → N (14) → J (10): −4 each ✓.
Step 3: Test the options
(UF, SB, QX): U (21) → S (19) → Q (17) is −2; F (6) → B (2) → X (2 − 4 = −2 → 24) is −4 ✓. (SQ, QO, MH): S → Q is −2 but Q → M is −4 ✗. (GP, EN, AK): E → A is −4 ✗. (HB, FZ, BW): F → B is −4 ✗.
Step 4: Answer
Only (UF, SB, QX) follows −2 on the first letters and −4 on the second letters.""", trick=r"Check the first letters first: they must fall by 2 every time.")
S[6] = dict(raw=r"""Step 1: Find the differences of the known terms
−355 → −367 is −12, −367 → −380 is −13, −380 → −394 is −14, −394 → −409 is −15, −409 → −425 is −16.
Step 2: Work backwards
The differences grow by 1, so before −12 come −11 and, before that, −10.
Step 3: Find the missing term
\( -334 - 10 = -344 \).
Step 4: Check
\( -344 - 11 = -355 \) ✓. The missing term is −344.""", trick=r"Read the pattern from the end where the terms are known, then step back.")
S[7] = dict(raw=r"""Step 1: Place M and K
N and M sit at the two ends. K is next to both J and M, so K sits next to M and J sits on K's other side.
Step 2: Try M at the left end
M K J _ N: then L must take the 4th seat, which is to the RIGHT of J — this breaks "L is to the left of J".
Step 3: Try M at the right end
N _ J K M: L takes the 2nd seat, which is to the left of J ✓.
Step 4: Answer
Order (left to right): N, L, J, K, M. J sits in the middle (3rd) seat.""", trick=r"Fix the end people first, then test both directions.")
S[8] = dict(raw=r"""Step 1: Take the fixed facts
O is the tallest. M is shorter only than Q and O, so M is 3rd tallest and Q is 2nd.
Step 2: Arrange N, P and R
P is taller than R but shorter than N, so N > P > R.
Step 3: Combine
O > Q > M > N > P > R.
Step 4: Answer
The boys taller than N are O, Q and M — 3 boys.""", trick=r"'Less than only X and Y' means exactly two people are above.")
S[9] = dict(raw=r"""Step 1: Compare the first pair
In the first figure the square is at the top, the small tick points right and the T-bar is at the bottom. In the second figure the square is on the left, the tick points up and the bar is on the right.
Step 2: Find the rule
Top → left, right → top, bottom → right: the figure is turned 90° anticlockwise.
Step 3: Apply the rule to the third figure
In the third figure the bar is at the top-left and the ball is at the bottom-right. Turned 90° anticlockwise, the top-left goes to the bottom-left and the bottom-right goes to the top-right.
Step 4: Pick the figure
The answer must have the ball at the top-right and the bar at the bottom-left — only figure 1 matches (figure 4 has them the other way round, which is a 180° turn of figure 1).""", trick=r"Track one end of the figure (the ball) through the same turn.")
S[10] = dict(raw=r"""Step 1: Compare the corners of the first pair
First figure: 2 (top-left), 1 (top-right), 3 (bottom-left), 4 (bottom-right). Second figure: 1, 2, 4, 3 — the two corners in each row change places.
Step 2: Compare the middle letters
MNOP becomes PMNO: the last letter moves to the front.
Step 3: Apply both rules to the third figure
Corners U, A, O, H become A, U, H, O. Middle 5698 becomes 8569.
Step 4: Pick the figure
The answer needs A U on top, 8569 in the middle and H O at the bottom — only figure 3 matches (figure 1 has 5869, figure 2 has O and U swapped, figure 4 has 8659).""", trick=r"Check the corners and the middle row separately.")
S[11] = dict(raw=r"""Step 1: Study the first pair QR75 → NO28
Q (17) → N (14) is −3, R (18) → O (15) is −3, and \( 75 - 47 = 28 \).
Step 2: Confirm with MN99 → JK52
M (13) → J (10) is −3, N (14) → K (11) is −3, and \( 99 - 47 = 52 \) ✓.
Step 3: Work backwards from BS46
Letters: B (2) + 3 = E (5), S (19) + 3 = V (22). Number: \( 46 + 47 = 93 \).
Step 4: Answer
The missing cluster is EV93 (check: E − 3 = B, V − 3 = S, 93 − 47 = 46 ✓).""", trick=r"Rule −3, −3, −47; to find the first term add them back.")
S[12] = dict(raw=r"""Step 1: Study KLP8 → FGV100
K (11) → F (6) is −5, L (12) → G (7) is −5, P (16) → V (22) is +6, and \( (8 + 2)^{2} = 100 \).
Step 2: Confirm with MSB5 → HNH49
M → H is −5, S → N is −5, B (2) → H (8) is +6, and \( (5 + 2)^{2} = 49 \) ✓.
Step 3: Apply to ZXO9
Z (26) − 5 = U (21), X (24) − 5 = S (19), O (15) + 6 = U (21), and \( (9 + 2)^{2} = 121 \).
Step 4: Answer
The cluster is USU121.""", trick=r"Letters −5, −5, +6; number → (n + 2)².")
S[13] = dict(raw=r"""Step 1: Study 2809 → 2761
\( 2809 - 2761 = 48 \), so the second number is 48 less.
Step 2: Confirm with 2487 → 2439
\( 2487 - 2439 = 48 \) ✓.
Step 3: Work backwards from 5520
The missing number minus 48 = 5520, so it is \( 5520 + 48 = 5568 \).
Step 4: Answer
The missing number is 5568.""", trick=r"Constant difference 48 — add it back to get the first number.")
S[14] = dict(raw=r"""Step 1: Study 27 → 841
\( 841 = 29^{2} \) and \( 29 = 27 + 2 \).
Step 2: Confirm with 21 → 529
\( 529 = 23^{2} \) and \( 23 = 21 + 2 \) ✓.
Step 3: Apply to 17
\( (17 + 2)^{2} = 19^{2} = 361 \).
Step 4: Answer
The missing number is 361.""", trick=r"Number → (number + 2)².")
S[15] = dict(raw=r"""Step 1: Study KETO → PIPJ
K (11) → P (16): K and P are opposite letters (11 + 16 = 27). E (5) → I (9) is +4, T (20) → P (16) is −4, O (15) → J (10) is −5.
Step 2: Confirm with DAMN → WEII
D (4) → W (23): opposite letters (4 + 23 = 27). A → E is +4, M (13) → I (9) is −4, N (14) → I (9) is −5 ✓.
Step 3: Apply to HISS
H (8) → opposite = 27 − 8 = 19 = S; I (9) + 4 = 13 = M; S (19) − 4 = 15 = O; S (19) − 5 = 14 = N.
Step 4: Answer
HISS is coded as SMON.""", trick=r"Opposite letters add up to 27; then +4, −4, −5.")
S[16] = dict(raw=r"""Step 1: Study CRANK → FWZLG
C (3) → F (6) is +3, R (18) → W (23) is +5, A (1) → Z (26) is −1, N (14) → L (12) is −2, K (11) → G (7) is −4.
Step 2: Confirm with FEMME → IJLKA
F → I +3, E → J +5, M → L −1, M → K −2, E (5) → A (1) −4 ✓.
Step 3: Apply to GUTSY
G + 3 = J, U (21) + 5 = Z (26), T (20) − 1 = S, S (19) − 2 = Q, Y (25) − 4 = U (21).
Step 4: Answer
GUTSY is coded as JZSQU.""", trick=r"Pattern +3, +5, −1, −2, −4 letter by letter.")
S[17] = dict(raw=r"""Step 1: First letters
H, ?, L, N, P: H (8), L (12), N (14), P (16) go up by 2, so the missing first letter is J (10).
Step 2: Second letters
N (14), ?, H (8), E (5), B (2) go down by 3, so the missing one is K (11).
Step 3: Numbers
108, ?, 276, 360, 444 go up by 84: \( 108 + 84 = 192 \).
Step 4: Answer
The missing term is JK192 (check: 192 + 84 = 276 ✓).""", trick=r"Split each term into its letters and its number and solve each part.")
S[18] = dict(raw=r"""Step 1: First letters
Z, A, B, C: each moves +1 (Z wraps to A), so next is D.
Step 2: Second letters
B, A, Z, Y: each moves −1, so next is X.
Step 3: Third letters and numbers
U, V, W, X → next is Y. Numbers 500, 708, 916, 1124 rise by 208: \( 1124 + 208 = 1332 \).
Step 4: Answer
The next term is DXY1332.""", trick=r"Three letter tracks (+1, −1, +1) and a number track (+208).")
S[19] = dict(raw=r"""Step 1: Use the overlap formula
Between H and H + 1 o'clock the hands overlap \( \dfrac{60H}{11} \) minutes after H.
Step 2: Put H = 6
\( \dfrac{60 \times 6}{11} = \dfrac{360}{11} \) minutes.
Step 3: Convert
\( \dfrac{360}{11} \approx 32.73 \) minutes, i.e. about 32 minutes 44 seconds.
Step 4: Answer
The hands overlap at about 6:33 AM.""", trick=r"Overlap time after H o'clock = 60H/11 minutes.")
S[20] = dict(raw=r"""Step 1: Find the time passed
From 10 AM to 8 PM is 10 hours = \( 10 \times 60 = 600 \) minutes.
Step 2: Count the 4-minute blocks
\( 600 \div 4 = 150 \) blocks.
Step 3: Find the time gained
\( 150 \times 3 = 450 \) seconds = 7 minutes 30 seconds.
Step 4: Answer
The clock runs fast, so at 8 PM it shows 8:07:30 PM.""", trick=r"Gain = (minutes passed ÷ 4) × 3 seconds.")
