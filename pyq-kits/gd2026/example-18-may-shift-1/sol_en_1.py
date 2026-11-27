S = {}
S[1] = dict(raw=r"""Step 1: Write the first letters
G (7), D (4), A (1), ?, U (21), R (18), O (15), L (12): each step is −3, so the missing first letter is A (1) − 3 = −2 → 24 = X.
Step 2: Write the second letters
V (22), R (18), M (13), ?, Z (26), R (18), I (9), Y (25).
Step 3: Find the gaps of the second letters
The gaps are −4, −5, then −6, −7, −8, −9, −10: M (13) − 6 = 7 = G.
Step 4: Answer and check
The missing term is XG. Check: G (7) − 7 = 0 → Z ✓, Z − 8 = R ✓, R − 9 = I ✓, I − 10 = −1 → Y ✓.""", trick=r"First letters −3; second letters −4, −5, −6 … (wrap past A to Z).")
S[2] = dict(raw=r"""Step 1: Write the first letters
?, S (19), W (23), Z (26), D (30 → 4), G (7), K (11), N (14): the gaps go +4, +3, +4, +3, +4, +3.
Step 2: Find the first letter of the missing term
The gap before S must be +3, so the first letter is S (19) − 3 = 16 = P.
Step 3: Write the second letters
?, N (14), J (10), E (5), Y (25), R (18), J (10), A (1): the gaps are −4, −5, −6, −7, −8, −9, so the gap before N is −3 and the second letter is N (14) + 3 = 17 = Q.
Step 4: Answer and check
The missing term is PQ. Check: P + 3 = S ✓ and Q − 3 = N ✓.""", trick=r"First letters +3, +4 alternately; second letters −3, −4, −5 …")
S[3] = dict(raw=r"""Step 1: Write the first letters
O (15), R (18), V (22), ?, C (29 → 3), F (32 → 6), J (36 → 10), M (39 → 13): the gaps alternate +3, +4.
Step 2: Find the first letter
After +4 (R → V) comes +3: V (22) + 3 = 25 = Y, and Y + 4 = 29 → C ✓.
Step 3: Find the second letter
Second letters S (19), P (16), L (12), ?, A (1), T (20), L (12), C (3) fall by 3, 4, then 5, 6, 7, 8, 9: L (12) − 5 = 7 = G, and G − 6 = 1 = A ✓.
Step 4: Answer
The missing term is YG; then A − 7 = −6 → T ✓, T − 8 = L ✓, L − 9 = C ✓.""", trick=r"First letters +3, +4 alternately; second letters −3, −4, −5 …")
S[4] = dict(raw=r"""Step 1: Study the first set (AT, CV, GA)
First letters A (1) → C (3) → G (7): +2, then +4. Second letters T (20) → V (22) → A (27 → 1): +2, then +5.
Step 2: Confirm with (BZ, DB, HG)
B → D → H is +2, +4 and Z (26) → B (28 → 2) → G (33 → 7) is +2, +5 ✓.
Step 3: Test the options
(YO, AQ, EV): Y (25) → A (27) → E (31) is +2, +4 and O (15) → Q (17) → V (22) is +2, +5 ✓. In (DO, FP, HX), (IZ, KB, MI) and (CA, EF, GJ) the first letters go +2, +2 ✗.
Step 4: Answer
Only (YO, AQ, EV) follows +2, +4 on the first letters and +2, +5 on the second letters.""", trick=r"Read column-wise: first letters +2, +4; second letters +2, +5.")
S[5] = dict(raw=r"""Step 1: Find the day on 1 January 1919
1 January 1900 was a Monday. From 1900 to 1918 there are 19 years with 4 leap years (1904, 1908, 1912, 1916), so the odd days are \( 19 + 4 = 23 \) → 2. Monday + 2 = Wednesday.
Step 2: Find the day on 1 August 1919
Odd days from January to July (1919 is not a leap year): \( 3 + 0 + 3 + 2 + 3 + 2 + 3 = 16 \) → 2. Wednesday + 2 = Friday.
Step 3: Check August
A 31-day month has its first 3 weekdays 5 times: Friday, Saturday and Sunday. So August 1919 had 5 Saturdays ✓.
Step 4: Check December
Odd days from August to November: \( 3 + 2 + 3 + 2 = 10 \) → 3, so 1 December was Friday + 3 = Monday. December had 5 Mondays, Tuesdays and Wednesdays, but only 4 Saturdays. So only August qualifies.""", trick=r"A 31-day month has 5 Saturdays only if it begins on Thursday, Friday or Saturday.")
S[6] = dict(raw=r"""Step 1: Study the first pair
The first figure has 4 vertical lines inside a square; the second figure is a hexagon, which has 6 sides.
Step 2: Find the rule
Number of sides = number of lines + 2 (\( 4 + 2 = 6 \)).
Step 3: Apply it to the third figure
The third figure has 3 vertical lines, so the missing figure must have \( 3 + 2 = 5 \) sides.
Step 4: Answer
The pentagon (5 sides) fits; the circle, the triangle (3 sides) and the rectangle (4 sides) do not.""", trick=r"Lines + 2 = sides of the shape: 4 lines → hexagon, so 3 lines → pentagon.")
S[7] = dict(raw=r"""Step 1: Track the corner elements of the first pair
Z (top-left) goes to bottom-right, P (top-right) to bottom-left, B (bottom-left) to top-right and N (bottom-right) to top-left: each corner moves to the opposite corner (180°).
Step 2: Track the middle (edge) elements
Top-middle goes to right-middle, left-middle to top-middle, right-middle to bottom-middle and bottom-middle to left-middle: the edge elements move 90° clockwise.
Step 3: Apply the rule to the third figure (7 4 2 / F _ 9 / 3 8 5)
Corners: 5 goes top-left, 3 top-right, 2 bottom-left, 7 bottom-right. Edges: F goes to the top, 4 to the right, 9 to the bottom, 8 to the left.
Step 4: Answer
The missing figure reads 5 F 3 / 8 _ 4 / 2 9 7.""", trick=r"Corners jump to the opposite corner; middles turn one step clockwise.")
S[8] = dict(raw=r"""Step 1: Study TK460 → SN360
T (20) → S (19) is −1, K (11) → N (14) is +3, and \( 460 - 100 = 360 \).
Step 2: Confirm with JQ210 → IT110
J (10) → I (9) is −1, Q (17) → T (20) is +3, and \( 210 - 100 = 110 \) ✓.
Step 3: Apply to PR320
P (16) − 1 = 15 = O, R (18) + 3 = 21 = U, and \( 320 - 100 = 220 \).
Step 4: Answer
The missing cluster is OU220.""", trick=r"First letter −1, second letter +3, number −100.")
S[9] = dict(raw=r"""Step 1: Study LPR110 → KOQ210
L → K, P → O, R → Q: every letter moves −1, and \( 110 + 100 = 210 \).
Step 2: Confirm with ZKW90 → YJV190
Z → Y, K → J, W → V (−1 each) and \( 90 + 100 = 190 \) ✓.
Step 3: Apply to PRT40
P → O, R → Q, T → S, and \( 40 + 100 = 140 \).
Step 4: Answer
The missing cluster is OQS140.""", trick=r"Every letter −1, number +100.")
S[10] = dict(raw=r"""Step 1: Study the first pair
\( 3249 + 40 = 3289 \).
Step 2: Confirm with the second pair
\( 3658 + 40 = 3698 \) ✓, so the second number = first number + 40.
Step 3: Work backwards
The missing first number + 40 = 8635, so it is \( 8635 - 40 = 8595 \).
Step 4: Check
\( 8595 + 40 = 8635 \) ✓.""", trick=r"Each pair differs by +40 — subtract 40 from 8635.")
S[11] = dict(raw=r"""Step 1: Study 523 → 1050
\( 523 \times 2 = 1046 \) and \( 1046 + 4 = 1050 \).
Step 2: Confirm with 513 → 1030
\( 513 \times 2 + 4 = 1026 + 4 = 1030 \) ✓. The rule is second = \( 2 \times \) first + 4.
Step 3: Work backwards from 1836
\( 2 \times ? + 4 = 1836 \Rightarrow 2 \times ? = 1832 \Rightarrow ? = 916 \).
Step 4: Check
\( 916 \times 2 + 4 = 1836 \) ✓.""", trick=r"Double and add 4; reverse it: subtract 4, then halve.")
S[12] = dict(raw=r"""Step 1: Compare BLUSH with FQTPC
B → F (+4), L → Q (+5), U → T (−1), S → P (−3), H → C (−5).
Step 2: Confirm with GOATS → KTZQN
G → K (+4), O → T (+5), A → Z (−1), T → Q (−3), S → N (−5) ✓.
Step 3: Apply +4, +5, −1, −3, −5 to WOODS
W (23) + 4 = 27 → A, O (15) + 5 = 20 = T, O − 1 = N, D (4) − 3 = 1 = A, S (19) − 5 = 14 = N.
Step 4: Answer
WOODS is coded as ATNAN.""", trick=r"Position-wise shifts +4, +5, −1, −3, −5.")
S[13] = dict(raw=r"""Step 1: Check the numbers
1331 = \( 11^{3} \), 1728 = \( 12^{3} \), 2197 = \( 13^{3} \), 2744 = \( 14^{3} \), 3375 = \( 15^{3} \); the next should be \( 16^{3} = 4096 \), but the last term has 4913 = \( 17^{3} \).
Step 2: Check the first letters
M (13), P (16), S (19), V (22), Y (25): +3 each, so the next should be 28 → B, not C.
Step 3: Check the second letters
X (24), R (18), L (12), F (6), Z (0 → 26): −6 each, so the next should be T (20), not S.
Step 4: Answer
The wrong term is CS4913; the correct term would be BT4096. Every other term fits all three patterns.""", trick=r"Letters +3 and −6, numbers 11³, 12³, 13³ … — only the last term breaks all three.")
S[14] = dict(raw=r"""Step 1: First letters
K (11), ?, G (7), E (5), C (3): −2 each, so the missing first letter is I (9).
Step 2: Second letters
M (13), ?, G (7), D (4), A (1): −3 each, so the missing second letter is J (10).
Step 3: Third letters
Y (25), ?, Q (17), M (13), I (9): −4 each, so the missing third letter is U (21).
Step 4: Numbers
80, ?, 180, 270, 405: each is 1.5 times the one before (\( 180 \times 1.5 = 270 \), \( 270 \times 1.5 = 405 \)), so the missing number is \( 80 \times 1.5 = 120 \). The term is IJU120.""", trick=r"Letters −2, −3, −4 column-wise; numbers × 1.5.")
S[15] = dict(raw=r"""Step 1: Use the formula
Angle = \( \left| 30H - \dfrac{11}{2}M \right| \), where H = hours and M = minutes.
Step 2: Put in the values
At 5:05, H = 5 and M = 5: \( 30 \times 5 = 150 \) and \( \dfrac{11}{2} \times 5 = 27.5 \).
Step 3: Subtract
\( 150 - 27.5 = 122.5 \).
Step 4: Answer
The angle is \( 122.5^{\circ} \) (it is less than \( 180^{\circ} \), so it is the smaller angle).""", trick=r"θ = |30H − 5.5M| = 150 − 27.5.")
S[16] = dict(raw=r"""Step 1: Use the formula
Angle = \( \left| 30H - \dfrac{11}{2}M \right| \).
Step 2: Put in the values
At 7:45, \( 30 \times 7 = 210 \) and \( \dfrac{11}{2} \times 45 = 247.5 \).
Step 3: Subtract
\( \left| 210 - 247.5 \right| = 37.5 \).
Step 4: Answer
The angle is \( 37.5^{\circ} \).""", trick=r"θ = |30H − 5.5M| = |210 − 247.5|.")
S[17] = dict(raw=r"""Step 1: Note what stays fixed
The inner frame turns upside down every time (open at the top, then open at the bottom). On each of its four sides there is a small semicircle that is either a bump (curving outward) or a cup (curving inward).
Step 2: Track the marks from one figure to the next
Figure 1 → 2: only the top mark changes. Figure 2 → 3: only the left mark changes. Figure 3 → 4: only the bottom mark changes.
Step 3: Find the next change
The changes go top → left → bottom, i.e. anticlockwise, so in the fifth figure the right mark changes from a bump to a cup.
Step 4: Answer
The fifth figure is open at the top with an inward-curving mark at the top, a bump on the left, and cups on the right and at the bottom — the only option with all four marks right.""", trick=r"One mark changes per step, moving anticlockwise: top, left, bottom, then right.")
S[18] = dict(raw=r"""Step 1: Record the shaded half of each circle in figure 1
Top-left: upper half; top-right: left half; bottom-left: right half; bottom-right: lower half.
Step 2: Track the changes
Figure 1 → 2: only the top-left circle changes (upper → lower half). Figure 2 → 3: only the top-right circle changes (left → right half). Figure 3 → 4: only the bottom-left circle changes (right → left half).
Step 3: Find the next change
The order is top-left, top-right, bottom-left, so next the bottom-right circle changes: its shading flips from the lower half to the upper half.
Step 4: Answer
The fifth figure has top-left lower half, top-right right half, bottom-left left half and bottom-right upper half shaded.""", trick=r"One circle flips its shading per step, in reading order.")
S[19] = dict(raw=r"""Step 1: Follow one letter
D enters at the bottom-left cell, then moves to the middle-left cell (mirrored), then to the top-left cell (normal), then to the top-middle cell (mirrored). Each step it moves one cell clockwise along the edge and is mirrored.
Step 2: Follow the others
E enters in figure 2 and follows D one step behind; 6 enters in figure 3 and P in figure 4, each following the same path.
Step 3: Move every symbol one more step
D → top-right (normal D), E → top-middle (mirrored E), 6 → top-left (normal 6), P → middle-left (mirrored P), and a new letter Q enters at the bottom-left.
Step 4: Answer
The fifth figure reads 6, mirrored E, D in the top row, mirrored P in the middle-left cell and Q at the bottom-left.""", trick=r"Letters enter at the bottom-left, march clockwise one cell per step and flip each step.")
S[20] = dict(raw=r"""Step 1: Let the present ages be x and 5x
M = x and S = 5x, since the ratio is \( 1 : 5 \).
Step 2: Use the age difference
\( 5x - x = 8 \Rightarrow 4x = 8 \Rightarrow x = 2 \). So M = 2 years and S = 10 years.
Step 3: Add 7 years
M = \( 2 + 7 = 9 \) and S = \( 10 + 7 = 17 \).
Step 4: Answer
The ratio after 7 years is \( 9 : 17 \).""", trick=r"Ratio difference 4 parts = 8 years → 1 part = 2; ages 2 and 10.")
