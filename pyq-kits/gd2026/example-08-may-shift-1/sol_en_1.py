S = {}
S[1] = dict(raw=r"""Step 1: Find the common difference
548 − 540 = 8, 540 − 532 = 8, 532 − 524 = 8 — the series falls by 8 each time.
Step 2: Find the expected next terms
\( 524 - 8 = 516 \), \( 516 - 8 = 508 \), \( 508 - 8 = 500 \), \( 500 - 8 = 492 \).
Step 3: Compare with the given terms
The fifth term is printed as 519, but it should be 516.
Step 4: Check
With 516 in place every gap is exactly 8, and 508, 500, 492 all fit, so 519 is the wrong term.""", trick=r"Constant −8: the odd number in an even-step series is the wrong term.")
S[2] = dict(raw=r"""Step 1: Write the first letters
B (2), Y (25), ?, S (19), P (16), M (13), J (10), G (7): each is −3 (2 − 3 = −1 → 25 = Y). So the missing first letter is Y − 3 = V.
Step 2: Write the second letters
U (21), R (18), ?, I (9), C (3), V (22), N (14), E (5).
Step 3: Find the gaps
I → C is −6, C → V is −7 (3 − 7 = −4 → 22), V → N is −8, N → E is −9. So the gaps grow by 1: −3, −4, −5, −6 …
Step 4: Fill the blank
R (18) − 4 = 14 = N, and N (14) − 5 = 9 = I ✓. The missing term is VN.""", trick=r"First letters −3; second letters −3, −4, −5, −6 … (wrap past A to Z).")
S[3] = dict(raw=r"""Step 1: Write the first letters
F (6), C (3), Z (26), W (23), T (20), ?, N (14), K (11): each is −3, so the missing first letter is T − 3 = Q.
Step 2: Write the second letters
G (7), C (3), X (24), R (18), K (11), ?, T (20), J (10).
Step 3: Find the gaps
G → C is −4, C → X is −5 (3 − 5 = −2 → 24), X → R is −6, R → K is −7, so the next gap is −8.
Step 4: Fill the blank
K (11) − 8 = 3 = C; check: C (3) − 9 = −6 → 20 = T ✓ and T (20) − 10 = 10 = J ✓. The missing term is QC.""", trick=r"First letters −3; second letters −4, −5, −6, −7, −8 …")
S[4] = dict(raw=r"""Step 1: Find the rule in (UN, RG, OZ)
First letters: U (21) → R (18) → O (15), −3 each. Second letters: N (14) → G (7) → Z (7 − 7 = 0 → 26), −7 each.
Step 2: Confirm with (SA, PT, MM)
S (19) → P (16) → M (13), −3 ✓. A (1) → T (1 − 7 = −6 → 20) → M (13), −7 ✓.
Step 3: Test the options
(LM, IF, FY): L (12) → I (9) → F (6) is −3; M (13) → F (6) → Y (6 − 7 = −1 → 25) is −7 ✓. In (BD, VA, QT), B → V is not −3; in (YZ, YW, NP), Y → Y is 0; in (JA, JX, YQ), J → J is 0.
Step 4: Answer
Only (LM, IF, FY) follows −3 on the first letters and −7 on the second letters.""", trick=r"Two rules: first letters −3, second letters −7.")
S[5] = dict(raw=r"""Step 1: Find the differences of the known terms
−386 → −390 is −4, −390 → −396 is −6, −396 → −404 is −8, −404 → −414 is −10, −414 → −426 is −12, −426 → −440 is −14.
Step 2: Spot the pattern
The differences grow by 2: −4, −6, −8, −10, −12, −14. So the first difference is −2.
Step 3: Work backwards
? − 2 = −386, so ? = \( -386 + 2 = -384 \).
Step 4: Check
\( -384 - 2 = -386 \) ✓, and the rest of the chain follows.""", trick=r"Differences −2, −4, −6 …: add the first gap back to get the first term.")
S[6] = dict(raw=r"""Step 1: Find the differences
125 − 26 = 99, 224 − 125 = 99, 323 − 224 = 99, 422 − 323 = 99.
Step 2: Confirm the rule
521 − 422 = 99 and 620 − 521 = 99, so the series adds 99 each time.
Step 3: Find the missing term
\( 620 + 99 = 719 \).
Step 4: Shortcut check
Adding 99 is +100 − 1: 620 → 720 → 719 ✓.""", trick=r"+99 = +100 then −1 (the hundreds rise by 1, the units fall by 1).")
S[7] = dict(raw=r"""Step 1: Use the two clues about L
L is second to the left of J, so J sits two places to the right of L. L is second to the right of P, so P sits two places to the left of L.
Step 2: Fix P, L and J
P _ L _ J needs all five seats: P = 1st, L = 3rd, J = 5th from the left.
Step 3: Place K and Q
The free seats are 2nd and 4th. K is second to the left of Q, so K = 2nd and Q = 4th.
Step 4: Answer
Order from the left: P, K, L, Q, J. The person at second position from the left is K.""", trick=r"Two 'second to' clues around one person in a row of five fix seats 1, 3 and 5.")
S[8] = dict(raw=r"""Step 1: Place S and P
P is lighter than only S, so S is the heaviest and P is second.
Step 2: Place T
Boys heavier than P = 1 (only S). So exactly 1 boy is lighter than T — T is fifth (second lightest).
Step 3: Place R and V
R is heavier than only V and T, so R is fourth, and V (lighter than T) is the lightest.
Step 4: Place Q and answer
Order: S > P > Q > R > T > V. Q is heavier than R, T and V — 3 boys.""", trick=r"'Heavier than only two' means third from the bottom.")
S[9] = dict(raw=r"""Step 1: Study the first pair
In the first figure the three arrows hang down from a bar at the top. In the second figure the bar is at the bottom and the arrows point up.
Step 2: Find the rule
Top and bottom have swapped while left and right are unchanged — the second figure is the vertical flip (water image) of the first.
Step 3: Apply the rule to the third figure
In the third figure the three small squares stand on top, joined by stems to a bar at the bottom. Its vertical flip has the bar at the top and the squares hanging below it, all three stems of equal length.
Step 4: Eliminate the others
One option repeats the third figure unchanged, one turns it sideways through 90°, and one has the middle square on a shorter stem. Only the figure with the bar on top and three equal hanging squares is the flip.""", trick=r"Up-arrows ↔ down-arrows = flip top-to-bottom; check that nothing else changes.")
S[10] = dict(raw=r"""Step 1: Track the letters in the first pair
First figure: P top, T right, G bottom, N left. Second figure: T top, G right, N bottom, P left. Each letter has moved one side anticlockwise (90° anticlockwise).
Step 2: Track the small symbols
The first figure has two open circles in its upper half; the second keeps those two open circles and adds two filled circles in the other half of the line.
Step 3: Apply to the third figure
Third figure: S top, C right, K bottom, R left, with two open squares on the left half. Moving each letter one side anticlockwise gives C top, K right, R bottom, S left.
Step 4: Place the symbols and choose
The two open squares stay on the left half (beside S) and two filled squares are added on the right half (beside K): C on top, S □□■■ K, R below. The figure with the filled squares beside S, and both figures with R on top, fail.""", trick=r"First fix the letter positions, then check where the open and filled shapes sit.")
S[11] = dict(raw=r"""Step 1: Find the rule in ZP54 → BR108
Z (26) + 2 = 28 → 2 = B; P (16) + 2 = 18 = R; \( 54 \times 2 = 108 \).
Step 2: Confirm with CR60 → ET120
C (3) + 2 = 5 = E; R (18) + 2 = 20 = T; \( 60 \times 2 = 120 \) ✓.
Step 3: Work backwards from ZL126
First letter: Z (26) − 2 = 24 = X. Second letter: L (12) − 2 = 10 = J. Number: \( 126 \div 2 = 63 \).
Step 4: Answer
The missing cluster is XJ63 (X + 2 = Z, J + 2 = L, \( 63 \times 2 = 126 \)).""", trick=r"Letters +2, number ×2 — undo with −2 and ÷2.")
S[12] = dict(raw=r"""Step 1: Find the letter rule in RKB110 → ENU330
Reverse RKB to get BKR, then add 3: B → E, K → N, R → U, giving ENU.
Step 2: Find the number rule
\( 110 + 220 = 330 \). Check with CLM220 → POF440: reverse CLM = MLC; M + 3 = P, L + 3 = O, C + 3 = F → POF ✓, and \( 220 + 220 = 440 \) ✓.
Step 3: Apply to DSJ140
Reverse DSJ = JSD; J + 3 = M, S + 3 = V, D + 3 = G → MVG. Number: \( 140 + 220 = 360 \).
Step 4: Answer
DSJ140 is related to MVG360.""", trick=r"Reverse the letters, then +3; the number adds 220.")
S[13] = dict(raw=r"""Step 1: Find the rule in the first pair
\( 9106 - 9058 = 48 \).
Step 2: Confirm with the second pair
\( 7852 - 7804 = 48 \) ✓, so the second number is the first + 48.
Step 3: Work backwards
? + 48 = 7472, so ? = \( 7472 - 48 = 7424 \).
Step 4: Check
\( 7424 + 48 = 7472 \) ✓.""", trick=r"Same gap of +48 in every pair; subtract it from the last number.")
S[14] = dict(raw=r"""Step 1: Find the rule in 561 → 2253
\( 561 \times 4 = 2244 \) and \( 2244 + 9 = 2253 \).
Step 2: Confirm with 859 → 3445
\( 859 \times 4 = 3436 \) and \( 3436 + 9 = 3445 \) ✓. So the second number = first × 4 + 9.
Step 3: Apply to 530
\( 530 \times 4 = 2120 \) and \( 2120 + 9 = 2129 \).
Step 4: Answer
530 is related to 2129.""", trick=r"Second ≈ 4 × first: 561 × 4 = 2244, the extra 9 gives the rule.")
S[15] = dict(raw=r"""Step 1: Compare KNOT with POPU
K (11) → P (16): 11 + 16 = 27, so P is the opposite letter of K. N → O, O → P, T → U are each +1.
Step 2: Confirm with ROPE → IPQF
R (18) → I (9): 18 + 9 = 27, the opposite letter ✓. O → P, P → Q, E → F are +1 ✓.
Step 3: Apply to DOJO
D (4) → opposite letter 27 − 4 = 23 = W; O → P, J → K, O → P.
Step 4: Answer
DOJO is coded as WPKP.""", trick=r"First letter → its opposite (pairs add to 27); the rest +1.")
S[16] = dict(raw=r"""Step 1: Use reverse letter values (A = 26 … Z = 1)
HEART: H 19 + E 22 + A 26 + R 9 + T 7 = 83. Code 81 = 83 − 2.
Step 2: Confirm with CHAIR
C 24 + H 19 + A 26 + I 18 + R 9 = 96. Code 94 = 96 − 2 ✓.
Step 3: Apply to ROAD
R 9 + O 12 + A 26 + D 23 = 70.
Step 4: Answer
\( 70 - 2 = 68 \), so ROAD is coded as 68.""", trick=r"Reverse value = 27 − position; code = sum − 2.")
S[17] = dict(raw=r"""Step 1: Check the first letters
A (1), H (8), O (15), V (22), C (29 → 3): each +7, so the next should be C + 7 = J (10), but KT150 starts with K.
Step 2: Check the second letters
Z, Y, X, W, V: each −1, so the next should be U, but the term has T.
Step 3: Check the numbers
586, 500, 414, 328, 242: each −86, so the next should be \( 242 - 86 = 156 \), but the term has 150.
Step 4: Answer
The first five terms follow all three rules; the last term should be JU156, so KT150 is the wrong term.""", trick=r"Check letters and numbers separately; the term that breaks every rule is wrong.")
S[18] = dict(raw=r"""Step 1: Check the first letters
E (5) → I (9) → M (13) → Q (17): +4 each, so the next is U (21).
Step 2: Check the second and third letters
Second: R (18) → V (22) → Z (26) → D (4) → H (8). Third: A (1) → E (5) → I (9) → M (13) → Q (17). Both +4.
Step 3: Check the numbers
20 → 30 → 45 → 67.5: each ×1.5, so the next is \( 67.5 \times 1.5 = 101.25 \).
Step 4: Answer
The next term is UHQ101.25.""", trick=r"All three letters +4; number ×1.5.")
S[19] = dict(raw=r"""Step 1: Use the angle formula
Angle between the hands = \( \left| 30H - \dfrac{11}{2}M \right| \), with H = 8.
Step 2: Set it equal to 75°
\( 240 - \dfrac{11}{2}M = \pm 75 \).
Step 3: Solve both cases
Case 1: \( \dfrac{11}{2}M = 165 \Rightarrow M = 30 \) (8:30). Case 2: \( \dfrac{11}{2}M = 315 \Rightarrow M = \dfrac{630}{11} \approx 57.27 \).
Step 4: Choose from the options
8:30 is not offered, so the time is about 8:57.""", trick=r"θ = |30H − 5.5M|; between 8 and 9 the 75° angle occurs at 8:30 and about 8:57.")
S[20] = dict(raw=r"""Step 1: Find the time elapsed
From 10 AM to 10 PM = 12 hours = \( 12 \times 60 = 720 \) minutes.
Step 2: Count the 4-minute blocks
\( 720 \div 4 = 180 \) blocks.
Step 3: Find the total gain
\( 180 \times 3 = 540 \) seconds = \( 540 \div 60 = 9 \) minutes.
Step 4: Answer
A fast clock shows the correct time plus the gain: 10:00:00 PM + 9 min = 10:09:00 PM.""", trick=r"Gain = (total minutes ÷ 4) × 3 s; a fast clock runs ahead.")
