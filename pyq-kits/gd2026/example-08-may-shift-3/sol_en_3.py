S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket
\( 25 + 19 = 44 \).
Step 2: Multiply
\( 44 \times 2 = 88 \).
Step 3: Rewrite the expression
\( 71 + 56 - 88 + 92 - 38 \).
Step 4: Add and subtract from left to right
\( 71 + 56 = 127 \), \( 127 - 88 = 39 \), \( 39 + 92 = 131 \), \( 131 - 38 = 93 \).""", trick=r"BODMAS: bracket, then ×, then + and − from left to right.")
S[42] = dict(raw=r"""Step 1: Solve "of" first
\( 27 \text{ of } 2 = 27 \times 2 = 54 \) and \( 18 \text{ of } 2 = 18 \times 2 = 36 \).
Step 2: Solve the division
\( 44 \div 4 = 11 \).
Step 3: Rewrite the expression
\( 89 + 33 - 54 + 11 + 36 - 36 \).
Step 4: Add and subtract from left to right
\( 89 + 33 = 122 \), \( 122 - 54 = 68 \), \( 68 + 11 = 79 \), \( 79 + 36 - 36 = 79 \).""", trick=r"'of' means multiply and is done before ÷, + and −.")
S[43] = dict(raw=r"""Step 1: Write the numbers using the HCF
Let the numbers be \( 13a \) and \( 13b \), where a and b have no common factor.
Step 2: Use the sum
\( 13a + 13b = 156 \Rightarrow a + b = 12 \).
Step 3: Use the LCM
LCM \( = 13ab = 455 \Rightarrow ab = 35 \). Two numbers with sum 12 and product 35 are 5 and 7.
Step 4: Find the numbers
\( 13 \times 5 = 65 \) and \( 13 \times 7 = 91 \). Check: \( 65 + 91 = 156 \) ✓.""", trick=r"Numbers = HCF × co-primes; LCM = HCF × their product.")
S[44] = dict(raw=r"""Step 1: First bracket
\( \sqrt{0.0169} = 0.13 \), so \( \dfrac{0.13}{1.3} = 0.1 \).
Step 2: Second bracket
\( \sqrt{3.24} = 1.8 \), so \( \dfrac{0.18}{1.8} = 0.1 \).
Step 3: Third bracket
\( \sqrt{0.0576} = 0.24 \), so \( \dfrac{0.24}{0.24} = 1 \).
Step 4: Multiply
\( 0.1 \times 0.1 \times 1 = 0.01 \).""", trick=r"Square root of a decimal: the number of decimal places halves (0.0169 → 0.13).")
S[45] = dict(raw=r"""Step 1: Find each square root
\( \sqrt{169} = 13 \), \( \sqrt{81} = 9 \), \( \sqrt{121} = 11 \).
Step 2: Multiply the first two
\( 13 \times 9 = 117 \).
Step 3: Multiply by the third
\( 117 \times 11 = 1287 \).
Step 4: Answer
\( x = 1287 \).""", trick=r"Multiply by 11 quickly: 117 → 1 | 1+1 | 1+7 | 7 = 1287.")
S[46] = dict(raw=r"""Step 1: Write the area formula
Area = length × breadth.
Step 2: Find the breadth
\( 54 = 9 \times b \Rightarrow b = \dfrac{54}{9} = 6 \) cm.
Step 3: Form the ratio
Ratio of length to breadth = \( 9 : 6 \).
Step 4: Simplify
Divide both by 3: \( 3 : 2 \).""", trick=r"Breadth = area ÷ length, then cancel the common factor.")
S[47] = dict(raw=r"""Step 1: Take the smallest 4-digit number
The smallest 4-digit number is 1000.
Step 2: Divide by 17
\( 17 \times 58 = 986 \), so 1000 leaves a remainder of \( 1000 - 986 = 14 \).
Step 3: Add the shortfall
\( 1000 + (17 - 14) = 1003 \).
Step 4: Check
\( 17 \times 59 = 1003 \) ✓. The answer is 1003.""", trick=r"Smallest n-digit multiple = smallest n-digit number + (divisor − remainder).")
S[48] = dict(raw=r"""Step 1: Use the identity
\( a^{2} - b^{2} = (a - b)(a + b) \).
Step 2: Find a − b and a + b
\( 3.452 - 2.948 = 0.504 \) and \( 3.452 + 2.948 = 6.4 \).
Step 3: Substitute
\( \dfrac{0.504 \times 6.4}{0.504} \).
Step 4: Cancel
The 0.504 cancels, leaving 6.4.""", trick=r"When the divisor equals a − b, the answer is a + b.")
S[49] = dict(raw=r"""Step 1: Use the perimeter
\( 2(l + b) = 60 \Rightarrow l + b = 30 \).
Step 2: Use the condition l = 4b
\( 4b + b = 30 \Rightarrow b = 6 \) cm and \( l = 24 \) cm.
Step 3: Find the diagonal
Diagonal \( = \sqrt{24^{2} + 6^{2}} = \sqrt{576 + 36} = \sqrt{612} \).
Step 4: Simplify
\( 612 = 36 \times 17 \), so \( \sqrt{612} = 6\sqrt{17} \) cm.""", trick=r"Diagonal of a rectangle = √(l² + b²).")
S[50] = dict(raw=r"""Step 1: Find the totals
A + B + C = \( 30 \times 3 = 90 \), A + B = \( 34 \times 2 = 68 \), B + C = \( 28 \times 2 = 56 \).
Step 2: Find C
C = \( 90 - 68 = 22 \) kg.
Step 3: Find B
B = \( 56 - 22 = 34 \) kg.
Step 4: Check
A = \( 68 - 34 = 34 \); \( 34 + 34 + 22 = 90 \) ✓. B weighs 34 kg.""", trick=r"B = (A+B) + (B+C) − (A+B+C) = 68 + 56 − 90 = 34.")
S[51] = dict(raw=r"""Step 1: Old total
\( 8 \times 30 = 240 \).
Step 2: New total
\( 8 \times 42 = 336 \).
Step 3: Find the increase
\( 336 - 240 = 96 \). The new number is 96 more than 20.
Step 4: New number
\( 20 + 96 = 116 \).""", trick=r"New number = old number + (rise in average × count) = 20 + 12 × 8.")
S[52] = dict(raw=r"""Step 1: Write the numbers using the ratio
Let the numbers be \( 3k \) and \( 7k \).
Step 2: Use the HCF
3 and 7 have no common factor, so the HCF of \( 3k \) and \( 7k \) is k. So \( k = 5 \).
Step 3: Find the numbers
\( 3 \times 5 = 15 \) and \( 7 \times 5 = 35 \).
Step 4: Check
The ratio of 15 and 35 is \( 3 : 7 \) and their HCF is 5 ✓.""", trick=r"Numbers = HCF × the ratio terms (when the ratio is in lowest terms).")
S[53] = dict(raw=r"""Step 1: Let the mixture be M kg
18% of M is element A.
Step 2: Form the equation
\( \dfrac{18}{100} \times M = 90 \).
Step 3: Solve
\( M = \dfrac{90 \times 100}{18} = 500 \).
Step 4: Answer
500 kg of mixture is needed.""", trick=r"Whole = part × 100 ÷ percentage.")
S[54] = dict(raw=r"""Step 1: Recall the formula
Profit % = \( \dfrac{\text{Profit}}{\text{CP}} \times 100 \).
Step 2: Substitute
\( 20 = \dfrac{50}{\text{CP}} \times 100 \).
Step 3: Solve
\( \text{CP} = \dfrac{50 \times 100}{20} = 250 \).
Step 4: Answer
The cost price is ₹250.""", trick=r"20% profit = ₹50 → 100% = ₹250.")
S[55] = dict(raw=r"""Step 1: Take CP = 100
At 60% profit, SP = 160.
Step 2: New cost price
CP rises by 30%: new CP = 130.
Step 3: New selling price for 40% profit
New SP = \( 130 \times \dfrac{140}{100} = 182 \).
Step 4: Find y
SP rises from 160 to 182, i.e. by 22: \( y = \dfrac{22}{160} \times 100 = 13.75 \).""", trick=r"Take CP = 100 and track both prices separately.")
S[56] = dict(raw=r"""Step 1: Take income = 100
Expenditure = 50 and saving = 50.
Step 2: New income and saving
Income rises 40% to 140; saving rises 20% to \( 50 \times 1.2 = 60 \).
Step 3: New expenditure
\( 140 - 60 = 80 \).
Step 4: Percentage increase
\( \dfrac{80 - 50}{50} \times 100 = 60 \) percent.""", trick=r"Expenditure = income − saving; work with income = 100.")
S[57] = dict(raw=r"""Step 1: Write what is given
\( \dfrac{1}{3} \) of the tank is emptied in 45 minutes.
Step 2: Scale up to the full tank
The full tank is 3 times that part.
Step 3: Multiply
\( 45 \times 3 = 135 \) minutes.
Step 4: Answer
The pipe empties the full tank in 135 minutes.""", trick=r"Full time = part time ÷ fraction = 45 ÷ 1/3.")
S[58] = dict(raw=r"""Step 1: Find the one-day work of each person
1 man: \( \dfrac{1}{6 \times 18} = \dfrac{1}{108} \); 1 woman: \( \dfrac{1}{8 \times 12} = \dfrac{1}{96} \); 1 boy: \( \dfrac{1}{5 \times 20} = \dfrac{1}{100} \).
Step 2: One-day work of the group
10 boys: \( \dfrac{10}{100} = \dfrac{1}{10} \); 12 men: \( \dfrac{12}{108} = \dfrac{1}{9} \); 16 women: \( \dfrac{16}{96} = \dfrac{1}{6} \).
Step 3: Add
\( \dfrac{1}{10} + \dfrac{1}{9} + \dfrac{1}{6} = \dfrac{9 + 10 + 15}{90} = \dfrac{34}{90} = \dfrac{17}{45} \).
Step 4: Find the days
Days \( = \dfrac{45}{17} \).""", trick=r"Convert each group to one-day work, add, then take the reciprocal.")
S[59] = dict(raw=r"""Step 1: Note the distance
To cross each other, the trains together cover the sum of their lengths: 600 m.
Step 2: Note the speed
In opposite directions the relative speed is the sum of the speeds: 40 m/s.
Step 3: Use time = distance ÷ speed
\( \dfrac{600}{40} = 15 \).
Step 4: Answer
The trains cross each other in 15 seconds.""", trick=r"Opposite directions: add the speeds; distance = sum of the lengths.")
S[60] = dict(raw=r"""Step 1: Note the time
A and B start at the same time and meet at S, so both travel for the same time.
Step 2: Recall the rule
For equal times, distance is proportional to speed.
Step 3: Form the ratio
Ratio of A's distance to B's distance = \( 50 : 30 \).
Step 4: Simplify
\( 50 : 30 = 5 : 3 \).""", trick=r"Same time → distances in the ratio of speeds.")
