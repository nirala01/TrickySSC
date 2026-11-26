S = {}
S[1] = dict(raw=r"""Step 1: Write the letter positions
Q (17), V (22), B (2), I (9), ?, Z (26), J (10), U (21).
Step 2: Find the gaps
Q → V is +5, V → B is +6 (22 + 6 = 28 → 28 − 26 = 2), B → I is +7. The gaps grow by 1.
Step 3: Find the missing letter
The next gap is +8: \( 9 + 8 = 17 \) = Q.
Step 4: Check the rest
Q (17) + 9 = 26 = Z ✓, Z (26) + 10 = 36 − 26 = 10 = J ✓, J (10) + 11 = 21 = U ✓. The missing letter is Q.""", trick=r"Gaps +5, +6, +7, +8 …; subtract 26 whenever you pass Z.")
S[2] = dict(raw=r"""Step 1: Read the relation
The question says: 1st cluster is to 2nd as ? is to 4th (RJK), and as 5th is to 6th. So ABQ → CDS and RMN → TOP give the rule, and ? → RJK.
Step 2: Find the rule
A → C, B → D, Q → S: each letter +2. R → T, M → O, N → P: each letter +2 ✓.
Step 3: Work backwards from RJK
? + 2 = RJK, so each letter of ? is 2 less: R − 2 = P, J − 2 = H, K − 2 = I.
Step 4: Answer
The missing cluster is PHI (check: P + 2 = R, H + 2 = J, I + 2 = K ✓).""", trick=r"+2 on every letter; to go back from the result, subtract 2.")
S[3] = dict(raw=r"""Step 1: Write the first letters
Y (25), V (22), S (19), P (16), M (13), J (10), G (7): each is −3, so the next first letter is \( 7 - 3 = 4 \) = D.
Step 2: Write the second letters
J (10), H (8), E (5), A (1), V (22), P (16), I (9).
Step 3: Find the gaps
J → H is −2, H → E is −3, E → A is −4, A → V is −5 (1 − 5 = −4 → 22), V → P is −6, P → I is −7. So the next gap is −8.
Step 4: Fill the blank
I (9) − 8 = 1 = A. The missing term is DA.""", trick=r"First letters −3; second letters −2, −3, −4 … (wrap past A to Z).")
S[4] = dict(raw=r"""Step 1: Find the rule in LI → HD
L (12) → H (8) is −4, I (9) → D (4) is −5.
Step 2: Confirm with GA → CV
G (7) → C (3) is −4, A (1) → V is −5 (1 − 5 = −4 → 22 = V) ✓.
Step 3: Work backwards for ? → RY
First letter: ? − 4 = R (18), so ? = 22 = V. Second letter: ? − 5 = Y (25), so ? = 30 → 30 − 26 = 4 = D.
Step 4: Answer
The missing cluster is VD (check: V − 4 = R, D − 5 = −1 → 25 = Y ✓).""", trick=r"Rule −4, −5; to find the first term, add 4 and 5 back.")
S[5] = dict(raw=r"""Step 1: Study (HB, LF, OU)
H (8) → L (12) is +4 and B (2) → F (6) is +4. Then O is the opposite letter of L (12 + 15 = 27) and U is the opposite of F (6 + 21 = 27).
Step 2: Confirm with (AR, EV, VE)
A → E and R → V are +4. V is the opposite of E (5 + 22 = 27) and E is the opposite of V ✓.
Step 3: Test the options
(RI, VM, EN): R (18) → V (22) and I (9) → M (13) are +4; E is the opposite of V and N is the opposite of M (13 + 14 = 27) ✓. In (MH, QI, MP), H → I is +1; in (NM, RN, LK), M → N is +1; in (ZO, DP, ZH), O → P is +1.
Step 4: Answer
Only (RI, VM, EN) follows the rule: +4 for the second cluster, opposite letters for the third.""", trick=r"Opposite letters add up to 27 (A–Z, E–V, M–N).")
S[6] = dict(raw=r"""Step 1: Count the days left in this month
The month has 29 days, so from the 10th to the 29th there are \( 29 - 10 = 19 \) days.
Step 2: Add the days of the next month
From the 29th to the 19th of the next month: \( 19 + 19 = 38 \) days.
Step 3: Find the odd days
\( 38 \div 7 \) leaves a remainder of 3, so the day moves 3 places forward.
Step 4: Answer
Friday + 3 = Monday. The 19th of the next month is a Monday.""", trick=r"Total gap in days ÷ 7 → remainder = days to move forward.")
S[7] = dict(raw=r"""Step 1: Note the type of year
2010 is an ordinary year (not a leap year), so we need a later year with the same first day and also an ordinary year.
Step 2: Count odd days year by year
Ordinary year = 1 odd day, leap year = 2. From 2010 to 2020: 2010, 2011, 2013, 2014, 2015, 2017, 2018, 2019 give 1 each (8) and 2012, 2016, 2020 give 2 each (6).
Step 3: Total the odd days
\( 8 + 6 = 14 \), and \( 14 \div 7 \) leaves 0, so 2021 starts on the same day as 2010.
Step 4: Answer
2021 is also an ordinary year, so the calendar of 2010 repeats in 2021.""", trick=r"Year after a leap year (like 2010, 2 years after 2008): calendar repeats after 11 years.")
S[8] = dict(raw=r"""Step 1: Find the differences of the known terms
−408 → −424 is −16, −462 → −484 is −22, −484 → −508 is −24, −508 → −534 is −26, −534 → −562 is −28.
Step 2: Spot the pattern
The differences grow by 2: −16, −18, −20, −22, −24 …
Step 3: Fill the gap
\( -424 - 18 = -442 \).
Step 4: Check
\( -442 - 20 = -462 \) ✓, which matches the next given term. The missing term is −442.""", trick=r"Differences −16, −18, −20 …: each gap is 2 more than the last.")
S[9] = dict(raw=r"""Step 1: Place D
Only C and F are to the left of D, so D is third from the left.
Step 2: Place G and H
Only H is to the right of G, so G is fourth and H is fifth (the right end).
Step 3: Place F and C
F is at an extreme end; the right end is H, so F is first and C is second.
Step 4: Answer
Order from the left: F, C, D, G, H. The person at the right end is H.""", trick=r"'Only X to the right of Y' → Y is second from the right, X at the right end.")
S[10] = dict(raw=r"""Step 1: Fix C, S and P
Number the seats so that 'to the right' means moving one seat on. Put C at seat 0. S is fifth to the right of C, so S = seat 5. S is second to the right of P, so P = seat 3.
Step 2: Place Q
Free seats: 1, 2, 4, 6. Q is not a neighbour of P (seats 2, 4) or S (seats 4, 6), so Q = seat 1.
Step 3: Place A and B
B is fourth to the right of A. With A = 2, B = \( 2 + 4 = 6 \) (free) ✓; A = 4 or 6 would put B on a taken seat. So A = 2, B = 6 and R = 4.
Step 4: Count to the left of B
Going left from B (seat 6): S (5), R (4), P (3), then A (2). Between B and A there are 3 boys.""", trick=r"Fix the person mentioned most (S), then place the rest by elimination.")
S[11] = dict(raw=r"""Step 1: Compare the first two figures
In the first figure the small square and the triangle-arrow are above the bar, and the Y-shape and the dot are below it. In the second figure they have changed places: the square and the triangle are below, the Y-shape and the dot are above.
Step 2: Find the rule
Left and right positions stay the same while top and bottom swap — the second figure is the water image (vertical flip) of the first.
Step 3: Apply it to the third figure
The third figure has a Y-shape (left) and a triangle-arrow (right) on top and a dot and a square below. Its water image has the dot and the square on top, and below the bar an upside-down Y on the left and a triangle pointing up on the right.
Step 4: Answer
Figure 1 matches this water image exactly; the other figures swap left and right or keep the top and bottom unchanged.""", trick=r"Water image: top ↔ bottom, left and right unchanged.")
S[12] = dict(raw=r"""Step 1: Count the arrows in the first figure
The diamond has 6 arrows pointing outwards.
Step 2: Find the rule
The second figure has 6 letters A — the number of letters equals the number of arrows.
Step 3: Count the arrows in the third figure
The rectangle has 3 arrows on the left and 2 on the right: \( 3 + 2 = 5 \) arrows.
Step 4: Answer
So the answer must have 5 letters F. Figure 2 has 5 F's; the others have 7, 6 and 6.""", trick=r"Count the parts in the first figure — that count becomes the number of letters.")
S[13] = dict(raw=r"""Step 1: Study TU130 → TS90
The output letters come from the input letters swapped and moved back by 1: U − 1 = T, T − 1 = S → TS. The number: \( 130 - 40 = 90 \).
Step 2: Confirm with AW95 → VZ55
W − 1 = V, A − 1 = Z (wraps to the end) → VZ ✓, and \( 95 - 40 = 55 \) ✓.
Step 3: Work backwards for ? → TR80
The second input letter − 1 = T, so it is U; the first input letter − 1 = R, so it is S. The number is \( 80 + 40 = 120 \).
Step 4: Answer
The missing cluster is SU120.""", trick=r"Swap the two letters, move each back by 1, and subtract 40.")
S[14] = dict(raw=r"""Step 1: Study BZA80 → AXX440
B → A (−1), Z → X (−2), A → X (−3, wrapping past A), and \( 80 + 360 = 440 \).
Step 2: Confirm with LMK110 → KKH470
L → K (−1), M → K (−2), K → H (−3), and \( 110 + 360 = 470 \) ✓.
Step 3: Apply to TJP90
T − 1 = S, J − 2 = H, P − 3 = M, and \( 90 + 360 = 450 \).
Step 4: Answer
The missing cluster is SHM450.""", trick=r"Letters −1, −2, −3 and the number +360.")
S[15] = dict(raw=r"""Step 1: Test 167 → 497
\( 167 \times 3 = 501 \), and \( 501 - 4 = 497 \) ✓.
Step 2: Confirm with 437 → 1307
\( 437 \times 3 = 1311 \), and \( 1311 - 4 = 1307 \) ✓. So the rule is ×3 − 4.
Step 3: Work backwards for ? → 62
\( 3 \times ? - 4 = 62 \), so \( 3 \times ? = 66 \) and ? = 22.
Step 4: Check
\( 22 \times 3 - 4 = 66 - 4 = 62 \) ✓. The missing number is 22.""", trick=r"Rule ×3 − 4; reverse it with +4 then ÷3.")
S[16] = dict(raw=r"""Step 1: Compare NIPS with ONON
N (14) → O (15) is +1, I (9) → N (14) is +5, P (16) → O (15) is −1, S (19) → N (14) is −5.
Step 2: Confirm with SILT → TNKO
S → T (+1), I → N (+5), L (12) → K (11) (−1), T (20) → O (15) (−5) ✓.
Step 3: Apply to TOGA
T (20) + 1 = U, O (15) + 5 = T, G (7) − 1 = F, A (1) − 5 = −4 → 22 = V.
Step 4: Answer
TOGA is coded as UTFV.""", trick=r"Pattern +1, +5, −1, −5 on the four letters.")
S[17] = dict(raw=r"""Step 1: Find how much time must be gained
The watch is 7 minutes slow, so it must gain 7 minutes = \( 7 \times 60 = 420 \) seconds.
Step 2: Find the hours needed
It gains 7 seconds per hour, so it needs \( 420 \div 7 = 60 \) hours.
Step 3: Add the hours to 2 PM
60 hours = 2 days + 12 hours. 2 PM + 12 hours = 2 AM.
Step 4: Answer
The watch will show the correct time again at 2:00 AM.""", trick=r"Time needed = total lag ÷ gain per hour (both in the same unit).")
S[18] = dict(raw=r"""Step 1: Watch the pattern grow
Figure 1: a square with a line up. Figure 2: a line to the right is added. Figure 3: a second square at the end of that line. Figure 4: a line going down from the second square.
Step 2: Find the rule
One new part is added at the free end each time — line, square, line, square … — and the last square is shaded in figures 2 and 4 but open in figures 1 and 3.
Step 3: Predict the fifth figure
A third square is added at the bottom of the downward line, and as an odd-numbered figure all squares are open.
Step 4: Answer
Figure 3 shows the open square added below with no extra line — it fits.""", trick=r"Each step adds one part at the free end; shading alternates.")
S[19] = dict(raw=r"""Step 1: Name the five positions
Top-left (1), top-middle (2), top-right (3), middle (4) and bottom (5). Figure 1: ▲ R H / F / C.
Step 2: Track each symbol from figure 1 to figure 2
▲ goes 1 → 2, R goes 2 → 3, H goes 3 → 5, C goes 5 → 4 and F goes 4 → 1, giving F ▲ R / C / H ✓.
Step 3: Apply the same movement again
Figure 3 (C F ▲ / H / R) and figure 4 (H C F / R / ▲) follow the same rule. From figure 4: H 1 → 2, C 2 → 3, F 3 → 5, ▲ 5 → 4, R 4 → 1.
Step 4: Answer
Figure 5 is R H C / ▲ / F, which is figure 3.""", trick=r"Same movement every step: 1→2→3→5→4→1.")
S[20] = dict(raw=r"""Step 1: Use the ratio
Let the ages be 5k and 7k (ratio \( 5 : 7 \)).
Step 2: Use the difference
\( 7k - 5k = 2k = 6 \), so k = 3. M = 15 years, S = 21 years.
Step 3: Add 9 years
M = \( 15 + 9 = 24 \), S = \( 21 + 9 = 30 \).
Step 4: Simplify the ratio
\( 24 : 30 = 4 : 5 \).""", trick=r"Difference of ratio parts = difference of ages → find one part first.")
