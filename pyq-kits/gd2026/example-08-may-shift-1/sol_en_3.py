S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first
\( 37 + 19 = 56 \).
Step 2: Multiply
\( 56 \times 2 = 112 \).
Step 3: Add and subtract from left to right
\( 95 + 62 = 157 \); \( 157 - 69 = 88 \); \( 88 + 112 = 200 \).
Step 4: Finish
\( 200 - 103 = 97 \).""", trick=r"BODMAS: bracket → × → then + and − from the left.")
S[42] = dict(raw=r"""Step 1: Solve "of" (it is a multiplication done first)
\( 28 \text{ of } 2 = 28 \times 2 = 56 \).
Step 2: Do the other multiplication and the division
\( 14 \times 2 = 28 \) and \( 39 \div 3 = 13 \).
Step 3: Rewrite the expression
\( 96 - 27 + 28 + 13 - 56 + 17 \).
Step 4: Add and subtract from the left
\( 96 - 27 = 69 \); \( 69 + 28 = 97 \); \( 97 + 13 = 110 \); \( 110 - 56 = 54 \); \( 54 + 17 = 71 \).""", trick=r"'of' means ×, and it comes before ÷ and × in BODMAS.")
S[43] = dict(raw=r"""Step 1: Write the numbers using the HCF
Let the numbers be \( 18a \) and \( 18b \), where a and b are co-prime.
Step 2: Use the sum
\( 18a + 18b = 198 \Rightarrow a + b = 11 \).
Step 3: Use the LCM
LCM = \( 18ab = 540 \Rightarrow ab = 30 \). Two co-prime numbers with sum 11 and product 30 are 5 and 6.
Step 4: Find the numbers and check
\( 18 \times 5 = 90 \) and \( 18 \times 6 = 108 \). Check: \( 90 \times 108 = 9720 = 18 \times 540 \) ✓ and \( 90 + 108 = 198 \) ✓.""", trick=r"Product of two numbers = HCF × LCM; both must be multiples of the HCF.")
S[44] = dict(raw=r"""Step 1: Use the identity
\( a^{4} - b^{4} = (a^{2} + b^{2})(a^{2} - b^{2}) \).
Step 2: Cancel the common factor
\( \dfrac{(a^{2} + b^{2})(a^{2} - b^{2})}{a^{2} - b^{2}} = a^{2} + b^{2} \), with a = 0.7 and b = 0.3.
Step 3: Square each number
\( (0.7)^{2} = 0.49 \) and \( (0.3)^{2} = 0.09 \).
Step 4: Add
\( 0.49 + 0.09 = 0.58 \).""", trick=r"(a⁴ − b⁴) ÷ (a² − b²) = a² + b².")
S[45] = dict(raw=r"""Step 1: Find each square root
\( \sqrt{100} = 10 \), \( \sqrt{25} = 5 \), \( \sqrt{64} = 8 \).
Step 2: Divide first (BODMAS)
\( 10 \div 5 = 2 \).
Step 3: Add
\( x = 2 + 8 = 10 \).
Step 4: Find 2x
\( 2x = 2 \times 10 = 20 \).""", trick=r"Roots first, then ÷ before +; don't forget to double at the end.")
S[46] = dict(raw=r"""Step 1: Find the known root
\( \sqrt{20.25} = 4.5 \), because \( 4.5 \times 4.5 = 20.25 \).
Step 2: Isolate the other root
\( \sqrt{16 + x} = 9.5 - 4.5 = 5 \).
Step 3: Square both sides
\( 16 + x = 25 \).
Step 4: Solve
\( x = 25 - 16 = 9 \). Check: \( 4.5 + \sqrt{25} = 4.5 + 5 = 9.5 \) ✓.""", trick=r"√20.25 = 4.5 (like 45² = 2025); then the other root must be 5.")
S[47] = dict(raw=r"""Step 1: Use Pythagoras in the rectangle
\( \text{diagonal}^{2} = l^{2} + b^{2} \).
Step 2: Put in the values
\( 13^{2} = 5^{2} + b^{2} \Rightarrow 169 = 25 + b^{2} \Rightarrow b^{2} = 144 \).
Step 3: Find the breadth
\( b = \sqrt{144} = 12 \) cm.
Step 4: Write the ratio
Length to breadth = \( 5 : 12 \) (5, 12, 13 is a Pythagorean triplet).""", trick=r"Triplet 5–12–13: the other side is 12.")
S[48] = dict(raw=r"""Step 1: Use the perimeter
\( 2(l + b) = 160 \Rightarrow l + b = 80 \).
Step 2: Use the difference
\( l - b = 8 \).
Step 3: Solve
\( l = \dfrac{80 + 8}{2} = 44 \) m and \( b = \dfrac{80 - 8}{2} = 36 \) m.
Step 4: Find the area
Area = \( 44 \times 36 = 1584 \) square metres.""", trick=r"Sum and difference given → length = (sum + diff) ÷ 2.")
S[49] = dict(raw=r"""Step 1: Find the total of the 8 numbers
Sum = \( 8 \times P = 8P \).
Step 2: Find the total after removing one number
7 numbers with average P + 2: sum = \( 7(P + 2) = 7P + 14 \).
Step 3: Find the removed number
Removed number = \( 8P - (7P + 14) = P - 14 \).
Step 4: Check with a value
Take P = 30: total 240; removed = 16; new sum 224 and \( 224 \div 7 = 32 = P + 2 \) ✓.""", trick=r"Removed number = old total − new total.")
S[50] = dict(raw=r"""Step 1: Use the sum-of-squares formula
\( 1^{2} + 2^{2} + \ldots + n^{2} = \dfrac{n(n + 1)(2n + 1)}{6} \).
Step 2: Put n = 60
\( \dfrac{60 \times 61 \times 121}{6} \).
Step 3: Simplify
\( \dfrac{60}{6} = 10 \), so the sum = \( 10 \times 61 \times 121 \).
Step 4: Multiply
\( 61 \times 121 = 7381 \), and \( 10 \times 7381 = 73810 \).""", trick=r"Σn² = n(n+1)(2n+1)/6; the answer must end in 0 here because of the factor 10.")
S[51] = dict(raw=r"""Step 1: Find the middle of the last 11 numbers
For consecutive numbers the average is the middle term. The last 11 numbers are the 13th to the 23rd; their middle is the 18th number, so the 18th number = 34.
Step 2: Find the middle of all 23 numbers
The middle of 23 numbers is the 12th number.
Step 3: Move back from the 18th to the 12th
\( 34 - (18 - 12) = 34 - 6 = 28 \).
Step 4: Answer
The average of all 23 numbers = the 12th number = 28. (The numbers are 17 to 39.)""", trick=r"Consecutive numbers: average = middle term.")
S[52] = dict(raw=r"""Step 1: Know the rule
They meet again at the start after a time that is a multiple of every lap time — the LCM.
Step 2: Factorise the times
\( 180 = 2^{2} \times 3^{2} \times 5 \), \( 270 = 2 \times 3^{3} \times 5 \), \( 360 = 2^{3} \times 3^{2} \times 5 \).
Step 3: Find the LCM
LCM = \( 2^{3} \times 3^{3} \times 5 = 1080 \) seconds.
Step 4: Convert to minutes
\( 1080 \div 60 = 18 \) minutes.""", trick=r"Meeting at the start = LCM of lap times.")
S[53] = dict(raw=r"""Step 1: Write what is given
Element A = 20% of the mixture.
Step 2: Form the equation
\( 20\% \text{ of } M = 120 \Rightarrow \dfrac{20}{100} \times M = 120 \).
Step 3: Solve
\( M = \dfrac{120 \times 100}{20} = 600 \) kg.
Step 4: Check
\( 20\% \) of 600 kg = \( 600 \times 0.2 = 120 \) kg ✓.""", trick=r"20% = 1/5, so the mixture is 5 × 120 = 600 kg.")
S[54] = dict(raw=r"""Step 1: Write the formula
\( SP = CP \times \dfrac{100 + \text{profit}\%}{100} \).
Step 2: Put in the values
\( SP = 6800 \times \dfrac{130}{100} \).
Step 3: Calculate
\( 68 \times 130 = 8840 \).
Step 4: Answer
The selling price is ₹8840 (profit = \( 30\% \) of 6800 = ₹2040).""", trick=r"30% of 6800 = 2040; 6800 + 2040 = 8840.")
S[55] = dict(raw=r"""Step 1: Form the equation
\( 20\% \text{ of } CP = 25\% \text{ of } SP \Rightarrow \dfrac{CP}{SP} = \dfrac{25}{20} = \dfrac{5}{4} \).
Step 2: Take values
Let CP = 5 units and SP = 4 units. SP is less than CP, so there is a loss.
Step 3: Find the loss
Loss = \( 5 - 4 = 1 \) unit.
Step 4: Find the loss percentage
Loss % = \( \dfrac{1}{5} \times 100 = 20\% \).""", trick=r"\( \text{CP} : \text{SP} = 25 : 20 = 5 : 4 \) → loss 1 on 5 = 20%.")
S[56] = dict(raw=r"""Step 1: Take A = 100
B is 30% more than A: B = \( 100 \times 1.3 = 130 \).
Step 2: Find C
C is 20% less than B: C = \( 130 \times 0.8 = 104 \).
Step 3: Find A as a percentage of C
\( \dfrac{100}{104} \times 100 \).
Step 4: Calculate
\( \dfrac{10000}{104} \approx 96.15\% \).""", trick=r"Start with 100: 100 → 130 → 104; A/C = 100/104.")
S[57] = dict(raw=r"""Step 1: Find S's time for the whole work
S does \( \dfrac{2}{3} \) of the work in 16 days, so the whole work takes \( 16 \times \dfrac{3}{2} = 24 \) days.
Step 2: Use efficiency
R is 4 times as efficient as S, so R needs \( \dfrac{1}{4} \) of S's time.
Step 3: Find R's time
\( \dfrac{24}{4} = 6 \) days.
Step 4: Check with units of work
Let the work = 24 units: S does 1 unit/day, R does 4 units/day, and \( 24 \div 4 = 6 \) days ✓.""", trick=r"Time is inversely proportional to efficiency: 4 times as efficient → one-fourth the time.")
S[58] = dict(raw=r"""Step 1: Use the work formula
\( M_{1} D_{1} H_{1} = M_{2} D_{2} H_{2} \) for the same work.
Step 2: Put in the values
\( 40 \times 50 \times 9 = M_{2} \times 75 \times 6 \).
Step 3: Calculate both sides
\( 18000 = 450 M_{2} \).
Step 4: Solve
\( M_{2} = \dfrac{18000}{450} = 40 \) men — 75 days × 6 h = 450 h, the same as 50 days × 9 h, so the same number of men is needed.""", trick=r"Compare total hours: 50 × 9 = 450 = 75 × 6, so no change in men.")
S[59] = dict(raw=r"""Step 1: Find the total distance
When two trains cross each other, the distance = sum of their lengths = \( 500 + 200 = 700 \) m.
Step 2: Find the relative speed
In opposite directions the relative speed is the sum of the speeds.
Step 3: Use speed = distance ÷ time
Total speed = \( \dfrac{700}{35} \).
Step 4: Calculate
\( 700 \div 35 = 20 \) m/s.""", trick=r"Opposite directions: (L₁ + L₂) ÷ t = sum of speeds.")
S[60] = dict(raw=r"""Step 1: Convert the speed to m/s
\( 10 \times \dfrac{5}{18} = \dfrac{50}{18} = \dfrac{25}{9} \) m/s.
Step 2: Distance to cover
To pass a standing man the train covers its own length, 250 m.
Step 3: Find the time in seconds
Time = \( 250 \div \dfrac{25}{9} = 250 \times \dfrac{9}{25} = 90 \) s.
Step 4: Convert to minutes
\( \dfrac{90}{60} = \dfrac{3}{2} \) minutes.""", trick=r"10 km/h ≈ 2.78 m/s; 250 m ÷ 2.78 ≈ 90 s = 1.5 min.")
