S = {}
S[1] = dict(raw=r"""Step 1: Find the differences between neighbouring terms
−557 → −562: −5; −562 → −569: −7; −569 → −576: −7; −576 → −583: −7; −583 → −590: −7; −590 → −597: −7; −597 → −604: −7.
Step 2: Spot the rule
Every gap except the first is −7, so the series falls by 7 at each step.
Step 3: Find the correct first term
Working back from −562: −562 + 7 = −555.
Step 4: Name the wrong term
The series should start at −555, so −557 is the wrong term; all other terms fit −7.""", trick=r"When only one gap breaks the pattern, the wrong term sits at that gap.")
S[2] = dict(raw=r"""Step 1: Find the differences
−199 → −202: −3; −202 → −207: −5; −207 → −214: −7; −214 → −223: −9.
Step 2: Spot the rule
The gaps are consecutive odd numbers: −3, −5, −7, −9, so the next gaps are −11, −13, −15.
Step 3: Find the missing term
−223 − 11 = −234.
Step 4: Check
−234 − 13 = −247 ✓ and −247 − 15 = −262 ✓, so the missing term is −234.""", trick=r"Gaps −3, −5, −7, −9 … keep adding the next odd number.")
S[3] = dict(raw=r"""Step 1: Look at the first letters
Y (25), D (4), I (9), N (14), S (19), X (24), C (3): each is +5 (25 + 5 = 30 → 30 − 26 = 4 = D, and 24 + 5 = 29 → 3 = C).
Step 2: Look at the second letters
R (18), M (13), H (8), C (3), X (24), S (19), N (14): each is −5 (3 − 5 = −2 → 24 = X).
Step 3: Find the next term
First letter: C (3) + 5 = 8 = H. Second letter: N (14) − 5 = 9 = I.
Step 4: Answer
The missing term is HI.""", trick=r"First letter +5, second letter −5; wrap around after Z and before A.")
S[4] = dict(raw=r"""Step 1: Look at the first letters
I (9), K (11), N (14), P (16), S (19), ?, X (24), Z (26): gaps +2, +3, +2, +3, so the next is +2 → S (19) + 2 = 21 = U; then U + 3 = X ✓ and X + 2 = Z ✓.
Step 2: Look at the second letters
P (16), N (14), K (11), G (7), B (2): gaps −2, −3, −4, −5, so the next gap is −6.
Step 3: Find the missing second letter
B (2) − 6 = −4 → −4 + 26 = 22 = V; then V (22) − 7 = 15 = O ✓ and O (15) − 8 = 7 = G ✓.
Step 4: Answer
The missing term is UV.""", trick=r"First letters alternate +2, +3; second letters fall by 2, 3, 4, 5, 6 …")
S[5] = dict(raw=r"""Step 1: Find the rule in (YS, BW, FB)
First letters: Y (25) → B (2): +3; B → F (6): +4. Second letters: S (19) → W (23): +4; W (23) → B (2): +5.
Step 2: Confirm with (QW, TA, XF)
Q (17) → T (20): +3; T → X (24): +4. W (23) → A (1): +4; A → F (6): +5 ✓.
Step 3: Test the options
(CA, FE, JJ): C (3) → F (6) +3, F → J (10) +4; A (1) → E (5) +4, E → J (10) +5 ✓. (FW, GA, NF) fails at once: F → G is only +1. (DS, HW, IB): D → H is +4, not +3. (IZ, KD, QI): I → K is +2.
Step 4: Answer
Only (CA, FE, JJ) follows +3, +4 on the first letters and +4, +5 on the second letters.""", trick=r"Write two rules: first letters +3, +4; second letters +4, +5.")
S[6] = dict(raw=r"""Step 1: Find the differences among the known terms
−568 → −498: +70; −498 → −428: +70; −428 → −358: +70; −358 → −288: +70; −288 → −218: +70.
Step 2: Spot the rule
The series rises by 70 at every step.
Step 3: Find the missing term
−708 + 70 = −638.
Step 4: Check
−638 + 70 = −568 ✓, so the missing term is −638.""", trick=r"Constant gap +70: the missing term is first term + 70.")
S[7] = dict(raw=r"""Step 1: Fix C
Five seats 1 to 5 from left to right (all face north). C is in the middle, so C is at seat 3.
Step 2: Place the left and right groups
A and B are to the left of C (seats 1, 2); D and E are to the right of C (seats 4, 5).
Step 3: Use "B and D are not at the ends"
B cannot be at seat 1, so B = 2 and A = 1. D cannot be at seat 5, so D = 4 and E = 5.
Step 4: Answer
Order: A, B, C, D, E. The person at the right end is E.""", trick=r"Facing north, your right is the reader's right — seat 5 is the right end.")
S[8] = dict(raw=r"""Step 1: Set the direction rule
All face the centre, so "left" means moving clockwise and "right" means anticlockwise. Number seats 0 to 6 clockwise and put U at 0.
Step 2: Place V and T
V is second to the left of U → seat 2. T is second to the right of U → seat 5 (two anticlockwise steps).
Step 3: Place S, P, Q and R
S sits next to both P and V. Seat 1 is between U and V, so P cannot be beside S there; hence S = 3 and P = 4. Q and R take seats 1 and 6. R is not next to V, so R ≠ 1 → R = 6, Q = 1.
Step 4: Count from S towards its left
Clockwise from S (3): P (4), T (5), then R (6). Between S and R sit P and T, that is, 2 girls.""", trick=r"Facing the centre: left = clockwise. Fix one person first, then place the 'second to left/right' clues.")
S[9] = dict(raw=r"""Step 1: Study the first pair
The first box has 3 horizontal double-headed arrows. The second box keeps them and adds 3 vertical double-headed arrows, making a 3 × 3 grid of arrows.
Step 2: State the rule
Keep the given arrows and add the same number of double-headed arrows in the perpendicular direction.
Step 3: Apply it to the third box
The third box has 3 vertical double-headed arrows, so the answer must add 3 horizontal double-headed arrows — 6 arrows in all, every one with a head at both ends.
Step 4: Reject the near misses
One option has only 2 vertical arrows; one has a horizontal arrow with a single head; one has a vertical arrow with a single head. Only the figure with 3 complete vertical and 3 complete horizontal double-headed arrows fits.""", trick=r"Count the arrows AND check both heads of every arrow.")
S[10] = dict(raw=r"""Step 1: Study the first pair
Figure 1: 2 (top), 4 (right), 7 (bottom), 6 (left). Figure 2: 7 (top), 6 (right), 2 (bottom), and a mirrored 4 (left).
Step 2: State the rule
Top and bottom swap; left and right swap. The element that moves from the right to the left is shown as its mirror image; the others stay upright.
Step 3: Apply it to R (top), F (right), P (bottom), S (left)
Top ↔ bottom: P goes to the top and R to the bottom (upright). Left ↔ right: S goes to the right (upright) and F goes to the left, mirrored.
Step 4: Pick the figure
The answer shows P at the top, a mirrored F on the left, S on the right and an upright R at the bottom. The other figures mirror R, put S on top, or turn F upside down.""", trick=r"Opposite positions swap; copy exactly which element gets mirrored in the example.")
S[11] = dict(raw=r"""Step 1: Find the letter rule in AE80 → DZ40
Reverse the letters: AE → EA. Then move each one step back: E → D, A → Z. So AE → DZ.
Step 2: Find the number rule and confirm with TK60 → JS20
80 → 40 and 60 → 20: subtract 40. TK reversed is KT; K → J and T → S gives JS ✓.
Step 3: Apply to LP70
Reverse: PL. One step back: P → O, L → K → OK. Number: 70 − 40 = 30.
Step 4: Answer
LP70 is related to OK30.""", trick=r"Reverse the pair, step each letter back by 1, subtract 40.")
S[12] = dict(raw=r"""Step 1: Find the rule in IK13 → OS168
I (9) → O (15): +6; K (11) → S (19): +8; 13 → 168 = \( 13^{2} - 1 \).
Step 2: Confirm with JH15 → PP224
J (10) + 6 = P (16); H (8) + 8 = P (16); \( 15^{2} - 1 = 224 \) ✓.
Step 3: Apply to DC11
D (4) + 6 = 10 = J; C (3) + 8 = 11 = K; \( 11^{2} - 1 = 120 \).
Step 4: Answer
DC11 is related to JK120.""", trick=r"Letters +6, +8; number n → n² − 1.")
S[13] = dict(raw=r"""Step 1: Find the rule in the first pair
3691 − 3641 = 50, so the second number = first number + 50.
Step 2: Confirm with the second pair
1767 − 1717 = 50 ✓.
Step 3: Work backwards for the missing number
Here the second number 5946 is given, so the first number = 5946 − 50.
Step 4: Answer
5946 − 50 = 5896.""", trick=r"Second = first + 50, so first = second − 50.")
S[14] = dict(raw=r"""Step 1: Find the rule in the first pair
1272 − 798 = 474, so the second number = first number + 474.
Step 2: Confirm with the second pair
1052 − 578 = 474 ✓.
Step 3: Work backwards
First number = 889 − 474.
Step 4: Answer
889 − 474 = 415.""", trick=r"Same constant gap in both pairs → subtract it from the given second number.")
S[15] = dict(raw=r"""Step 1: Find the rule in NAME → OFLZ
N (14) → O (15): +1; A (1) → F (6): +5; M (13) → L (12): −1; E (5) → Z (26): −5 (5 − 5 = 0 → 26).
Step 2: Confirm with GOAT → HTZO
G → H (+1), O (15) → T (20) (+5), A (1) → Z (26) (−1), T (20) → O (15) (−5) ✓.
Step 3: Apply +1, +5, −1, −5 to VOID
V (22) + 1 = W; O (15) + 5 = T; I (9) − 1 = H; D (4) − 5 = −1 → 25 = Y.
Step 4: Answer
VOID is coded as WTHY.""", trick=r"Pattern +1, +5, −1, −5 by position.")
S[16] = dict(raw=r"""Step 1: Test reverse letter positions (A = 26, B = 25, …, Z = 1) on MUST
M = 14, U = 6, S = 8, T = 7 → 14 + 6 + 8 + 7 = 35 ✓.
Step 2: Confirm with PAUZE
P = 11, A = 26, U = 6, Z = 1, E = 22 → 11 + 26 + 6 + 1 + 22 = 66 ✓.
Step 3: Apply to SOAP
S = 8, O = 12, A = 26, P = 11.
Step 4: Add
8 + 12 + 26 + 11 = 57, so SOAP is coded as 57.""", trick=r"Reverse position = 27 − normal position; add them up.")
S[17] = dict(raw=r"""Step 1: First letters
A (1), G (7), M (13), S (19), Y (25): +6 each, so the next is 25 + 6 = 31 → 5 = E.
Step 2: Second letters
Z (26), W (23), T (20), Q (17), N (14): −3 each, so the next is 14 − 3 = 11 = K.
Step 3: Numbers
1, 4, 9, 16, 25 are \( 1^{2}, 2^{2}, 3^{2}, 4^{2}, 5^{2} \), so the next is \( 6^{2} = 36 \).
Step 4: Name the wrong term
The last term should be EK36, but the series shows FJ49. So FJ49 is the wrong term.""", trick=r"Check each part separately: +6, −3 and perfect squares.")
S[18] = dict(raw=r"""Step 1: First letters
G (7) → A (1) → U (21) → O (15): −6 each (1 − 6 = −5 → 21), so the next is 15 − 6 = 9 = I.
Step 2: Second letters
U (21) → O (15) → I (9) → C (3): −6 each, so the next is 3 − 6 = −3 → 23 = W.
Step 3: Third letters
X (24) → R (18) → L (12) → F (6): −6 each, so the next is 6 − 6 = 0 → 26 = Z.
Step 4: Numbers and answer
797 → 716 → 635 → 554: −81 each, so the next is 554 − 81 = 473. The missing term is IWZ473.""", trick=r"Every letter −6, the number −81.")
S[19] = dict(raw=r"""Step 1: Use the angle formula
Angle between the hands \( = |30H - 5.5M| \), with H = 4.
Step 2: Set the angle to 180°
The hands are opposite when the angle is 180°: \( 5.5M - 120 = 180 \).
Step 3: Solve for M
\( 5.5M = 300 \Rightarrow M = \dfrac{300}{5.5} = 54\dfrac{6}{11} \) minutes.
Step 4: Round
\( 54\dfrac{6}{11} \) minutes past 4 is about 4:55.""", trick=r"Opposite hands: \( M = \dfrac{2}{11}(30H + 180) \) when the minute hand is ahead.")
S[20] = dict(raw=r"""Step 1: Find the time that passes
From 3 AM to 9 AM = 6 hours = \( 6 \times 60 = 360 \) minutes.
Step 2: Find how many 2-minute blocks there are
\( \dfrac{360}{2} = 180 \) blocks.
Step 3: Find the total gain
1 second per block → 180 seconds = 3 minutes.
Step 4: Find the time shown
The clock runs fast, so it shows 9:00 + 3 minutes = 9:03 AM.""", trick=r"Gain = (minutes passed ÷ 2) seconds.")
