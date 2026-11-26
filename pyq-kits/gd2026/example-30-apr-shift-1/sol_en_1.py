S = {}
S[1] = dict(raw=r"""Step 1: Study KS → PH
K (11) and P (16) add up to 27, and S (19) and H (8) add up to 27. So each letter is replaced by its opposite letter (A ↔ Z, B ↔ Y …).
Step 2: Confirm with DN → WM
D (4) + W (23) = 27 and N (14) + M (13) = 27 ✓ — the same opposite-letter rule.
Step 3: Work back from TQ
The missing cluster's opposite letters must be T and Q. Opposite of T (20) is G (7); opposite of Q (17) is J (10).
Step 4: Answer
The missing cluster is GJ. Check: G ↔ T and J ↔ Q ✓""", trick=r"Opposite letters always add up to 27 (A + Z = 1 + 26).")
S[2] = dict(raw=r"""Step 1: Read the first set (KI, IG, FD)
First letters K → I → F move −2, then −3. Second letters I → G → D also move −2, then −3.
Step 2: Confirm with (IJ, GH, DE)
I → G → D is −2, −3 and J → H → E is −2, −3 ✓
Step 3: Test the options
(KT, IR, FO): K → I → F is −2, −3 and T → R → O is −2, −3 ✓
(IA, FX, BU) starts with I → F (−3); (JF, IC, EZ) starts with J → I (−1); (JI, EF, DC) starts with J → E (−5) — all break the rule.
Step 4: Answer
The set (KT, IR, FO) follows the same rule.""", trick=r"Check the first jump of each option first — most wrong sets fail at once.")
S[3] = dict(raw=r"""Step 1: Know the rule
Two years have the same calendar when they start on the same day and are both leap or both ordinary years. 2025 is an ordinary year.
Step 2: Count odd days from 2025
Ordinary year = 1 odd day, leap year = 2 odd days. 2025 (1) + 2026 (1) + 2027 (1) + 2028 (2) + 2029 (1) + 2030 (1) = 7 odd days.
Step 3: Conclude
7 odd days make a complete week, so 1 January 2031 falls on the same day as 1 January 2025, and 2031 is also an ordinary year.
Step 4: Reject the others
2036 is a leap year, so it can never match 2025; 2037 and 2043 do not give a total that is a multiple of 7 from 2025 to the year before them.""", trick=r"For an ordinary year just after a leap year (like 2025), the calendar repeats after 6 years.")
S[4] = dict(raw=r"""Step 1: Place E
In a row of 5, E is second from the left, so E is at seat 2.
Step 2: Place B and D
B and D are the immediate neighbours of E, so they take seats 1 and 3. B is not at an end, so B = 3 and D = 1.
Step 3: Place A and C
Seats 4 and 5 are left, and C is to the immediate right of A, so A = 4 and C = 5.
Order from left: D, E, B, A, C.
Step 4: Count
C is at the right end, so 4 boys sit to its left.""", trick=r"Fix the 'second from the end' person first, then the neighbours.")
S[5] = dict(raw=r"""Step 1: Place K
K is taller than only 3 persons, so exactly 2 persons are taller than K — K is 3rd from the top.
Step 2: Place J
J is taller than M, N and O, so J is in the top 3. J is not the tallest and is not K, so J is 2nd.
Step 3: Fix the order
The tallest must be L. Order: L > J > K > (M, N, O in some order).
Step 4: Height of M
M is shorter than K, and K is shorter than J (165 cm), so M is less than 165 cm. Among the given values only 160 cm is less than 165 cm.""", trick=r"Anyone below J must be under 165 cm — only one option is.")
S[6] = dict(raw=r"""Step 1: List the letters of AGRICULTURE
A, G, R, R, I, C, U, U, L, T, E — note there is no S and no D.
Step 2: Test ARTICLES and RECRUITS
Both need an S, which AGRICULTURE does not have.
Step 3: Test CULTURED
It needs a D, which is not there.
Step 4: Test GLACIER
G, L, A, C, I, E, R — each letter is available once ✓ So GLACIER can be formed.""", trick=r"First look for a letter that is missing altogether (S, D).")
S[7] = dict(raw=r"""Step 1: Count the letters of CONGRATULATIONS
C 1, O 2, N 2, G 1, R 1, A 2, T 2, U 1, L 1, I 1, S 1 — there is no E.
Step 2: Check SOLUTION, CARTON and RATIONAL
SOLUTION needs S, O, O, L, U, T, I, N; CARTON needs C, A, R, T, O, N; RATIONAL needs R, A, A, T, I, O, N, L — all available ✓
Step 3: Check LANGUAGES
It needs two Gs and an E, but CONGRATULATIONS has only one G and no E.
Step 4: Answer
LANGUAGES cannot be formed.""", trick=r"A letter that does not exist (E) settles it at once.")
S[8] = dict(raw=r"""Step 1: Find the differences
444 − 432 = 12, 432 − 420 = 12, 420 − 408 = 12
Step 2: Pattern
Each term is 12 less than the one before it.
Step 3: Next term
\( 408 - 12 = 396 \)
Step 4: Answer
The missing number is 396.""", trick=r"Constant gap −12.")
S[9] = dict(raw=r"""Step 1: Find the differences
842 − 826 = 16, 826 − 794 = 32, 794 − 746 = 48
Step 2: Pattern
The gaps are 16, 32, 48 — multiples of 16 (\( 16 \times 1, 16 \times 2, 16 \times 3 \)), so the next gap is \( 16 \times 4 = 64 \).
Step 3: Next term
\( 746 - 64 = 682 \)
Step 4: Answer
The missing number is 682.""", trick=r"Gaps grow by 16 each time.")
S[10] = dict(raw=r"""Step 1: Test multiply-and-add
\( 7 \times 3 + 1 = 22 \), \( 22 \times 4 + 4 = 92 \), \( 92 \times 5 + 9 = 469 \), \( 469 \times 6 + 16 = 2830 \)
Step 2: Spot the pattern
The multipliers are 3, 4, 5, 6 and the numbers added are \( 1^{2}, 2^{2}, 3^{2}, 4^{2} \).
Step 3: Next term
\( 2830 \times 7 + 5^{2} = 19810 + 25 = 19835 \)
Step 4: Answer
The next number is 19,835.""", trick=r"Rule: × (3, 4, 5 …) + (1, 4, 9 …).")
S[11] = dict(raw=r"""Step 1: Compare the first two figures
In the first figure the triangle end of the stick points down and the pentagon is on the right. In the second figure the triangle (now an arrowhead) points to the top-right and the pentagon is at the top-left.
Step 2: Find the rotation
Down → top-right and right → top-left are both turns of 135° anticlockwise, so the whole figure is rotated 135° anticlockwise.
Step 3: Rotate the third figure
In the third figure the arrow points left and the circle is on the right. A 135° anticlockwise turn sends the arrow to point bottom-right and the circle to the top-left.
Step 4: Match
The figure with the circle at the top-left and the arrow pointing to the bottom-right on crossed lines is the answer; the other figures show the arrow or circle in the wrong place.""", trick=r"Track two parts (arrow and circle) — both must turn the same way by the same angle.")
S[12] = dict(raw=r"""Step 1: Corners in the first pair
Top row: ● and P swap places. Bottom row: Q and ▲ swap places.
Step 2: Middle row in the first pair
ACBD → DACB: the last letter moves to the front and the rest shift right.
Step 3: Apply to the third figure
Top Z, X → X, Z; bottom Y, W → W, Y; middle ● ▲ ☗ ■ → ■ ● ▲ ☗ (last symbol to the front).
Step 4: Match
The figure with X Z on top, ■ ● ▲ ☗ in the middle and W Y at the bottom is the answer. One option keeps W at top-right, and the others put the middle symbols in a different order.""", trick=r"Corners swap within each row; middle row = last item to the front.")
S[13] = dict(raw=r"""Step 1: Letters in BL95 → OE141
L (12) + 3 = O (15) and B (2) + 3 = E (5): the two letters are swapped and each moves 3 forward.
Step 2: Check DK81 → NG127
K (11) + 3 = N (14), D (4) + 3 = G (7) ✓ Numbers: \( 95 + 46 = 141 \) and \( 81 + 46 = 127 \).
Step 3: Apply to KF63
Swap and +3: F (6) + 3 = I (9), K (11) + 3 = N (14) → IN. Number: \( 63 + 46 = 109 \).
Step 4: Answer
IN109""", trick=r"Swap the letters, +3 each; number +46.")
S[14] = dict(raw=r"""Step 1: Read YXD500 → VUA260
Y − 3 = V, X − 3 = U, D − 3 = A; \( 500 - 240 = 260 \).
Step 2: Confirm with KMO480 → HJL240
K − 3 = H, M − 3 = J, O − 3 = L; \( 480 - 240 = 240 \) ✓
Step 3: Apply to RTU420
R (18) − 3 = O (15), T (20) − 3 = Q (17), U (21) − 3 = R (18); \( 420 - 240 = 180 \).
Step 4: Answer
OQR180""", trick=r"Each letter −3, number −240.")
S[15] = dict(raw=r"""Step 1: First pair
\( 6307 - 6251 = 56 \)
Step 2: Second pair
\( 8253 - 8197 = 56 \) — the same difference.
Step 3: Apply
\( 4661 - 56 = 4605 \)
Step 4: Answer
The missing number is 4605.""", trick=r"Both pairs drop by 56.")
S[16] = dict(raw=r"""Step 1: Read the pairs in the right direction
The third number is related to the fourth: \( 714 - 393 = 321 \).
Step 2: Confirm
\( 759 - 438 = 321 \) ✓ — the first number of each pair is 321 more than the second.
Step 3: Apply to the pair ending in 581
\( ? = 581 + 321 = 902 \)
Step 4: Answer
The missing number is 902.""", trick=r"Gap 321; the missing number is the larger one, so add.")
S[17] = dict(raw=r"""Step 1: Compare SKIS with XJFN
S → X (+5), K → J (−1), I → F (−3), S → N (−5).
Step 2: Confirm with SAWS → XZTN
S → X (+5), A → Z (−1, wrapping round), W → T (−3), S → N (−5) ✓ — the shifts go by position: +5, −1, −3, −5.
Step 3: Apply to MAMA
M + 5 = R, A − 1 = Z, M − 3 = J, A − 5 = V (1 − 5 + 26 = 22).
Step 4: Answer
MAMA is coded as RZJV.""", trick=r"Same position → same shift (+5, −1, −3, −5).")
S[18] = dict(raw=r"""Step 1: Sentences 1 and 2
'song pen' is common and 'psk gsk' is common, so song and pen are psk and gsk.
Step 2: Sentences 1 and 3
'work' is the only common word and 'ask' the only common code, so work = ask.
Step 3: Find bus
Sentence 1 has work song pen bus = psk gsk msk ask. Removing psk, gsk (song, pen) and ask (work) leaves bus = msk.
Step 4: Answer
'bus work' = ask msk (order of codes does not matter).""", trick=r"Common word ↔ common code between two sentences.")
S[19] = dict(raw=r"""Step 1: Letter part
CD, DE, EF, FG — both letters move one step forward, so the next pair is GH.
Step 2: Number part
24, 200, 376, 552 — the differences are 176 each.
Step 3: Next number
\( 552 + 176 = 728 \)
Step 4: Answer
GH728""", trick=r"Letters +1, numbers +176.")
S[20] = dict(raw=r"""Step 1: Rate of losing time
From 10:30 AM to 4:30 PM is 6 hours, and the clock falls back from 3 to 9 minutes slow — it loses 6 minutes in 6 hours, i.e. 1 minute per hour.
Step 2: Time to go back
At 10:30 AM it is 3 minutes slow. It was correct when it had lost 0 minutes, i.e. 3 hours earlier.
Step 3: Find the time
\( 10:30 \text{ AM} - 3 \text{ hours} = 7:30 \text{ AM} \)
Step 4: Check
From 7:30 AM to 4:30 PM is 9 hours → 9 minutes slow ✓""", trick=r"Minutes slow ÷ minutes lost per hour = hours since it was correct.")
