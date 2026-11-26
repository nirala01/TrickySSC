S = {}
S[1] = dict(raw=r"""Step 1: Convert the letters to positions
W = 23, Y = 25, ?, E = 5, I = 9, K = 11, O = 15, Q = 17, U = 21.
Step 2: Find the gaps
W → Y is +2; E → I is +4, I → K is +2, K → O is +4, O → Q is +2, Q → U is +4. The steps alternate +2, +4.
Step 3: Find the missing term
After the +2 step (W → Y) comes a +4 step: 25 + 4 = 29 → 29 − 26 = 3 = C.
Step 4: Check
C (3) + 2 = E (5) ✓, which continues the +2, +4 pattern. So the missing letter is C.""", trick=r"Alternate +2 and +4; after Z count again from A.")
S[2] = dict(raw=r"""Step 1: Study FR → HW
F (6) + 2 = H (8); R (18) + 5 = W (23). So the first letter moves 2 ahead and the second 5 ahead.
Step 2: Confirm with GT → IY
G (7) + 2 = I (9); T (20) + 5 = Y (25) ✓ — the same +2, +5 rule.
Step 3: Apply it to IN
I (9) + 2 = K (11); N (14) + 5 = S (19). So IN → KS.
Step 4: Check the others
JS is +1, +5; IR is 0, +4; KU is +2, +7 — none follows +2, +5. The answer is KS.""", trick=r"First letter +2, second letter +5.")
S[3] = dict(raw=r"""Step 1: Split each cluster into first and second letters
First letters: N, P, T, V, Z, ?, F, H. Second letters: Z, T, N, H, B, ?, P, J.
Step 2: Pattern of the first letters
N → P (+2) → T (+4) → V (+2) → Z (+4) → ? (+2) = B (26 + 2 = 28 → 2) → F (+4) → H (+2) ✓
Step 3: Pattern of the second letters
Z (26) → T (20) → N (14) → H (8) → B (2): each step is −6. Next: 2 − 6 = −4 → 22 = V, then V → P (16) → J (10) ✓
Step 4: Answer
The missing cluster is BV.""", trick=r"First letters +2, +4 alternately; second letters −6 each time.")
S[4] = dict(raw=r"""Step 1: Read the first set (VS, XU, ZW)
First letters V → X → Z move +2 each time; second letters S → U → W also move +2 each time.
Step 2: Confirm with (FT, HV, JX)
F → H → J is +2, +2 and T → V → X is +2, +2 ✓
Step 3: Test the options
(ET, GV, IX): E → G → I is +2, +2 and T → V → X is +2, +2 ✓
(ZA, BB, DE) has A → B → E (+1, +3); (JP, LS, NT) has P → S → T (+3, +1); (VI, XL, ZM) has I → L → M (+3, +1) — all break the rule.
Step 4: Answer
The set (ET, GV, IX) follows the same +2, +2 rule.""", trick=r"Check first letters and second letters separately — both +2, +2 here.")
S[5] = dict(raw=r"""Step 1: Know the type of year
2013 is an ordinary year (not divisible by 4), so we need a later ordinary year that starts on the same day.
Step 2: Count odd days year by year
2013 → 1, 2014 → 1, 2015 → 1, 2016 (leap) → 2, 2017 → 1, 2018 → 1. Total = 7 odd days = 0 odd days.
Step 3: Conclude
So 1 January 2019 falls on the same day as 1 January 2013, and 2019 is also an ordinary year. The two calendars match.
Step 4: Reject the others
2025 starts on a Wednesday (2013 on a Tuesday); 2035 and 2037 do not start on a Tuesday either. The answer is 2019.""", trick=r"For an ordinary year after a leap year (like 2013), add 6 years: 2013 + 6 = 2019.")
S[6] = dict(raw=r"""Step 1: Note the direction
All face south, so a person's right is our left as we look at them. We simply count "to the right" in their own direction.
Step 2: Fix the ends
A is fourth to the right of G. In a row of 5, this is possible only if G is at one end and A at the other end.
Step 3: Fill the middle
B is immediately to the right of S and H is to the left of S. Going from G towards A: G, H, S, B, A ✓
Step 4: Answer
The persons at the extreme ends are A and G.""", trick=r"In a row of 5, “fourth to the right” puts the two people at the two ends.")
S[7] = dict(raw=r"""Step 1: Use seat numbers
All face away from the centre. Number the seats 0–6 so that one seat to a girl's right is +1 (and to her left −1). Put G3 at 0.
Step 2: Place G6, G1 and G7
G6 is second to the left of G3 → seat 5. G1 is third to the right of G3 → seat 3. G7 is third to the right of G6 → 5 + 3 = 8 → seat 1.
Step 3: Place G4, G2 and G5
Seats 2, 4, 6 are left. G4 is not next to G6 (seat 5), so G4 is not at 4 or 6 → G4 = 2. G2 is not next to G1 (seat 3), so G2 is not at 4 → G2 = 6. Hence G5 = 4.
Step 4: Answer
The seat immediately to the left of G5 is 4 − 1 = 3, which is G1.""", trick=r"Seat numbers (right = +1, left = −1) make outward-facing problems easy.")
S[8] = dict(raw=r"""Step 1: List the letters of ECOSYSTEM
E – 2, C – 1, O – 1, S – 2, Y – 1, T – 1, M – 1.
Step 2: Check COMETS and MEETS
COMETS uses C, O, M, E, T, S — all present ✓. MEETS uses M, E, E, T, S — two E's are available ✓
Step 3: Check SEEMS
SEEMS uses S, E, E, M, S — two S's and two E's are available ✓
Step 4: Check STEAMS
STEAMS needs the letter A, which is not in ECOSYSTEM. So STEAMS cannot be formed.""", trick=r"Look first for a letter that is missing from the given word (here A).")
S[9] = dict(raw=r"""Step 1: Look at how each term grows
1 → 3 → 10 → 41 → 206 → 1237: the terms grow faster each time, so try multiplication.
Step 2: Find the rule
1 × 2 + 1 = 3, 3 × 3 + 1 = 10, 10 × 4 + 1 = 41, 41 × 5 + 1 = 206, 206 × 6 + 1 = 1237.
Step 3: Next term
1237 × 7 + 1 = 8659 + 1 = 8660.
Step 4: Answer
The next number is 8660.""", trick=r"Multiply by 2, 3, 4, 5 … and add 1 each time.")
S[10] = dict(raw=r"""Step 1: Find the differences
723 − 705 = 18, 705 − 690 = 15, 690 − 678 = 12.
Step 2: Spot the pattern
The differences fall by 3 each time: 18, 15, 12, so the next difference is 9.
Step 3: Next term
678 − 9 = 669.
Step 4: Answer
The missing number is 669.""", trick=r"Differences 18, 15, 12, 9 — decreasing by 3.")
S[11] = dict(raw=r"""Step 1: Try multiplication with an increasing multiplier
4 × 3 = 12, and 13 − 12 = 1; 13 × 4 = 52, and 56 − 52 = 4.
Step 2: Find the full rule
4 × 3 + 1² = 13, 13 × 4 + 2² = 56, 56 × 5 + 3² = 289, 289 × 6 + 4² = 1750.
Step 3: Next term
1750 × 7 + 5² = 12250 + 25 = 12275.
Step 4: Answer
The next number is 12,275.""", trick=r"×3 + 1², ×4 + 2², ×5 + 3² … → ×7 + 5².")
S[12] = dict(raw=r"""Step 1: Study the first pair
The first figure is a black triangle with a small white triangle at its tip. The second figure keeps this triangle and places beside it a copy with the colours reversed — a white triangle with a black tip.
Step 2: State the rule
Second figure = the original figure + its colour-inverted copy (same direction).
Step 3: Apply it to the third figure
The third figure is a black triangle pointing right with a small white tip. So the answer must show this same triangle together with a right-pointing white triangle that has a black tip.
Step 4: Eliminate the others
One choice pairs it with a plain outline triangle (no black tip), and the others have triangles pointing left. Only the figure with the right-pointing black triangle (white tip) above a right-pointing white triangle (black tip) fits.""", trick=r"Original + its colour-reversed copy, both in the same direction.")
S[13] = dict(raw=r"""Step 1: Study the letters
EFGH → HEFG: the last letter moves to the front.
Step 2: Study the corner symbols
In the first figure: top-left ▲, top-right ■, bottom-left ●, bottom-right pentagon. In the second figure the two top symbols swap places and the two bottom symbols swap places (a left–right swap).
Step 3: Apply both rules to the third figure
IJKL → LIJK. Corners: top-left ○ and top-right □ swap → □ at top-left, ○ at top-right; bottom-left 5 and bottom-right ▲ swap → ▲ at bottom-left, 5 at bottom-right.
Step 4: Pick the figure
The answer shows LIJK with □ top-left, ○ top-right, ▲ bottom-left and 5 bottom-right. The figure with LIKJ has the wrong letter order, and the others keep the old corner positions or mix the symbols.""", trick=r"Two changes: last letter to the front, and corner symbols swap left ↔ right.")
S[14] = dict(raw=r"""Step 1: Study JT290 → KU436
J → K (+1), T → U (+1); 436 − 290 = 146.
Step 2: Confirm with BF300 → CG446
B → C (+1), F → G (+1); 446 − 300 = 146 ✓
Step 3: Apply it to KO480
K → L, O → P; 480 + 146 = 626. So the answer is LP626.
Step 4: Check the others
LN626 has N (O − 1), LP706 and NM706 have the wrong number (+226). Only LP626 fits.""", trick=r"Each letter +1 and the number +146.")
S[15] = dict(raw=r"""Step 1: Look for the letter rule
Direct shifts do not work (L → M is +1 but A → K is +10). So reverse the letters first: LPR → RPL and AKP → PKA.
Step 2: Find the shifts after reversing
RPL → MSM: R − 5 = M, P + 3 = S, L + 1 = M. PKA → KNB: P − 5 = K, K + 3 = N, A + 1 = B ✓ The numbers rise by 100 (80 → 180, 110 → 210).
Step 3: Apply it to YVT150
Reverse: TVY. Then T − 5 = O, V + 3 = Y, Y + 1 = Z → OYZ. Number: 150 + 100 = 250.
Step 4: Answer
The cluster is OYZ250.""", trick=r"Reverse the letters, then −5, +3, +1; the number +100.")
S[16] = dict(raw=r"""Step 1: Compare the first letters
All words begin with "Dis". The fourth letters are f (Disfavour) and g (all the others), so Disfavour comes first.
Step 2: Compare the fifth letters
Disgorge (o), Disgrace (r), Disguise (u), Disgust (u): o comes before r, and r before u.
Step 3: Compare Disguise and Disgust
Both begin with "Disgu". The sixth letters are i (Disgu-i-se) and s (Disgu-s-t); i comes before s, so Disguise comes before Disgust.
Step 4: Final order
Disfavour (1), Disgorge (2), Disgrace (3), Disguise (4), Disgust (5) → 12345.""", trick=r"Compare letter by letter: f < g, then o < r < u, then i < s.")
S[17] = dict(raw=r"""Step 1: Find the rule from the first pair
9334 − 9285 = 49.
Step 2: Confirm with the third pair
4522 − 4473 = 49 ✓ So the second number = first number + 49.
Step 3: Work backwards for the missing number
? + 49 = 7980 → ? = 7980 − 49 = 7931.
Step 4: Answer
The missing number is 7931.""", trick=r"Second = first + 49, so first = second − 49.")
S[18] = dict(raw=r"""Step 1: Compare BASIL with CCWGI
B → C (+1), A → C (+2), S → W (+4), I → G (−2), L → I (−3).
Step 2: Confirm with TUMOR → UWQMO
T → U (+1), U → W (+2), M → Q (+4), O → M (−2), R → O (−3) ✓
Step 3: Apply to DELTA
D + 1 = E, E + 2 = G, L + 4 = P, T − 2 = R, A − 3 = X (1 − 3 = −2 → 24).
Step 4: Answer
DELTA is coded as EGPRX.""", trick=r"Position-wise shifts: +1, +2, +4, −2, −3.")
S[19] = dict(raw=r"""Step 1: Find the rate of gain
From 5:00 AM to 5:00 PM (12 hours) the clock goes from 4 minutes fast to 16 minutes fast, so it gains 12 minutes in 12 hours = 1 minute per hour.
Step 2: Work back to zero
At 5:00 AM it is 4 minutes fast. It was correct when it had gained nothing yet, i.e. 4 hours earlier.
Step 3: Find the time
5:00 AM − 4 hours = 1:00 AM.
Step 4: Answer
The clock showed the correct time at 1:00 AM.""", trick=r"Gain per hour = 12 ÷ 12 = 1 min; 4 min fast → correct 4 hours earlier.")
S[20] = dict(raw=r"""Step 1: Follow the hook (the "1"-shaped line)
It moves along the border in the clockwise sense: bottom-right → bottom-middle → bottom-left → left side → next it reaches the top-left.
Step 2: Follow the horizontal arrow
It also moves clockwise: top-left → top-middle → top-right → right side → next it reaches the bottom-right.
Step 3: Note the shapes
In figures 1 and 3 the arrow's barb points down and the hook bends to the left; in figures 2 and 4 they turn the other way. So the fifth figure looks like figure 1 and 3: barb down, hook bent left.
Step 4: Pick the figure
The answer has the hook at the top-left and the arrow at the bottom-right with its barb pointing down. The similar figure with the barb pointing up, and the figures with the hook in the middle, do not fit.""", trick=r"Track each element separately: position (around the border) and shape (alternating).")
