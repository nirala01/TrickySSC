S = {}
S[1] = dict(raw=r"""Step 1: Look at how each term grows
−89 → −176: \( -89 \times 2 = -178 \) and \( -178 + 2 = -176 \).
Step 2: Test the rule on the known terms
\( -698 \times 2 + 2 = -1394 \) ✓, \( -1394 \times 2 + 2 = -2786 \) ✓, \( -2786 \times 2 + 2 = -5570 \) ✓.
Step 3: Find the missing term
\( -176 \times 2 + 2 = -352 + 2 = -350 \).
Step 4: Check it with the next term
\( -350 \times 2 + 2 = -700 + 2 = -698 \) ✓, so the missing term is −350.""", trick=r"Rule: next term = previous × 2 + 2 (for negative numbers the “+ 2” makes the value less negative).")
S[2] = dict(raw=r"""Step 1: Write the letter positions
X = 24, B = 2, H = 8, ?, R = 18, V = 22, B = 2, F = 6, L = 12.
Step 2: Find the gaps that are known
X → B: 24 + 4 = 28 → 28 − 26 = 2 (B), so +4; B → H: +6; R → V: +4; V → B: 22 + 6 = 28 → B, so +6; B → F: +4; F → L: +6.
Step 3: Fill the missing term
The gaps alternate +4, +6. After H (+6) the next gap is +4: H (8) + 4 = 12 = L.
Step 4: Check
L (12) + 6 = 18 = R ✓, so the missing letter is L.""", trick=r"Alternating gaps +4, +6; after Z count again from A.")
S[3] = dict(raw=r"""Step 1: Study the first letters
A (1) → F (6): +5; J (10) → O (15): +5.
Step 2: Study the second letters
Z (26) → A (1) and S (19) → H (8). Z and A are opposite letters (26 + 1 = 27), and S and H are opposite letters (19 + 8 = 27).
Step 3: Apply the rule to KM
K (11) + 5 = 16 = P; the opposite of M (13) is 27 − 13 = 14 = N.
Step 4: Answer
The required cluster is PN.""", trick=r"First letter +5; second letter → its opposite (the two positions add up to 27).")
S[4] = dict(raw=r"""Step 1: Split each cluster into first and second letters
First letters: E, G, I, ?, M, O, Q, S. Second letters: A, Y, W, ?, S, Q, O, M.
Step 2: Pattern of the first letters
E (5) → G (7) → I (9): +2 each time, so the next is 9 + 2 = 11 = K, and K + 2 = M ✓.
Step 3: Pattern of the second letters
A (1) → Y (25) → W (23): −2 each time (A − 2 goes back to Y). Next: 23 − 2 = 21 = U, and U − 2 = S ✓.
Step 4: Answer
The missing cluster is KU.""", trick=r"First letter +2, second letter −2.")
S[5] = dict(raw=r"""Step 1: Study HJ → FD
H (8) − 2 = 6 = F; J (10) − 6 = 4 = D.
Step 2: Confirm with AC → YW
A (1) − 2 = −1 → 26 − 1 = 25 = Y ✓; C (3) − 6 = −3 → 26 − 3 = 23 = W ✓.
Step 3: Apply the rule to EX
E (5) − 2 = 3 = C; X (24) − 6 = 18 = R.
Step 4: Answer
The required cluster is CR.""", trick=r"First letter −2, second letter −6; going below A, continue from Z.")
S[6] = dict(raw=r"""Step 1: Find the rule in (MB, OF, RK)
First letters M (13) → O (15) → R (18): +2, +3. Second letters B (2) → F (6) → K (11): +4, +5.
Step 2: Confirm with (DL, FP, IU)
D (4) → F (6) → I (9): +2, +3 ✓. L (12) → P (16) → U (21): +4, +5 ✓.
Step 3: Test the options
(MF, OJ, RO): M → O → R is +2, +3 ✓; F (6) → J (10) → O (15) is +4, +5 ✓.
Step 4: Reject the rest
(XA, ZD, AI) has Z → A (+1); (TV, VY, AD) has V → A (+5); (TQ, VT, CY) has V → C (+7). Only (MF, OJ, RO) follows the rule.""", trick=r"First letters +2, +3; second letters +4, +5 — check both rows separately.")
S[7] = dict(raw=r"""Step 1: Is 2100 a leap year?
A century year is a leap year only if it is divisible by 400. \( 2100 \div 400 = 5.25 \), so 2100 is NOT a leap year.
Step 2: Days in each month
January 31, February 28 (not a leap year), March 31, April 30.
Step 3: Add them
\( 31 + 28 + 31 + 30 = 120 \).
Step 4: Answer
The total is 120 days.""", trick=r"Century years (1900, 2100, 2200) are leap years only if divisible by 400 — so February 2100 has 28 days.")
S[8] = dict(raw=r"""Step 1: Use a known reference
1 January 1900 was a Monday.
Step 2: Count the years from 1900 to 1905
1900, 1901, 1902, 1903, 1904, 1905 → 6 years. Only 1904 is a leap year (1900 is not, as it is not divisible by 400).
Step 3: Count the odd days
Each ordinary year gives 1 odd day and a leap year gives 2: \( 5 \times 1 + 1 \times 2 = 7 \) odd days = 1 full week = 0 odd days.
Step 4: Answer
With 0 odd days, 1 January 1906 falls on the same day as 1 January 1900 — Monday.""", trick=r"1 Jan 1900 = Monday; ordinary year = 1 odd day, leap year = 2 odd days.")
S[9] = dict(raw=r"""Step 1: Place J
J is slower than only one car, so J is the 2nd fastest.
Step 2: Place K
K is the second lowest, so K is 4th from the top (J > K ✓).
Step 3: Place N, L and M
N > L > M, and the empty places are 1st, 3rd and 5th. So N is 1st, L is 3rd and M is 5th.
Step 4: Answer
Order: N > J > L > K > M. The only car faster than J is N.""", trick=r"Fix the cars with exact ranks first (J 2nd, K 4th), then fill N > L > M in the gaps.")
S[10] = dict(raw=r"""Step 1: Directions when facing away from the centre
For a person facing outside, “left” is the anticlockwise direction and “right” is clockwise. Number the seats 0–6 clockwise and put B7 at seat 0.
Step 2: Place B6 and B5
B6 is second to the left of B7 → seat 5 (two places anticlockwise). B5 is second to the left of B6 → seat 3.
Step 3: Place B4, B1, B3 and B2
B4 is next to both B1 and B7. Seat 6 would need B1 at seat 5 (taken), so B4 is at seat 1 and B1 at seat 2. B3 is not next to B7, so B3 cannot take seat 6; B3 is at seat 4 and B2 at seat 6.
Step 4: Read the answer
The immediate left of B3 (seat 4) is the anticlockwise neighbour, seat 3 — that is B5.""", trick=r"Facing outside: left = anticlockwise, right = clockwise (opposite of facing the centre).")
S[11] = dict(raw=r"""Step 1: Read the first pair row by row
First figure, top to bottom: thick bar, line with a fork (feather) at the right, right arrow, double-headed arrow.
Second figure: line with the fork, thick bar, double-headed arrow, right arrow.
Step 2: Find the rule
Rows 1 and 2 swap places, and rows 3 and 4 swap places; no element changes its direction.
Step 3: Apply it to the third figure
Third figure: double-headed arrow, right arrow, fork line, thick bar. Swapping 1↔2 and 3↔4 gives: right arrow, double-headed arrow, thick bar, fork line.
Step 4: Answer
Only the figure reading “right arrow, double-headed arrow, thick bar, fork line (fork at the right)” matches; the others have a left arrow, a wrong order or a reversed fork.""", trick=r"Pair-swap rule: swap the top two rows and the bottom two rows.")
S[12] = dict(raw=r"""Step 1: Read the first pair side by side
First figure: top 2Y, right A over 5, bottom P7, left N over 9. Second figure: top Y2, right 5 over A, bottom 7P, left 9 over N.
Step 2: Find the rule
On every side the two symbols simply swap places; the sides themselves stay where they are.
Step 3: Apply it to the third figure
Third figure: top 1 9, right 3 over 7, bottom 2 8, left 4 over 9. Swapping each pair gives: top 9 1, right 7 over 3, bottom 8 2, left 9 over 4.
Step 4: Answer
The figure with 9 1 at the top, 9 over 4 on the left, 7 over 3 on the right and 8 2 at the bottom is the answer (one look-alike keeps 3 over 7, two others keep 1 9 at the top).""", trick=r"Each side's pair of symbols swaps places.")
S[13] = dict(raw=r"""Step 1: Study BG12 → EJ59
B (2) + 3 = E (5); G (7) + 3 = J (10); 12 + 47 = 59.
Step 2: Confirm with PQ48 → ST95
P (16) + 3 = S (19); Q (17) + 3 = T (20); 48 + 47 = 95 ✓.
Step 3: Apply to LM33
L (12) + 3 = O (15); M (13) + 3 = P (16); 33 + 47 = 80.
Step 4: Answer
The required cluster is OP80.""", trick=r"Both letters +3, number +47.")
S[14] = dict(raw=r"""Step 1: Study AK40 → EE100
A (1) + 4 = E (5); K (11) − 6 = E (5); \( 40 \times 2.5 = 100 \).
Step 2: Confirm with DL80 → HF200
D (4) + 4 = H (8); L (12) − 6 = F (6); \( 80 \times 2.5 = 200 \) ✓.
Step 3: Apply to BM60
B (2) + 4 = F (6); M (13) − 6 = G (7); \( 60 \times 2.5 = 150 \).
Step 4: Answer
The required cluster is FG150.""", trick=r"First letter +4, second letter −6, number × 2.5.")
S[15] = dict(raw=r"""Step 1: Study 777 → 257
\( 777 \div 3 = 259 \) and \( 259 - 2 = 257 \).
Step 2: Confirm with 1812 → 602
\( 1812 \div 3 = 604 \) and \( 604 - 2 = 602 \) ✓.
Step 3: Apply to 2436
\( 2436 \div 3 = 812 \) and \( 812 - 2 = 810 \).
Step 4: Answer
The required number is 810.""", trick=r"Rule: divide by 3, then subtract 2.")
S[16] = dict(raw=r"""Step 1: Study WEES → ZJCO
W (23) + 3 = Z; E (5) + 5 = J (10); E (5) − 2 = C (3); S (19) − 4 = O (15).
Step 2: Confirm with EACH → HFAD
E + 3 = H; A + 5 = F; C − 2 = A; H − 4 = D ✓.
Step 3: Apply to PREY
P (16) + 3 = S; R (18) + 5 = W (23); E (5) − 2 = C; Y (25) − 4 = U (21).
Step 4: Answer
PREY is coded as SWCU.""", trick=r"Position rule: +3, +5, −2, −4.")
S[17] = dict(raw=r"""Step 1: Find the time passed
From 6 AM to 4 PM is 10 hours = \( 10 \times 60 = 600 \) minutes.
Step 2: Count the 5-minute intervals
\( 600 \div 5 = 120 \) intervals.
Step 3: Find the total gain
\( 120 \times 2 = 240 \) seconds = 4 minutes.
Step 4: Answer
A gaining clock runs ahead, so it shows 4:00 + 4 minutes = 4:04 PM.""", trick=r"Gain = (minutes passed ÷ 5) × 2 seconds; a gaining clock shows MORE than the real time.")
S[18] = dict(raw=r"""Step 1: Read each figure as four small boxes from top-left to bottom-right
Write “╲” for a box whose line runs from its top-left to bottom-right corner and “╱” for the other way.
Figure 1: ╲ ╱ ╱ ╲ — Figure 2: ╱ ╱ ╱ ╲ — Figure 3: ╱ ╲ ╱ ╲ — Figure 4: ╱ ╲ ╲ ╲.
Step 2: Find the rule
From one figure to the next exactly one box turns its line, and the turning box moves down by one place: box 1, then box 2, then box 3.
Step 3: Apply it to the next figure
Now box 4 turns: ╱ ╲ ╲ ╲ becomes ╱ ╲ ╲ ╱.
Step 4: Answer
The figure reading ╱ ╲ ╲ ╱ is the answer; the others read ╲ ╱ ╲ ╲, ╱ ╱ ╲ ╱ and ╲ ╲ ╲ ╲.""", trick=r"One box changes per step, moving down the diagonal one place each time.")
S[19] = dict(raw=r"""Step 1: Follow one letter
Y starts in the top-left cell (figure 1), is upside down in the top-middle (figure 2), upright in the top-right (figure 3) and upside down in the middle-right cell (figure 4).
Step 2: Find the rule
In every step each letter moves one cell clockwise along the border and turns upside down, and a new upright letter appears in the top-left cell (Y, A, P, V, …).
Step 3: Apply it to figure 5
Y moves to bottom-right and becomes upright Y; A moves to middle-right and becomes ∀ (upside-down A); P moves to top-right and becomes upright P; V moves to top-middle and becomes Λ; a new letter X appears at the top-left.
Step 4: Answer
The grid with X, Λ, P in the top row, ∀ at the middle-right and Y at the bottom-right is the answer.""", trick=r"Clockwise one cell + flip upside down every step; a new letter enters at the top-left.")
S[20] = dict(raw=r"""Step 1: Find the son's present age
After 11 years the son will be 16, so now he is \( 16 - 11 = 5 \) years.
Step 2: Son's age 3 years ago
\( 5 - 3 = 2 \) years.
Step 3: Father's age
15 years ago the father was \( 6 \times 2 = 12 \) years, so now he is \( 12 + 15 = 27 \) years.
Step 4: Ratio
The ratio of their present ages is \( 27 : 5 \).""", trick=r"Find the son's present age first, then work out the father's age from the “6 times” clue.")
