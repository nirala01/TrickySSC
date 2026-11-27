S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first
\( 36 + 14 = 50 \).
Step 2: Multiply
\( 50 \times 2 = 100 \).
Step 3: Rewrite the expression
\( 62 + 83 - 38 + 100 - 89 \).
Step 4: Add and subtract from left to right
\( 145 - 38 = 107 \), \( 107 + 100 = 207 \), \( 207 - 89 = 118 \).""", trick=r"Positives \( 62 + 83 + 100 = 245 \); negatives \( 38 + 89 = 127 \); \( 245 - 127 = 118 \).")
S[42] = dict(raw=r"""Step 1: Division and the bracket first
\( 62 \div 2 = 31 \) and \( 27 \times 2 = 54 \).
Step 2: Rewrite the expression
\( 45 + 31 - 16 + 54 + 38 - 21 \).
Step 3: Add all the positive terms
\( 45 + 31 + 54 + 38 = 168 \).
Step 4: Subtract the negative terms
\( 16 + 21 = 37 \), so \( 168 - 37 = 131 \).""", trick=r"BODMAS: divide and bracket first → \( 168 - 37 = 131 \).")
S[43] = dict(raw=r"""Step 1: Cube roots
\( \sqrt[3]{0.027} = 0.3 \) (since \( 0.3^{3} = 0.027 \)), \( \sqrt[3]{0.064} = 0.4 \) and \( \sqrt[3]{0.216} = 0.6 \).
Step 2: Square root
\( \sqrt{0.49} = 0.7 \) (since \( 0.7^{2} = 0.49 \)).
Step 3: Substitute
\( 0.3 + 0.7 + 0.4 - 0.6 \).
Step 4: Simplify
\( 1.0 + 0.4 = 1.4 \) and \( 1.4 - 0.6 = 0.8 \).""", trick=r"\( 0.3 + 0.7 + 0.4 - 0.6 = 0.8 \).")
S[44] = dict(raw=r"""Step 1: Compare the two radicands
\( 306.25 \) becomes \( 0.000000030625 \) when the decimal point moves 10 places to the left.
Step 2: Use the rule for square roots
Moving the decimal 2 places in the number moves it 1 place in the square root, so 10 places in the number means 5 places in the root.
Step 3: Move the decimal in 17.5
\( 17.5 \) with the decimal moved 5 places left is \( 0.000175 \).
Step 4: Check
\( 0.000175^{2} = 0.000000030625 \) ✓. So \( \sqrt{0.000000030625} = 0.000175 \).""", trick=r"Decimal shifts in the root are half of those in the number: \( 10 \div 2 = 5 \) places.")
S[45] = dict(raw=r"""Step 1: Simplify the first fraction
\( \dfrac{0.16}{0.0004} = \dfrac{1600}{4} = 400 \), so \( \sqrt{400} = 20 \).
Step 2: Simplify the second root
\( \sqrt{\dfrac{0.25}{0.49}} = \dfrac{\sqrt{0.25}}{\sqrt{0.49}} = \dfrac{0.5}{0.7} = \dfrac{5}{7} \).
Step 3: Multiply
\( 20 \times \dfrac{5}{7} = \dfrac{100}{7} \).
Step 4: Answer
The value is \( \dfrac{100}{7} \).""", trick=r"\( \sqrt{400} \times \dfrac{5}{7} = \dfrac{100}{7} \).")
S[46] = dict(raw=r"""Step 1: Write the formula
Perimeter of a square \( = 4 \times \text{side} \).
Step 2: Substitute the side
\( 4 \times 15 \).
Step 3: Calculate
\( 4 \times 15 = 60 \).
Step 4: Answer
The perimeter is \( 60 \) cm.""", trick=r"\( 4 \times 15 = 60 \) cm.")
S[47] = dict(raw=r"""Step 1: Write the formula
Perimeter of a rectangle \( = 2(l + b) \).
Step 2: Substitute the values
\( 2(9 + 4) \).
Step 3: Calculate
\( 2 \times 13 = 26 \).
Step 4: Answer
The perimeter is \( 26 \) cm.""", trick=r"\( 2(9 + 4) = 26 \) cm.")
S[48] = dict(raw=r"""Step 1: Recall the rules
A number is divisible by 4 if its last two digits form a number divisible by 4, and by 9 if the sum of its digits is divisible by 9.
Step 2: Test 10263
Last two digits 63, and \( 63 \div 4 \) leaves 3, so not divisible by 4. Digit sum \( 1 + 0 + 2 + 6 + 3 = 12 \), not divisible by 9.
Step 3: Test the others
10260: digit sum \( 9 \) → divisible by 9. 10116: last two digits 16 → divisible by 4. 10296: last two digits 96 → divisible by 4 (and digit sum 18 → by 9 too).
Step 4: Answer
Only \( 10263 \) is divisible by neither 4 nor 9.""", trick=r"Last two digits for 4, digit sum for 9 → 10263 fails both.")
S[49] = dict(raw=r"""Step 1: Use the identity
\( 2(a^{2} + b^{2}) - (a - b)^{2} = 2a^{2} + 2b^{2} - a^{2} + 2ab - b^{2} = a^{2} + 2ab + b^{2} = (a + b)^{2} \).
Step 2: Put the values
Here \( a = 412 \) and \( b = 188 \).
Step 3: Add
\( a + b = 412 + 188 = 600 \).
Step 4: Square
\( 600^{2} = 360000 \).""", trick=r"\( 2(a^{2} + b^{2}) - (a - b)^{2} = (a + b)^{2} = 600^{2} = 360000 \).")
S[50] = dict(raw=r"""Step 1: Total of all 14 numbers
\( 14 \times 45 = 630 \).
Step 2: Total of the remaining 9 numbers
\( 14 - 5 = 9 \) numbers with average 35, so their total is \( 9 \times 35 = 315 \).
Step 3: Total of the 5 numbers
\( 630 - 315 = 315 \).
Step 4: Find x
\( x = \dfrac{315}{5} = 63 \).""", trick=r"\( 5x = 630 - 315 = 315 \Rightarrow x = 63 \).")
S[51] = dict(raw=r"""Step 1: Find the LCM of 12 and 15
\( 12 = 2^{2} \times 3 \), \( 15 = 3 \times 5 \), so \( \text{LCM} = 2^{2} \times 3 \times 5 = 60 \). Any number divisible by both is a multiple of 60.
Step 2: Smallest 3-digit multiple of 60
\( 60 \times 2 = 120 \), so \( A = 120 \).
Step 3: Largest 3-digit multiple of 60
\( 999 \div 60 = 16 \) remainder 39, so \( B = 60 \times 16 = 960 \).
Step 4: Find B − A
\( 960 - 120 = 840 \).""", trick=r"Multiples of 60: \( 960 - 120 = 840 \).")
S[52] = dict(raw=r"""Step 1: Understand the condition
Every group must have the same size and each class must be split exactly, so the group size must divide 36, 60 and 72.
Step 2: Factorise
\( 36 = 2^{2} \times 3^{2} \), \( 60 = 2^{2} \times 3 \times 5 \), \( 72 = 2^{3} \times 3^{2} \).
Step 3: Find the HCF
\( \text{HCF} = 2^{2} \times 3 = 12 \).
Step 4: Answer
The maximum number of students in each group is \( 12 \) (3, 5 and 6 groups from the three classes).""", trick=r"Maximum equal group = HCF\( (36, 60, 72) = 12 \).")
S[53] = dict(raw=r"""Step 1: Write the formula
Rate of tax \( = \dfrac{\text{tax}}{\text{value}} \times 100 \).
Step 2: Substitute
\( \dfrac{36}{900} \times 100 \).
Step 3: Simplify
\( \dfrac{36}{9} = 4 \).
Step 4: Answer
The rate of tax is 4 percent.""", trick=r"\( 36 \) on \( 900 \) → \( 4 \) per \( 100 \) → 4%.")
S[54] = dict(raw=r"""Step 1: Profit is a percentage of the cost price
30% of CP \( = 120 \).
Step 2: Find the CP
\( \text{CP} = \dfrac{120 \times 100}{30} = 400 \).
Step 3: Find the SP
\( \text{SP} = \text{CP} + \text{profit} = 400 + 120 = 520 \).
Step 4: Answer
The selling price is ₹520.""", trick=r"\( 120 \div 0.3 = 400 \); \( 400 + 120 = 520 \).")
S[55] = dict(raw=r"""Step 1: Take a convenient SP
Let \( \text{SP} = 100 \).
Step 2: Find the profit
Profit is 25% of SP, so profit \( = 25 \).
Step 3: Find the CP
\( \text{CP} = \text{SP} - \text{profit} = 100 - 25 = 75 \).
Step 4: Form the ratio
Profit to CP \( = 25 : 75 = 1 : 3 \).""", trick=r"Profit \( = \dfrac{1}{4} \) of SP → CP \( = \dfrac{3}{4} \) of SP → \( 1 : 3 \).")
S[56] = dict(raw=r"""Step 1: Take the initial income as I
Expenditure \( = 0.4I \), so saving \( = 0.6I \).
Step 2: Apply the increases
New income \( = 1.5I \) and new expenditure \( = 0.4I \times 1.4 = 0.56I \).
Step 3: New saving
\( 1.5I - 0.56I = 0.94I \).
Step 4: Use the given saving
\( 0.94I = 4700 \), so \( I = \dfrac{4700}{0.94} = 5000 \). The initial income is ₹5000.""", trick=r"New saving \( = 1.5 - 0.56 = 0.94 \) of the old income → \( 4700 \div 0.94 = 5000 \).")
S[57] = dict(raw=r"""Step 1: Write the efficiencies
A is twice as good as B, so if B does 1 unit a day, A does 2 units a day.
Step 2: Find the total work
Together they do \( 2 + 1 = 3 \) units a day for 24 days, so the work \( = 3 \times 24 = 72 \) units.
Step 3: Time for B alone
\( \dfrac{72}{1} = 72 \) days.
Step 4: Check
A alone would take \( 72 \div 2 = 36 \) days, and \( \dfrac{1}{36} + \dfrac{1}{72} = \dfrac{3}{72} = \dfrac{1}{24} \) ✓.""", trick=r"Efficiency \( 2 : 1 \) → work \( = 3 \times 24 = 72 \) → B alone 72 days.")
S[58] = dict(raw=r"""Step 1: Write the one-day work
Let the one-day work of R, M and T be \( 2k \), \( 3k \) and \( 4k \).
Step 2: Total work done by each
R: \( 2k \times 6 = 12k \), M: \( 3k \times 8 = 24k \), T: \( 4k \times 10 = 40k \).
Step 3: Share the money in the ratio of work
Total \( = 12k + 24k + 40k = 76k \), so each part is worth \( \dfrac{760}{76} = 10 \).
Step 4: M's share
\( 24 \times 10 = 240 \). M gets ₹240.""", trick=r"Work ratio \( 12 : 24 : 40 \) (76 parts) → M \( = \dfrac{24}{76} \times 760 = 240 \).")
S[59] = dict(raw=r"""Step 1: Speed of B
\( \dfrac{42}{7} = 6 \) km/h.
Step 2: Speed of C
\( \dfrac{108}{9} = 12 \) km/h.
Step 3: Form the ratio
\( 6 : 12 \).
Step 4: Simplify
\( 6 : 12 = 1 : 2 \).""", trick=r"\( 6 \) km/h vs \( 12 \) km/h → \( 1 : 2 \).")
S[60] = dict(raw=r"""Step 1: Relate speed and time
For the same distance, time is inversely proportional to speed. At 90% speed, time becomes \( \dfrac{10}{9} \) of the usual time T.
Step 2: Find the extra time
Extra time \( = \dfrac{10}{9}T - T = \dfrac{T}{9} \).
Step 3: Use the delay
\( \dfrac{T}{9} = 10 \) minutes, so \( T = 90 \) minutes.
Step 4: Check
At the slower speed he takes \( \dfrac{10}{9} \times 90 = 100 \) minutes, which is 10 minutes more ✓.""", trick=r"Speed \( \dfrac{9}{10} \) → time \( \dfrac{10}{9} \) → extra \( \dfrac{1}{9} \) of T \( = 10 \) → T \( = 90 \).")
