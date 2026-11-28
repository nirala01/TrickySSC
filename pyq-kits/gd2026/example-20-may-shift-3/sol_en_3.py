S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket
\( 36 + 21 = 57 \).
Step 2: Do the multiplication
\( 48 \times 2 = 96 \).
Step 3: Rewrite the expression
\( 96 - 58 + 81 - 57 + 96 \).
Step 4: Add the positives, then subtract the negatives
\( 96 + 81 + 96 = 273 \) and \( 58 + 57 = 115 \), so the value \( = 273 - 115 = 158 \).""", trick=r"BODMAS: bracket and × first → \( 273 - 115 = 158 \).")
S[42] = dict(raw=r"""Step 1: Solve the bracket
\( 14 \times 2 = 28 \).
Step 2: Do the division
\( 16 \div 4 = 4 \).
Step 3: Rewrite the expression
\( 86 + 55 - 39 + 28 - 28 + 4 \). Here \( + 28 \) and \( - 28 \) cancel.
Step 4: Finish the addition and subtraction
\( 86 + 55 = 141 \), \( 141 - 39 = 102 \) and \( 102 + 4 = 106 \).""", trick=r"\( +28 \) and \( -28 \) cancel → \( 86 + 55 - 39 + 4 = 106 \).")
S[43] = dict(raw=r"""Step 1: Change the limits to decimals
\( 2\dfrac{3}{10} = 2.3 \) and \( 2\dfrac{4}{5} = 2.8 \). The required fraction must lie between 2.3 and 2.8.
Step 2: Test the fractions with denominator 18
\( \dfrac{41}{18} = 2\dfrac{5}{18} \approx 2.28 \), which is just below 2.3. \( \dfrac{47}{18} = 2\dfrac{11}{18} \approx 2.61 \), which lies between 2.3 and 2.8.
Step 3: Test the other two fractions
\( \dfrac{59}{20} = 2.95 \) and \( \dfrac{62}{21} = 2\dfrac{20}{21} \approx 2.95 \); both are above 2.8.
Step 4: Answer
Only \( \dfrac{47}{18} \) satisfies \( 2.3 < 2.61 < 2.8 \).""", trick=r"Limits 2.3 and 2.8 → only \( \dfrac{47}{18} \approx 2.61 \) falls inside.")
S[44] = dict(raw=r"""Step 1: Recall the identity
\( (a + b)^2 - (a - b)^2 = 4ab \).
Step 2: Identify a and b
Here \( a = \sqrt{5} \) and \( b = \sqrt{2} \).
Step 3: Substitute
Value \( = 4 \times \sqrt{5} \times \sqrt{2} = 4\sqrt{10} \).
Step 4: Check by expanding
\( (\sqrt{5} + \sqrt{2})^2 = 7 + 2\sqrt{10} \) and \( (\sqrt{5} - \sqrt{2})^2 = 7 - 2\sqrt{10} \); their difference is \( 4\sqrt{10} \) ✓.""", trick=r"\( (a + b)^2 - (a - b)^2 = 4ab \) → \( 4\sqrt{5 \times 2} = 4\sqrt{10} \).")
S[45] = dict(raw=r"""Step 1: Aim for a perfect square
We want to write \( 5 + 2\sqrt{6} \) as \( (\sqrt{a} + \sqrt{b})^2 = a + b + 2\sqrt{ab} \).
Step 2: Find a and b
We need \( a + b = 5 \) and \( ab = 6 \). The numbers 3 and 2 work, since \( 3 + 2 = 5 \) and \( 3 \times 2 = 6 \).
Step 3: Rewrite and take the root
\( 5 + 2\sqrt{6} = (\sqrt{3} + \sqrt{2})^2 \), so \( \sqrt{5 + 2\sqrt{6}} = \sqrt{3} + \sqrt{2} \).
Step 4: Check
\( (\sqrt{3} + \sqrt{2})^2 = 3 + 2 + 2\sqrt{6} = 5 + 2\sqrt{6} \) ✓.""", trick=r"\( \sqrt{(a + b) + 2\sqrt{ab}} = \sqrt{a} + \sqrt{b} \): sum 5, product 6 → 3 and 2.")
S[46] = dict(raw=r"""Step 1: Recall the formula
Area of a square \( = \text{side}^2 \).
Step 2: Substitute the side
Side \( = 8 \) cm, so area \( = 8^2 \).
Step 3: Calculate
\( 8 \times 8 = 64 \) square cm.
Step 4: Check
\( \sqrt{64} = 8 \), which is the given side ✓.""", trick=r"Area \( = \text{side}^2 = 8^2 = 64 \).")
S[47] = dict(raw=r"""Step 1: Recall the perimeter formula
Perimeter of a square \( = 4 \times \text{side} \).
Step 2: Find the side
Side \( = \dfrac{36}{4} = 9 \) cm.
Step 3: Find the area
Area \( = \text{side}^2 = 9^2 = 81 \) square cm.
Step 4: Check
\( 4 \times 9 = 36 \) cm, the given perimeter ✓.""", trick=r"Side \( = \dfrac{36}{4} = 9 \) → area \( = 9^2 = 81 \).")
S[48] = dict(raw=r"""Step 1: Recall the identity
\( a^2 + b^2 + c^2 + 2(ab + bc + ca) = (a + b + c)^2 \).
Step 2: Match the terms
Here \( a = 15 \), \( b = 10 \) and \( c = 25 \), and the bracket holds \( ab + bc + ca \) exactly.
Step 3: Add the three numbers
\( 15 + 10 + 25 = 50 \).
Step 4: Square the sum
Value \( = 50^2 = 2500 \). Check: \( 225 + 100 + 625 = 950 \) and \( 2(150 + 250 + 375) = 1550 \), and \( 950 + 1550 = 2500 \) ✓.""", trick=r"It is \( (a + b + c)^2 \) → \( (15 + 10 + 25)^2 = 50^2 = 2500 \).")
S[49] = dict(raw=r"""Step 1: Recall the identity
\( a^2 + b^2 + c^2 + 2(ab + bc + ca) = (a + b + c)^2 \).
Step 2: Match the terms
Here \( a = 22 \), \( b = 18 \) and \( c = 30 \), and the bracket holds \( ab + bc + ca \) exactly.
Step 3: Add the three numbers
\( 22 + 18 + 30 = 70 \).
Step 4: Square the sum
Value \( = 70^2 = 4900 \). Check: \( 484 + 324 + 900 = 1708 \) and \( 2(396 + 540 + 660) = 3192 \), and \( 1708 + 3192 = 4900 \) ✓.""", trick=r"It is \( (a + b + c)^2 \) → \( (22 + 18 + 30)^2 = 70^2 = 4900 \).")
S[50] = dict(raw=r"""Step 1: Find the sum of the original 80 numbers
Sum \( = 80 \times 23.5 = 1880 \).
Step 2: Find the new count
\( 80 + 20 = 100 \) numbers.
Step 3: Find the sum of all 100 numbers
Sum \( = 100 \times 32.1 = 3210 \).
Step 4: Find the sum of the new numbers
Sum of the 20 new numbers \( = 3210 - 1880 = 1330 \).""", trick=r"\( 100 \times 32.1 - 80 \times 23.5 = 3210 - 1880 = 1330 \).")
S[51] = dict(raw=r"""Step 1: Combine the three divisors
5, 7 and 11 are prime, so a number divisible by all three must be divisible by \( 5 \times 7 \times 11 = 385 \).
Step 2: Use the test of 5
A multiple of 5 ends in 0 or 5, so 1927 and 1933 are out. Only 1935 and 1925 remain.
Step 3: Divide by 385
\( 385 \times 5 = 1925 \), so 1925 is divisible by 385.
Step 4: Check the other number
\( 1935 = 1925 + 10 \), and 10 is not a multiple of 7 or 11, so 1935 fails. Also \( 1925 \div 7 = 275 \) and \( 1925 \div 11 = 175 \) ✓.""", trick=r"LCM of 5, 7, 11 is 385 → \( 385 \times 5 = 1925 \).")
S[52] = dict(raw=r"""Step 1: Understand what is needed
Every student gets the same number of chips and the same number of toffees with nothing left over, so the number of students must divide both 198 and 330. The maximum such number is the HCF.
Step 2: Factorise
\( 198 = 2 \times 3^2 \times 11 \) and \( 330 = 2 \times 3 \times 5 \times 11 \).
Step 3: Take the common factors
\( \text{HCF} = 2 \times 3 \times 11 = 66 \).
Step 4: Check
\( 198 \div 66 = 3 \) chips and \( 330 \div 66 = 5 \) toffees per student ✓.""", trick=r"Maximum equal sharing = HCF: \( \text{HCF}(198, 330) = 66 \).")
S[53] = dict(raw=r"""Step 1: Add the percentages
8% of the number + 10% of the same number \( = 18\% \) of the number.
Step 2: Form the equation
\( 18\% \) of the number \( = 2664 \).
Step 3: Find the number
Number \( = \dfrac{2664 \times 100}{18} = 148 \times 100 = 14800 \).
Step 4: Check
\( 8\% \) of 14800 \( = 1184 \) and \( 10\% \) of 14800 \( = 1480 \), and \( 1184 + 1480 = 2664 \) ✓.""", trick=r"\( 18\% = 2664 \) → \( 1\% = 148 \) → number \( = 14800 \).")
S[54] = dict(raw=r"""Step 1: Write the prices in parts
Cost price and selling price are in the ratio \( 3 : 5 \), so let them be 3 parts and 5 parts.
Step 2: Find the profit in parts
Profit \( = 5 - 3 = 2 \) parts.
Step 3: Find the value of one part
\( 2 \) parts \( = \) ₹720, so 1 part \( = \dfrac{720}{2} = \) ₹360.
Step 4: Find the cost price
Cost price \( = 3 \times 360 = \) ₹1080. Check: selling price \( = 5 \times 360 = \) ₹1800 and \( 1800 - 1080 = 720 \) ✓.""", trick=r"Profit \( = 2 \) parts \( = \) ₹720 → 1 part \( = \) ₹360 → CP \( = 3 \times 360 = \) ₹1080.")
S[55] = dict(raw=r"""Step 1: Form the equation
\( 40\% \) of P \( + 30\% \) of Q \( = 50\% \) of Q, that is \( 0.4P + 0.3Q = 0.5Q \).
Step 2: Collect the Q terms
\( 0.4P = 0.5Q - 0.3Q = 0.2Q \).
Step 3: Find P in terms of Q
\( P = \dfrac{0.2}{0.4}Q = \dfrac{1}{2}Q \).
Step 4: Convert to a percentage
\( \dfrac{P}{Q} \times 100 = \dfrac{1}{2} \times 100 = 50\% \). So P is 50 percent of Q.""", trick=r"\( 40\% \) of P \( = 20\% \) of Q → P is half of Q \( = 50\% \).")
S[56] = dict(raw=r"""Step 1: Find the cost price of one article
CP \( = \dfrac{400}{880} = \) ₹\( \dfrac{5}{11} \).
Step 2: Find the selling price of one article
SP \( = \) ₹\( \dfrac{7}{11} \).
Step 3: Find the profit on one article
Profit \( = \dfrac{7}{11} - \dfrac{5}{11} = \) ₹\( \dfrac{2}{11} \).
Step 4: Find the profit percentage
Profit % \( = \dfrac{2/11}{5/11} \times 100 = \dfrac{2}{5} \times 100 = 40\% \). Check with 880 articles: SP \( = 80 \times 7 = \) ₹560 against a CP of ₹400, a profit of ₹160, and \( \dfrac{160}{400} \times 100 = 40\% \) ✓.""", trick=r"11 articles cost ₹5 and sell for ₹7 → profit \( = \dfrac{2}{5} = 40\% \).")
S[57] = dict(raw=r"""Step 1: Take the total work as the LCM
LCM of 14, 21 and 42 is 42, so let the work be 42 units.
Step 2: Find each person's daily work
A does \( \dfrac{42}{14} = 3 \) units, B does \( \dfrac{42}{21} = 2 \) units and C does \( \dfrac{42}{42} = 1 \) unit per day.
Step 3: Find the combined daily work
Together they do \( 3 + 2 + 1 = 6 \) units per day.
Step 4: Find the required work and the time
\( \dfrac{100}{7}\% = \dfrac{1}{7} \) of the work \( = \dfrac{42}{7} = 6 \) units. Time \( = \dfrac{6}{6} = 1 \) day.""", trick=r"\( \dfrac{100}{7}\% = \dfrac{1}{7} \); together they do \( \dfrac{1}{7} \) of the work per day → 1 day.")
S[58] = dict(raw=r"""Step 1: Find the total work in man-days
Total work \( = 40 \times 84 = 3360 \) man-days.
Step 2: Find 25 percent of the work
\( 25\% \) of 3360 \( = \dfrac{3360}{4} = 840 \) man-days.
Step 3: Divide by the new number of men
Days \( = \dfrac{840}{56} = 15 \).
Step 4: Check
\( 56 \times 15 = 840 \) and \( 840 \times 4 = 3360 \) ✓.""", trick=r"\( \dfrac{40 \times 84}{4 \times 56} = 15 \) days.")
S[59] = dict(raw=r"""Step 1: Find the distance covered
To pass a stationary man the train covers its own length, 200 m.
Step 2: Find the speed in m/s
Speed \( = \dfrac{200}{12} = \dfrac{50}{3} \) m/s.
Step 3: Convert to km/hr
Multiply by \( \dfrac{18}{5} \): speed \( = \dfrac{50}{3} \times \dfrac{18}{5} = 60 \) km/hr.
Step 4: Check
60 km/hr \( = 60 \times \dfrac{5}{18} = \dfrac{50}{3} \) m/s, and \( \dfrac{50}{3} \times 12 = 200 \) m ✓.""", trick=r"\( \dfrac{200}{12} \times \dfrac{18}{5} = 60 \) km/hr.")
S[60] = dict(raw=r"""Step 1: Write the speeds
Let the speed of the train be \( v \) m/s. Then the speed of the man is \( \dfrac{v}{2} \) m/s.
Step 2: Find the relative speed
They move in the same direction, so relative speed \( = v - \dfrac{v}{2} = \dfrac{v}{2} \) m/s.
Step 3: Use the crossing time
The train covers its own length of 420 m at the relative speed in 42 seconds, so \( \dfrac{v}{2} = \dfrac{420}{42} = 10 \).
Step 4: Find the speed of the train
\( v = 2 \times 10 = 20 \) m/s. Check: man's speed \( = 10 \) m/s, relative speed \( = 10 \) m/s, and \( \dfrac{420}{10} = 42 \) seconds ✓.""", trick=r"Same direction: \( v - \dfrac{v}{2} = \dfrac{420}{42} = 10 \) → \( v = 20 \) m/s.")
