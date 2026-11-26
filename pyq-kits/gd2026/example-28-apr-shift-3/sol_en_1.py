S = {}
S[1] = dict(raw=r"""Step 1: Find the differences
56 − 34 = 22, 76 − 56 = 20, 94 − 76 = 18, 110 − 94 = 16
Step 2: Spot the pattern
The differences fall by 2 each time: 22, 20, 18, 16, so the next difference is 14.
Step 3: Next term
\( 110 + 14 = 124 \)
Step 4: Check
\( 34 + 22 + 20 + 18 + 16 + 14 = 124 \) ✓""", trick=r"Gaps 22, 20, 18, 16 … — keep subtracting 2.")
S[2] = dict(raw=r"""Step 1: Test multiplication by 3
\( -33 \times 3 = -99 \), and −99 + 1 = −98 — the next term.
Step 2: Confirm the rule on every term
\( -98 \times 3 + 1 = -293,\; -293 \times 3 + 1 = -878,\; -878 \times 3 + 1 = -2633,\; -2633 \times 3 + 1 = -7898 \)
Step 3: Apply the rule once more
\( -7898 \times 3 = -23694 \), then −23694 + 1 = −23693
Step 4: Answer
The missing term is −23693.""", trick=r"Terms roughly triple each time → try ×3 and fix the small leftover (+1).")
S[3] = dict(raw=r"""Step 1: First letters of EN → YM and DP → XK
E (5) − 6 = Y (wrapping: 5 − 6 + 26 = 25) and D (4) − 6 = X (24). So the first letter moves 6 places back.
Step 2: Second letters
N (14) → M (13) and P (16) → K (11). In both pairs the letters are opposites: 14 + 13 = 27 and 16 + 11 = 27.
Step 3: Work backwards from DJ
The first letter of the missing cluster must be D + 6 = J. The second letter is the opposite of J (10), which is 27 − 10 = 17 = Q.
Step 4: Answer
The missing cluster is JQ. Check: J − 6 = D and Q's opposite is J ✓""", trick=r"Opposite letters add to 27 (J–Q, N–M, P–K).")
S[4] = dict(raw=r"""Step 1: Study (PO, RT, TY)
First letters P → R → T move +2; second letters O → T → Y move +5.
Step 2: Check (TQ, VV, XA)
T → V → X is +2 and Q → V → A is +5 (V + 5 wraps to A) — the same rule.
Step 3: Test the options
(BQ, DV, FA): B → D → F is +2 and Q → V → A is +5 — it fits.
(MO, QS, TV) breaks at M → Q; (JE, KE, QL) breaks at J → K; (IJ, HI, PQ) breaks at I → H.
Step 4: Answer
The set (BQ, DV, FA) follows the same rule.""", trick=r"Check both letter positions separately: +2 for the first, +5 for the second.")
S[5] = dict(raw=r"""Step 1: Count the days from 21 July to 21 November
July 21→31 = 10, August = 31, September = 30, October = 31, November 1→21 = 21.
Step 2: Total
\( 10 + 31 + 30 + 31 + 21 = 123 \) days
Step 3: Odd days
\( 123 = 17 \times 7 + 4 \), so there are 4 odd days.
Step 4: Move forward
Wednesday + 4 days = Sunday.""", trick=r"Same date, later month: add the days of the months in between and take the remainder by 7.")
S[6] = dict(raw=r"""Step 1: Place A
Only three cars are faster than A, so A is 4th from the top (second slowest).
Step 2: Place S
S is faster than at least four cars, so S is the fastest (1st).
Step 3: Place M and T
T is slower than M and S and T is not the slowest. The free places are 2nd, 3rd and 5th; T cannot be 5th, and M must be above T, so M is 2nd and T is 3rd.
Step 4: Answer
Order (fastest to slowest): S, M, T, A, B. So car B is the slowest.""", trick=r"Fix the cars with exact positions first (A 4th, S 1st), then fill the gaps.")
S[7] = dict(raw=r"""Step 1: Fix R and V
Facing the centre, right = anticlockwise. Place R; V is second to the right of R.
Step 2: Place U and T
T is third to the right of U, Q is next to T, and S sits next to T but not beside R or V. This works only when U is to the immediate right of R and T is three places further to the right.
Step 3: Place Q, S and P
S is the neighbour of T on the far side, Q is T's other neighbour, and P is third to the right of Q (because Q is third to the left of P). P lands in the seat to the immediate left of R.
Going right (anticlockwise) from R: R, U, V, Q, T, S, P.
Step 4: Answer
P sits to the immediate left of R.""", trick=r"Facing the centre: right = anticlockwise, left = clockwise.")
S[8] = dict(raw=r"""Step 1: Count the letters of ENDANGERED
E × 3, N × 2, D × 2, A × 1, G × 1, R × 1
Step 2: Check EARNED
E, A, R, N, E, D — needs E twice, A, R, N, D once each — all available.
Step 3: Check the other words
DECREE needs C; GARDENS needs S; DANGEROUS needs O, U and S — none of these letters is in ENDANGERED.
Step 4: Answer
Only EARNED can be formed.""", trick=r"Look for a letter the main word does not have — it rules a word out at once.")
S[9] = dict(raw=r"""Step 1: Count the letters of CALENDAR
C, A × 2, L, E, N, D, R
Step 2: Check LEND, CARD and CARNAL
LEND (L, E, N, D), CARD (C, A, R, D) and CARNAL (C, A, R, N, A, L — A twice) can all be formed.
Step 3: Check DENTAL
DENTAL needs the letter T, which is not in CALENDAR.
Step 4: Answer
DENTAL cannot be formed.""", trick=r"Scan each word for a missing letter (T here).")
S[10] = dict(raw=r"""Step 1: Find the daily rise
25.5 − 24.0 = 1.5, 27.2 − 25.5 = 1.7, 29.1 − 27.2 = 1.9
Step 2: Spot the pattern
The rise grows by 0.2 each day, so the next rises are 2.1 and 2.3.
Step 3: Day 5
\( 29.1 + 2.1 = 31.2 \)
Step 4: Day 6
\( 31.2 + 2.3 = 33.5 \), so the expected temperature is 33.5°C.""", trick=r"Differences 1.5, 1.7, 1.9 … rise by 0.2.")
S[11] = dict(raw=r"""Step 1: Study the first pair
An unshaded square (4 sides) in a frame becomes a shaded pentagon (5 sides) in a frame.
Step 2: Write the rule
The shape gains one side and changes from unshaded to shaded; the frame stays.
Step 3: Apply it to the hexagon
An unshaded hexagon (6 sides) must become a shaded heptagon (7 sides) in a frame.
Step 4: Reject the others
The unshaded heptagon fails the shading change, and the shaded or unshaded hexagon fails the +1 side change. The shaded heptagon is the answer.""", trick=r"Two changes together: sides +1, unshaded → shaded.")
S[12] = dict(raw=r"""Step 1: Compare the third figure with the second
Flip the second figure left to right: it becomes U _ V on top and H Z X at the bottom. The third figure has the same layout: ○ _ & on top and △ @ E at the bottom. So ○ takes U's place, & takes V's, △ takes H's, @ takes Z's and E takes X's.
Step 2: Flip the first figure left to right
The first figure (U H on top, Z in the middle, V X at the bottom, all on the right) becomes H U on top, Z in the middle and X V at the bottom, all on the left.
Step 3: Substitute the symbols
H → △ and U → ○ give △ ○ on top; Z → @ gives @ in the middle; X → E and V → & give E & at the bottom.
Step 4: Answer
The figure with △ ○ on top, @ in the middle and E & at the bottom completes the analogy.""", trick=r"Match the third figure with the mirror of the second, then copy the mirror of the first with the new symbols.")
S[13] = dict(raw=r"""Step 1: Study AL220 → MB240
A (1) + 1 = B and L (12) + 1 = M; the output writes the second letter's result first: MB. The number rises by 20.
Step 2: Check JK330 → LK350
K + 1 = L and J + 1 = K, written as LK; 330 + 20 = 350 ✓
Step 3: Apply the rule to ST110
T + 1 = U, S + 1 = T → UT; 110 + 20 = 130.
Step 4: Answer
The missing cluster is UT130.""", trick=r"Each letter +1, then swap their order; number +20.")
S[14] = dict(raw=r"""Step 1: Study DZ155 → GG355
D (4) + 3 = G and Z (26) + 7 = 33 − 26 = 7 = G; the number rises by 200.
Step 2: Check BK605 → ER805
B + 3 = E, K (11) + 7 = R (18) and 605 + 200 = 805 ✓
Step 3: Work backwards from DZ445
First letter: D − 3 = A. Second letter: Z − 7 = S (19). Number: 445 − 200 = 245.
Step 4: Answer
The missing cluster is AS245. Check: A + 3 = D, S + 7 = Z, 245 + 200 = 445 ✓""", trick=r"Rule is +3, +7, +200 — the blank comes first, so reverse it: −3, −7, −200.")
S[15] = dict(raw=r"""Step 1: Find the change in the given pairs
\( 5245 - 5191 = 54 \) and \( 8313 - 8259 = 54 \)
Step 2: Write the rule
Second number = first number + 54.
Step 3: Apply it to 7084
\( 7084 + 54 = 7138 \)
Step 4: Answer
The missing number is 7138.""", trick=r"Same fixed difference (+54) in both example pairs.")
S[16] = dict(raw=r"""Step 1: Recognise the cubes
\( 1728 = 12^{3} \) and \( 4913 = 17^{3} \)
Step 2: Link them with the first numbers
14 − 2 = 12 and 19 − 2 = 17, so the rule is (number − 2) cubed.
Step 3: Apply it to 29
\( 29 - 2 = 27 \) and \( 27^{3} = 19683 \)
Step 4: Answer
The missing number is 19683.""", trick=r"Learn cubes 10–30: 12³ = 1728, 17³ = 4913, 27³ = 19683.")
S[17] = dict(raw=r"""Step 1: Decode FIRE → IMNZ
F + 3 = I, I + 4 = M, R − 4 = N, E − 5 = Z (E is 5, 5 − 5 wraps to 26 = Z).
Step 2: Check POLE → SSHZ
P + 3 = S, O + 4 = S, L − 4 = H, E − 5 = Z ✓
Step 3: Apply +3, +4, −4, −5 to HIYA
H + 3 = K, I + 4 = M, Y − 4 = U, A − 5 = V (1 − 5 + 26 = 22).
Step 4: Answer
HIYA is coded as KMUV.""", trick=r"Position-wise shifts: +3, +4, −4, −5.")
S[18] = dict(raw=r"""Step 1: Codes common to two sentences
memory (1st and 2nd sentences) = so; thought (2nd and 3rd) = la; today and request (1st and 3rd) = vn / mk.
Step 2: More common codes
bring (1st and 4th) = nj; seat (2nd and 4th) = no; teach (3rd and 4th) = ta.
Step 3: The code left for prime
In the 4th sentence the codes are no, ta, nj, xl; no = seat, ta = teach, nj = bring, so prime = xl.
Step 4: Answer
'teach prime' is coded as 'xl ta' (the order of codes does not matter).""", trick=r"Pick out the word shared by two sentences and the code shared by the same two.")
S[19] = dict(raw=r"""Step 1: First letters
C, G, K, O, … go up by 4: C → G → K → O → S → W.
Step 2: Second letters and numbers
F, D, B, Z, X, V go back by 2, and the numbers are squares: 1, 4, 9, 16, 25, 36.
Step 3: Find the break
The fifth term should be S (O + 4) with X (Z − 2): SX25. The given TW25 breaks both letter rules.
Step 4: Answer
TW25 is the wrong term.""", trick=r"Check each part of the term on its own: +4, −2, n².")
S[20] = dict(raw=r"""Step 1: Total gain
The clock gains 6 minutes every hour, so in 18 hours it gains \( 18 \times 6 = 108 \) minutes = 1 hour 48 minutes.
Step 2: Relation between the times
Clock time = actual time + gain (the clock was correct when it was set 18 hours earlier).
Step 3: Subtract the gain
8:00 PM − 1 hour 48 minutes = 6:12 PM.
Step 4: Answer
The actual time is 6:12 PM.""", trick=r"Fast clock → subtract the total gain from what it shows.")
