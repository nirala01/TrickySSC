S = {}
S[41] = dict(raw=r"""Step 1: Solve "of" and the bracket first (BODMAS)
\( 28 \text{ of } 2 = 28 \times 2 = 56 \) and \( (29) = 29 \).
Step 2: Do the division
\( 46 \div 2 = 23 \).
Step 3: Rewrite the expression
\( 77 - 33 + 56 + 23 - 17 + 29 \).
Step 4: Add and subtract from left to right
\( 77 - 33 = 44 \), \( 44 + 56 = 100 \), \( 100 + 23 = 123 \), \( 123 - 17 = 106 \), \( 106 + 29 = 135 \).""", trick=r"'of' means ×, and it comes before ÷, + and −.")
S[42] = dict(raw=r"""Step 1: Simplify the first fraction
\( \dfrac{0.08}{0.4} = \dfrac{8}{40} = 0.2 \).
Step 2: Simplify the second fraction
\( \dfrac{0.024}{0.6} = \dfrac{24}{600} = 0.04 \).
Step 3: Subtract
\( 0.2 - 0.04 = 0.16 \).
Step 4: Check
\( 0.16 + 0.04 = 0.2 \) ✓.""", trick=r"Clear the decimals: 0.08/0.4 = 8/40 and 0.024/0.6 = 24/600.")
S[43] = dict(raw=r"""Step 1: Spot the identity
\( (a + b)^{2} - 4ab = (a - b)^{2} \), with a = 7.75 and b = 2.75.
Step 2: Find a − b
\( 7.75 - 2.75 = 5 \).
Step 3: Square it
\( 5^{2} = 25 \).
Step 4: Check directly
\( (10.5)^{2} = 110.25 \) and \( 4 \times 7.75 \times 2.75 = 85.25 \); \( 110.25 - 85.25 = 25 \) ✓.""", trick=r"(a + b)² − 4ab = (a − b)², so the answer is (7.75 − 2.75)².")
S[44] = dict(raw=r"""Step 1: Write the number in terms of 210.25
\( 0.00021025 = 210.25 \times 10^{-6} \) (the decimal moves 6 places).
Step 2: Take the square root
\( \sqrt{0.00021025} = \sqrt{210.25} \times \sqrt{10^{-6}} = 14.5 \times 10^{-3} \).
Step 3: Simplify
\( 14.5 \times 10^{-3} = 0.0145 \).
Step 4: Check
\( 0.0145 \times 0.0145 = 0.00021025 \) ✓.""", trick=r"Decimal places in a square root are half of those in the number: 8 places → 4 places.")
S[45] = dict(raw=r"""Step 1: List the numbers between 20 and 40 that could be prime
Odd numbers not ending in 5: 21, 23, 27, 29, 31, 33, 37, 39.
Step 2: Remove the composites
\( 21 = 3 \times 7 \), \( 27 = 3 \times 9 \), \( 33 = 3 \times 11 \), \( 39 = 3 \times 13 \).
Step 3: Write the primes
23, 29, 31 and 37.
Step 4: Add them
\( 23 + 29 + 31 + 37 = 120 \).""", trick=r"Primes between 20 and 40: 23, 29, 31, 37.")
S[46] = dict(raw=r"""Step 1: Spot the identity
\( a^{3} + b^{3} + 3ab(a + b) = (a + b)^{3} \).
Step 2: Match the terms
a = 15, b = 5 and \( a + b = 20 \), so the expression is \( (15 + 5)^{3} \).
Step 3: Cube
\( 20^{3} = 8000 \).
Step 4: Check directly
\( 3375 + 125 + 4500 = 8000 \) ✓ (since \( 3 \times 15 \times 5 \times 20 = 4500 \)).""", trick=r"a³ + b³ + 3ab(a + b) is simply (a + b)³.")
S[47] = dict(raw=r"""Step 1: Write the perimeter formula
Perimeter of a rectangle \( = 2(l + b) \).
Step 2: Put in the value
\( 2(l + b) = 24 \).
Step 3: Find l + b
\( l + b = 24 \div 2 = 12 \) cm.
Step 4: Check with the length
\( b = 12 - 5 = 7 \) cm, and \( 2(5 + 7) = 24 \) ✓.""", trick=r"Length + breadth = half the perimeter.")
S[48] = dict(raw=r"""Step 1: Start with the innermost root
\( \sqrt{49} = 7 \).
Step 2: Solve the middle root
\( \sqrt{93 + 7} = \sqrt{100} = 10 \).
Step 3: Solve the outer root
\( \sqrt{1671 + 10} = \sqrt{1681} \).
Step 4: Find the value
\( 41 \times 41 = 1681 \), so x = 41.""", trick=r"Open nested roots from the inside out.")
S[49] = dict(raw=r"""Step 1: Recall the rule
A number is divisible by 6 only if it is divisible by both 2 and 3.
Step 2: Test for 2
84P6 ends in 6, so it is always even ✓.
Step 3: Test for 3
The digit sum \( 8 + 4 + P + 6 = 18 + P \) must be a multiple of 3, so P can be 0, 3, 6 or 9.
Step 4: Find the value that fails
For P = 7 the digit sum is 25, which is not a multiple of 3, so P cannot be 7.""", trick=r"Divisible by 6 = even + digit sum divisible by 3.")
S[50] = dict(raw=r"""Step 1: Find the original sum
Sum of 10 numbers \( = 10X \).
Step 2: Find the change
30 is replaced by 10, so the sum falls by \( 30 - 10 = 20 \). New sum \( = 10X - 20 \).
Step 3: Find the new average
\( \dfrac{10X - 20}{10} = X - 2 \).
Step 4: Answer
The new average is X − 2.""", trick=r"Change in average = change in sum ÷ count = −20 ÷ 10.")
S[51] = dict(raw=r"""Step 1: Use the rule for "same remainder"
The required number is the HCF of the differences between the numbers.
Step 2: Find the differences
\( 121 - 103 = 18 \), \( 139 - 121 = 18 \), \( 157 - 139 = 18 \).
Step 3: Find the HCF
HCF of 18, 18 and 18 \( = 18 \).
Step 4: Check
\( 103 = 5 \times 18 + 13 \), \( 121 = 6 \times 18 + 13 \), \( 139 = 7 \times 18 + 13 \), \( 157 = 8 \times 18 + 13 \) — remainder 13 each time ✓.""", trick=r"Same remainder → HCF of the differences.")
S[52] = dict(raw=r"""Step 1: Take the cost price as 100
CP = 100 and a 10% loss gives SP = 90.
Step 2: Increase both by 20%
New CP \( = 100 \times 1.2 = 120 \) and new SP \( = 90 \times 1.2 = 108 \).
Step 3: Find the new loss
\( 120 - 108 = 12 \).
Step 4: Find the loss percentage
\( \dfrac{12}{120} \times 100 = 10\% \).""", trick=r"Raising CP and SP by the same percentage leaves the profit/loss % unchanged.")
S[53] = dict(raw=r"""Step 1: Take B as 100
A is 20% less than B, so A = 80.
Step 2: Find the difference
\( B - A = 100 - 80 = 20 \).
Step 3: Compare with A
B is more than A by \( \dfrac{20}{80} \times 100 \).
Step 4: Calculate
\( \dfrac{20}{80} \times 100 = 25\% \).""", trick=r"x% less → \( \dfrac{x}{100 - x} \times 100 \)% more: \( \dfrac{20}{80} \) = 25%.")
S[54] = dict(raw=r"""Step 1: Find the cost price
CP = SP + loss \( = 3500 + 500 = 4000 \), i.e. ₹4000.
Step 2: Write the formula
Loss % \( = \dfrac{\text{Loss}}{\text{CP}} \times 100 \).
Step 3: Put in the values
\( \dfrac{500}{4000} \times 100 \).
Step 4: Calculate
\( = 12.5\% \).""", trick=r"Loss % is always on CP, not on SP: 500 ÷ 4000.")
S[55] = dict(raw=r"""Step 1: Take the salary as 100
After a 25% increase it becomes \( 100 \times 1.25 = 125 \).
Step 2: Apply the 40% decrease
\( 125 \times 0.6 = 75 \).
Step 3: Find the net change
\( 75 - 100 = -25 \).
Step 4: Answer
The salary decreases by 25%. (Formula check: \( 25 - 40 - \dfrac{25 \times 40}{100} = -25 \).)""", trick=r"Net % change = a + b + ab/100 with b = −40.")
S[56] = dict(raw=r"""Step 1: Find one day's work
R does \( \dfrac{1}{24} \) and S does \( \dfrac{1}{36} \) of the work in a day.
Step 2: Add them
\( \dfrac{1}{24} + \dfrac{1}{36} = \dfrac{3 + 2}{72} = \dfrac{5}{72} \) per day.
Step 3: Work done in 8 days
\( 8 \times \dfrac{5}{72} = \dfrac{40}{72} = \dfrac{5}{9} \).
Step 4: Work left
\( 1 - \dfrac{5}{9} = \dfrac{4}{9} \).""", trick=r"LCM method: total work 72 units, both together 5 units/day, 8 days → 40 units, 32 left = \( \dfrac{4}{9} \).")
S[57] = dict(raw=r"""Step 1: Write the work equation
\( M_{1} \times D_{1} \times H_{1} = M_{2} \times D_{2} \times H_{2} \).
Step 2: Put in the values
\( 30 \times 40 \times 9 = M_{2} \times 60 \times 6 \).
Step 3: Simplify
\( 10800 = 360 \times M_{2} \).
Step 4: Solve
\( M_{2} = 10800 \div 360 = 30 \) men.""", trick=r"Men × days × hours stays the same: 40 × 9 = 60 × 6, so the men stay 30.")
S[58] = dict(raw=r"""Step 1: Recall the relation
For the same distance, time is inversely proportional to speed.
Step 2: Write the speed ratio
Speed of A to speed of B \( = 10 : 20 = 1 : 2 \).
Step 3: Invert it for time
Time of A to time of B \( = 2 : 1 \).
Step 4: Check with a distance of 20 km
A takes 2 hours and B takes 1 hour, so the ratio is \( 2 : 1 \) ✓.""", trick=r"Same distance: time ratio = speed ratio turned upside down.")
S[59] = dict(raw=r"""Step 1: Relate the new speed and time
At 60% (\( \dfrac{3}{5} \)) of the usual speed, the time becomes \( \dfrac{5}{3} \) of the usual time.
Step 2: Find the extra time as a fraction
Extra time \( = \dfrac{5}{3}T - T = \dfrac{2}{3}T \).
Step 3: Equate to the delay
\( \dfrac{2}{3}T = 18 \).
Step 4: Solve
\( T = 18 \times \dfrac{3}{2} = 27 \) minutes.""", trick=r"Speed × 3/5 → time × 5/3; the extra 2/3 of T is 18 minutes.")
S[60] = dict(raw=r"""Step 1: Find the cost price
CP \( = X - 40\% \text{ of } X = 0.6X \).
Step 2: Find the selling price
SP \( = X + 10\% \text{ of } X = 1.1X \).
Step 3: Find the profit
Profit \( = 1.1X - 0.6X = 0.5X \).
Step 4: Find the profit percentage
\( \dfrac{0.5X}{0.6X} \times 100 = \dfrac{5}{6} \times 100 = 83.33\% \).""", trick=r"Take X = 100: CP 60, SP 110, profit 50 on 60.")
