S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket
\( 18 \div 2 = 9 \)
Step 2: Solve “of”
“33 of 1” means \( 33 \times 1 = 33 \)
Step 3: Write the expression again
\( 91 - 42 + 33 + 9 + 27 - 13 \)
Step 4: Simplify
\( 91 + 33 + 9 + 27 = 160 \) and \( 160 - 42 - 13 = 105 \)""", trick=r"“of” means multiply and is done before + and −.")
S[42] = dict(raw=r"""Step 1: Write the numbers using the HCF
Let the numbers be \( 12a \) and \( 12b \), where a and b are co-prime.
Step 2: Use the sum
\( 12a + 12b = 156 \Rightarrow a + b = 13 \)
Step 3: Use the LCM
\( \text{LCM} = 12ab = 480 \Rightarrow ab = 40 \). Two co-prime numbers with sum 13 and product 40 are 5 and 8.
Step 4: Find the numbers and check
\( 12 \times 5 = 60 \) and \( 12 \times 8 = 96 \); \( 60 + 96 = 156 \) ✓ and \( 60 \times 96 = 5760 = 12 \times 480 \) ✓""", trick=r"Numbers = HCF × a and HCF × b; a + b = sum ÷ HCF, a × b = LCM ÷ HCF.")
S[43] = dict(raw=r"""Step 1: Add the whole-number parts
\( 6 + 4 - 2 - 1 = 7 \)
Step 2: Take the LCM of the denominators
LCM of 3, 2, 4, 6 is 12: \( \dfrac{1}{3} = \dfrac{4}{12} \), \( \dfrac{1}{2} = \dfrac{6}{12} \), \( \dfrac{1}{4} = \dfrac{3}{12} \), \( \dfrac{1}{6} = \dfrac{2}{12} \)
Step 3: Combine the fractions
\( \dfrac{4 + 6 - 3 - 2}{12} = \dfrac{5}{12} \)
Step 4: Answer
\( 7 + \dfrac{5}{12} = 7\dfrac{5}{12} \)""", trick=r"Handle whole parts and fraction parts separately, then join them.")
S[44] = dict(raw=r"""Step 1: Find the square roots
\( \sqrt{0.04} = 0.2 \), \( \sqrt{0.16} = 0.4 \), \( \sqrt{0.36} = 0.6 \)
Step 2: Simplify each bracket
\( \dfrac{0.2}{0.4} = 0.5 \), \( \dfrac{0.8}{0.4} = 2 \), \( \dfrac{1.2}{0.6} = 2 \)
Step 3: Multiply
\( 0.5 \times 2 \times 2 \)
Step 4: Answer
\( 0.5 \times 4 = 2 \)""", trick=r"√0.04 = 0.2, √0.16 = 0.4, √0.36 = 0.6 — then the brackets give 0.5, 2, 2.")
S[45] = dict(raw=r"""Step 1: Write the equation
\( \sqrt{x + 1} = 5 \)
Step 2: Square both sides
\( x + 1 = 5^{2} = 25 \)
Step 3: Solve for x
\( x = 25 - 1 = 24 \)
Step 4: Check
\( \sqrt{24 + 1} = \sqrt{25} = 5 \) ✓""", trick=r"Remove a square root by squaring both sides.")
S[46] = dict(raw=r"""Step 1: Take three consecutive even numbers
Let them be \( x - 2 \), \( x \) and \( x + 2 \).
Step 2: Use the sum
\( (x - 2) + x + (x + 2) = 3x = 72 \)
Step 3: Solve
\( x = \dfrac{72}{3} = 24 \), so the numbers are 22, 24 and 26.
Step 4: Answer
The largest number is \( 24 + 2 = 26 \) (check: \( 22 + 24 + 26 = 72 \) ✓).""", trick=r"Middle number = sum ÷ 3; largest = middle + 2.")
S[47] = dict(raw=r"""Step 1: Use the identity
\( (a + b)^{2} + (a - b)^{2} = 2(a^{2} + b^{2}) \) with \( a = \sqrt{11} \), \( b = \sqrt{4} \)
Step 2: Simplify the numerator
\( 2(11 + 4) = 2 \times 15 = 30 \)
Step 3: Divide by the denominator
\( \dfrac{30}{10\sqrt{15}} = \dfrac{3}{\sqrt{15}} \)
Step 4: Rationalise
\( \dfrac{3}{\sqrt{15}} \times \dfrac{\sqrt{15}}{\sqrt{15}} = \dfrac{3\sqrt{15}}{15} = \dfrac{\sqrt{15}}{5} \)""", trick=r"(a + b)² + (a − b)² = 2(a² + b²) — the √ cross terms cancel.")
S[48] = dict(raw=r"""Step 1: Take only the unit digits
242 → 2, 367 → 7, 847 → 7
Step 2: Multiply the first two
\( 2 \times 7 = 14 \) → unit digit 4
Step 3: Multiply by the third
\( 4 \times 7 = 28 \) → unit digit 8
Step 4: Answer
The unit digit of the product is 8.""", trick=r"Unit digit of a product depends only on the unit digits: 2 × 7 × 7 → 8.")
S[49] = dict(raw=r"""Step 1: Use Pythagoras in the rectangle
\( \text{diagonal}^{2} = l^{2} + b^{2} \Rightarrow 13^{2} = 12^{2} + b^{2} \)
Step 2: Find the breadth
\( b^{2} = 169 - 144 = 25 \Rightarrow b = 5 \) cm
Step 3: Area formula
\( \text{Area} = l \times b \)
Step 4: Answer
\( 12 \times 5 = 60 \) square cm""", trick=r"5–12–13 is a Pythagorean triplet.")
S[50] = dict(raw=r"""Step 1: Use the identity
\( (a - b)^{2} + 4ab = a^{2} - 2ab + b^{2} + 4ab = (a + b)^{2} \)
Step 2: Put a = 540 and b = 460
The expression becomes \( (540 + 460)^{2} \)
Step 3: Add
\( 540 + 460 = 1000 \)
Step 4: Answer
\( 1000^{2} = 1000000 \)""", trick=r"(a − b)² + 4ab = (a + b)².")
S[51] = dict(raw=r"""Step 1: Total age of E, F and G
\( 40 \times 3 = 120 \) years
Step 2: Write the given sum
\( E + F = 50 \) years
Step 3: Subtract
\( G = 120 - 50 \)
Step 4: Answer
\( G = 70 \) years""", trick=r"Total = average × number of people.")
S[52] = dict(raw=r"""Step 1: Find X
\( X = \dfrac{40}{100} \times 60 = 24 \)
Step 2: Find Y
\( Y = \dfrac{50}{100} \times 40 = 20 \)
Step 3: Add
\( X + Y = 24 + 20 \)
Step 4: Answer
\( X + Y = 44 \)""", trick=r"40% of 60 = 24 and 50% of 40 = 20.")
S[53] = dict(raw=r"""Step 1: Loss is a percentage of CP
\( 28\% \text{ of CP} = 98 \)
Step 2: Find CP
\( \text{CP} = \dfrac{98 \times 100}{28} = 350 \), i.e. ₹350
Step 3: Find SP
\( \text{SP} = \text{CP} - \text{loss} = 350 - 98 \)
Step 4: Answer
\( \text{SP} = 252 \), i.e. ₹252""", trick=r"CP = loss × 100 ÷ loss%, then SP = CP − loss.")
S[54] = dict(raw=r"""Step 1: Write the condition
Profit at ₹1200 = \( 1200 - \text{CP} \); loss at ₹1000 = \( \text{CP} - 1000 \); so \( 1200 - \text{CP} = 9(\text{CP} - 1000) \)
Step 2: Solve for CP
\( 1200 - \text{CP} = 9\,\text{CP} - 9000 \Rightarrow 10\,\text{CP} = 10200 \Rightarrow \text{CP} = 1020 \)
Step 3: Selling price for 20% profit
\( \text{SP} = 1020 \times \dfrac{120}{100} \)
Step 4: Answer
\( \text{SP} = 1224 \), i.e. ₹1224""", trick=r"Set profit = 9 × loss, solve for CP, then add 20%.")
S[55] = dict(raw=r"""Step 1: Share left after the matriculates
\( 100\% - 30\% = 70\% \) of the employees
Step 2: Post-graduates
60% of the remaining are graduates, so the post-graduates are the other 40% of the remaining: \( 40\% \text{ of } 70\% = 28\% \) of all employees
Step 3: Total employees
\( 28\% = 84 \Rightarrow \text{total} = \dfrac{84 \times 100}{28} = 300 \)
Step 4: Matriculates
\( 30\% \text{ of } 300 = 90 \)""", trick=r"Post-graduates = 0.7 × 0.4 = 28% of the total.")
S[56] = dict(raw=r"""Step 1: One day's work of each
A: \( \dfrac{1}{8} \), B: \( \dfrac{1}{12} \), C: \( \dfrac{1}{24} \)
Step 2: Add them (LCM 24)
\( \dfrac{3}{24} + \dfrac{2}{24} + \dfrac{1}{24} = \dfrac{6}{24} \)
Step 3: Simplify
\( \dfrac{6}{24} = \dfrac{1}{4} \) of the work in one day
Step 4: Answer
Together they finish the work in 4 days.""", trick=r"Total work = 24 units: A 3, B 2, C 1 per day → 24 ÷ 6 = 4 days.")
S[57] = dict(raw=r"""Step 1: Write the efficiencies
Let P's one-day work be p, Q's be q and R's be r. Then \( q + r = 2p \) and \( p + r = 1.5q \).
Step 2: Use the 90 days
Q and R together finish in 90 days, so \( q + r = \dfrac{1}{90} \).
Step 3: Find P's rate
\( 2p = \dfrac{1}{90} \Rightarrow p = \dfrac{1}{180} \)
Step 4: Answer
P alone takes 180 days. (The second clue only fixes q and r: \( q = 1.2p \), \( r = 0.8p \).)""", trick=r"“Q + R are 2 times as efficient as P” → P takes 2 × 90 = 180 days.")
S[58] = dict(raw=r"""Step 1: Distance to be covered
When two trains cross, the distance is the sum of their lengths: \( 165 + 165 = 330 \) m
Step 2: Relative speed
In opposite directions the speeds add: \( s + s = 2s \)
Step 3: Use time
\( 2s = \dfrac{330}{15} = 22 \) m/s
Step 4: Answer
\( s = 11 \) m/s""", trick=r"Opposite directions: relative speed = sum; distance = sum of lengths.")
S[59] = dict(raw=r"""Step 1: Distance in each hour
1st hour 20 km, 2nd 30 km, 3rd 40 km, 4th 50 km, 5th 60 km, 6th 70 km
Step 2: Add hour by hour
\( 20 + 30 + 40 + 50 + 60 = 200 \) km after 5 hours
Step 3: Add the 6th hour
\( 200 + 70 = 270 \) km
Step 4: Answer
The bus covers 270 km in exactly 6 hours.""", trick=r"Sum of an AP: \( \dfrac{n}{2}[2a + (n - 1)d] = 3(40 + 50) = 270 \) for n = 6.")
S[60] = dict(raw=r"""Step 1: Marked price of one article
SP after 15% discount = ₹60, so \( \text{MP} = \dfrac{60 \times 100}{85} = \dfrac{1200}{17} \)
Step 2: Cost price of one article
Profit 30%, so \( \text{CP} = \dfrac{60 \times 100}{130} = \dfrac{600}{13} \)
Step 3: Profit if sold at MP
\( \dfrac{\text{MP}}{\text{CP}} = \dfrac{1200}{17} \times \dfrac{13}{600} = \dfrac{26}{17} \approx 1.5294 \)
Step 4: Answer
Profit % \( = (1.5294 - 1) \times 100 \approx 52.94\% \)""", trick=r"New profit% = (130 ÷ 85 − 1) × 100 = 52.94% — the number of articles does not matter.")
