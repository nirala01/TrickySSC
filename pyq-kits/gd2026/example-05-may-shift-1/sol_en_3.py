S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first
\( 38 + 19 = 57 \)
Step 2: Multiply
\( 57 \times 2 = 114 \)
Step 3: Add and subtract from left to right
\( 82 + 41 - 27 + 114 - 77 = 123 - 27 + 114 - 77 = 96 + 114 - 77 \)
Step 4: Final value
\( 210 - 77 = 133 \)""", trick=r"BODMAS: bracket → × → + and − from left to right.")
S[42] = dict(raw=r"""Step 1: Read "of" and ÷ first
\( 33 \text{ of } 2 = 33 \times 2 = 66 \) and \( 36 \div 6 = 6 \)
Step 2: Rewrite the expression
\( 92 + 63 - 6 + 66 - 58 + 29 \)
Step 3: Add the positive terms
\( 92 + 63 + 66 + 29 = 250 \)
Step 4: Subtract the rest
\( 250 - 6 - 58 = 186 \)""", trick=r"'of' means multiply and is done before ÷ and the other operations.")
S[43] = dict(raw=r"""Step 1: First product
\( 0.625 \times 0.4 = 0.25 \)
Step 2: Second product
\( 0.25 \times 0.8 = 0.2 \)
Step 3: Add the numerator
\( 0.25 + 0.2 = 0.45 \)
Step 4: Divide
\( \dfrac{0.45}{0.18} = \dfrac{45}{18} = 2.5 \)""", trick=r"0.625 = 5/8, so 5/8 × 0.4 = 0.25; then 0.45 ÷ 0.18 = 2.5.")
S[44] = dict(raw=r"""Step 1: Spot the identity
\( 31.875 = 2 \times 4.25 \times 3.75 \) because \( 4.25 \times 3.75 = 15.9375 \) and \( 2 \times 15.9375 = 31.875 \).
Step 2: Write the expression as a square
\( 4.25^{2} + 3.75^{2} + 2 \times 4.25 \times 3.75 = (4.25 + 3.75)^{2} \)
Step 3: Add inside the bracket
\( 4.25 + 3.75 = 8 \)
Step 4: Square
\( 8^{2} = 64 \)""", trick=r"a² + b² + 2ab = (a + b)².")
S[45] = dict(raw=r"""Step 1: Square and products
\( 15^{2} = 225 \), \( 5 \times 7 = 35 \), \( 4 \times 18 = 72 \)
Step 2: Simplify under the root
\( 225 + 35 - 72 + 8 = 196 \)
Step 3: Take the square root
\( \sqrt{196} = 14 \)
Step 4: Check
\( 14^{2} = 196 \), so the value is 14.""", trick=r"Simplify fully under the root before taking √.")
S[46] = dict(raw=r"""Step 1: Use Pythagoras
Diagonal \( d = \sqrt{a^{2} + a^{2}} = a\sqrt{2} \) for a square of side a.
Step 2: Substitute
\( d = 12\sqrt{2} \) cm
Step 3: Approximate value
\( 12 \times 1.414 \approx 16.97 \) cm
Step 4: Eliminate the others
\( 12\sqrt{3} \) is the space diagonal of a cube of side 12, and 48 cm is the perimeter. So the diagonal is \( 12\sqrt{2} \) cm.""", trick=r"Diagonal of a square = side × √2.")
S[47] = dict(raw=r"""Step 1: Side of the rhombus
\( \text{side} = \dfrac{58}{4} = 14.5 \) cm
Step 2: Half of the known diagonal
\( \dfrac{20}{2} = 10 \) cm. The diagonals bisect each other at right angles.
Step 3: Half of the other diagonal
\( \sqrt{14.5^{2} - 10^{2}} = \sqrt{210.25 - 100} = \sqrt{110.25} = 10.5 \) cm, so the other diagonal \( = 21 \) cm.
Step 4: Sum
\( 20 + 21 = 41 \) cm""", trick=r"(d₁/2)² + (d₂/2)² = side².")
S[48] = dict(raw=r"""Step 1: Use the area
\( \dfrac{d_1 d_2}{2} = 840 \Rightarrow d_1 d_2 = 1680 \)
Step 2: Use the side
\( d_1^{2} + d_2^{2} = 4 \times 37^{2} = 4 \times 1369 = 5476 \)
Step 3: Form the square of the sum
\( (d_1 + d_2)^{2} = d_1^{2} + d_2^{2} + 2 d_1 d_2 = 5476 + 3360 = 8836 \)
Step 4: Take the root
\( d_1 + d_2 = \sqrt{8836} = 94 \) cm (the diagonals are 70 cm and 24 cm).""", trick=r"(d₁ + d₂)² = 4a² + 4 × Area.")
S[49] = dict(raw=r"""Step 1: Use the property of HCF
\( \text{HCF}(A, B, C) = \text{HCF}(\text{HCF}(A, B), C) \)
Step 2: Substitute
\( \text{HCF}(36, 18) \)
Step 3: Find it
18 divides 36 exactly, so \( \text{HCF}(36, 18) = 18 \).
Step 4: Answer
The HCF of A, B and C is 18.""", trick=r"HCF of three numbers = HCF of (HCF of two) and the third.")
S[50] = dict(raw=r"""Step 1: They change together again after the LCM of the intervals
\( \text{LCM}(90, 120, 150) \)
Step 2: Factorise
\( 90 = 2 \times 3^{2} \times 5 \), \( 120 = 2^{3} \times 3 \times 5 \), \( 150 = 2 \times 3 \times 5^{2} \)
Step 3: LCM
\( 2^{3} \times 3^{2} \times 5^{2} = 1800 \) seconds \( = 30 \) minutes
Step 4: Add to the starting time
5:20 p.m. + 30 minutes = 5:50 p.m.""", trick=r"Next simultaneous change = LCM of the intervals.")
S[51] = dict(raw=r"""Step 1: Time for the whole tank
100 minutes \( = 100 \times 60 = 6000 \) seconds
Step 2: Fraction to be filled
\( 80\% = \dfrac{4}{5} \)
Step 3: Time for that fraction
\( \dfrac{4}{5} \times 6000 = 4800 \) seconds
Step 4: Check
4800 seconds \( = 80 \) minutes, which is 80% of 100 minutes ✓""", trick=r"80% of 100 min = 80 min = 4800 s.")
S[52] = dict(raw=r"""Step 1: Write the efficiencies as equations
\( Q + R = 3P \) and \( P + R = 2.5Q \)
Step 2: Use the given time
Q and R together finish in 60 days, so \( Q + R = \dfrac{1}{60} \) of the work per day.
Step 3: Find P's rate
\( 3P = \dfrac{1}{60} \Rightarrow P = \dfrac{1}{180} \) per day
Step 4: Answer
P alone takes \( 3 \times 60 = 180 \) days. (The second condition is not needed to find P.)""", trick=r"Q + R = 3P → P's time = 3 × 60 = 180 days.")
S[53] = dict(raw=r"""Step 1: Distance to cover
A man is a point, so the train covers only its own length: 450 m.
Step 2: Speed in m/s
\( 20 \times \dfrac{5}{18} = \dfrac{50}{9} \) m/s
Step 3: Time in seconds
\( \dfrac{450}{50/9} = 450 \times \dfrac{9}{50} = 81 \) s
Step 4: Convert to minutes
\( \dfrac{81}{60} = \dfrac{27}{20} \) minutes""", trick=r"Time (min) = length (km) ÷ speed (km/h) × 60 = 0.45 ÷ 20 × 60 = 27/20.")
S[54] = dict(raw=r"""Step 1: Distance to cover
The train covers its own length: 500 m.
Step 2: Speed in m/s
\( 40 \times \dfrac{5}{18} = \dfrac{100}{9} \) m/s
Step 3: Time in seconds
\( \dfrac{500}{100/9} = 45 \) s
Step 4: Convert to minutes
\( \dfrac{45}{60} = \dfrac{3}{4} \) minute""", trick=r"0.5 km ÷ 40 km/h = 1/80 h = 0.75 min.")
S[55] = dict(raw=r"""Step 1: Write the differences
\( p - q = 3k \), \( q - r = 4k \), \( r - s = 7k \)
Step 2: Express p and s through r
\( q = r + 4k \), so \( p = q + 3k = r + 7k \); and \( s = r - 7k \).
Step 3: Add p and s
\( p + s = (r + 7k) + (r - 7k) = 2r \)
Step 4: Ratio
\( (p + s) : r = 2r : r = 2 : 1 \)""", trick=r"p is 7k above r and s is 7k below r, so p + s = 2r.")
S[56] = dict(raw=r"""Step 1: Let the numbers be
\( A = 3x \), \( B = x \)
Step 2: Form the equation
\( \dfrac{3x + 2}{x + 2} = \dfrac{5}{3} \Rightarrow 9x + 6 = 5x + 10 \)
Step 3: Solve
\( 4x = 4 \Rightarrow x = 1 \), so A = 3 and B = 1.
Step 4: Sum
\( 3 + 1 = 4 \). (Check: 5 and 3 give the ratio \( 5 : 3 \) ✓)""", trick=r"Test x = 1: A = 3, B = 1 → after adding 2, 5 and 3 ✓.")
S[57] = dict(raw=r"""Step 1: Take the cost price as 35
(35 is divisible by both 5 and 7.)
Step 2: Marked price
\( \dfrac{7}{5} \times 35 = 49 \)
Step 3: Selling price
\( \dfrac{6}{7} \times 49 = 42 \)
Step 4: Profit percentage
\( \dfrac{42 - 35}{35} \times 100 = \dfrac{7}{35} \times 100 = 20\% \)""", trick=r"SP/CP = 7/5 × 6/7 = 6/5 → 20% profit.")
S[58] = dict(raw=r"""Step 1: Use SP = MP × (1 − discount)
Step 2: First two
\( 8000 \times 0.75 = 6000 \); \( 6000 \times 0.75 = 4500 \)
Step 3: Last two
\( 5000 \times 0.70 = 3500 \); \( 8000 \times 0.70 = 5600 \)
Step 4: Compare
The highest selling price is ₹6000, for marked price ₹8000 with a 25% discount.""", trick=r"Same MP → smaller discount gives higher SP.")
S[59] = dict(raw=r"""Step 1: Use MP = SP ÷ (1 − discount)
Step 2: First option
\( \dfrac{3000}{0.75} = 4000 \) ✓
Step 3: Check the others
\( \dfrac{2500}{0.85} \approx 2941 \), \( \dfrac{3800}{0.88} \approx 4318 \), \( \dfrac{3200}{0.85} \approx 3765 \)
Step 4: Answer
Only selling price ₹3000 with a 25% discount gives a marked price of ₹4000.""", trick=r"Check backwards: 4000 × 0.75 = 3000 ✓.")
S[60] = dict(raw=r"""Step 1: Set up the proportion
\( 12 : 4 = 18 : x \)
Step 2: Product of extremes = product of means
\( 12x = 4 \times 18 = 72 \)
Step 3: Solve
\( x = \dfrac{72}{12} = 6 \)
Step 4: Check
\( \dfrac{12}{4} = 3 = \dfrac{18}{6} \) ✓""", trick=r"Fourth proportional of a, b, c = bc ÷ a.")
