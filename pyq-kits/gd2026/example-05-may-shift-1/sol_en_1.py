S = {}
S[1] = dict(raw=r"""Step 1: Convert the letters to positions
K = 11, F = 6, Y = 25, T = 20, ?, H = 8, A = 1, V = 22, O = 15.
Step 2: Find the pattern
K → F is −5, F → Y is −7 (6 − 7 = −1, wraps round to 25), Y → T is −5. The steps alternate −5, −7.
Step 3: Find the missing term
After T comes a −7 step: 20 − 7 = 13 = M.
Step 4: Check the rest
M (13) − 5 = H (8) ✓, H − 7 = A (1) ✓, A − 5 wraps to V (22) ✓, V − 7 = O (15) ✓. So the missing letter is M.""", trick=r"Alternate steps of −5 and −7 (wrap round after A).")
S[2] = dict(raw=r"""Step 1: Study EQ → ZK
E (5) − 5 = 0 → wraps round to Z (26); Q (17) − 6 = K (11). So the first letter moves 5 back and the second 6 back.
Step 2: Confirm with CJ → XD
C (3) − 5 = −2 → X (24); J (10) − 6 = D (4) ✓ — the same −5, −6 rule.
Step 3: Work back from IR
The missing cluster ? must give I and R after −5 and −6. First letter = I (9) + 5 = N (14). Second letter = R (18) + 6 = X (24).
Step 4: Answer and check
The missing cluster is NX. Check: N − 5 = I and X − 6 = R ✓. PX gives K and R, PY gives K and S, NY gives I and S — all fail.""", trick=r"Find the shift from a complete pair (−5, −6), then go backwards (+5, +6) from IR.")
S[3] = dict(raw=r"""Step 1: Read the first set (HA, JC, OH)
First letters H → J → O move +2 then +5. Second letters A → C → H also move +2 then +5.
Step 2: Confirm with (QC, SE, XJ)
Q → S → X is +2, +5 and C → E → J is +2, +5 ✓
Step 3: Test the options
(EI, GK, LP): E → G → L is +2, +5 and I → K → P is +2, +5 ✓
(KO, MT, NY) has O → T (+5) first; (FC, HH, HM) has H → H (0); (DV, FA, JF) has F → J (+4) — all break the rule.
Step 4: Answer
The set (EI, GK, LP) follows the same +2, +5 rule.""", trick=r"Check first letters and second letters separately — here +2, then +5.")
S[4] = dict(raw=r"""Step 1: Read the first set (QT, LN, GH)
First letters Q → L → G move 5 back each time. Second letters T → N → H move 6 back each time.
Step 2: Confirm with (AU, VO, QI)
A → V (wraps round) → Q is −5, −5 and U → O → I is −6, −6 ✓
Step 3: Test the options
(KD, FX, AR): K → F → A is −5, −5 and D → X (4 − 6 = −2, wraps to 24) → R is −6, −6 ✓
(OJ, ME, IY) starts O → M (−2); (XH, PC, IW) starts X → P (−8); (CG, WB, NV) has G → B (−5) in the second letters — all break the rule.
Step 4: Answer
The set (KD, FX, AR) follows the same −5, −6 rule.""", trick=r"First letters −5, second letters −6; remember to wrap round after A.")
S[5] = dict(raw=r"""Step 1: Count the days after 19 June 2024
June: 30 − 19 = 11 days; July 31, August 31, September 30, October 31, November 30; December up to 25 = 25 days.
Step 2: Add them
11 + 31 + 31 + 30 + 31 + 30 + 25 = 189 days.
Step 3: Find the odd days
189 ÷ 7 = 27 weeks exactly, so the odd days = 0.
Step 4: Answer
With 0 odd days the day stays the same, so 25 December 2024 is also a Saturday (as per the given data).""", trick=r"Odd days = total days mod 7; 0 odd days → same day.")
S[6] = dict(raw=r"""Step 1: Fix the given day
31 January 2019 is a Wednesday (as given).
Step 2: Count days to 30 June 2019
2019 is not a leap year: February 28 + March 31 + April 30 + May 31 + June 30 = 150 days.
Step 3: Find the odd days
150 ÷ 7 leaves remainder 3, so 30 June is 3 days after Wednesday = Saturday.
Step 4: Last Wednesday of June
Going back from Saturday 30 June: Friday 29, Thursday 28, Wednesday 27. The last Wednesday is 27 June.""", trick=r"Find the weekday of the month's last date, then step back to the required day.")
S[7] = dict(raw=r"""Step 1: Set up seat numbers
The girls face away from the centre. Number the seats 0–6 so that one seat to a girl's right is +1 (and to her left −1). Put X at 0; W is second to the left of X → W = 5.
Step 2: Place B and C
B and C are W's neighbours, so they take seats 4 and 6. Z is fourth to the left of B: if B = 4, Z = 0, which is X's seat — impossible. So B = 6, C = 4 and Z = 6 − 4 = 2.
Step 3: Place Y and A
Seats 1 and 3 are left. Y is not next to C (seat 4), so Y ≠ 3; hence Y = 1 and A = 3.
Step 4: Check the statements
I: B (6) has neighbours W (5) and X (0) ✓. II: the seat immediately to W's left is 5 − 1 = 4 = C ✓. Both statements are correct.""", trick=r"Use seat numbers (right = +1, left = −1) and test the two possible places for B.")
S[8] = dict(raw=r"""Step 1: Fix U, R and T
All face the centre. T is second to the right of U and R is a neighbour of both T and U, so R sits between them: U, R, T going to the right.
Step 2: Place V
V is second to the left of U, so one seat lies between V and U on U's left.
Step 3: Place S, P and Q
S is next to V and also next to P. The seat between V and U cannot be S (then P would have to sit next to U or V, both taken), so S sits on V's other side, P next to S, and Q fills the seat between V and U.
Step 4: Answer
Going to the right from Q: Q, U, R, T, P, S, V. Going to Q's left: V (1st), S (2nd), P (3rd). So P is third to the left of Q.""", trick=r"Fix the two people with known distances from one person (U), then fill the gaps.")
S[9] = dict(raw=r"""Step 1: Set the direction
The boys face away from the centre. Number the seats 0–6 so that one seat to anyone's right is +1. Put G at 0.
Step 2: Place F, C and B
F is fifth to the right of G → seat 5. C is fourth to the left of G → seat −4 = 3. B is next to both F (5) and G (0), so B = 6.
Step 3: Place A, D and E
A is second to the left of B → seat 4. Seats 1 and 2 are left for D and E; D is not next to C (seat 3), so D = 1 and E = 2.
Step 4: Answer
E (2) is 3 seats to the left of F (5) — E is third to the left of F.""", trick=r"Use seat numbers (right = +1) and convert 'nth to the left' into −n.")
S[10] = dict(raw=r"""Step 1: List the letters of EXPLANATION
E, X, P, L, A, N, A, T, I, O, N.
Step 2: Check PLAN, AXLE and LATE
PLAN uses P, L, A, N ✓; AXLE uses A, X, L, E ✓; LATE uses L, A, T, E ✓.
Step 3: Check CAT
CAT needs the letter C, which is not in EXPLANATION.
Step 4: Answer
CAT cannot be formed.""", trick=r"Look for a letter that is missing from the given word — here C.")
S[11] = dict(raw=r"""Step 1: Count the letters of CONSIDERATION
C 1, O 2, N 2, S 1, I 2, D 1, E 1, R 1, A 1, T 1.
Step 2: Check DONATION, RATION and CONSIDER
Each uses only available letters within these counts ✓
Step 3: Check DENOMINATION
It needs the letter M (and three N's), which CONSIDERATION does not have.
Step 4: Answer
DENOMINATION cannot be formed.""", trick=r"Look for a missing letter (M) or a letter used more times than available.")
S[12] = dict(raw=r"""Step 1: Write the equations
Let cows = c and hens = h. Heads: \( c + h = 50 \). Legs: \( 4c + 2h = 140 \).
Step 2: Remove h
Multiply the first by 2: \( 2c + 2h = 100 \). Subtract from the legs equation: \( 2c = 40 \).
Step 3: Solve
\( c = 20 \), so \( h = 50 - 20 = 30 \).
Step 4: Check
Legs \( = 4 \times 20 + 2 \times 30 = 80 + 60 = 140 \) ✓. There are 30 hens.""", trick=r"Cows = (legs − 2 × heads) ÷ 2 = (140 − 100) ÷ 2 = 20; hens = 50 − 20.")
S[13] = dict(raw=r"""Step 1: Spot the rule
0, 1, 1, 2, 3, 5, 8 … each term is the sum of the two before it (Fibonacci series).
Step 2: Check each term
0 + 1 = 1, 1 + 1 = 2, 1 + 2 = 3, 2 + 3 = 5, 3 + 5 = 8 ✓
Step 3: Find the break
5 + 8 = 13, but the series shows 12. Then 8 + 13 = 21 ✓ and 13 + 21 = 34 ✓.
Step 4: Answer
12 is the wrong number; it should be 13.""", trick=r"Fibonacci: each term = sum of the previous two.")
S[14] = dict(raw=r"""Step 1: Try multiplying by 2, 3, 4, 5 …
5 × 2 = 10, 13 − 10 = 3; 13 × 3 = 39, 44 − 39 = 5; 44 × 4 = 176, 183 − 176 = 7.
Step 2: Continue
183 × 5 = 915, 926 − 915 = 11. The added numbers 3, 5, 7, 11 are consecutive primes.
Step 3: Next term
Multiply by 6 and add the next prime 13: 926 × 6 + 13 = 5556 + 13.
Step 4: Answer
= 5569.""", trick=r"× 2, × 3, × 4 … and add 3, 5, 7, 11, 13 (primes).")
S[15] = dict(raw=r"""Step 1: Number part
2, 9, 28, 65, 126 = 1³ + 1, 2³ + 1, 3³ + 1, 4³ + 1, 5³ + 1. Next = 6³ + 1 = 217.
Step 2: Letter part
B (2), D (4), G (7), K (11), P (16): the gaps are +2, +3, +4, +5.
Step 3: Next letter
16 + 6 = 22 = V.
Step 4: Answer
The next term is 217V.""", trick=r"Numbers n³ + 1; letter gaps grow by 1.")
S[16] = dict(raw=r"""Step 1: Study TVP250 → SYW470
Reverse TVP to PVT and move each letter +3: P → S, V → Y, T → W, giving SYW. The number goes 250 → 470, i.e. +220.
Step 2: Confirm with UKL350 → ONX570
Reverse UKL to LKU; +3 each: L → O, K → N, U → X = ONX ✓; 350 + 220 = 570 ✓.
Step 3: Apply to LQT150
Reverse LQT to TQL; +3 each: T → W, Q → T, L → O = WTO; 150 + 220 = 370.
Step 4: Answer
The cluster is WTO370.""", trick=r"Reverse the letters, shift each +3, and add 220 to the number.")
S[17] = dict(raw=r"""Step 1: Compare the first letters
All five words start with S-I-N.
Step 2: Look at what follows 'Sin'
Sin (nothing more) comes first. Then Since (c), Sing (g), Single (g, l), Sink (k).
Step 3: Settle Sing and Single
Sing is a prefix of Single, so Sing comes before Single.
Step 4: Answer
Sin, Since, Sing, Single, Sink = 5, 1, 3, 4, 2 → 51342.""", trick=r"A shorter word that is the start of a longer one comes first (Sin before Since, Sing before Single).")
S[18] = dict(raw=r"""Step 1: First pair
546 − 511 = 35, so the second number is 35 less than the first.
Step 2: Second pair
9745 − 9710 = 35 ✓ — the same rule.
Step 3: Apply to 5736
5736 − 35 = 5701.
Step 4: Answer
The missing number is 5701.""", trick=r"Each pair: second = first − 35.")
S[19] = dict(raw=r"""Step 1: Study PART → QDPO
P + 1 = Q, A + 3 = D, R − 2 = P, T − 5 = O.
Step 2: Confirm with GUNS → HXLN
G + 1 = H, U + 3 = X, N − 2 = L, S − 5 = N ✓ — the rule is +1, +3, −2, −5.
Step 3: Apply to BONK
B + 1 = C, O + 3 = R, N − 2 = L, K − 5 = F.
Step 4: Answer
BONK is coded as CRLF.""", trick=r"Position-wise shifts: +1, +3, −2, −5.")
S[20] = dict(raw=r"""Step 1: Study BEAMS → CHFLQ
B + 1 = C, E + 3 = H, A + 5 = F, M − 1 = L, S − 2 = Q.
Step 2: Confirm with ARISE → BUNRC
A + 1 = B, R + 3 = U, I + 5 = N, S − 1 = R, E − 2 = C ✓ — the rule is +1, +3, +5, −1, −2.
Step 3: Apply to CONGO
C + 1 = D, O + 3 = R, N + 5 = S, G − 1 = F, O − 2 = M.
Step 4: Answer
CONGO is coded as DRSFM.""", trick=r"Position-wise shifts: +1, +3, +5, −1, −2.")
