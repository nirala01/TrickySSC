S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first
\( 41 + 29 = 70 \)
Step 2: Rewrite the expression
\( 82 + 66 - 70 + 73 - 54 + 36 \)
Step 3: Add the positive terms
\( 82 + 66 + 73 + 36 = 257 \)
Step 4: Subtract the rest
\( 257 - 70 - 54 = 133 \)""", trick=r"Bracket first, then add all the + terms and subtract all the − terms.")
S[42] = dict(raw=r"""Step 1: Multiplication and division first
\( 22 \times 2 = 44 \) and \( 37 \div 1 = 37 \)
Step 2: Rewrite the expression
\( 93 - 48 + 44 + 37 - 19 + 16 \)
Step 3: Add the positive terms
\( 93 + 44 + 37 + 16 = 190 \)
Step 4: Subtract the rest
\( 190 - 48 - 19 = 123 \)""", trick=r"BODMAS: × and ÷ before + and −.")
S[43] = dict(raw=r"""Step 1: Change the given fraction to a decimal
\( \dfrac{5}{6} \approx 0.833 \)
Step 2: Change the options to decimals
\( \dfrac{10}{11} \approx 0.909 \), \( \dfrac{4}{5} = 0.8 \), \( \dfrac{9}{10} = 0.9 \), \( \dfrac{7}{8} = 0.875 \)
Step 3: Compare
Only \( 0.8 < 0.833 \); the other three are larger.
Step 4: Cross-check by cross-multiplying
\( \dfrac{4}{5} \) vs \( \dfrac{5}{6} \): \( 4 \times 6 = 24 < 5 \times 5 = 25 \), so \( \dfrac{4}{5} < \dfrac{5}{6} \).""", trick=r"For fractions n/(n+1), a smaller n gives a smaller fraction: 4/5 < 5/6 < 7/8 < 9/10 < 10/11.")
S[44] = dict(raw=r"""Step 1: Spot the identity
\( (a + b)^{2} - 4ab = (a - b)^{2} \)
Step 2: Identify a and b
\( a = 15.3 \), \( b = 5.3 \)
Step 3: Find a − b
\( 15.3 - 5.3 = 10 \)
Step 4: Square it
\( 10^{2} = 100 \)""", trick=r"(a + b)² − 4ab = (a − b)².")
S[45] = dict(raw=r"""Step 1: Formula
Perimeter of a square \( = 4 \times \text{side} \)
Step 2: Substitute
\( 4 \times 8 \)
Step 3: Calculate
\( 4 \times 8 = 32 \) cm
Step 4: Check
All four sides are 8 cm: \( 8 + 8 + 8 + 8 = 32 \) cm.""", trick=r"Perimeter of square = 4 × side.")
S[46] = dict(raw=r"""Step 1: Area formula of a rhombus
\( \text{Area} = \dfrac{d_1 \times d_2}{2} \)
Step 2: Substitute the known values
\( 84 = \dfrac{14 \times d_2}{2} = 7 d_2 \)
Step 3: Find the other diagonal
\( d_2 = \dfrac{84}{7} = 12 \) cm
Step 4: Ratio of the diagonals
\( 14 : 12 = 7 : 6 \)""", trick=r"Area of rhombus = ½ × d₁ × d₂.")
S[47] = dict(raw=r"""Step 1: Side of the rhombus
\( \text{side} = \dfrac{60}{4} = 15 \) cm
Step 2: Half of the known diagonal
\( \dfrac{18}{2} = 9 \) cm. The diagonals bisect each other at right angles.
Step 3: Half of the other diagonal
\( \sqrt{15^{2} - 9^{2}} = \sqrt{225 - 81} = \sqrt{144} = 12 \) cm, so the other diagonal \( = 24 \) cm.
Step 4: Sum
\( 18 + 24 = 42 \) cm""", trick=r"(d₁/2)² + (d₂/2)² = side²; 9-12-15 is a 3-4-5 triple.")
S[48] = dict(raw=r"""Step 1: Total age of the group
\( 16 \times 20 = 320 \) years
Step 2: Two boys leave
\( 320 - (18 + 19) = 320 - 37 = 283 \) years, with 14 boys left.
Step 3: One boy joins
\( 283 + 32 = 315 \) years, with 15 boys.
Step 4: New average
\( \dfrac{315}{15} = 21 \) years""", trick=r"Average = total ÷ number; update the total and the count separately.")
S[49] = dict(raw=r"""Step 1: Use the rule for two numbers
\( \text{HCF} \times \text{LCM} = A \times B \)
Step 2: Multiply A and B
\( (2^{5} \times 3^{2}) \times (2^{8} \times 3^{4}) \)
Step 3: Add the powers of the same base
\( 2^{5 + 8} \times 3^{2 + 4} = 2^{13} \times 3^{6} \)
Step 4: Check by finding HCF and LCM
\( \text{HCF} = 2^{5} \times 3^{2} \), \( \text{LCM} = 2^{8} \times 3^{4} \); their product is again \( 2^{13} \times 3^{6} \).""", trick=r"HCF × LCM = product of the two numbers.")
S[50] = dict(raw=r"""Step 1: List the numbers between 5 and 12
6, 7, 8, 9, 10, 11
Step 2: Pick the primes
Only 7 and 11 are prime (6, 8, 9, 10 have other factors).
Step 3: LCM of primes
The LCM of different primes is their product: \( 7 \times 11 \)
Step 4: Calculate
\( 7 \times 11 = 77 \)""", trick=r"LCM of distinct primes = their product.")
S[51] = dict(raw=r"""Step 1: Write the formula
\( \text{B as a percent of A} = \dfrac{B}{A} \times 100 \)
Step 2: Substitute
\( \dfrac{6X}{8X} \times 100 \)
Step 3: Cancel X
\( \dfrac{6}{8} \times 100 = \dfrac{3}{4} \times 100 \)
Step 4: Calculate
\( 75\% \)""", trick=r"6/8 = 3/4 = 75%.")
S[52] = dict(raw=r"""Step 1: Note the values
\( \text{CP} = ₹8000 \), \( \text{SP} = ₹6000 \); SP is less than CP, so there is a loss.
Step 2: Find the loss
\( 8000 - 6000 = ₹2000 \)
Step 3: Loss percentage formula
\( \text{Loss}\% = \dfrac{\text{Loss}}{\text{CP}} \times 100 \)
Step 4: Calculate
\( \dfrac{2000}{8000} \times 100 = 25\% \)""", trick=r"Loss % is always on CP: 2000/8000 = 1/4 = 25%.")
S[53] = dict(raw=r"""Step 1: Write the condition
\( 25\% \text{ of CP} = 10\% \text{ of SP} \)
Step 2: Find the ratio
\( \dfrac{\text{CP}}{\text{SP}} = \dfrac{10}{25} = \dfrac{2}{5} \), so take \( \text{CP} = 2 \), \( \text{SP} = 5 \).
Step 3: Profit
\( 5 - 2 = 3 \)
Step 4: Profit percentage
\( \dfrac{3}{2} \times 100 = 150\% \)""", trick=r"CP:SP = 10:25 = 2:5 → profit 3 on 2 = 150%.")
S[54] = dict(raw=r"""Step 1: Find 180% of 120
\( \dfrac{180}{100} \times 120 = 216 \)
Step 2: Set up the equation
\( 420 - x = 216 \)
Step 3: Solve
\( x = 420 - 216 = 204 \)
Step 4: Check
\( 420 - 204 = 216 \), which is 180% of 120.""", trick=r"180% of 120 = 1.8 × 120 = 216; 420 − 216 = 204.")
S[55] = dict(raw=r"""Step 1: Work left after the first day
\( 1 - \dfrac{4}{7} = \dfrac{3}{7} \)
Step 2: Work done on the second day
\( \dfrac{2}{5} \times \dfrac{3}{7} = \dfrac{6}{35} \)
Step 3: Work left now
\( \dfrac{3}{7} - \dfrac{6}{35} = \dfrac{15 - 6}{35} = \dfrac{9}{35} \)
Step 4: Total work
\( \dfrac{9}{35} \text{ of total} = 18 \Rightarrow \text{total} = 18 \times \dfrac{35}{9} = 70 \) units""", trick=r"Remaining = 3/7 × 3/5 = 9/35 of the work = 18 → whole = 70.")
S[56] = dict(raw=r"""Step 1: Work done by A
\( 2 \times 5 = 10 \) units
Step 2: Work done by B
\( 6 \times 2 = 12 \) units; total \( = 22 \) units
Step 3: Wages per unit
\( \dfrac{2750}{22} = ₹125 \)
Step 4: Shares and difference
A gets \( 10 \times 125 = ₹1250 \), B gets \( 12 \times 125 = ₹1500 \); difference \( = 1500 - 1250 = ₹250 \)""", trick=r"Wages are shared in the ratio of work done, 10:12; difference 2 parts of 22.")
S[57] = dict(raw=r"""Step 1: Total distance to cross
\( 238 + 238 = 476 \) m (sum of both lengths)
Step 2: Relative speed in opposite directions
\( s + s = 2s \) (same speed s each)
Step 3: Use distance = speed × time
\( 2s \times 14 = 476 \Rightarrow 2s = 34 \)
Step 4: Speed of each train
\( s = 17 \) m/s""", trick=r"Opposite directions → add the speeds; distance = sum of lengths.")
S[58] = dict(raw=r"""Step 1: Take a convenient distance
Let the total distance be 600 km (divisible by 3, 40 and 50). One-third = 200 km, the rest = 400 km.
Step 2: Time for each part
\( \dfrac{200}{40} = 5 \) h and \( \dfrac{400}{50} = 8 \) h
Step 3: Total time
\( 5 + 8 = 13 \) h
Step 4: Average speed
\( \dfrac{600}{13} \) km/hr""", trick=r"Average speed = total distance ÷ total time (not the average of the speeds).")
S[59] = dict(raw=r"""Step 1: Take a convenient cost price
Let \( \text{CP} = 24 \) (divisible by 3 and 8).
Step 2: Marked price
\( \dfrac{8}{3} \times 24 = 64 \)
Step 3: Selling price
\( \dfrac{5}{8} \times 64 = 40 \)
Step 4: Profit percentage
\( \dfrac{40 - 24}{24} \times 100 = \dfrac{16}{24} \times 100 = \dfrac{200}{3}\% \)""", trick=r"SP/CP = 8/3 × 5/8 = 5/3 → profit 2/3 = 66⅔%.")
S[60] = dict(raw=r"""Step 1: Selling price after discount
\( 6000 \times \dfrac{70}{100} = ₹4200 \)
Step 2: Relation of SP and CP
A 50% profit means \( \text{SP} = \dfrac{150}{100} \times \text{CP} \)
Step 3: Find CP
\( \text{CP} = 4200 \times \dfrac{100}{150} = ₹2800 \)
Step 4: Check
\( 2800 \times 1.5 = 4200 \) ✓""", trick=r"CP = MP × (1 − d) ÷ (1 + p) = 6000 × 0.7 ÷ 1.5.")
