S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first
\( 28 + 17 = 45 \)
Step 2: Multiplication
\( 45 \times 2 = 90 \)
Step 3: Add and subtract from left to right
\( 61 + 45 - 32 + 90 - 84 = 106 - 32 + 90 - 84 = 74 + 90 - 84 \)
Step 4: Result
\( 164 - 84 = 80 \)""", trick=r"BODMAS: bracket → × → + and − from the left.")
S[42] = dict(raw=r"""Step 1: Bracket
\( 27 \div 3 = 9 \)
Step 2: Multiplication
\( 28 \times 1 = 28 \)
Step 3: Rewrite
\( 94 - 47 + 31 + 9 + 28 - 19 \)
Step 4: Left to right
\( 47 + 31 = 78,\; 78 + 9 = 87,\; 87 + 28 = 115,\; 115 - 19 = 96 \)""", trick=r"Group the plus terms (31 + 9 + 28 = 68), then 94 − 47 − 19 + 68 = 96.")
S[43] = dict(raw=r"""Step 1: Split the root
\( \sqrt{1.44 \times 0.0225} = \sqrt{1.44} \times \sqrt{0.0225} \)
Step 2: First root
\( \sqrt{1.44} = 1.2 \) because \( 1.2 \times 1.2 = 1.44 \)
Step 3: Second root
\( \sqrt{0.0225} = 0.15 \) because \( 0.15 \times 0.15 = 0.0225 \)
Step 4: Multiply
\( 1.2 \times 0.15 = 0.18 \)""", trick=r"Root of a product = product of the roots.")
S[44] = dict(raw=r"""Step 1: Square roots
\( \sqrt{0.09} = 0.3 \) and \( \sqrt{0.64} = 0.8 \)
Step 2: Cube root
\( \sqrt[3]{0.125} = 0.5 \) because \( 0.5 \times 0.5 \times 0.5 = 0.125 \)
Step 3: Fourth root
\( \sqrt[4]{0.0081} = 0.3 \) because \( 0.3^{4} = 0.0081 \)
Step 4: Combine
\( 0.3 + 0.5 + 0.3 - 0.8 = 0.3 \)""", trick=r"0.0081 has 4 decimal places → its fourth root has 1 (0.3).")
S[45] = dict(raw=r"""Step 1: Use the area
\( \text{Area} = \dfrac{d_{1} \times d_{2}}{2} = 840 \Rightarrow d_{1} d_{2} = 1680 \)
Step 2: Use the side
The diagonals bisect each other at right angles, so \( \left(\dfrac{d_{1}}{2}\right)^{2} + \left(\dfrac{d_{2}}{2}\right)^{2} = 29^{2} \Rightarrow d_{1}^{2} + d_{2}^{2} = 4 \times 841 = 3364 \)
Step 3: Square of the sum
\( (d_{1} + d_{2})^{2} = d_{1}^{2} + d_{2}^{2} + 2 d_{1} d_{2} = 3364 + 3360 = 6724 \)
Step 4: Sum of diagonals
\( d_{1} + d_{2} = \sqrt{6724} = 82 \) cm (the diagonals are 40 cm and 42 cm).""", trick=r"Half-diagonals 20 and 21 with side 29 — the 20-21-29 triple.")
S[46] = dict(raw=r"""Step 1: Formula
\( \text{Area of a parallelogram} = \text{base} \times \text{height} \)
Step 2: Values
Base = 12 cm, corresponding height = 7 cm
Step 3: Multiply
\( 12 \times 7 = 84 \)
Step 4: Answer
The area is 84 square cm.""", trick=r"Parallelogram area = base × height (not half).")
S[47] = dict(raw=r"""Step 1: Formula
\( \text{LCM of fractions} = \dfrac{\text{LCM of numerators}}{\text{HCF of denominators}} \)
Step 2: LCM of the numerators 3, 4, 8
\( \text{LCM}(3, 4, 8) = 24 \)
Step 3: HCF of the denominators 5, 15, 25
\( \text{HCF}(5, 15, 25) = 5 \)
Step 4: Result
\( \text{LCM} = \dfrac{24}{5} \)""", trick=r"LCM of fractions = LCM(top) ÷ HCF(bottom).")
S[48] = dict(raw=r"""Step 1: Write the numbers
Let the numbers be \( 3x \) and \( 5x \).
Step 2: Their LCM
3 and 5 are co-prime, so \( \text{LCM} = 15x \).
Step 3: Find x
\( 15x = 120 \Rightarrow x = 8 \); the numbers are 24 and 40.
Step 4: Sum
\( 24 + 40 = 64 \)""", trick=r"Ratio a:b (co-prime) → LCM = abx, sum = (a + b)x.")
S[49] = dict(raw=r"""Step 1: Two-fifths of 4500
\( \dfrac{2}{5} \times 4500 = 1800 \)
Step 2: 20 percent of that
\( \dfrac{20}{100} \times 1800 = 360 \)
Step 3: 30 percent of that
\( \dfrac{30}{100} \times 360 = 108 \)
Step 4: Check in one line
\( 0.3 \times 0.2 \times 0.4 \times 4500 = 0.024 \times 4500 = 108 \)""", trick=r"Chain of 'of' → multiply all the fractions together.")
S[50] = dict(raw=r"""Step 1: Formula
\( \text{B as a percent of A} = \dfrac{B}{A} \times 100 \)
Step 2: Substitute
\( \dfrac{5X}{2X} \times 100 \)
Step 3: Simplify
\( \dfrac{5}{2} \times 100 = 250 \)
Step 4: Answer
B is 250 percent of A.""", trick=r"'B is what percent of A' → A goes in the denominator.")
S[51] = dict(raw=r"""Step 1: Take a cost price
Let CP = 100, so SP = 110 (10 percent profit).
Step 2: Decrease both by 20 percent
New CP \( = 100 \times 0.8 = 80 \), new SP \( = 110 \times 0.8 = 88 \)
Step 3: New profit
\( 88 - 80 = 8 \)
Step 4: New profit percent
\( \dfrac{8}{80} \times 100 = 10\% \)""", trick=r"Same percent change on CP and SP keeps the profit percent the same.")
S[52] = dict(raw=r"""Step 1: Cost price of one article
\( \dfrac{260}{20} = 13 \) rupees
Step 2: Selling price of one article
\( \dfrac{260}{25} = 10.4 \) rupees
Step 3: Loss on one article
\( 13 - 10.4 = 2.6 \) — SP is less than CP, so it is a loss.
Step 4: Loss percent
\( \dfrac{2.6}{13} \times 100 = 20\% \) loss""", trick=r"Same money for 20 and 25 articles → loss = \( \dfrac{25 - 20}{25} \times 100 = 20\% \).")
S[53] = dict(raw=r"""Step 1: One day's work of each
A \( = \dfrac{1}{10} \), B \( = \dfrac{1}{15} \), C \( = \dfrac{1}{30} \)
Step 2: Together in one day
\( \dfrac{1}{10} + \dfrac{1}{15} + \dfrac{1}{30} = \dfrac{3 + 2 + 1}{30} = \dfrac{6}{30} = \dfrac{1}{5} \)
Step 3: Time for the whole work
Together they finish the work in 5 days.
Step 4: Time for 30 percent of the work
\( 5 \times \dfrac{30}{100} = \dfrac{3}{2} \) days""", trick=r"Total work = LCM 30 units; efficiencies 3, 2, 1 → 6 units a day; 30% = 9 units → 1.5 days.")
S[54] = dict(raw=r"""Step 1: Woman-days for half the work
\( 10 \times 20 = 200 \) woman-days
Step 2: The remaining half needs the same
The other half also needs 200 woman-days.
Step 3: Women needed in 4 days
\( \dfrac{200}{4} = 50 \) women
Step 4: Extra women
\( 50 - 10 = 40 \) more women""", trick=r"M₁D₁ = M₂D₂ for equal work; subtract the women already working.")
S[55] = dict(raw=r"""Step 1: Convert the speed
\( 54 \times \dfrac{5}{18} = 15 \) m/s
Step 2: Convert the time
6 minutes \( = 6 \times 60 = 360 \) s
Step 3: Distance
\( 15 \times 360 = 5400 \) m
Step 4: Answer
The boy's own length is negligible, so the bridge is 5400 m long.""", trick=r"km/h × 5/18 = m/s.")
S[56] = dict(raw=r"""Step 1: Convert the speed
\( 90 \times \dfrac{5}{18} = 25 \) m/s
Step 2: Distance covered while crossing the platform
\( 25 \times 54 = 1350 \) m = train + platform
Step 3: Use the platform length
Let the train be L; the platform is 2L, so \( L + 2L = 3L = 1350 \)
Step 4: Train length
\( L = \dfrac{1350}{3} = 450 \) m""", trick=r"Crossing a platform → distance = train + platform.")
S[57] = dict(raw=r"""Step 1: Total parts
\( 2 + 4 + 5 + 7 = 18 \) parts
Step 2: Value of one part
\( \dfrac{54}{18} = 3 \)
Step 3: Largest and smallest
Largest \( = 7 \times 3 = 21 \), smallest \( = 2 \times 3 = 6 \)
Step 4: Difference
\( 21 - 6 = 15 \)""", trick=r"Difference = (7 − 2) parts × 3 = 15.")
S[58] = dict(raw=r"""Step 1: Selling price
\( \text{SP} = 3000 \times \dfrac{125}{100} = 3750 \) rupees
Step 2: Discount amount
\( 5000 - 3750 = 1250 \) rupees
Step 3: Discount percent (on the marked price)
\( \dfrac{1250}{5000} \times 100 \)
Step 4: Result
\( = 25\% \)""", trick=r"Discount % is always on the marked price.")
S[59] = dict(raw=r"""Step 1: Take a cost price
Let CP = 100, so MP = 125.
Step 2: No loss condition
The maximum discount brings SP down to CP = 100.
Step 3: Discount amount
\( 125 - 100 = 25 \)
Step 4: Discount percent
\( \dfrac{25}{125} \times 100 = 20\% \)""", trick=r"Mark-up x% → no-loss discount = \( \dfrac{x}{100 + x} \times 100 \).")
S[60] = dict(raw=r"""Step 1: Meaning
The fourth proportional x satisfies \( 8 : 10 = 16 : x \).
Step 2: Product of extremes = product of means
\( 8 \times x = 10 \times 16 \)
Step 3: Solve
\( x = \dfrac{160}{8} = 20 \)
Step 4: Check
\( \dfrac{8}{10} = \dfrac{16}{20} = 0.8 \) ✓""", trick=r"Fourth proportional of a, b, c = \( \dfrac{bc}{a} \).")
