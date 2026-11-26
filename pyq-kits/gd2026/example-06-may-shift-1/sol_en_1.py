S = {}
S[1] = dict(raw=r"""Step 1: Find the gaps between the terms
985 → 979 → 973 → 967 → 961 → 955 → 949: each step is −6.
Step 2: Apply the rule to the last term
After 949 the next term should be 949 − 6 = 943.
Step 3: Compare with the printed term
The series shows 946 instead of 943, so the gap there is only −3.
Step 4: Answer
All other terms fit the −6 rule; the wrong term is 946.""", trick=r"Constant-difference series: one term breaks the common gap — here −6.")
S[2] = dict(raw=r"""Step 1: Find the gaps
315 → 318 (+3), 318 → 323 (+5), 323 → 331 (+8), 331 → 339 (+8), 339 → 350 (+11), 350 → 363 (+13), 363 → 378 (+15).
Step 2: Spot the pattern in the gaps
The gaps should be consecutive odd numbers: +3, +5, +7, +9, +11, +13, +15.
Step 3: Rebuild the series
315, 318, 323, 330, 339, 350, 363, 378 — the fourth term should be 323 + 7 = 330.
Step 4: Answer
330 + 9 = 339 ✓, so only 331 breaks the pattern. The wrong term is 331.""", trick=r"Gaps +3, +5, +7, +9 …: when two gaps look odd (+8, +8), the term between them is wrong.")
S[3] = dict(raw=r"""Step 1: Find the gaps
−289 → −299 (−10), −299 → −310 (−11), −310 → −322 (−12), −322 → −335 (−13), −335 → −348 (−13), −348 → −364 (−16), −364 → −380 (−16).
Step 2: Spot the pattern
The gaps should grow by 1 each time: −10, −11, −12, −13, −14, −15, −16.
Step 3: Rebuild the series
−335 − 14 = −349, then −349 − 15 = −364 ✓ and −364 − 16 = −380 ✓.
Step 4: Answer
The sixth term should be −349, not −348. The wrong term is −348.""", trick=r"Gaps −10, −11, −12 …; the term between two broken gaps is the wrong one.")
S[4] = dict(raw=r"""Step 1: Split each cluster into first and second letters
First letters: D, H, L, P, T, X, ?, F. Second letters: D, Z, V, R, N, J, ?, B.
Step 2: Pattern of the first letters
D (4) → H (8) → L (12) → P (16) → T (20) → X (24): +4 each time. Next: 24 + 4 = 28 → 28 − 26 = 2 = B, and B + 4 = F ✓.
Step 3: Pattern of the second letters
D (4) → Z (26) → V (22) → R (18) → N (14) → J (10): −4 each time. Next: 10 − 4 = 6 = F, and F − 4 = B ✓.
Step 4: Answer
The missing cluster is BF.""", trick=r"First letter +4, second letter −4; after Z count again from A.")
S[5] = dict(raw=r"""Step 1: Pattern of the first letters
O (15) → L (12) → I (9) → F (6) → C (3): −3 each time. Next: 3 − 3 = 0 → Z (26), then W and T ✓.
Step 2: Pattern of the second letters
T (20) → Q (17) → M (13) → H (8) → B (2): the gap grows −3, −4, −5, −6.
Step 3: Continue the second letters
Next gap −7: 2 − 7 = −5 → 26 − 5 = 21 = U. Check: U (21) − 8 = 13 = M ✓, M (13) − 9 = 4 = D ✓.
Step 4: Answer
The missing cluster is ZU.""", trick=r"First letters −3 throughout; second letters −3, −4, −5, … (gap grows by 1).")
S[6] = dict(raw=r"""Step 1: Find the rule in (GE, II, LN)
First letters G (7) → I (9) → L (12): +2, +3. Second letters E (5) → I (9) → N (14): +4, +5.
Step 2: Confirm with (OQ, QU, TZ)
O (15) → Q (17) → T (20): +2, +3 ✓. Q (17) → U (21) → Z (26): +4, +5 ✓.
Step 3: Test the options
(GW, IA, LF): G → I → L is +2, +3 ✓; W (23) + 4 = 27 → A ✓, A (1) + 5 = F (6) ✓.
Step 4: Reject the rest
(JD, LI, PL) has L → P (+4) in the first letters; (RB, TH, XJ) has T → X (+4); (AQ, CU, GY) has C → G (+4). Only (GW, IA, LF) follows the rule.""", trick=r"First letters +2, +3; second letters +4, +5 — check both rows separately.")
S[7] = dict(raw=r"""Step 1: Join the “immediate left” clues
R is immediately left of S and S is immediately left of T, so R, S, T sit together in that order.
Step 2: Place A
A is second to the right of T, so one seat lies between T and A: R, S, T, _, A.
Step 3: Fill the gap
Only P is left, so the row from left to right is R, S, T, P, A.
Step 4: Find the middle
In a row of 5 the middle seat is the 3rd one — T sits in the middle.""", trick=r"Build the fixed block (R S T) first, then place the rest around it.")
S[8] = dict(raw=r"""Step 1: Fix U and use the two “second” clues
Facing the centre, a person's left is clockwise. Put U at seat 0; V (second to the left of U) is at seat 2 clockwise, and T (second to the right of U) is at seat 2 anticlockwise.
Step 2: Place S and P
S is next to both P and V. If S sat between U and V, its two neighbours would be U and V, leaving no room for P. So S sits on the other side of V (seat 3), and P sits next to S at seat 4, just before T at seat 5.
Step 3: Place R and Q
The two empty seats are between U and V, and between T and U. R is not next to V, so R sits between T and U and Q sits between U and V.
Step 4: Read the answer
Clockwise from U: U, Q, V, S, P, T, R. R's immediate right is the seat anticlockwise from R, which is T.""", trick=r"Facing the centre: left = clockwise, right = anticlockwise.")
S[9] = dict(raw=r"""Step 1: Study the first pair
The first figure has 3 straight lines; the related figure is a triangle, a shape with 3 sides.
Step 2: Find the rule
Number of lines in the first figure = number of sides of the shape in the second figure.
Step 3: Apply it to the third figure
The third figure has 4 lines (2 vertical and 2 horizontal), so the answer must be a shape with 4 sides.
Step 4: Answer
Pentagon (5), circle (0) and hexagon (6) do not fit; the square (4 sides) is the answer.""", trick=r"Count the lines → draw a shape with that many sides.")
S[10] = dict(raw=r"""Step 1: Study the first pair
Top to bottom the first figure has triangle, square, circle; left to right the second figure has square, triangle, circle.
Step 2: Find the rule
The figure is turned from a column into a row, the first two symbols swap places, the last one stays last, and nothing changes its shape or shading.
Step 3: Apply it to the third figure
Column: outline right-angled triangle, R, square → row: R, triangle, square, with the triangle exactly as it was (outline, same direction).
Step 4: Answer
The row “R, outline triangle, square” is the answer; the other rows have the wrong order, a turned triangle or a filled triangle.""", trick=r"Column → row: swap the first two symbols, keep the last; shapes and shading stay the same.")
S[11] = dict(raw=r"""Step 1: Study AZ300 → CD440
A (1) + 2 = C (3); Z (26) + 4 = 30 → D (4); 300 + 140 = 440.
Step 2: Confirm with BY400 → DC540
B (2) + 2 = D (4); Y (25) + 4 = 29 → C (3); 400 + 140 = 540 ✓.
Step 3: Apply to CX200
C (3) + 2 = E (5); X (24) + 4 = 28 → B (2); 200 + 140 = 340.
Step 4: Answer
CX200 → EB340.""", trick=r"First letter +2, second letter +4 (past Z, start again at A), number +140.")
S[12] = dict(raw=r"""Step 1: Study AJ80 → GF200
A (1) + 6 = G (7); J (10) − 4 = F (6); 80 × 2.5 = 200.
Step 2: Confirm with DL70 → JH175
D (4) + 6 = J (10); L (12) − 4 = H (8); 70 × 2.5 = 175 ✓.
Step 3: Work backwards from MM225
First letter: ? + 6 = M (13) → G (7). Second letter: ? − 4 = M (13) → Q (17). Number: ? × 2.5 = 225 → 90.
Step 4: Answer
The missing cluster is GQ90 (check: G + 6 = M, Q − 4 = M, 90 × 2.5 = 225 ✓).""", trick=r"When the blank is on the left, reverse every step: −6, +4, ÷2.5.")
S[13] = dict(raw=r"""Step 1: Study 4740 → 4770
4770 − 4740 = 30.
Step 2: Confirm with 670 → 700
700 − 670 = 30 ✓, so the rule is “add 30”.
Step 3: Apply to 2049
2049 + 30 = 2079.
Step 4: Answer
The number related to 2049 is 2079.""", trick=r"Subtract within each pair; the same difference gives the rule.")
S[14] = dict(raw=r"""Step 1: Study 867 → 1341
1341 − 867 = 474.
Step 2: Confirm with 776 → 1250
1250 − 776 = 474 ✓, so the second number = first number + 474.
Step 3: Work backwards from 541
? + 474 = 541 → ? = 541 − 474 = 67.
Step 4: Answer
The missing number is 67.""", trick=r"Find the common difference (474), then reverse it for the blank.")
S[15] = dict(raw=r"""Step 1: Compare WOOD with BNLY letter by letter
W (23) + 5 = 28 → B (2); O (15) − 1 = N (14); O (15) − 3 = L (12); D (4) − 5 = −1 → Y (25).
Step 2: Confirm with BYTE → GXQZ
B (2) + 5 = G (7); Y (25) − 1 = X (24); T (20) − 3 = Q (17); E (5) − 5 = 0 → Z (26) ✓.
Step 3: Apply +5, −1, −3, −5 to BOOS
B + 5 = G; O − 1 = N; O − 3 = L; S (19) − 5 = N (14).
Step 4: Answer
BOOS is coded as GNLN.""", trick=r"Position-wise shifts: +5, −1, −3, −5.")
S[16] = dict(raw=r"""Step 1: Compare sentences 1 and 2
“india” is common to “india won world cup” and “india plays cricket”; “pq” is common to their codes, so india = pq.
Step 2: Compare sentences 2 and 3
“cricket” is common to “india plays cricket” and “cricket england sport”; “tm” is common to their codes, so cricket = tm.
Step 3: Combine
“india cricket” = pq + tm.
Step 4: Answer
The code is “pq tm” (the order of word codes does not matter, but both codes must be present).""", trick=r"Common word ↔ common code.")
S[17] = dict(raw=r"""Step 1: First letters
K (11), ?, G (7), E (5), C (3): −2 each time, so the missing first letter is I (9).
Step 2: Second letters
M (13), ?, G (7), D (4), A (1): −3 each time, so the missing second letter is J (10).
Step 3: Numbers
126, ?, 378, 504, 630: +126 each time, so the missing number is 252.
Step 4: Answer
The missing term is IJ252.""", trick=r"Treat the letters and the number as three separate series.")
S[18] = dict(raw=r"""Step 1: Numbers
32, 48, ?, 108, 162, 243: each term is × 1.5 (32 × 1.5 = 48, 72 × 1.5 = 108, 108 × 1.5 = 162, 162 × 1.5 = 243). The third number should be 72, not 70.
Step 2: First letters
M (13), O (15), ?, S (19), U (21), W (23): +2 each time, so the third should be Q, not R.
Step 3: Second and third letters
Second letters A, E, ?, M, Q, U go +4 (I, not H); third letters N, T, ?, F, L, R go +6 (Z, not Y).
Step 4: Answer
The correct third term is QIZ72, so RHY70 is the wrong term.""", trick=r"Check the number first (× 1.5 here) — it often finds the wrong term quickly.")
S[19] = dict(raw=r"""Step 1: Use the overlap formula
Between H and H + 1 o'clock the hands overlap at \( \dfrac{60H}{11} \) minutes past H.
Step 2: Put H = 2
\( \dfrac{60 \times 2}{11} = \dfrac{120}{11} = 10\dfrac{10}{11} \) minutes.
Step 3: Convert
\( 10\dfrac{10}{11} \) minutes ≈ 10 minutes 55 seconds past 2.
Step 4: Answer
The hands overlap at about 2:11 AM.""", trick=r"Overlap time = 60H/11 minutes past H.")
S[20] = dict(raw=r"""Step 1: Find how much the watch must gain
It is 2 minutes slow, so it must gain 2 minutes = 120 seconds.
Step 2: Find the time needed
It gains 4 seconds per hour, so it needs \( \dfrac{120}{4} = 30 \) hours.
Step 3: Add the time
10 PM + 24 hours = 10 PM next day; + 6 more hours = 4 AM.
Step 4: Answer
The watch shows the correct time again at 4:00 AM.""", trick=r"Hours needed = time to make up ÷ gain per hour.")
