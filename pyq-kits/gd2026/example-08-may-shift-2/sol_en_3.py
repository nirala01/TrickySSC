S = {}
S[41] = dict(raw=r"""Step 1: Solve "of" first
\( 38 \text{ of } 1 = 38 \times 1 = 38 \).
Step 2: Solve the division and the bracket
\( 19 \div 1 = 19 \) and \( (18 \times 1) = 18 \).
Step 3: Rewrite the expression
\( 93 - 27 + 38 + 19 - 18 + 44 \).
Step 4: Add and subtract from left to right
\( 93 - 27 = 66 \), \( 66 + 38 = 104 \), \( 104 + 19 = 123 \), \( 123 - 18 = 105 \), \( 105 + 44 = 149 \).""", trick=r"BODMAS: 'of' is done with multiplication, before + and −.")
S[42] = dict(raw=r"""Step 1: See what is asked
Every box must have the same number of each item with nothing left over, so the number of boxes must divide 144, 180 and 216. The maximum such number is their HCF.
Step 2: Factorise
\( 144 = 2^{4} \times 3^{2} \), \( 180 = 2^{2} \times 3^{2} \times 5 \), \( 216 = 2^{3} \times 3^{3} \).
Step 3: Take the lowest powers
HCF = \( 2^{2} \times 3^{2} = 36 \).
Step 4: Check
\( 144 \div 36 = 4 \), \( 180 \div 36 = 5 \), \( 216 \div 36 = 6 \) — no item is left. Maximum boxes = 36.""", trick=r"'Maximum boxes, nothing left' = HCF.")
S[43] = dict(raw=r"""Step 1: Work out the products
\( 0.5 \times 0.5 = 0.25 \) and \( 0.5 \times 0.05 = 0.025 \).
Step 2: Add them
\( 0.25 + 0.025 = 0.275 \).
Step 3: Divide by 0.1375
\( \dfrac{0.275}{0.1375} = \dfrac{2750}{1375} \).
Step 4: Simplify
\( 1375 \times 2 = 2750 \), so the value is 2.""", trick=r"Clear the decimals by multiplying top and bottom by the same power of 10.")
S[44] = dict(raw=r"""Step 1: Find each square root
\( \sqrt{20.25} = 4.5 \), \( \sqrt{0.36} = 0.6 \), \( \sqrt{6.25} = 2.5 \), \( \sqrt{2.25} = 1.5 \).
Step 2: Write the expression
\( 4.5 + 0.6 + 2.5 - 1.5 \).
Step 3: Add the positive terms
\( 4.5 + 0.6 + 2.5 = 7.6 \).
Step 4: Subtract
\( 7.6 - 1.5 = 6.1 \).""", trick=r"Know the decimal squares: 4.5² = 20.25, 2.5² = 6.25, 1.5² = 2.25.")
S[45] = dict(raw=r"""Step 1: Find the square roots
\( \sqrt{100} = 10 \), \( \sqrt{25} = 5 \), \( \sqrt{49} = 7 \).
Step 2: Divide first (BODMAS)
\( 10 \div 5 = 2 \).
Step 3: Add
\( x = 2 + 7 = 9 \).
Step 4: Square
\( x^{2} = 9^{2} = 81 \).""", trick=r"Division before addition: 10 ÷ 5 + 7, not 10 ÷ 12.")
S[46] = dict(raw=r"""Step 1: Write the numbers
Let the three consecutive even numbers be n, n + 2 and n + 4.
Step 2: Form the equation
\( n + (n + 2) + (n + 4) = 60 \), so \( 3n + 6 = 60 \).
Step 3: Solve
\( 3n = 54 \), so n = 18.
Step 4: Check
\( 18 + 20 + 22 = 60 \) ✓. The smallest number is 18.""", trick=r"Middle number = sum ÷ 3 = 20; smallest = 20 − 2.")
S[47] = dict(raw=r"""Step 1: Solve the brackets
\( 21 + 11 = 32 \) and \( 21 - 11 = 10 \).
Step 2: Multiply
\( 32 \times 10 = 320 \).
Step 3: Take the square root
\( \sqrt{320} \).
Step 4: Square it
\( \left(\sqrt{320}\right)^{2} = 320 \) — squaring undoes the square root.""", trick=r"(a + b)(a − b) = a² − b²: 21² − 11² = 441 − 121 = 320.")
S[48] = dict(raw=r"""Step 1: Recall the rule
A number is divisible by 9 if the sum of its digits is divisible by 9.
Step 2: Add the known digits
\( 5 + 8 + 8 = 21 \), so the digit sum is \( 21 + P \).
Step 3: Find P
The next multiple of 9 after 21 is 27, so \( P = 27 - 21 = 6 \) (P is a single digit, so 36 is too far).
Step 4: Check
5868: digit sum \( 5 + 8 + 6 + 8 = 27 \), and \( 5868 \div 9 = 652 \) ✓.""", trick=r"Digit sum → nearest multiple of 9.")
S[49] = dict(raw=r"""Step 1: Simplify each surd
\( \sqrt{48} = \sqrt{16 \times 3} = 4\sqrt{3} \), \( \sqrt{27} = \sqrt{9 \times 3} = 3\sqrt{3} \), \( \sqrt{12} = \sqrt{4 \times 3} = 2\sqrt{3} \).
Step 2: Rewrite
\( 4\sqrt{3} + 3\sqrt{3} - 2\sqrt{3} \).
Step 3: Combine like surds
\( (4 + 3 - 2)\sqrt{3} = 5\sqrt{3} \).
Step 4: Answer
The value is \( 5\sqrt{3} \).""", trick=r"Pull out the largest perfect square, then add the numbers in front of √3.")
S[50] = dict(raw=r"""Step 1: Write what is given
Area: \( l \times b = 192 \). Diagonal: \( l^{2} + b^{2} = 20^{2} = 400 \).
Step 2: Use the identity
\( (l + b)^{2} = l^{2} + b^{2} + 2lb = 400 + 384 = 784 \).
Step 3: Find l + b
\( l + b = \sqrt{784} = 28 \).
Step 4: Find the perimeter
Perimeter = \( 2(l + b) = 2 \times 28 = 56 \) cm. (Check: l = 16, b = 12 gives area 192 and diagonal 20 ✓.)""", trick=r"(l + b)² = d² + 2 × area.")
S[51] = dict(raw=r"""Step 1: Note the effect of subtracting M
If M is subtracted from every number, the average also falls by M.
Step 2: Find the fall in the average
\( 34 - 29 = 5 \).
Step 3: So M = 5.
Step 4: Check with totals
Old total \( 24 \times 34 = 816 \); new total \( 816 - 24 \times 5 = 696 \); \( 696 \div 24 = 29 \) ✓.""", trick=r"Same change to every item = same change to the average.")
S[52] = dict(raw=r"""Step 1: Write the formula
Profit = \( \dfrac{\text{Profit\%} \times \text{CP}}{100} \).
Step 2: Put the values
\( \dfrac{25 \times 500}{100} \).
Step 3: Calculate
\( \dfrac{12500}{100} = 125 \).
Step 4: Answer
The profit is ₹125 (so the SP is ₹625).""", trick=r"25% = one-fourth: 500 ÷ 4 = 125.")
S[53] = dict(raw=r"""Step 1: Find the number
\( 60\% \) of N = 75, so \( N = \dfrac{75 \times 100}{60} = 125 \).
Step 2: Find 180% of it
\( \dfrac{180 \times 125}{100} \).
Step 3: Calculate
\( 1.8 \times 125 = 225 \).
Step 4: Shortcut check
180% is 3 times 60%, so the answer is \( 3 \times 75 = 225 \) ✓.""", trick=r"180% = 3 × 60% → 3 × 75.")
S[54] = dict(raw=r"""Step 1: Find the maximum marks
5 subjects of 200 marks each: \( 5 \times 200 = 1000 \).
Step 2: Find the total marks obtained
\( 60\% \) of 1000 = 600.
Step 3: Find the marks in subject 1
\( 25\% \) of 600 = \( \dfrac{25 \times 600}{100} = 150 \).
Step 4: Answer
He scored 150 marks in subject 1.""", trick=r"25% of the obtained total, not of the maximum marks.")
S[55] = dict(raw=r"""Step 1: Form the equation
\( 0.30 \times \text{CP} = 0.25 \times \text{SP} \).
Step 2: Find the ratio
\( \dfrac{\text{SP}}{\text{CP}} = \dfrac{30}{25} = \dfrac{6}{5} \).
Step 3: Take CP = 5 and SP = 6
Profit = \( 6 - 5 = 1 \).
Step 4: Profit percentage
\( \dfrac{1}{5} \times 100 = 20\% \).""", trick=r"CP × 30 = SP × 25 → SP:CP = 30:25.")
S[56] = dict(raw=r"""Step 1: Find the time for the whole work
50% in 10 days, so 100% in \( 10 \times 2 = 20 \) days.
Step 2: Find one day's work
\( \dfrac{100\%}{20} = 5\% \) per day.
Step 3: Work in 7 days
\( 7 \times 5\% = 35\% \).
Step 4: Answer
A completes 35% of the work in 7 days.""", trick=r"50% in 10 days → 5% a day.")
S[57] = dict(raw=r"""Step 1: Write one day's work
(P + Q) does \( \dfrac{1}{20} \) per day; R does \( \dfrac{1}{30} \) per day.
Step 2: Add
\( \dfrac{1}{20} + \dfrac{1}{30} = \dfrac{3 + 2}{60} = \dfrac{5}{60} = \dfrac{1}{12} \).
Step 3: Find the days
Together they need 12 days.
Step 4: Check with total work
Take work = 60 units: P + Q do 3 a day, R does 2 a day, together 5 a day → \( 60 \div 5 = 12 \) days ✓.""", trick=r"LCM method: total work = LCM(20, 30) = 60 units.")
S[58] = dict(raw=r"""Step 1: Recall the conversion
1 m/s = \( \dfrac{18}{5} \) km/h.
Step 2: Multiply
\( 100 \times \dfrac{18}{5} \).
Step 3: Calculate
\( 20 \times 18 = 360 \).
Step 4: Answer
The speed is 360 km/h.""", trick=r"m/s → km/h: × 18/5; km/h → m/s: × 5/18.")
S[59] = dict(raw=r"""Step 1: Find the relative speed
The train passes the man (a point) in 8 s, so relative speed = \( \dfrac{800}{8} = 100 \) m/s.
Step 2: Add the speeds (opposite directions)
Let the man's speed be v, so the train's is 4v. Relative speed = \( 4v + v = 5v = 100 \), so v = 20 m/s.
Step 3: Train's speed
\( 4 \times 20 = 80 \) m/s.
Step 4: Convert to km/h
\( 80 \times \dfrac{18}{5} = 288 \) km/h.""", trick=r"Opposite directions → add the speeds.")
S[60] = dict(raw=r"""Step 1: Find the cost price
MP = X; 25% discount, so CP = \( 0.75X \).
Step 2: Find the selling price
30% more than X: SP = \( 1.30X \).
Step 3: Find the profit
\( 1.30X - 0.75X = 0.55X \).
Step 4: Profit percentage
\( \dfrac{0.55X}{0.75X} \times 100 = \dfrac{220}{3} \approx 73.33\% \).""", trick=r"Profit % is on the buyer's cost (0.75X), not on X.")
