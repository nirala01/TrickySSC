S = {}
S[1] = dict(raw=r"""Step 1: Split each term into its first and second letter
First letters: ?, L, J, H, F, D, B, Z. Second letters: ?, Y, T, N, G, Y, P, F.
Step 2: Find the rule for the first letters
L (12) → J (10) → H (8) → F (6) → D (4) → B (2) → Z (0 → 26): each step is −2. So the first letter of the missing term is L + 2 = N (14).
Step 3: Find the rule for the second letters
Y (25) → T (20) → N (14) → G (7) → Y (−1 → 25) → P (16) → F (6): the gaps are −5, −6, −7, −8, −9, −10. Going one step back, the gap before Y must be −4, so the missing letter is Y + 4 = 29 → 29 − 26 = 3 = C.
Step 4: Answer
The missing term is NC (N − 2 = L ✓ and C − 4 = Y ✓).""", trick=r"First letters −2 each; second letters −4, −5, −6 … −10.")
S[2] = dict(raw=r"""Step 1: First letters
K (11) → O (15) → T (20) → X (24) → C (29 → 3) → G (7): the gaps alternate +4, +5, +4, +5, +4. The next gap is +5, so G + 5 = L (12); check L + 4 = P (16) ✓.
Step 2: Second letters
Z (26) → V (22) → Q (17) → K (11) → D (4) → V (4 − 8 = −4 → 22): the gaps are −4, −5, −6, −7, −8.
Step 3: Find the missing second letter
The next gap is −9: V (22) − 9 = 13 = M. Check: M (13) − 10 = 3 = C ✓, which matches the last term PC.
Step 4: Answer
The missing term is LM.""", trick=r"First letters +4, +5 alternately; second letters −4, −5, −6 …")
S[3] = dict(raw=r"""Step 1: First letters
I (9) → L (12) → Q (17) → T (20) → Y (25) → B (28 → 2): the gaps alternate +3, +5, +3, +5, +3.
Step 2: Missing first letter
The next gap is +5: B (2) + 5 = G (7). Check: G + 3 = J (10) ✓ (last term JD).
Step 3: Second letters
F (6) → E (5) → C (3) → Z (0 → 26) → V (22) → Q (17): the gaps are −1, −2, −3, −4, −5. The next gap is −6: Q (17) − 6 = K (11). Check: K − 7 = D (4) ✓.
Step 4: Answer
The missing term is GK.""", trick=r"First letters +3, +5 alternately; second letters −1, −2, −3 …")
S[4] = dict(raw=r"""Step 1: Study the first set (HW, KA, OF)
First letters H (8) → K (11) → O (15): +3, then +4. Second letters W (23) → A (27 → 1) → F (6): +4, then +5.
Step 2: Confirm with the second set (NU, QY, UD)
N (14) → Q (17) → U (21) is +3, +4 and U (21) → Y (25) → D (30 → 4) is +4, +5 ✓.
Step 3: Test the options
(JK, MO, QT): J (10) → M (13) → Q (17) is +3, +4 and K (11) → O (15) → T (20) is +4, +5 ✓. In (WL, XO, ZU) the first letters move +1, +2; in (DL, GQ, IU) they move +3, +2; in (DW, HX, MF) they move +4, +5 ✗.
Step 4: Answer
Only (JK, MO, QT) follows the rule.""", trick=r"First letters +3, +4; second letters +4, +5.")
S[5] = dict(raw=r"""Step 1: Count odd days up to 1600
1600 years leave 0 odd days.
Step 2: Odd days from 1601 to 1677
There are 77 years, of which 19 are leap years (1604, 1608, …, 1676). Odd days \( = 77 + 19 = 96 \), and \( 96 \div 7 \) leaves a remainder of 5.
Step 3: Day on 31 December 1677
Total odd days = 5, so 31 December 1677 was a Friday (0 = Sunday, 1 = Monday, …, 5 = Friday).
Step 4: Answer
1 January 1678 comes one day later, so it was a Saturday.""", trick=r"Odd days till the end of 1677 = 5 (Friday), so 1 Jan 1678 = Saturday.")
S[6] = dict(raw=r"""Step 1: Study the first pair
In the first figure a small square sits inside the outer frame. In the second figure a new shape with ONE MORE side (a five-sided, house-shaped pentagon) appears, and the old square sits inside it.
Step 2: Write the rule
The inner shape is enclosed by a new shape that has one side more than it; the outer frame stays the same.
Step 3: Apply the rule to the third figure
The third figure has a triangle (3 sides) inside the frame. So the answer must show a shape with 4 sides — a square — with a small triangle inside it, all within the frame.
Step 4: Check the options
A pentagon around a triangle adds two sides; a triangle around a square or a triangle around a triangle does not add a side. Only the frame with a square enclosing a small triangle fits.""", trick=r"Number of sides +1, and the old shape goes inside the new one.")
S[7] = dict(raw=r"""Step 1: Track the letters in the first pair
First figure: A at the top, H on the left, C on the right, Y at the bottom. Second figure: C at the top, A on the left, Y on the right, H at the bottom.
Step 2: Find the movement
A moves top → left, H moves left → bottom, Y moves bottom → right and C moves right → top: every letter turns 90° anticlockwise.
Step 3: Track the small marks
Two small hollow circles become two hollow circles followed by two filled ones. So in the third figure the two hollow squares become two hollow squares followed by two filled squares.
Step 4: Apply both rules to the third figure
Y (top) → left, E (left) → bottom, Z (bottom) → right, X (right) → top. The answer has X at the top, Y on the left, Z on the right, E at the bottom, and two hollow then two filled squares — only one option matches.""", trick=r"Letters turn 90° anticlockwise; add two filled marks after the hollow ones.")
S[8] = dict(raw=r"""Step 1: Study MS444 → PJ398
Reverse the letters: MS → SM. Then move each back by 3: S (19) − 3 = P (16), M (13) − 3 = J (10), giving PJ. Number: \( 444 - 46 = 398 \).
Step 2: Confirm with TT250 → QQ204
TT reversed is TT; T (20) − 3 = Q (17) for both letters, giving QQ ✓. Number: \( 250 - 46 = 204 \) ✓.
Step 3: Apply to JP354
Reverse: JP → PJ. P (16) − 3 = M (13), J (10) − 3 = G (7), giving MG. Number: \( 354 - 46 = 308 \).
Step 4: Answer
The required cluster is MG308.""", trick=r"Reverse the letters, move each back 3; subtract 46 from the number.")
S[9] = dict(raw=r"""Step 1: Study ACK320 → FFB420
Reverse the letters: ACK → KCA. Then K (11) − 5 = F (6), C (3) + 3 = F (6), A (1) + 1 = B (2), giving FFB. Number: \( 320 + 100 = 420 \).
Step 2: Confirm with PSJ180 → EVQ280
Reverse: PSJ → JSP. J (10) − 5 = E (5), S (19) + 3 = V (22), P (16) + 1 = Q (17), giving EVQ ✓. Number: \( 180 + 100 = 280 \) ✓.
Step 3: Apply to DLM140
Reverse: DLM → MLD. M (13) − 5 = H (8), L (12) + 3 = O (15), D (4) + 1 = E (5), giving HOE. Number: \( 140 + 100 = 240 \).
Step 4: Answer
The required cluster is HOE240.""", trick=r"Reverse the letters, then −5, +3, +1; add 100 to the number.")
S[10] = dict(raw=r"""Step 1: Study 4146 and 4188
\( 4188 - 4146 = 42 \), so the second number = first number + 42.
Step 2: Confirm with 2034 and 2076
\( 2034 + 42 = 2076 \) ✓.
Step 3: Apply to the first pair
The missing number + 42 = 5011, so the missing number \( = 5011 - 42 = 4969 \).
Step 4: Answer
The missing number is 4969.""", trick=r"Second number = first number + 42.")
S[11] = dict(raw=r"""Step 1: Study 2655 and 887
\( 887 \times 3 = 2661 \) and \( 2661 - 6 = 2655 \). So the first number = (second number × 3) − 6.
Step 2: Confirm with 2694 and 900
\( 900 \times 3 - 6 = 2700 - 6 = 2694 \) ✓.
Step 3: Apply to the pair with 461
\( 461 \times 3 - 6 = 1383 - 6 = 1377 \).
Step 4: Answer
The missing number is 1377.""", trick=r"First number = 3 × second number − 6.")
S[12] = dict(raw=r"""Step 1: Use reverse positions (A = 26, B = 25, …, Z = 1)
SHARE: S = 8, H = 19, A = 26, R = 9, E = 22. Sum \( = 8 + 19 + 26 + 9 + 22 = 84 \), and \( 84 + 1 = 85 \) ✓.
Step 2: Confirm with PAID
P = 11, A = 26, I = 18, D = 23. Sum \( = 78 \), and \( 78 + 1 = 79 \) ✓.
Step 3: Apply to GEAR
G = 20, E = 22, A = 26, R = 9. Sum \( = 20 + 22 + 26 + 9 = 77 \).
Step 4: Answer
Code \( = 77 + 1 = 78 \).""", trick=r"Code = sum of reverse letter positions + 1.")
S[13] = dict(raw=r"""Step 1: First letters
R (18) → N (14) → J (10) → F (6): each step is −4, so the next first letter is F − 4 = B (2).
Step 2: Second letters
B (2) → X (−2 → 24) → T (20) → P (16): each step is −4, so the next second letter is P − 4 = L (12).
Step 3: Numbers
2000 → 1760 → 1520 → 1280: each step is −240, so the next number is \( 1280 - 240 = 1040 \).
Step 4: Answer
The missing term is BL1040.""", trick=r"Both letters −4; number −240.")
S[14] = dict(raw=r"""Step 1: First letters
M (13) → K (11) → ? → G (7) → E (5): each step is −2, so the missing first letter is I (9).
Step 2: Second and third letters
Second letters A → C → ? → G → I move +2, so the missing one is E. Third letters L → N → ? → R → T move +2, so the missing one is P.
Step 3: Numbers
500 → 602 → ? → 806 → 908: each step is +102, so the missing number is \( 602 + 102 = 704 \).
Step 4: Answer
The missing term is IEP704.""", trick=r"First letter −2, the other two +2; number +102.")
S[15] = dict(raw=r"""Step 1: Use the clock formula
Angle \( = |30H - 5.5M| \), where H = hours and M = minutes. Here H = 3.
Step 2: Set the angle to 120°
At 3:00 the minute hand is 90° behind the hour hand, so it must overtake it and get 120° ahead: \( 5.5M - 90 = 120 \).
Step 3: Solve for M
\( 5.5M = 210 \Rightarrow M = \dfrac{210}{5.5} = 38\dfrac{2}{11} \approx 38.18 \) minutes.
Step 4: Answer
The angle is 120° at about 3:38 AM.""", trick=r"\( 5.5M = 120 + 90 \Rightarrow M \approx 38 \).")
S[16] = dict(raw=r"""Step 1: Use the clock formula
Angle \( = |30H - 5.5M| \). Opposite hands means the angle is 180°. Here H = 2.
Step 2: Set up the equation
At 2:00 the minute hand is 60° behind, so it must get 180° ahead: \( 5.5M - 60 = 180 \).
Step 3: Solve for M
\( 5.5M = 240 \Rightarrow M = \dfrac{240}{5.5} = 43\dfrac{7}{11} \approx 43.6 \) minutes.
Step 4: Answer
The hands are opposite at about 2:44 AM.""", trick=r"\( 5.5M = 180 + 60 \Rightarrow M \approx 43.6 \), i.e. 2:44.")
S[17] = dict(raw=r"""Step 1: Name the eight spoke ends
Call them by direction: top, top-right, right, bottom-right, bottom, bottom-left, left and top-left.
Step 2: Follow the filled circle
Top-right → top → top-left → left: it moves one spoke (45°) anticlockwise each time. Next it goes to the bottom-left spoke.
Step 3: Follow the hollow circle
Top-left → left → bottom-left → bottom: it also moves one spoke anticlockwise each time. Next it goes to the bottom-right spoke.
Step 4: Answer
The next figure has the filled circle on the bottom-left spoke and the hollow circle on the bottom-right spoke — only one option shows this.""", trick=r"Both circles step 45° anticlockwise each time.")
S[18] = dict(raw=r"""Step 1: Look at the first figure
It is a closed plus (cross) shape — all four arms have closed ends.
Step 2: Follow the change
In the second figure the top arm opens (its two lines run straight out); in the third the right arm also opens; in the fourth the bottom arm opens too, and only the left arm is still closed.
Step 3: Find the rule
One more arm opens at each step, going clockwise: top → right → bottom → left.
Step 4: Answer
Next, the left arm also opens, so all four arms are open lines, making a plain # (two vertical and two horizontal lines) — only one option shows this.""", trick=r"Arms open one by one clockwise; the fifth figure is a #.")
S[19] = dict(raw=r"""Step 1: Check the direction of the main line
Vertical → slanting from top-left to bottom-right → horizontal → slanting from bottom-left to top-right.
Step 2: Find the rule
The whole figure turns 45° anticlockwise at every step, keeping all its marks.
Step 3: Find the fifth figure
After four turns of 45° (180° in all) the figure is the first figure turned upside down: the big arrow now points up at the top, the T-mark is on the left and the small arrow is at the bottom right, pointing right.
Step 4: Answer
Only one option shows the first figure rotated by 180°; the other vertical option is its mirror image.""", trick=r"45° anticlockwise each step; 4 steps = 180°, so turn the first figure upside down.")
S[20] = dict(raw=r"""Step 1: Write the present ages
Let S = 5x and T = 3x.
Step 2: Use the ratio after 2 years
\( \dfrac{5x + 2}{3x + 2} = \dfrac{7}{5} \Rightarrow 25x + 10 = 21x + 14 \).
Step 3: Solve
\( 4x = 4 \Rightarrow x = 1 \), so S = 5 years and T = 3 years. Check: after 2 years the ages are 7 and 5 ✓.
Step 4: Answer
S after 3 years \( = 5 + 3 = 8 \) years.""", trick=r"Cross-multiply: \( 5(5x + 2) = 7(3x + 2) \Rightarrow x = 1 \).")
