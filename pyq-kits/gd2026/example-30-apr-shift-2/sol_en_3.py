S = {}
S[41] = dict(raw=r"""Step 1: Bracket first
\( 45 + 19 = 64 \)
Step 2: Multiplication
\( 26 \times 2 = 52 \)
Step 3: Rewrite
\( 64 - 37 + 52 - 13 \)
Step 4: Left to right
\( 64 - 37 = 27,\; 27 + 52 = 79,\; 79 - 13 = 66 \)""", trick=r"BODMAS: bracket → × → + and − from the left.")
S[42] = dict(raw=r"""Step 1: Bracket ('of' means multiply)
\( 18 \text{ of } 1 = 18 \times 1 = 18 \)
Step 2: Division
\( 33 \div 3 = 11 \)
Step 3: Rewrite
\( 94 - 38 + 28 + 11 + 21 - 18 \)
Step 4: Left to right
\( 56 + 28 = 84,\; 84 + 11 = 95,\; 95 + 21 = 116,\; 116 - 18 = 98 \)""", trick=r"Bracket ('of') → ÷ → then add and subtract from the left.")
S[43] = dict(raw=r"""Step 1: Convert to decimals
\( \dfrac{5}{6} \approx 0.833 \)
Step 2: Convert the options
\( \dfrac{3}{4} = 0.75,\; \dfrac{2}{3} \approx 0.667,\; \dfrac{10}{11} \approx 0.909,\; \dfrac{4}{5} = 0.8 \)
Step 3: Compare
Only \( 0.909 > 0.833 \).
Step 4: Cross-check
\( \dfrac{10}{11} \) vs \( \dfrac{5}{6} \): \( 10 \times 6 = 60 > 5 \times 11 = 55 \), so \( \dfrac{10}{11} > \dfrac{5}{6} \) ✓""", trick=r"For fractions of the form n/(n+1), the bigger n, the bigger the fraction: 10/11 > 5/6 > 4/5 > 3/4 > 2/3.")
S[44] = dict(raw=r"""Step 1: Cube root
\( 0.512 = \dfrac{512}{1000} \) and \( 8^{3} = 512,\; 10^{3} = 1000 \), so \( \sqrt[3]{0.512} = 0.8 \)
Step 2: Square root
\( 2.25 = \dfrac{225}{100} \), so \( \sqrt{2.25} = \dfrac{15}{10} = 1.5 \)
Step 3: Multiply
\( 0.8 \times 1.5 = 1.2 \)
Step 4: Check
\( 0.8^{3} = 0.512 \) and \( 1.5^{2} = 2.25 \) ✓""", trick=r"0.512 → 0.8 (8³ = 512); 2.25 → 1.5 (15² = 225).")
S[45] = dict(raw=r"""Step 1: Area gives the product of diagonals
\( \dfrac{d_1 d_2}{2} = 720 \Rightarrow d_1 d_2 = 1440 \)
Step 2: Side gives the sum of squares
The diagonals bisect at right angles: \( \left(\dfrac{d_1}{2}\right)^{2} + \left(\dfrac{d_2}{2}\right)^{2} = 41^{2} \Rightarrow d_1^{2} + d_2^{2} = 4 \times 1681 = 6724 \)
Step 3: Square of the sum
\( (d_1 + d_2)^{2} = 6724 + 2 \times 1440 = 9604 \)
Step 4: Sum
\( d_1 + d_2 = \sqrt{9604} = 98 \) cm (the diagonals are 80 cm and 18 cm).""", trick=r"(d₁ + d₂)² = 4a² + 4 × Area.")
S[46] = dict(raw=r"""Step 1: Property
Adjacent angles of a parallelogram are supplementary: they add up to \( 180^{\circ} \).
Step 2: Write the equation
\( 45^{\circ} + x = 180^{\circ} \)
Step 3: Solve
\( x = 180^{\circ} - 45^{\circ} = 135^{\circ} \)
Step 4: Check
The angles are \( 45^{\circ}, 135^{\circ}, 45^{\circ}, 135^{\circ} \) and their sum is \( 360^{\circ} \) ✓""", trick=r"Adjacent angles of a parallelogram = 180°.")
S[47] = dict(raw=r"""Step 1: Write both as fractions in lowest terms
\( 0.75 = \dfrac{3}{4} \) and \( \dfrac{25}{30} = \dfrac{5}{6} \)
Step 2: Formula
\( \text{LCM of fractions} = \dfrac{\text{LCM of numerators}}{\text{HCF of denominators}} \)
Step 3: Apply
LCM of 3 and 5 = 15; HCF of 4 and 6 = 2. So LCM \( = \dfrac{15}{2} \)
Step 4: Check
\( \dfrac{15}{2} \div \dfrac{3}{4} = 10 \) and \( \dfrac{15}{2} \div \dfrac{5}{6} = 9 \) — both whole numbers ✓""", trick=r"LCM of fractions = LCM(numerators) ÷ HCF(denominators) — reduce the fractions first.")
S[48] = dict(raw=r"""Step 1: Write the numbers using the HCF
In the ratio \( 5 : 3 \) with HCF 12, the numbers are \( 5 \times 12 = 60 \) and \( 3 \times 12 = 36 \).
Step 2: Check the LCM
\( \text{LCM} = 12 \times 5 \times 3 = 180 \) ✓
Step 3: Check with the product rule
\( 60 \times 36 = 2160 = 12 \times 180 \) ✓
Step 4: Sum
\( 60 + 36 = 96 \)""", trick=r"Numbers = HCF × ratio terms; sum = HCF × (5 + 3) = 12 × 8 = 96.")
S[49] = dict(raw=r"""Step 1: Write the statement
\( A\% \text{ of } A = \dfrac{A}{100} \times A = 676 \)
Step 2: Simplify
\( \dfrac{A^{2}}{100} = 676 \)
Step 3: Solve for the square
\( A^{2} = 676 \times 100 = 67600 \)
Step 4: Check
\( A = \sqrt{67600} = 260 \), and \( 260\% \text{ of } 260 = 2.6 \times 260 = 676 \) ✓""", trick=r"A% of A = A²/100, so A² = 100 × 676.")
S[50] = dict(raw=r"""Step 1: Find the number
\( 20\% \text{ of } N = 80 \Rightarrow N = \dfrac{80 \times 100}{20} = 400 \)
Step 2: Find 160%
\( 160\% \text{ of } 400 = \dfrac{160}{100} \times 400 \)
Step 3: Calculate
\( 1.6 \times 400 = 640 \)
Step 4: Shortcut check
160% is 8 times 20%, so \( 8 \times 80 = 640 \) ✓""", trick=r"160 ÷ 20 = 8, so the answer is 8 × 80.")
S[51] = dict(raw=r"""Step 1: Assume a cost price
Let \( \text{CP} = 100 \); then \( \text{SP} = 130 \).
Step 2: Decrease both by 40%
New \( \text{CP} = 60 \), new \( \text{SP} = 0.6 \times 130 = 78 \).
Step 3: New profit
\( 78 - 60 = 18 \)
Step 4: New profit percentage
\( \dfrac{18}{60} \times 100 = 30\% \) — unchanged, because both values were cut by the same percentage.""", trick=r"Same % change on CP and SP keeps the profit % unchanged.")
S[52] = dict(raw=r"""Step 1: CP of one article
\( \dfrac{260}{30} \)
Step 2: SP of one article
\( \dfrac{260}{40} \)
Step 3: Compare with the same money
For ₹260, one gets 30 articles at cost but must sell 40 articles. Loss = cost of \( 40 - 30 = 10 \) articles on a cost of 40 articles.
Step 4: Loss percentage
\( \dfrac{10}{40} \times 100 = 25\% \) loss""", trick=r"CP of x = SP of y (same money): loss % = (y − x) ÷ y × 100.")
S[53] = dict(raw=r"""Step 1: Total work as LCM
LCM of 14, 21 and 42 = 42 units.
Step 2: One-day work
\( A = \dfrac{42}{14} = 3,\; B = \dfrac{42}{21} = 2,\; C = \dfrac{42}{42} = 1 \) unit per day
Step 3: Together
\( 3 + 2 + 1 = 6 \) units per day
Step 4: Days
\( \dfrac{42}{6} = 7 \) days""", trick=r"Take total work = LCM of the days.")
S[54] = dict(raw=r"""Step 1: Total work in each unit
Work = \( 5 \times 15 = 75 \) man-days = \( 6 \times 10 = 60 \) woman-days = \( 4 \times 12 = 48 \) boy-days.
Step 2: Work by the group in one day
\( \dfrac{8}{48} + \dfrac{10}{75} + \dfrac{12}{60} = \dfrac{1}{6} + \dfrac{2}{15} + \dfrac{1}{5} \)
Step 3: Add
\( \dfrac{5 + 4 + 6}{30} = \dfrac{15}{30} = \dfrac{1}{2} \)
Step 4: Days
Half the work is done each day, so the whole work takes 2 days.""", trick=r"Convert each group to its share of work per day, then add.")
S[55] = dict(raw=r"""Step 1: Relative speed
Opposite directions with the same speed v: relative speed \( = v + v = 2v \)
Step 2: Distance to cross
Sum of the lengths \( = 304 + 304 = 608 \) m
Step 3: Equation
\( 2v = \dfrac{608}{16} = 38 \) m/s
Step 4: Speed of each train
\( v = \dfrac{38}{2} = 19 \) m/s""", trick=r"Equal trains, opposite directions: v = length ÷ time = 304 ÷ 16.")
S[56] = dict(raw=r"""Step 1: Time for 143 km
\( \dfrac{143}{11} = 13 \) hours
Step 2: Time for 77 km
\( \dfrac{77}{11} = 7 \) hours
Step 3: Difference
\( 13 - 7 = 6 \) hours
Step 4: Shortcut check
\( \dfrac{143 - 77}{11} = \dfrac{66}{11} = 6 \) ✓""", trick=r"Same speed: time difference = distance difference ÷ speed.")
S[57] = dict(raw=r"""Step 1: Assume the numbers
\( A = 5x,\; B = 4x \)
Step 2: After adding 6
\( \dfrac{5x + 6}{4x + 6} = \dfrac{6}{5} \)
Step 3: Solve
\( 25x + 30 = 24x + 36 \Rightarrow x = 6 \), so A = 30 and B = 24.
Step 4: Final sum
\( (30 + 6) + (24 + 6) = 36 + 30 = 66 \)""", trick=r"Ratio 5:4 → 6:5 by adding 6: each 'part' = 6, final sum = 11 parts = 66.")
S[58] = dict(raw=r"""Step 1: Marked price
After a 30% discount, \( 70\% \text{ of MP} = 420 \Rightarrow \text{MP} = \dfrac{420 \times 100}{70} = 600 \)
Step 2: Without discount
SP would be the MP = ₹600.
Step 3: Use the 50% profit
\( 150\% \text{ of CP} = 600 \)
Step 4: Cost price
\( \text{CP} = \dfrac{600 \times 100}{150} = 400 \), i.e. ₹400.""", trick=r"MP = 420 ÷ 0.7 = 600; CP = 600 ÷ 1.5 = 400.")
S[59] = dict(raw=r"""Step 1: Assume a cost price
Let \( \text{CP} = 100 \); with 10% profit, \( \text{SP} = 110 \).
Step 2: Discount
\( \dfrac{3}{11} \times 110 = 30 \)
Step 3: Marked price
\( \text{MP} = \text{SP} + \text{Discount} = 110 + 30 = 140 \)
Step 4: CP below MP
\( \dfrac{140 - 100}{140} \times 100 = \dfrac{40}{140} \times 100 \approx 28.57\% \)""", trick=r"Take CP = 100: MP = 140, so CP is 40 less on a base of 140.")
S[60] = dict(raw=r"""Step 1: Condition for proportion
\( (12 + x) : (20 + x) = (28 + x) : (44 + x) \Rightarrow (12 + x)(44 + x) = (20 + x)(28 + x) \)
Step 2: Expand
\( 528 + 56x + x^{2} = 560 + 48x + x^{2} \)
Step 3: Solve
\( 8x = 32 \Rightarrow x = 4 \)
Step 4: Check
16, 24, 32, 48: \( 16 \times 48 = 768 = 24 \times 32 \) ✓""", trick=r"Product of extremes = product of means.")
