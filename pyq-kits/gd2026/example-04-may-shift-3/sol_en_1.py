S = {}
S[1] = dict(raw=r"""Step 1: Study MY → PE
M (13) + 3 = P (16) and Y (25) + 6 = 31, which wraps round to E (31 − 26 = 5). So the first letter moves 3 ahead and the second letter 6 ahead.
Step 2: Confirm with QZ → TF
Q (17) + 3 = T (20) and Z (26) + 6 = 32 → F (6) ✓ — the same +3, +6 rule.
Step 3: Work back from UD
The missing cluster must give U and D after +3 and +6. First letter = U (21) − 3 = R (18). Second letter = D (4) − 6 = −2 → 24 = X.
Step 4: Answer and check
The missing cluster is RX. Check: R + 3 = U and X + 6 = D ✓. RY gives U and E, SX gives V and D, SY gives V and E — all fail.""", trick=r"Find the shift from a complete pair (+3, +6), then go backwards from the given cluster.")
S[2] = dict(raw=r"""Step 1: Read the first set (JP, EI, ZB)
First letters J → E → Z move 5 back each time (E − 5 wraps round to Z). Second letters P → I → B move 7 back each time.
Step 2: Confirm with (MO, HH, CA)
M → H → C is −5, −5 and O → H → A is −7, −7 ✓
Step 3: Test the options
(YM, TF, OY): Y → T → O is −5, −5 and M → F → Y is −7, −7 (F − 7 wraps round to Y) ✓
(TT, LO, EH) starts T → L (−8); (ZH, VC, OV) starts Z → V (−4); (HM, DH, WA) starts H → D (−4) — all break the rule.
Step 4: Answer
The set (YM, TF, OY) follows the same −5, −7 rule.""", trick=r"Check first letters and second letters separately — here −5 and −7.")
S[3] = dict(raw=r"""Step 1: Fix A and D
All face north, so their right is our right. Seats are 1 to 7 from the left. D is fifth to the right of A and D is not at an end, so A = seat 1 and D = seat 6 (A at 2 would push D to seat 7, an end).
Step 2: Place F and B
F is fourth from the left = seat 4. Two boys sit between F and B, so B is at seat 1 or 7; seat 1 is A, so B = seat 7.
Step 3: Place G and E
Seats 2, 3 and 5 are left for C, G and E. Two boys between G and E means they sit at 2 and 5. G is not next to F (seat 4), so G cannot be at 5 → G = 2, E = 5.
Step 4: Answer
Order: A, G, C, F, E, D, B. C is at seat 3 — third from the left end.""", trick=r"Start with the clue that fixes an end seat (D not at an end) — it locks A at seat 1.")
S[4] = dict(raw=r"""Step 1: Fix Q and R
No one is to the right of Q, so Q is at the right end = seat 7. R is fourth to the left of Q → seat 3.
Step 2: Place W
W is second to the left of R → seat 1.
Step 3: Place U and T
Seats 2, 4, 5 and 6 are left. T is fourth to the right of U, so the only pair is U = 2, T = 6. P is not second to the right of U (seat 4), so P = 5 and S = 4.
Step 4: Count
Order: W, U, R, S, P, T, Q. To the right of R are S, P, T and Q → 4 boys.""", trick=r"Seats to the right of seat k in a row of 7 = 7 − k = 7 − 3 = 4.")
S[5] = dict(raw=r"""Step 1: Write the numbers
Let the three consecutive odd numbers be \( x - 2,\; x,\; x + 2 \).
Step 2: Form the equation
\( (x - 2) + x + (x + 2) = 3x = 111 \)
Step 3: Solve
\( x = \dfrac{111}{3} = 37 \), so the numbers are 35, 37 and 39.
Step 4: Answer and check
Largest number = 39. Check: \( 35 + 37 + 39 = 111 \) ✓""", trick=r"Middle number = sum ÷ 3 = 37; largest = middle + 2 = 39.")
S[6] = dict(raw=r"""Step 1: Recall the formula
\( \text{Average} = \dfrac{\text{Sum of the numbers}}{\text{How many numbers}} \)
Step 2: Add the numbers
\( 15 + 18 + 19 + 26 + 30 = 108 \)
Step 3: Divide by the count
There are 5 numbers: \( \dfrac{108}{5} = 21.6 \)
Step 4: Answer
The average is 21.6.""", trick=r"Divide by 5 quickly: multiply by 2 and divide by 10 → 108 × 2 = 216 → 21.6.")
S[7] = dict(raw=r"""Step 1: First statement
Ajay is older than Bharat but younger than Chetan: Chetan > Ajay > Bharat.
Step 2: Second statement
Dev is younger than Bharat but older than Farhan: Bharat > Dev > Farhan.
Step 3: Join them through Bharat
Chetan > Ajay > Bharat > Dev > Farhan.
Step 4: Answer
Chetan is the oldest (and Farhan the youngest).""", trick=r"Write each clue as a chain with '>' and join them at the common name.")
S[8] = dict(raw=r"""Step 1: Find the differences
4 − 1 = 3, 10 − 4 = 6, 20 − 10 = 10, 35 − 20 = 15, 56 − 35 = 21
Step 2: Read the differences
3, 6, 10, 15, 21 are triangular numbers; their own gaps are 3, 4, 5, 6, so the next gap is 7 and the next difference is 21 + 7 = 28.
Step 3: Next term
56 + 28 = 84
Step 4: Answer
The next number is 84 (these are the tetrahedral numbers 1, 4, 10, 20, 35, 56, 84).""", trick=r"Differences +3, +6, +10, +15, +21 → next +28.")
S[9] = dict(raw=r"""Step 1: Compare neighbouring terms
204 = 102 × 2 and 408 = 204 × 2 — each term is double the previous one.
Step 2: Find the missing term
408 × 2 = 816
Step 3: Check the rest of the series
816 × 2 = 1632 ✓ and 1632 × 2 = 3264 ✓
Step 4: Answer
The missing number is 816.""", trick=r"Ratio series: each term × 2.")
S[10] = dict(raw=r"""Step 1: Find the differences
54 − 43 = 11, 76 − 54 = 22, 109 − 76 = 33 — the gaps are multiples of 11.
Step 2: First blank
Next gap = 44: 109 + 44 = 153.
Step 3: Check and continue
153 + 55 = 208 ✓, 208 + 66 = 274 ✓, so the last gap is 77: 274 + 77 = 351.
Step 4: Answer
The missing terms are 153 and 351.""", trick=r"Gaps 11, 22, 33, … — the next gap is always 11 more.")
S[11] = dict(raw=r"""Step 1: First letters
P → S → V: +3 each time. Next: V + 3 = Y, and Y + 3 = B (wraps round) ✓ matches BAY.
Step 2: Second letters
M → J → G: −3 each time. Next: G − 3 = D, and D − 3 = A ✓
Step 3: Third letters
K → H → E: −3 each time. Next: E − 3 = B, and B − 3 = Y ✓
Step 4: Answer
The missing term is YDB.""", trick=r"Split the cluster into three letter positions: +3, −3, −3.")
S[12] = dict(raw=r"""Step 1: Read the first pair
The first figure has four elements stacked from top to bottom: circle, square, rectangle, triangle. In the second figure the order is square, rectangle, triangle, circle.
Step 2: Find the rule
The top element (circle) has moved to the bottom and every other element has moved one place up; nothing is rotated or shaded.
Step 3: Apply it to the third figure
Its elements from top to bottom are: arrow, circle-with-line, triangle, square. Moving the top arrow to the bottom gives: circle-with-line, triangle, square, arrow.
Step 4: Check the options
Only one option shows circle-with-line on top, then triangle, then square, with the arrow at the bottom pointing the same way. The others swap the square and triangle, change the arrow's direction or change the shading of the triangle.""", trick=r"Top element goes to the bottom; the rest move up one place.")
S[13] = dict(raw=r"""Step 1: Track each element in the first pair
The element at the bottom-right of the first figure moves to the top-left, the top-left one moves to the middle, and the middle one moves to the bottom-right.
Step 2: Check how each element is drawn
Each moved element is turned upside down (flipped top to bottom): the inverted Y becomes an upright Y, and the stick with the circle at its lower end now has the circle at the top.
Step 3: Apply it to the third figure
The upward arrow at the bottom-right goes to the top-left as a downward arrow; the bracket at the top-left goes to the middle (it looks the same after a top-to-bottom flip); the hooked line in the middle goes to the bottom-right, flipped.
Step 4: Check the options
Only one option has a downward arrow at the top-left, the bracket in the middle and the flipped hooked line at the bottom-right. The others keep the upward arrow or put the elements in the wrong places.""", trick=r"Move each element one place round (bottom-right → top-left → middle → bottom-right) and flip it upside down.")
S[14] = dict(raw=r"""Step 1: Study LT70 → UK140
Number: 70 × 2 = 140. Letters: the second letter T + 1 = U comes first, and the first letter L − 1 = K comes second.
Step 2: Confirm with KK90 → LJ180
90 × 2 = 180 ✓. Second letter K + 1 = L comes first, first letter K − 1 = J comes second ✓
Step 3: Work back from FH130
Number: 130 ÷ 2 = 65. F = (second letter) + 1 → second letter = E. H = (first letter) − 1 → first letter = I.
Step 4: Answer and check
The missing cluster is IE65. Check: second letter E + 1 = F, first letter I − 1 = H, 65 × 2 = 130 → FH130 ✓""", trick=r"Number doubles; letters swap places with +1 / −1.")
S[15] = dict(raw=r"""Step 1: Study DLP300 → BJN540
Each letter moves 2 back: D → B, L → J, P → N. Number: 300 + 240 = 540.
Step 2: Confirm with LKJ720 → JIH960
L → J, K → I, J → H (each −2) and 720 + 240 = 960 ✓
Step 3: Apply to MVZ620
M − 2 = K, V − 2 = T, Z − 2 = X; 620 + 240 = 860.
Step 4: Answer
The cluster is KTX860.""", trick=r"Letters −2 each, number +240.")
S[16] = dict(raw=r"""Step 1: Compare the common start
All five words begin with P-L-A-N.
Step 2: Shortest first
"Plan" (4) has nothing after PLAN, so it comes first. Next is "Plane" (5): PLAN + E.
Step 3: Compare the rest
"Planet" (1) = PLANE + T comes right after Plane. Then "Plank" (2) — K — and "Plant" (3) — T, since K comes before T.
Step 4: Answer
Order: Plan, Plane, Planet, Plank, Plant → 4, 5, 1, 2, 3 = 45123.""", trick=r"A word that is the start of another word always comes first: Plan → Plane → Planet.")
S[17] = dict(raw=r"""Step 1: Study 776 → 1553
\( 776 \times 2 = 1552 \) and \( 1552 + 1 = 1553 \).
Step 2: Confirm with 133 → 267
\( 133 \times 2 + 1 = 267 \) ✓
Step 3: Apply to 218
\( 218 \times 2 + 1 = 437 \)
Step 4: Answer
The missing number is 437.""", trick=r"Rule: double it and add 1.")
S[18] = dict(raw=r"""Step 1: Study 18 → 400
\( 400 = 20^2 \) and \( 20 = 18 + 2 \).
Step 2: Confirm with 23 → 625
\( 625 = 25^2 \) and \( 25 = 23 + 2 \) ✓
Step 3: Apply to 14
\( (14 + 2)^2 = 16^2 = 256 \)
Step 4: Answer
The number is 256.""", trick=r"Add 2, then square.")
S[19] = dict(raw=r"""Step 1: First letter of SUNG → HVOH
S (19) → H (8): 19 + 8 = 27, so H is the opposite letter of S (A↔Z, B↔Y, …).
Step 2: Remaining letters
U → V, N → O, G → H: each +1.
Step 3: Confirm with PLEX → KMFY
P (16) ↔ K (11), 16 + 11 = 27 ✓; L → M, E → F, X → Y (+1 each) ✓
Step 4: Apply to BABE
B ↔ Y (2 + 25 = 27); A → B, B → C, E → F. Code: YBCF.""", trick=r"Opposite-letter pairs add up to 27 (B + Y = 2 + 25).")
S[20] = dict(raw=r"""Step 1: Compare BABES → DDGBO letter by letter
B → D (+2), A → D (+3), B → G (+5), E → B (−3), S → O (−4).
Step 2: Confirm with ROCKS → TRHHO
R → T (+2), O → R (+3), C → H (+5), K → H (−3), S → O (−4) ✓
Step 3: Apply to SEIZE
S + 2 = U, E + 3 = H, I + 5 = N, Z − 3 = W, E − 4 = A.
Step 4: Answer
SEIZE is coded as UHNWA.""", trick=r"Position-wise shifts: +2, +3, +5, −3, −4.")
