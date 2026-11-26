S = {}
S[41] = dict(raw=r"""Step 1: Bracket first
\( 39 + 16 = 55 \)
Step 2: Multiplication next
\( 55 \times 2 = 110 \)
Step 3: Add and subtract from left to right
\( 65 + 83 - 44 + 110 - 88 = 148 - 44 + 110 - 88 = 104 + 110 - 88 \)
Step 4: Final value
\( 214 - 88 = 126 \)""", trick=r"BODMAS: bracket → × → + and − from left to right.")
S[42] = dict(raw=r"""Step 1: Solve "of" and the bracket
\( (24 \text{ of } 1) = 24 \times 1 = 24 \)
Step 2: Division next
\( 66 \div 6 = 11 \)
Step 3: Rewrite the expression
\( 53 + 45 - 18 + 11 - 24 + 37 \)
Step 4: Add and subtract from left to right
\( 98 - 18 = 80,\; 80 + 11 = 91,\; 91 - 24 = 67,\; 67 + 37 = 104 \)""", trick=r"'of' means multiply; do it with the bracket before ÷.")
S[43] = dict(raw=r"""Step 1: Line up the decimal points
\( 420.00000 + 42.00500 + 4.20050 + 0.42005 \)
Step 2: Add the first two
\( 420 + 42.005 = 462.005 \)
Step 3: Add the next one
\( 462.005 + 4.2005 = 466.2055 \)
Step 4: Add the last one
\( 466.2055 + 0.42005 = 466.62555 \)""", trick=r"Pad with zeros so every number has 5 decimal places, then add.")
S[44] = dict(raw=r"""Step 1: Spot the identity
\( (a - b)^{3} = a^{3} - 3a^{2}b + 3ab^{2} - b^{3} \)
Step 2: Match the terms
\( (2.5)^{2} \times 2.5 = (2.5)^{3} \), so \( a = 2.5 \) and \( b = 0.5 \); the middle terms are \( 3a^{2}b \) and \( 3ab^{2} \).
Step 3: Apply the identity
Value \( = (2.5 - 0.5)^{3} = 2^{3} \)
Step 4: Final value
\( 2^{3} = 8 \), i.e. 8.0""", trick=r"a³ − 3a²b + 3ab² − b³ = (a − b)³.")
S[45] = dict(raw=r"""Step 1: Formula for the first n natural numbers
\( 1 + 2 + 3 + ... + n = \dfrac{n(n + 1)}{2} \)
Step 2: Put n = 30
\( \dfrac{30 \times 31}{2} \)
Step 3: Simplify
\( 15 \times 31 = 465 \)
Step 4: Check by pairing
Pairs \( 1 + 30,\; 2 + 29, \) and so on, each make 31; there are 15 pairs, \( 15 \times 31 = 465 \) ✓""", trick=r"Sum 1 to n = n(n + 1) ÷ 2.")
S[46] = dict(raw=r"""Step 1: Find the side
\( \text{Side} = \dfrac{52}{4} = 13 \) cm
Step 2: Use the right triangle formed by the diagonals
The diagonals of a rhombus bisect each other at 90°, so half-diagonals and the side form a right triangle. Half of 24 is 12.
Step 3: Pythagoras
\( \text{Other half} = \sqrt{13^{2} - 12^{2}} = \sqrt{169 - 144} = \sqrt{25} = 5 \)
Step 4: Other diagonal
\( 2 \times 5 = 10 \) cm""", trick=r"Rhombus: side² = (d₁/2)² + (d₂/2)² — here 5, 12, 13.")
S[47] = dict(raw=r"""Step 1: Relation between side and diagonals
\( d_{1}^{2} + d_{2}^{2} = 4 \times \text{side}^{2} = 4 \times 17^{2} = 1156 \)
Step 2: Use the sum of the diagonals
\( (d_{1} + d_{2})^{2} = 46^{2} = 2116 \)
Step 3: Find the product
\( 2d_{1}d_{2} = 2116 - 1156 = 960 \Rightarrow d_{1}d_{2} = 480 \)
Step 4: Area
\( \text{Area} = \dfrac{d_{1}d_{2}}{2} = \dfrac{480}{2} = 240 \) sq cm (the diagonals are 30 cm and 16 cm).""", trick=r"(d₁ + d₂)² − (d₁² + d₂²) = 2d₁d₂; area = d₁d₂ ÷ 2.")
S[48] = dict(raw=r"""Step 1: Write each fraction in its lowest terms
\( \dfrac{3}{4},\; \dfrac{6}{8} = \dfrac{3}{4},\; \dfrac{9}{10} \)
Step 2: Formula
\( \text{LCM of fractions} = \dfrac{\text{LCM of numerators}}{\text{HCF of denominators}} \)
Step 3: Apply it
\( \text{LCM}(3, 3, 9) = 9 \) and \( \text{HCF}(4, 4, 10) = 2 \), so the LCM \( = \dfrac{9}{2} \).
Step 4: Check
\( \dfrac{9}{2} \div \dfrac{3}{4} = 6 \) and \( \dfrac{9}{2} \div \dfrac{9}{10} = 5 \) — both whole numbers ✓ (using \( \dfrac{6}{8} \) unreduced gives \( \dfrac{18}{2} = 9 \), a common multiple but not the least).""", trick=r"Reduce first, then LCM of tops ÷ HCF of bottoms.")
S[49] = dict(raw=r"""Step 1: Key property
For two numbers, \( \text{HCF} \times \text{LCM} = \text{product of the numbers} \)
Step 2: Put the values
\( 18 \times 540 \)
Step 3: Multiply
\( 18 \times 540 = 9720 \)
Step 4: Check with an example
The numbers could be 54 and 180 (HCF 18, LCM 540): \( 54 \times 180 = 9720 \) ✓""", trick=r"Product of two numbers = HCF × LCM.")
S[50] = dict(raw=r"""Step 1: Formula
\( \text{SP} = \text{CP} \times \dfrac{100 - \text{Loss}\%}{100} \)
Step 2: Put the values
\( \text{SP} = 4800 \times \dfrac{60}{100} \)
Step 3: Simplify
\( 48 \times 60 = 2880 \)
Step 4: Check
Loss \( = 4800 - 2880 = 1920 \), and \( \dfrac{1920}{4800} \times 100 = 40\% \) ✓ — SP is ₹2880.""", trick=r"40% loss → SP = 60% of CP.")
S[51] = dict(raw=r"""Step 1: Share of good eggs
\( 100\% - 30\% = 70\% \) are not rotten.
Step 2: Set up
\( 70\% \text{ of } 420 = \dfrac{70}{100} \times 420 \)
Step 3: Simplify
\( 7 \times 42 = 294 \)
Step 4: Check
Rotten eggs \( = 30\% \text{ of } 420 = 126 \), and \( 126 + 294 = 420 \) ✓""", trick=r"Find the remaining percentage directly: 70% of 420.")
S[52] = dict(raw=r"""Step 1: Take the ratio as values
\( \text{SP} : \text{CP} = 5 : 4 \), so let SP = 5 units and CP = 4 units.
Step 2: Profit
\( 5 - 4 = 1 \) unit
Step 3: Profit percentage on CP
\( \dfrac{1}{4} \times 100 = 25\% \)
Step 4: Check
\( 4 \times 1.25 = 5 \) ✓""", trick=r"Profit% = (SP − CP) ÷ CP × 100 with the ratio values.")
S[53] = dict(raw=r"""Step 1: Write the equation
\( \dfrac{1}{4} \times \dfrac{80}{100} \times a = \dfrac{3}{5} \times \dfrac{30}{100} \times b \Rightarrow 0.2a = 0.18b \)
Step 2: Ratio of the numbers
\( \dfrac{a}{b} = \dfrac{0.18}{0.2} = \dfrac{9}{10} \), so a = 9k and b = 10k.
Step 3: Use the difference
\( 10k - 9k = 400 \Rightarrow k = 400 \), so a = 3600 and b = 4000.
Step 4: 25% of the sum
\( \dfrac{25}{100} \times (3600 + 4000) = \dfrac{7600}{4} = 1900 \)""", trick=r"Convert both sides to decimals: 0.2a = 0.18b → ratio 9 to 10.")
S[54] = dict(raw=r"""Step 1: Wages are shared in the ratio of work done
Working together for the same time, each person's share equals his one-day work.
Step 2: One-day work
\( \dfrac{1}{18} : \dfrac{1}{24} : \dfrac{1}{36} \); multiplying by 72 gives \( 4 : 3 : 2 \) for R, P and G.
Step 3: P's share
\( \dfrac{3}{4 + 3 + 2} \times 7200 = \dfrac{3}{9} \times 7200 \)
Step 4: Simplify
\( \dfrac{7200}{3} = 2400 \), i.e. ₹2400.""", trick=r"Same working time → share ∝ 1 ÷ (days taken).")
S[55] = dict(raw=r"""Step 1: Total hours each needs
R: \( 12 \times 4 = 48 \) hours; S: \( 6 \times 8 = 48 \) hours.
Step 2: Work per hour together
\( \dfrac{1}{48} + \dfrac{1}{48} = \dfrac{2}{48} = \dfrac{1}{24} \)
Step 3: Total hours needed together
They need 24 working hours in all.
Step 4: Hours per day for 4 days
\( \dfrac{24}{4} = 6 \) hours a day""", trick=r"Convert to hours first: 48 h each → together 24 h → 6 h/day over 4 days.")
S[56] = dict(raw=r"""Step 1: Conversion factor
\( 1 \text{ m/s} = \dfrac{18}{5} \text{ km/hr} \) (because \( \dfrac{3600}{1000} = \dfrac{18}{5} \))
Step 2: Multiply
\( 50 \times \dfrac{18}{5} \)
Step 3: Simplify
\( 10 \times 18 = 180 \) km/hr
Step 4: Check
180 km/hr \( = \dfrac{180000}{3600} = 50 \) m/s ✓""", trick=r"m/s → km/hr: multiply by 18/5.")
S[57] = dict(raw=r"""Step 1: Formula for equal distances
\( \text{Average speed} = \dfrac{\text{Total distance}}{\text{Total time}} \); take each distance as d.
Step 2: Total time
\( \dfrac{d}{10} + \dfrac{d}{30} + \dfrac{d}{60} = \dfrac{6d + 2d + d}{60} = \dfrac{9d}{60} \)
Step 3: Average speed
\( \dfrac{3d}{\left(\dfrac{9d}{60}\right)} = \dfrac{180}{9} = 20 \) km/hr
Step 4: Check with d = 60 km
Times 6 h, 2 h and 1 h: \( \dfrac{180}{9} = 20 \) ✓""", trick=r"Never average the speeds directly; use total distance ÷ total time.")
S[58] = dict(raw=r"""Step 1: Take CP = 100
MP \( = 450\% \text{ of } 100 = 450 \)
Step 2: Find SP
CP is 25% of SP, so \( \text{SP} = 4 \times 100 = 400 \)
Step 3: Discount
\( 450 - 400 = 50 \)
Step 4: Discount percentage on MP
\( \dfrac{50}{450} \times 100 = 11.11\% \)""", trick=r"Discount % is always on the marked price.")
S[59] = dict(raw=r"""Step 1: Effect of the two discounts
After 20% off, 80% is paid; after a further 25% off, 75% of that is paid.
Step 2: Combined multiplier
\( 0.8 \times 0.75 = 0.6 \), so SP is 60% of MP.
Step 3: Find MP
\( \text{MP} = \dfrac{18000}{0.6} = 30000 \)
Step 4: Check
\( 30000 \times 0.8 = 24000,\; 24000 \times 0.75 = 18000 \) ✓ — MP is ₹30000.""", trick=r"20% and 25% successive = 40% single discount.")
S[60] = dict(raw=r"""Step 1: First discount
\( 4000 \times \dfrac{75}{100} = 3000 \)
Step 2: Second discount amount
\( 3000 - 2400 = 600 \)
Step 3: Second discount percentage
\( A = \dfrac{600}{3000} \times 100 = 20 \)
Step 4: Check
\( 4000 \times 0.75 \times 0.8 = 2400 \) ✓""", trick=r"The second discount is on the price after the first discount.")
