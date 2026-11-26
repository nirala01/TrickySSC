S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket
\( 47 + 15 = 62 \)
Step 2: Multiply
\( 62 \times 2 = 124 \)
Step 3: Add and subtract from left to right
\( 73 + 88 - 64 + 124 - 99 = 161 - 64 + 124 - 99 = 122 \)""", trick=r"BODMAS: bracket, then ×, then + and − left to right.")
S[42] = dict(raw=r"""Step 1: Solve "of" and the division
\( 33 \text{ of } 1 = 33 \times 1 = 33 \) and \( 26 \div 2 = 13 \)
Step 2: Rewrite the expression
\( 63 + 41 - 29 + 33 - 18 + 13 \)
Step 3: Add and subtract
\( 104 - 29 = 75,\; 75 + 33 = 108,\; 108 - 18 = 90,\; 90 + 13 = 103 \)""", trick=r"“of” means multiply and is done before ÷.")
S[43] = dict(raw=r"""Step 1: Convert the limits to decimals
\( \dfrac{1}{4} = 0.25 \) and \( \dfrac{3}{4} = 0.75 \)
Step 2: Convert each option
\( \dfrac{7}{11} \approx 0.636,\; \dfrac{11}{13} \approx 0.846,\; \dfrac{9}{11} \approx 0.818,\; \dfrac{15}{17} \approx 0.882 \)
Step 3: Compare
Only \( 0.636 \) lies between 0.25 and 0.75, so \( \dfrac{7}{11} \) is the answer.""", trick=r"Each wrong option is above 0.8; only one fraction stays below 0.75.")
S[44] = dict(raw=r"""Step 1: Spot the identity
\( (a + b)^{2} - 4ab = (a - b)^{2} \)
Step 2: Put a = 9.8 and b = 1.8
\( (9.8 - 1.8)^{2} \)
Step 3: Calculate
\( 8^{2} = 64 \)""", trick=r"(a + b)² − 4ab is always (a − b)².")
S[45] = dict(raw=r"""Step 1: Find the other diagonal
\( \text{Area} = \dfrac{1}{2} d_{1} d_{2} \Rightarrow 336 = \dfrac{1}{2} \times 14 \times d_{2} \Rightarrow d_{2} = 48 \)
Step 2: Find the side
The diagonals bisect each other at right angles, so \( \text{side} = \sqrt{7^{2} + 24^{2}} = \sqrt{49 + 576} = \sqrt{625} = 25 \)
Step 3: Perimeter
\( 4 \times 25 = 100 \) cm""", trick=r"Half-diagonals 7 and 24 make the 7-24-25 triangle.")
S[46] = dict(raw=r"""Step 1: Use the property
Adjacent angles of a parallelogram add up to \( 180^{\circ} \).
Step 2: Divide in the ratio \( 4 : 5 \)
\( 4x + 5x = 180 \Rightarrow 9x = 180 \Rightarrow x = 20 \)
Step 3: Larger angle
\( 5x = 5 \times 20 = 100^{\circ} \)""", trick=r"180 ÷ 9 = 20 per part; larger angle = 5 parts.")
S[47] = dict(raw=r"""Step 1: Find the HCF
11 is prime and does not divide 30, so \( Y = \text{HCF} = 1 \).
Step 2: Find the LCM
For co-prime numbers, \( X = \text{LCM} = 11 \times 30 = 330 \).
Step 3: Calculate X − 2Y
\( 330 - 2 \times 1 = 328 \)""", trick=r"Co-prime numbers: HCF = 1, LCM = product.")
S[48] = dict(raw=r"""Step 1: Write the numbers
With HCF 7 and ratio \( 9 : 4 \), the numbers are \( 9 \times 7 = 63 \) and \( 4 \times 7 = 28 \).
Step 2: Check the LCM
\( \text{LCM} = 7 \times 9 \times 4 = 252 \) ✓
Step 3: Sum
\( 63 + 28 = 91 \)""", trick=r"Sum = HCF × (sum of ratio terms) = 7 × 13 = 91.")
S[49] = dict(raw=r"""Step 1: 50% of 600
\( \dfrac{50}{100} \times 600 = 300 \)
Step 2: 60% less than 300
A number 60% less is 40% of it: \( \dfrac{40}{100} \times 300 \)
Step 3: Calculate
\( 0.4 \times 300 = 120 \)""", trick=r"“60% less than” = “40% of”.")
S[50] = dict(raw=r"""Step 1: Rotten eggs
\( 50\% \text{ of } 450 = \dfrac{450}{2} = 225 \)
Step 2: Good eggs
\( 450 - 225 = 225 \)
Step 3: Answer
225 eggs are not rotten.""", trick=r"Half rotten means half good.")
S[51] = dict(raw=r"""Step 1: Take CP = 100
At 40% profit, \( \text{SP} = 140 \).
Step 2: Reduce both by 50%
New CP = 50 and new SP = 70.
Step 3: New profit %
\( \dfrac{70 - 50}{50} \times 100 = 40\% \)""", trick=r"Cutting CP and SP by the same % leaves profit % unchanged.")
S[52] = dict(raw=r"""Step 1: Take CP = 100
At 30% loss, \( \text{SP} = 70 \).
Step 2: Reduce both by 40%
New CP = 60 and new SP = 42.
Step 3: New loss %
\( \dfrac{60 - 42}{60} \times 100 = \dfrac{18}{60} \times 100 = 30\% \)""", trick=r"Same % change on CP and SP keeps the loss % the same.")
S[53] = dict(raw=r"""Step 1: Work done on day 1
\( \dfrac{2}{3} \times 84 = 56 \) units, leaving \( 84 - 56 = 28 \) units.
Step 2: Work done on day 2
\( \dfrac{1}{4} \times 28 = 7 \) units.
Step 3: Work remaining
\( 28 - 7 = 21 \) units""", trick=r"Remaining = 84 × 1/3 × 3/4 = 21.")
S[54] = dict(raw=r"""Step 1: Total work done
A: \( 5 \times 3 = 15 \) units; B: \( 6 \times 2 = 12 \) units.
Step 2: Ratio of shares
Shares are in the ratio of work, \( 15 : 12 = 5 : 4 \), so the difference is 1 part.
Step 3: Find A's share
\( 1 \text{ part} = ₹600 \Rightarrow \text{A's share} = 5 \times 600 = ₹3000 \)""", trick=r"Wages are shared in the ratio of total work done.")
S[55] = dict(raw=r"""Step 1: Formula
\( \text{Downstream speed} = \text{boat speed} + \text{stream speed} \)
Step 2: Substitute
\( 17 + 5 \)
Step 3: Answer
\( 22 \) km/hr""", trick=r"Downstream = add; upstream = subtract.")
S[56] = dict(raw=r"""Step 1: Present speed
36 km in 60 minutes means \( 36 \) km/hr.
Step 2: New speed
\( 36 - 20 = 16 \) km/hr
Step 3: New time
\( \dfrac{36}{16} = 2.25 \) hours \( = 2.25 \times 60 = 135 \) minutes""", trick=r"Time ∝ 1/speed: 60 × 36/16 = 135 minutes.")
S[57] = dict(raw=r"""Step 1: Let the numbers be 5x and 3x
\( \dfrac{5x + 5}{3x + 5} = \dfrac{3}{2} \)
Step 2: Solve
\( 10x + 10 = 9x + 15 \Rightarrow x = 5 \)
Step 3: Sum of the original numbers
\( 5x + 3x = 8x = 8 \times 5 = 40 \)""", trick=r"Check: 25 and 15 become 30 and 20, which is \( 3 : 2 \).")
S[58] = dict(raw=r"""Step 1: Take MP = 14
Discount \( = \dfrac{5}{14} \times 14 = 5 \), so \( \text{SP} = 9 \).
Step 2: Find CP
SP is 140% of CP, so \( \text{CP} = \dfrac{9}{1.4} = \dfrac{45}{7} \approx 6.4286 \).
Step 3: How much less than MP
\( \dfrac{14 - 6.4286}{14} \times 100 = \dfrac{7.5714}{14} \times 100 \approx 54.08\% \)""", trick=r"Take MP as the denominator of the discount fraction.")
S[59] = dict(raw=r"""Step 1: Take CP = 100
MP is 50% more, so \( \text{MP} = 150 \).
Step 2: Selling price
25% profit gives \( \text{SP} = 125 \).
Step 3: Discount %
\( \dfrac{150 - 125}{150} \times 100 = \dfrac{25}{150} \times 100 = 16.67\% \)""", trick=r"Discount % is always on MP, not CP.")
S[60] = dict(raw=r"""Step 1: Meaning of fourth proportional
If \( a : b = c : x \), then \( x = \dfrac{b \times c}{a} \).
Step 2: Substitute a = 18, b = 4, c = 45
\( x = \dfrac{4 \times 45}{18} \)
Step 3: Calculate
\( \dfrac{180}{18} = 10 \)""", trick=r"Fourth proportional = (2nd × 3rd) ÷ 1st.")
