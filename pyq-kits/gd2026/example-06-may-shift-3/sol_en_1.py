S = {}
S[1] = dict(raw=r"""Step 1: Find the differences between the known terms
−772 → −767: +5; −767 → −761: +6; −761 → −754: +7; −754 → −746: +8; −746 → −737: +9.
Step 2: Spot the pattern
The differences increase by 1 each time, so the first two gaps must be +3 and +4.
Step 3: Find the missing term
\( -779 + 3 = -776 \).
Step 4: Check
\( -776 + 4 = -772 \) ✓, so the missing term is −776.""", trick=r"Differences +3, +4, +5, +6 … — work backwards from the known gaps.")
S[2] = dict(raw=r"""Step 1: Find the differences between the known terms
−66 → −76: −10; −76 → −87: −11; −87 → −99: −12.
Step 2: Spot the pattern
Each step subtracts one more than the step before: −10, −11, −12, −13, −14 …
Step 3: Find the missing term
\( -99 - 13 = -112 \).
Step 4: Check
\( -112 - 14 = -126 \) ✓, \( -126 - 15 = -141 \) ✓, \( -141 - 16 = -157 \) ✓.""", trick=r"Gaps −10, −11, −12, −13 … grow by 1.")
S[3] = dict(raw=r"""Step 1: Split each cluster into first and second letters
First letters: B, Y, ?, S, P, M, J, G. Second letters: T, P, ?, E, X, P, G, W.
Step 2: Pattern of the first letters
B (2) → Y (25) → … → S (19) → P (16) → M (13) → J (10) → G (7): −3 each time (2 − 3 = −1 → 25 = Y). So the missing first letter is 25 − 3 = 22 = V.
Step 3: Pattern of the second letters
T (20) → P (16): −4; E (5) → X (24): −7 (5 − 7 = −2 → 24); X → P: −8; P → G: −9; G (7) → W (23): −10. So the gaps are −4, −5, −6, −7 …, and the missing letter is 16 − 5 = 11 = K.
Step 4: Check and answer
K (11) − 6 = 5 = E ✓, so the missing cluster is VK.""", trick=r"First letter −3 each time; second letter −4, −5, −6 … (wrap from A back to Z).")
S[4] = dict(raw=r"""Step 1: Pattern of the first letters
W (23) → Y (25): +2; Y → B: 25 + 3 = 28 → 2 (B), +3; B → F: +4; F → K: +5; K → Q: +6.
Step 2: Find the missing first letter
Next gap is +7: Q (17) + 7 = 24 = X; check X + 8 = 32 → 6 = F ✓.
Step 3: Pattern of the second letters
U (21) → T (20): −1; T → R: −2; R → O: −3; O → K: −4; K → F: −5. Next gap −6: F (6) − 6 = 0 → 26 = Z; check Z − 7 = 19 = S ✓.
Step 4: Answer
The missing cluster is XZ.""", trick=r"First letters +2, +3, +4 …; second letters −1, −2, −3 … (wrap around the alphabet).")
S[5] = dict(raw=r"""Step 1: Find the rule in (LA, OD, SH)
First letters L (12) → O (15) → S (19): +3, +4. Second letters A (1) → D (4) → H (8): +3, +4.
Step 2: Confirm with (IX, LA, PE)
I (9) → L (12) → P (16): +3, +4 ✓. X (24) → A (24 + 3 = 27 → 1) → E (5): +3, +4 ✓.
Step 3: Test the options
(FA, ID, MH): F (6) → I (9) → M (13) is +3, +4 ✓; A (1) → D (4) → H (8) is +3, +4 ✓.
Step 4: Reject the rest
(PB, SF, WJ) has B → F (+4) first; (XN, AR, AV) has A → A (0); (UF, XJ, DN) has X → D (+6). Only (FA, ID, MH) follows the rule.""", trick=r"Both letters move +3 then +4 — check the first letters and the second letters separately.")
S[6] = dict(raw=r"""Step 1: Find the differences
466 → 565: +99; 763 → 862: +99; 862 → 961: +99.
Step 2: Spot the pattern
Every term is 99 more than the one before it.
Step 3: Find the missing term
\( 565 + 99 = 664 \).
Step 4: Check
\( 664 + 99 = 763 \) ✓, so the missing term is 664.""", trick=r"Constant gap +99 (add 100, subtract 1).")
S[7] = dict(raw=r"""Step 1: Place P and Q
P is second to the left of Q, so the order is P _ Q. With 5 seats, P can be at seat 1, 2 or 3 (counting from the left).
Step 2: Use “S is right of P and left of R”
If P = 2, Q = 4, then S = 3 and R = 5; T would be at seat 1, but then only one boy sits between S and T — rejected. If P = 3, Q = 5, then S = 4 and R has no seat to the right of S — rejected.
Step 3: Take P = 1, Q = 3
S must be at seat 2 (seat 4 would leave T at seat 1, which P already holds). Two boys between S and T puts T at seat 5, so R = 4.
Step 4: Answer
Order: P, S, Q, R, T. P and S sit side by side, so 0 boys sit between them.""", trick=r"Fix the two-gap pair (P _ Q) first, then test each position.")
S[8] = dict(raw=r"""Step 1: Fix U and use the U clues
Facing the centre, “right” means anticlockwise. Put U at a seat; V is second to the left of U (2 seats clockwise) and T is second to the right of U (2 seats anticlockwise).
Step 2: Place S and P
S sits next to both P and V. On V's side away from U there is a free seat for S, and P sits beyond S. (The seat between V and U cannot hold S, because P would then need U's seat.)
Step 3: Place R and Q
Two seats are left: one next to V and one between U and T. R is not a neighbour of V, so R sits between U and T, and Q sits next to V.
Step 4: Answer
Going anticlockwise from R: R → T → P. So P is second to the right of R.""", trick=r"Facing the centre: right = anticlockwise, left = clockwise.")
S[9] = dict(raw=r"""Step 1: Study the first pair
A pentagon in a square becomes a hexagon (one more side) in a square, with the original pentagon placed inside the hexagon.
Step 2: Write the rule
Outer shape = the given shape with one more side; inner shape = the given shape itself.
Step 3: Apply the rule to the hexagon
The answer must show a heptagon (7 sides) in a square with a hexagon inside it.
Step 4: Check the options
Figure 1 has a hexagon with a rhombus, figure 2 a hexagon with a circle, figure 3 a pentagon with a hexagon. Only figure 4 shows a heptagon with a hexagon inside.""", trick=r"Count sides: outer shape = n + 1 sides, inner shape = the original n-sided shape.")
S[10] = dict(raw=r"""Step 1: Study the first pair
3A27B → A32B7: the 1st and 2nd characters swap (3A → A3), the 3rd stays (2), and the 4th and 5th swap (7B → B7).
Step 2: Write the rule
Swap characters 1 and 2, keep character 3, swap characters 4 and 5.
Step 3: Apply the rule to J8VX7
J8 → 8J, V stays, X7 → 7X, giving 8JV7X.
Step 4: Check the options
Figure 1 shows 8JV7X ✓. The others (8J7VX, XJV78, 7JV8X) do not follow the rule.""", trick=r"Mark the positions 1-2-3-4-5 and watch which positions swap.")
S[11] = dict(raw=r"""Step 1: Study AR190 → YO690
A (1) → Y (25): −2; R (18) → O (15): −3; 190 → 690: +500.
Step 2: Confirm with YT240 → WQ740
Y (25) − 2 = W (23) ✓; T (20) − 3 = Q (17) ✓; 240 + 500 = 740 ✓.
Step 3: Work backwards from RS650
The first cluster becomes RS650, so reverse each step: R (18) + 2 = 20 = T; S (19) + 3 = 22 = V; 650 − 500 = 150.
Step 4: Answer
The required cluster is TV150.""", trick=r"Find the forward rule, then reverse it (−2 → +2, −3 → +3, +500 → −500).")
S[12] = dict(raw=r"""Step 1: Study TUV11 → OPB169
T (20) − 5 = O (15); U (21) − 5 = P (16); V (22) + 6 = 28 → 2 = B; \( (11 + 2)^{2} = 13^{2} = 169 \).
Step 2: Confirm with LMO15 → GHU289
L (12) − 5 = G (7) ✓; M (13) − 5 = H (8) ✓; O (15) + 6 = U (21) ✓; \( (15 + 2)^{2} = 17^{2} = 289 \) ✓.
Step 3: Work backwards from LOR121
L (12) + 5 = Q (17); O (15) + 5 = T (20); R (18) − 6 = L (12); \( 121 = 11^{2} \), so the number is \( 11 - 2 = 9 \).
Step 4: Answer
The required cluster is QTL9.""", trick=r"Letters −5, −5, +6; number → (n + 2)². Reverse every step to go back.")
S[13] = dict(raw=r"""Step 1: Study the first pair
\( 5945 - 5894 = 51 \), so the second number is 51 less.
Step 2: Confirm with the second pair
\( 6244 - 6193 = 51 \) ✓.
Step 3: Apply the rule
\( 3370 - 51 = 3319 \).
Step 4: Answer
The required number is 3319.""", trick=r"Same difference in both pairs → subtract 51.")
S[14] = dict(raw=r"""Step 1: Study the second pair
\( 384 - 157 = 227 \).
Step 2: Confirm with the third pair
\( 743 - 516 = 227 \) ✓.
Step 3: Apply the rule to 220
\( 220 + 227 = 447 \).
Step 4: Answer
The required number is 447.""", trick=r"Both pairs differ by 227 → add 227.")
S[15] = dict(raw=r"""Step 1: Study NOPE → OQSI
N (14) + 1 = O; O (15) + 2 = Q; P (16) + 3 = S; E (5) + 4 = I.
Step 2: Confirm with DIED → EKHH
D + 1 = E; I (9) + 2 = K; E (5) + 3 = H; D (4) + 4 = H ✓.
Step 3: Apply the rule to DUES
D + 1 = E; U (21) + 2 = W; E (5) + 3 = H; S (19) + 4 = W.
Step 4: Answer
DUES is coded as EWHW.""", trick=r"Add +1, +2, +3, +4 to the letters in order.")
S[16] = dict(raw=r"""Step 1: Study WINED → XLMBY
W (23) + 1 = X; I (9) + 3 = L; N (14) − 1 = M; E (5) − 3 = B; D (4) − 5 = −1 → 25 = Y.
Step 2: Confirm with CRAZE → DUZWZ
C + 1 = D; R (18) + 3 = U; A (1) − 1 = 0 → Z; Z (26) − 3 = W; E (5) − 5 = 0 → Z ✓.
Step 3: Apply the rule to RELAX
R (18) + 1 = S; E (5) + 3 = H; L (12) − 1 = K; A (1) − 3 = −2 → 24 = X; X (24) − 5 = 19 = S.
Step 4: Answer
RELAX is coded as SHKXS.""", trick=r"Pattern +1, +3, −1, −3, −5; wrap around below A.")
S[17] = dict(raw=r"""Step 1: Check the numbers
169, 196, 225, 256, 289, 324 are \( 13^{2}, 14^{2}, 15^{2}, 16^{2}, 17^{2}, 18^{2} \) — all correct.
Step 2: Check the second letters
Q (17), N (14), K (11), H (8), E (5), B (2): −3 each time — all correct.
Step 3: Check the first letters
W (23), C (29 → 3), I (35 → 9), O (41 → 15): +6 each time. Going back, the term before W should be 23 − 6 = 17 = Q, and K (11) + 6 = 17 = Q.
Step 4: Find the wrong term
The second term starts with R instead of Q; it should be QN196. So RN196 is wrong.""", trick=r"Check numbers, second letters and first letters one by one — the odd step shows the wrong term.")
S[18] = dict(raw=r"""Step 1: Check the numbers
\( 40 \times 1.5 = 60 \), \( 60 \times 1.5 = 90 \), \( 90 \times 1.5 = 135 \), \( 135 \times 1.5 = 202.5 \) — all correct.
Step 2: Check the first and third letters
First: B, E, H, K, N (+3) ✓. Third: X (24), E (31 → 5), L (12), S (19), Z (26): +7 each time ✓.
Step 3: Check the second letters
O (15) → T (20) → Y (25): +5 each time. Next should be 25 + 5 = 30 → 4 = D, then D + 5 = I ✓ (NIZ). But KES has E, not D.
Step 4: Find the wrong term
The correct term is KDS135, so KES135 is wrong.""", trick=r"Test each position separately: first +3, second +5, third +7, number × 1.5.")
S[19] = dict(raw=r"""Step 1: Write the angle formula
Angle between the hands \( = \left| 30h - \dfrac{11}{2}m \right| \), where h = 3.
Step 2: Set the angle to 180° (opposite hands)
After 3:15 the minute hand is ahead, so \( \dfrac{11}{2}m - 90 = 180 \).
Step 3: Solve
\( \dfrac{11}{2}m = 270 \Rightarrow m = \dfrac{540}{11} = 49\dfrac{1}{11} \) minutes.
Step 4: Answer
The hands are opposite at about 3:49 PM.""", trick=r"Opposite hands: \( \dfrac{11}{2}m = 30h + 180 \) (or \( 30h - 180 \)).")
S[20] = dict(raw=r"""Step 1: Find how much time must be gained
The watch is 6 minutes slow, so it must gain \( 6 \times 60 = 360 \) seconds.
Step 2: Use the rate
It gains 12 seconds every hour.
Step 3: Find the hours needed
\( 360 \div 12 = 30 \) hours.
Step 4: Add to the start time
7 AM + 30 hours = 7 AM next day + 6 hours = 1 PM (the next day). So it shows the correct time at 1:00 PM.""", trick=r"Hours needed = time to make up ÷ gain per hour.")
