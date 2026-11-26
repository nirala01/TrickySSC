S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first (“of” means multiply)
\( 18 \text{ of } 2 = 18 \times 2 = 36 \).
Step 2: Rewrite the expression
\( 88 + 21 - 34 + 28 + 36 + 17 - 13 \).
Step 3: Add all the positive terms and the negative terms
Positive: \( 88 + 21 + 28 + 36 + 17 = 190 \). Negative: \( 34 + 13 = 47 \).
Step 4: Subtract
\( 190 - 47 = 143 \).""", trick=r"Group plus terms and minus terms, then subtract once.")
S[42] = dict(raw=r"""Step 1: Write the numbers using the HCF
Let the numbers be 80a and 80b, where a and b are co-prime.
Step 2: Use LCM = HCF × a × b
\( 80ab = 3600 \Rightarrow ab = 45 \). Co-prime pairs: (45, 1) and (9, 5).
Step 3: Use the difference
\( 80(a - b) = 320 \Rightarrow a - b = 4 \). Only (9, 5) gives a difference of 4.
Step 4: Find the numbers and check
\( 80 \times 9 = 720 \) and \( 80 \times 5 = 400 \); \( 720 - 400 = 320 \) ✓ and \( 720 \times 400 = 288000 = 80 \times 3600 \) ✓.""", trick=r"Numbers = HCF × co-prime pair; product of the pair = LCM ÷ HCF.")
S[43] = dict(raw=r"""Step 1: Separate the whole numbers and the fractions
\( (3 + 33 + 333 + 3333) + \left(\dfrac{1}{2} + \dfrac{1}{2} + \dfrac{1}{2} + \dfrac{1}{2}\right) \).
Step 2: Add the whole numbers
\( 3 + 33 + 333 + 3333 = 3702 \).
Step 3: Add the fractions
\( 4 \times \dfrac{1}{2} = 2 \).
Step 4: Add both parts
\( 3702 + 2 = 3704 \).""", trick=r"Add whole parts and fraction parts separately.")
S[44] = dict(raw=r"""Step 1: Use the identity
\( (a + b)^{2} - (a - b)^{2} = 4ab \).
Step 2: Apply it with a = 7.5 and b = 2.5
Numerator \( = 4 \times 7.5 \times 2.5 \).
Step 3: Divide by the denominator
\( \dfrac{4 \times 7.5 \times 2.5}{7.5 \times 2.5} = 4 \).
Step 4: Check by direct working
\( 10^{2} - 5^{2} = 75 \) and \( 7.5 \times 2.5 = 18.75 \); \( 75 \div 18.75 = 4 \) ✓.""", trick=r"(a + b)² − (a − b)² = 4ab, so the answer is always 4 when divided by ab.")
S[45] = dict(raw=r"""Step 1: Use the identity
\( (a + b)^{2} + (a - b)^{2} = 2(a^{2} + b^{2}) \).
Step 2: Put a = √5 and b = √3
\( a^{2} = 5 \) and \( b^{2} = 3 \).
Step 3: Substitute
\( 2(5 + 3) = 2 \times 8 = 16 \).
Step 4: Check
\( (\sqrt{5} + \sqrt{3})^{2} = 8 + 2\sqrt{15} \) and \( (\sqrt{5} - \sqrt{3})^{2} = 8 - 2\sqrt{15} \); the sum is 16 ✓.""", trick=r"(a + b)² + (a − b)² = 2(a² + b²) — the root terms cancel.")
S[46] = dict(raw=r"""Step 1: Write three consecutive even numbers
Let them be x − 2, x and x + 2.
Step 2: Use the sum
\( (x - 2) + x + (x + 2) = 3x = 24 \Rightarrow x = 8 \).
Step 3: Write the numbers
The numbers are 6, 8 and 10.
Step 4: Find the product
\( 6 \times 8 \times 10 = 480 \).""", trick=r"Middle number = sum ÷ 3.")
S[47] = dict(raw=r"""Step 1: Use the identity
\( (a + b)^{2} - (a - b)^{2} = 4ab \).
Step 2: Put a = 5 and b = √3
\( 4 \times 5 \times \sqrt{3} = 20\sqrt{3} \).
Step 3: Subtract the last term
\( 20\sqrt{3} - 4\sqrt{3} = 16\sqrt{3} \).
Step 4: Check by expansion
\( (28 + 10\sqrt{3}) - (28 - 10\sqrt{3}) = 20\sqrt{3} \), and \( 20\sqrt{3} - 4\sqrt{3} = 16\sqrt{3} \) ✓.""", trick=r"4ab first, then handle the extra term.")
S[48] = dict(raw=r"""Step 1: Use the identity
\( (a + b)^{2} - (a - b)^{2} = 4ab \), with a = 290 and b = 210.
Step 2: Apply it
\( 4 \times 290 \times 210 = 243600 \).
Step 3: Test the options
\( 580 \times 420 = 243600 \) ✓ (it is \( 2 \times 290 \) times \( 2 \times 210 \)). \( 530 \times 430 = 227900 \), \( 480 \times 530 = 254400 \), \( 590 \times 470 = 277300 \).
Step 4: Check directly
\( 500^{2} - 80^{2} = 250000 - 6400 = 243600 \) ✓.""", trick=r"4ab = (2a) × (2b) = 580 × 420.")
S[49] = dict(raw=r"""Step 1: Use Pythagoras in the rectangle
\( \text{diagonal}^{2} = l^{2} + b^{2} \).
Step 2: Substitute the values
\( 10^{2} = 6^{2} + b^{2} \Rightarrow 100 = 36 + b^{2} \).
Step 3: Solve for b
\( b^{2} = 64 \Rightarrow b = 8 \) cm.
Step 4: Check
6, 8, 10 is a Pythagorean triplet (3, 4, 5 doubled) ✓.""", trick=r"6-8-10 is the 3-4-5 triplet doubled.")
S[50] = dict(raw=r"""Step 1: Start from the largest 4-digit number
The largest 4-digit number is 9999.
Step 2: Divide by 72
\( 9999 = 72 \times 138 + 63 \), so the remainder is 63.
Step 3: Subtract the remainder
\( 9999 - 63 = 9936 \).
Step 4: Check
\( 9936 \div 72 = 138 \) ✓ (9936 is divisible by 8 and by 9: digit sum 27).""", trick=r"Largest n-digit multiple = 999… − remainder.")
S[51] = dict(raw=r"""Step 1: Total age of E, F and G
\( 3 \times 50 = 150 \) years.
Step 2: Use E + F
E + F = 96 years.
Step 3: Find G
\( G = 150 - 96 = 54 \) years.
Step 4: Check
\( (96 + 54) \div 3 = 50 \) ✓.""", trick=r"Missing value = average × count − known total.")
S[52] = dict(raw=r"""Step 1: Find the fail percentage
50% passed, so \( 100\% - 50\% = 50\% \) failed.
Step 2: Find the total
50% of total = 20000, so total \( = 20000 \times \dfrac{100}{50} = 40000 \).
Step 3: Find the number who passed
50% of 40000 = 20000.
Step 4: Check
\( 20000 + 20000 = 40000 \) ✓.""", trick=r"Pass % = Fail % here, so passed = failed = 20000.")
S[53] = dict(raw=r"""Step 1: Note the prices
CP = ₹5000 and SP = ₹4000; SP < CP, so there is a loss.
Step 2: Find the loss
\( 5000 - 4000 = 1000 \).
Step 3: Find the loss percentage
\( \dfrac{1000}{5000} \times 100 = 20\% \).
Step 4: Answer
The loss is 20 percent.""", trick=r"Loss % is always on CP: 1000 out of 5000 = 1/5 = 20%.")
S[54] = dict(raw=r"""Step 1: Write profit and loss in terms of CP
Profit at ₹1600 = 1600 − CP; loss at ₹1200 = CP − 1200.
Step 2: Use “profit = 19 × loss”
\( 1600 - CP = 19(CP - 1200) \Rightarrow 1600 + 22800 = 20 \times CP \).
Step 3: Find CP
\( CP = \dfrac{24400}{20} = 1220 \).
Step 4: Find SP for 30% profit
\( 1220 \times \dfrac{130}{100} = 1586 \), so SP = ₹1586. Check: profit 380 = 19 × 20 ✓.""", trick=r"CP = (1600 + 19 × 1200) ÷ 20.")
S[55] = dict(raw=r"""Step 1: Take the salary as 100
Let the salary be 100.
Step 2: Apply the 40% increase
\( 100 \times 1.4 = 140 \).
Step 3: Apply the 25% decrease
\( 140 \times 0.75 = 105 \).
Step 4: Find the net change
\( 105 - 100 = 5 \), so the net change is a 5% increase. (Formula: \( 40 - 25 - \dfrac{40 \times 25}{100} = 5 \).)""", trick=r"Net % = a − b − ab/100 for an increase a followed by a decrease b.")
S[56] = dict(raw=r"""Step 1: Work left after the first day
He did \( \dfrac{2}{3} \), so \( 1 - \dfrac{2}{3} = \dfrac{1}{3} \) was left.
Step 2: Work done on the second day
\( \dfrac{1}{4} \) of \( \dfrac{1}{3} = \dfrac{1}{12} \).
Step 3: Work still left
\( \dfrac{1}{3} - \dfrac{1}{12} = \dfrac{1}{4} \) of the total.
Step 4: Find the total
\( \dfrac{1}{4} \) of total = 20 units, so total = \( 20 \times 4 = 80 \) units.""", trick=r"Left = 1/3 × 3/4 = 1/4 of the work.")
S[57] = dict(raw=r"""Step 1: One-day work of P and Q together
\( \dfrac{1}{12} \).
Step 2: One-day work of R
\( \dfrac{1}{18} \).
Step 3: One-day work of all three
\( \dfrac{1}{12} + \dfrac{1}{18} = \dfrac{3 + 2}{36} = \dfrac{5}{36} \).
Step 4: Find the time
\( \dfrac{36}{5} = 7.2 \) days.""", trick=r"Together time = (12 × 18) ÷ (12 + 18) = 216 ÷ 30 = 7.2.")
S[58] = dict(raw=r"""Step 1: Total distance to cross each other
\( 250 + 350 = 600 \) m.
Step 2: Relative speed (opposite directions add)
\( \dfrac{600}{60} = 10 \) m/s.
Step 3: Speed of each train
The speeds are equal, so each is \( \dfrac{10}{2} = 5 \) m/s.
Step 4: Convert to km/hr
\( 5 \times \dfrac{18}{5} = 18 \) km/hr.""", trick=r"Opposite directions → add speeds; m/s × 18/5 = km/h.")
S[59] = dict(raw=r"""Step 1: Distance in each hour
The speeds hour by hour are 22, 30, 38, 46, 54, 62 … km/h (an AP with d = 8).
Step 2: Add hour by hour
\( 22 + 30 = 52 \); \( + 38 = 90 \); \( + 46 = 136 \); \( + 54 = 190 \); \( + 62 = 252 \).
Step 3: Count the hours
252 km is reached at the end of the 6th hour.
Step 4: Check with the AP sum
\( \dfrac{6}{2}(2 \times 22 + 5 \times 8) = 3 \times 84 = 252 \) ✓.""", trick=r"Sum of an AP: n/2 × (2a + (n − 1)d).")
S[60] = dict(raw=r"""Step 1: Take the marked price as 100
Let MP = 100.
Step 2: Apply the first discount of 30%
\( 100 \times 0.7 = 70 \).
Step 3: Apply the second discount of 20%
\( 70 \times 0.8 = 56 \), so SP = 56.
Step 4: Find the ratio
\( \text{MP} : \text{SP} = 100 : 56 \), which simplifies to \( 25 : 14 \).""", trick=r"SP = MP × 0.7 × 0.8 = 0.56 MP.")
