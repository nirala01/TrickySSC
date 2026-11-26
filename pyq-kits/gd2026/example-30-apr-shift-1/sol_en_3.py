S = {}
S[41] = dict(raw=r"""Step 1: Bracket first
\( 29 + 19 = 48 \)
Step 2: Multiplication
\( 48 \times 2 = 96 \)
Step 3: Rewrite
\( 76 + 85 - 49 + 96 - 91 \)
Step 4: Left to right
\( 161 - 49 = 112,\; 112 + 96 = 208,\; 208 - 91 = 117 \)""", trick=r"BODMAS: bracket → × → + and − from the left.")
S[42] = dict(raw=r"""Step 1: Bracket ('of' means multiply)
\( 19 \text{ of } 2 = 19 \times 2 = 38 \)
Step 2: Division
\( 28 \div 4 = 7 \)
Step 3: Rewrite
\( 92 - 36 + 7 + 38 - 14 + 17 \)
Step 4: Left to right
\( 56 + 7 = 63,\; 63 + 38 = 101,\; 101 - 14 = 87,\; 87 + 17 = 104 \)""", trick=r"'of' = ×, and it is done before ÷, × outside.")
S[43] = dict(raw=r"""Step 1: Write as a fraction
\( 0.36 \div 0.00036 = \dfrac{0.36}{0.00036} \)
Step 2: Remove the decimals
Multiply top and bottom by 100000: \( \dfrac{36000}{36} \)
Step 3: Divide
\( 36000 \div 36 = 1000 \)
Step 4: Check
\( 0.00036 \times 1000 = 0.36 \) ✓""", trick=r"Same digits (36); decimal shift 2 → 5 places = 3 places → 1000.")
S[44] = dict(raw=r"""Step 1: Use the identity
\( (a + b)^{2} - (a - b)^{2} = 4ab \)
Step 2: Put a = 12.4 and b = 3.6
Numerator \( = 4 \times 12.4 \times 3.6 \)
Step 3: Divide by the denominator
\( \dfrac{4 \times 12.4 \times 3.6}{12.4 \times 3.6} = 4 \)
Step 4: Check by numbers
\( 16^{2} - 8.8^{2} = 256 - 77.44 = 178.56 \) and \( 12.4 \times 3.6 = 44.64 \); \( 178.56 \div 44.64 = 4 \) ✓""", trick=r"(a + b)² − (a − b)² = 4ab, so the answer is always 4.")
S[45] = dict(raw=r"""Step 1: Spot the identity
\( (a + b)^{3} = a^{3} + b^{3} + 3ab(a + b) \)
Step 2: Match the terms
a = 10, b = 6 and \( a + b = 16 \), so \( 3 \times 10 \times 6 \times 16 = 3ab(a + b) \).
Step 3: Apply
\( 10^{3} + 6^{3} + 3 \times 10 \times 6 \times 16 = (10 + 6)^{3} = 16^{3} \)
Step 4: Value
\( 16^{3} = 4096 \)""", trick=r"a³ + b³ + 3ab(a + b) = (a + b)³.")
S[46] = dict(raw=r"""Step 1: Formula
\( \text{Area of a rhombus} = \dfrac{d_{1} \times d_{2}}{2} \)
Step 2: Substitute
\( 54 = \dfrac{9 \times d_{2}}{2} \)
Step 3: Solve
\( d_{2} = \dfrac{54 \times 2}{9} = 12 \)
Step 4: Answer
The other diagonal is 12 cm.""", trick=r"Other diagonal = 2 × area ÷ known diagonal.")
S[47] = dict(raw=r"""Step 1: Use the area
\( \dfrac{d_{1} d_{2}}{2} = 24 \Rightarrow d_{1} d_{2} = 48 \)
Step 2: Find the squares
\( d_{1}^{2} + d_{2}^{2} = (d_{1} + d_{2})^{2} - 2 d_{1} d_{2} = 196 - 96 = 100 \)
Step 3: Side of the rhombus
The diagonals bisect at right angles, so \( \text{side} = \dfrac{\sqrt{d_{1}^{2} + d_{2}^{2}}}{2} = \dfrac{\sqrt{100}}{2} = 5 \)
Step 4: Check
The diagonals are 6 cm and 8 cm (sum 14, product 48); half-diagonals 3 and 4 give side 5 ✓""", trick=r"Half-diagonals 3 and 4 → side 5 (3-4-5 triangle).")
S[48] = dict(raw=r"""Step 1: Rule
\( \text{LCM}(A, B, C) = \text{LCM}(\text{LCM}(A, B), C) = \text{LCM}(40, 18) \)
Step 2: Prime factors
\( 40 = 2^{3} \times 5 \), \( 18 = 2 \times 3^{2} \)
Step 3: Highest powers
\( \text{LCM} = 2^{3} \times 3^{2} \times 5 \)
Step 4: Value
\( 8 \times 9 \times 5 = 360 \)""", trick=r"LCM of three = LCM of (LCM of two) with the third.")
S[49] = dict(raw=r"""Step 1: Rule
For two numbers, \( \text{HCF} \times \text{LCM} = \text{product of the numbers} \)
Step 2: Substitute
\( 15 \times 360 \)
Step 3: Multiply
\( 15 \times 360 = 5400 \)
Step 4: Example check
45 and 120 have HCF 15 and LCM 360, and \( 45 \times 120 = 5400 \) ✓""", trick=r"Product = HCF × LCM (two numbers only).")
S[50] = dict(raw=r"""Step 1: Take B = 100
A is 50 percent less, so \( A = 100 - 50 = 50 \).
Step 2: Excess of B over A
\( 100 - 50 = 50 \)
Step 3: Percentage on A
\( \dfrac{50}{50} \times 100 = 100\% \)
Step 4: Answer
B is 100 percent more than A.""", trick=r"Less by r% → more by \( \dfrac{r}{100 - r} \times 100 \) %.")
S[51] = dict(raw=r"""Step 1: Profit
\( 550 - 500 = 50 \) rupees
Step 2: Formula
\( \text{Profit \%} = \dfrac{\text{Profit}}{\text{CP}} \times 100 \)
Step 3: Substitute
\( \dfrac{50}{500} \times 100 = 10\% \)
Step 4: Answer
The profit is 10 percent.""", trick=r"Profit % is always on the cost price.")
S[52] = dict(raw=r"""Step 1: 25 percent of 500
\( \dfrac{25}{100} \times 500 = 125 \)
Step 2: Form the equation
125 is 25 percent more than A, so \( 1.25A = 125 \).
Step 3: Solve
\( A = \dfrac{125}{1.25} = 100 \)
Step 4: Check
25 percent more than 100 is 125 ✓""", trick=r"25% more = × \( \dfrac{5}{4} \), so divide by \( \dfrac{5}{4} \).")
S[53] = dict(raw=r"""Step 1: Take SP = 100
The loss is 30 percent of the SP, so loss = 30.
Step 2: Find CP
\( \text{CP} = \text{SP} + \text{loss} = 100 + 30 = 130 \)
Step 3: Loss percent on CP
\( \dfrac{30}{130} \times 100 = 23.08\% \) (approx.)
Step 4: Answer
The loss on the cost price is about 23.08 percent.""", trick=r"Loss r% on SP → loss on CP = \( \dfrac{r}{100 + r} \times 100 \) %.")
S[54] = dict(raw=r"""Step 1: One day's work
\( \dfrac{1}{18} + \dfrac{1}{27} + \dfrac{1}{36} = \dfrac{6 + 4 + 3}{108} = \dfrac{13}{108} \)
Step 2: Time for the whole work
\( \dfrac{108}{13} \) days
Step 3: Time for two-thirds of the work
\( \dfrac{2}{3} \times \dfrac{108}{13} = \dfrac{72}{13} \) days
Step 4: Answer
They need \( \dfrac{72}{13} \) days (about 5.5 days).""", trick=r"Use total work = LCM 108 units: rates 6, 4, 3 → 13 units a day; 72 units ÷ 13.")
S[55] = dict(raw=r"""Step 1: Work done in a day
A does \( \dfrac{1}{21} \) and B does \( \dfrac{1}{28} \) of the work per day.
Step 2: Ratio of their shares
They work for the same days, so wages are in the ratio \( \dfrac{1}{21} : \dfrac{1}{28} = 28 : 21 = 4 : 3 \).
Step 3: Shares
A gets \( \dfrac{4}{7} \times 4200 = 2400 \) and B gets \( \dfrac{3}{7} \times 4200 = 1800 \) rupees.
Step 4: Difference
\( 2400 - 1800 = 600 \) rupees""", trick=r"Same time together → wages in ratio of efficiency (inverse of days).")
S[56] = dict(raw=r"""Step 1: Time in hours
4 hours 30 minutes \( = 4.5 \) hours
Step 2: Distance
\( 8 \times 4.5 = 36 \) km
Step 3: Speed of the cycle
\( \dfrac{36}{4} = 9 \) km/hr
Step 4: Check
\( 9 \times 4 = 36 \) km ✓""", trick=r"Same distance → speed × time stays equal: 8 × 4.5 = s × 4.")
S[57] = dict(raw=r"""Step 1: Distance on the first bridge
\( 150 + 250 = 400 \) m (train length + bridge length)
Step 2: Speed
\( \dfrac{400}{8} = 50 \) m/s
Step 3: Distance on the second bridge
\( 150 + 500 = 650 \) m
Step 4: Time
\( \dfrac{650}{50} = 13 \) seconds""", trick=r"Crossing a bridge = train length + bridge length.")
S[58] = dict(raw=r"""Step 1: Take CP = 100
Loss is 30 percent, so \( \text{SP} = 70 \).
Step 2: Discount
\( \text{Discount} = \dfrac{7}{10} \times 70 = 49 \)
Step 3: Marked price
\( \text{MP} = \text{SP} + \text{Discount} = 70 + 49 = 119 \)
Step 4: CP as percent of MP
\( \dfrac{100}{119} \times 100 = 84.03\% \) (approx.)""", trick=r"MP = 1.7 × SP = 1.7 × 0.7 × CP = 1.19 CP.")
S[59] = dict(raw=r"""Step 1: Net price factor
\( (1 - 0.30)(1 - 0.20) = 0.7 \times 0.8 = 0.56 \)
Step 2: Price paid
\( 0.56 \times 500 = 280 \) rupees
Step 3: Net discount
\( 500 - 280 = 220 \) rupees
Step 4: Check with the formula
Single equivalent discount \( = 30 + 20 - \dfrac{30 \times 20}{100} = 44\% \), and 44 percent of 500 is ₹220 ✓""", trick=r"Two discounts a% and b% = \( a + b - \dfrac{ab}{100} \) %.")
S[60] = dict(raw=r"""Step 1: Formula
Net discount \( = a + b - \dfrac{ab}{100} \)
Step 2: Substitute a = 10, b = 30
\( 10 + 30 - \dfrac{10 \times 30}{100} \)
Step 3: Simplify
\( 40 - 3 = 37\% \)
Step 4: Check
Price factor \( 0.9 \times 0.7 = 0.63 \), so the discount is \( 1 - 0.63 = 0.37 = 37\% \) ✓""", trick=r"Successive discounts are not simply added (10 + 30 ≠ 40).")
