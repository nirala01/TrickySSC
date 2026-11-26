S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket
\( 41 + 21 = 62 \)
Step 2: Write the expression again
\( 73 + 92 - 61 + 62 - 78 + 33 \)
Step 3: Add all the positive terms
\( 73 + 92 + 62 + 33 = 260 \)
Step 4: Subtract the negative terms
\( 260 - 61 - 78 = 260 - 139 = 121 \)""", trick=r"Add all the plus terms together, then subtract all the minus terms together.")
S[42] = dict(raw=r"""Step 1: Solve the bracket
\( 36 \div 6 = 6 \)
Step 2: Solve “of”
“42 of 1” means \( 42 \times 1 = 42 \)
Step 3: Write the expression again
\( 79 + 29 - 6 + 42 + 13 - 24 \)
Step 4: Simplify
\( 79 + 29 + 42 + 13 = 163 \) and \( 163 - 6 - 24 = 133 \)""", trick=r"BODMAS: Bracket, then “of”, then ÷ and ×, then + and −.")
S[43] = dict(raw=r"""Step 1: Use the rule
Product of two numbers = HCF × LCM
Step 2: Put in the values
\( 42 \times x = 14 \times 168 \)
Step 3: Solve
\( x = \dfrac{14 \times 168}{42} = \dfrac{2352}{42} = 56 \)
Step 4: Check
\( 42 = 14 \times 3 \) and \( 56 = 14 \times 4 \); 3 and 4 are co-prime, so HCF = 14 ✓ and LCM = \( 14 \times 3 \times 4 = 168 \) ✓""", trick=r"Other number = (HCF × LCM) ÷ given number.")
S[44] = dict(raw=r"""Step 1: Compare with an identity
\( (a - b)^{3} = a^{3} - 3a^{2}b + 3ab^{2} - b^{3} \)
Step 2: Match the terms
\( (4.2)^{2} \times 4.2 = (4.2)^{3} \), so \( a = 4.2 \) and \( b = 0.2 \)
Step 3: Write it as one cube
\( (4.2 - 0.2)^{3} = 4^{3} \)
Step 4: Answer
\( 4^{3} = 64 \)""", trick=r"Spot the pattern a³ − 3a²b + 3ab² − b³ = (a − b)³.")
S[45] = dict(raw=r"""Step 1: Find the square roots
\( \sqrt{484} = 22 \), \( \sqrt{121} = 11 \), \( \sqrt{64} = 8 \)
Step 2: Divide first (BODMAS)
\( 22 \div 11 = 2 \)
Step 3: Find x
\( x = 2 + 8 = 10 \)
Step 4: Find x²
\( x^{2} = 10^{2} = 100 \)""", trick=r"Do ÷ before +: √484 ÷ √121 = 2, then add 8.")
S[46] = dict(raw=r"""Step 1: Use the identity
\( (a + b)^{2} + (a - b)^{2} = 2(a^{2} + b^{2}) \)
Step 2: Put a = 5 and b = √3
\( 2\left(5^{2} + (\sqrt{3})^{2}\right) = 2(25 + 3) \)
Step 3: Simplify
\( 2 \times 28 = 56 \)
Step 4: Subtract 40
\( 56 - 40 = 16 \)""", trick=r"(a + b)² + (a − b)² = 2(a² + b²) — the √ terms cancel.")
S[47] = dict(raw=r"""Step 1: Know the rules
A number is divisible by 3 if its digit sum is divisible by 3, and by 8 if its last three digits are divisible by 8.
Step 2: Test 5448
Digit sum \( 5 + 4 + 4 + 8 = 21 \) (divisible by 3) ✓; \( 448 \div 8 = 56 \) ✓
Step 3: Test the others
5240: digit sum 11 ✗; 5560: digit sum 16 ✗; 6170: digit sum 14 ✗ and \( 170 \div 8 \) is not exact
Step 4: Answer
Only 5448 is divisible by both 3 and 8 (that is, by 24): \( 5448 = 24 \times 227 \)""", trick=r"Divisible by 3 and 8 = divisible by 24 — check the digit sum and the last three digits.")
S[48] = dict(raw=r"""Step 1: Find the outer rectangle
A path of 4 m outside adds 4 m on each side: length \( 180 + 2 \times 4 = 188 \) m, breadth \( 70 + 2 \times 4 = 78 \) m
Step 2: Area of the outer rectangle
\( 188 \times 78 = 14664 \) sq m
Step 3: Area of the garden
\( 180 \times 70 = 12600 \) sq m
Step 4: Area of the path
\( 14664 - 12600 = 2064 \) sq m. (Shortcut: \( 2w(l + b + 2w) = 2 \times 4 \times (180 + 70 + 8) = 8 \times 258 = 2064 \))""", trick=r"Path outside: area = 2w(l + b + 2w).")
S[49] = dict(raw=r"""Step 1: Let the numbers be
First number = x, second number = 2x (the first is half of the second)
Step 2: Use the average
Sum \( = 66 \times 2 = 132 \)
Step 3: Solve
\( x + 2x = 132 \Rightarrow 3x = 132 \Rightarrow x = 44 \)
Step 4: Check
Second number = 88; \( (44 + 88) \div 2 = 66 \) ✓""", trick=r"Ratio 1 : 2 → 3 parts = 132, 1 part = 44.".replace(' : ', ' to '))
S[50] = dict(raw=r"""Step 1: Find the side
Perimeter = 4 × side, so side \( = 100 \div 4 = 25 \) cm
Step 2: Use the half-diagonals
The diagonals of a rhombus bisect each other at right angles. Half of 30 cm is 15 cm.
Step 3: Find the other diagonal
\( \sqrt{25^{2} - 15^{2}} = \sqrt{625 - 225} = \sqrt{400} = 20 \) cm, so the other diagonal \( = 2 \times 20 = 40 \) cm
Step 4: Find the area
Area \( = \dfrac{1}{2} \times 30 \times 40 = 600 \) sq cm""", trick=r"Rhombus: side² = (d₁/2)² + (d₂/2)²; area = ½ d₁ d₂. Here 15-20-25 is a 3-4-5 triangle.")
S[51] = dict(raw=r"""Step 1: Sum of the first group
\( 5 \times 23 = 115 \)
Step 2: Sum of the remaining group
Remaining numbers \( = 14 - 5 = 9 \); sum \( = 9 \times 37 = 333 \)
Step 3: Total sum
\( 115 + 333 = 448 \)
Step 4: Find m
\( m = 448 \div 14 = 32 \)""", trick=r"Combined average = (total of all groups) ÷ (total count).")
S[52] = dict(raw=r"""Step 1: The largest square tile has side = HCF of the sides
HCF of 525 and 700
Step 2: Find the HCF
\( 525 = 3 \times 5^{2} \times 7 \) and \( 700 = 2^{2} \times 5^{2} \times 7 \), so HCF \( = 5^{2} \times 7 = 175 \) cm
Step 3: Tiles along each side
\( 525 \div 175 = 3 \) and \( 700 \div 175 = 4 \)
Step 4: Number of tiles
\( 3 \times 4 = 12 \) tiles""", trick=r"Largest square tile → HCF; number of tiles = area ÷ tile area.")
S[53] = dict(raw=r"""Step 1: Let the number be N
\( \dfrac{2}{5} \) of 60% of N = 420
Step 2: Write it as an equation
\( \dfrac{2}{5} \times \dfrac{60}{100} \times N = 420 \)
Step 3: Simplify
\( \dfrac{120}{500} \times N = 420 \Rightarrow 0.24N = 420 \)
Step 4: Solve
\( N = 420 \div 0.24 = 1750 \)""", trick=r"2/5 of 60% = 24%; 24% of N = 420 → N = 1750.")
S[54] = dict(raw=r"""Step 1: The difference is the loss
CP − SP = ₹720, and this loss is 30% of CP.
Step 2: Find the CP
\( 0.30 \times \text{CP} = 720 \Rightarrow \text{CP} = 720 \div 0.3 = 2400 \)
Step 3: Find the SP
\( \text{SP} = 2400 - 720 = 1680 \)
Step 4: Check
Loss % \( = \dfrac{720}{2400} \times 100 = 30\% \) ✓, so SP = ₹1680""", trick=r"Loss amount = loss% of CP → CP first, then SP = CP − loss.")
S[55] = dict(raw=r"""Step 1: Take CP = 100
Let the cost price be ₹100.
Step 2: Find the SP
50% profit → SP \( = 100 + 50 = 150 \)
Step 3: Form the ratio
\( \text{SP} : \text{CP} = 150 : 100 \)
Step 4: Simplify
\( 150 : 100 = 3 : 2 \)""", trick=r"Profit r% → SP to CP = (100 + r) to 100.")
S[56] = dict(raw=r"""Step 1: Let the numbers be a (first) and b (second)
\( a + b = \dfrac{35}{20}a \)
Step 2: Find b
\( b = \dfrac{35}{20}a - a = \dfrac{15}{20}a \)
Step 3: Write as a percentage
\( \dfrac{15}{20} \times 100 = 75\% \)
Step 4: Answer
The second number is 75% of the first number.""", trick=r"Sum = 35/20 of a → b = (35 − 20)/20 of a = 15/20 = 75%.")
S[57] = dict(raw=r"""Step 1: Work done in 1 hour
The pipe empties the full tank in 20 hours, so in 1 hour it empties \( \dfrac{1}{20} \) of the tank.
Step 2: Work done in 5 hours
\( 5 \times \dfrac{1}{20} = \dfrac{5}{20} \)
Step 3: Simplify
\( \dfrac{5}{20} = \dfrac{1}{4} \)
Step 4: Answer
In 5 hours it empties \( \dfrac{1}{4} \) of the tank.""", trick=r"Part done = time taken ÷ total time = 5/20.")
S[58] = dict(raw=r"""Step 1: One-day work
P + Q: \( \dfrac{1}{12} \); R: \( \dfrac{1}{18} \)
Step 2: Together in one day
\( \dfrac{1}{12} + \dfrac{1}{18} = \dfrac{3}{36} + \dfrac{2}{36} = \dfrac{5}{36} \)
Step 3: Time for the whole work
\( \dfrac{36}{5} = 7.2 \) days
Step 4: Time for one-third of the work
\( \dfrac{1}{3} \times 7.2 = 2.4 \) days""", trick=r"Take total work = LCM(12, 18) = 36 units: (P + Q) = 3/day, R = 2/day, together 5/day; 1/3 of 36 = 12 units → 12 ÷ 5 = 2.4 days.")
S[59] = dict(raw=r"""Step 1: Know the conversion
1 km/h \( = \dfrac{1000}{3600} = \dfrac{5}{18} \) m/s
Step 2: Multiply
\( 90 \times \dfrac{5}{18} \)
Step 3: Simplify
\( \dfrac{450}{18} = 25 \)
Step 4: Answer
The speed is 25 m/s.""", trick=r"km/h → m/s: multiply by 5/18; m/s → km/h: multiply by 18/5.")
S[60] = dict(raw=r"""Step 1: Moving towards each other, the speeds add
Relative speed = speed of G + speed of H
Step 2: Find the relative speed
\( \dfrac{390}{3} = 130 \) km/h
Step 3: Find H's speed
\( 130 - 80 = 50 \) km/h
Step 4: Check
In 3 hours G covers \( 80 \times 3 = 240 \) km and H covers \( 50 \times 3 = 150 \) km; \( 240 + 150 = 390 \) ✓""", trick=r"Opposite directions: time to meet = distance ÷ (sum of speeds).")
