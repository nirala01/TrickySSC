S = {}
S[1] = dict(raw=r"""Step 1: Compare neighbouring terms
4096 → 2048 is ÷2; 2048 → 512 is ÷4; 512 → 256 is ÷2; 256 → 64 is ÷4; 64 → 32 is ÷2.
Step 2: Spot the rule
The divisors alternate ÷2, ÷4, ÷2, ÷4 …, so the next step is ÷4.
Step 3: Find the missing term
\( 32 \div 4 = 8 \).
Step 4: Check with the last term
The step after that is ÷2: \( 8 \div 2 = 4 \) ✓, which is the given last term.""", trick=r"Alternate ÷2, ÷4 — write the divisor under every gap.")
S[2] = dict(raw=r"""Step 1: Write the letter positions
Y = 25, E = 5, Q = 17, W = 23, C = 3, I = 9, O = 15.
Step 2: Find the gap
Y (25) + 6 = 31 → 31 − 26 = 5 = E. Q (17) + 6 = 23 = W, W (23) + 6 = 29 → 3 = C, C + 6 = 9 = I, I + 6 = 15 = O.
Step 3: Find the missing letter
E (5) + 6 = 11 = K.
Step 4: Check
K (11) + 6 = 17 = Q ✓, so the missing letter is K.""", trick=r"Constant +6; after Z go back to A (subtract 26).")
S[3] = dict(raw=r"""Step 1: Find the rule in PS → SX
P (16) + 3 = S (19); S (19) + 5 = X (24).
Step 2: Confirm with XT → AY
X (24) + 3 = 27 → 1 = A; T (20) + 5 = 25 = Y ✓.
Step 3: Work backwards for ? → DK
First letter: D (4) − 3 = 1 = A. Second letter: K (11) − 5 = 6 = F.
Step 4: Answer
The missing cluster is AF (A + 3 = D, F + 5 = K).""", trick=r"Find the rule forward, then undo it (−3, −5) to get the first cluster.")
S[4] = dict(raw=r"""Step 1: Find the rule from VA to BZ
First letter: V (22) + 6 = 28 → 2 = B. Second letter: A (1) → Z (26), its opposite letter (1 + 26 = 27).
Step 2: Confirm with LI to RR
L (12) + 6 = 18 = R ✓. I (9) → R (18), and 9 + 18 = 27, so R is the opposite letter of I ✓.
Step 3: Apply the rule to GY
First letter: G (7) + 6 = 13 = M. Second letter: opposite of Y (25) is 27 − 25 = 2 = B.
Step 4: Answer
GY is related to MB.""", trick=r"Opposite letters add up to 27: A–Z, I–R, Y–B.")
S[5] = dict(raw=r"""Step 1: Look at the first letters
L, O, R, U, ?, A, D, G: each is +3 (L 12 → O 15 → R 18 → U 21).
Step 2: Look at the second letters
J, G, D, A, ?, U, R, O: each is −3 (J 10 → G 7 → D 4 → A 1).
Step 3: Find the missing term
First letter: U (21) + 3 = 24 = X. Second letter: A (1) − 3 = −2 → 24 = X.
Step 4: Check
X + 3 = 27 → A ✓ and X − 3 = U ✓, so the missing term is XX.""", trick=r"First letter +3, second letter −3; wrap around at both ends.")
S[6] = dict(raw=r"""Step 1: Find the rule in (TK, PE, LY)
First letters: T (20) → P (16) → L (12): −4 each time. Second letters: K (11) → E (5) → Y (25): −6 each time (5 − 6 = −1 → 25).
Step 2: Confirm with (KF, GZ, CT)
K → G → C: −4; F (6) → Z (26) → T (20): −6 ✓.
Step 3: Test the options
(RV, NP, JJ): R (18) → N (14) → J (10) is −4; V (22) → P (16) → J (10) is −6 ✓. (RB, NX, IR) fails because N → I is −5; (LU, HQ, EK) fails because H → E is −3; (BW, XS, OM) fails because X → O is −9.
Step 4: Answer
Only (RV, NP, JJ) follows −4 on the first letters and −6 on the second letters.""", trick=r"Two rules: first letters −4, second letters −6.")
S[7] = dict(raw=r"""Step 1: Identify the next year
The next year after a leap year is an ordinary year, so its February has 28 days.
Step 2: Count the weeks
28 days = exactly 4 weeks, so every weekday occurs exactly 4 times, whatever day 1 February is.
Step 3: Count the two days asked
Wednesdays = 4 and Sundays = 4.
Step 4: Add
\( 4 + 4 = 8 \). (The date 25 December is extra information.)""", trick=r"A 28-day February has every weekday exactly 4 times.")
S[8] = dict(raw=r"""Step 1: Count the days from 5 September 2015 to 5 February 2016
September: 30 − 5 = 25; October 31; November 30; December 31; January 31; February 5.
Step 2: Add them
\( 25 + 31 + 30 + 31 + 31 + 5 = 153 \) days.
Step 3: Find the odd days
\( 153 \div 7 \) = 21 weeks and 6 days, so there are 6 odd days.
Step 4: Move forward
Saturday + 6 days = Friday.""", trick=r"Odd days = total days ÷ 7 remainder; Saturday + 6 = Friday (or Saturday − 1).")
S[9] = dict(raw=r"""Step 1: Place D
Only C and F are to the left of D, so D is third from the left.
Step 2: Place G and H
Only H is to the right of G, so H is at the right end (fifth) and G is fourth.
Step 3: Place F and C
F is at an end; the right end is taken, so F is first and C is second.
Step 4: Answer
Order: F, C, D, G, H. Between D and H sits only G, so 1 person.""", trick=r"'Only X is to the right of Y' fixes X at the end and Y next to it.")
S[10] = dict(raw=r"""Step 1: Read "R is taller than only four girls"
Out of six girls, R is taller than four, so exactly one girl is taller than R — R is second tallest.
Step 2: Find the tallest
U is taller than S and P, and S, P are taller than Q and T, so U is taller than four girls. U cannot be below R, so U is the tallest.
Step 3: Fix the order
U > R > (S, P) > (Q, T). T is among the two shortest.
Step 4: Find R's possible height
R is taller than T (140 cm), so R must be more than 140 cm. Only 168 cm is possible.""", trick=r"'Taller than only four' out of six = second tallest.")
S[11] = dict(raw=r"""Step 1: Compare the first two figures
Top row: triangle (left) and circle (right) become circle (left) and triangle (right). Bottom row: rectangle (left) and square (right) become square (left) and rectangle (right).
Step 2: Find the rule
Every left element swaps with the element on its right — the figure is mirrored left to right.
Step 3: Apply it to the third figure
Triangle (top left) ↔ K (top right), R (bottom left) ↔ T (bottom right). The result is K, triangle on top and T, R below.
Step 4: Check the options
Only the figure with K and triangle on top and T and R below matches; the one keeping R, T unchanged misses the bottom swap.""", trick=r"Check both rows — the bottom row swaps too (rectangle and square).")
S[12] = dict(raw=r"""Step 1: Locate the letters of the first figure
Top row: B, A (centre, right); middle: R (right); bottom: D, F (centre, right).
Step 2: Compare with the second figure
Middle row: D (left), B (right); bottom row: F, R, A. This is the first figure turned 90° clockwise (the right column becomes the bottom row, the bottom row becomes the left column).
Step 3: Turn the third figure 90° clockwise
Left column J, M, O (top to bottom) becomes the top row O, M, J; the bottom row O, L, N becomes the left column, so L comes below O and N at the bottom left.
Step 4: Answer
The figure shows O M J on top, L in the middle-left and N at the bottom-left.""", trick=r"In a 90° clockwise turn, the left column becomes the top row read from bottom to top.")
S[13] = dict(raw=r"""Step 1: Find the rule from KO825 to HK425
K (11) − 3 = H (8); O (15) − 4 = K (11); 825 − 400 = 425.
Step 2: Confirm with HF916 to EB516
H − 3 = E; F (6) − 4 = B (2); 916 − 400 = 516 ✓.
Step 3: Work backwards from CT428
First letter: C (3) + 3 = F (6). Second letter: T (20) + 4 = X (24). Number: 428 + 400 = 828.
Step 4: Answer
The missing cluster is FX828.""", trick=r"Rule −3, −4, −400 forward; undo it with +3, +4, +400.")
S[14] = dict(raw=r"""Step 1: Find the rule from GKN11 to CGJ121
Each letter −4: G → C, K → G, N → J. Number: \( 11^{2} = 121 \).
Step 2: Confirm with LMF13 to HIB169
L → H, M → I, F → B (each −4); \( 13^{2} = 169 \) ✓.
Step 3: Apply to OSR15
O (15) − 4 = K, S (19) − 4 = O, R (18) − 4 = N; \( 15^{2} = 225 \).
Step 4: Answer
The missing cluster is KON225.""", trick=r"Letters −4, number squared.")
S[15] = dict(raw=r"""Step 1: Find the rule in 13 → 242
\( 242 - 13 = 229 \).
Step 2: Confirm with 138 → 367
\( 367 - 138 = 229 \) ✓, so the second number is the first plus 229.
Step 3: Apply it to 608
\( 608 + 229 = 837 \).
Step 4: Answer
The missing number is 837.""", trick=r"Same difference in both given pairs → add it.")
S[16] = dict(raw=r"""Step 1: Compare TILE with UKKA
T → U (+1), I → K (+2), L → K (−1), E → A (−4).
Step 2: Confirm with NUMB → OWLX
N → O (+1), U → W (+2), M → L (−1), B (2) → X (24) (−4, wrapping) ✓.
Step 3: Apply +1, +2, −1, −4 to NOTE
N → O, O → Q, T → S, E → A.
Step 4: Answer
NOTE is coded as OQSA.""", trick=r"Pattern +1, +2, −1, −4 by position.")
S[17] = dict(raw=r"""Step 1: Find the time passed
7 AM to 7 PM = 12 hours = \( 12 \times 60 = 720 \) minutes.
Step 2: Count the 3-minute blocks
\( 720 \div 3 = 240 \) blocks.
Step 3: Find the total gain
\( 240 \times 2 = 480 \) seconds = 8 minutes.
Step 4: Read the clock
The clock runs fast, so it shows 7 PM + 8 minutes = 7:08:00 PM.""", trick=r"Gain = (minutes passed ÷ 3) × 2 seconds.")
S[18] = dict(raw=r"""Step 1: Watch each corner box
Each of the four corner boxes is half black and half white; note where the white half is.
Step 2: Track the changes
Figure 1 → 2: only the top-left box flips (white top → white bottom). 2 → 3: only the top-right box flips. 3 → 4: only the bottom-left box flips. So the boxes change one at a time in the order top-left, top-right, bottom-left.
Step 3: Find the next change
The next box to change is the bottom-right one, so its white half moves from the right side to the left side; the other three stay as in figure 4.
Step 4: Answer
The answer has top-left white at the bottom, top-right white at the top, bottom-left white at the top and bottom-right white on the left.""", trick=r"One corner changes per step — find which corner has not changed yet.")
S[19] = dict(raw=r"""Step 1: Read each figure as a ring of six places
Top row left to right, then bottom row right to left. Figure 1: K, C, T, M, N, H.
Step 2: Compare figure 1 with figure 2
Every letter moves one place clockwise (H goes to top-left, K to top-centre, T to bottom-right, M to bottom-centre, N to bottom-left) and the letter reaching the top-right is a new one (R).
Step 3: Apply to figure 4 (M N A / T R F)
Clockwise move: T → top-left, M → top-centre, a new letter at top-right; A → bottom-right, F → bottom-centre, R → bottom-left.
Step 4: Answer
The next figure is T M (new letter) on top and R F A below, which is the figure T M D / R F A.""", trick=r"Letters rotate one step clockwise; only the top-right letter is replaced.")
S[20] = dict(raw=r"""Step 1: Write the present ages
Let the ages be \( 7x \) and \( 12x \).
Step 2: Use the sum
\( 7x + 12x = 19x = 57 \Rightarrow x = 3 \), so the ages are 21 and 36 years.
Step 3: Go 6 years back
\( 21 - 6 = 15 \) and \( 36 - 6 = 30 \).
Step 4: Find the ratio
\( 15 : 30 = 1 : 2 \).""", trick=r"Ratio sum 7 + 12 = 19 parts = 57 → 1 part = 3.")
