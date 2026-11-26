S = {}
S[41] = dict(raw=r"""Step 1: Do the multiplication and division first (BODMAS)
\( 27 \times 2 = 54 \) and \( 44 \div 2 = 22 \). The bracket (16) is just 16.
Step 2: Rewrite the expression
\( 91 - 38 + 54 + 16 + 22 - 31 \).
Step 3: Add and subtract from left to right
\( 91 - 38 = 53 \), \( 53 + 54 = 107 \), \( 107 + 16 = 123 \).
Step 4: Finish
\( 123 + 22 = 145 \), \( 145 - 31 = 114 \).""", trick=r"BODMAS: × and ÷ before + and −.")
S[42] = dict(raw=r"""Step 1: Write the numbers using the HCF
Let the numbers be \( 6a \) and \( 6b \), where a and b have no common factor.
Step 2: Use the sum
\( 6a + 6b = 30 \Rightarrow a + b = 5 \).
Step 3: Use the LCM
LCM \( = 6ab = 36 \Rightarrow ab = 6 \). Two co-prime numbers with sum 5 and product 6 are 2 and 3.
Step 4: Find and check the numbers
\( 6 \times 2 = 12 \) and \( 6 \times 3 = 18 \). Check: \( 12 + 18 = 30 \), HCF = 6, LCM = 36 ✓.""", trick=r"Check: HCF × LCM = product of the numbers, \( 6 \times 36 = 216 = 12 \times 18 \).")
S[43] = dict(raw=r"""Step 1: Remove the decimals
\( \dfrac{0.1225}{0.25} = \dfrac{1225}{2500} \) (multiply top and bottom by 10000).
Step 2: Simplify the fraction
\( \dfrac{1225}{2500} = \dfrac{49}{100} = 0.49 \).
Step 3: Take the square root
\( \sqrt{0.49} = 0.7 \).
Step 4: Check
\( 0.7 \times 0.7 = 0.49 \) and \( 0.49 \times 0.25 = 0.1225 \) ✓.""", trick=r"\( \sqrt{0.1225} = 0.35 \) and \( \sqrt{0.25} = 0.5 \); \( 0.35 \div 0.5 = 0.7 \).")
S[44] = dict(raw=r"""Step 1: Recall the identity
\( (a + b)^{2} + (a - b)^{2} = 2(a^{2} + b^{2}) \).
Step 2: Identify a and b
\( a = 4.2 \), \( b = 3.8 \). The denominator \( 4.2 \times 4.2 + 3.8 \times 3.8 = a^{2} + b^{2} \).
Step 3: Simplify
\( \dfrac{2(a^{2} + b^{2})}{a^{2} + b^{2}} = 2 \).
Step 4: Check by numbers
\( 8^{2} + 0.4^{2} = 64.16 \) and \( 17.64 + 14.44 = 32.08 \); \( 64.16 \div 32.08 = 2 \) ✓.""", trick=r"\( (a + b)^{2} + (a - b)^{2} \) is always twice \( a^{2} + b^{2} \).")
S[45] = dict(raw=r"""Step 1: Find the square roots
\( \sqrt{81} = 9 \), \( \sqrt{9} = 3 \), \( \sqrt{36} = 6 \).
Step 2: Divide first (BODMAS)
\( 9 \div 3 = 3 \).
Step 3: Find x
\( x = 3 + 6 = 9 \).
Step 4: Find 2x
\( 2x = 2 \times 9 = 18 \).""", trick=r"Roots first, then ÷ before +; the question asks for 2x, not x.")
S[46] = dict(raw=r"""Step 1: List the numbers between 40 and 50
41, 42, 43, 44, 45, 46, 47, 48, 49.
Step 2: Remove the composite numbers
Even numbers are out; 45 is divisible by 5 and 49 is \( 7 \times 7 \).
Step 3: Check the rest
41, 43 and 47 are not divisible by 2, 3 or 5 (and \( 7^{2} = 49 \) is larger than each), so they are prime.
Step 4: Add
\( 41 + 43 + 47 = 131 \).""", trick=r"Primes in the 40s: 41, 43, 47.")
S[47] = dict(raw=r"""Step 1: Recall the identity
\( (a + b)^{2} - (a - b)^{2} = 4ab \).
Step 2: Apply it with a = 1 and b = √5
\( (1 + \sqrt{5})^{2} - (1 - \sqrt{5})^{2} = 4 \times 1 \times \sqrt{5} = 4\sqrt{5} \).
Step 3: Subtract the last term
\( 4\sqrt{5} - 14\sqrt{5} = -10\sqrt{5} \).
Step 4: Check by expanding
\( (6 + 2\sqrt{5}) - (6 - 2\sqrt{5}) = 4\sqrt{5} \) ✓, so the value is \( -10\sqrt{5} \).""", trick=r"\( (a + b)^{2} - (a - b)^{2} = 4ab \).")
S[48] = dict(raw=r"""Step 1: Recall the formula
The sum of the first n natural numbers is \( \dfrac{n(n + 1)}{2} \).
Step 2: Put n = 35
\( \dfrac{35 \times 36}{2} \).
Step 3: Calculate
\( 35 \times 18 = 630 \).
Step 4: Check by pairing
Pair 1 with 34, 2 with 33 … gives 17 pairs of 35 plus the 35 itself: \( 17 \times 35 + 35 = 18 \times 35 = 630 \) ✓.""", trick=r"\( 1 + 2 + \ldots + n = \dfrac{n(n + 1)}{2} \).")
S[49] = dict(raw=r"""Step 1: Recall the rule of 8
A number is divisible by 8 when the number formed by its last three digits is divisible by 8. Here that number is 3P2.
Step 2: Test P = 0 and P = 1
\( 302 \div 8 = 37.75 \) ✗; \( 312 \div 8 = 39 \) ✓.
Step 3: Test P = 5 and P = 9
\( 352 \div 8 = 44 \) ✓; \( 392 \div 8 = 49 \) ✓.
Step 4: Answer
Only P = 0 fails, so P cannot be 0.""", trick=r"Divisible by 8 → check the last three digits.")
S[50] = dict(raw=r"""Step 1: Write what is given
Let the sides be l and b: \( lb = 120 \) and \( l^{2} + b^{2} = 17^{2} = 289 \).
Step 2: Use the identity
\( (l + b)^{2} = l^{2} + b^{2} + 2lb = 289 + 240 = 529 \).
Step 3: Find l + b
\( l + b = \sqrt{529} = 23 \) cm.
Step 4: Find the perimeter
Perimeter \( = 2(l + b) = 2 \times 23 = 46 \) cm (the sides are 15 cm and 8 cm).""", trick=r"Area and diagonal → \( (l + b)^{2} = d^{2} + 2 \times \) area.")
S[51] = dict(raw=r"""Step 1: Write the two averages
Average of l and m \( = \dfrac{l + m}{2} \); average of m and n \( = \dfrac{m + n}{2} \).
Step 2: Use the difference
\( \dfrac{l + m}{2} - \dfrac{m + n}{2} = 23 \).
Step 3: Simplify
\( \dfrac{l - n}{2} = 23 \) — the m cancels out.
Step 4: Answer
\( l - n = 2 \times 23 = 46 \).""", trick=r"Difference of two-number averages × 2 = difference of the odd ones out.")
S[52] = dict(raw=r"""Step 1: Write the relation
\( \text{SP} = \text{CP} \times \dfrac{100 + \text{Profit}\%}{100} \).
Step 2: Put in the values
\( 2400 = \text{CP} \times \dfrac{120}{100} \).
Step 3: Solve for CP
\( \text{CP} = 2400 \times \dfrac{100}{120} = 2000 \).
Step 4: Check
Profit \( = 2400 - 2000 = 400 \), and \( \dfrac{400}{2000} \times 100 = 20\% \) ✓. The cost price is ₹2000.""", trick=r"20% profit → SP is \( \dfrac{6}{5} \) of CP, so CP = \( \dfrac{5}{6} \) of SP.")
S[53] = dict(raw=r"""Step 1: Write the formula
B as a percent of A \( = \dfrac{B}{A} \times 100 \).
Step 2: Put in the values
\( \dfrac{9X}{4X} \times 100 \).
Step 3: Cancel X
\( \dfrac{9}{4} \times 100 = 225 \).
Step 4: Answer
B is \( 225\% \) of A.""", trick=r"'B is what percent of A' → A goes in the denominator.")
S[54] = dict(raw=r"""Step 1: Convert to the same unit
Actual height \( = 4 \text{ m } 70 \text{ cm} = 470 \) cm; estimated \( = 3 \text{ m } 52 \text{ cm} = 352 \) cm.
Step 2: Find the error
\( 470 - 352 = 118 \) cm.
Step 3: Find the error percentage (on the actual value)
\( \dfrac{118}{470} \times 100 \).
Step 4: Calculate
\( \dfrac{11800}{470} \approx 25.11\% \).""", trick=r"Error % = error ÷ ACTUAL value × 100.")
S[55] = dict(raw=r"""Step 1: Write the condition
\( 40\% \text{ of CP} = 30\% \text{ of SP} \), so \( 40 \times \text{CP} = 30 \times \text{SP} \).
Step 2: Find the ratio
\( \dfrac{\text{SP}}{\text{CP}} = \dfrac{40}{30} = \dfrac{4}{3} \).
Step 3: Find the profit
Take CP = 3 and SP = 4; profit = 1.
Step 4: Find the profit percentage
\( \dfrac{1}{3} \times 100 = 33.33\% \).""", trick=r"The bigger percent goes with the smaller amount: \( \text{CP} : \text{SP} = 30 : 40 \).")
S[56] = dict(raw=r"""Step 1: Find the food left after 10 days
The food was for 1000 men for 60 days. After 10 days it is enough for 1000 men for \( 60 - 10 = 50 \) days.
Step 2: Find the men left
\( 1000 - 500 = 500 \) men.
Step 3: Use men × days = constant
\( 1000 \times 50 = 500 \times d \).
Step 4: Solve
\( d = \dfrac{50000}{500} = 100 \) days.""", trick=r"Half the men → the remaining food lasts twice as long: \( 2 \times 50 = 100 \).")
S[57] = dict(raw=r"""Step 1: Find each person's one-day work
X: \( \dfrac{1}{10} \), Y: \( \dfrac{1}{15} \), Z: \( \dfrac{1}{30} \).
Step 2: Find the ratio of their work
Take the work as 30 units (LCM): X does 3, Y 2 and Z 1 unit a day, so the ratio is \( 3 : 2 : 1 \), and wages are shared in the same ratio.
Step 3: Find one part of the wages
X's 3 parts = ₹8000, so one part \( = \dfrac{8000}{3} \).
Step 4: Find Y and Z's share
Y + Z = 3 parts = ₹8000 (the same as X's share).""", trick=r"Wages are shared in the ratio of work done each day.")
S[58] = dict(raw=r"""Step 1: Recall the relation
For the same distance, time is inversely proportional to speed.
Step 2: Write the ratio of speeds
\( 14 : 38 = 7 : 19 \).
Step 3: Invert it for time
Ratio of the times of A and B \( = 19 : 7 \).
Step 4: Check
For 266 km (LCM of 14 and 38): A takes \( 266 \div 14 = 19 \) h and B takes \( 266 \div 38 = 7 \) h ✓.""", trick=r"Same distance → time ratio = speed ratio turned upside down.")
S[59] = dict(raw=r"""Step 1: Note the directions
G and H start at the same time from opposite ends and move towards each other, so their speeds add.
Step 2: Find the combined speed
Together they cover 500 km in 5 hours: \( \dfrac{500}{5} = 100 \) km/hr.
Step 3: Find H's speed
\( 100 - 60 = 40 \) km/hr.
Step 4: Check
In 5 hours G covers \( 60 \times 5 = 300 \) km and H covers \( 40 \times 5 = 200 \) km; \( 300 + 200 = 500 \) ✓.""", trick=r"Towards each other → relative speed = sum of speeds.")
S[60] = dict(raw=r"""Step 1: Find Y in terms of X
A 40% discount means he pays 60% of the marked price: \( Y = 0.6X \).
Step 2: Find Z in terms of Y
Z is 30% more than Y: \( Z = 1.3Y \).
Step 3: Find Z in terms of X
\( Z = 1.3 \times 0.6X = 0.78X \).
Step 4: Write the ratio
\( Z : X = 0.78 : 1 = 78 : 100 = 39 : 50 \).""", trick=r"Chain the multipliers: \( 0.6 \times 1.3 = 0.78 \).")
