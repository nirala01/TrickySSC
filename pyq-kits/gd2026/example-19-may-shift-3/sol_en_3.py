S = {}
S[41] = dict(raw=r"""Step 1: Solve the bracket
\( 31 + 16 = 47 \).
Step 2: Multiply
\( 39 \times 2 = 78 \).
Step 3: Rewrite the expression
\( 84 - 56 + 78 - 47 \).
Step 4: Work from left to right
\( 84 - 56 = 28 \), \( 28 + 78 = 106 \), \( 106 - 47 = 59 \).""", trick=r"Positives \( 84 + 78 = 162 \); negatives \( 56 + 47 = 103 \); \( 162 - 103 = 59 \).")
S[42] = dict(raw=r"""Step 1: Solve the bracket
\( 42 \div 2 = 21 \).
Step 2: Add all the positive terms
\( 93 + 19 + 21 + 33 + 26 = 192 \).
Step 3: Add all the negative terms
\( 28 + 17 = 45 \).
Step 4: Subtract
\( 192 - 45 = 147 \).""", trick=r"Sum of positives − sum of negatives \( = 192 - 45 = 147 \).")
S[43] = dict(raw=r"""Step 1: Write the proportion
Time ∝ \( r^{3} \), so \( \dfrac{T_2}{T_1} = \left(\dfrac{r_2}{r_1}\right)^{3} \).
Step 2: Put in the values
\( \dfrac{T_2}{5} = \left(\dfrac{20}{10}\right)^{3} = 2^{3} = 8 \).
Step 3: Find the new time
\( T_2 = 5 \times 8 = 40 \) minutes.
Step 4: Find the additional time
\( 40 - 5 = 35 \) minutes more than the smaller balloon.""", trick=r"Radius doubles → time × 8 → 40 min; extra \( = 40 - 5 = 35 \) min.")
S[44] = dict(raw=r"""Step 1: Find the share of tin in each alloy
Alloy 1: \( \dfrac{5}{8} \); Alloy 2: \( \dfrac{3}{4} \); required mixture (tin to copper 4 to 2): \( \dfrac{4}{6} = \dfrac{2}{3} \).
Step 2: Use alligation
Alloy 1 share \( = \dfrac{3}{4} - \dfrac{2}{3} = \dfrac{1}{12} \); Alloy 2 share \( = \dfrac{2}{3} - \dfrac{5}{8} = \dfrac{1}{24} \).
Step 3: Get the ratio
Alloy 1 to Alloy 2 \( = \dfrac{1}{12} \div \dfrac{1}{24} = 2 \), i.e. 2 parts to 1 part.
Step 4: Find the quantity
1 part = 20 kg (the second alloy), so the first alloy \( = 2 \times 20 = 40 \) kg.
Check: tin \( = 25 + 15 = 40 \) kg, copper \( = 15 + 5 = 20 \) kg, and \( 40 \div 20 = 2 \) ✓.""", trick=r"Alligation on tin fractions \( \dfrac{5}{8}, \dfrac{3}{4} → \dfrac{2}{3} \) gives 2 to 1 → 40 kg.")
S[45] = dict(raw=r"""Step 1: Let the original speed be v km/h
Distance \( = 4v \).
Step 2: Write the distance at the reduced speed
Distance \( = 5(v - 20) \).
Step 3: Equate and solve
\( 4v = 5v - 100 \Rightarrow v = 100 \) km/h.
Step 4: Check
\( 4 \times 100 = 400 \) km and \( 5 \times 80 = 400 \) km ✓.""", trick=r"Times 4 and 5 → speeds in ratio 5 to 4; the 1 part = 20 km/h, so speed \( = 5 \times 20 = 100 \).")
S[46] = dict(raw=r"""Step 1: Notice the pattern
In \( \dfrac{13}{16}, \dfrac{11}{14}, \dfrac{15}{18}, \dfrac{8}{11} \), the denominator is 3 more than the numerator each time.
Step 2: Use the rule
When the gap between numerator and denominator is the same, the fraction with the smallest numerator is the smallest (it is farthest from 1).
Step 3: Confirm with decimals
\( \dfrac{8}{11} \approx 0.727 \), \( \dfrac{11}{14} \approx 0.786 \), \( \dfrac{13}{16} = 0.8125 \), \( \dfrac{15}{18} \approx 0.833 \).
Step 4: Answer
The smallest is \( \dfrac{8}{11} \).""", trick=r"Same gap (3) → smallest numerator wins → \( \dfrac{8}{11} \).")
S[47] = dict(raw=r"""Step 1: Use the identity
\( a^{2} - b^{2} = (a + b)(a - b) \).
Step 2: Put in the gap
Consecutive odd numbers differ by 2, so \( (a + b) \times 2 = 80 \).
Step 3: Solve
\( a + b = 40 \).
Step 4: Check
The numbers are 21 and 19: \( 441 - 361 = 80 \) ✓, and \( 21 + 19 = 40 \).""", trick=r"Difference of squares ÷ 2 = sum → \( 80 \div 2 = 40 \).")
S[48] = dict(raw=r"""Step 1: List the odd numbers between 70 and 80
71, 73, 75, 77, 79 (even numbers are not prime).
Step 2: Remove the multiples of 5 and 7
75 ends in 5, and \( 77 = 7 \times 11 \).
Step 3: Test the rest
71, 73 and 79 are not divisible by 2, 3, 5 or 7 (we need to test only up to \( \sqrt{80} \approx 9 \)), so they are prime.
Step 4: Count
There are 3 prime numbers: 71, 73 and 79.""", trick=r"70s primes: 71, 73, 79 → 3.")
S[49] = dict(raw=r"""Step 1: Identify the AP
First term \( a = 1 \), common difference \( d = 3 \), last term \( l = 100 \).
Step 2: Find the number of terms
\( n = \dfrac{l - a}{d} + 1 = \dfrac{99}{3} + 1 = 34 \).
Step 3: Use the sum formula
\( S = \dfrac{n}{2}(a + l) = \dfrac{34}{2} \times 101 \).
Step 4: Calculate
\( 17 \times 101 = 1717 \).""", trick=r"\( n = 34 \); sum \( = 17 \times 101 = 1717 \).")
S[50] = dict(raw=r"""Step 1: Use Pythagoras
The diagonal of a rectangle \( = \sqrt{l^{2} + b^{2}} \).
Step 2: Put in the values
\( \sqrt{3^{2} + 4^{2}} = \sqrt{9 + 16} \).
Step 3: Simplify
\( \sqrt{25} = 5 \).
Step 4: Answer
The diagonal is 5 cm (the 3–4–5 triplet).""", trick=r"Sides 3 and 4 → diagonal 5 (Pythagorean triplet).")
S[51] = dict(raw=r"""Step 1: Use Pythagoras
Diagonal \( = \sqrt{l^{2} + b^{2}} \).
Step 2: Put in the values
\( \sqrt{15^{2} + 20^{2}} = \sqrt{225 + 400} \).
Step 3: Simplify
\( \sqrt{625} = 25 \).
Step 4: Check with the triplet
15 and 20 are \( 5 \times 3 \) and \( 5 \times 4 \), so the diagonal is \( 5 \times 5 = 25 \) cm.""", trick=r"\( 5 \times (3, 4, 5) \) → diagonal 25 cm.")
S[52] = dict(raw=r"""Step 1: Write the perimeter formula
\( P = 2(l + b) \).
Step 2: Put in the values
\( 24 = 2(5 + b) \).
Step 3: Solve
\( 5 + b = 12 \Rightarrow b = 7 \) cm.
Step 4: Check
\( 2(5 + 7) = 24 \) cm ✓.""", trick=r"Half the perimeter − length \( = 12 - 5 = 7 \).")
S[53] = dict(raw=r"""Step 1: Write the series as 2 times natural numbers
\( 2 + 4 + \ldots + 496 = 2(1 + 2 + \ldots + 248) \).
Step 2: Use the sum of the first n natural numbers
\( 1 + 2 + \ldots + n = \dfrac{n(n + 1)}{2} \), with \( n = 248 \).
Step 3: Simplify
\( 2 \times \dfrac{248 \times 249}{2} = 248 \times 249 \).
Step 4: Calculate
\( 248 \times 249 = 248 \times 250 - 248 = 62000 - 248 = 61752 \).""", trick=r"Sum of the first n even numbers \( = n(n + 1) = 248 \times 249 = 61752 \).")
S[54] = dict(raw=r"""Step 1: Total runs of 7 players
\( 7 \times 60 = 420 \).
Step 2: Runs of the first 6 players
\( 125 + 50 + 18 + 36 + 40 + 42 = 311 \).
Step 3: Runs of the 7th player
\( 420 - 311 = 109 \).
Step 4: Count the players below 109
50, 18, 36, 40 and 42 are less than 109; only 125 is more. So 5 players scored less than the 7th player.""", trick=r"7th player \( = 420 - 311 = 109 \); five scores are below it.")
S[55] = dict(raw=r"""Step 1: Use alligation on the average costs
Blue ₹70, red ₹50, overall ₹60.
Step 2: Find the ratio
Blue to red \( = (60 - 50) \) to \( (70 - 60) = 10 \) to 10, i.e. 1 to 1.
Step 3: Split the 30 hats
Red hats \( = \dfrac{1}{2} \times 30 = 15 \).
Step 4: Check
\( 15 \times 70 + 15 \times 50 = 1050 + 750 = 1800 \), and \( 1800 \div 30 = 60 \) ✓.""", trick=r"Overall average is exactly midway between 70 and 50 → equal numbers → 15 red.")
S[56] = dict(raw=r"""Step 1: 40% of 350
\( \dfrac{40}{100} \times 350 = 140 \).
Step 2: 20% of 600
\( \dfrac{20}{100} \times 600 = 120 \).
Step 3: Add
\( 140 + 120 = 260 \).
Step 4: Answer
The value is 260.""", trick=r"\( 4 \times 35 = 140 \) and \( 2 \times 60 = 120 \) → 260.")
S[57] = dict(raw=r"""Step 1: Find the cost price
CP \( = \) SP − profit \( = 4400 - 400 = 4000 \).
Step 2: Write the formula
Profit% \( = \dfrac{\text{Profit}}{\text{CP}} \times 100 \).
Step 3: Put in the values
\( \dfrac{400}{4000} \times 100 = 10\% \).
Step 4: Answer
The profit is 10 percent (profit is always on the cost price, not on ₹4400).""", trick=r"Profit% on CP: \( \dfrac{400}{4000} = 10\% \).")
S[58] = dict(raw=r"""Step 1: Use the chain rule
\( \dfrac{M_1 D_1}{W_1} = \dfrac{M_2 D_2}{W_2} \).
Step 2: Put in the values
\( \dfrac{15 \times 40}{1} = \dfrac{M_2 \times 20}{\dfrac{1}{2}} \).
Step 3: Solve
\( 600 = 40 M_2 \Rightarrow M_2 = 15 \).
Step 4: Check
Half the work needs \( 300 \) man-days; \( 15 \times 20 = 300 \) ✓.""", trick=r"Half the work in half the time → same number of men, 15.")
S[59] = dict(raw=r"""Step 1: Take total work = LCM of 8, 6 and 12 = 24 units
M + R = \( \dfrac{24}{8} = 3 \) units/day, R + P = \( \dfrac{24}{6} = 4 \) units/day, P + M = \( \dfrac{24}{12} = 2 \) units/day.
Step 2: Add the three pairs
\( 2(M + R + P) = 3 + 4 + 2 = 9 \Rightarrow M + R + P = 4.5 \) units/day.
Step 3: Work in 3 days
\( 4.5 \times 3 = 13.5 \) units.
Step 4: Write it as a fraction of the work
\( \dfrac{13.5}{24} = \dfrac{27}{48} = \dfrac{9}{16} \).""", trick=r"All three together \( = \dfrac{1}{2}\left(\dfrac{1}{8} + \dfrac{1}{6} + \dfrac{1}{12}\right) = \dfrac{3}{16} \) a day → \( \dfrac{9}{16} \) in 3 days.")
S[60] = dict(raw=r"""Step 1: Find the value of one ratio part
Boys to girls \( = 3 : 5 \), so \( 3 + 5 = 8 \) parts \( = 360 \) and 1 part \( = 45 \).
Step 2: Find the present number of boys
\( 3 \times 45 = 135 \).
Step 3: Add the new admissions
\( 135 + 30 = 165 \).
Step 4: Answer
There are now 165 boys (girls stay \( 5 \times 45 = 225 \)).""", trick=r"\( \dfrac{3}{8} \times 360 = 135 \); \( 135 + 30 = 165 \).")
