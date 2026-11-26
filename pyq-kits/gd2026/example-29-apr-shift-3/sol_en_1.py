S = {}
S[1] = dict(raw=r"""Step 1: Study ANT → WJP
A (1) → W (23), N (14) → J (10), T (20) → P (16). Every letter moves 4 places back (A − 4 wraps round to W).
Step 2: Confirm with EUM → AQI
E (5) − 4 = A (1), U (21) − 4 = Q (17), M (13) − 4 = I (9) ✓ — the same −4 rule.
Step 3: Work backwards to the missing cluster
The missing cluster must give XVF after moving each letter 4 back, so add 4 to each letter of XVF: X (24) + 4 = B (28 − 26 = 2), V (22) + 4 = Z (26), F (6) + 4 = J (10).
Step 4: Answer
The missing cluster is BZJ. Check: B − 4 = X, Z − 4 = V, J − 4 = F ✓""", trick=r"Find the shift (−4) from a complete pair; for a missing FIRST term, reverse it (+4).")
S[2] = dict(raw=r"""Step 1: Read the first set (OJ, QL, JO)
OJ → QL: O + 2 = Q and J + 2 = L. Then QL → JO: Q (17) and J (10) add to 27, L (12) and O (15) add to 27 — so the third cluster is the opposite (mirror) of the second.
Step 2: Confirm with (EB, GD, TW)
EB → GD is +2, +2; G (7) ↔ T (20) and D (4) ↔ W (23) are opposite pairs (sum 27) ✓
Step 3: Test the options
(SL, UN, FM): SL → UN is +2, +2; U (21) ↔ F (6) and N (14) ↔ M (13) are opposites ✓
(AV, FW, YD) fails at A → F (+5); (DW, IX, VC) fails at D → I (+5); (VX, ZY, DB) fails at V → Z (+4).
Step 4: Answer
The set (SL, UN, FM) follows the same rule.""", trick=r"Rule = +2, +2, then opposite letters (pairs that add to 27).")
S[3] = dict(raw=r"""Step 1: Fix P and X
In a row of 7, X is sixth to the right of P, so P is at seat 1 (left end) and X at seat 7 (right end).
Step 2: Fix S, then Q and W
S is in the exact middle, seat 4. Q is fourth to the left of W, so they are 4 seats apart; with seats 2, 3, 5, 6 free, only Q = 2 and W = 6 works.
Step 3: Place R and T
Seats 3 and 5 are left. R is not fourth to the right of P (seat 5), so R = 3 and T = 5.
Order from left: P, Q, R, S, T, W, X.
Step 4: Count
To the right of T sit W and X — 2 boys.""", trick=r"Start with the clue that pins an end (sixth to the right in a row of 7 → both ends).")
S[4] = dict(raw=r"""Step 1: Link J, L and P
L is 2 places right of J and P is 3 places right of L, so P is 5 places right of J. J can be seat 1 or 2.
Step 2: Try J = 1
J 1, L 3, P 6. Free seats 2, 4, 5, 7. M and N must be adjacent, so M 4, N 5; then H and K take seats 2 and 7, and K (right of H) would be at the end — not allowed. So J = 1 fails.
Step 3: Try J = 2
J 2, L 4, P 7. Free seats 1, 3, 5, 6: M 5, N 6, and H 1, K 3 (K right of H and not at an end) ✓
Order from left: H, J, K, L, M, N, P.
Step 4: Answer
P sits at the right end of the row.""", trick=r"When two placements are possible, test each against the 'not at an end' clue.")
S[5] = dict(raw=r"""Step 1: Write the prime factors
\( 12 = 2^{2} \times 3 \), \( 15 = 3 \times 5 \), \( 20 = 2^{2} \times 5 \)
Step 2: Take the highest power of each prime
\( 2^{2} \), \( 3 \) and \( 5 \)
Step 3: Multiply
\( \text{LCM} = 4 \times 3 \times 5 = 60 \)
Step 4: Check
\( 60 \div 12 = 5 \), \( 60 \div 15 = 4 \), \( 60 \div 20 = 3 \) — all exact, so 60 is the smallest such number.""", trick=r"Smallest number divisible by all = LCM.")
S[6] = dict(raw=r"""Step 1: Make one set of notes
One note of each kind is worth \( 10 + 20 + 50 + 100 + 200 = 380 \) rupees.
Step 2: Number of sets
\( 7600 \div 380 = 20 \), so there are 20 notes of each denomination.
Step 3: Total notes
5 denominations, 20 each: \( 5 \times 20 = 100 \) notes
Step 4: Check
\( 20 \times 380 = 7600 \) ✓""", trick=r"Equal number of each note → total ÷ (sum of one of each) = notes per kind.")
S[7] = dict(raw=r"""Step 1: Find the rule from APPLE → CRRNG
A → C, P → R, P → R, L → N, E → G — every letter moves 2 places forward.
Step 2: Apply +2 to ORANGE
O → Q, R → T, A → C, N → P, G → I, E → G
Step 3: Write the code
QTCPIG
Step 4: Check the close options
QTCPIH ends wrongly (E + 2 = G, not H); QTCPJG has J for G + 2 = I.""", trick=r"Same shift for every letter → just add +2 to each.")
S[8] = dict(raw=r"""Step 1: Compare with powers of 2
\( 2^{1} = 2,\; 2^{2} = 4,\; 2^{3} = 8,\; 2^{4} = 16 \)
Step 2: Find what is added
\( 3 = 2 + 1,\; 8 = 4 + 4,\; 17 = 8 + 9,\; 32 = 16 + 16 \) — the extra part is \( 1^{2}, 2^{2}, 3^{2}, 4^{2} \).
Step 3: Fifth term
\( 2^{5} + 5^{2} = 32 + 25 = 57 \)
Step 4: Check the last term
\( 2^{6} + 6^{2} = 64 + 36 = 100 \) ✓""", trick=r"Term n = \( 2^{n} + n^{2} \).")
S[9] = dict(raw=r"""Step 1: Find the differences
405 − 385 = 20, 385 − 370 = 15, 370 − 360 = 10
Step 2: Spot the pattern
The differences fall by 5: 20, 15, 10, so the next difference is 5.
Step 3: Next term
\( 360 - 5 = 355 \)
Step 4: Answer
The missing number is 355.""", trick=r"Gaps 20, 15, 10, 5 — reduce by 5 each time.")
S[10] = dict(raw=r"""Step 1: Number part
1, 3, 6, 10, 15 increase by 2, 3, 4, 5, so the next number is \( 15 + 6 = 21 \).
Step 2: Letter part
A, C, F, J, O are letters 1, 3, 6, 10, 15 — the letter's position equals the number in front of it.
Step 3: Next letter
Position 21 is U.
Step 4: Answer
The next term is 21U.""", trick=r"Letter position = the number beside it (triangular numbers).")
S[11] = dict(raw=r"""Step 1: Number part
3 → 6 → 18 → 72: multiply by 2, 3, 4, so the next is \( 72 \times 5 = 360 \).
Step 2: Letter part
B (2), D (4), G (7), K (11): gaps +2, +3, +4.
Step 3: Next letter
\( 11 + 5 = 16 \) → P
Step 4: Answer
The next term is 360P.""", trick=r"Numbers ×2, ×3, ×4, ×5; letters +2, +3, +4, +5.")
S[12] = dict(raw=r"""Step 1: Compare the first two figures
First figure (top to bottom): @, #, &. Second figure: &, @, #.
Step 2: Find the rule
The bottom symbol moves to the top and the other two move down one place (a cyclic shift downward).
Step 3: Apply the rule to the third figure
Third figure: +, ×, $. Moving $ to the top gives $, +, ×.
Step 4: Match the options
Only one figure shows $ on top, + in the middle and × at the bottom. The look-alike with ÷ at the bottom has the wrong symbol.""", trick=r"Bottom symbol jumps to the top; the rest slide down.")
S[13] = dict(raw=r"""Step 1: Compare the first two figures
First: top S T A, bottom G P K. Second: top A P S, bottom K T G.
Step 2: Find the rule
Each row is reversed (S T A → A T S, G P K → K P G) and then the two middle letters swap rows (T ↔ P), giving A P S and K T G.
Step 3: Apply the rule to the third figure
Top V L N → N L V, bottom M C D → D C M; swap the middle letters L ↔ C: top N C V, bottom D L M.
Step 4: Match the options
The required figure has N C V on top and D L M at the bottom. The look-alike with M L D at the bottom forgot to reverse the bottom row.""", trick=r"Reverse both rows, then swap the middle letters.")
S[14] = dict(raw=r"""Step 1: Rule from CK42 → EM84
C + 2 = E, K + 2 = M, and \( 42 \times 2 = 84 \).
Step 2: Confirm with KI14 → MK28
K + 2 = M, I + 2 = K, \( 14 \times 2 = 28 \) ✓
Step 3: Reverse the rule for ? → ZW96
Letters: Z − 2 = X, W − 2 = U. Number: \( 96 \div 2 = 48 \).
Step 4: Answer
The missing cluster is XU48. Check: X + 2 = Z, U + 2 = W, \( 48 \times 2 = 96 \) ✓""", trick=r"Letters +2, number ×2 — reverse it (−2, ÷2) for a missing first term.")
S[15] = dict(raw=r"""Step 1: Rule from DEW14 → GHT28
D + 3 = G, E + 3 = H, W − 3 = T, and \( 14 \times 2 = 28 \).
Step 2: Confirm with LKO28 → ONL56
L + 3 = O, K + 3 = N, O − 3 = L, \( 28 \times 2 = 56 \) ✓
Step 3: Apply to ACJ40
A + 3 = D, C + 3 = F, J − 3 = G, \( 40 \times 2 = 80 \)
Step 4: Answer
The cluster is DFG80.""", trick=r"First two letters +3, last letter −3, number doubled.")
S[16] = dict(raw=r"""Step 1: Common start
All five words begin with G-I-R, so compare from the fourth letter.
Step 2: Fourth letters
Giraffe (a), Gird (d), Girdle (d), Girl (l), Girth (t). So Giraffe comes first and Girth last.
Step 3: Gird vs Girdle
Gird is the beginning of Girdle, so the shorter word Gird comes first.
Step 4: Order
Giraffe (5), Gird (4), Girdle (3), Girl (2), Girth (1) → 5, 4, 3, 2, 1.""", trick=r"A word that is the start of another word comes before it (Gird before Girdle).")
S[17] = dict(raw=r"""Step 1: Rule from 136 → 671
\( 671 - 136 = 535 \)
Step 2: Confirm with 950 → 1485
\( 1485 - 950 = 535 \) ✓ — the rule is "add 535".
Step 3: Apply to 332
\( 332 + 535 = 867 \)
Step 4: Answer
The missing number is 867.""", trick=r"Both given pairs differ by the same amount (535) → add it.")
S[18] = dict(raw=r"""Step 1: Test division by 3 on 1083 → 363
\( 1083 \div 3 = 361 \), and \( 361 + 2 = 363 \).
Step 2: Confirm with 2487 → 831
\( 2487 \div 3 = 829 \), and \( 829 + 2 = 831 \) ✓
Step 3: Apply to 804
\( 804 \div 3 = 268 \), then \( 268 + 2 = 270 \)
Step 4: Answer
The missing number is 270.""", trick=r"Second number is about one-third of the first → ÷3, then fix the small gap (+2).")
S[19] = dict(raw=r"""Step 1: Test the letter-position sum on SCENE
S 19 + C 3 + E 5 + N 14 + E 5 = 46 ✓
Step 2: Confirm with PICTURE
P 16 + I 9 + C 3 + T 20 + U 21 + R 18 + E 5 = 92 ✓
Step 3: Apply to RATE
R 18 + A 1 + T 20 + E 5
Step 4: Total
\( 18 + 1 + 20 + 5 = 44 \)""", trick=r"Word → number code: first try the sum of letter positions.")
S[20] = dict(raw=r"""Step 1: Rule from MIMIC → PNLGY
M → P (+3), I → N (+5), M → L (−1), I → G (−2), C → Y (−4, wrapping round).
Step 2: Confirm with AEONS → DJNLO
A + 3 = D, E + 5 = J, O − 1 = N, N − 2 = L, S − 4 = O ✓
Step 3: Apply +3, +5, −1, −2, −4 to RECON
R + 3 = U, E + 5 = J, C − 1 = B, O − 2 = M, N − 4 = J
Step 4: Answer
RECON is coded as UJBMJ.""", trick=r"Position-wise shifts: +3, +5, −1, −2, −4.")
