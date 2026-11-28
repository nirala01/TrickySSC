S = {}
S[1] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: C, ?, K, O, S, W, A, E. Second letters: F, ?, X, T, P, L, H, D.
Step 2: Rule for the first letters
K (11) → O (15) → S (19) → W (23) → A (23 + 4 − 26 = 1) → E (5) is +4 each time. Going back from K, the missing first letter is K − 4 = G (7), and C (3) + 4 = G ✓.
Step 3: Rule for the second letters
X (24) → T (20) → P (16) → L (12) → H (8) → D (4) is −4 each time. Going back from X, the missing letter is 24 + 4 = 28, and 28 − 26 = 2 = B; also F (6) − 4 = B ✓.
Step 4: Answer
The missing term is GB. DA and JB have the wrong first letter, and GD has the wrong second letter.""", trick=r"First letters +4, second letters −4 → C + 4 = G and F − 4 = B.")
S[2] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: V, A, F, K, P, U, ?, E. Second letters: Q, L, G, B, W, R, ?, H.
Step 2: Rule for the first letters
V (22) → A (22 + 5 − 26 = 1) → F (6) → K (11) → P (16) → U (21) is +5 each time. So the missing first letter is U + 5 = Z (26), and Z + 5 = 31 − 26 = 5 = E ✓.
Step 3: Rule for the second letters
Q (17) → L (12) → G (7) → B (2) → W (2 − 5 + 26 = 23) → R (18) is −5 each time. So the missing second letter is R − 5 = M (13), and M − 5 = H (8) ✓.
Step 4: Answer
The missing term is ZM. ZJ has the wrong second letter, and AL and BM have the wrong first letter.""", trick=r"First letters +5, second letters −5 → U + 5 = Z and R − 5 = M.")
S[3] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: N, Q, V, Y, D, G, ?, O. Second letters: X, W, U, R, N, I, ?, V.
Step 2: Rule for the first letters
N (14) → Q (17) is +3, Q → V (22) is +5, V → Y (25) is +3, Y → D (25 + 5 − 26 = 4) is +5, D → G (7) is +3. The jumps alternate +3, +5, so the next jump is +5: G + 5 = L (12), and L + 3 = O (15) ✓.
Step 3: Rule for the second letters
X (24) → W (23) is −1, W → U (21) is −2, U → R (18) is −3, R → N (14) is −4, N → I (9) is −5. The next jump is −6: I − 6 = C (3).
Step 4: Check with the last term
C − 7 = 3 − 7 + 26 = 22 = V ✓. So the missing term is LC; MB, JC and LF each break one of the two rules.""", trick=r"First letters +3, +5 alternately; second letters −1, −2, −3 … → G + 5 = L, I − 6 = C.")
S[4] = dict(raw=r"""Step 1: Study the first set
In (QX, SZ, VC), first letters: Q (17) → S (19) is +2 and S → V (22) is +3. Second letters: X (24) → Z (26) is +2 and Z → C (26 + 3 − 26 = 3) is +3.
Step 2: Confirm with the second set
In (SZ, UB, XE): S → U is +2 and U → X is +3; Z → B is +2 and B → E is +3 ✓. So both letters move +2 and then +3.
Step 3: Test the alternatives
(KH, MJ, PM): K → M is +2 and M → P is +3; H → J is +2 and J → M is +3 ✓.
Step 4: Reject the others
(GL, JO, JR): G → J is +3 and then J stays J. (VU, YX, VA): V → Y is +3 and then Y → V goes backwards. (SM, PP, RS): S → P is −3. None of them follows the +2, +3 rule.""", trick=r"Both letters go +2, then +3 → only (KH, MJ, PM) fits.")
S[5] = dict(raw=r"""Step 1: Find the day on 1 January 1915
1 January 1900 was a Monday. From 1900 to 1915 there are 15 years with 3 leap years (1904, 1908, 1912), so the odd days are 15 + 3 = 18, and 18 leaves remainder 4 when divided by 7. Monday + 4 = Friday.
Step 2: Find the day on 1 August 1915
Days from 1 January to 31 July = 31 + 28 + 31 + 30 + 31 + 30 + 31 = 212, and 212 leaves remainder 2. Friday + 2 = Sunday. So 1 August was a Sunday and 3 August was a Tuesday.
Step 3: Count the Tuesdays of August
August has 31 days, so its Tuesdays fall on 3, 10, 17, 24 and 31: five Tuesdays ✓.
Step 4: Check December
Days from 1 January to 30 November = 334, and 334 leaves remainder 5. Friday + 5 = Wednesday, so 1 December was a Wednesday and the Tuesdays fall on 7, 14, 21 and 28: only four. Hence only August (I) had five Tuesdays.""", trick=r"A 31-day month has five of only its first three weekdays: August 1915 began on Sunday (Sun, Mon, Tue), December on Wednesday (Wed, Thu, Fri).")
S[6] = dict(raw=r"""Step 1: Read the first pair
The first figure is a solid black pentagon (5 sides). The second figure is an empty, unshaded square (4 sides) inside a frame.
Step 2: Find the rule
Two things change together: the number of sides falls by one (5 → 4), and the black shape becomes white (unshaded).
Step 3: Apply the rule to the third figure
The third figure is a solid black heptagon (7 sides). One side fewer gives a hexagon (6 sides), and it must be white.
Step 4: Pick the matching figure
The correct figure is the white hexagon. The white heptagon keeps 7 sides, the white pentagon drops two sides, and the black hexagon has the right number of sides but keeps the shading.""", trick=r"Sides − 1 and black → white: black 7-sided → white 6-sided.")
S[7] = dict(raw=r"""Step 1: Note the layout of each box
Every box has four letters at the corners and four elements at the middle of the sides (shapes or letters).
Step 2: Find the rule from the first pair
Corners: A moves from top-left to top-right, B from top-right to bottom-right, C from bottom-right to bottom-left and D from bottom-left to top-left. Sides: the triangle moves from the top to the right, the square from the right to the bottom, the circle from the bottom to the left and the pentagon from the left to the top. So every element moves one place clockwise: corner to the next corner, side to the next side.
Step 3: Apply the rule to the third box
Corners E (top-left), H (top-right), I (bottom-right), G (bottom-left) become G (top-left), E (top-right), H (bottom-right), I (bottom-left). Sides: the rectangle (top) goes to the right, F (right) goes to the bottom, R (bottom) goes to the left and J (left) goes to the top.
Step 4: Pick the matching figure
The answer box reads G J E in the top row, R and the rectangle in the middle row, and I F H in the bottom row. The other figures swap F with H in the bottom row, put F on the left side in place of R, or place F at the top-right corner.""", trick=r"Everything shifts one place clockwise → top row G J E, middle R ▬, bottom I F H.")
S[8] = dict(raw=r"""Step 1: Compare the first pair
QF100 → RH220: Q (17) → R (18) is +1, F (6) → H (8) is +2, and 100 → 220 is +120.
Step 2: Confirm with the third pair
MK270 → NM390: M → N is +1, K (11) → M (13) is +2, and 270 + 120 = 390 ✓.
Step 3: Apply the rule to LX150
L (12) + 1 = M, X (24) + 2 = Z (26), and 150 + 120 = 270.
Step 4: Answer
The cluster is MZ270. ZM260 and NZ260 have the wrong number (260) and wrong letters, and MN270 has N in place of Z.""", trick=r"First letter +1, second letter +2, number +120 → MZ270.")
S[9] = dict(raw=r"""Step 1: Compare the first pair
DKM140 → HNE240. The number rises by 100. Taking the letters in reverse order (M, K, D): M (13) → H (8) is −5, K (11) → N (14) is +3 and D (4) → E (5) is +1.
Step 2: Confirm with the third pair
LTJ320 → EWM420: reverse order is J, T, L. J (10) − 5 = E, T (20) + 3 = W, L (12) + 1 = M, and 320 + 100 = 420 ✓.
Step 3: Apply the rule to TPF160
Reverse order is F, P, T. F (6) − 5 = A, P (16) + 3 = S, T (20) + 1 = U, and 160 + 100 = 260.
Step 4: Answer
The cluster is ASU260. AUS160 and VSB160 keep the number 160, and ASV260 ends in V in place of U.""", trick=r"Reverse the letters, then −5, +3, +1; number +100 → ASU260.")
S[10] = dict(raw=r"""Step 1: Compare the second pair
8345 → 8385: 8385 − 8345 = 40, so 40 is added.
Step 2: Confirm with the third pair
9297 + 40 = 9337 ✓.
Step 3: Apply the rule to 2349
2349 + 40 = 2389.
Step 4: Check
2389 − 2349 = 40, the same gap as in the other two pairs, so the missing number is 2389.""", trick=r"Each pair differs by 40 → 2349 + 40 = 2389.")
S[11] = dict(raw=r"""Step 1: Compare the first pair
159 × 3 = 477, and 477 + 6 = 483. So the rule is: multiply by 3 and add 6.
Step 2: Confirm with the third pair
914 × 3 = 2742, and 2742 + 6 = 2748 ✓.
Step 3: Apply the rule to 726
726 × 3 = 2178, and 2178 + 6 = 2184.
Step 4: Check
2184 − 6 = 2178 and 2178 ÷ 3 = 726 ✓. Note that 2178 (only × 3, without the + 6) is given as a trap.""", trick=r"× 3, then + 6 → 726 × 3 + 6 = 2184.")
S[12] = dict(raw=r"""Step 1: Find the code for “off”
“off” appears in the first, third and fourth sentences. The only code common to “el ua pk lo”, “ua ts el fa” and “el ha lo fa” is “el”. So off = el.
Step 2: Find the code for “sun”
“sun” appears in the second and third sentences. The codes common to “ja ha ts fa” and “ua ts el fa” are “ts” and “fa”.
Step 3: Separate “sun” from “come”
“come” appears in the second, third and fourth sentences, and the only code common to all three is “fa”. So come = fa, which leaves sun = ts.
Step 4: Write the answer and check
“off sun” = “el ts”. Check with the third sentence: off = el, sun = ts, should = ua, come = fa gives “ua ts el fa” ✓.""", trick=r"off is common to sentences 1, 3, 4 → el; sun is common to 2, 3 (minus come = fa) → ts.")
S[13] = dict(raw=r"""Step 1: Study the first letters
Z (26) → B (2) → D (4) → F (6) → H (8) is +2 each time, so the sixth term should begin with H + 2 = J.
Step 2: Study the second letters
D (4) → J (10) → P (16) → V (22) → B (22 + 6 − 26 = 2) is +6 each time, so the sixth term should have B + 6 = H.
Step 3: Study the numbers
144 → 160 → 176 → 192 → 208 is +16 each time, so the sixth number should be 208 + 16 = 224.
Step 4: Find the wrong term
The sixth term should be JH224, but the series gives KI240 (letters one step too far and the number 16 too large). The first five terms follow all three rules, so KI240 is the wrong term.""", trick=r"Letters +2 and +6, number +16 → last term should be JH224, not KI240.")
S[14] = dict(raw=r"""Step 1: Study the numbers and the first letters
Numbers: 200, 400, 800, 1600, 3200, 6400 double every time ✓. First letters: N (14) → Q (17) → T (20) → W (23) → Z (26) → C (26 + 3 − 26 = 3) are +3 every time ✓.
Step 2: Study the second letters
M (13), K (11), G (7), D (4), A (1), X (24). From G onwards the rule is −3: G → D → A → X (1 − 3 + 26 = 24). Going back, G + 3 = J and J + 3 = M ✓, so the second term should have J, not K.
Step 3: Study the third letters
T (20), Y (25), B (2), F (6), J (10), N (14). From B onwards the rule is +4: B → F → J → N. Going back, B − 4 = 2 − 4 + 26 = 24 = X and X − 4 = T ✓, so the second term should have X, not Y.
Step 4: Find the wrong term
The second term should be QJX400, but the series gives QKY400. Every other term fits all the rules, so QKY400 is the wrong term.""", trick=r"Letters +3, −3, +4 and number × 2 → second term should be QJX400.")
S[15] = dict(raw=r"""Step 1: Position of the minute hand
The minute hand moves 6° per minute. At 50 minutes it is at 50 × 6 = 300° from the 12 mark.
Step 2: Position of the hour hand
The hour hand moves 30° per hour and 0.5° per minute. At 4:50 it is at 4 × 30 + 50 × 0.5 = 120 + 25 = 145°.
Step 3: Find the angle
Angle between the hands = 300 − 145 = 155°.
Step 4: Check with the formula
Angle = |30H − 5.5M| = |30 × 4 − 5.5 × 50| = |120 − 275| = 155°. It is less than 180°, so it is the required angle.""", trick=r"|30H − 5.5M| = |120 − 275| = 155°.")
S[16] = dict(raw=r"""Step 1: Position of the minute hand
The minute hand moves 6° per minute. At 10 minutes it is at 10 × 6 = 60° from the 12 mark.
Step 2: Position of the hour hand
The hour hand moves 30° per hour and 0.5° per minute. At 9:10 it is at 9 × 30 + 10 × 0.5 = 270 + 5 = 275°.
Step 3: Find the gap between the hands
Gap = 275 − 60 = 215°. This is more than 180°, so it is the reflex angle.
Step 4: Take the smaller angle
Angle between the hands = 360 − 215 = 145°. The formula |30H − 5.5M| = |270 − 55| = 215° gives the same reflex value, so the answer is 145°.""", trick=r"|30H − 5.5M| = 215°; more than 180°, so 360 − 215 = 145°.")
S[17] = dict(raw=r"""Step 1: Note the parts of each figure
Every box has four arrows along one side and some straight lines along the opposite side.
Step 2: Track the arrows
The arrows are on the left pointing right, then on the top pointing down, then on the right pointing left, then at the bottom pointing up. The figure turns a quarter turn (90°) clockwise each step, so in the fifth figure the arrows are back on the left, pointing right.
Step 3: Track the lines
The lines are: one short line, then one full line, then one full and one short line, then two full lines. So half a line is added at every step: ½, 1, 1½, 2, and next comes 2½.
Step 4: Pick the matching figure
The fifth figure has the arrows on the left and, on the right, two full lines with one short line. The figure with three full lines has 3, the one with four full lines has 4, and the one with three full lines and a short line has 3½.""", trick=r"Quarter turn clockwise each step; lines grow ½, 1, 1½, 2 → 2½ (two full + one short).")
S[18] = dict(raw=r"""Step 1: Note the parts of each figure
Every box has a vertical line with five small curved hooks: three on the left (top, middle, bottom) and two on the right (upper, lower). Each hook either bends down (like an arch) or bends up (like a cup).
Step 2: Compare neighbouring figures
First to second: only the bottom-left hook flips (arch to cup). Second to third: only the lower-right hook flips (cup to arch). Third to fourth: only the middle-left hook flips (cup to arch).
Step 3: Find the rule
Exactly one hook flips per step, and the flipping hook climbs the line in a zig-zag: bottom-left, lower-right, middle-left. The next one in this order is the upper-right hook.
Step 4: Build the fifth figure
Take the fourth figure and flip only its upper-right hook from an arch to a cup. The result has, on the left, arch, arch, cup (top to bottom) and, on the right, a cup above an arch. The other figures also change the top-left hook, or flip both right hooks, so they do not fit.""", trick=r"One hook flips per step, zig-zagging upward: bottom-left, lower-right, middle-left → upper-right next.")
S[19] = dict(raw=r"""Step 1: Note the parts of each figure
Every box has a row of down arrows at the top and one small triangle in a bottom corner.
Step 2: Track the arrows
The arrows number 5, 4, 3 and 2: one arrow is removed from the right end at each step. So the fifth figure has just 1 arrow, at the top-left.
Step 3: Track the triangle
The triangle is black at the bottom-right, white at the bottom-left, black at the bottom-right, white at the bottom-left. It alternates, so the fifth figure has a black triangle at the bottom-right.
Step 4: Pick the matching figure
All four alternatives have one arrow, so the triangle decides: the correct figure has a black triangle at the bottom-right. A white triangle (in either corner) has the wrong shade, and a black triangle at the bottom-left has the wrong corner.""", trick=r"Arrows 5, 4, 3, 2 → 1; triangle alternates black-right, white-left → black at the bottom-right.")
S[20] = dict(raw=r"""Step 1: Write the present ages
The ages are in the ratio \( 9 : 10 \), so let them be 9x and 10x years.
Step 2: Use the sum
9x + 10x = 95, so 19x = 95 and x = 5.
Step 3: Find the present ages
The ages are 9 × 5 = 45 years and 10 × 5 = 50 years (45 + 50 = 95 ✓).
Step 4: Find the ratio after 8 years
After 8 years the ages are 45 + 8 = 53 and 50 + 8 = 58, so the ratio is \( 53 : 58 \). It cannot be reduced, because 53 is a prime number.""", trick=r"19 parts = 95 → 45 and 50; add 8 to each → \( 53 : 58 \).")
