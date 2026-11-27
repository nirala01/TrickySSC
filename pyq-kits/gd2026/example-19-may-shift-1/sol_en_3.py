S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first
\( 31 + 27 = 58 \).
Step 2: Multiply
\( 58 \times 2 = 116 \).
Step 3: Rewrite the expression
\( 69 + 74 - 116 + 88 - 44 \).
Step 4: Add and subtract from left to right
\( 143 - 116 = 27 \), \( 27 + 88 = 115 \), \( 115 - 44 = 71 \).""", trick=r"Positives \( 69 + 74 + 88 = 231 \); negatives \( 116 + 44 = 160 \); \( 231 - 160 = 71 \).")
S[42] = dict(raw=r"""Step 1: Solve "of" and the bracket first
\( 18 \text{ of } 1 = 18 \times 1 = 18 \).
Step 2: Multiply and divide
\( 33 \times 1 = 33 \) and \( 47 \div 1 = 47 \).
Step 3: Rewrite the expression
\( 83 - 29 + 33 + 47 - 36 + 18 \).
Step 4: Add and subtract from left to right
\( 54 + 33 = 87 \), \( 87 + 47 = 134 \), \( 134 - 36 = 98 \), \( 98 + 18 = 116 \).""", trick=r"Positives \( 83 + 33 + 47 + 18 = 181 \); negatives \( 29 + 36 = 65 \); \( 181 - 65 = 116 \).")
S[43] = dict(raw=r"""Step 1: Find the total work in man-days
\( 12 \times 15 = 180 \) man-days.
Step 2: Work done in the first 6 days
\( 12 \times 6 = 72 \) man-days, so the work left \( = 180 - 72 = 108 \) man-days.
Step 3: Men left after 4 leave
\( 12 - 4 = 8 \) men.
Step 4: Days needed for the rest
\( 108 \div 8 = 13.5 \) days.""", trick=r"Remaining \( = 12 \times 9 = 108 \) man-days; \( 108 \div 8 = 13.5 \) days.")
S[44] = dict(raw=r"""Step 1: Write the areas
Area of a square \( = a^{2} \), so \( a_{1}^{2} : a_{2}^{2} = 9 : 16 \).
Step 2: Take square roots
\( a_{1} : a_{2} = \sqrt{9} : \sqrt{16} \).
Step 3: Simplify
\( \sqrt{9} = 3 \) and \( \sqrt{16} = 4 \), so the sides are in the ratio \( 3 : 4 \).
Step 4: Check
\( 3^{2} : 4^{2} = 9 : 16 \) ✓.""", trick=r"Ratio of sides \( = \sqrt{\text{ratio of areas}} \) → \( 3 : 4 \).")
S[45] = dict(raw=r"""Step 1: Write the quantities
Let alcohol \( = 5x \) litres and water \( = 2x \) litres.
Step 2: Form the equation after adding water
Alcohol stays \( 5x \); water becomes \( 2x + 15 \). So \( 5x : (2x + 15) = 5 : 4 \Rightarrow 2x + 15 = 4x \).
Step 3: Solve
\( 2x = 15 \Rightarrow x = 7.5 \).
Step 4: Original mixture
\( 5x + 2x = 7x = 7 \times 7.5 = 52.5 \) litres.""", trick=r"Alcohol fixed at 5 parts; water 2 → 4 parts, so 2 parts \( = 15 \) L, 1 part \( = 7.5 \) L, total \( 7 \times 7.5 = 52.5 \) L.")
S[46] = dict(raw=r"""Step 1: Add the whole-number parts
\( 9 + 99 + 999 + 9999 = 11106 \).
Step 2: Write each fraction as a difference
\( \dfrac{1}{2} = 1 - \dfrac{1}{2} \), \( \dfrac{1}{6} = \dfrac{1}{2} - \dfrac{1}{3} \), \( \dfrac{1}{12} = \dfrac{1}{3} - \dfrac{1}{4} \), \( \dfrac{1}{20} = \dfrac{1}{4} - \dfrac{1}{5} \).
Step 3: Add the fractions
The middle terms cancel, leaving \( 1 - \dfrac{1}{5} = \dfrac{4}{5} \).
Step 4: Combine
\( 11106 + \dfrac{4}{5} = 11106\dfrac{4}{5} \).""", trick=r"\( \dfrac{1}{n(n+1)} = \dfrac{1}{n} - \dfrac{1}{n+1} \) → fractions add to \( 1 - \dfrac{1}{5} = \dfrac{4}{5} \).")
S[47] = dict(raw=r"""Step 1: Choose a common denominator
LCM of 18, 9, 6, 15 and 24 is 360.
Step 2: Convert the given fraction
\( \dfrac{13}{18} = \dfrac{260}{360} \).
Step 3: Convert the options
\( \dfrac{7}{9} = \dfrac{280}{360} \), \( \dfrac{5}{6} = \dfrac{300}{360} \), \( \dfrac{11}{15} = \dfrac{264}{360} \), \( \dfrac{17}{24} = \dfrac{255}{360} \).
Step 4: Compare
Only \( \dfrac{255}{360} \) is less than \( \dfrac{260}{360} \), so \( \dfrac{17}{24} \) is smaller than \( \dfrac{13}{18} \).""", trick=r"Decimals: \( \dfrac{13}{18} \approx 0.722 \), \( \dfrac{17}{24} \approx 0.708 \) — the only smaller one.")
S[48] = dict(raw=r"""Step 1: Recognise the identity
\( a^{2} + b^{2} + 2ab = (a + b)^{2} \).
Step 2: Match the values
Here \( a = 195 \) and \( b = 105 \).
Step 3: Add
\( a + b = 195 + 105 = 300 \).
Step 4: Square
\( 300^{2} = 90000 \).""", trick=r"\( (195 + 105)^{2} = 300^{2} = 90000 \).")
S[49] = dict(raw=r"""Step 1: Recall the formula
Perimeter of a square \( = 4 \times \text{side} \).
Step 2: Form the equation
\( 4 \times \text{side} = 24 \).
Step 3: Solve
\( \text{side} = 24 \div 4 = 6 \) cm.
Step 4: Check
\( 4 \times 6 = 24 \) ✓.""", trick=r"Side \( = \dfrac{\text{perimeter}}{4} = 6 \) cm.")
S[50] = dict(raw=r"""Step 1: Find the side
\( \text{side} = 40 \div 4 = 10 \) cm.
Step 2: Recall the diagonal formula
Diagonal of a square \( = \text{side} \times \sqrt{2} \).
Step 3: Calculate
\( 10 \times \sqrt{2} = 10\sqrt{2} \) cm.
Step 4: Check
By Pythagoras, \( d^{2} = 10^{2} + 10^{2} = 200 \), so \( d = \sqrt{200} = 10\sqrt{2} \) ✓.""", trick=r"Side \( = 10 \), diagonal \( = 10\sqrt{2} \).")
S[51] = dict(raw=r"""Step 1: Recall the rule of 8
A number is divisible by 8 if the number formed by its last three digits is divisible by 8.
Step 2: Write the last three digits
For 47P6 the last three digits form 7P6.
Step 3: Test the options
\( 716 \div 8 = 89.5 \), \( 726 \div 8 = 90.75 \), \( 736 \div 8 = 92 \), \( 746 \div 8 = 93.25 \).
Step 4: Answer
Only 736 is divisible by 8, so P = 3 (4736 ÷ 8 = 592).""", trick=r"Check the last three digits: 7P6 → 736 ✓ → P = 3.")
S[52] = dict(raw=r"""Step 1: Write the total
Sum of the 35 results \( = 35N \).
Step 2: Subtract 5 from each result
Total decrease \( = 35 \times 5 = 175 \), so the new sum \( = 35N - 175 \).
Step 3: Find the new average
\( \dfrac{35N - 175}{35} = N - 5 \).
Step 4: Answer
The new average is N − 5.""", trick=r"Subtracting the same number from every value lowers the average by that number: \( N - 5 \).")
S[53] = dict(raw=r"""Step 1: Find the eight numbers
The average of 8 consecutive odd numbers lies midway between the 4th and 5th numbers, which are 39 and 41. So the numbers are 33, 35, 37, 39, 41, 43, 45, 47.
Step 2: Add the two new numbers
The odd number just before 33 is 31, and the one just after 47 is 49.
Step 3: Find the new total
Old total \( = 8 \times 40 = 320 \); new total \( = 320 + 31 + 49 = 400 \).
Step 4: Find the new average
\( 400 \div 10 = 40 \).""", trick=r"31 and 49 are equally spaced around 40, so the average stays 40.")
S[54] = dict(raw=r"""Step 1: Write the numbers using the ratio
Let the numbers be \( 2x \) and \( 5x \).
Step 2: Use the HCF
2 and 5 have no common factor, so the HCF of \( 2x \) and \( 5x \) is \( x \). Hence \( x = 11 \).
Step 3: Find the numbers
\( 2 \times 11 = 22 \) and \( 5 \times 11 = 55 \).
Step 4: Find the sum
\( 22 + 55 = 77 \).""", trick=r"Sum \( = (2 + 5) \times 11 = 77 \).")
S[55] = dict(raw=r"""Step 1: Find when the bells ring together
They ring together after every LCM of 3, 6, 9, 12, 15 and 18 seconds.
Step 2: Calculate the LCM
\( 18 = 2 \times 3^{2} \), \( 12 = 2^{2} \times 3 \), \( 15 = 3 \times 5 \); LCM \( = 2^{2} \times 3^{2} \times 5 = 180 \) seconds \( = 3 \) minutes.
Step 3: Count the intervals in 24 minutes
\( 24 \div 3 = 8 \).
Step 4: Include the first ringing
\( 8 + 1 = 9 \) times.""", trick=r"LCM \( = 180 \) s \( = 3 \) min; \( \dfrac{24}{3} + 1 = 9 \).")
S[56] = dict(raw=r"""Step 1: Write the condition
\( 5 \times \text{SP} = 4 \times \text{CP} \).
Step 2: Find the ratio
\( \text{SP} : \text{CP} = 4 : 5 \); take CP \( = 5 \) units and SP \( = 4 \) units.
Step 3: Find the loss
Loss \( = 5 - 4 = 1 \) unit.
Step 4: Loss percentage
\( \dfrac{1}{5} \times 100 = 20 \) percent.""", trick=r"SP \( = \dfrac{4}{5} \) of CP → loss \( = \dfrac{1}{5} \) = 20 percent.")
S[57] = dict(raw=r"""Step 1: Write the equation
50 percent of P + 40 percent of Q = 80 percent of Q, i.e. \( 0.5P + 0.4Q = 0.8Q \).
Step 2: Simplify
\( 0.5P = 0.8Q - 0.4Q = 0.4Q \).
Step 3: Express P in terms of Q
\( P = \dfrac{0.4}{0.5} Q = 0.8Q \).
Step 4: Convert to a percentage
\( 0.8 \times 100 = 80 \), so P is 80 percent of Q.""", trick=r"\( 0.5P = 0.4Q \Rightarrow \dfrac{P}{Q} = \dfrac{4}{5} \) = 80 percent.")
S[58] = dict(raw=r"""Step 1: Find the CP and SP of one article
CP of 1 article \( = \dfrac{182}{15} \) rupees; SP of 1 article \( = \dfrac{182}{20} \) rupees.
Step 2: Compare
SP is less than CP, so there is a loss.
Step 3: Find the loss on one article
Loss \( = 182 \left( \dfrac{1}{15} - \dfrac{1}{20} \right) = 182 \times \dfrac{1}{60} = \dfrac{182}{60} \) rupees.
Step 4: Find the ratio
Ratio of loss to CP \( = \dfrac{182}{60} \div \dfrac{182}{15} = \dfrac{15}{60} = \dfrac{1}{4} \), i.e. \( 1 : 4 \).""", trick=r"Same money buys 15 but sells for 20: loss per article \( = \dfrac{20 - 15}{20} \) of CP → \( 1 : 4 \).")
S[59] = dict(raw=r"""Step 1: One day's work of each person
1 man \( = \dfrac{1}{3 \times 12} = \dfrac{1}{36} \), 1 woman \( = \dfrac{1}{4 \times 8} = \dfrac{1}{32} \), 1 boy \( = \dfrac{1}{6 \times 18} = \dfrac{1}{108} \).
Step 2: Work of each group in one day
12 boys \( = \dfrac{12}{108} = \dfrac{1}{9} \), 6 men \( = \dfrac{6}{36} = \dfrac{1}{6} \), 8 women \( = \dfrac{8}{32} = \dfrac{1}{4} \).
Step 3: Add them
\( \dfrac{1}{9} + \dfrac{1}{6} + \dfrac{1}{4} = \dfrac{4 + 6 + 9}{36} = \dfrac{19}{36} \).
Step 4: Find the time
Time \( = \dfrac{36}{19} \) days.""", trick=r"Groups do \( \dfrac{1}{9} + \dfrac{1}{6} + \dfrac{1}{4} = \dfrac{19}{36} \) a day → \( \dfrac{36}{19} \) days.")
S[60] = dict(raw=r"""Step 1: Find the total distance
\( 36 + 42 = 78 \) km.
Step 2: Note the total time
Both distances together take 6 hours.
Step 3: Use the same speed
Since the speed is the same throughout, speed \( = \dfrac{\text{total distance}}{\text{total time}} \).
Step 4: Calculate
\( 78 \div 6 = 13 \) km/hr.""", trick=r"Speed \( = \dfrac{78}{6} = 13 \) km/hr.")
