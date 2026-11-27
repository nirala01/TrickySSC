S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first (BODMAS)
\( 24 + 17 = 41 \).
Step 2: Do the multiplication
\( 35 \times 2 = 70 \).
Step 3: Rewrite the expression
\( 93 - 47 + 69 - 41 + 70 \).
Step 4: Add and subtract from left to right
\( 93 - 47 = 46 \), \( 46 + 69 = 115 \), \( 115 - 41 = 74 \), \( 74 + 70 = 144 \).""", trick=r"Bracket, then ×, then + and − from left to right.")
S[42] = dict(raw=r"""Step 1: Solve the bracket and the multiplication
\( 27 \times 1 = 27 \).
Step 2: Do the division
\( 39 \div 3 = 13 \).
Step 3: Rewrite the expression
\( 92 + 27 - 41 + 13 + 21 - 17 \).
Step 4: Add and subtract from left to right
\( 92 + 27 = 119 \), \( 119 - 41 = 78 \), \( 78 + 13 = 91 \), \( 91 + 21 = 112 \), \( 112 - 17 = 95 \).""", trick=r"Do ÷ before + and −: \( 39 \div 3 = 13 \).")
S[43] = dict(raw=r"""Step 1: Recall the formulas for fractions
HCF of fractions \( = \dfrac{\text{HCF of numerators}}{\text{LCM of denominators}} \) and LCM of fractions \( = \dfrac{\text{LCM of numerators}}{\text{HCF of denominators}} \).
Step 2: Work with the numerators 3, 5, 7
HCF \( = 1 \) and LCM \( = 3 \times 5 \times 7 = 105 \).
Step 3: Work with the denominators 8, 12, 18
\( 8 = 2^{3} \), \( 12 = 2^{2} \times 3 \), \( 18 = 2 \times 3^{2} \). HCF \( = 2 \) and LCM \( = 2^{3} \times 3^{2} = 72 \).
Step 4: Put them together
HCF \( = \dfrac{1}{72} \) and LCM \( = \dfrac{105}{2} \).""", trick=r"HCF of fractions = HCF(top) ÷ LCM(bottom); LCM = LCM(top) ÷ HCF(bottom).")
S[44] = dict(raw=r"""Step 1: Use the identity for the numerator
With \( a = 2.5 \) and \( b = 1.5 \): \( a^{3} - b^{3} = (a - b)(a^{2} + ab + b^{2}) = 1 \times (6.25 + 3.75 + 2.25) = 12.25 \).
Step 2: Finish the numerator
\( 12.25 - 0.25 = 12 \).
Step 3: Simplify the denominator
\( 7.5 = 2 \times 2.5 \times 1.5 = 2ab \), so \( a^{2} + b^{2} - 2ab = (a - b)^{2} = 1^{2} = 1 \).
Step 4: Divide
\( \dfrac{12}{1} = 12 \).""", trick=r"Spot \( 7.5 = 2ab \): the denominator is \( (a - b)^{2} = 1 \).")
S[45] = dict(raw=r"""Step 1: Find the square roots
\( \sqrt{289} = 17 \), \( \sqrt{225} = 15 \), \( \sqrt{144} = 12 \).
Step 2: Multiply first (BODMAS)
\( 17 \times 15 = 255 \).
Step 3: Find x
\( x = 255 + 12 = 267 \).
Step 4: Find 2x
\( 2x = 2 \times 267 = 534 \).""", trick=r"Roots first, × before +; the question asks for 2x, not x.")
S[46] = dict(raw=r"""Step 1: Simplify the surds in the numerator
\( \sqrt{98} = 7\sqrt{2} \) and \( \sqrt{147} = 7\sqrt{3} \), so the numerator is \( 7(\sqrt{2} - \sqrt{3}) \).
Step 2: Simplify the surds in the denominator
\( \sqrt{18} = 3\sqrt{2} \) and \( \sqrt{27} = 3\sqrt{3} \), so the denominator is \( 3(\sqrt{2} - \sqrt{3}) \).
Step 3: Cancel the common factor
\( \dfrac{7(\sqrt{2} - \sqrt{3})}{3(\sqrt{2} - \sqrt{3})} = \dfrac{7}{3} \).
Step 4: Check
\( \sqrt{98} = \sqrt{49 \times 2} \) and \( \sqrt{18} = \sqrt{9 \times 2} \); the ratio of 49 to 9 under the root is \( \dfrac{7}{3} \) ✓.""", trick=r"Take out the perfect squares: 49 on top, 9 below → \( \dfrac{7}{3} \).")
S[47] = dict(raw=r"""Step 1: Write the breadth in terms of the length
Let the length be L; then breadth \( = \dfrac{4}{5}L \).
Step 2: Use the area
\( L \times \dfrac{4}{5}L = 320 \Rightarrow L^{2} = 400 \Rightarrow L = 20 \) m.
Step 3: Find the breadth
Breadth \( = \dfrac{4}{5} \times 20 = 16 \) m.
Step 4: Find the difference
\( 20 - 16 = 4 \) m (check: \( 20 \times 16 = 320 \) ✓).""", trick=r"Sides 5k and 4k: \( 20k^{2} = 320 \Rightarrow k = 4 \); difference = k = 4.")
S[48] = dict(raw=r"""Step 1: Recall the identity
\( (a - b)^{2} + 4ab = (a + b)^{2} \).
Step 2: Identify a and b
\( a = 325 \), \( b = 275 \).
Step 3: Apply the identity
\( (325 + 275)^{2} = 600^{2} \).
Step 4: Calculate
\( 600^{2} = 360000 \).""", trick=r"\( (a - b)^{2} + 4ab \) is just \( (a + b)^{2} \).")
S[49] = dict(raw=r"""Step 1: Use the perimeter
\( 2(l + b) = 140 \Rightarrow l + b = 70 \).
Step 2: Use the difference
\( l - b = 10 \).
Step 3: Solve
\( l = \dfrac{70 + 10}{2} = 40 \) m and \( b = \dfrac{70 - 10}{2} = 30 \) m.
Step 4: Find the area
Area \( = 40 \times 30 = 1200 \) sq m.""", trick=r"Sum 70, difference 10 → 40 and 30.")
S[50] = dict(raw=r"""Step 1: Find the total weight of A, B and C
\( 30 \times 3 = 90 \) kg.
Step 2: Find the totals of the pairs
A + B \( = 32 \times 2 = 64 \) kg and B + C \( = 38 \times 2 = 76 \) kg.
Step 3: Add the pair totals
\( (A + B) + (B + C) = 64 + 76 = 140 \) kg, which is A + B + C plus one extra B.
Step 4: Find B
\( B = 140 - 90 = 50 \) kg.""", trick=r"B = (A + B) + (B + C) − (A + B + C).")
S[51] = dict(raw=r"""Step 1: Find the sum of the first 100 numbers
\( 100 \times 53.5 = 5350 \).
Step 2: Find the total number of numbers
\( 100 + 50 = 150 \).
Step 3: Find the new total
\( 150 \times 74.1 = 11115 \).
Step 4: Find the sum of the new numbers
\( 11115 - 5350 = 5765 \).""", trick=r"New sum = new total − old total.")
S[52] = dict(raw=r"""Step 1: Understand the question
The lights change together again after a time that is a multiple of 30, 45 and 60 seconds — the LCM.
Step 2: Factorise
\( 30 = 2 \times 3 \times 5 \), \( 45 = 3^{2} \times 5 \), \( 60 = 2^{2} \times 3 \times 5 \).
Step 3: Find the LCM
LCM \( = 2^{2} \times 3^{2} \times 5 = 180 \) seconds \( = 3 \) minutes.
Step 4: Find the time
\( 7{:}00 \) a.m. + 3 minutes \( = 7{:}03 \) a.m.""", trick=r"'Change together again' = LCM.")
S[53] = dict(raw=r"""Step 1: Write the relation
SP \( = \) CP \( \times \dfrac{100 + \text{Profit}\%}{100} \).
Step 2: Substitute
\( 5625 = \) CP \( \times \dfrac{125}{100} \).
Step 3: Solve
CP \( = 5625 \times \dfrac{100}{125} = 5625 \times \dfrac{4}{5} = 4500 \).
Step 4: Check
25% of ₹4500 is ₹1125, and \( 4500 + 1125 = 5625 \) ✓. CP = ₹4500.""", trick=r"25% profit → SP is \( \dfrac{5}{4} \) of CP, so CP is \( \dfrac{4}{5} \) of SP.")
S[54] = dict(raw=r"""Step 1: Write A in terms of B
A is 20% less than B, so \( A = 80\% \) of B \( = 0.8B \).
Step 2: Substitute A = 480
\( 0.8B = 480 \).
Step 3: Solve
\( B = \dfrac{480}{0.8} = 600 \).
Step 4: Check
20% of 600 is 120, and \( 600 - 120 = 480 \) ✓.""", trick=r"A = 80% of B → B = A ÷ 0.8.")
S[55] = dict(raw=r"""Step 1: Find 30% of 500
\( \dfrac{30}{100} \times 500 = 150 \).
Step 2: Write the relation
150 is 50% more than A, so \( 150 = 1.5A \).
Step 3: Solve
\( A = \dfrac{150}{1.5} = 100 \).
Step 4: Check
50% of 100 is 50, and \( 100 + 50 = 150 \) ✓.""", trick=r"50% more = \( \dfrac{3}{2} \) times, so A = \( \dfrac{2}{3} \) of 150.")
S[56] = dict(raw=r"""Step 1: Take a convenient selling price
Let SP \( = 100 \).
Step 2: Find the profit
The profit is 30% of the SP \( = 30 \).
Step 3: Find the cost price
CP \( = 100 - 30 = 70 \).
Step 4: Find the ratio
Profit to CP \( = 30 \) to \( 70 = \) \( 3 : 7 \).""", trick=r"Profit on SP: take SP = 100, then CP = 100 − profit.")
S[57] = dict(raw=r"""Step 1: Write the time for the whole tank
The full tank is emptied in 48 minutes.
Step 2: Find the rate
The pipe empties \( \dfrac{1}{48} \) of the tank each minute.
Step 3: Find the time for the given part
Time \( = \dfrac{1}{6} \div \dfrac{1}{48} = \dfrac{48}{6} \).
Step 4: Calculate
\( \dfrac{48}{6} = 8 \) minutes.""", trick=r"Part of the tank × full time: \( \dfrac{1}{6} \times 48 = 8 \).")
S[58] = dict(raw=r"""Step 1: Write the one-day work
P + Q do \( \dfrac{1}{8} \) of the work per day; R does \( \dfrac{1}{16} \) per day.
Step 2: Add the rates
\( \dfrac{1}{8} + \dfrac{1}{16} = \dfrac{2 + 1}{16} = \dfrac{3}{16} \) per day.
Step 3: Find the time for the whole work
\( \dfrac{16}{3} \) days.
Step 4: Find the time for half the work
\( \dfrac{1}{2} \times \dfrac{16}{3} = \dfrac{8}{3} \) days.""", trick=r"Total work = LCM 16 units: rates 2 + 1 = 3 units/day; half = 8 units → \( \dfrac{8}{3} \) days.")
S[59] = dict(raw=r"""Step 1: Understand crossing
When two trains cross each other, the distance covered is the sum of their lengths.
Step 2: Find the relative speed
In opposite directions the speeds add: relative speed \( = 40 \) m/s (given as the total speed).
Step 3: Use time = distance ÷ speed
Time \( = \dfrac{800}{40} \).
Step 4: Calculate
\( \dfrac{800}{40} = 20 \) seconds.""", trick=r"Opposite directions: add speeds; distance = sum of lengths.")
S[60] = dict(raw=r"""Step 1: Use the man-crossing time
A standing man is a point, so the train covers its own length in 4 s: length of train \( = 4v \), where v is the speed.
Step 2: Use the platform-crossing time
Crossing the platform, the train covers its length plus the platform: \( \text{train} + \text{platform} = 12v \).
Step 3: Form the ratio
\( \dfrac{4v}{12v} = \dfrac{1}{3} \).
Step 4: Answer
Length of train to total length of train and platform \( = \) \( 1 : 3 \).""", trick=r"At the same speed, lengths are in the ratio of times: 4 to 12.")
