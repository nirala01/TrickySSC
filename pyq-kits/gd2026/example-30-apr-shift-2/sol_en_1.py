S = {}
S[1] = dict(raw=r"""Step 1: Study FS → IW
F (6) + 3 = I (9) and S (19) + 4 = W (23). So the first letter moves +3 and the second letter moves +4.
Step 2: Confirm with WJ → ZN
W (23) + 3 = Z (26) and J (10) + 4 = N (14) ✓ — the same +3, +4 rule.
Step 3: Work back from LC
The missing cluster must give L and C after +3 and +4. L (12) − 3 = I (9) and C (3) − 4 → going back 4 from C wraps round to Y (25).
Step 4: Answer and check
The missing cluster is IY. Check: I + 3 = L and Y + 4 = C (Y → Z → A → B → C) ✓""", trick=r"Find the shift from the first pair, then move backwards from the given cluster.")
S[2] = dict(raw=r"""Step 1: Read the first set (KY, MC, PH)
First letters K → M → P move +2, then +3. Second letters Y → C → H move +4, then +5.
Step 2: Confirm with (AG, CK, FP)
A → C → F is +2, +3 and G → K → P is +4, +5 ✓
Step 3: Test the options
(UL, WP, ZU): U → W → Z is +2, +3 and L → P → U is +4, +5 ✓
(FD, GD, LI) starts F → G (+1); (TW, WX, ZC) starts T → W (+3); (KI, MK, QP) has M → Q (+4) in the first letters — all break the rule.
Step 4: Answer
The set (UL, WP, ZU) follows the same rule.""", trick=r"Check first letters (+2, +3) and second letters (+4, +5) separately.")
S[3] = dict(raw=r"""Step 1: Fix U and its neighbours
Facing the centre, "right" means anticlockwise. T is second to the right of U and R sits next to both T and U, so R is immediately to the right of U and T is next to R.
Step 2: Place V
V is second to the left of U, so one seat lies between U and V on U's left.
Step 3: Place S, P and Q
S must sit next to V and next to P. The seat between U and V is too small for both, so S sits on V's other side and P next to S. Q takes the seat between U and V.
Clockwise from U: U, Q, V, S, P, T, R.
Step 4: Count from R
Moving right (anticlockwise) from R: 1st T, 2nd P, 3rd S, 4th V. So V is fourth to the right of R.""", trick=r"Facing the centre: right = anticlockwise, left = clockwise.")
S[4] = dict(raw=r"""Step 1: Place B and R
No one is to the left of B, so B is at the left end (position 1). N and H are left of R and K, S, P are right of R, so R must be at position 4.
Step 2: Fill the right side
K and S cannot be at the ends, so position 7 (right end) must be P.
Step 3: Fill the rest
N is not second from an end, so N is at 3 and H at 2. S is not second from an end (position 6), so S is at 5 and K at 6.
Order from left: B, H, N, R, S, K, P.
Step 4: Answer
P sits at the right end of the row.""", trick=r"'No one to the left of B' fixes B at the left end — start there.")
S[5] = dict(raw=r"""Step 1: What is asked
The smallest number divisible by 18, 24 and 30 is their LCM.
Step 2: Prime factors
\( 18 = 2 \times 3^{2},\; 24 = 2^{3} \times 3,\; 30 = 2 \times 3 \times 5 \)
Step 3: Take the highest powers
\( \text{LCM} = 2^{3} \times 3^{2} \times 5 = 8 \times 9 \times 5 = 360 \)
Step 4: Check
\( 360 \div 18 = 20,\; 360 \div 24 = 15,\; 360 \div 30 = 12 \) ✓ — 180 is not divisible by 24, so 360 is the smallest.""", trick=r"Smallest number divisible by all = LCM.")
S[6] = dict(raw=r"""Step 1: Formula
\( \text{SI} = \dfrac{P \times R \times T}{100} \)
Step 2: SI for one year
\( \dfrac{6000 \times 12 \times 1}{100} = 720 \)
Step 3: SI for 3 years and 2 years
\( 3 \times 720 = 2160 \) and \( 2 \times 720 = 1440 \)
Step 4: Difference
\( 2160 - 1440 = 720 \), i.e. ₹720 — exactly one year's interest.""", trick=r"Simple interest is the same every year, so the gap between 3 and 2 years = one year's SI.")
S[7] = dict(raw=r"""Step 1: First statement
Manoj is younger than Sanjay but older than Rohit: Sanjay > Manoj > Rohit (by age).
Step 2: Second statement
Anil is older than Sanjay but younger than Vikas: Vikas > Anil > Sanjay.
Step 3: Join the two
Vikas > Anil > Sanjay > Manoj > Rohit.
Step 4: Answer
Rohit is at the bottom of the chain, so Rohit is the youngest.""", trick=r"Write each statement as a chain and join them at the common name (Sanjay).")
S[8] = dict(raw=r"""Step 1: Find the differences
91 − 55 = 36, 140 − 91 = 49, 204 − 140 = 64, 285 − 204 = 81.
Step 2: Spot the pattern
36, 49, 64, 81 are the squares of 6, 7, 8 and 9.
Step 3: Next difference
The next difference is the square of 10 = 100.
Step 4: Missing number
285 + 100 = 385.""", trick=r"Differences are consecutive squares (6², 7², 8², 9², 10²).")
S[9] = dict(raw=r"""Step 1: Look at the terms
156 = 12 × 13, 182 = 13 × 14, 210 = 14 × 15, 240 = 15 × 16.
Step 2: Spot the pattern
Each term is the product of two consecutive numbers, and both numbers go up by 1 each time.
Step 3: Next term
16 × 17 = 272.
Step 4: Check with differences
Differences 26, 28, 30 grow by 2, so the next difference is 32 and 240 + 32 = 272 ✓""", trick=r"n(n + 1) series: differences increase by 2.")
S[10] = dict(raw=r"""Step 1: Number part
2, 4, 12, 48: 2 × 2 = 4, 4 × 3 = 12, 12 × 4 = 48, so next is 48 × 5 = 240.
Step 2: Letter part
A (1), C (3), F (6), J (10): the gaps are +2, +3, +4.
Step 3: Next letter
The next gap is +5: 10 + 5 = 15 = O.
Step 4: Answer
The next term is 240O (the letter O, not zero). 192O and 192P have the wrong number; 240P has the wrong letter.""", trick=r"Numbers × 2, × 3, × 4, × 5; letters +2, +3, +4, +5.")
S[11] = dict(raw=r"""Step 1: Number part
1, 8, 27, 64, 125 are the cubes of 1, 2, 3, 4, 5, so the next is the cube of 6 = 216.
Step 2: Letter part
A (1), B (2), D (4), G (7), K (11): the gaps are +1, +2, +3, +4.
Step 3: Next letter
The next gap is +5: 11 + 5 = 16 = P.
Step 4: Answer
The next term is 216P. 216O, 216Q and 216R have the right cube but the wrong letter.""", trick=r"Cubes for the numbers; letter gaps grow by 1.")
S[12] = dict(raw=r"""Step 1: Study the first pair
The first figure is a plain rectangle in a frame. The second figure shows the same rectangle with a second rectangle drawn just inside it (a double outline) and a "+" sign in the centre.
Step 2: The rule
Draw one more copy of the shape inside it, and put a "+" in the middle.
Step 3: Apply to the circle
The third figure is a plain circle, so the answer must be a circle with a second circle just inside it and a "+" in the centre.
Step 4: Reject the others
The circle with a "+" hanging below (a symbol) adds an extra part; the rectangle with "+" is the wrong shape; the single circle with "+" has no double outline. Only the double circle with "+" in the centre follows the rule.""", trick=r"Same shape → double outline + plus inside.")
S[13] = dict(raw=r"""Step 1: Count in the first pair
The circle has 8 arrows pointing outwards. The second figure has 8 star symbols (a 3 × 3 grid with the centre empty).
Step 2: The rule
The number of arrows in the first figure = the number of symbols in the second figure.
Step 3: Count in the third figure
The pentagon has 5 arrows (four pointing out from the corners and one pointing in from the top). So the answer must show 5 symbols.
Step 4: Check the options
The figures show 6, 8, 3 and 5 "@" symbols. Only the figure with 5 "@" symbols fits.""", trick=r"Count the arrows — the answer has the same count of symbols.")
S[14] = dict(raw=r"""Step 1: Study AR318 → DV718
Letters: A + 3 = D and R + 4 = V. Numbers: 3 + 4 = 7, while 18 stays 18.
Step 2: Confirm with BK515 → EO915
B + 3 = E and K + 4 = O; 5 + 4 = 9, while 15 stays 15 ✓
Step 3: Work back from MS710
The missing cluster becomes MS710, so go backwards: M − 3 = J, S − 4 = O, 7 − 4 = 3, and 10 stays 10.
Step 4: Answer
The missing cluster is JO310 (the letter O). Check: J + 3 = M, O + 4 = S, 3 + 4 = 7 ✓""", trick=r"Letters +3, +4; first number +4; last number unchanged.")
S[15] = dict(raw=r"""Step 1: Study DFG43 → EDB86
Read DFG backwards (G, F, D) and move each letter 2 back: G → E, F → D, D → B, giving EDB. The number doubles: 43 × 2 = 86.
Step 2: Confirm with TFK46 → IDR92
K, F, T backwards, each −2: K → I, F → D, T → R gives IDR; 46 × 2 = 92 ✓
Step 3: Apply to LPJ29
Backwards J, P, L, each −2: J → H, P → N, L → J gives HNJ; 29 × 2 = 58.
Step 4: Answer
The answer is HNJ58.""", trick=r"Reverse the letters, step each back by 2, double the number.")
S[16] = dict(raw=r"""Step 1: Common start
All five words begin with "Pri", so compare the fourth letter.
Step 2: Fourth letters
Price (c), Prick (c), Pride (d), Priest (e), Prig (g) — so c, c, d, e, g.
Step 3: Break the tie
Price and Prick both have "Pric": the fifth letters are e and k, so Price comes before Prick.
Step 4: Order
Price (5), Prick (1), Pride (2), Priest (4), Prig (3) → 5, 1, 2, 4, 3 = 51243.""", trick=r"Compare letter by letter; the first difference decides.")
S[17] = dict(raw=r"""Step 1: Pair 826 and 1287
1287 − 826 = 461.
Step 2: Pair 891 and 1352
1352 − 891 = 461 ✓ — the second number is always the first + 461.
Step 3: Apply to 965
965 + 461 = 1426.
Step 4: Answer and check
The missing number is 1426. Check: 1426 − 965 = 461 ✓""", trick=r"Constant difference (+461) in every pair.")
S[18] = dict(raw=r"""Step 1: Study 2586 → 859
2586 ÷ 3 = 862 and 862 − 3 = 859.
Step 2: Confirm with 2304 → 765
2304 ÷ 3 = 768 and 768 − 3 = 765 ✓
Step 3: Work back from 660
If (? ÷ 3) − 3 = 660, then ? ÷ 3 = 663, so ? = 663 × 3 = 1989.
Step 4: Answer
The missing number is 1989. Check: 1989 ÷ 3 = 663, 663 − 3 = 660 ✓""", trick=r"Rule: divide by 3, then subtract 3 — reverse it to find the first number.")
S[19] = dict(raw=r"""Step 1: Study EDGE → FFJI
E + 1 = F, D + 2 = F, G + 3 = J, E + 4 = I.
Step 2: Confirm with RAKI → SCNM
R + 1 = S, A + 2 = C, K + 3 = N, I + 4 = M ✓
Step 3: Apply to VISE
V + 1 = W, I + 2 = K, S + 3 = V, E + 4 = I.
Step 4: Answer
VISE is coded as WKVI.""", trick=r"Positions shift +1, +2, +3, +4 from left to right.")
S[20] = dict(raw=r"""Step 1: Study BINDI → DLSAE
B + 2 = D, I + 3 = L, N + 5 = S, D − 3 = A, I − 4 = E.
Step 2: Confirm with CUBED → EXGBZ
C + 2 = E, U + 3 = X, B + 5 = G, E − 3 = B, D − 4 = Z (going back past A) ✓
Step 3: Apply to OFTEN
O + 2 = Q, F + 3 = I, T + 5 = Y, E − 3 = B, N − 4 = J.
Step 4: Answer
OFTEN is coded as QIYBJ.""", trick=r"Pattern +2, +3, +5, −3, −4 on the five letters.")
