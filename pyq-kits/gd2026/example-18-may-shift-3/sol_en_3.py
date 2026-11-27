S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first
\( 43 + 12 = 55 \).
Step 2: Multiply
\( 55 \times 2 = 110 \).
Step 3: Add and subtract from left to right
\( 79 + 88 - 54 + 110 - 89 = 167 - 54 + 110 - 89 = 113 + 110 - 89 \).
Step 4: Finish
\( 223 - 89 = 134 \).""", trick=r"Bracket → multiply → then add and subtract left to right.")
S[42] = dict(raw=r"""Step 1: Solve the bracket
\( 14 \times 2 = 28 \).
Step 2: Divide
\( 33 \div 3 = 11 \).
Step 3: Rewrite the expression
\( 68 + 28 - 22 + 11 - 19 + 28 \).
Step 4: Add and subtract from left to right
\( 96 - 22 = 74 \), \( 74 + 11 = 85 \), \( 85 - 19 = 66 \), \( 66 + 28 = 94 \).""", trick=r"Positives \( 68 + 28 + 11 + 28 = 135 \); negatives \( 22 + 19 = 41 \); \( 135 - 41 = 94 \).")
S[43] = dict(raw=r"""Step 1: Find the cube root
\( 13^{3} = 2197 \), so \( \sqrt[3]{2.197} = 1.3 \) (three decimal places become one).
Step 2: Find the square root
\( 11^{2} = 121 \), so \( \sqrt{1.21} = 1.1 \) (two decimal places become one).
Step 3: Multiply
\( 1.3 \times 1.1 = 1.43 \).
Step 4: Answer
The value is 1.43.""", trick=r"\( \sqrt[3]{2.197} = 1.3 \), \( \sqrt{1.21} = 1.1 \), product 1.43.")
S[44] = dict(raw=r"""Step 1: Find each square root
\( \sqrt{225} = 15 \), \( \sqrt{25} = 5 \), \( \sqrt{81} = 9 \).
Step 2: Divide first (BODMAS)
\( 15 \div 5 = 3 \).
Step 3: Add
\( x = 3 + 9 = 12 \).
Step 4: Find 2x
\( 2x = 2 \times 12 = 24 \).""", trick=r"\( x = 3 + 9 = 12 \Rightarrow 2x = 24 \).")
S[45] = dict(raw=r"""Step 1: Recall the formula
Area of a square \( = \text{side}^{2} \).
Step 2: Put in the side
Side = 6 cm.
Step 3: Calculate
\( 6^{2} = 6 \times 6 = 36 \).
Step 4: Answer
The area is 36 square cm.""", trick=r"Area = side × side = 36.")
S[46] = dict(raw=r"""Step 1: Recall the formula
Diagonal of a square \( = \text{side} \times \sqrt{2} \).
Step 2: Why it works
By Pythagoras, \( d^{2} = a^{2} + a^{2} = 2a^{2} \Rightarrow d = a\sqrt{2} \).
Step 3: Put in the side
\( d = 7 \times \sqrt{2} = 7\sqrt{2} \).
Step 4: Answer
The diagonal is \( 7\sqrt{2} \) cm (about 9.9 cm).""", trick=r"Diagonal of a square = side × √2.")
S[47] = dict(raw=r"""Step 1: Recall the rules
Divisible by 3 → digit sum divisible by 3. Divisible by 11 → (sum of alternate digits) difference is 0 or a multiple of 11.
Step 2: Test 10019
Digit sum \( = 1 + 0 + 0 + 1 + 9 = 11 \) → not divisible by 3. Alternate sums \( (9 + 0 + 1) - (1 + 0) = 9 \) → not divisible by 11.
Step 3: Test the others
9999: digit sum 36 (divisible by 3) and \( 9999 = 11 \times 909 \). 10032: digit sum 6 (divisible by 3). 9042: digit sum 15 (divisible by 3).
Step 4: Answer
Only 10019 is divisible by neither 3 nor 11.""", trick=r"Check digit sums first: only 10019 has a sum (11) not divisible by 3.")
S[48] = dict(raw=r"""Step 1: Rule for 6
A number is divisible by 6 if it is divisible by both 2 and 3.
Step 2: Check 2
36P2 ends in 2, so it is always even ✓.
Step 3: Check 3
Digit sum \( = 3 + 6 + P + 2 = 11 + P \) must be a multiple of 3, so P = 1, 4 or 7.
Step 4: Answer
Among the options, only P = 7 works (\( 11 + 7 = 18 \)); 3672 \( = 6 \times 612 \) ✓.""", trick=r"Even + digit sum \( 11 + P \) a multiple of 3 → P = 7.")
S[49] = dict(raw=r"""Step 1: Solve the inner roots
\( \sqrt{400} = 20 \) and \( \sqrt{25} = 5 \).
Step 2: Add them
\( 20 + 5 = 25 \).
Step 3: Take the outer root
\( \sqrt{25} = 5 \).
Step 4: Answer
The value is 5.""", trick=r"Work from inside: \( \sqrt{20 + 5} = 5 \).")
S[50] = dict(raw=r"""Step 1: Old total
\( 4 \times 28 = 112 \).
Step 2: New total
\( 4 \times 34 = 136 \).
Step 3: Increase in total
\( 136 - 112 = 24 \).
Step 4: New number
New number \( = 24 + 24 = 48 \).""", trick=r"New number = old number + (rise in average × count) \( = 24 + 6 \times 4 = 48 \).")
S[51] = dict(raw=r"""Step 1: LCM of 3, 4 and 5
\( \text{LCM} = 60 \).
Step 2: Form of B
B leaves remainder 1 with each divisor, so \( B = 60k + 1 \): 61, 121, …, 601, 661, …
Step 3: Use B = 700 − A
B must be just below 700, so the largest such value is \( 60 \times 11 + 1 = 661 \).
Step 4: Find A
\( A = 700 - 661 = 39 \). Check: \( 661 = 3 \times 220 + 1 = 4 \times 165 + 1 = 5 \times 132 + 1 \) ✓.""", trick=r"B = LCM × k + 1 = 661, so A = 39.")
S[52] = dict(raw=r"""Step 1: Use HCF
The maximum number of boys = HCF of 156 and 234.
Step 2: Find the HCF
\( 234 - 156 = 78 \), and \( 156 = 78 \times 2 \), \( 234 = 78 \times 3 \), so HCF = 78.
Step 3: Chips per boy
\( 156 \div 78 = 2 \) chips each (and \( 234 \div 78 = 3 \) toffees each).
Step 4: Answer
Each boy gets 2 chips.""", trick=r"HCF(156, 234) = 78 boys → \( \dfrac{156}{78} = 2 \).")
S[53] = dict(raw=r"""Step 1: Take parts
Let CP = 2k and SP = 5k.
Step 2: Profit in parts
Profit \( = 5k - 2k = 3k \).
Step 3: Find k
\( 3k = 210 \Rightarrow k = 70 \).
Step 4: Selling price
SP \( = 5k = 5 \times 70 = ₹350 \).""", trick=r"3 parts = ₹210 → 1 part = 70 → SP = 5 parts = ₹350.")
S[54] = dict(raw=r"""Step 1: Take values
Let B = 1, so A = 5 (A is 5 times B).
Step 2: Difference
\( A - B = 5 - 1 = 4 \).
Step 3: Percentage less (compare with A)
\( \dfrac{4}{5} \times 100 = 80\% \).
Step 4: Answer
B is 80% less than A.""", trick=r"Less than A → divide the difference by A: \( \dfrac{4}{5} = 80\% \).")
S[55] = dict(raw=r"""Step 1: Find the cost price
CP \( = \text{SP} - \text{Profit} = 4200 - 200 = ₹4000 \).
Step 2: Recall the formula
Profit% \( = \dfrac{\text{Profit}}{\text{CP}} \times 100 \).
Step 3: Calculate
\( \dfrac{200}{4000} \times 100 = 5\% \).
Step 4: Answer
The profit is 5 per cent (always on CP, not on SP).""", trick=r"Profit% is on CP: \( \dfrac{200}{4000} = 5\% \).")
S[56] = dict(raw=r"""Step 1: Take the initial income as I
Expenditure \( = 0.5I \), saving \( = 0.5I \).
Step 2: After the increase
Income \( = 1.4I \); expenditure \( = 0.5I \times 1.3 = 0.65I \).
Step 3: New saving
\( 1.4I - 0.65I = 0.75I \), and this equals ₹7500.
Step 4: Solve
\( I = \dfrac{7500}{0.75} = ₹10000 \). Check: new income 14000, new expenditure 6500, saving 7500 ✓.""", trick=r"Take income 100: new saving \( = 140 - 65 = 75 \) → 75 units = ₹7500 → 100 units = ₹10000.")
S[57] = dict(raw=r"""Step 1: One-day work of M and N
M \( = \dfrac{1}{40} \), N \( = \dfrac{1}{80} \).
Step 2: Together in one day
\( \dfrac{1}{40} + \dfrac{1}{80} = \dfrac{2 + 1}{80} = \dfrac{3}{80} \).
Step 3: Work in 8 days
\( 8 \times \dfrac{3}{80} = \dfrac{24}{80} = \dfrac{3}{10} \).
Step 4: As a percentage
\( \dfrac{3}{10} \times 100 = 30\% \).""", trick=r"Total work 80 units: M 2/day, N 1/day → 24 units in 8 days = 30%.")
S[58] = dict(raw=r"""Step 1: One-day work
P + Q \( = \dfrac{1}{9} \), R \( = \dfrac{1}{18} \).
Step 2: All three together
\( \dfrac{1}{9} + \dfrac{1}{18} = \dfrac{2 + 1}{18} = \dfrac{3}{18} = \dfrac{1}{6} \) of the work per day.
Step 3: Time for the required part
Time \( = \dfrac{1}{6} \div \dfrac{1}{6} = 1 \).
Step 4: Answer
They complete \( \dfrac{1}{6} \) of the work in 1 day.""", trick=r"Together they finish the whole work in 6 days, so \( \dfrac{1}{6} \) of it takes 1 day.")
S[59] = dict(raw=r"""Step 1: Bring both speeds to the same unit
\( 30 \text{ m/s} = 30 \times \dfrac{18}{5} = 108 \text{ km/hr} \).
Step 2: Distances in one hour
A covers 50 km and B covers 108 km.
Step 3: Form the ratio
\( 50 : 108 \).
Step 4: Simplify
Divide both by 2: \( 25 : 54 \).""", trick=r"m/s → km/hr: × 18/5; then same time, so distance ratio = speed ratio.")
S[60] = dict(raw=r"""Step 1: Crossing the pole
Length of train \( L = 12v \) (it covers its own length in 12 s).
Step 2: Crossing the platform
\( L + 550 = 22v \).
Step 3: Subtract the two equations
\( 550 = 22v - 12v = 10v \Rightarrow v = 55 \) m/s.
Step 4: Length
\( L = 12 \times 55 = 660 \) m. So the train is 660 m long and moves at 55 m/s.""", trick=r"Extra 10 s covers the 550 m platform → speed 55 m/s.")
