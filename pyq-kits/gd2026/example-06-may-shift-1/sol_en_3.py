S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket first
\( 42 + 19 = 61 \)
Step 2: Then the multiplication
\( 65 \times 2 = 130 \), so the expression becomes \( 91 + 32 - 28 + 130 - 61 \)
Step 3: Add the positive terms
\( 91 + 32 + 130 = 253 \)
Step 4: Subtract the rest
\( 253 - 28 - 61 = 164 \)""", trick=r"BODMAS: bracket, then ×, then add all + terms and subtract all − terms.")
S[42] = dict(raw=r"""Step 1: Solve the bracket
\( 33 \div 3 = 11 \)
Step 2: Solve “of”
“18 of 1” means \( 18 \times 1 = 18 \)
Step 3: Write the expression again
\( 79 + 36 - 44 + 18 + 11 + 27 \)
Step 4: Simplify
\( 79 + 36 + 18 + 11 + 27 = 171 \) and \( 171 - 44 = 127 \)""", trick=r"“of” means multiply and is done before + and −.")
S[43] = dict(raw=r"""Step 1: Use the rule for two numbers
\( \text{HCF} \times \text{LCM} = \text{product of the two numbers} \)
Step 2: Put in the values
\( 18 \times 540 = 90 \times x \)
Step 3: Solve
\( x = \dfrac{18 \times 540}{90} = \dfrac{9720}{90} = 108 \)
Step 4: Check
\( 90 = 18 \times 5 \) and \( 108 = 18 \times 6 \); 5 and 6 are co-prime, so HCF = 18 and LCM \( = 18 \times 5 \times 6 = 540 \) ✓""", trick=r"Other number = HCF × LCM ÷ given number.")
S[44] = dict(raw=r"""Step 1: Factorise the numerator
\( a^{4} - b^{4} = (a^{2} - b^{2})(a^{2} + b^{2}) \) with \( a = 0.7 \), \( b = 0.3 \)
Step 2: Cancel the common factor
\( \dfrac{(a^{2} - b^{2})(a^{2} + b^{2})}{a^{2} + b^{2}} = a^{2} - b^{2} \)
Step 3: Put in the values
\( (0.7)^{2} - (0.3)^{2} = 0.49 - 0.09 \)
Step 4: Answer
\( 0.49 - 0.09 = 0.40 \)""", trick=r"(a⁴ − b⁴) ÷ (a² + b²) = a² − b² = (a + b)(a − b) = 1 × 0.4.")
S[45] = dict(raw=r"""Step 1: Take a common denominator
\( \dfrac{1}{4 + \sqrt{2}} + \dfrac{1}{4 - \sqrt{2}} = \dfrac{(4 - \sqrt{2}) + (4 + \sqrt{2})}{(4 + \sqrt{2})(4 - \sqrt{2})} \)
Step 2: Simplify the numerator
\( (4 - \sqrt{2}) + (4 + \sqrt{2}) = 8 \)
Step 3: Simplify the denominator
\( (4 + \sqrt{2})(4 - \sqrt{2}) = 16 - 2 = 14 \)
Step 4: Answer
\( \dfrac{8}{14} = \dfrac{4}{7} \)""", trick=r"1/(a + √b) + 1/(a − √b) = 2a/(a² − b).")
S[46] = dict(raw=r"""Step 1: Find the inner square roots
\( \sqrt{108900} = 330 \) because \( 330^{2} = 108900 \)
Step 2: The second inner root
\( \sqrt{12321} = 111 \) because \( 111^{2} = 12321 \)
Step 3: Add them
\( 330 + 111 = 441 \)
Step 4: Take the outer square root
\( \sqrt{441} = 21 \)""", trick=r"Work from the inside out: √108900 = 330, √12321 = 111, √441 = 21.")
S[47] = dict(raw=r"""Step 1: Size of the garden with the path
The path is outside, so add 2 m on each side: \( 150 + 4 = 154 \) m and \( 60 + 4 = 64 \) m.
Step 2: Outer area
\( 154 \times 64 = 9856 \) m²
Step 3: Area of the garden
\( 150 \times 60 = 9000 \) m²
Step 4: Area of the path
\( 9856 - 9000 = 856 \) m² (shortcut: \( 2w(l + b + 2w) = 4 \times 214 = 856 \) ✓)""", trick=r"Outer path area = 2w(l + b + 2w).")
S[48] = dict(raw=r"""Step 1: Use the formula for the sum of squares
\( 1^{2} + 2^{2} + \ldots + n^{2} = \dfrac{n(n + 1)(2n + 1)}{6} \)
Step 2: Put n = 30
\( \dfrac{30 \times 31 \times 61}{6} \)
Step 3: Simplify
\( \dfrac{30}{6} = 5 \), so the sum \( = 5 \times 31 \times 61 \)
Step 4: Answer
\( 5 \times 31 = 155 \) and \( 155 \times 61 = 9455 \)""", trick=r"Σn² = n(n + 1)(2n + 1)/6.")
S[49] = dict(raw=r"""Step 1: Use the side–diagonal relation
The diagonals of a rhombus bisect each other at right angles, so \( d_{1}^{2} + d_{2}^{2} = 4a^{2} = 4 \times 225 = 900 \)
Step 2: Square the sum of the diagonals
\( (d_{1} + d_{2})^{2} = 42^{2} = 1764 \)
Step 3: Find the product of the diagonals
\( 2d_{1}d_{2} = 1764 - 900 = 864 \), so \( d_{1}d_{2} = 432 \)
Step 4: Area
\( \text{Area} = \dfrac{d_{1}d_{2}}{2} = \dfrac{432}{2} = 216 \) cm² (the diagonals are 24 cm and 18 cm)""", trick=r"Rhombus: d₁² + d₂² = 4a²; area = d₁d₂/2.")
S[50] = dict(raw=r"""Step 1: Let the old average be x
Total weight of 39 students \( = 39x \)
Step 2: Write the new total
After the new student joins, \( 39x + 40 = 40(x - 0.5) \)
Step 3: Solve
\( 39x + 40 = 40x - 20 \Rightarrow x = 60 \) kg
Step 4: New average
\( 60 - 0.5 = 59.5 \) kg""", trick=r"New average = newcomer's weight + old count × fall in average = 40 + 39 × 0.5 = 59.5.")
S[51] = dict(raw=r"""Step 1: What we know
Only two facts are given: the average is p and the smallest number is 22.
Step 2: Test statement I
Numbers 22 and 30 have average \( \dfrac{22 + 30}{2} = 26 \), not 35, so p need not be 35.
Step 3: Test statement II
Numbers 22 and 30 have largest number 30, not 50, so 50 need not be the largest number.
Step 4: Conclusion
Neither statement must always be true; we only know \( p \ge 22 \).""", trick=r"“Always true” → one counter-example is enough to reject a statement.")
S[52] = dict(raw=r"""Step 1: Write the numbers with the ratio
Let the numbers be \( 7k \) and \( 9k \).
Step 2: Use the HCF
7 and 9 are co-prime, so \( \text{HCF}(7k, 9k) = k \), hence \( k = 3 \).
Step 3: Find the numbers
\( 7 \times 3 = 21 \) and \( 9 \times 3 = 27 \)
Step 4: Check
\( 21 : 27 = 7 : 9 \) and \( \text{HCF}(21, 27) = 3 \) ✓ (14, 18 has HCF 2; 28, 36 has HCF 4).""", trick=r"Ratio a:b in lowest terms → numbers = a × HCF and b × HCF.")
S[53] = dict(raw=r"""Step 1: Let the mixture needed be M kg
16% of M must be 64 kg.
Step 2: Write the equation
\( \dfrac{16}{100} \times M = 64 \)
Step 3: Solve
\( M = \dfrac{64 \times 100}{16} = 400 \) kg
Step 4: Check
\( 16\% \) of 400 \( = 0.16 \times 400 = 64 \) kg ✓""", trick=r"Whole = part ÷ percentage × 100.")
S[54] = dict(raw=r"""Step 1: Write CP and SP in parts
\( \text{CP} : \text{SP} = 5 : 2 \), so let CP = 5 parts and SP = 2 parts.
Step 2: Find the loss in parts
Loss \( = 5 - 2 = 3 \) parts
Step 3: Value of one part
3 parts = ₹300, so 1 part \( = \dfrac{300}{3} = 100 \), i.e. ₹100
Step 4: Cost price
\( \text{CP} = 5 \times 100 = 500 \), i.e. ₹500""", trick=r"Loss = CP parts − SP parts; then scale up.")
S[55] = dict(raw=r"""Step 1: Write CP and SP in parts
\( \text{CP} : \text{SP} = 10 : 13 \), so CP = 10 parts and SP = 13 parts.
Step 2: Find the profit
Profit \( = 13 - 10 = 3 \) parts
Step 3: Form the ratio
\( \text{Profit} : \text{CP} = 3 : 10 \)
Step 4: Check
Profit% \( = \dfrac{3}{10} \times 100 = 30\% \), which matches a CP of 10 rising to an SP of 13 ✓""", trick=r"Profit-to-CP ratio = (SP − CP) ÷ CP.")
S[56] = dict(raw=r"""Step 1: Convert to minutes
Actual time \( = 8 \times 60 + 20 = 500 \) minutes; estimate \( = 8 \times 60 + 40 = 520 \) minutes.
Step 2: Find the error
\( 520 - 500 = 20 \) minutes
Step 3: Error percentage on the actual value
\( \dfrac{20}{500} \times 100 \)
Step 4: Answer
\( \dfrac{2000}{500} = 4\% \)""", trick=r"Error % = error ÷ true value × 100.")
S[57] = dict(raw=r"""Step 1: Write what is given
\( \dfrac{1}{5} \) of the tank is emptied in 36 minutes.
Step 2: Scale to the whole tank
The whole tank is 5 times as much: time \( = 36 \times 5 \)
Step 3: Calculate
\( 36 \times 5 = 180 \) minutes
Step 4: Check
In 180 minutes the pipe empties \( \dfrac{180}{36} \times \dfrac{1}{5} = 1 \) whole tank ✓""", trick=r"Time for whole = time for the part ÷ the fraction.")
S[58] = dict(raw=r"""Step 1: Take the total work as the LCM of 15, 25 and 50
Total work \( = 150 \) units. A does \( \dfrac{150}{15} = 10 \), B does \( \dfrac{150}{25} = 6 \) and C does \( \dfrac{150}{50} = 3 \) units a day.
Step 2: Work done in the first 5 days
Together they do \( 10 + 6 + 3 = 19 \) units a day, so in 5 days \( 19 \times 5 = 95 \) units.
Step 3: Work left
\( 150 - 95 = 55 \) units
Step 4: Time taken by C alone
\( \dfrac{55}{3} = 18\dfrac{1}{3} \) days""", trick=r"Total work = LCM; units per day = LCM ÷ days.")
S[59] = dict(raw=r"""Step 1: Know the conversion
\( 1 \text{ km/h} = \dfrac{1000}{3600} \text{ m/s} = \dfrac{5}{18} \text{ m/s} \)
Step 2: Multiply
\( 108 \times \dfrac{5}{18} \)
Step 3: Simplify
\( \dfrac{108}{18} = 6 \) and \( 6 \times 5 = 30 \)
Step 4: Answer
The speed is 30 m/s.""", trick=r"km/h → m/s: multiply by 5/18.")
S[60] = dict(raw=r"""Step 1: Convert the speed
\( 54 \times \dfrac{5}{18} = 15 \) m/s
Step 2: Distance covered while crossing the platform
\( 15 \times 18 = 270 \) m = length of train + length of platform
Step 3: Use the given relation
Let the train be L m; the platform is 2L m, so \( L + 2L = 3L = 270 \)
Step 4: Answer
\( L = \dfrac{270}{3} = 90 \) m""", trick=r"Crossing a platform: distance = train + platform.")
