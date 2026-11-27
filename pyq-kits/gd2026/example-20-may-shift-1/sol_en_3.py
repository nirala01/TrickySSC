S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket
\( 36 + 18 = 54 \).
Step 2: Multiply
\( 54 \times 2 = 108 \).
Step 3: Rewrite the expression
\( 79 + 65 - 41 + 108 - 97 \).
Step 4: Add the positives, then subtract the negatives
\( 79 + 65 + 108 = 252 \) and \( 41 + 97 = 138 \), so the value \( = 252 - 138 = 114 \).""", trick=r"Positives \( 252 \), negatives \( 138 \) → \( 252 - 138 = 114 \).")
S[42] = dict(raw=r"""Step 1: Solve the bracket
\( 42 \div 6 = 7 \).
Step 2: Solve “of”
\( 14 \text{ of } 2 = 14 \times 2 = 28 \).
Step 3: Rewrite the expression
\( 88 + 33 - 26 + 28 + 7 - 19 \).
Step 4: Add the positives, then subtract the negatives
\( 88 + 33 + 28 + 7 = 156 \) and \( 26 + 19 = 45 \), so the value \( = 156 - 45 = 111 \).""", trick=r"BODMAS: bracket and “of” first → \( 156 - 45 = 111 \).")
S[43] = dict(raw=r"""Step 1: Find the cube
\( (1.5)^{3} = 1.5 \times 1.5 \times 1.5 = 3.375 \).
Step 2: Work out the numerator
\( 8 \times 3.375 = 27 \), so the numerator \( = 27 + 1 = 28 \).
Step 3: Work out the denominator
\( (3)^{2} - 2 = 9 - 2 = 7 \).
Step 4: Divide
\( \dfrac{28}{7} = 4 \).""", trick=r"\( 8(1.5)^{3} = (2 \times 1.5)^{3} = 3^{3} = 27 \) → \( \dfrac{28}{7} = 4 \).")
S[44] = dict(raw=r"""Step 1: Use the rule for multiplying roots
\( \sqrt{a} \times \sqrt{b} = \sqrt{a \times b} \).
Step 2: Multiply the numbers under the root
\( \sqrt{45} \times \sqrt{5} = \sqrt{45 \times 5} = \sqrt{225} \).
Step 3: Take the square root
\( \sqrt{225} = 15 \), because \( 15 \times 15 = 225 \).
Step 4: Check another way
\( \sqrt{45} = 3\sqrt{5} \), so \( 3\sqrt{5} \times \sqrt{5} = 3 \times 5 = 15 \) ✓.""", trick=r"\( \sqrt{45 \times 5} = \sqrt{225} = 15 \).")
S[45] = dict(raw=r"""Step 1: Rationalise the fraction
\( \dfrac{1}{\sqrt{10} - \sqrt{3}} = \dfrac{\sqrt{10} + \sqrt{3}}{(\sqrt{10} - \sqrt{3})(\sqrt{10} + \sqrt{3})} \).
Step 2: Simplify the denominator
\( (\sqrt{10})^{2} - (\sqrt{3})^{2} = 10 - 3 = 7 \), so the fraction \( = \dfrac{\sqrt{10} + \sqrt{3}}{7} \).
Step 3: Add the two terms
\( (\sqrt{10} + \sqrt{3}) + \dfrac{\sqrt{10} + \sqrt{3}}{7} = (\sqrt{10} + \sqrt{3})\left(1 + \dfrac{1}{7}\right) \).
Step 4: Final value
\( 1 + \dfrac{1}{7} = \dfrac{8}{7} \), so the value \( = \dfrac{8}{7}(\sqrt{10} + \sqrt{3}) \).""", trick=r"\( \dfrac{1}{\sqrt{a} - \sqrt{b}} = \dfrac{\sqrt{a} + \sqrt{b}}{a - b} \); here \( a - b = 7 \), so the total is \( \dfrac{8}{7} \) of \( \sqrt{10} + \sqrt{3} \).")
S[46] = dict(raw=r"""Step 1: Write the formula
Perimeter of a square \( = 4 \times \text{side} \).
Step 2: Put in the value
Perimeter \( = 4 \times 6.5 \).
Step 3: Multiply
\( 4 \times 6 = 24 \) and \( 4 \times 0.5 = 2 \), so \( 4 \times 6.5 = 24 + 2 = 26 \).
Step 4: Answer
The perimeter of the square is 26 cm.""", trick=r"\( 4 \times 6.5 = 26 \) cm.")
S[47] = dict(raw=r"""Step 1: Write the formula
Area of a square \( = \text{side} \times \text{side} \).
Step 2: Put in the value
Area \( = 12 \times 12 \).
Step 3: Multiply
\( 12 \times 12 = 144 \).
Step 4: Answer
The area of the square is 144 square cm. (The perimeter would be \( 4 \times 12 = 48 \) cm — do not mix up the two.)""", trick=r"\( 12^{2} = 144 \) square cm.")
S[48] = dict(raw=r"""Step 1: Recall the two rules
A number is divisible by 3 if the sum of its digits is divisible by 3, and by 4 if the number formed by its last two digits is divisible by 4.
Step 2: Test 9041
Digit sum \( = 9 + 0 + 4 + 1 = 14 \), which is not divisible by 3. Last two digits 41 are not divisible by 4. So 9041 is divisible by neither.
Step 3: Test 90120 and 10020
90120: digit sum \( = 12 \) (divisible by 3) and last two digits 20 (divisible by 4). 10020: digit sum \( = 3 \) and last two digits 20 — both are divisible by 3 and by 4.
Step 4: Test 10068
Digit sum \( = 1 + 0 + 0 + 6 + 8 = 15 \) (divisible by 3) and last two digits 68 \( = 4 \times 17 \) (divisible by 4). So the only number divisible by neither 3 nor 4 is 9041.""", trick=r"9041: digit sum 14 (not a multiple of 3), ends in 41 (odd, so not a multiple of 4).")
S[49] = dict(raw=r"""Step 1: Let \( a = 345 \) and \( b = 155 \)
The expression is \( 2(a^{2} + b^{2}) - (a - b)^{2} \).
Step 2: Expand
\( 2a^{2} + 2b^{2} - (a^{2} - 2ab + b^{2}) = a^{2} + 2ab + b^{2} \).
Step 3: Recognise the identity
\( a^{2} + 2ab + b^{2} = (a + b)^{2} \).
Step 4: Put in the values
\( a + b = 345 + 155 = 500 \), so the value \( = 500^{2} = 250000 \).""", trick=r"\( 2(a^{2} + b^{2}) - (a - b)^{2} = (a + b)^{2} = 500^{2} = 250000 \).")
S[50] = dict(raw=r"""Step 1: Sum of the original 110 numbers
\( 110 \times 70.5 = 7755 \).
Step 2: Total count after the addition
\( 110 + 40 = 150 \) numbers.
Step 3: Sum of all 150 numbers
\( 150 \times 55.1 = 8265 \).
Step 4: Sum of the 40 new numbers
\( 8265 - 7755 = 510 \).""", trick=r"New sum − old sum \( = 150 \times 55.1 - 110 \times 70.5 = 8265 - 7755 = 510 \).")
S[51] = dict(raw=r"""Step 1: Find the LCM of 14 and 20
\( 14 = 2 \times 7 \) and \( 20 = 2^{2} \times 5 \), so LCM \( = 2^{2} \times 5 \times 7 = 140 \). A number divisible by both 14 and 20 is a multiple of 140.
Step 2: Smallest 3-digit multiple (A)
140 itself is a 3-digit number, so \( A = 140 \).
Step 3: Largest 3-digit multiple (B)
\( 140 \times 7 = 980 \) and \( 140 \times 8 = 1120 \) (4 digits), so \( B = 980 \).
Step 4: Subtract
\( B - A = 980 - 140 = 840 \).""", trick=r"Multiples of 140: first 140, seventh 980 → gap \( = 6 \times 140 = 840 \).")
S[52] = dict(raw=r"""Step 1: Use the property
If a number leaves the same remainder with several numbers, it divides their differences exactly. The largest such number is the HCF of the differences.
Step 2: Find the differences
\( 146 - 122 = 24 \), \( 170 - 146 = 24 \), \( 194 - 170 = 24 \).
Step 3: Take the HCF
All the differences are 24, so the HCF is 24.
Step 4: Check
\( 122 = 24 \times 5 + 2 \), \( 146 = 24 \times 6 + 2 \), \( 170 = 24 \times 7 + 2 \), \( 194 = 24 \times 8 + 2 \) — the remainder is 2 every time ✓. So the required number is 24.""", trick=r"Same remainder → HCF of the differences \( = 24 \).")
S[53] = dict(raw=r"""Step 1: Write A in terms of B
A is 25% less than B, so \( A = 75\% \text{ of } B = \dfrac{3}{4}B \).
Step 2: Put in the value of A
\( \dfrac{3}{4}B = 270 \).
Step 3: Solve for B
\( B = 270 \times \dfrac{4}{3} = 90 \times 4 = 360 \).
Step 4: Check
25% of 360 \( = 90 \), and \( 360 - 90 = 270 \) ✓.""", trick=r"3 parts = 270 → 1 part = 90 → B = 4 parts = 360.")
S[54] = dict(raw=r"""Step 1: Relate loss to cost price
Loss % is calculated on the cost price (CP), so \( 30\% \text{ of CP} = 69 \).
Step 2: Find the cost price
\( \text{CP} = 69 \times \dfrac{100}{30} = 230 \), i.e. ₹230.
Step 3: Find the selling price
\( \text{SP} = \text{CP} - \text{loss} = 230 - 69 = 161 \), i.e. ₹161.
Step 4: Check
\( \dfrac{69}{230} \times 100 = 30\% \) ✓.""", trick=r"30% = ₹69 → 10% = ₹23 → SP = 70% = \( 7 \times 23 = 161 \).")
S[55] = dict(raw=r"""Step 1: Total maximum marks
\( 600 + 200 = 800 \).
Step 2: Total marks obtained
\( 60\% \text{ of } 800 = \dfrac{60}{100} \times 800 = 480 \).
Step 3: Marks in the second exam
\( 480 - 380 = 100 \).
Step 4: Percentage in the second exam
\( \dfrac{100}{200} \times 100 = 50\% \).""", trick=r"Needs 480 in all; has 380 → 100 out of 200 = 50%.")
S[56] = dict(raw=r"""Step 1: Take the prices from the ratio
Let cost price \( = 9k \) and selling price \( = 11k \).
Step 2: Find the profit
Profit \( = 11k - 9k = 2k \).
Step 3: Write the required ratio
\( \dfrac{\text{Profit}}{\text{Cost price}} = \dfrac{2k}{9k} = \dfrac{2}{9} \).
Step 4: Answer
Profit to cost price is 2 to 9 (a profit of \( \dfrac{2}{9} \times 100 \approx 22.2\% \)). The ratio 2 to 11 would compare profit with the selling price, not the cost price.""", trick=r"Profit \( = 11 - 9 = 2 \) parts; CP = 9 parts → 2 to 9.")
S[57] = dict(raw=r"""Step 1: Turn efficiency into time
Efficiency of A to B is 3 to 4. Time is inversely proportional to efficiency, so the time of A to B is 4 to 3.
Step 2: Write the times
Let A take \( 4k \) days and B take \( 3k \) days.
Step 3: Use the difference
\( 4k - 3k = 12 \Rightarrow k = 12 \).
Step 4: Find x
A takes \( x = 4 \times 12 = 48 \) days (and B takes 36 days, which is 12 days less ✓).""", trick=r"Time ratio 4 to 3; 1 part = 12 days → A = 4 parts = 48 days.")
S[58] = dict(raw=r"""Step 1: Convert women into men
A woman is twice as efficient as a man, so 1 woman = 2 men.
Step 2: Convert the 10 women
\( 10 \text{ women} = 10 \times 2 = 20 \text{ men} \).
Step 3: Total work force in men
\( 5 + 20 = 25 \) men complete the work in 15 days.
Step 4: Answer
The number of days is the same (15), so 25 men are needed. Check: work \( = 25 \times 15 = 375 \) man-days, and \( 375 \div 15 = 25 \) ✓.""", trick=r"1 woman = 2 men → \( 5 + 20 = 25 \) men for the same 15 days.")
S[59] = dict(raw=r"""Step 1: Speed of B
\( \dfrac{48}{6} = 8 \) km/h.
Step 2: Speed of C
\( \dfrac{100}{10} = 10 \) km/h.
Step 3: Write the ratio
\( \dfrac{\text{Speed of B}}{\text{Speed of C}} = \dfrac{8}{10} \).
Step 4: Simplify
\( \dfrac{8}{10} = \dfrac{4}{5} \), so the ratio of the speeds is 4 to 5.""", trick=r"8 km/h and 10 km/h → 4 to 5.")
S[60] = dict(raw=r"""Step 1: Use the pole
A train crosses a pole by covering its own length. If the speed is \( v \) m/s, the length of the train \( = 25v \) metres.
Step 2: Use the platform
To cross the platform the train covers its own length plus 500 m in 75 s, so \( 25v + 500 = 75v \).
Step 3: Solve
\( 50v = 500 \Rightarrow v = 10 \) m/s.
Step 4: Check
Length of the train \( = 25 \times 10 = 250 \) m; \( \dfrac{250 + 500}{75} = 10 \) m/s ✓.""", trick=r"The extra 500 m takes \( 75 - 25 = 50 \) s → speed \( = \dfrac{500}{50} = 10 \) m/s.")
