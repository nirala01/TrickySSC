S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first
\( 29 + 15 = 44 \).
Step 2: Multiply
\( 44 \times 2 = 88 \).
Step 3: Rewrite the expression
\( 66 + 48 - 88 + 84 - 33 \).
Step 4: Add and subtract from left to right
\( 114 - 88 = 26 \), \( 26 + 84 = 110 \), \( 110 - 33 = 77 \).""", trick=r"BODMAS: bracket, then ×, then + and − from the left.")
S[42] = dict(raw=r"""Step 1: Solve "of" and the bracket
"of" means multiplication: \( 18 \text{ of } 2 = 18 \times 2 = 36 \).
Step 2: Multiply
\( 31 \times 1 = 31 \).
Step 3: Rewrite the expression
\( 89 - 42 + 31 + 36 + 27 - 19 \).
Step 4: Add and subtract from left to right
\( 47 + 31 = 78 \), \( 78 + 36 = 114 \), \( 114 + 27 = 141 \), \( 141 - 19 = 122 \).""", trick=r"In BODMAS, 'of' means × and is done before + and −.")
S[43] = dict(raw=r"""Step 1: Find the cube
\( (4.5)^{3} = 4.5 \times 4.5 \times 4.5 = 91.125 \).
Step 2: Work out the numerator
\( 8 \times 91.125 - 1 = 729 - 1 = 728 \).
Step 3: Work out the denominator
\( (10)^{2} - 9 = 100 - 9 = 91 \).
Step 4: Divide
\( \dfrac{728}{91} = 8 \).""", trick=r"8 × 4.5³ = 9³ = 729, so the top is 728 = 8 × 91.")
S[44] = dict(raw=r"""Step 1: Find the square root of 2025
\( \sqrt{2025} = 45 \), because \( 45 \times 45 = 2025 \).
Step 2: Simplify the right side
\( \sqrt{x} = \dfrac{100}{45} = \dfrac{20}{9} \).
Step 3: Square both sides
\( x = \left( \dfrac{20}{9} \right)^{2} \).
Step 4: Answer
\( x = \dfrac{400}{81} \).""", trick=r"√2025 = 45; square 20/9 to get 400/81.")
S[45] = dict(raw=r"""Step 1: Rationalise the fraction
Multiply the top and bottom by \( \sqrt{6} + \sqrt{2} \): \( \dfrac{1}{\sqrt{6} - \sqrt{2}} = \dfrac{\sqrt{6} + \sqrt{2}}{6 - 2} \).
Step 2: Simplify
\( \dfrac{1}{\sqrt{6} - \sqrt{2}} = \dfrac{\sqrt{6} + \sqrt{2}}{4} \).
Step 3: Add the two terms
\( (\sqrt{6} + \sqrt{2}) + \dfrac{1}{4}(\sqrt{6} + \sqrt{2}) = \left( 1 + \dfrac{1}{4} \right)(\sqrt{6} + \sqrt{2}) \).
Step 4: Answer
The value is \( \dfrac{5}{4}(\sqrt{6} + \sqrt{2}) \).""", trick=r"(√a − √b)(√a + √b) = a − b = 4, so 1/(√6 − √2) = (√6 + √2)/4.")
S[46] = dict(raw=r"""Step 1: Use the formula
Diagonal of a square = side \( \times \sqrt{2} \).
Step 2: Why it works
By Pythagoras, diagonal \( = \sqrt{10^{2} + 10^{2}} = \sqrt{200} \).
Step 3: Simplify
\( \sqrt{200} = \sqrt{100 \times 2} = 10\sqrt{2} \).
Step 4: Answer
The diagonal is \( 10\sqrt{2} \) cm.""", trick=r"Square's diagonal = a√2.")
S[47] = dict(raw=r"""Step 1: Use the rule of 3
A number is divisible by 3 if the sum of its digits is divisible by 3.
Step 2: Add the known digits
\( 9 + 5 + 9 = 23 \), so the digit sum is \( 23 + P \).
Step 3: Find possible values of P
\( 23 + P \) must be 24, 27 or 30, so P = 1, 4 or 7.
Step 4: Match with the options
Only 7 is among the options: \( 23 + 7 = 30 \), which is divisible by 3 ✓.""", trick=r"Digit sum 23 + P must be a multiple of 3 → P = 1, 4, 7.")
S[48] = dict(raw=r"""Step 1: Use Pythagoras
\( \text{diagonal}^{2} = \text{length}^{2} + \text{breadth}^{2} \).
Step 2: Put in the values
\( 15^{2} = 9^{2} + b^{2} \Rightarrow 225 = 81 + b^{2} \).
Step 3: Find the breadth
\( b^{2} = 144 \Rightarrow b = 12 \) cm.
Step 4: Find the ratio
Length to breadth = \( 9 : 12 = 3 : 4 \).""", trick=r"9, 12, 15 is the 3, 4, 5 triple × 3.")
S[49] = dict(raw=r"""Step 1: Spot the identity
\( (a + b)^{2} - 4ab = (a - b)^{2} \).
Step 2: Identify a and b
Here \( a = 460 \) and \( b = 240 \).
Step 3: Find a − b
\( 460 - 240 = 220 \).
Step 4: Square it
\( 220^{2} = 48400 \).""", trick=r"(a + b)² − 4ab = (a − b)² = 220².")
S[50] = dict(raw=r"""Step 1: Find the total age of 28 boys
\( 28 \times 19 = 532 \) years.
Step 2: Find the total after two boys leave
26 boys remain with the same average 19: \( 26 \times 19 = 494 \) years.
Step 3: Find the total of the two boys who left
\( 532 - 494 = 38 \) years, so \( x + 21 = 38 \).
Step 4: Answer
\( x = 38 - 21 = 17 \).""", trick=r"Average unchanged → the two leavers average 19 too: x + 21 = 38.")
S[51] = dict(raw=r"""Step 1: Write the prime factors
\( 5 = 5 \), \( 7 = 7 \), \( 9 = 3^{2} \), \( 21 = 3 \times 7 \).
Step 2: Take the highest power of each prime
\( 3^{2} \), 5 and 7.
Step 3: Multiply
LCM \( = 9 \times 5 \times 7 = 315 \).
Step 4: Check
\( 315 \div 5 = 63 \), \( 315 \div 7 = 45 \), \( 315 \div 9 = 35 \), \( 315 \div 21 = 15 \) ✓.""", trick=r"Least number divisible by all = LCM = 9 × 5 × 7.")
S[52] = dict(raw=r"""Step 1: Use the same-remainder rule
The required number is the HCF of the differences of the numbers.
Step 2: Find the differences
\( 50 - 38 = 12 \), \( 74 - 50 = 24 \), \( 98 - 74 = 24 \).
Step 3: Find the HCF
HCF of 12, 24 and 24 = 12.
Step 4: Check
\( 38 = 3 \times 12 + 2 \), \( 50 = 4 \times 12 + 2 \), \( 74 = 6 \times 12 + 2 \), \( 98 = 8 \times 12 + 2 \): remainder 2 each time ✓.""", trick=r"Same remainder → HCF of the differences.")
S[53] = dict(raw=r"""Step 1: Identify the profit
The difference between SP and CP is the profit: ₹385.
Step 2: Write the equation
Profit = 7% of CP, so \( \dfrac{7}{100} \times \text{CP} = 385 \).
Step 3: Solve
\( \text{CP} = \dfrac{385 \times 100}{7} = 55 \times 100 = 5500 \).
Step 4: Answer
The cost price is ₹5500 (check: 7% of 5500 = 385 ✓).""", trick=r"7% of CP = ₹385 → 1% = ₹55 → CP = ₹5500.")
S[54] = dict(raw=r"""Step 1: Write the equation
\( \dfrac{70}{100} \times \dfrac{60}{100} \times N = 420 \).
Step 2: Simplify
\( 0.42N = 420 \).
Step 3: Find the number
\( N = \dfrac{420}{0.42} = 1000 \).
Step 4: Find 10% of it
\( \dfrac{10}{100} \times 1000 = 100 \).""", trick=r"70% of 60% = 42%; 42% = 420 → 100% = 1000.")
S[55] = dict(raw=r"""Step 1: Find the cost price
CP = SP + loss = \( 2300 + 200 = 2500 \) (₹).
Step 2: Write the formula
Loss% = \( \dfrac{\text{Loss}}{\text{CP}} \times 100 \).
Step 3: Put in the values
\( \dfrac{200}{2500} \times 100 = 8 \).
Step 4: Answer
The loss is 8%.""", trick=r"Loss% is always on CP: 200 out of 2500.")
S[56] = dict(raw=r"""Step 1: Take income = 100
Expenditure = 70 and saving = 30.
Step 2: Apply the increases
New income = \( 100 \times 1.3 = 130 \); new saving = \( 30 \times 1.4 = 42 \).
Step 3: Find the new expenditure
\( 130 - 42 = 88 \), so the expenditure rises by \( 88 - 70 = 18 \).
Step 4: Find the percentage increase
\( \dfrac{18}{70} \times 100 \approx 25.71\% \).""", trick=r"Income = expenditure + saving; take income 100.")
S[57] = dict(raw=r"""Step 1: Set the efficiencies
B does 1 unit of work per day, so A does 6 units per day.
Step 2: Find the total work
Together they do \( 6 + 1 = 7 \) units per day for 18 days: \( 7 \times 18 = 126 \) units.
Step 3: Find B's time
B alone does 1 unit per day, so B needs \( \dfrac{126}{1} = 126 \) days.
Step 4: Check
A alone would need \( \dfrac{126}{6} = 21 \) days, and \( \dfrac{1}{21} + \dfrac{1}{126} = \dfrac{7}{126} = \dfrac{1}{18} \) ✓.""", trick=r"Efficiency 6 to 1 → total 7 units × 18 days; B does 1 unit a day.")
S[58] = dict(raw=r"""Step 1: Use the work formula
\( M_{1} \times D_{1} \times H_{1} = M_{2} \times D_{2} \times H_{2} \) for the same work.
Step 2: Put in the values
\( 50 \times 30 \times 6 = M_{2} \times 45 \times 4 \).
Step 3: Simplify
\( 9000 = 180 M_{2} \).
Step 4: Answer
\( M_{2} = \dfrac{9000}{180} = 50 \) men.""", trick=r"Man-hours stay the same: 30 × 6 = 180 = 45 × 4, so the men stay 50.")
S[59] = dict(raw=r"""Step 1: Find the distance to be covered
When two trains cross each other, the distance is the sum of their lengths: \( 300 + 500 = 800 \) m.
Step 2: Find the relative speed
\( \dfrac{800}{10} = 80 \) m/s.
Step 3: Use opposite directions
In opposite directions the speeds add: \( 20 + v = 80 \).
Step 4: Answer
\( v = 60 \) m/s.""", trick=r"Opposite directions: add speeds; distance = sum of lengths.")
S[60] = dict(raw=r"""Step 1: Find the original speed
72 minutes = \( \dfrac{72}{60} = 1.2 \) hours, so speed = \( \dfrac{48}{1.2} = 40 \) km/hr.
Step 2: Find the new speed
\( 40 - 10 = 30 \) km/hr.
Step 3: Find the new time in hours
\( \dfrac{48}{30} = 1.6 \) hours.
Step 4: Convert to minutes
\( 1.6 \times 60 = 96 \) minutes.""", trick=r"Same distance: time ∝ 1/speed → 72 × 40/30 = 96.")
