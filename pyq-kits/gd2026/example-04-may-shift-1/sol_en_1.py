S = {}
S[1] = dict(raw=r"""Step 1: Read the rule from the pair HM and KN
H (8) + 3 = K (11), and M (13) → its opposite letter N (14), since 13 + 14 = 27.
Step 2: Confirm with the pair XG and AT
X (24) + 3 = 27 → A (1), and G (7) → its opposite letter T (20), since 7 + 20 = 27.
Step 3: Apply the rule to RD
R (18) + 3 = U (21), and D (4) → its opposite letter W (23).
So the missing cluster is UW.""", trick=r"Opposite pairs add to 27: A–Z, D–W, G–T, M–N.")
S[2] = dict(raw=r"""Step 1: Study (BS, DW, FA)
First letters B → D → F move +2 each; second letters S → W → A move +4 each (W + 4 wraps to A).
Step 2: Check (KD, MH, OL)
K → M → O is +2 and D → H → L is +4 — the same rule.
Step 3: Test the options
(NZ, PD, RH): N → P → R is +2 and Z → D → H is +4 (wrapping after Z). It follows the rule.
(NB, PD, WH) breaks at P → W; (TS, VU, YY) breaks at V → Y; (UL, WN, ZR) breaks at W → Z.""", trick=r"Check both letter positions of every pair; after Z count again from A.")
S[3] = dict(raw=r"""Step 1: Fix R and V
Facing the centre, moving to the right means moving anticlockwise. Fix R first; V is second to the right of R.
Step 2: Place T and U
T is third to the right of U. The only placement where S can sit beside T without touching R or V puts U to the immediate right of R, with T three seats further to the right.
Step 3: Place S, Q and P
S sits next to T, away from R and V. Q is the other neighbour of T, and P is the seat three places to the right of Q (Q is third to the left of P).
Order going left from R: R, P, S, T, Q, V, U.
Step 4: Answer
Counting four places to the left of T: Q, V, U, R. So R is fourth to the left of T.""", trick=r"Facing the centre: right = anticlockwise, left = clockwise.")
S[4] = dict(raw=r"""Step 1: Fix G, C and F
Facing the centre, right = anticlockwise. C is second to the right of G, and F is to the immediate right of C.
Step 2: Place D, B, E
B sits between D and E, so D, B and E occupy three seats in a row. The only three consecutive free seats are next to G on its left side.
Step 3: Use A
A is third to the left of E. This works only when E is the seat next to F, with A in the last free seat beside G.
Going left from G: G, D, B, E, F, C, A.
Step 4: Answer
The person to the immediate right of F is E.""", trick=r"Place the fixed chain (D-B-E) first; it leaves only one gap.")
S[5] = dict(raw=r"""Step 1: Write the prime factors
\( 5 = 5,\; 8 = 2^{3},\; 9 = 3^{2},\; 10 = 2 \times 5 \)
Step 2: Take the highest power of each prime
\( \text{LCM} = 2^{3} \times 3^{2} \times 5 \)
Step 3: Multiply
\( 8 \times 9 \times 5 = 360 \)
The smallest number divisible by all four is 360.""", trick=r"Smallest number divisible by all = LCM.")
S[6] = dict(raw=r"""Step 1: Total of the first group
\( 40 \times 72 = 2880 \)
Step 2: Total of the second group
\( 20 \times 78 = 1560 \)
Step 3: Combined average
\( \dfrac{2880 + 1560}{60} = \dfrac{4440}{60} = 74 \)""", trick=r"Weighted average: 72 + (78 − 72) × 20/60 = 72 + 2 = 74.")
S[7] = dict(raw=r"""Step 1: First statement
Sohan > Ravi > Meena (in age).
Step 2: Second statement
Karan > Arjun > Ravi.
Step 3: Combine
Everyone else is older than Ravi, and Ravi is older than Meena.
So Meena is the youngest.""", trick=r"Write each statement as a chain with > signs and join them at the common name.")
S[8] = dict(raw=r"""Step 1: Find the differences
35 − 22 = 13, 51 − 35 = 16, 70 − 51 = 19, 92 − 70 = 22
Step 2: Spot the pattern
The differences increase by 3: 13, 16, 19, 22, so the next difference is 25.
Step 3: Next term
\( 92 + 25 = 117 \)""", trick=r"When the gaps themselves grow steadily, find the gap of the gaps.")
S[9] = dict(raw=r"""Step 1: Compare neighbouring terms
16 × 2 = 32, 32 × 2 = 64.
Step 2: Continue the rule
\( 64 \times 2 = 128 \)
Step 3: Check with the last term
\( 128 \times 2 = 256 \) ✓, so the missing term is 128.""", trick=r"Each term doubles: powers of 2 from 16 to 256.")
S[10] = dict(raw=r"""Step 1: Number part
7, 18, 37, 66, 107 → differences 11, 19, 29, 41.
Step 2: Gap of the gaps
19 − 11 = 8, 29 − 19 = 10, 41 − 29 = 12 → next is 14, so the next difference is 41 + 14 = 55 and the number is 107 + 55 = 162.
Step 3: Letter part
F, K, P, U, Z move +5 each; Z + 5 wraps round to E.
The next term is 162E.""", trick=r"Split alphanumeric terms into a number series and a letter series.")
S[11] = dict(raw=r"""Step 1: First letters
V, Y, ?, E, H → +3 each, so the missing first letter is Y + 3 = B.
Step 2: Second letters
K, G, ?, Y, U → −4 each, so the missing letter is G − 4 = C.
Step 3: Third letters
C, H, ?, R, W → +5 each, so the missing letter is H + 5 = M.
The missing term is BCM.""", trick=r"Treat each letter position as its own series.")
S[12] = dict(raw=r"""Step 1: Look at the first pair
The first figure is a square holding an outline triangle (3 sides). In the second figure the triangle has become small and shaded, and a new shape with one more side — a square (4 sides) — has appeared between it and the outer square.
Step 2: Apply the same change to the third figure
The third figure is a square holding an outline pentagon (5 sides). So the pentagon must become small and shaded, with a hexagon (6 sides) drawn around it inside the outer square.
Step 3: Pick the option
Only one option shows a shaded pentagon inside a hexagon inside the square. The option with a second square around the shaded pentagon does not follow the "one more side" step that the answer key uses.""", trick=r"In figure analogies, count sides: here the new middle shape has one more side than the original.")
S[13] = dict(raw=r"""Step 1: Track each symbol in the first pair
Bottom-left 4 moves to top-left; top-left arrow moves to top-right; top-right 6 moves to bottom-right; bottom-right 2 moves to bottom-left. Every symbol moves one corner clockwise.
Step 2: Notice the mirror effect
Each symbol is also flipped left–right (the arrow now points the other way, and 2, 4, 6 appear reversed).
Step 3: Apply both changes to R, G, 6, Z
6 moves to top-left, R to top-right, G to bottom-right and Z to bottom-left — and all four are mirror-reversed.
Only one option has all four symbols in these corners and all four reversed; the option that keeps an un-reversed 6 is the trap.""", trick=r"Check two things separately: where each symbol moves, and whether it is flipped.")
S[14] = dict(raw=r"""Step 1: Rule from AC300 and CG240
A + 2 = C, C + 4 = G, and 300 − 60 = 240.
Step 2: Confirm with PK125 and RO65
P + 2 = R, K + 4 = O, and 125 − 60 = 65 ✓.
Step 3: Apply to TV120
T + 2 = V, V + 4 = Z, and 120 − 60 = 60.
The answer is VZ60.""", trick=r"Letters: +2, +4; number: −60.")
S[15] = dict(raw=r"""Step 1: Rule from UXY80 and UTQ120
U stays U, X − 4 = T, Y − 8 = Q, and \( 80 \times \dfrac{3}{2} = 120 \).
Step 2: Confirm with LRP40 and LNH60
L stays L, R − 4 = N, P − 8 = H, and \( 40 \times \dfrac{3}{2} = 60 \) ✓.
Step 3: Apply to TSK60
The number part gives \( 60 \times \dfrac{3}{2} = 90 \), which leaves GOQ90 and GOP90.
The letters of TSK under this rule give T, O, C, which matches no option — the third cluster appears to be misprinted in the source. The keyed option GOP90 is exactly what the rule gives for the cluster GSX60 (G stays G, S − 4 = O, X − 8 = P).
We carry the official key, GOP90.""", trick=r"Letters 0, −4, −8; number × 1.5.")
S[16] = dict(raw=r"""Step 1: All five words begin with "Hu"
So compare the third letters: n (Hunt, Hunk, Hunch, Hunger) and r (Hurl). Hurl comes last.
Step 2: Compare the four "Hun-" words by the fourth letter
Hunch (c) → Hunger (g) → Hunk (k) → Hunt (t).
Step 3: Write the numbers
Hunch (3), Hunger (4), Hunk (2), Hunt (1), Hurl (5) → 34215.""", trick=r"Go letter by letter; settle the odd one (Hurl) first.")
S[17] = dict(raw=r"""Step 1: Rule from 527 and 2114
\( 527 \times 4 + 6 = 2108 + 6 = 2114 \)
Step 2: Confirm with 965 and 3866
\( 965 \times 4 + 6 = 3860 + 6 = 3866 \) ✓
Step 3: Apply to 408
\( 408 \times 4 + 6 = 1632 + 6 = 1638 \)""", trick=r"Second ÷ first ≈ 4 → test ×4 and adjust.")
S[18] = dict(raw=r"""Step 1: Rule from 398 and 120
\( 398 - 120 = 278 \), so the rule may be "subtract 278".
Step 2: Confirm with 84 and −194
\( 84 - 278 = -194 \) ✓
Step 3: Apply to 719
\( 719 - 278 = 441 \)""", trick=r"A negative answer in a pair is a hint that the rule is subtraction.")
S[19] = dict(raw=r"""Step 1: Compare BEGUN with EHJXQ
B → E, E → H, G → J, U → X, N → Q: every letter moves +3.
Step 2: Confirm with SIZED → VLCHG
S → V, I → L, Z → C, E → H, D → G: again +3 ✓.
Step 3: Code BOULE
B → E, O → R, U → X, L → O, E → H, giving ERXOH.""", trick=r"Same shift for every letter — check one letter of each word and move on.")
S[20] = dict(raw=r"""Step 1: Compare DOTTY with EPVWC
D → E (+1), O → P (+1), T → V (+2), T → W (+3), Y → C (+4).
Step 2: Confirm with CHIRP → DIKUT
C → D (+1), H → I (+1), I → K (+2), R → U (+3), P → T (+4) ✓.
Step 3: Code FEELS with +1, +1, +2, +3, +4
F → G, E → F, E → G, L → O, S → W, giving GFGOW.""", trick=r"Position-wise shifts +1, +1, +2, +3, +4.")
