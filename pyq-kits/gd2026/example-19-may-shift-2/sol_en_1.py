S = {}
S[1] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: D, F, H, J, L, N, P, ?. Second letters: X, V, T, R, P, N, L, ?.
Step 2: Rule for the first letters
D (4) → F (6) → H (8) → J (10) → L (12) → N (14) → P (16): each step is +2, so the next first letter is P + 2 = R (18).
Step 3: Rule for the second letters
X (24) → V (22) → T (20) → R (18) → P (16) → N (14) → L (12): each step is −2, so the next second letter is L − 2 = J (10).
Step 4: Answer
The missing term is RJ. SJ and OM break the +2 rule, and RI breaks the −2 rule.""", trick=r"First letters +2, second letters −2 → P + 2 = R, L − 2 = J.")
S[2] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: W, Z, ?, F, I, L, O, R. Second letters: X, U, ?, O, L, I, F, C.
Step 2: Rule for the first letters
W (23) → Z (26) is +3, and F (6) → I (9) → L (12) → O (15) → R (18) is also +3. So the missing first letter is Z + 3 = 29 → 29 − 26 = 3 = C.
Step 3: Rule for the second letters
X (24) → U (21) is −3, and O (15) → L (12) → I (9) → F (6) → C (3) is also −3. So the missing second letter is U − 3 = R (18).
Step 4: Check and answer
C + 3 = F ✓ and R − 3 = O ✓. The missing term is CR.""", trick=r"First letters +3 (Z → C wraps round), second letters −3 → CR.")
S[3] = dict(raw=r"""Step 1: Split each term into first and second letters
First letters: ?, O, T, X, C, G, L, P. Second letters: ?, I, D, X, Q, I, Z, P.
Step 2: Rule for the first letters
O (15) → T (20) → X (24) → C (29 → 3) → G (7) → L (12) → P (16): the gaps alternate +5, +4, +5, +4, +5, +4. So the gap before O is +4, and the missing first letter is O − 4 = K (11).
Step 3: Rule for the second letters
I (9) → D (4) is −5, D → X (4 − 6 = −2 → 24) is −6, X (24) → Q (17) is −7, Q → I (9) is −8, I → Z (9 − 9 = 0 → 26) is −9, Z (26) → P (16) is −10. One step back the gap is −4, so the missing second letter is I + 4 = M (13).
Step 4: Answer
The missing term is KM (K + 4 = O ✓ and M − 4 = I ✓). KO fails because O − 6 = I would break the −4, −5, −6 … pattern.""", trick=r"First letters +4, +5 alternately; second letters −4, −5, −6 … −10 → KM.")
S[4] = dict(raw=r"""Step 1: Study the first set (TN, RG, PZ)
First letters T (20) → R (18) → P (16): −2, −2. Second letters N (14) → G (7) → Z (7 − 7 = 0 → 26): −7, −7.
Step 2: Confirm with the second set (CR, AK, YD)
C (3) → A (1) → Y (1 − 2 = −1 → 25) is −2, −2 and R (18) → K (11) → D (4) is −7, −7 ✓.
Step 3: Test the options
(TO, RH, PA): T → R → P is −2, −2 and O (15) → H (8) → A (1) is −7, −7 ✓.
(WV, TT, RM): W → T is −3 ✗. (MW, MU, CN): M → M is 0 ✗. (AW, YU, VN): Y → V is −3 ✗.
Step 4: Answer
Only (TO, RH, PA) follows the same rule.""", trick=r"First letters −2, −2; second letters −7, −7.")
S[5] = dict(raw=r"""Step 1: Count the days from 11 July to 11 December 2016
11 July → 11 August = 31 days (July has 31), → 11 September = 31 (August), → 11 October = 30 (September), → 11 November = 31 (October), → 11 December = 30 (November).
Step 2: Add them
31 + 31 + 30 + 31 + 30 = 153 days.
Step 3: Find the odd days
153 ÷ 7 = 21 weeks and 6 days, so there are 6 odd days.
Step 4: Move forward from Monday
Monday + 6 days = Sunday. So 11 December 2016 was a Sunday.""", trick=r"153 days = 21 weeks + 6 odd days → Monday + 6 = Sunday.")
S[6] = dict(raw=r"""Step 1: Look at the first pair
The first figure is a pentagon (5 sides) in a square frame; the second figure is a square (4 sides) in a square frame.
Step 2: Find the rule
The shape inside the frame loses one side: 5 sides → 4 sides. The frame stays the same.
Step 3: Apply the rule to the second pair
The third figure is a hexagon (6 sides), so the answer must be a shape with 6 − 1 = 5 sides — a pentagon in a square frame.
Step 4: Check the options
Figure 1 is a circle, Figure 2 a square and Figure 4 a triangle; only Figure 3 shows a pentagon. So Figure 3 completes the analogy.""", trick=r"Sides drop by one: pentagon → square, so hexagon → pentagon.")
S[7] = dict(raw=r"""Step 1: Follow the corner symbols in the first pair
Figure 1: 6 top-left, V top-right, 7 bottom-left, U bottom-right. Figure 2: V top-left, U top-right, 6 bottom-left, 7 bottom-right.
Step 2: Find the rule for the corners
Each corner symbol moves one corner anticlockwise: top-right → top-left, top-left → bottom-left, bottom-left → bottom-right, bottom-right → top-right.
Step 3: Find the rule for the centre
The filled square and the hollow square swap sides (filled | hollow becomes hollow | filled).
Step 4: Apply both rules to the third figure
Figure 3 has W top-left, X top-right, 8 bottom-left, 9 bottom-right and filled | hollow circles. So the answer has X top-left, 9 top-right, W bottom-left, 8 bottom-right and hollow | filled circles — that is Figure 3.""", trick=r"Corners turn one place anticlockwise; the centre pair swaps.")
S[8] = dict(raw=r"""Step 1: Study the first pair (AD182 → GD90)
Letters: second letter D (4) + 3 = G (7) becomes the new first letter; first letter A (1) + 3 = D (4) becomes the new second letter. Number: 182 − 92 = 90.
Step 2: Confirm with the second pair (FK312 → NI220)
Second letter K (11) + 3 = N (14) comes first; first letter F (6) + 3 = I (9) comes second; 312 − 92 = 220 ✓.
Step 3: Apply the rule to ET202
Second letter T (20) + 3 = W (23) comes first; first letter E (5) + 3 = H (8) comes second; 202 − 92 = 110.
Step 4: Answer
The required cluster is WH110. HV110 has the right number but the wrong letters.""", trick=r"Swap the letters, add 3 to each, and subtract 92 from the number.")
S[9] = dict(raw=r"""Step 1: Study the given pairs (AKM32 → DNJ64)
A (1) + 3 = D, K (11) + 3 = N, M (13) − 3 = J (10), and 32 × 2 = 64.
Step 2: Confirm with DMO26 → GPL52
D + 3 = G, M + 3 = P, O (15) − 3 = L (12), and 26 × 2 = 52 ✓.
Step 3: Work backwards from FTJ42
Reverse each step: F (6) − 3 = C (3), T (20) − 3 = Q (17), J (10) + 3 = M (13), and 42 ÷ 2 = 21.
Step 4: Answer
The missing cluster is CQM21. Check: C + 3 = F, Q + 3 = T, M − 3 = J and 21 × 2 = 42 ✓.""", trick=r"Forward rule +3, +3, −3 and × 2 → reverse it on FTJ42 to get CQM21.")
S[10] = dict(raw=r"""Step 1: Study the first pair
854 − 803 = 51.
Step 2: Confirm with the second pair
2210 − 2159 = 51 ✓. So the second number = first number − 51.
Step 3: Apply the rule to the third pair
? − 51 = 9585, so ? = 9585 + 51 = 9636.
Step 4: Check
9636 − 51 = 9585 ✓. The missing number is 9636.""", trick=r"Subtract 51 each time → ? = 9585 + 51 = 9636.")
S[11] = dict(raw=r"""Step 1: Study the first pair
151 × 2 = 302, and 302 − 3 = 299.
Step 2: Confirm with the second pair
446 × 2 = 892, and 892 − 3 = 889 ✓. So the second number = 2 × first number − 3.
Step 3: Apply the rule to the third pair
2 × ? − 3 = 1641, so 2 × ? = 1644 and ? = 822.
Step 4: Check
822 × 2 − 3 = 1644 − 3 = 1641 ✓. The missing number is 822.""", trick=r"Double and subtract 3 → (1641 + 3) ÷ 2 = 822.")
S[12] = dict(raw=r"""Step 1: Compare the first two sentences
"rahul play chess" → rs ta ln and "chess require patience" → ta pq da. The common word is chess and the common code is ta, so chess = ta.
Step 2: Compare the second and third sentences
"chess require patience" → ta pq da and "patience help to win game" → da rn lm zx no. The common word is patience and the common code is da, so patience = da.
Step 3: Code the required words
chess patience = ta da (the order of codes does not matter in this type of question).
Step 4: Check the options
ln and lm belong to other words, and rn belongs to the third sentence only, so "ta da" is the only correct code.""", trick=r"Common word ↔ common code: chess = ta, patience = da.")
S[13] = dict(raw=r"""Step 1: First letters
S (19) → V (22) → Y (25) → ? → E (5): each step is +3. Y + 3 = 28 → 28 − 26 = 2 = B, and B + 3 = E ✓.
Step 2: Second letters
N (14) → J (10) → F (6) → ? → X (24): each step is −4. F − 4 = 2 = B, and B − 4 = −2 → 24 = X ✓.
Step 3: Numbers
816 − 682 = 134 and 682 − 548 = 134, so each number falls by 134: 548 − 134 = 414, and 414 − 134 = 280 ✓.
Step 4: Answer
The missing term is BB414.""", trick=r"Letters +3 and −4, numbers −134 → BB414.")
S[14] = dict(raw=r"""Step 1: First letters
B (2) → E (5) → ? → K (11) → N (14): each step is +3, so the missing first letter is H (8).
Step 2: Second letters
D (4) → H (8) → ? → P (16) → T (20): each step is +4, so the missing second letter is L (12).
Step 3: Third letters
C (3) → H (8) → ? → R (18) → W (23): each step is +5, so the missing third letter is M (13).
Step 4: Numbers and answer
22 → 44 → ? → 176 → 352: each number doubles, so the missing number is 88. The missing term is HLM88.""", trick=r"Letters +3, +4, +5; numbers × 2 → HLM88.")
S[15] = dict(raw=r"""Step 1: Write the angle formula
Angle between the hands = |30H − 5.5M| degrees, where H is the hour and M the minutes.
Step 2: Put H = 12 (treated as 0)
At 12 o'clock both hands are together, so after M minutes the angle is 5.5M degrees.
Step 3: Solve for 40°
5.5M = 40, so M = 40 ÷ 5.5 = 7.27 minutes (about 7 min 16 s).
Step 4: Answer
The angle is 40° at about 12:07 PM.""", trick=r"From 12 o'clock the gap grows 5.5° per minute: 40 ÷ 5.5 ≈ 7 minutes.")
S[16] = dict(raw=r"""Step 1: Write the angle formula
Angle = |30H − 5.5M|. For the hands to be opposite, the angle must be 180°.
Step 2: Put H = 8
30 × 8 = 240, so |240 − 5.5M| = 180.
Step 3: Solve
240 − 5.5M = 180 gives 5.5M = 60, so M = 60 ÷ 5.5 = 10.9 minutes (about 10 min 55 s). The other case, 5.5M − 240 = 180, gives M = 76.4, which is more than 60, so it is rejected.
Step 4: Answer
The hands are opposite at about 8:11 AM.""", trick=r"Opposite = 180°: (240 − 180) ÷ 5.5 ≈ 10.9 min → 8:11.")
S[17] = dict(raw=r"""Step 1: Track the filled arrowhead
It points NE in figure 1, N in figure 2, NW in figure 3 and W in figure 4 — it turns 45° anticlockwise each time, so in figure 5 it points SW.
Step 2: Track the hollow triangle
It is at SE, E, NE and N in figures 1 to 4 — also 45° anticlockwise each time — so in figure 5 it is at NW.
Step 3: Track the third mark
It alternates diamond and square and also moves 45° anticlockwise: diamond SW, square S, diamond SE, square E. So figure 5 has a diamond at NE.
Step 4: Choose the figure
The answer has a filled arrowhead at SW, a hollow triangle at NW and a diamond at NE — that is Figure 1.""", trick=r"All three marks step 45° anticlockwise; the third mark alternates diamond and square.")
S[18] = dict(raw=r"""Step 1: Name the four brackets
Each figure has a V with four small brackets: one at the top, one on the right, one at the bottom and one on the left.
Step 2: Compare the figures one by one
Figure 1 → 2: only the top bracket flips. Figure 2 → 3: only the right bracket flips. Figure 3 → 4: only the bottom bracket flips.
Step 3: Find the next change
The brackets flip one at a time in clockwise order (top, right, bottom …), so next the left bracket flips, while the other three stay as in figure 4.
Step 4: Choose the figure
The answer keeps the top, right and bottom brackets of figure 4 and has the left bracket turned the other way — that is Figure 2.""", trick=r"One bracket flips per step, going clockwise: top → right → bottom → left.")
S[19] = dict(raw=r"""Step 1: Count the bars
Figure 1 has 1 bar, figure 2 has 1, figure 3 has 2, figure 4 has 2 — each number of bars appears twice.
Step 2: Look at the shading
The bars alternate hollow, filled, hollow, filled.
Step 3: Find the fifth figure
After two pairs, the number of bars becomes 3, and after a filled figure the next one is hollow. So figure 5 has three hollow bars.
Step 4: Choose the figure
Figure 3 shows three hollow bars; Figures 1, 2 and 4 contain filled bars. So Figure 3 is the answer.""", trick=r"Bars 1, 1, 2, 2, 3 …; shading hollow, filled, hollow … → three hollow bars.")
S[20] = dict(raw=r"""Step 1: Find the present ages
Let the ages be 5x and 12x. Then 5x + 12x = 34, so 17x = 34 and x = 2. The ages are 10 years and 24 years.
Step 2: Go back 3 years
10 − 3 = 7 years and 24 − 3 = 21 years.
Step 3: Form the ratio
7 to 21 simplifies (÷ 7) to 1 to 3.
Step 4: Answer
Three years ago the ratio of their ages was \( 1 : 3 \).""", trick=r"17 parts = 34 → 1 part = 2 → ages 10, 24 → 7, 21 → \( 1 : 3 \).")
