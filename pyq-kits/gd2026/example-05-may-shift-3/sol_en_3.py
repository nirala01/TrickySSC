S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first
\( 27 \div 3 = 9 \)
Step 2: Then the multiplication
\( 19 \times 1 = 19 \), so the expression becomes \( 94 + 36 - 9 + 33 + 19 - 29 \)
Step 3: Add the positive terms
\( 94 + 36 + 33 + 19 = 182 \)
Step 4: Subtract the rest
\( 182 - 9 - 29 = 144 \)""", trick=r"BODMAS: bracket, then × and ÷, then add all + terms and subtract all − terms.")
S[42] = dict(raw=r"""Step 1: The bells ring together again after the LCM of their intervals
We need LCM of 18, 24 and 30 seconds.
Step 2: Prime factors
\( 18 = 2 \times 3^{2} \), \( 24 = 2^{3} \times 3 \), \( 30 = 2 \times 3 \times 5 \)
Step 3: Take the highest powers
\( \text{LCM} = 2^{3} \times 3^{2} \times 5 = 360 \) seconds
Step 4: Convert to minutes
\( \dfrac{360}{60} = 6 \) minutes, i.e. at 10:06:00 AM.""", trick=r"“Ring together again” → LCM of the intervals.")
S[43] = dict(raw=r"""Step 1: Write each denominator as a product of consecutive odd numbers
\( 3 = 1 \times 3 \), \( 15 = 3 \times 5 \), \( 35 = 5 \times 7 \), \( 63 = 7 \times 9 \)
Step 2: Split each fraction
\( \dfrac{1}{n(n+2)} = \dfrac{1}{2}\left(\dfrac{1}{n} - \dfrac{1}{n+2}\right) \)
Step 3: Add — the middle terms cancel
\( \dfrac{1}{2}\left(1 - \dfrac{1}{3} + \dfrac{1}{3} - \dfrac{1}{5} + \dfrac{1}{5} - \dfrac{1}{7} + \dfrac{1}{7} - \dfrac{1}{9}\right) = \dfrac{1}{2}\left(1 - \dfrac{1}{9}\right) \)
Step 4: Simplify
\( \dfrac{1}{2} \times \dfrac{8}{9} = \dfrac{4}{9} \)""", trick=r"1/(1·3) + … + 1/(7·9) = ½(1 − 1/9) = 4/9.")
S[44] = dict(raw=r"""Step 1: Spot the identity
\( (a - b)^{2} + 4ab = (a + b)^{2} \)
Step 2: Identify a and b
\( a = 2.85 \), \( b = 1.15 \)
Step 3: Find a + b
\( 2.85 + 1.15 = 4 \)
Step 4: Square it
\( 4^{2} = 16 \)""", trick=r"(a − b)² + 4ab = (a + b)².")
S[45] = dict(raw=r"""Step 1: Find the square roots
\( \sqrt{196} = 14 \), \( \sqrt{49} = 7 \), \( \sqrt{81} = 9 \)
Step 2: Division first (BODMAS)
\( 14 \div 7 = 2 \)
Step 3: Then the addition
\( x = 2 + 9 = 11 \)
Step 4: Find 2x
\( 2x = 2 \times 11 = 22 \)""", trick=r"Roots first, then ÷ before +.")
S[46] = dict(raw=r"""Step 1: Estimate the middle number
\( \sqrt[3]{315} \) is a little less than 7 (since \( 7^{3} = 343 \)), so try odd numbers around 7.
Step 2: Test 5, 7, 9
\( 5 \times 7 \times 9 = 35 \times 9 = 315 \) ✓
Step 3: Add the three numbers
\( 5 + 7 + 9 = 21 \)
Step 4: Check
The middle number is 7 and the sum of three consecutive odd numbers \( = 3 \times 7 = 21 \) ✓""", trick=r"Sum of three consecutive odd numbers = 3 × the middle number.")
S[47] = dict(raw=r"""Step 1: Spot the identity
\( a^{2} + b^{2} + 2ab = (a + b)^{2} \)
Step 2: Identify a and b
\( a = 150 \), \( b = 250 \)
Step 3: Add them
\( 150 + 250 = 400 \)
Step 4: Square
\( 400^{2} = 160000 \)""", trick=r"a² + b² + 2ab = (a + b)².")
S[48] = dict(raw=r"""Step 1: Compare the numbers in the numerator and denominator
\( 4.1 = 10 \times 0.41 \), \( 41.1 = 10 \times 4.11 \), \( 411.1 = 10 \times 41.11 \)
Step 2: Square them
Each numerator square is \( 10^{2} = 100 \) times the matching denominator square, e.g. \( (4.1)^{2} = 100 \times (0.41)^{2} \).
Step 3: Simplify the fraction
\( \dfrac{100[(0.41)^{2} + (4.11)^{2} + (41.11)^{2}]}{(0.41)^{2} + (4.11)^{2} + (41.11)^{2}} = 100 \)
Step 4: Take the square root
\( \sqrt{100} = 10 \)""", trick=r"Each top number is 10 times the bottom one → ratio 100 → root 10.")
S[49] = dict(raw=r"""Step 1: Use Pythagoras for the breadth
\( \text{diagonal}^{2} = l^{2} + b^{2} \Rightarrow 17^{2} = 15^{2} + b^{2} \)
Step 2: Solve for b
\( b^{2} = 289 - 225 = 64 \Rightarrow b = 8 \) cm
Step 3: Perimeter formula
\( P = 2(l + b) \)
Step 4: Substitute
\( P = 2(15 + 8) = 2 \times 23 = 46 \) cm""", trick=r"8-15-17 is a Pythagorean triple.")
S[50] = dict(raw=r"""Step 1: Spot the identity
\( 2(a^{2} + b^{2}) - (a - b)^{2} = a^{2} + b^{2} + 2ab = (a + b)^{2} \)
Step 2: Identify a and b
\( a = 530 \), \( b = 270 \)
Step 3: Find a + b
\( 530 + 270 = 800 \)
Step 4: Square
\( 800^{2} = 640000 \)""", trick=r"2(a² + b²) − (a − b)² = (a + b)².")
S[51] = dict(raw=r"""Step 1: Total expenditure for 5 days
\( 5 \times 120 = 600 \), i.e. ₹600
Step 2: Total for the first 4 days
\( 50 + 105 + 95 + 160 = 410 \), i.e. ₹410
Step 3: Expenditure on the 5th day
\( 600 - 410 = 190 \), i.e. ₹190
Step 4: Check
\( \dfrac{410 + 190}{5} = \dfrac{600}{5} = 120 \) ✓""", trick=r"Missing value = average × count − sum of the known values.")
S[52] = dict(raw=r"""Step 1: The difference between SP and CP is the profit
Profit = ₹252
Step 2: Profit is 9% of the cost price
\( 9\% \text{ of CP} = 252 \)
Step 3: Find the cost price
\( \text{CP} = \dfrac{252 \times 100}{9} = 28 \times 100 = 2800 \), i.e. ₹2800
Step 4: Check
\( 9\% \text{ of } 2800 = 252 \) ✓""", trick=r"CP = profit × 100 ÷ profit %.")
S[53] = dict(raw=r"""Step 1: First take 60% of 6800
\( \dfrac{60}{100} \times 6800 = 4080 \)
Step 2: Then take 40% of the result
\( \dfrac{40}{100} \times 4080 = 1632 \)
Step 3: Shortcut — multiply the percentages
\( 0.4 \times 0.6 = 0.24 \)
Step 4: Check
\( 0.24 \times 6800 = 1632 \) ✓""", trick=r"Successive percentages multiply: 40% of 60% = 24%.")
S[54] = dict(raw=r"""Step 1: Take the values from the ratio
Let \( \text{CP} = 3k \) and \( \text{SP} = 5k \).
Step 2: Find the profit
\( \text{Profit} = 5k - 3k = 2k \)
Step 3: Ratio of profit to CP
\( 2k : 3k \)
Step 4: Simplify
\( 2 : 3 \)""", trick=r"Profit = SP − CP in ratio units; then compare with CP.")
S[55] = dict(raw=r"""Step 1: Let the total number of employees be N
Matriculates \( = 20\% \text{ of } N = 0.2N \); remaining \( = 0.8N \).
Step 2: Graduates are 40% of the remaining
\( 0.4 \times 0.8N = 0.32N \); post-graduates \( = 0.8N - 0.32N = 0.48N \)
Step 3: Use the given number
\( 0.48N = 144 \Rightarrow N = \dfrac{144}{0.48} = 300 \)
Step 4: Matriculates
\( 0.2 \times 300 = 60 \)""", trick=r"Post-graduates = 80% × 60% = 48% of all employees.")
S[56] = dict(raw=r"""Step 1: Work done per day
\( \dfrac{30\%}{6} = 5\% \) of the work each day
Step 2: Work in 10 days
\( 10 \times 5\% = 50\% \)
Step 3: Check with the whole work
A finishes 100% in \( \dfrac{100}{5} = 20 \) days, so in 10 days he does \( \dfrac{10}{20} = \dfrac{1}{2} \).
Step 4: Answer
\( \dfrac{1}{2} = 50\% \) of the work.""", trick=r"Work is proportional to time: 30% in 6 days → 50% in 10 days.")
S[57] = dict(raw=r"""Step 1: Write the efficiencies
Let P, Q, R be the work done per day. \( Q + R = 5P \) and \( P + R = 3Q \).
Step 2: Use the total
\( P + Q + R = 6P \) (from the first) and \( P + Q + R = 4Q \) (from the second), so \( 6P = 4Q \Rightarrow Q = 1.5P \).
Step 3: Total work
Q and R together finish in 45 days, so work \( = (Q + R) \times 45 = 5P \times 45 = 225P \).
Step 4: Time for P alone
\( \dfrac{225P}{P} = 225 \) days""", trick=r"Q + R = 5P means Q and R together are 5 times as fast as P → P takes 5 × 45 days.")
S[58] = dict(raw=r"""Step 1: Change the speed to m/s
\( 18 \times \dfrac{5}{18} = 5 \) m/s
Step 2: Change the time to seconds
\( 8 \times 60 = 480 \) seconds
Step 3: Distance = speed × time
\( 5 \times 480 = 2400 \) m
Step 4: Check in km
\( 18 \times \dfrac{8}{60} = 2.4 \) km \( = 2400 \) m ✓""", trick=r"km/h × 5/18 = m/s.")
S[59] = dict(raw=r"""Step 1: Distance covered by the bus
\( 80 \times 10 = 800 \) km
Step 2: Distance and time of the train
Distance \( = 800 + 100 = 900 \) km; time \( = 10 + 5 = 15 \) hours
Step 3: Speed of the train
\( \dfrac{900}{15} = 60 \) km/h
Step 4: Check
\( 60 \times 15 = 900 \) km ✓""", trick=r"Find the train's own distance and time first, then divide.")
S[60] = dict(raw=r"""Step 1: Formula
\( \text{Discount}\% = \dfrac{\text{MP} - \text{SP}}{\text{MP}} \times 100 \)
Step 2: SP ₹2000, MP ₹2500
\( \dfrac{500}{2500} \times 100 = 20\% \) ✓
Step 3: Check the other pairs
\( \dfrac{700}{2500} \times 100 = 28\% \), \( \dfrac{600}{2800} \times 100 \approx 21.4\% \), \( \dfrac{300}{1800} \times 100 \approx 16.7\% \)
Step 4: Answer
Only SP ₹2000 and MP ₹2500 gives a 20% discount.""", trick=r"20% discount → SP = 80% of MP: 80% of 2500 = 2000.")
