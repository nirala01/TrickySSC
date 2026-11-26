S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket
\( 41 + 23 = 64 \)
Step 2: Multiply
\( 64 \times 2 = 128 \)
Step 3: Add and subtract from left to right
\( 56 + 74 - 52 + 128 - 96 = 130 - 52 + 128 - 96 \)
Step 4: Finish
\( 78 + 128 - 96 = 206 - 96 = 110 \)""", trick=r"BODMAS: bracket → × → + and − left to right.")
S[42] = dict(raw=r"""Step 1: Solve the bracket
\( 96 \div 12 = 8 \)
Step 2: Solve "of"
\( 29 \text{ of } 2 = 29 \times 2 = 58 \)
Step 3: Rewrite the expression
\( 72 + 38 - 8 + 58 - 14 \)
Step 4: Add and subtract
\( 110 - 8 = 102,\; 102 + 58 = 160,\; 160 - 14 = 146 \)""", trick=r"“of” means multiply and is done before + and −.")
S[43] = dict(raw=r"""Step 1: Add the whole numbers
\( 7 + 9 - 5 = 11 \)
Step 2: Combine the fractions with LCD 84
\( \dfrac{2}{7} + \dfrac{1}{3} - \dfrac{3}{4} = \dfrac{24 + 28 - 63}{84} = -\dfrac{11}{84} \)
Step 3: Put them together
\( 11 - \dfrac{11}{84} \)
Step 4: Write as a mixed number
\( 10 + \dfrac{84 - 11}{84} = 10\dfrac{73}{84} \)""", trick=r"Whole parts first, then fractions; borrow 1 if the fraction part is negative.")
S[44] = dict(raw=r"""Step 1: Find the square roots
\( \sqrt{0.09} = 0.3 \) and \( \sqrt{0.36} = 0.6 \)
Step 2: Simplify each fraction
\( \dfrac{0.3}{0.6} = \dfrac{1}{2},\; \dfrac{0.4}{0.6} = \dfrac{2}{3},\; \dfrac{1.8}{0.6} = 3 \)
Step 3: Multiply
\( \dfrac{1}{2} \times \dfrac{2}{3} \times 3 = 1 \)
Step 4: Answer
The value is 1.""", trick=r"Square roots of 0.09 and 0.36 are 0.3 and 0.6.")
S[45] = dict(raw=r"""Step 1: Evaluate the square and products
\( 18^{2} = 324,\; 8 \times 8 = 64,\; 5 \times 22 = 110 \)
Step 2: Combine
\( 324 + 64 - 110 + 11 = 289 \)
Step 3: Take the square root
\( \sqrt{289} = 17 \)
Step 4: Check
\( 17 \times 17 = 289 \) ✓""", trick=r"Simplify fully inside the root before taking the square root.")
S[46] = dict(raw=r"""Step 1: Find the other diagonal
\( \text{Area} = \dfrac{d_{1} \times d_{2}}{2} \Rightarrow 216 = \dfrac{18 \times d_{2}}{2} \Rightarrow d_{2} = 24 \) cm
Step 2: Half-diagonals
\( 9 \) cm and \( 12 \) cm; the diagonals bisect each other at right angles.
Step 3: Side
\( \sqrt{9^{2} + 12^{2}} = \sqrt{81 + 144} = \sqrt{225} = 15 \) cm
Step 4: Perimeter
\( 4 \times 15 = 60 \) cm""", trick=r"Half-diagonals 9 and 12 form a 3-4-5 triangle → side 15.")
S[47] = dict(raw=r"""Step 1: Find the other diagonal
\( 384 = \dfrac{24 \times d_{2}}{2} \Rightarrow d_{2} = 32 \) cm
Step 2: Half-diagonals
\( 12 \) cm and \( 16 \) cm
Step 3: Side
\( \sqrt{12^{2} + 16^{2}} = \sqrt{144 + 256} = \sqrt{400} = 20 \) cm
Step 4: Perimeter
\( 4 \times 20 = 80 \) cm""", trick=r"12-16-20 is a 3-4-5 triangle scaled by 4.")
S[48] = dict(raw=r"""Step 1: Use the property of LCM
\( \text{LCM}(A, B, C, D) = \text{LCM}(\text{LCM}(A, B), \text{LCM}(C, D)) \)
Step 2: Substitute
\( \text{LCM}(20, 30) \)
Step 3: Prime factors
\( 20 = 2^{2} \times 5,\; 30 = 2 \times 3 \times 5 \Rightarrow \text{LCM} = 2^{2} \times 3 \times 5 \)
Step 4: Answer
\( 4 \times 3 \times 5 = 60 \)""", trick=r"LCM of group LCMs = overall LCM.")
S[49] = dict(raw=r"""Step 1: Key fact
The HCF of two numbers always divides their LCM.
Step 2: Divisors of 90
\( 90 = 2 \times 3^{2} \times 5 \); its divisors include 1, 2, 3, 5, 6, 9, 10, 15, 18, 30, 45, 90.
Step 3: Check the options
\( 90 \div 15 = 6 \) exactly; 28, 24 and 36 do not divide 90.
Step 4: Answer
Only 15 can be the HCF (for example, 15 and 90, or 30 and 45).""", trick=r"HCF must be a factor of the LCM.")
S[50] = dict(raw=r"""Step 1: Write the formula
\( \text{Profit} = \text{CP} \times \dfrac{\text{Profit}\%}{100} \)
Step 2: Substitute
\( 480 \times \dfrac{10}{100} \)
Step 3: Calculate
\( = 48 \)
Step 4: Answer
The profit is ₹48.""", trick=r"10% of a number = move the decimal one place left.")
S[51] = dict(raw=r"""Step 1: Write the equation
\( \dfrac{x}{100} \times x = 225 \)
Step 2: Simplify
\( x^{2} = 22500 \)
Step 3: Take the square root
\( x = \sqrt{22500} = 150 \)
Step 4: Check
\( 150\% \) of 150 = \( 1.5 \times 150 = 225 \) ✓""", trick=r"x% of x = x²/100.")
S[52] = dict(raw=r"""Step 1: Take SP = 100
Loss = 25% of SP = 25.
Step 2: Find CP
\( \text{CP} = \text{SP} + \text{Loss} = 100 + 25 = 125 \)
Step 3: Loss % on CP
\( \dfrac{25}{125} \times 100 = 20\% \)
Step 4: Answer
The loss on cost price is 20 percent.""", trick=r"Loss of 1/4 on SP = loss of 1/5 on CP.")
S[53] = dict(raw=r"""Step 1: Let Q's marks = 100k
Then \( P = 75k \) and \( R = 60k \).
Step 2: Use the total
\( 100k + 75k + 60k = 235k = 1410 \Rightarrow k = 6 \)
Step 3: Find Q and R
\( Q = 600,\; R = 360 \)
Step 4: Difference
\( 600 - 360 = 240 \)""", trick=r"Take Q = 100, so P = 75 and R = 60 → 235 parts in all.")
S[54] = dict(raw=r"""Step 1: One day's work of A, B and C
\( \dfrac{1}{18} \)
Step 2: One day's work of A and B
\( \dfrac{1}{24} \)
Step 3: C's one day's work
\( \dfrac{1}{18} - \dfrac{1}{24} = \dfrac{4 - 3}{72} = \dfrac{1}{72} \)
Step 4: Answer
C alone takes 72 days.""", trick=r"Product ÷ difference: (18 × 24) ÷ (24 − 18) = 72.")
S[55] = dict(raw=r"""Step 1: Efficiency ratio
\( \dfrac{1}{12} : \dfrac{1}{18} : \dfrac{1}{36} = 3 : 2 : 1 \) (multiply by 36)
Step 2: Value of one part
Wages are shared in the ratio of work done, so X's 3 parts = 4800, giving 1 part = 1600.
Step 3: Wages of Y and Z
\( Y = 2 \times 1600 = 3200,\; Z = 1600 \)
Step 4: Required difference
\( |(Y + Z) - (X + Z)| = |Y - X| = |3200 - 4800| = 1600 \)""", trick=r"Z cancels out: the difference is just |Y − X|.")
S[56] = dict(raw=r"""Step 1: Relative speed (same direction)
\( 75 - 25 = 50 \) km/hr
Step 2: Convert to m/s
\( 50 \times \dfrac{5}{18} = \dfrac{125}{9} \) m/s
Step 3: Distance to cover
\( 120 + 130 = 250 \) m
Step 4: Time
\( 250 \div \dfrac{125}{9} = 250 \times \dfrac{9}{125} = 18 \) seconds""", trick=r"Same direction → subtract speeds; distance = sum of lengths.")
S[57] = dict(raw=r"""Step 1: Speed of the boat in still water
\( \dfrac{25 + 15}{2} = 20 \) km/hr
Step 2: Speed of the stream
\( \dfrac{25 - 15}{2} = 5 \) km/hr
Step 3: Difference
\( 20 - 5 = 15 \) km/hr
Step 4: Shortcut check
Boat − stream = upstream speed = 15 km/hr ✓""", trick=r"Boat speed − stream speed = upstream speed.")
S[58] = dict(raw=r"""Step 1: Selling price
\( \text{SP} = 1000 \times \dfrac{150}{100} = 1500 \)
Step 2: Relation with MP
A 40% discount means \( \text{SP} = 60\% \) of MP.
Step 3: Marked price
\( \text{MP} = 1500 \times \dfrac{100}{60} = 2500 \)
Step 4: Answer
The marked price is ₹2500.""", trick=r"MP = SP ÷ (1 − discount).")
S[59] = dict(raw=r"""Step 1: Selling price in terms of CP
25% loss → \( \text{SP} = \dfrac{3}{4} \text{CP} \)
Step 2: Marked price in terms of SP
\( \text{MP} = \text{SP} + \dfrac{5}{9}\text{SP} = \dfrac{14}{9}\text{SP} \)
Step 3: Combine
\( \text{MP} = \dfrac{14}{9} \times \dfrac{3}{4}\text{CP} = \dfrac{42}{36}\text{CP} \)
Step 4: Simplify
\( \text{MP} = \dfrac{7}{6} \) of cost price""", trick=r"Chain the fractions: MP/SP × SP/CP.")
S[60] = dict(raw=r"""Step 1: Discount
\( 30\% \) of 1000 = 300
Step 2: Selling price
\( 1000 - 300 = 700 \)
Step 3: Profit
\( 700 - 520 = 180 \)
Step 4: Answer
The profit is ₹180.""", trick=r"SP = MP × 0.7; profit = SP − CP.")
