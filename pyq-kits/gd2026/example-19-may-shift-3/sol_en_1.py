S = {}
S[1] = dict(raw=r"""Step 1: Compare neighbouring terms
\( 28431 \div 9477 = 3 \), \( 9477 \div 3159 = 3 \), \( 3159 \div 1053 = 3 \).
Step 2: Confirm the rule on the rest
\( 1053 \div 3 = 351 \), \( 351 \div 3 = 117 \), \( 117 \div 3 = 39 \) — every term is the previous term divided by 3.
Step 3: Apply the rule to the missing term
\( 39 \div 3 = 13 \).
Step 4: Answer
The missing term is 13 (23, 17 and 11 are not one-third of 39).""", trick=r"Each term ÷ 3 → \( 39 \div 3 = 13 \).")
S[2] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: G, I, ?, M, O, Q, S, U. Second letters: I, N, ?, X, C, H, M, R.
Step 2: Rule for the first letters
G (7) → I (9) → … → M (13) → O (15) → Q (17) → S (19) → U (21): each step is +2, so the missing first letter is I + 2 = K (11).
Step 3: Rule for the second letters
I (9) → N (14) is +5, and X (24) → C (29 − 26 = 3) → H (8) → M (13) → R (18) is also +5. So the missing second letter is N + 5 = S (19), and S + 5 = X ✓.
Step 4: Answer
The missing term is KS. KP breaks the +5 rule, IV breaks the +2 rule and LS has L instead of K.""", trick=r"First letters +2, second letters +5 → K and S.")
S[3] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: E, H, M, ?, U, X, C, F. Second letters: V, Y, C, ?, J, M, Q, T.
Step 2: Rule for the first letters
E (5) → H (8) is +3, H → M (13) is +5, then +3, +5 …, so M + 3 = P (16), P + 5 = U (21) ✓, U + 3 = X ✓, X + 5 = C (29 − 26) ✓, C + 3 = F ✓.
Step 3: Rule for the second letters
V (22) → Y (25) is +3, Y → C (29 − 26 = 3) is +4, then +3, +4 …, so C + 3 = F (6), F + 4 = J (10) ✓, J + 3 = M ✓, M + 4 = Q ✓, Q + 3 = T ✓.
Step 4: Answer
The missing term is PF. PC breaks the second-letter rule, RF the first-letter rule, and OG both.""", trick=r"First letters +3, +5 alternately; second letters +3, +4 alternately → PF.")
S[4] = dict(raw=r"""Step 1: Find the common difference
\( -3 - (-128) = 125 \), \( 122 - (-3) = 125 \), \( 247 - 122 = 125 \).
Step 2: Check the remaining terms
\( 247 + 125 = 372 \) ✓, \( 372 + 125 = 497 \) ✓, \( 497 + 125 = 622 \) ✓.
Step 3: Test the last term
\( 622 + 125 = 747 \), but the series shows 745.
Step 4: Answer
745 is the wrong term; it should be 747. −128, 122 and 247 all fit the +125 rule.""", trick=r"Add 125 each time; \( 622 + 125 = 747 \), not 745.")
S[5] = dict(raw=r"""Step 1: Find the first differences
\( 995 - 976 = 19 \), \( 976 - 955 = 21 \) — the differences grow by 2: 19, 21, 23, 25 …
Step 2: Build the correct series
\( 955 - 23 = 932 \), \( 932 - 25 = 907 \), \( 907 - 27 = 880 \), \( 880 - 29 = 851 \), \( 851 - 31 = 820 \).
Step 3: Compare with the given terms
Every term matches except the fourth: the series shows 929 where 932 should be.
Step 4: Answer
929 is the wrong term. With 929 in place, the gaps would be 26 and 22, which break the +2 pattern.""", trick=r"Subtract 19, 21, 23, 25 … → the fourth term must be 932.")
S[6] = dict(raw=r"""Step 1: Fix C and A
Facing north, right means towards the right end. A is fourth to the right of C, and only five people sit in the row, so C is at seat 1 (left end) and A at seat 5 (right end).
Step 2: Place B
B is second to the right of C, so B is at seat 3.
Step 3: Place D and E
D is to the immediate left of B, so D is at seat 2. The only seat left is 4, which goes to E.
Step 4: Count between E and A
Order from left: C, D, B, E, A. E (seat 4) and A (seat 5) are neighbours, so 0 persons sit between them.""", trick=r"C … A fill the two ends; order C D B E A → nobody between E and A.")
S[7] = dict(raw=r"""Step 1: Note the direction rule
For people facing the centre, the right-hand side is anticlockwise and the left-hand side is clockwise. Number the seats 0–6 clockwise and put C at 0.
Step 2: Place F, A and G
F is second to the right of C → seat 5. A is third to the left of C → seat 3. G is third to the left of F → \( 5 + 3 = 8 \), i.e. seat 1.
Step 3: Place D, B and E
Free seats: 2, 4, 6. D is not next to F (F's neighbours are seats 4 and 6), so D is at seat 2. B is not next to A (A's neighbours are seats 2 and 4), so B is at seat 6. E takes seat 4.
Step 4: Read the answer
The immediate right of F (seat 5) is one seat anticlockwise, seat 4 — that is E.""", trick=r"Facing the centre: right = anticlockwise. C0, G1, D2, A3, E4, F5, B6 → E is right of F.")
S[8] = dict(raw=r"""Step 1: Place D and C
Facing the centre, left is clockwise. Put D at seat 0 (seats numbered clockwise); C is fifth to the left of D → seat 5.
Step 2: Place A and Z
A sits next to both Z and D, so A is at seat 1 or seat 6. Seat 6 is next to C, and C's two neighbours must be B and Y, so A is at seat 1 and Z at seat 2.
Step 3: Place B, Y and X
C's neighbours (seats 4 and 6) are B and Y, so X is at seat 3. B is not next to X (seats 2 and 4), so B is at seat 6 and Y at seat 4.
Step 4: Check the pairs
Clockwise order: D, A, Z, X, Y, C, B. X (3) and Y (4) sit side by side. X–C, D–Y and A–B are not neighbours.""", trick=r"D0, A1, Z2, X3, Y4, C5, B6 → X and Y are neighbours.")
S[9] = dict(raw=r"""Step 1: Find the part filled in one hour
The tank fills in 6 hours, so in 1 hour it fills \( \dfrac{1}{6} \) of the tank.
Step 2: Multiply by the time given
In 2 hours it fills \( 2 \times \dfrac{1}{6} = \dfrac{2}{6} \).
Step 3: Simplify the fraction
\( \dfrac{2}{6} = \dfrac{1}{3} \).
Step 4: Answer
One-third of the tank is filled in 2 hours (check: 2 hours is one-third of 6 hours).""", trick=r"Part filled = time taken ÷ total time \( = \dfrac{2}{6} = \dfrac{1}{3} \).")
S[10] = dict(raw=r"""Step 1: Find the rule in the first pair
\( 7705 - 7650 = 55 \).
Step 2: Confirm with the third pair
\( 1178 - 1123 = 55 \) ✓, so second number = first number + 55.
Step 3: Apply the rule
\( 8436 + 55 = 8491 \).
Step 4: Answer
The missing number is 8491; 8487, 8489 and 8490 are 51, 53 and 54 more than 8436.""", trick=r"Add 55: \( 8436 + 55 = 8491 \).")
S[11] = dict(raw=r"""Step 1: Find the rule in the first pair
\( 8243 - 8209 = 34 \).
Step 2: Confirm with the third pair
\( 335 - 301 = 34 \) ✓, so second number = first number + 34.
Step 3: Apply the rule
\( 8433 + 34 = 8467 \).
Step 4: Answer
The missing number is 8467; 8466, 8469 and 8463 differ from 8433 by 33, 36 and 30.""", trick=r"Add 34: \( 8433 + 34 = 8467 \).")
S[12] = dict(raw=r"""Step 1: Compare LAMP with NDJK letter by letter
L (12) → N (14) is +2, A (1) → D (4) is +3, M (13) → J (10) is −3, P (16) → K (11) is −5.
Step 2: Confirm with PIKE → RLHZ
P → R is +2, I → L is +3, K → H is −3, E (5) → Z (5 − 5 = 0 → 26) is −5 ✓.
Step 3: Apply +2, +3, −3, −5 to ENVY
E (5) + 2 = G, N (14) + 3 = Q, V (22) − 3 = S, Y (25) − 5 = T.
Step 4: Answer
ENVY is coded as GQST.""", trick=r"Positions shift +2, +3, −3, −5 → ENVY = GQST.")
S[13] = dict(raw=r"""Step 1: First letters
P (16), ?, J (10), G (7), D (4): each step is −3, so the missing first letter is P − 3 = M (13).
Step 2: Second letters
K (11), ?, G (7), E (5), C (3): each step is −2, so the missing second letter is K − 2 = I (9).
Step 3: Numbers
27, ?, 125, 216, 343 are \( 3^{3} \), ?, \( 5^{3} \), \( 6^{3} \), \( 7^{3} \), so the missing number is \( 4^{3} = 64 \).
Step 4: Answer
The missing term is MI64. NJ64 has the wrong letters and LI36 the wrong number.""", trick=r"Letters −3 and −2; numbers are cubes 3³, 4³, 5³ … → MI64.")
S[14] = dict(raw=r"""Step 1: First letters
Y, Z, A, B, C, D: +1 each time (Z → A wraps round) — all correct.
Step 2: Second and third letters
Second letters should go C, B, A, Z, Y, X (−1 each), but the fourth term has A instead of Z. Third letters B, A, Z, Y, X, W (−1) are all correct.
Step 3: Numbers
1000, 1113, 1226, 1339, 1452, 1565 is +113 each time; the fourth term shows 1340 instead of 1339.
Step 4: Answer
The fourth term should be BZY1339, so BAY1340 is the wrong term.""", trick=r"Letters +1, −1, −1 and numbers +113 → the fourth term should be BZY1339.")
S[15] = dict(raw=r"""Step 1: First letters
M (13), P, S, V, Y, B: +3 each time (Y + 3 = 28 → B) — all correct.
Step 2: Second letters
P (16), T (20), X (24), then +4 gives B (28 − 26 = 2), F, J. The fourth term shows C instead of B.
Step 3: Third letters and numbers
Third letters A, V, Q, L, G, B fall by 5 each time ✓. Numbers 1, 3, 9, 27, 81, 243 are × 3 each time ✓.
Step 4: Answer
The fourth term should be VBL27, so VCL27 is the wrong term.""", trick=r"Second letters +4: X + 4 = B, not C → VCL27 is wrong.")
S[16] = dict(raw=r"""Step 1: Write the angle formula
Angle between the hands \( = |30H - 5.5M| \), where H = hour and M = minutes past the hour.
Step 2: Put H = 1
\( |30 - 5.5M| = 60 \). Since \( 30 - 5.5M = 60 \) gives a negative M, use \( 5.5M - 30 = 60 \).
Step 3: Solve for M
\( 5.5M = 90 \Rightarrow M = \dfrac{90}{5.5} = \dfrac{180}{11} = 16\dfrac{4}{11} \) minutes.
Step 4: Answer
The time is about 1:16 AM. At 1:20 the angle is 80°, at 1:14 it is 47°.""", trick=r"Minute hand must gain 30° + 60° = 90° at 5.5° a minute → \( \dfrac{90}{5.5} \approx 16 \) min.")
S[17] = dict(raw=r"""Step 1: Total time passed
From 4 AM to 4 PM is 12 hours \( = 12 \times 60 = 720 \) minutes.
Step 2: Count the 4-minute blocks
\( 720 \div 4 = 180 \) blocks.
Step 3: Total time gained
\( 180 \times 2 = 360 \) seconds \( = 6 \) minutes.
Step 4: Answer
A fast clock shows correct time + gain, so it shows 4:06:00 PM.""", trick=r"2 s per 4 min = 30 s per hour → 12 h × 30 s = 6 min fast.")
S[18] = dict(raw=r"""Step 1: Read each figure as six arrows
Number the arrow places top-left, top-right, middle-left, middle-right, bottom-left, bottom-right. In the first figure the top row points →, ← and the bottom row →, ←; the middle row points ←, ←.
Step 2: Find what changes each step
Figure 1 → 2: the middle-left arrow turns to →. Figure 2 → 3: the bottom-left arrow turns to ←. Figure 3 → 4: the bottom-right arrow turns to →. Exactly one arrow reverses per step, and the place moves middle-left → bottom-left → bottom-right, i.e. anticlockwise round the grid.
Step 3: Predict the fifth figure
Next in that path is middle-right, so its ← turns to →. The fifth figure is: top → ←, middle → →, bottom ← →.
Step 4: Match the options
Only the figure with top row → ←, middle row → → and bottom row ← → matches; the others differ in the top or bottom row.""", trick=r"One arrow flips per figure, moving anticlockwise: ML, BL, BR, then MR.")
S[19] = dict(raw=r"""Step 1: Read the first figure as three rows
Figure 1: K A / N M / L H.
Step 2: Find the two moves
Figure 1 → 2: the rows shift down one place (the bottom row L H goes to the top): L H / K A / N M. Figure 2 → 3: each row swaps its two letters: H L / A K / M N.
Step 3: Confirm the alternation
Figure 3 → 4: the rows shift down again: M N / H L / A K ✓. So the next step is a swap.
Step 4: Predict and match
Swapping each row of figure 4 gives N M / L H / K A — the figure with N M on top and K A at the bottom.""", trick=r"Shift rows down, swap sides, shift, swap → N M / L H / K A.")
S[20] = dict(raw=r"""Step 1: Count the squares
The figures show 1, 1, 2, 2 squares — each number appears twice, so the fifth figure has 3 squares.
Step 2: Look at the shading
The squares are filled, hollow, filled, hollow — shading alternates from one figure to the next.
Step 3: Combine both rules
The fifth figure comes after a hollow figure, so it is filled, and it has 3 squares.
Step 4: Match the options
The answer is three filled squares; the other figures are all hollow or mix filled and hollow squares.""", trick=r"Count 1, 1, 2, 2, 3 and shading filled/hollow alternately → three filled squares.")
