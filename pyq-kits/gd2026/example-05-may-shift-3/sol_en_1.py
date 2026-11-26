S = {}
S[1] = dict(raw=r"""Step 1: Look at how the known terms grow
97 → 199 → 403 → 811 → 1627: each term is a little more than double the one before it.
Step 2: Find the exact rule
97 × 2 + 5 = 199, 199 × 2 + 5 = 403, 403 × 2 + 5 = 811, 811 × 2 + 5 = 1627 ✓. So each term = previous term × 2 + 5.
Step 3: Work backwards to the missing first term
? × 2 + 5 = 97 → ? × 2 = 92 → ? = 46.
Step 4: Check the tail of the series
1627 × 2 + 5 = 3259 and 3259 × 2 + 5 = 6523 ✓. The missing term is 46.""", trick=r"Doubling series: test “× 2 + k”; to go backwards, subtract k and halve.")
S[2] = dict(raw=r"""Step 1: Convert the letters to positions
W = 23, T = 20, O = 15, L = 12, ? , D = 4, Y = 25, V = 22.
Step 2: Find the gaps
W → T is −3, T → O is −5, O → L is −3. The steps alternate −3, −5.
Step 3: Find the missing letter
After a −3 step comes a −5 step: 12 − 5 = 7 = G.
Step 4: Check the rest
G (7) − 3 = D (4) ✓, D (4) − 5 = −1 → 25 = Y ✓, Y (25) − 3 = V (22) ✓. The missing letter is G.""", trick=r"Alternate −3 and −5; before A, count back from Z (A − 1 = Z).")
S[3] = dict(raw=r"""Step 1: Study the first pair RF → TI
R (18) + 2 = T (20); F (6) + 3 = I (9). So the first letter moves 2 ahead and the second letter 3 ahead.
Step 2: Confirm with XA → ZD
X (24) + 2 = Z (26); A (1) + 3 = D (4) ✓ — the same +2, +3 rule.
Step 3: Apply the rule to QC
Q (17) + 2 = S (19); C (3) + 3 = F (6). So QC → SF.
Step 4: Reject the others
VG is +5, +4; SD is +2, +1; QF is 0, +3 — none follows +2, +3. The answer is SF.""", trick=r"First letter +2, second letter +3.")
S[4] = dict(raw=r"""Step 1: Split each cluster into first and second letters
First letters: ?, U, R, O, L, I, F, C. Second letters: ?, F, C, Y, T, N, G, Y.
Step 2: Pattern of the first letters
U → R → O → L → I → F → C: each step is −3. So the first letter before U is U + 3 = X.
Step 3: Pattern of the second letters
F → C (−3), C → Y (−4), Y → T (−5), T → N (−6), N → G (−7), G → Y (−8): the gap grows by 1 each time. So the step before F was −2, i.e. the missing letter is F + 2 = H.
Step 4: Answer
The missing cluster is XH.""", trick=r"Split the clusters: first letters −3 throughout; second letters −2, −3, −4, … (gap grows by 1).")
S[5] = dict(raw=r"""Step 1: Study CH → AS
C (3) − 2 = A (1). H (8) and S (19) are opposite letters, because 8 + 19 = 27.
Step 2: Confirm with TK → RP
T (20) − 2 = R (18). K (11) and P (16) are opposite letters (11 + 16 = 27) ✓
Step 3: Work backwards from LH
The first letter of ? minus 2 gives L (12), so it is N (14). The second letter of ? is the opposite of H, which is S (19). So ? = NS.
Step 4: Check NS → LH
N (14) − 2 = L (12) ✓ and S (19) + H (8) = 27 ✓. The answer is NS.""", trick=r"Opposite letters add up to 27 (A–Z, H–S, K–P).")
S[6] = dict(raw=r"""Step 1: Find the rule in (LW, JQ, HK)
First letters L → J → H: −2 each time. Second letters W → Q → K: −6 each time.
Step 2: Confirm with (QE, OY, MS)
Q → O → M is −2, −2; E (5) − 6 = −1 → 25 = Y, Y → S is −6 ✓
Step 3: Test the options
(VT, TN, RH): V → T → R is −2, −2 and T → N → H is −6, −6 ✓
Step 4: Reject the rest
(TG, UE, LY) has T → U (+1); (OD, OB, GV) has O → O (0); (OB, JZ, GT) has O → J (−5). Only (VT, TN, RH) follows the rule.""", trick=r"Check the first letters and the second letters separately: −2 and −6 here.")
S[7] = dict(raw=r"""Step 1: Count the days from 21 September 2024 to 27 April 2025
September: 30 − 21 = 9; October 31; November 30; December 31; January 31; February 28 (2025 is not a leap year); March 31; April 27.
Step 2: Add them
9 + 31 + 30 + 31 + 31 + 28 + 31 + 27 = 218 days.
Step 3: Find the odd days
218 ÷ 7 = 31 weeks and 1 day, so there is 1 odd day.
Step 4: Move forward
Thursday + 1 = Friday. So 27 April 2025 is a Friday (on the day given in the question).""", trick=r"Odd days = total days ÷ 7 remainder; move that many days ahead.")
S[8] = dict(raw=r"""Step 1: Count the days from 25 November 2020 to 25 March 2021
November: 30 − 25 = 5; December 31; January 31; February 28 (2021 is not a leap year); March 25.
Step 2: Add them
5 + 31 + 31 + 28 + 25 = 120 days.
Step 3: Find the odd days
120 ÷ 7 = 17 weeks and 1 day, so there is 1 odd day.
Step 4: Move forward
Wednesday + 1 = Thursday. So 25 March 2021 was a Thursday.""", trick=r"Count the remaining days of the first month, the full months, then the days of the last month.")
S[9] = dict(raw=r"""Step 1: Use “only E is to the left of D”
Only one girl sits to the left of D, so D is second from the left and E is at the left end.
Step 2: Use “only C is to the right of A”
Only one girl sits to the right of A, so A is fourth and C is at the right end.
Step 3: Fill the remaining seat
Arrangement from left: E, D, _, A, C. The only empty seat is third, so B sits there.
Step 4: Answer
B is third from the left end.""", trick=r"“Only X is to the left of Y” puts Y second and X at the end.")
S[10] = dict(raw=r"""Step 1: Write the comparisons
No one is elder than A, so A is the eldest. B > C > D (C is elder than D but younger than B). D > E and E > F.
Step 2: Join them into one chain
A > B > C > D > E > F.
Step 3: Count the boys older than B
Only A is older than B.
Step 4: Answer
The age of 1 boy is more than B's.""", trick=r"Join all the clues into one chain from eldest to youngest.")
S[11] = dict(raw=r"""Step 1: Study the first pair
The first figure has three vertical lines (with arrows). The second figure keeps these lines and adds the same number of lines at right angles to them, so a grid of lines is formed.
Step 2: Apply the rule to the third figure
The third figure has three horizontal lines. So the answer must keep three horizontal lines and add three vertical lines across them.
Step 3: Test the options
Count the lines in each option: the answer figure is the one with exactly three horizontal and three vertical lines. The other figures have the wrong count — two or four horizontal lines, or four vertical lines.
Step 4: Answer
The grid of three horizontal and three vertical lines completes the analogy.""", trick=r"Count the lines in each direction before comparing the options.")
S[12] = dict(raw=r"""Step 1: Study the first pair
In the first figure: top ○, bottom ●, left ▼, right □. In the second figure: top ●, bottom ○, left □, right ▼.
Step 2: Find the rule
The top and bottom symbols change places, and the left and right symbols change places (the whole figure turns through 180°).
Step 3: Apply the rule to the third figure
Third figure: top X, bottom Y, left Z, right G. After the change: top Y, bottom X, left G, right Z.
Step 4: Answer
The figure with Y at the top, X at the bottom, G on the left and Z on the right is the answer.""", trick=r"Swap top ↔ bottom and left ↔ right (a half turn).")
S[13] = dict(raw=r"""Step 1: Study ZA300 → YZ154
Z − 1 = Y, A − 1 = Z (one step back), and 300 − 146 = 154.
Step 2: Confirm with WY500 → VX354
W − 1 = V, Y − 1 = X, and 500 − 146 = 354 ✓
Step 3: Apply the rule to TQ700
T − 1 = S, Q − 1 = P, and 700 − 146 = 554. So TQ700 → SP554.
Step 4: Reject the others
UP554 and UR454 move T forward; PS354 changes the order of the letters and the number. The answer is SP554.""", trick=r"Each letter −1, number −146.")
S[14] = dict(raw=r"""Step 1: Study KPL22 → JOK441
K − 1 = J, P − 1 = O, L − 1 = K; and 441 = 21², where 21 = 22 − 1.
Step 2: Confirm with IRO28 → HQN729
I − 1 = H, R − 1 = Q, O − 1 = N; and 729 = 27², where 27 = 28 − 1 ✓
Step 3: Work backwards from TKQ625
Letters: T + 1 = U, K + 1 = L, Q + 1 = R → ULR. Number: 625 = 25², so the first number is 25 + 1 = 26. So ? = ULR26.
Step 4: Answer
ULR26 → TKQ625 follows the same rule.""", trick=r"Letters −1; number: subtract 1 and square it.")
S[15] = dict(raw=r"""Step 1: Study 282 → 138
282 ÷ 2 = 141, and 141 − 3 = 138.
Step 2: Confirm with 1166 → 580
1166 ÷ 2 = 583, and 583 − 3 = 580 ✓. So the second number = first number ÷ 2 − 3.
Step 3: Work backwards from 991
? ÷ 2 − 3 = 991 → ? ÷ 2 = 994 → ? = 1988.
Step 4: Check
1988 ÷ 2 = 994 and 994 − 3 = 991 ✓. The answer is 1988.""", trick=r"Rule: half the number, then subtract 3.")
S[16] = dict(raw=r"""Step 1: Compare ACAI with DGWD letter by letter
A (1) → D (4): +3; C (3) → G (7): +4; A (1) → W (23): −4; I (9) → D (4): −5.
Step 2: Confirm with CHAP → FLWK
C → F (+3), H → L (+4), A → W (−4), P → K (−5) ✓
Step 3: Apply +3, +4, −4, −5 to PIER
P (16) + 3 = S; I (9) + 4 = M; E (5) − 4 = A; R (18) − 5 = M.
Step 4: Answer
PIER is coded as SMAM.""", trick=r"Position-wise shifts: +3, +4, −4, −5.")
S[17] = dict(raw=r"""Step 1: Note what must be made up
At 8 AM the watch is 8 minutes slow, i.e. 8 × 60 = 480 seconds behind.
Step 2: Rate of gaining
It gains 8 seconds every hour.
Step 3: Time needed
480 ÷ 8 = 60 hours.
Step 4: Find the clock time
60 hours = 2 days and 12 hours. 8 AM + 12 hours = 8 PM. So it will show the correct time at 8:00 PM (two and a half days later).""", trick=r"Time taken = total error ÷ gain per hour.")
S[18] = dict(raw=r"""Step 1: Look at the parts of each figure
Each figure has a bent line with three symbols — an arrow, a small square and a circle. Two symbols sit at the ends of the line and one on the short branch in the middle.
Step 2: Track the symbols
Figure 1: arrow at the lower end, square on the branch, circle at the upper end. Figure 2: square at the lower end, circle on the branch, arrow at the upper end. Figure 3: circle at the lower end, arrow on the branch, square at the upper end. Figure 4 repeats Figure 1's order, in the flipped position.
Step 3: Predict the fifth figure
The order repeats every three figures and the shape flips each time, so Figure 5 must match Figure 2's order — square at the lower end, circle on the branch, arrow at the upper end — drawn in the same position as Figures 1 and 3.
Step 4: Answer
The option with the square at the lower end, the circle on the branch and the arrow at the upper end is the answer.""", trick=r"Track one symbol at a time: lower end → branch → upper end, in a cycle of three.")
S[19] = dict(raw=r"""Step 1: Look at what is added in each figure
Figure 1: T in the bottom-right cell. Figure 2: 7 added in the middle-right cell. Figure 3: M added in the top-right cell. Figure 4: U added in the bottom-middle cell.
Step 2: Look at what happens to the old symbols
At every step all the symbols already in the grid are turned upside down (water image): T → ⊥ → T → ⊥, and 7 and M are flipped in the next figure.
Step 3: Build Figure 5
Flip the symbols of Figure 4 again: bottom-right T, middle-right flipped 7, top-right M (upright again), bottom-middle U turned upside down (∩). Then add a new upright letter in the next cell — P in the centre.
Step 4: Answer
The grid with M, flipped 7, an upright P, ∩ and T is the answer.""", trick=r"Each step: flip everything already drawn, then add one new upright symbol.")
S[20] = dict(raw=r"""Step 1: Write the ages with the ratio
Let the ages be \( 5x \) and \( 7x \) years.
Step 2: Use the difference
\( 7x - 5x = 2x = 8 \), so \( x = 4 \). Present ages: 20 years and 28 years.
Step 3: Ages 7 years ago
\( 20 - 7 = 13 \) and \( 28 - 7 = 21 \).
Step 4: Ratio
\( 13 : 21 \)""", trick=r"Difference of ratio parts = difference of ages; then subtract the same years from both.")
