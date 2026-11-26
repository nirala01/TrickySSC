S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first (BODMAS)
\( 33 + 26 = 59 \).
Step 2: Do the multiplication
\( 52 \times 2 = 104 \).
Step 3: Rewrite the expression
\( 89 - 47 + 96 - 59 + 104 \).
Step 4: Add the plus terms and subtract the minus terms
Plus: \( 89 + 96 + 104 = 289 \). Minus: \( 47 + 59 = 106 \). Result: \( 289 - 106 = 183 \).""", trick=r"Bracket → × → then group all plus and all minus terms.")
S[42] = dict(raw=r"""Step 1: Solve the bracket
\( 36 \div 6 = 6 \).
Step 2: Do the multiplication
\( 29 \times 1 = 29 \).
Step 3: Rewrite the expression
\( 87 + 22 - 6 + 29 - 13 + 18 \).
Step 4: Add and subtract
Plus: \( 87 + 22 + 29 + 18 = 156 \). Minus: \( 6 + 13 = 19 \). Result: \( 156 - 19 = 137 \).""", trick=r"Group the positives and the negatives, then subtract once.")
S[43] = dict(raw=r"""Step 1: Identify the tool
Equal shares to the maximum number of students → the HCF of 84 and 108.
Step 2: Factorise
\( 84 = 2^{2} \times 3 \times 7 \) and \( 108 = 2^{2} \times 3^{3} \).
Step 3: Find the HCF
Common factors: \( 2^{2} \times 3 = 12 \) students.
Step 4: Find each share
Chocolates: \( \dfrac{84}{12} = 7 \); candies: \( \dfrac{108}{12} = 9 \). So 12 students get 7 chocolates and 9 candies each.""", trick=r"'Maximum number of equal groups' always means HCF.")
S[44] = dict(raw=r"""Step 1: Spot the identity
\( (a - b)^{2} + 4ab = a^{2} - 2ab + b^{2} + 4ab = (a + b)^{2} \).
Step 2: Set the values
\( a = 12.35 \), \( b = 7.65 \).
Step 3: Add a and b
\( a + b = 12.35 + 7.65 = 20 \).
Step 4: Square
\( 20^{2} = 400 \).""", trick=r"\( (a - b)^{2} + 4ab = (a + b)^{2} \) — just add the two numbers and square.")
S[45] = dict(raw=r"""Step 1: Use the identity
\( (a + b)^{2} + (a - b)^{2} = 2(a^{2} + b^{2}) \).
Step 2: Set the values
\( a = \sqrt{3} \), \( b = \sqrt{2} \), so \( a^{2} = 3 \) and \( b^{2} = 2 \).
Step 3: Substitute
\( 2(3 + 2) = 2 \times 5 \).
Step 4: Answer
\( 2 \times 5 = 10 \).""", trick=r"\( (a + b)^{2} + (a - b)^{2} = 2(a^{2} + b^{2}) \): the 2ab terms cancel.")
S[46] = dict(raw=r"""Step 1: Use \( a^{2} - b^{2} = (a + b)(a - b) \)
\( (6.203)^{2} - (5.797)^{2} = (6.203 + 5.797)(6.203 - 5.797) \).
Step 2: Simplify the two brackets
\( 6.203 + 5.797 = 12 \) and \( 6.203 - 5.797 = 0.406 \).
Step 3: Multiply
\( 12 \times 0.406 = 4.872 \).
Step 4: Divide by 0.812
\( \dfrac{4.872}{0.812} = 6 \) (note \( 0.812 = 2 \times 0.406 \), so the value is \( \dfrac{12}{2} = 6 \)).""", trick=r"The denominator is twice (a − b), so the answer is (a + b) ÷ 2.")
S[47] = dict(raw=r"""Step 1: Use Pythagoras on the diagonal
\( d^{2} = l^{2} + b^{2} \Rightarrow 15^{2} = 9^{2} + b^{2} \).
Step 2: Solve for the breadth
\( b^{2} = 225 - 81 = 144 \Rightarrow b = 12 \) cm.
Step 3: Write the area formula
Area \( = l \times b \).
Step 4: Calculate
\( 9 \times 12 = 108 \) square cm.""", trick=r"9, 12, 15 is the 3-4-5 triple × 3.")
S[48] = dict(raw=r"""Step 1: Spot the identity
\( (a - b)^{2} + 4ab = (a + b)^{2} \).
Step 2: Set the values
\( a = 412 \), \( b = 388 \).
Step 3: Add a and b
\( 412 + 388 = 800 \).
Step 4: Square
\( 800^{2} = 640000 \).""", trick=r"Same identity as always: add the two numbers, then square.")
S[49] = dict(raw=r"""Step 1: Use the perimeter
\( 2(l + b) = 48 \Rightarrow l + b = 24 \).
Step 2: Use the length–breadth relation
\( l = 3b \Rightarrow 3b + b = 24 \Rightarrow b = 6 \) cm, \( l = 18 \) cm.
Step 3: Apply Pythagoras for the diagonal
\( d = \sqrt{18^{2} + 6^{2}} = \sqrt{324 + 36} = \sqrt{360} \).
Step 4: Simplify the surd
\( \sqrt{360} = \sqrt{36 \times 10} = 6\sqrt{10} \) cm.""", trick=r"With l = 3b, the diagonal is \( b\sqrt{10} \).")
S[50] = dict(raw=r"""Step 1: Find the total
Sum of 8 numbers \( = 8 \times 57 = 456 \).
Step 2: Turn the averages into sums
Both groups have 4 numbers, so "average of first 4 = 2 × average of last 4" means sum of first 4 = 2 × sum of last 4.
Step 3: Set up the equation
Let the sum of the last 4 be x. Then \( 2x + x = 456 \Rightarrow 3x = 456 \).
Step 4: Solve
\( x = \dfrac{456}{3} = 152 \).""", trick=r"Equal-sized groups: the ratio of averages = the ratio of sums (2:1 → 3 parts).")
S[51] = dict(raw=r"""Step 1: Name the numbers
Let the 17 consecutive numbers be n, n + 1, …, n + 16.
Step 2: Find the average
For consecutive numbers the average is the middle (9th) number: \( A = n + 8 \).
Step 3: Add the smallest and the largest
\( n + (n + 16) = 2n + 16 = 2(n + 8) \).
Step 4: Express in terms of A
\( 2(n + 8) = 2A \).""", trick=r"In any AP, first + last = 2 × average.")
S[52] = dict(raw=r"""Step 1: Identify the tool
Maximum boys with equal shares of both items → the HCF of 210 and 294.
Step 2: Factorise
\( 210 = 2 \times 3 \times 5 \times 7 \) and \( 294 = 2 \times 3 \times 7^{2} \).
Step 3: Find the HCF
\( 2 \times 3 \times 7 = 42 \) boys.
Step 4: Find the chips per boy
\( \dfrac{210}{42} = 5 \) chips (and \( \dfrac{294}{42} = 7 \) toffees).""", trick=r"HCF gives the number of boys; divide to get each share.")
S[53] = dict(raw=r"""Step 1: Let the number be x
Then \( 30\% \) of x \( = 0.3x \).
Step 2: Form the equation
\( 0.3x + 70 = x \).
Step 3: Solve
\( 70 = x - 0.3x = 0.7x \Rightarrow x = \dfrac{70}{0.7} = 100 \).
Step 4: Check
\( 30\% \) of 100 \( = 30 \), and \( 30 + 70 = 100 \) ✓.""", trick=r"70 is the remaining 70% of the number → number = 100.")
S[54] = dict(raw=r"""Step 1: Relate SP and CP
With a profit of \( 30\% \), \( SP = 130\% \) of CP.
Step 2: Form the equation
\( 1.3 \times CP = 7540 \).
Step 3: Solve
\( CP = \dfrac{7540}{1.3} = 5800 \).
Step 4: Check
\( 30\% \) of ₹5800 \( = 1740 \) and \( 5800 + 1740 = 7540 \) ✓. CP = ₹5800.""", trick=r"CP = SP × \( \dfrac{100}{100 + \text{profit}\% } \).")
S[55] = dict(raw=r"""Step 1: Understand the difference
SP − CP is the profit, so the profit = ₹120.
Step 2: Find the CP
Profit \( = 30\% \) of CP → \( 0.3 \times CP = 120 \Rightarrow CP = 400 \).
Step 3: Find the SP
\( SP = 400 + 120 = 520 \).
Step 4: Check
\( \dfrac{120}{400} \times 100 = 30\% \) ✓. SP = ₹520.""", trick=r"30% → 120, so 130% → \( 120 \times \dfrac{130}{30} = 520 \).")
S[56] = dict(raw=r"""Step 1: Let the numbers be a (first) and b (second)
Given \( a + b = \dfrac{45}{20}a = 2.25a \).
Step 2: Isolate b
\( b = 2.25a - a = 1.25a \).
Step 3: Turn it into a percentage
\( \dfrac{b}{a} \times 100 = 1.25 \times 100 = 125\% \).
Step 4: Answer
The second number is \( 125\% \) of the first.""", trick=r"Subtract 1 from the multiplier: 2.25 − 1 = 1.25 → 125%.")
S[57] = dict(raw=r"""Step 1: Note the given rate
\( \dfrac{1}{4} \) of the tank is emptied in 8 minutes.
Step 2: Find the time for the whole tank
Whole tank \( = 4 \times 8 = 32 \) minutes.
Step 3: Find the time for half the tank
\( \dfrac{1}{2} \times 32 = 16 \) minutes.
Step 4: Check by ratio
\( \dfrac{1}{2} \) is twice \( \dfrac{1}{4} \), so the time doubles: \( 2 \times 8 = 16 \) ✓.""", trick=r"Half is double a quarter → double the time.")
S[58] = dict(raw=r"""Step 1: Write efficiencies as P, Q, R
\( Q + R = 8P \) and \( P + R = 5Q \).
Step 2: Express the total in two ways
\( P + Q + R = P + 8P = 9P \) and also \( = Q + 5Q = 6Q \). So \( 9P = 6Q \).
Step 3: Relate the whole team to Q
Total efficiency \( = 6Q \), so the team is 6 times as fast as Q alone.
Step 4: Find Q's time
Team takes 10 days → Q alone takes \( 6 \times 10 = 60 \) days.""", trick=r"Add the left side's missing person to each relation: total = 9P = 6Q.")
S[59] = dict(raw=r"""Step 1: Find the distance covered while crossing
Trains crossing each other cover the sum of their lengths: \( 400 + 800 = 1200 \) m.
Step 2: Use relative speed
In opposite directions, relative speed = sum of the speeds.
Step 3: Apply speed = distance ÷ time
\( \dfrac{1200}{80} = 15 \) m/s.
Step 4: Answer
The total (combined) speed of A and B is 15 m/s.""", trick=r"Opposite directions: (L₁ + L₂) ÷ t = s₁ + s₂.")
S[60] = dict(raw=r"""Step 1: Find the relative speed
The train covers its own length: \( \dfrac{400}{8} = 50 \) m/s.
Step 2: Add the speeds (opposite directions)
Let the man's speed be x; the train's is 4x. Relative speed \( = 4x + x = 5x = 50 \Rightarrow x = 10 \) m/s.
Step 3: Find the train's speed
\( 4 \times 10 = 40 \) m/s.
Step 4: Convert to km/h
\( 40 \times \dfrac{18}{5} = 144 \) km/h.""", trick=r"m/s × \( \dfrac{18}{5} \) = km/h.")
