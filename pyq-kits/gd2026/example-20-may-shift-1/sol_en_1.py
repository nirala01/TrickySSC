S = {}
S[1] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: Z, C, F, ?, L, O, R, U. Second letters: H, E, B, ?, V, S, P, M.
Step 2: Rule for the first letters
Z (26) → C (29 − 26 = 3) → F (6) is +3 each time, and L (12) → O (15) → R (18) → U (21) is also +3. So the missing first letter is F + 3 = I (9), and I + 3 = L ✓.
Step 3: Rule for the second letters
H (8) → E (5) → B (2) is −3 each time, and V (22) → S (19) → P (16) → M (13) is also −3. So the missing second letter is B − 3 = 2 − 3 + 26 = Y (25), and Y − 3 = V ✓.
Step 4: Answer
The missing term is IY. GY and HA have the wrong first letter, and IV has the wrong second letter.""", trick=r"First letters +3, second letters −3 → I and Y.")
S[2] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: M, O, S, U, Y, ?, E, G. Second letters: O, I, C, W, Q, ?, E, Y.
Step 2: Rule for the first letters
M (13) → O (15) is +2, O → S (19) is +4, S → U (21) is +2, U → Y (25) is +4. The jumps alternate +2, +4, so the next is Y + 2 = 27 − 26 = A (1). Check: A + 4 = E ✓, E + 2 = G ✓.
Step 3: Rule for the second letters
O (15) → I (9) → C (3) → W (3 − 6 + 26 = 23) → Q (17): each step is −6. So the missing second letter is Q − 6 = K (11), and K − 6 = E ✓, E − 6 + 26 = Y ✓.
Step 4: Answer
The missing term is AK. AL breaks the −6 rule, while DI and ZK break the first-letter rule.""", trick=r"First letters +2, +4 alternately; second letters −6 → AK.")
S[3] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: V, ?, F, J, P, T, Z, D. Second letters: Y, ?, T, P, K, E, X, P.
Step 2: Rule for the first letters
F (6) → J (10) is +4, J → P (16) is +6, P → T (20) is +4, T → Z (26) is +6, Z → D (30 − 26 = 4) is +4. The jumps alternate +4, +6. Working backwards, the jump into F is +6 and the jump from V is +4: V (22) + 4 = Z (26), and Z + 6 = 32 − 26 = F ✓.
Step 3: Rule for the second letters
T (20) → P (16) is −4, P → K (11) is −5, K → E (5) is −6, E → X (24) is −7, X → P (16) is −8. The gaps grow by one, so the first two gaps are −2 and −3: Y (25) − 2 = W (23), and W − 3 = T ✓.
Step 4: Answer
The missing term is ZW. AW and YU have the wrong first letter, and ZT has the wrong second letter.""", trick=r"First letters +4, +6 alternately; second letters −2, −3, −4 … → ZW.")
S[4] = dict(raw=r"""Step 1: Study the first set (IS, DM, YG)
First letters: I (9) → D (4) → Y (4 − 5 + 26 = 25), a fall of 5 each time. Second letters: S (19) → M (13) → G (7), a fall of 6 each time.
Step 2: Confirm with the second set (PD, KX, FR)
First letters: P (16) → K (11) → F (6), again −5. Second letters: D (4) → X (4 − 6 + 26 = 24) → R (18), again −6. So the rule is: first letter −5, second letter −6.
Step 3: Test the group that fits
(WM, RG, MA): W (23) → R (18) → M (13) is −5, −5; M (13) → G (7) → A (1) is −6, −6. Both rules hold.
Step 4: Reject the others
(ME, JZ, BT): M → J is only −3. (PK, PF, JZ) and (RJ, RE, KY): the first letter does not change from the first cluster to the second. So only (WM, RG, MA) follows the rule.""", trick=r"First letter −5, second letter −6 in every step → (WM, RG, MA).")
S[5] = dict(raw=r"""Step 1: Find the day on 1 January 1926
1 January 1900 was a Monday. From 1900 to the end of 1925 there are 26 years, of which 6 are leap years (1904, 1908, 1912, 1916, 1920, 1924). Odd days \( = 26 + 6 = 32 \), and \( 32 \div 7 \) leaves remainder 4. Monday + 4 days = Friday.
Step 2: Count the Fridays of January
January has 31 days and starts on a Friday, so its Fridays fall on 1, 8, 15, 22 and 29 — five Fridays.
Step 3: Check February and March
January has \( 31 = 28 + 3 \) days, so 1 February is Friday + 3 = Monday. 1926 is not a leap year, so February has exactly 28 days (4 Fridays) and 1 March is again a Monday; the Fridays of March are 5, 12, 19 and 26 — only four.
Step 4: Check May
March (31 days) pushes the day by 3 and April (30 days) by 2, so 1 May is Monday + 5 = Saturday. The Fridays of May are 7, 14, 21 and 28 — only four. Hence only January had 5 Fridays.""", trick=r"A 31-day month has 5 Fridays only if it starts on Wednesday, Thursday or Friday; January 1926 began on a Friday.")
S[6] = dict(raw=r"""Step 1: Read the first pair
The first figure has one upright bar whose top half is black and bottom half is white. The second figure has two such bars side by side.
Step 2: Find the rule
In the second figure the left bar is an exact copy of the original (black on top), and the right bar is the same bar turned upside down (white on top). So the rule is: keep the bar, and place an inverted copy next to it.
Step 3: Apply the rule to the third figure
The third figure is the same bar lying on its side — black on the left, white on the right. The answer must therefore show two lying bars, one black-left/white-right and the other its reverse, white-left/black-right.
Step 4: Match the options
Only one figure has two half-black bars that are reverses of each other (upper bar white-left/black-right, lower bar black-left/white-right). In each of the other three figures one bar is fully black or fully white, so they do not fit.""", trick=r"One bar becomes two: the bar itself + its reversed copy. Reject any figure with an all-black or all-white bar.")
S[7] = dict(raw=r"""Step 1: Read the first pair
In the first figure the long arrow comes out of the top corner of the diamond (pointing up) and a small arrow sits inside the left corner. In the second figure the long arrow comes out of the bottom corner (pointing down) and the small arrow sits inside the top corner.
Step 2: Find the two moves
The outer arrow jumps to the opposite corner (top → bottom, a half turn). The inner arrow moves to the next corner clockwise (left → top, a quarter turn).
Step 3: Apply the moves to the third figure
In the third figure the outer arrow is at the left corner and the inner arrow is inside the right corner. Outer arrow: left → right. Inner arrow: right → bottom (next corner clockwise).
Step 4: Match the options
The answer is the diamond with the long arrow coming out of the right corner and the small arrow inside the bottom corner. The other figures either keep the long arrow on the left or put the small arrow at the top.""", trick=r"Outer arrow → opposite corner; inner arrow → next corner clockwise.")
S[8] = dict(raw=r"""Step 1: Study the pair MO44 → PR91
M (13) + 3 = P (16), O (15) + 3 = R (18), and \( 44 + 47 = 91 \).
Step 2: Confirm with UZ28 → XC75
U (21) + 3 = X (24), Z (26) + 3 = 29 − 26 = C (3), and \( 28 + 47 = 75 \). So the rule is: each letter +3 and the number +47.
Step 3: Work backwards from FI68
The missing cluster must become FI68, so subtract: F (6) − 3 = C (3), I (9) − 3 = F (6), and \( 68 - 47 = 21 \).
Step 4: Answer
The missing cluster is CF21. Check: C + 3 = F, F + 3 = I, \( 21 + 47 = 68 \) ✓. FC21 has the letters in the wrong order, and CD22 and FD23 fail the number rule.""", trick=r"Letters +3, number +47; going back from FI68 gives CF21.")
S[9] = dict(raw=r"""Step 1: Study the pair TUE150 → LZW370
Add 3, 5 and 7 to the three letters: T (20) + 3 = W, U (21) + 5 = Z, E (5) + 7 = L. This gives WZL; written in reverse order it is LZW. The number: \( 150 + 220 = 370 \).
Step 2: Confirm with RAC340 → JFU560
R (18) + 3 = U, A (1) + 5 = F, C (3) + 7 = J gives UFJ, reversed JFU ✓. The number: \( 340 + 220 = 560 \) ✓.
Step 3: Apply the rule to KJR230
K (11) + 3 = N, J (10) + 5 = O, R (18) + 7 = Y gives NOY; reversed it is YON. The number: \( 230 + 220 = 450 \).
Step 4: Answer
The required cluster is YON450. NOY460 is not reversed and has the wrong number, YOM450 has M instead of N, and OYN420 fails on both counts.""", trick=r"Letters +3, +5, +7, then reverse the order; number +220 → YON450.")
S[10] = dict(raw=r"""Step 1: Study the first pair
\( 1435 - 1382 = 53 \), so the second number is the first number plus 53.
Step 2: Confirm with the third pair
\( 1407 - 1354 = 53 \) ✓. The rule is the same: first number + 53 = second number.
Step 3: Apply the rule to the middle pair
The missing number plus 53 must give 4398, so the missing number \( = 4398 - 53 = 4345 \).
Step 4: Check
\( 4345 + 53 = 4398 \) ✓. With 4341, 4343 or 4349 the difference would be 57, 55 or 49, not 53.""", trick=r"Every pair differs by 53 → \( 4398 - 53 = 4345 \).")
S[11] = dict(raw=r"""Step 1: Study the first pair
\( 658 \times 4 = 2632 \) and \( 2632 + 9 = 2641 \). So the second number is 4 times the first number plus 9.
Step 2: Confirm with the third pair
\( 859 \times 4 = 3436 \) and \( 3436 + 9 = 3445 \) ✓.
Step 3: Apply the rule to 644
\( 644 \times 4 = 2576 \) and \( 2576 + 9 = 2585 \).
Step 4: Answer
The missing number is 2585. The numbers 2584, 2590 and 2592 are \( 4 \times 644 \) plus 8, 14 and 16, so they do not follow the +9 rule.""", trick=r"Second number \( = 4 \times \) first number \( + 9 \) → \( 2576 + 9 = 2585 \).")
S[12] = dict(raw=r"""Step 1: Find the code for “be”
“be” occurs in the first sentence (ta ra sa) and the third sentence (ma la ta ka). The only common code is “ta”, so be = ta.
Step 2: Find the code for “time”
“time” occurs in the second sentence (pa ma ba sa na) and the third sentence (ma la ta ka). The only common code is “ma”, so time = ma.
Step 3: Cross-check with “careful”
“careful” is common to the first and second sentences, and the common code there is “sa”. So careful = sa, which does not disturb the two codes found above.
Step 4: Write the code for “time be”
time = ma and be = ta, so “time be” is coded with the two words ma and ta (in any order) — “ta ma”.""", trick=r"Match the common word with the common code: be = ta, time = ma.")
S[13] = dict(raw=r"""Step 1: Check the first letters
K (11) → D (4) → W (4 − 7 + 26 = 23) → P (16) → I (9) → B (2): each step is −7. No error here.
Step 2: Check the second letters
T, U, V, W, X, Y — consecutive letters (+1 each). No error here.
Step 3: Check the numbers
\( 308 - 254 = 54 \) and \( 362 - 308 = 54 \), so the numbers rise by 54. The next should be \( 362 + 54 = 416 \), but the series shows 420. After that \( 416 + 54 = 470 \) ✓ and \( 470 + 54 = 524 \) ✓.
Step 4: Answer
The wrong term is PW420; it should be PW416. KT254, WV362 and IX470 all fit the rules.""", trick=r"Numbers go up by 54: 254, 308, 362, 416, 470, 524 → 420 is wrong.")
S[14] = dict(raw=r"""Step 1: First letters
A, B, C, D — consecutive letters (+1), so the next first letter is E.
Step 2: Second letters
M, L, K, J — one step back each time (−1), so the next second letter is I.
Step 3: Third letters
Z, A, B, C — one step forward each time (Z + 1 wraps round to A), so the next third letter is D.
Step 4: Numbers
\( 2200 - 2027 = 173 \), \( 2027 - 1854 = 173 \), \( 1854 - 1681 = 173 \). The next number is \( 1681 - 173 = 1508 \). So the missing term is EID1508; the other choices have the wrong letter order and a wrong number.""", trick=r"Letters +1, −1, +1 and the number −173 → EID1508.")
S[15] = dict(raw=r"""Step 1: Write the formula
At H hours M minutes the angle between the hands is the difference between \( 30H \) and \( \dfrac{11}{2}M \) degrees.
Step 2: Put H = 5
\( 30 \times 5 = 150 \), so the angle is the difference between 150 and \( \dfrac{11}{2}M \). At exactly 5 o'clock the angle is \( 150^\circ \), and it shrinks as the minute hand moves ahead.
Step 3: Solve for 135 degrees
\( 150 - \dfrac{11}{2}M = 135 \Rightarrow \dfrac{11}{2}M = 15 \Rightarrow M = \dfrac{30}{11} \approx 2.73 \) minutes, i.e. about 3 minutes past 5.
Step 4: Check the other possibility and the options
The second time is when \( \dfrac{11}{2}M - 150 = 135 \), i.e. \( M = \dfrac{570}{11} \approx 51.8 \) minutes (about 5:52), which is not among the choices. At 5:00 the angle is \( 150^\circ \), and by 5:07 it is already about \( 111.5^\circ \). So the answer is about 5:03.""", trick=r"The gap closes at \( 5.5^\circ \) per minute: \( (150 - 135) \div 5.5 \approx 3 \) min → 5:03.")
S[16] = dict(raw=r"""Step 1: Position at 8 o'clock
At 8:00 the hour hand is at the 8 mark, so it is \( 8 \times 30 = 240^\circ \) ahead of the minute hand.
Step 2: Relative speed
The minute hand moves \( 6^\circ \) per minute and the hour hand \( \dfrac{1}{2}^\circ \) per minute, so the minute hand gains \( 6 - \dfrac{1}{2} = \dfrac{11}{2}^\circ \) every minute.
Step 3: Time to catch up
\( M = 240 \div \dfrac{11}{2} = \dfrac{480}{11} = 43\dfrac{7}{11} \) minutes \( \approx 43.6 \) minutes.
Step 4: Answer
The hands overlap at about 43.6 minutes past 8, i.e. about 8:44. At 8:40 the minute hand is still behind the hour hand, and by 8:46 or 8:48 it has already crossed it.""", trick=r"Overlap after H o'clock: \( M = \dfrac{60H}{11} = \dfrac{480}{11} \approx 44 \) min.")
S[17] = dict(raw=r"""Step 1: Understand the figure
Each box has eight small marks round its edge — a circle at each corner and a square at the middle of each side — and every mark has one slanting line in it.
Step 2: Compare one figure with the next
From figure 1 to figure 2 only the top-left circle changes: its slanting line flips to the other direction. From figure 2 to figure 3 only the square in the middle of the left side flips. From figure 3 to figure 4 only the bottom-left circle flips.
Step 3: State the rule
Exactly one mark flips in every step, and the flip travels anticlockwise round the box: top-left → left-middle → bottom-left. The next mark on this path is the square in the middle of the bottom side.
Step 4: Predict and match
The answer must be figure 4 with only the bottom-middle square flipped; the other seven marks stay as they are, so the square on the right side still slants the same way as before. Only one figure shows this. In the other figures the right-middle square has also changed, or the bottom-right circle has flipped instead of (or along with) the bottom-middle square.""", trick=r"One mark flips per step, moving anticlockwise: top-left, left, bottom-left, then bottom-middle.")
S[18] = dict(raw=r"""Step 1: Read the figures
Figure 1: a short line ending in a black dot. Figure 2: the dot has become a hollow circle and a new line rises from it. Figure 3: a black dot is added at the end of that new line. Figure 4: this dot becomes hollow and a new line goes to the right from it.
Step 2: Find the rule
The chain grows in two alternating moves: (i) the black end-dot turns hollow and a new line is added, turning by a right angle; (ii) a black dot is added at the free end of the newest line.
Step 3: Decide the next move
Figure 3 → 4 used move (i), so figure 4 → 5 uses move (ii): nothing else changes, and a black dot appears at the end of the line going right.
Step 4: Match the options
The answer shows the same chain as figure 4 — line, hollow circle, line up, hollow circle, line to the right — ending in a black dot. The other figures add an extra upward line or end in a hollow circle, which would need two moves.""", trick=r"Add a line, then add a black dot, alternately — the fifth figure only gains a black dot.")
S[19] = dict(raw=r"""Step 1: Count the dots
The four figures have 1, 2, 3 and 4 small circles, so the fifth figure must have 5.
Step 2: See which part holds the dots
The dots are in the left part (figure 1), the top part (figure 2), the right part (figure 3) and the bottom part (figure 4). The position moves a quarter turn clockwise each time, so next it returns to the left part.
Step 3: Look at the dividing line
The line that cuts the shape is upright, level, upright, level — so in the fifth figure it is upright again, which agrees with the dots being in the left half.
Step 4: Match the options
All four choices are a diamond cut by an upright line. The answer is the one with exactly five dots in the left half. The others have six dots, or have their dots in the right half.""", trick=r"Dots 1, 2, 3, 4 → 5; side left, top, right, bottom → left.")
S[20] = dict(raw=r"""Step 1: Write the present ages
Let the present ages be \( 10x \) and \( 13x \) years.
Step 2: Use the difference
\( 13x - 10x = 9 \Rightarrow 3x = 9 \Rightarrow x = 3 \). So the present ages are \( 10 \times 3 = 30 \) years and \( 13 \times 3 = 39 \) years.
Step 3: Go back 6 years
The ages were \( 30 - 6 = 24 \) years and \( 39 - 6 = 33 \) years.
Step 4: Simplify the ratio
\( \dfrac{24}{33} = \dfrac{8}{11} \), so the ratio 6 years ago was 8 to 11. Check: the difference \( 33 - 24 = 9 \) years is unchanged ✓.""", trick=r"3 parts = 9 years → ages 30 and 39; six years ago 24 and 33 → 8 to 11.")
