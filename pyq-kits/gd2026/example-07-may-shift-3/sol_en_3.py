S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket
\( 24 \times 1 = 24 \).
Step 2: Do the division
\( 44 \div 2 = 22 \).
Step 3: Rewrite the expression
\( 81 + 24 - 38 + 17 + 22 - 16 \).
Step 4: Add the plus terms and subtract the minus terms
Plus: \( 81 + 24 + 17 + 22 = 144 \). Minus: \( 38 + 16 = 54 \). Result: \( 144 - 54 = 90 \).""", trick=r"Bracket → ÷ → then all plus minus all minus.")
S[42] = dict(raw=r"""Step 1: Write the numbers using the HCF
Let the numbers be \( 24a \) and \( 24b \), where a and b have no common factor.
Step 2: Use the LCM
\( \text{LCM} = 24ab = 360 \Rightarrow ab = 15 \), so (a, b) = (5, 3) or (15, 1).
Step 3: Use the difference
\( 24(a - b) = 48 \Rightarrow a - b = 2 \), so a = 5 and b = 3.
Step 4: Find the numbers and check
\( 24 \times 5 = 120 \) and \( 24 \times 3 = 72 \); difference \( 120 - 72 = 48 \) ✓ and \( 120 \times 72 = 8640 = 24 \times 360 \) ✓.""", trick=r"Product of two numbers = HCF × LCM; then test the difference.")
S[43] = dict(raw=r"""Step 1: Solve the bracket from left to right
\( 11.85 - 5.45 = 6.40 \).
Step 2: Finish the bracket
\( 6.40 - 4.60 = 1.80 \).
Step 3: Subtract from 12.1
\( 12.1 - 1.8 = 10.3 \).
Step 4: Check
\( 10.3 + 1.8 = 12.1 \) ✓.""", trick=r"Clear the bracket first; line up the decimal points.")
S[44] = dict(raw=r"""Step 1: Recognise the pattern
\( (5.1)^{2} \times 5.1 = (5.1)^{3} \), so the expression is \( a^{3} - 3a^{2}b + 3ab^{2} - b^{3} \) with \( a = 5.1 \), \( b = 0.1 \).
Step 2: Use the identity
\( a^{3} - 3a^{2}b + 3ab^{2} - b^{3} = (a - b)^{3} \).
Step 3: Substitute
\( (5.1 - 0.1)^{3} = 5^{3} \).
Step 4: Evaluate
\( 5^{3} = 125 \).""", trick=r"Signs + − + − with 3a²b, 3ab² → (a − b)³.")
S[45] = dict(raw=r"""Step 1: Use the identity
\( (a + b)^{2} + (a - b)^{2} = 2(a^{2} + b^{2}) \).
Step 2: Put \( a = \sqrt{6} \), \( b = \sqrt{2} \)
\( a^{2} = 6 \) and \( b^{2} = 2 \).
Step 3: Substitute
\( 2(6 + 2) = 2 \times 8 \).
Step 4: Evaluate
\( 2 \times 8 = 16 \). (The 2ab terms cancel, so no surd is left.)""", trick=r"(a + b)² + (a − b)² = 2(a² + b²): just double the sum of squares.")
S[46] = dict(raw=r"""Step 1: Write the three consecutive even numbers
Let them be \( x - 2 \), \( x \) and \( x + 2 \).
Step 2: Form the equation
\( (x - 2) + x + (x + 2) = 3x = 54 \).
Step 3: Solve
\( x = 54 \div 3 = 18 \), so the numbers are 16, 18 and 20.
Step 4: Answer and check
The largest is 20; \( 16 + 18 + 20 = 54 \) ✓.""", trick=r"Middle number = sum ÷ 3; largest = middle + 2.")
S[47] = dict(raw=r"""Step 1: Spot the identity
\( a^{3} + b^{3} + 3ab(a + b) = (a + b)^{3} \).
Step 2: Match the numbers
Here \( a = 9 \), \( b = 7 \) and \( a + b = 16 \), so \( 3 \times 9 \times 7 \times 16 = 3ab(a + b) \).
Step 3: Apply the identity
The expression \( = (9 + 7)^{3} = 16^{3} \).
Step 4: Evaluate
\( 16^{3} = 16 \times 16 \times 16 = 256 \times 16 = 4096 \).""", trick=r"When the last factor equals a + b, the whole thing is (a + b)³.")
S[48] = dict(raw=r"""Step 1: Notice that y is the reciprocal of x
\( y = \dfrac{1}{x} \), so \( xy = 1 \).
Step 2: Find \( x + y \)
\( x + y = \dfrac{(2 + \sqrt{6})^{2} + (2 - \sqrt{6})^{2}}{(2 - \sqrt{6})(2 + \sqrt{6})} = \dfrac{2(4 + 6)}{4 - 6} = \dfrac{20}{-2} = -10 \).
Step 3: Use the identity
\( x^{2} + y^{2} = (x + y)^{2} - 2xy \).
Step 4: Evaluate
\( (-10)^{2} - 2 \times 1 = 100 - 2 = 98 \).""", trick=r"If y = 1/x: x² + y² = (x + y)² − 2.")
S[49] = dict(raw=r"""Step 1: Use Pythagoras in the rectangle
\( \text{diagonal}^{2} = \text{length}^{2} + \text{breadth}^{2} \).
Step 2: Substitute
\( 13^{2} = 12^{2} + b^{2} \Rightarrow 169 = 144 + b^{2} \).
Step 3: Solve
\( b^{2} = 169 - 144 = 25 \Rightarrow b = 5 \).
Step 4: Answer
The breadth is 5 cm (5, 12, 13 is a Pythagorean triplet).""", trick=r"Remember the triplet 5, 12, 13.")
S[50] = dict(raw=r"""Step 1: Find the squares
\( 25^{2} = 625 \) and \( 15^{2} = 225 \).
Step 2: Solve the bracket
\( 625 + 225 - 450 = 400 \).
Step 3: Multiply
\( 40 \times 400 = 16000 \).
Step 4: Check
\( 16000 \div 40 = 400 \) ✓.""", trick=r"Bracket first: 625 + 225 − 450 = 400.")
S[51] = dict(raw=r"""Step 1: Write the two averages
Average of l and m \( = \dfrac{l + m}{2} \); average of m and n \( = \dfrac{m + n}{2} \).
Step 2: Write the difference
\( \dfrac{l + m}{2} - \dfrac{m + n}{2} = 17 \).
Step 3: Simplify
\( \dfrac{l - n}{2} = 17 \) (m cancels).
Step 4: Solve
\( l - n = 34 \).""", trick=r"The common term cancels: difference of numbers = 2 × difference of averages.")
S[52] = dict(raw=r"""Step 1: Find the failed percentage
\( 100\% - 30\% = 70\% \) failed.
Step 2: Find the total
\( 70\% \) of total \( = 42000 \Rightarrow \) total \( = \dfrac{42000 \times 100}{70} = 60000 \).
Step 3: Find the passed students
\( 30\% \) of \( 60000 = 18000 \).
Step 4: Check
\( 18000 + 42000 = 60000 \) ✓.""", trick=r"70% → 42000, so 10% → 6000 and 30% → 18000.")
S[53] = dict(raw=r"""Step 1: Take a simple cost price
Let CP = ₹100, so SP = ₹130 (30% profit).
Step 2: Increase both by 40%
New CP \( = 100 \times 1.4 = 140 \); new SP \( = 130 \times 1.4 = 182 \).
Step 3: Find the new profit
\( 182 - 140 = 42 \).
Step 4: Find the profit percentage
\( \dfrac{42}{140} \times 100 = 30\% \). Raising CP and SP by the same percentage leaves the profit percentage unchanged.""", trick=r"Same % change on CP and SP → profit % stays the same.")
S[54] = dict(raw=r"""Step 1: Let the total be x
He sells \( 60\% \) of x, so \( 40\% \) of x remains.
Step 2: Find the spoilt fruits in terms of x
\( 30\% \) of \( 40\% \) of x \( = 0.3 \times 0.4x = 0.12x \).
Step 3: Use the given number
\( 0.12x = 48 \Rightarrow x = \dfrac{48}{0.12} = 400 \).
Step 4: Find the fruits sold on the first day
\( 60\% \) of \( 400 = 240 \).""", trick=r"Spoilt = 30% of 40% = 12% of the total.")
S[55] = dict(raw=r"""Step 1: Take a simple selling price
Let SP = ₹100, so profit = 25% of SP = ₹25.
Step 2: Find the cost price
\( \text{CP} = 100 - 25 = 75 \).
Step 3: Find the profit on CP
\( \dfrac{25}{75} \times 100 \).
Step 4: Evaluate
\( = 33.33\% \) (that is, \( 33\dfrac{1}{3}\% \)).""", trick=r"Profit on SP = 1/4 → profit on CP = 1/3.")
S[56] = dict(raw=r"""Step 1: Find the food left after 6 days
Food was for 900 men for 60 days; after 6 days it is enough for 900 men for \( 60 - 6 = 54 \) days.
Step 2: Find the men left
\( 900 - 300 = 600 \) men.
Step 3: Equate man-days
\( 900 \times 54 = 600 \times d \).
Step 4: Solve
\( d = \dfrac{900 \times 54}{600} = 81 \) days.""", trick=r"Men × days stays constant for the same food.")
S[57] = dict(raw=r"""Step 1: Find B's time
A takes twice as long as B, so B takes \( 60 \div 2 = 30 \) days.
Step 2: Find C's time
A and B together: \( \dfrac{1}{60} + \dfrac{1}{30} = \dfrac{3}{60} = \dfrac{1}{20} \), so 20 days; C also takes 20 days.
Step 3: Add the one-day work of all three
\( \dfrac{1}{60} + \dfrac{1}{30} + \dfrac{1}{20} = \dfrac{1 + 2 + 3}{60} = \dfrac{6}{60} = \dfrac{1}{10} \).
Step 4: Answer
A, B and C together finish the work in 10 days.""", trick=r"Use LCM 60 as total work: A 1, B 2, C 3 units/day → 60 ÷ 6 = 10.")
S[58] = dict(raw=r"""Step 1: Recall the conversion
\( 1 \text{ km/hr} = \dfrac{5}{18} \text{ m/s} \).
Step 2: Multiply
\( 270 \times \dfrac{5}{18} \).
Step 3: Simplify
\( \dfrac{270}{18} = 15 \), so \( 15 \times 5 = 75 \).
Step 4: Answer
The speed is 75 m/s.""", trick=r"km/hr → m/s: × 5/18.")
S[59] = dict(raw=r"""Step 1: Let the speed be v
Crossing a man, the train covers its own length: \( L = 5v \).
Step 2: Crossing the platform
It covers train + platform: \( L + y = 12v \).
Step 3: Form the ratio
\( \dfrac{L}{L + y} = \dfrac{5v}{12v} = \dfrac{5}{12} \).
Step 4: Answer
The ratio is \( 5 : 12 \).""", trick=r"Same speed → the distances are in the same ratio as the times, 5 to 12.")
S[60] = dict(raw=r"""Step 1: Write Y in terms of X
After a 20% discount, \( Y = 0.8X \).
Step 2: Write Z in terms of Y
Z is 20% more than Y: \( Z = 1.2Y \).
Step 3: Combine
\( Z = 1.2 \times 0.8X = 0.96X \).
Step 4: Find the ratio
\( Z : X = 0.96 : 1 = 96 : 100 = 24 : 25 \).""", trick=r"−20% then +20% = 0.8 × 1.2 = 0.96 = 24/25.")
