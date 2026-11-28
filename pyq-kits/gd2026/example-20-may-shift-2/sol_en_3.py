S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket
\( 49 + 9 = 58 \).
Step 2: Do the multiplication
\( 24 \times 2 = 48 \).
Step 3: Rewrite the expression
\( 73 + 62 - 38 + 48 - 58 \).
Step 4: Add the positives, then subtract the negatives
\( 73 + 62 + 48 = 183 \) and \( 38 + 58 = 96 \), so the value \( = 183 - 96 = 87 \).""", trick=r"BODMAS: bracket and × first → \( 183 - 96 = 87 \).")
S[42] = dict(raw=r"""Step 1: Solve the bracket
\( 33 \div 3 = 11 \).
Step 2: Do the multiplication
\( 18 \times 1 = 18 \).
Step 3: Rewrite the expression
\( 84 + 36 - 11 + 29 + 18 - 22 \).
Step 4: Add the positives, then subtract the negatives
\( 84 + 36 + 29 + 18 = 167 \) and \( 11 + 22 = 33 \), so the value \( = 167 - 33 = 134 \).""", trick=r"Bracket first (\( 33 \div 3 = 11 \)) → \( 167 - 33 = 134 \).")
S[43] = dict(raw=r"""Step 1: Find the daily work of each worker
M alone takes 10 days, so full-efficiency work is \( \dfrac{1}{10} \) per day; N does \( \dfrac{1}{20} \) per day.
Step 2: Apply the efficiency of M
M works at 60% efficiency, so M does \( \dfrac{60}{100} \times \dfrac{1}{10} = 0.06 \) of the work per day. N works at full efficiency, so N does \( 0.05 \) per day.
Step 3: Add the work done in a day
Together they do \( 0.06 + 0.05 = 0.11 \) of the work per day.
Step 4: Find the time
Time \( = \dfrac{1}{0.11} = \dfrac{100}{11} \approx 9.09 \) days, which is about 9 days.""", trick=r"Together \( 0.06 + 0.05 = 0.11 \) per day → \( \dfrac{1}{0.11} \approx 9 \) days.")
S[44] = dict(raw=r"""Step 1: Add the parts of the ratio
\( 7 + 5 = 12 \) parts make up all the balls.
Step 2: Find the value of one part
\( 60 \div 12 = 5 \) balls per part.
Step 3: Find the red balls
Red balls \( = 7 \times 5 = 35 \).
Step 4: Check
Blue balls \( = 5 \times 5 = 25 \), and \( 35 + 25 = 60 \) ✓, with the ratio \( 35 : 25 = 7 : 5 \) ✓.""", trick=r"Red \( = \dfrac{7}{12} \times 60 = 35 \).")
S[45] = dict(raw=r"""Step 1: Split every mixed number
Each term is a whole number 640 plus a fraction, so the sum is \( 640 \times 5 \) plus the sum of the fractions, because the denominators 3, 15, 35, 63 and 99 give five terms.
Step 2: Add the whole parts
\( 640 \times 5 = 3200 \).
Step 3: Add the fractions by splitting each one
\( \dfrac{1}{3} = \dfrac{1}{1 \times 3} \), \( \dfrac{1}{15} = \dfrac{1}{3 \times 5} \), \( \dfrac{1}{35} = \dfrac{1}{5 \times 7} \), \( \dfrac{1}{63} = \dfrac{1}{7 \times 9} \), \( \dfrac{1}{99} = \dfrac{1}{9 \times 11} \), and each \( \dfrac{1}{a(a+2)} = \dfrac{1}{2}\left(\dfrac{1}{a} - \dfrac{1}{a+2}\right) \). The middle terms cancel, leaving \( \dfrac{1}{2}\left(1 - \dfrac{1}{11}\right) = \dfrac{1}{2} \times \dfrac{10}{11} = \dfrac{5}{11} \).
Step 4: Join the two parts
Total \( = 3200 + \dfrac{5}{11} = 3200\dfrac{5}{11} \).""", trick=r"Five terms → \( 5 \times 640 = 3200 \); the fractions telescope to \( \dfrac{1}{2}\left(1 - \dfrac{1}{11}\right) = \dfrac{5}{11} \).")
S[46] = dict(raw=r"""Step 1: Write each fraction as 1 minus a small fraction
\( \dfrac{23}{24} = 1 - \dfrac{1}{24} \), \( \dfrac{19}{20} = 1 - \dfrac{1}{20} \), \( \dfrac{29}{30} = 1 - \dfrac{1}{30} \), \( \dfrac{14}{15} = 1 - \dfrac{1}{15} \).
Step 2: Compare the small fractions
The denominators are 24, 20, 30 and 15, and the smallest denominator gives the largest fraction: \( \dfrac{1}{15} > \dfrac{1}{20} > \dfrac{1}{24} > \dfrac{1}{30} \).
Step 3: Subtract
The more we take away from 1, the smaller the result, so the largest taken-away part \( \dfrac{1}{15} \) gives the smallest fraction.
Step 4: Check with decimals
\( \dfrac{23}{24} \approx 0.958 \), \( \dfrac{19}{20} = 0.95 \), \( \dfrac{29}{30} \approx 0.967 \), \( \dfrac{14}{15} \approx 0.933 \), so \( \dfrac{14}{15} \) is the smallest.""", trick=r"Each is 1 − (1 over n); the largest gap \( \dfrac{1}{15} \) leaves the smallest fraction \( \dfrac{14}{15} \).")
S[47] = dict(raw=r"""Step 1: Write the formula
Perimeter of a square \( = 4 \times \text{side} \).
Step 2: Put in the value
\( 4 \times \text{side} = 32 \).
Step 3: Solve for the side
\( \text{side} = \dfrac{32}{4} = 8 \) cm.
Step 4: Check
\( 4 \times 8 = 32 \) cm ✓.""", trick=r"Side \( = \dfrac{32}{4} = 8 \) cm.")
S[48] = dict(raw=r"""Step 1: Find the side from the perimeter
Perimeter \( = 4 \times \text{side} = 16 \), so \( \text{side} = \dfrac{16}{4} = 4 \) cm.
Step 2: Write the area formula
Area of a square \( = \text{side} \times \text{side} \).
Step 3: Put in the side
Area \( = 4 \times 4 \).
Step 4: Multiply
\( 4 \times 4 = 16 \) square cm.""", trick=r"Side 4 → area \( 4^{2} = 16 \) square cm.")
S[49] = dict(raw=r"""Step 1: Identify the series
\( 4 + 8 + 12 + \ldots + 88 \) is an arithmetic progression with first term \( a = 4 \) and common difference \( d = 4 \).
Step 2: Find the number of terms
\( n = \dfrac{88 - 4}{4} + 1 = 21 + 1 = 22 \).
Step 3: Use the sum formula
\( S = \dfrac{n}{2}(a + l) = \dfrac{22}{2}(4 + 88) \).
Step 4: Calculate
\( S = 11 \times 92 = 1012 \).""", trick=r"Take 4 common: \( 4(1 + 2 + \ldots + 22) = 4 \times 253 = 1012 \).")
S[50] = dict(raw=r"""Step 1: Recall the rule for 6
A number is divisible by 6 if it is divisible by both 2 and 3.
Step 2: Use the rule for 2
The last digit of 95P8 is 8, which is even, so the number is divisible by 2 for any P.
Step 3: Use the rule for 3
The digit sum \( 9 + 5 + P + 8 = 22 + P \) must be a multiple of 3. Among the digits 0, 2, 4 and 6, \( 22 + 2 = 24 \) is divisible by 3 (the others give 22, 26 and 28).
Step 4: Check
\( 9528 \div 6 = 1588 \) ✓, so \( P = 2 \).""", trick=r"Even last digit is already there; \( 22 + P \) must be a multiple of 3 → \( P = 2 \).")
S[51] = dict(raw=r"""Step 1: Find the total runs in 15 matches
\( 15 \times 38 = 570 \).
Step 2: Find the total needed for 16 matches
To have an average of 40 after 16 matches, the total must be \( 16 \times 40 = 640 \).
Step 3: Find the runs needed in the next match
\( 640 - 570 = 70 \).
Step 4: Check
\( \dfrac{570 + 70}{16} = \dfrac{640}{16} = 40 \) ✓.""", trick=r"Needed \( = 40 + 15 \times (40 - 38) = 40 + 30 = 70 \).")
S[52] = dict(raw=r"""Step 1: Find the 12 numbers
Twelve consecutive odd numbers with average 36 are centred between the 6th and 7th numbers, which are 35 and 37, so the numbers run from 25 to 47.
Step 2: Find the two new numbers
The odd number just before 25 is 23 and the one just after 47 is 49.
Step 3: Find the new sum
Old sum \( = 12 \times 36 = 432 \) and the new sum \( = 432 + 23 + 49 = 504 \).
Step 4: Find the new average
There are now 14 numbers, so the average \( = \dfrac{504}{14} = 36 \).""", trick=r"23 and 49 are equally far (13) from 36 → the average stays \( 36 \).")
S[53] = dict(raw=r"""Step 1: Prime factorise
\( 200 = 2 \times 100 = 2 \times 2 \times 50 = 2^{3} \times 5^{2} \).
Step 2: Write the formula
If \( N = p^{a} \times q^{b} \), the number of factors is \( (a + 1)(b + 1) \).
Step 3: Put in the powers
\( (3 + 1)(2 + 1) = 4 \times 3 \).
Step 4: Multiply
\( 4 \times 3 = 12 \) factors: 1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100 and 200.""", trick=r"\( 200 = 2^{3} \times 5^{2} \) → \( (3 + 1)(2 + 1) = 12 \).")
S[54] = dict(raw=r"""Step 1: Choose the method
The bells ring together again after the LCM of their intervals 6, 8, 10 and 15 seconds.
Step 2: Prime factorise
\( 6 = 2 \times 3 \), \( 8 = 2^{3} \), \( 10 = 2 \times 5 \), \( 15 = 3 \times 5 \).
Step 3: Take the highest powers
\( \text{LCM} = 2^{3} \times 3 \times 5 = 120 \) seconds.
Step 4: Convert to minutes
\( 120 \div 60 = 2 \) minutes.""", trick=r"LCM of 6, 8, 10, 15 is 120 seconds = 2 minutes.")
S[55] = dict(raw=r"""Step 1: Use the profit formula with the selling price
\( \text{SP} = \text{CP} \times \dfrac{100 + \text{profit}\%}{100} \).
Step 2: Find the cost price
\( 345 = \text{CP} \times \dfrac{115}{100} \), so \( \text{CP} = 345 \times \dfrac{100}{115} = 300 \).
Step 3: Find the profit
\( \text{Profit} = \text{SP} - \text{CP} = 345 - 300 = 45 \).
Step 4: Check
\( 15\% \text{ of } 300 = 45 \) ✓, so the profit is ₹45.""", trick=r"SP is 115% of CP, so CP \( = \dfrac{345}{115} \times 100 = 300 \); profit \( = 345 - 300 = 45 \).")
S[56] = dict(raw=r"""Step 1: Understand the data
SP − CP is the profit, so the profit is ₹150.
Step 2: Relate profit to cost price
A profit of 25% means \( \dfrac{25}{100} \times \text{CP} = 150 \), so \( \text{CP} = 150 \times 4 = 600 \).
Step 3: Find the selling price
\( \text{SP} = \text{CP} + \text{profit} = 600 + 150 = 750 \).
Step 4: Check
\( 125\% \text{ of } 600 = 750 \) ✓, so the selling price is ₹750.""", trick=r"Profit = 25% of CP = 150 → CP = 600 → SP = 750.")
S[57] = dict(raw=r"""Step 1: Take the initial income as 100 units
Expenditure \( = 70 \) units and savings \( = 100 - 70 = 30 \) units.
Step 2: Find the new income and expenditure
New income \( = 100 \times 1.6 = 160 \) units and new expenditure \( = 70 \times 1.5 = 105 \) units.
Step 3: Find the new saving
New saving \( = 160 - 105 = 55 \) units. The question gives the saving after the increase as ₹5500, so \( 55 \text{ units} = 5500 \) and 1 unit \( = 100 \).
Step 4: Find the initial income
Initial income \( = 100 \text{ units} = 100 \times 100 = 10000 \), that is ₹10000.""", trick=r"New saving \( = 1.6I - 1.05I = 0.55I = 5500 \) → \( I = 10000 \).")
S[58] = dict(raw=r"""Step 1: Take the total work as the LCM
\( \text{LCM}(18, 27, 54) = 54 \) units of work.
Step 2: Find the daily work of each
A does \( \dfrac{54}{18} = 3 \) units, B does \( \dfrac{54}{27} = 2 \) units and C does \( \dfrac{54}{54} = 1 \) unit per day, so all three together do \( 6 \) units a day.
Step 3: Find the work left after 3 days
In 3 days they do \( 6 \times 3 = 18 \) units, leaving \( 54 - 18 = 36 \) units.
Step 4: Find the time for A and C
A and C together do \( 3 + 1 = 4 \) units a day, so the remaining work takes \( \dfrac{36}{4} = 9 \) days.""", trick=r"Total 54 units; all three 6/day for 3 days = 18; the remaining \( 36 \div 4 = 9 \) days.")
S[59] = dict(raw=r"""Step 1: Write the formula
Time \( = \dfrac{\text{distance}}{\text{speed}} \).
Step 2: Time for 126 km
\( \dfrac{126}{18} = 7 \) hours.
Step 3: Time for 72 km
\( \dfrac{72}{18} = 4 \) hours.
Step 4: Find the difference
\( 7 - 4 = 3 \) hours (also \( \dfrac{126 - 72}{18} = \dfrac{54}{18} = 3 \)).""", trick=r"Difference \( = \dfrac{126 - 72}{18} = 3 \) hours.")
S[60] = dict(raw=r"""Step 1: Let the numbers be a and b and write the equation
\( 0.09a + 0.03b = 3(0.02a + 0.05b) \).
Step 2: Expand the right side
\( 3 \times 0.02a = 0.06a \) and \( 3 \times 0.05b = 0.15b \), so \( 0.09a + 0.03b = 0.06a + 0.15b \).
Step 3: Collect like terms
\( 0.09a - 0.06a = 0.15b - 0.03b \), which gives \( 0.03a = 0.12b \).
Step 4: Find the ratio
\( \dfrac{a}{b} = \dfrac{0.12}{0.03} = 4 \), so the ratio of the first number to the second is \( 4 : 1 \).""", trick=r"\( 0.03a = 0.12b \) → \( a : b = 4 : 1 \).")
