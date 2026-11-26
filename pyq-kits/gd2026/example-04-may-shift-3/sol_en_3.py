S = {}
S[41] = dict(raw=r"""Step 1: Bracket first
\( 47 + 11 = 58 \)
Step 2: Multiplication next
\( 49 \times 2 = 98 \)
Step 3: Rewrite the expression
\( 53 + 72 - 36 + 98 - 58 \)
Step 4: Add and subtract from left to right
\( 125 - 36 = 89,\; 89 + 98 = 187,\; 187 - 58 = 129 \)""", trick=r"BODMAS: bracket → × → + and − from left to right.")
S[42] = dict(raw=r"""Step 1: Solve "of" inside the bracket
\( (28 \text{ of } 1) = 28 \times 1 = 28 \)
Step 2: Division next
\( 36 \div 3 = 12 \)
Step 3: Rewrite the expression
\( 93 - 47 + 19 + 12 + 28 - 21 \)
Step 4: Add and subtract from left to right
\( 46 + 19 = 65,\; 65 + 12 = 77,\; 77 + 28 = 105,\; 105 - 21 = 84 \)""", trick=r"'of' means multiply; do it with the bracket before ÷.")
S[43] = dict(raw=r"""Step 1: Remove the decimals
\( \dfrac{0.0225}{0.04} = \dfrac{225}{400} \) (multiply top and bottom by 10000).
Step 2: Take the square root of top and bottom
\( \sqrt{\dfrac{225}{400}} = \dfrac{\sqrt{225}}{\sqrt{400}} = \dfrac{15}{20} \)
Step 3: Simplify
\( \dfrac{15}{20} = \dfrac{3}{4} = 0.75 \)
Step 4: Check
\( 0.75 \times 0.75 = 0.5625 \) and \( 0.5625 \times 0.04 = 0.0225 \) ✓""", trick=r"√0.0225 = 0.15 and √0.04 = 0.2, so 0.15 ÷ 0.2 = 0.75.")
S[44] = dict(raw=r"""Step 1: Square the first number
\( 4.10 \times 4.10 = 16.81 \)
Step 2: Square the second number
\( 1.90 \times 1.90 = 3.61 \)
Step 3: Add the squares
\( 16.81 + 3.61 = 20.42 \)
Step 4: Add the last term
\( 20.42 + 15.58 = 36.00 \)""", trick=r"Note 16.81 + 3.61 + 15.58 — the decimals .42 and .58 make a whole number.")
S[45] = dict(raw=r"""Step 1: Formula for the area of a rhombus
\( \text{Area} = \dfrac{1}{2} \times d_1 \times d_2 \)
Step 2: Put in the values
\( 180 = \dfrac{1}{2} \times 20 \times d_2 \Rightarrow 180 = 10 \times d_2 \)
Step 3: Find the other diagonal
\( d_2 = \dfrac{180}{10} = 18 \) cm
Step 4: Ratio of the diagonals
\( 20 : 18 = 10 : 9 \)""", trick=r"Other diagonal = 2 × Area ÷ given diagonal = 360 ÷ 20 = 18.")
S[46] = dict(raw=r"""Step 1: Find the side
All four sides of a rhombus are equal: \( \text{side} = \dfrac{100}{4} = 25 \) cm.
Step 2: Use half-diagonals
The diagonals bisect each other at right angles. Half of the given diagonal \( = \dfrac{30}{2} = 15 \) cm.
Step 3: Pythagoras in one right triangle
\( 25^2 = 15^2 + x^2 \Rightarrow x^2 = 625 - 225 = 400 \Rightarrow x = 20 \) cm
Step 4: Other diagonal
\( 2 \times 20 = 40 \) cm""", trick=r"15–20–25 is the 3–4–5 triangle × 5.")
S[47] = dict(raw=r"""Step 1: Use the property of LCM
\( \text{LCM}(A, B, C) = \text{LCM}(\text{LCM}(A, B), C) = \text{LCM}(36, 24) \)
Step 2: Prime factors
\( 36 = 2^2 \times 3^2 \) and \( 24 = 2^3 \times 3 \)
Step 3: Take the highest powers
\( \text{LCM} = 2^3 \times 3^2 = 8 \times 9 = 72 \)
Step 4: Check
72 ÷ 36 = 2 and 72 ÷ 24 = 3 — both divide exactly, and no smaller common multiple exists.""", trick=r"LCM of A, B, C = LCM of (LCM of A and B) and C.")
S[48] = dict(raw=r"""Step 1: Know the rule
The HCF of two numbers always divides their LCM exactly.
Step 2: Test each value with 12
\( 130 \div 12 \) leaves 10, \( 110 \div 12 \) leaves 2, \( 95 \div 12 \) leaves 11.
Step 3: The value that works
\( 144 \div 12 = 12 \) — exact.
Step 4: Example
The numbers 36 and 48 have HCF 12 and LCM 144, so 144 is possible.""", trick=r"LCM must be a multiple of the HCF.")
S[49] = dict(raw=r"""Step 1: Write A in terms of B
A is 30% less than B: \( A = B \times \dfrac{70}{100} = 0.7B \)
Step 2: Put in the value of A
\( 0.7B = 630 \)
Step 3: Solve
\( B = \dfrac{630}{0.7} = 900 \)
Step 4: Check
30% of 900 = 270 and \( 900 - 270 = 630 \) ✓""", trick=r"70% of B = 630 → 1% = 9 → 100% = 900.")
S[50] = dict(raw=r"""Step 1: Take a convenient value
Let \( B = 100 \). Then \( A = \dfrac{1}{4} \times 100 = 25 \).
Step 2: Find the difference
\( 100 - 25 = 75 \)
Step 3: Percentage less (compare with B)
\( \dfrac{75}{100} \times 100 = 75\% \)
Step 4: Answer
A is 75% less than B.""", trick=r"A = 1/4 of B means A is 3/4 = 75% less than B.")
S[51] = dict(raw=r"""Step 1: Loss is the difference
At a loss, CP − SP = loss = ₹520.
Step 2: Write loss in terms of CP
Loss = 20% of CP: \( \dfrac{20}{100} \times \text{CP} = 520 \)
Step 3: Solve
\( \text{CP} = \dfrac{520 \times 100}{20} = 2600 \)
Step 4: Answer and check
CP = ₹2600; SP = 2600 − 520 = ₹2080, and \( \dfrac{520}{2600} \times 100 = 20\% \) ✓""", trick=r"20% = 520 → 100% = 520 × 5 = 2600.")
S[52] = dict(raw=r"""Step 1: Loss is the difference
CP − SP = loss = ₹420.
Step 2: Write loss in terms of CP
\( \dfrac{16}{100} \times \text{CP} = 420 \)
Step 3: Solve
\( \text{CP} = \dfrac{420 \times 100}{16} = \dfrac{42000}{16} = 2625 \)
Step 4: Check
16% of 2625 = \( 2625 \times 0.16 = 420 \) ✓, so CP = ₹2625.""", trick=r"16% = 420 → 4% = 105 → 100% = 105 × 25 = 2625.")
S[53] = dict(raw=r"""Step 1: Work done per day
40% in 8 days → \( \dfrac{40\%}{8} = 5\% \) per day.
Step 2: Work in 15 days
\( 15 \times 5\% = 75\% \)
Step 3: As a fraction
\( 75\% = \dfrac{3}{4} \) of the work.
Step 4: Answer
A completes 75% of the work in 15 days.""", trick=r"Work is proportional to days: 40% × 15 ÷ 8 = 75%.")
S[54] = dict(raw=r"""Step 1: Total work of each
\( A = 6 \times 3 = 18 \) units, \( B = 4 \times 5 = 20 \) units.
Step 2: Wages are shared in the ratio of work
\( A : B = 18 : 20 = 9 : 10 \), total 19 parts (38 units).
Step 3: Value of one part
\( \dfrac{4408}{19} = 232 \)
Step 4: Difference
B − A = 10 − 9 = 1 part = ₹232 (A gets ₹2088, B gets ₹2320).""", trick=r"Wages ∝ total units of work done.")
S[55] = dict(raw=r"""Step 1: Distance covered while crossing
Distance = length of train + length of bridge.
Step 2: Calculate the distance
\( 15 \times 65 = 975 \) m
Step 3: Subtract the bridge
\( 975 - 500 = 475 \) m
Step 4: Answer
The train is 475 m long.""", trick=r"Train length = speed × time − bridge length.")
S[56] = dict(raw=r"""Step 1: Upstream speed
\( \dfrac{80}{8} = 10 \) km/hr
Step 2: Downstream speed
\( \dfrac{80}{4} = 20 \) km/hr
Step 3: Speed in still water
\( \dfrac{10 + 20}{2} = 15 \) km/hr
Step 4: Stream speed (check)
\( \dfrac{20 - 10}{2} = 5 \) km/hr, and \( 15 - 5 = 10 \), \( 15 + 5 = 20 \) ✓""", trick=r"Boat speed = (down + up) ÷ 2.")
S[57] = dict(raw=r"""Step 1: Take the numbers
A = 7x and B = 5x.
Step 2: Form the equation
\( \dfrac{7x + 3}{5x + 3} = \dfrac{4}{3} \)
Step 3: Solve
\( 21x + 9 = 20x + 12 \Rightarrow x = 3 \)
Step 4: Sum of the original numbers
A = 21, B = 15, so \( 21 + 15 = 36 \). Check: \( 24 : 18 = 4 : 3 \) ✓""", trick=r"Sum = 12x; find x and multiply.")
S[58] = dict(raw=r"""Step 1: Take a convenient cost price
Let CP = 100. Profit 20% → SP = 120.
Step 2: Find the discount
Discount \( = \dfrac{9}{11} \times 120 = \dfrac{1080}{11} \)
Step 3: Marked price
\( \text{MP} = \text{SP} + \text{Discount} = 120 + \dfrac{1080}{11} = \dfrac{1320 + 1080}{11} = \dfrac{2400}{11} \)
Step 4: Ratio
\( \text{MP} : \text{CP} = \dfrac{2400}{11} : 100 = 24 : 11 \)""", trick=r"MP = SP × (1 + 9/11) = SP × 20/11, and SP = CP × 6/5.")
S[59] = dict(raw=r"""Step 1: First discount
10% off ₹3000: \( 3000 \times \dfrac{90}{100} = 2700 \)
Step 2: Second discount amount
\( 2700 - 1890 = 810 \)
Step 3: Second discount rate
\( A = \dfrac{810}{2700} \times 100 = 30 \)
Step 4: Check
\( 3000 \times 0.9 \times 0.7 = 1890 \) ✓""", trick=r"1890 ÷ 3000 = 0.63 = 0.9 × 0.7 → second discount 30%.")
S[60] = dict(raw=r"""Step 1: Meaning of "in proportion"
\( 25 : 5 = 20 : X \)
Step 2: Product of extremes = product of means
\( 25 \times X = 5 \times 20 \)
Step 3: Solve
\( X = \dfrac{100}{25} = 4 \)
Step 4: Check
\( \dfrac{25}{5} = 5 \) and \( \dfrac{20}{4} = 5 \) ✓""", trick=r"Fourth proportional = (b × c) ÷ a.")
