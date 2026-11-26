S = {}
S[41] = dict(raw=r"""Step 1: Bracket first
\( 23 + 19 = 42 \)
Step 2: Multiplication next
\( 66 \times 2 = 132 \)
Step 3: Rewrite the expression
\( 132 - 44 + 42 - 18 \)
Step 4: Add and subtract from left to right
\( 132 - 44 = 88,\; 88 + 42 = 130,\; 130 - 18 = 112 \)""", trick=r"BODMAS: bracket → × → + and − from left to right.")
S[42] = dict(raw=r"""Step 1: Solve "of" inside the bracket
\( (28 \text{ of } 2) = 28 \times 2 = 56 \)
Step 2: Division and multiplication
\( 36 \div 6 = 6 \) and \( 17 \times 2 = 34 \)
Step 3: Rewrite the expression
\( 64 + 6 - 56 + 34 \)
Step 4: Add and subtract from left to right
\( 70 - 56 = 14,\; 14 + 34 = 48 \)""", trick=r"'of' means multiply; do it with the bracket before ÷ and ×.")
S[43] = dict(raw=r"""Step 1: Spot the pattern in the denominators
\( 2 = 1 \times 2,\; 6 = 2 \times 3,\; 12 = 3 \times 4,\; 20 = 4 \times 5,\; \ldots,\; 90 = 9 \times 10 \)
Step 2: Split each term
\( \dfrac{1}{n(n+1)} = \dfrac{1}{n} - \dfrac{1}{n+1} \), so \( \dfrac{1}{2} = 1 - \dfrac{1}{2},\; \dfrac{1}{6} = \dfrac{1}{2} - \dfrac{1}{3} \) and so on.
Step 3: Add — the middle terms cancel
\( \left(1 - \dfrac{1}{2}\right) + \left(\dfrac{1}{2} - \dfrac{1}{3}\right) + \ldots + \left(\dfrac{1}{9} - \dfrac{1}{10}\right) = 1 - \dfrac{1}{10} \)
Step 4: Final value
\( 1 - \dfrac{1}{10} = \dfrac{9}{10} \)""", trick=r"Sum of 1/(n(n+1)) up to n = 9 is 9/10 — the last n over (n + 1).")
S[44] = dict(raw=r"""Step 1: Write the given number in full
\( 0.6\overline{3} = 0.6333\ldots \)
Step 2: Write each option in full
\( 0.6\overline{4} = 0.6444\ldots,\; 0.6\overline{7} = 0.6777\ldots,\; 0.6\overline{1} = 0.6111\ldots,\; 0.6\overline{9} = 0.6999\ldots = 0.7 \)
Step 3: Compare the second decimal place
All start with 0.6; the next digits are 4, 7, 1 and 9 against 3. Only 1 is smaller than 3.
Step 4: Answer
\( 0.6111\ldots < 0.6333\ldots \), so \( 0.6\overline{1} \) is smaller.""", trick=r"Same first digit → compare the repeating digit (1 < 3).")
S[45] = dict(raw=r"""Step 1: Change the limits to decimals
\( 2\dfrac{1}{3} \approx 2.33 \) and \( 2\dfrac{5}{6} \approx 2.83 \)
Step 2: Convert each option
\( \dfrac{18}{7} \approx 2.57,\; \dfrac{17}{9} \approx 1.89,\; \dfrac{20}{11} \approx 1.82,\; \dfrac{38}{13} \approx 2.92 \)
Step 3: Check which lies between 2.33 and 2.83
\( 2.33 < 2.57 < 2.83 \) ✓; 1.89 and 1.82 are too small and 2.92 is too large.
Step 4: Answer
\( \dfrac{18}{7} \) lies between the two numbers.""", trick=r"Turn every fraction into a decimal and place it on the number line.")
S[46] = dict(raw=r"""Step 1: Formula
Area of a rhombus \( = \dfrac{1}{2} \times d_1 \times d_2 \)
Step 2: Substitute
\( 112 = \dfrac{1}{2} \times 14 \times d_2 \)
Step 3: Simplify
\( 112 = 7 \times d_2 \)
Step 4: Solve
\( d_2 = \dfrac{112}{7} = 16 \) cm""", trick=r"Other diagonal = 2 × area ÷ given diagonal = 224 ÷ 14 = 16.")
S[47] = dict(raw=r"""Step 1: Side of the rhombus
\( \text{side} = \dfrac{100}{4} = 25 \) cm
Step 2: Use half-diagonals
The diagonals bisect each other at right angles. Half of the given diagonal \( = \dfrac{40}{2} = 20 \) cm.
Step 3: Find the other half-diagonal (Pythagoras)
\( \sqrt{25^2 - 20^2} = \sqrt{625 - 400} = \sqrt{225} = 15 \) cm, so the other diagonal \( = 30 \) cm.
Step 4: Ratio
\( 40 : 30 = 4 : 3 \)""", trick=r"Side 25 with half-diagonal 20 → 15 (the 3-4-5 triple × 5).")
S[48] = dict(raw=r"""Step 1: Key rule
For two numbers, \( \text{HCF} \times \text{LCM} = \) product of the numbers.
Step 2: Write the equation
\( 154 \times n = 6930 \)
Step 3: Solve
\( n = \dfrac{6930}{154} = 45 \)
Step 4: Check
\( 154 \times 45 = 6930 \) ✓""", trick=r"Other number = (HCF × LCM) ÷ given number.")
S[49] = dict(raw=r"""Step 1: Write the numbers
Let the numbers be \( 2k \) and \( 3k \) (2 and 3 have no common factor).
Step 2: Their LCM
\( \text{LCM} = 2 \times 3 \times k = 6k \)
Step 3: Solve
\( 6k = 60 \Rightarrow k = 10 \)
Step 4: Numbers
\( 2 \times 10 = 20 \) and \( 3 \times 10 = 30 \); check: LCM of 20 and 30 is 60 ✓""", trick=r"LCM = product of ratio terms × k (when the terms are co-prime).")
S[50] = dict(raw=r"""Step 1: Take a value for B
Let \( B = 100 \). Then \( A = 6 \times 100 = 600 \).
Step 2: Difference
\( A - B = 600 - 100 = 500 \)
Step 3: Percentage less than A (base = A)
\( \dfrac{500}{600} \times 100\% \)
Step 4: Simplify
\( \dfrac{5}{6} \times 100\% = 83.33\% \)""", trick=r"'B less than A' → divide by A.")
S[51] = dict(raw=r"""Step 1: Profit
\( 1000 - 800 = ₹200 \)
Step 2: Formula
\( \text{Profit}\% = \dfrac{\text{Profit}}{\text{CP}} \times 100 \)
Step 3: Substitute
\( \dfrac{200}{800} \times 100 \)
Step 4: Simplify
\( \dfrac{1}{4} \times 100 = 25\% \)""", trick=r"Profit percent is always on the cost price.")
S[52] = dict(raw=r"""Step 1: Write the equation
\( \dfrac{1}{4} \times 70\% \text{ of } x = \dfrac{1}{5} \times 50\% \text{ of } y \Rightarrow 0.175x = 0.1y \)
Step 2: Relation
\( y = 1.75x \), so \( y > x \).
Step 3: Use the difference
\( y - x = 0.75x = 240 \Rightarrow x = 320,\; y = 1.75 \times 320 = 560 \)
Step 4: Required value
\( 150\% \text{ of } (320 + 560) = 1.5 \times 880 = 1320 \)""", trick=r"Ratio \( x : y = 4 : 7 \); difference 3 parts = 240 → 1 part = 80; sum 11 parts = 880.")
S[53] = dict(raw=r"""Step 1: Let the cost price be C
Profit at ₹2000 \( = 2000 - C \); loss at ₹1200 \( = C - 1200 \)
Step 2: Form the equation
\( 2000 - C = 19(C - 1200) \)
Step 3: Solve
\( 2000 - C = 19C - 22800 \Rightarrow 20C = 24800 \Rightarrow C = 1240 \)
Step 4: Profit percentage
\( \dfrac{2000 - 1240}{1240} \times 100 = \dfrac{760}{1240} \times 100 \approx 61.29\% \)""", trick=r"Divide the gap 2000 − 1200 = 800 in the ratio \( 19 : 1 \) → loss 40, so CP = 1240.")
S[54] = dict(raw=r"""Step 1: One-day work of each
A \( = \dfrac{1}{9} \), B \( = \dfrac{1}{12} \), C \( = \dfrac{1}{18} \)
Step 2: Add (LCM of 9, 12, 18 is 36)
\( \dfrac{4}{36} + \dfrac{3}{36} + \dfrac{2}{36} = \dfrac{9}{36} \)
Step 3: Simplify
\( \dfrac{9}{36} = \dfrac{1}{4} \) of the work per day
Step 4: Days together
\( 1 \div \dfrac{1}{4} = 4 \) days""", trick=r"Total work = 36 units; efficiencies 4 + 3 + 2 = 9 units/day → 36 ÷ 9 = 4.")
S[55] = dict(raw=r"""Step 1: Wages go in the ratio of work done
Working together for the same time, work done ∝ efficiency \( = \dfrac{1}{25} : \dfrac{1}{30} \)
Step 2: Simplify the ratio
\( \dfrac{1}{25} : \dfrac{1}{30} = 30 : 25 = 6 : 5 \)
Step 3: Shares
One part \( = \dfrac{6600}{6 + 5} = 600 \); A gets \( 6 \times 600 = ₹3600 \), B gets \( 5 \times 600 = ₹3000 \)
Step 4: Difference
\( 3600 - 3000 = ₹600 \)""", trick=r"Share ratio = inverse of days; difference = 1 part of 11 = ₹600.")
S[56] = dict(raw=r"""Step 1: Upstream formula
Upstream speed \( = \) boat speed \( - \) stream speed
Step 2: Substitute
\( 16 = 24 - s \)
Step 3: Solve
\( s = 24 - 16 \)
Step 4: Answer
\( s = 8 \) km/hr""", trick=r"Upstream = B − S, downstream = B + S.")
S[57] = dict(raw=r"""Step 1: Formula
\( \text{Time} = \dfrac{\text{Distance}}{\text{Speed}} \)
Step 2: Time for 540 km
\( \dfrac{540}{15} = 36 \) hours
Step 3: Time for 225 km
\( \dfrac{225}{15} = 15 \) hours
Step 4: Difference
\( 36 - 15 = 21 \) hours (or directly \( \dfrac{540 - 225}{15} = \dfrac{315}{15} = 21 \))""", trick=r"Same speed → time difference = distance difference ÷ speed.")
S[58] = dict(raw=r"""Step 1: Take CP = 100
\( \text{MP} = 100 + 80\% \text{ of } 100 = 180 \)
Step 2: Apply the discount
\( \text{SP} = 180 \times \dfrac{60}{100} = 108 \)
Step 3: Profit
\( 108 - 100 = 8 \)
Step 4: Profit percentage
\( \dfrac{8}{100} \times 100 = 8\% \)""", trick=r"1.8 × 0.6 = 1.08 → 8% profit.")
S[59] = dict(raw=r"""Step 1: Formula
\( \text{MP} = \dfrac{\text{SP}}{1 - \text{discount}} \)
Step 2: Test SP ₹3600 with 20% discount
\( \dfrac{3600}{0.8} = 4500 \) ✓
Step 3: Test the others
\( \dfrac{4200}{0.88} \approx 4773,\; \dfrac{3800}{0.86} \approx 4419,\; \dfrac{4100}{0.81} \approx 5062 \) — none is 4500.
Step 4: Answer
Only "SP ₹3600 and discount 20%" gives a marked price of ₹4500.""", trick=r"Quick check: 20% of 4500 = 900 and 4500 − 900 = 3600.")
S[60] = dict(raw=r"""Step 1: Take CP = 100
\( \text{MP} = 125 \)
Step 2: Selling price from the profit
\( \text{SP} = 100 + 18 = 118 \)
Step 3: Discount
\( 125 - 118 = 7 \)
Step 4: Discount percentage (on MP)
\( \dfrac{7}{125} \times 100 = 5.6\% \)""", trick=r"Discount % is always on the marked price: 7 ÷ 125 = 5.6%.")
