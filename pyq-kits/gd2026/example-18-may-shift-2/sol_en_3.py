S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket
\( 27 \times 1 = 27 \).
Step 2: Do the division
\( 42 \div 6 = 7 \).
Step 3: Add and subtract from left to right
\( 66 + 38 - 27 + 7 + 33 - 14 \): \( 66 + 38 = 104 \), \( 104 - 27 = 77 \), \( 77 + 7 = 84 \), \( 84 + 33 = 117 \), \( 117 - 14 = 103 \).
Step 4: Answer
The value is 103.""", trick=r"BODMAS: bracket, then ÷, then + and − from left to right.")
S[42] = dict(raw=r"""Step 1: Multiply inside the root
\( 0.81 \times 0.04 = 0.0324 \).
Step 2: Split the root
\( \sqrt{0.81 \times 0.04} = \sqrt{0.81} \times \sqrt{0.04} \).
Step 3: Take each root
\( \sqrt{0.81} = 0.9 \) and \( \sqrt{0.04} = 0.2 \).
Step 4: Answer
\( 0.9 \times 0.2 = 0.18 \). Check: \( 0.18^{2} = 0.0324 \) ✓.""", trick=r"√(ab) = √a × √b: 0.9 × 0.2 = 0.18.")
S[43] = dict(raw=r"""Step 1: Write 3.375 as a fraction
\( 3.375 = \dfrac{3375}{1000} \).
Step 2: Take the cube root
\( \sqrt[3]{\dfrac{3375}{1000}} = \dfrac{15}{10} = 1.5 \), because \( 15^{3} = 3375 \).
Step 3: Take the square root
\( \sqrt{0.81} = 0.9 \).
Step 4: Multiply
\( 1.5 \times 0.9 = 1.35 \).""", trick=r"∛3.375 = 1.5 and √0.81 = 0.9 → 1.35.")
S[44] = dict(raw=r"""Step 1: Expand the numerator
\( (\sqrt{3} + \sqrt{2})^{2} = 3 + 2 + 2\sqrt{6} = 5 + 2\sqrt{6} \).
Step 2: Rationalise the denominator
\( \dfrac{1}{\sqrt{3} - \sqrt{2}} = \dfrac{\sqrt{3} + \sqrt{2}}{3 - 2} = \sqrt{3} + \sqrt{2} \).
Step 3: Multiply
\( (5 + 2\sqrt{6})(\sqrt{3} + \sqrt{2}) = 5\sqrt{3} + 5\sqrt{2} + 2\sqrt{18} + 2\sqrt{12} \).
Step 4: Simplify the surds
\( 2\sqrt{18} = 6\sqrt{2} \) and \( 2\sqrt{12} = 4\sqrt{3} \), so the value is \( 9\sqrt{3} + 11\sqrt{2} \).""", trick=r"The expression is (√3 + √2)³ = 9√3 + 11√2.")
S[45] = dict(raw=r"""Step 1: Estimate the middle number
\( \sqrt[3]{3315} \) is a little more than 14, so the three odd numbers are near 15.
Step 2: Try 13, 15, 17
\( 13 \times 15 = 195 \) and \( 195 \times 17 = 3315 \) ✓.
Step 3: Check by factorising
\( 3315 = 3 \times 5 \times 13 \times 17 = 13 \times 15 \times 17 \).
Step 4: Answer
The largest of the three numbers is 17.""", trick=r"3315 ends in 5, so 15 is a factor; 3315 ÷ 15 = 221 = 13 × 17.")
S[46] = dict(raw=r"""Step 1: Pair the numbers
\( \dfrac{0.064}{0.004} = 16 \) and \( \dfrac{0.256}{0.16} = 1.6 \).
Step 2: Multiply
\( 16 \times 1.6 = 25.6 \).
Step 3: Take the square root
\( \sqrt{25.6} \) lies between \( \sqrt{25} = 5 \) and \( \sqrt{26.01} = 5.1 \); more exactly \( \sqrt{25.6} \approx 5.0596 \).
Step 4: Answer
To two decimal places the value is about 5.06. Check: \( 5.06^{2} = 25.6036 \approx 25.6 \) ✓.""", trick=r"Pair top with bottom: 16 × 1.6 = 25.6, and √25.6 ≈ 5.06.")
S[47] = dict(raw=r"""Step 1: Take 3 common
\( 3 + 6 + 9 + \ldots + 300 = 3(1 + 2 + 3 + \ldots + 100) \).
Step 2: Use the sum of the first n natural numbers
\( 1 + 2 + \ldots + 100 = \dfrac{100 \times 101}{2} = 5050 \).
Step 3: Multiply
\( 3 \times 5050 = 15150 \).
Step 4: Check with the AP formula
\( n = 100 \), sum \( = \dfrac{n}{2}(a + l) = 50 \times (3 + 300) = 15150 \) ✓.""", trick=r"3 × (sum of 1 to 100) = 3 × 5050 = 15150.")
S[48] = dict(raw=r"""Step 1: Recall the rules
A number is divisible by 9 if its digit sum is divisible by 9; by 11 if (sum of alternate digits) − (sum of the others) is 0 or a multiple of 11.
Step 2: Check 4950, 7425 and 7623 for 9
Digit sums: \( 4 + 9 + 5 + 0 = 18 \), \( 7 + 4 + 2 + 5 = 18 \), \( 7 + 6 + 2 + 3 = 18 \) — all divisible by 9.
Step 3: Check 7841
Digit sum \( 7 + 8 + 4 + 1 = 20 \), not divisible by 9. For 11: \( (7 + 4) - (8 + 1) = 2 \), not a multiple of 11.
Step 4: Answer
7841 is divisible neither by 9 nor by 11.""", trick=r"Digit sum 18 means divisible by 9 — only 7841 has a digit sum of 20.")
S[49] = dict(raw=r"""Step 1: Find the outer dimensions
The path is outside, so add 1.5 m on each side: length \( 90 + 3 = 93 \) m and breadth \( 50 + 3 = 53 \) m.
Step 2: Outer area
\( 93 \times 53 = 4929 \) square metres.
Step 3: Garden area
\( 90 \times 50 = 4500 \) square metres.
Step 4: Area of the path
\( 4929 - 4500 = 429 \) square metres. Check: \( 2 \times 1.5 \times (90 + 50) + 4 \times 1.5^{2} = 420 + 9 = 429 \) ✓.""", trick=r"Outer path area = 2w(l + b) + 4w².")
S[50] = dict(raw=r"""Step 1: Find the total
Average \( = N \), so the sum of the 30 numbers \( = 30N \).
Step 2: Divide each number by 6
The new sum is \( \dfrac{30N}{6} = 5N \).
Step 3: Find the new average
\( \dfrac{5N}{30} = \dfrac{N}{6} \).
Step 4: Rule
When every number is divided by 6, the average is also divided by 6.""", trick=r"Divide every number by k → the average is divided by k.")
S[51] = dict(raw=r"""Step 1: Understand the question
The longest rod that cuts all three pieces exactly is the HCF of 90, 75 and 105.
Step 2: Factorise
\( 90 = 2 \times 3^{2} \times 5 \), \( 75 = 3 \times 5^{2} \), \( 105 = 3 \times 5 \times 7 \).
Step 3: Take the common factors
HCF \( = 3 \times 5 = 15 \).
Step 4: Answer
The longest rod is 15 cm (90 cm gives 6 rods, 75 cm gives 5, 105 cm gives 7, with nothing wasted).""", trick=r"Longest equal piece = HCF of the lengths.")
S[52] = dict(raw=r"""Step 1: Form the equation
Let the number be x. Then \( x = 90 + \dfrac{25}{100}x \).
Step 2: Simplify
\( x - \dfrac{x}{4} = 90 \), so \( \dfrac{3x}{4} = 90 \).
Step 3: Solve
\( x = \dfrac{90 \times 4}{3} = 120 \).
Step 4: Check
25% of 120 is 30, and \( 90 + 30 = 120 \) ✓.""", trick=r"75% of the number = 90 → number = 120.")
S[53] = dict(raw=r"""Step 1: Use the ratio
Let CP \( = 2x \) and SP \( = 5x \).
Step 2: Find the profit in parts
Profit \( = 5x - 2x = 3x \).
Step 3: Use the given profit
\( 3x = ₹900 \), so \( x = ₹300 \).
Step 4: Answer
CP \( = 2x = ₹600 \). Check: SP \( = ₹1500 \) and \( 1500 - 600 = 900 \) ✓.""", trick=r"3 parts = ₹900, so CP (2 parts) = ₹600.")
S[54] = dict(raw=r"""Step 1: Convert to grams
True weight \( = 6600 \) g and measured weight \( = 7590 \) g.
Step 2: Find the error
\( 7590 - 6600 = 990 \) g.
Step 3: Error percentage on the true value
\( \dfrac{990}{6600} \times 100 = 15\% \).
Step 4: Answer
The error is 15%.""", trick=r"Error % = error ÷ true value × 100 = 990 ÷ 6600 × 100.")
S[55] = dict(raw=r"""Step 1: Take a convenient SP
Let SP \( = ₹100 \). Profit is 20% of SP \( = ₹20 \).
Step 2: Find the CP
CP \( = 100 - 20 = ₹80 \).
Step 3: Form the ratio
Profit to CP \( = 20 : 80 \).
Step 4: Simplify
\( 20 : 80 = 1 : 4 \).""", trick=r"Profit on SP: SP 100, profit 20, CP 80 → \( 1 : 4 \).")
S[56] = dict(raw=r"""Step 1: Find the work per hour
The pipe empties the tank in 36 hours, so in 1 hour it empties \( \dfrac{1}{36} \) of the tank.
Step 2: Multiply by the time
In 6 hours it empties \( 6 \times \dfrac{1}{36} \).
Step 3: Simplify
\( \dfrac{6}{36} = \dfrac{1}{6} \).
Step 4: Answer
It empties \( \dfrac{1}{6} \) of the tank.""", trick=r"Part done = time taken ÷ total time = 6 ÷ 36.")
S[57] = dict(raw=r"""Step 1: Times for A and B
A takes 80 days and takes four times as long as B, so B takes \( \dfrac{80}{4} = 20 \) days.
Step 2: Time for A and B together
\( \dfrac{1}{80} + \dfrac{1}{20} = \dfrac{1 + 4}{80} = \dfrac{1}{16} \), so A and B together take 16 days. C also takes 16 days.
Step 3: One day's work of A, B and C
\( \dfrac{1}{16} + \dfrac{1}{16} = \dfrac{1}{8} \).
Step 4: Answer
A, B and C together finish the work in 8 days.""", trick=r"C equals (A + B), so all three work at twice the (A + B) rate: 16 ÷ 2 = 8.")
S[58] = dict(raw=r"""Step 1: Recall the rule
For the same distance, time is inversely proportional to speed.
Step 2: Write the speeds
Speed of A \( = 8 \) km/hr and speed of B \( = 36 \) km/hr.
Step 3: Invert the ratio
Time of A to time of B \( = 36 : 8 \).
Step 4: Simplify
\( 36 : 8 = 9 : 2 \).""", trick=r"Same distance → time ratio is the speed ratio turned upside down.")
S[59] = dict(raw=r"""Step 1: Note what is equal
A and B start at the same time and meet at S, so both travel for the same time.
Step 2: Recall the rule
For equal time, distance is directly proportional to speed.
Step 3: Write the ratio
Distance of A to distance of B \( = 54 : 27 \).
Step 4: Simplify
\( 54 : 27 = 2 : 1 \).""", trick=r"Same time → distances in the ratio of the speeds.")
S[60] = dict(raw=r"""Step 1: Take a convenient marked price
Let MP \( = ₹100 \).
Step 2: Apply the first discount
After 10% off: \( 100 - 10 = ₹90 \).
Step 3: Apply the second discount
After 20% off on ₹90: \( 90 - 18 = ₹72 \) = SP.
Step 4: Form the ratio
MP to SP \( = 100 : 72 = 25 : 18 \).""", trick=r"Successive 10% and 20% → SP = 72% of MP.")
