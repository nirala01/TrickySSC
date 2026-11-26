from base import opt_bullets as ob, Q_EN
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “Vertically challenged” is a humorous, polite way of saying that a person is short.
-> The army has a minimum height requirement, so a short candidate is not selected.""",
{"horizontally challenged": "a joking way of saying “fat”, which does not fit a height test.",
 "vertically challenged": "correct — short in height.",
 "diagonally challenged": "not a real expression.",
 "obliquely challenged": "not a real expression."},
r"Vertically challenged = short.")
L(62, r"""-> A “vicious circle” is a chain of events in which each result causes the next one, so it repeats without end.
-> The endless cycle of birth and rebirth fits this idea.""",
{"vicious circle": "correct — an endless repeating cycle.",
 "viscous circle": "a misspelling trap — “viscous” means thick and sticky (like honey).",
 "abacus circle": "an abacus is a counting frame; this is not an expression.",
 "truant circle": "a truant is a student who stays away from school; not an expression."},
r"Vicious circle = endless cycle (not viscous = sticky).")
L(63, r"""-> “Amusement” means the feeling of enjoying something funny or the activity that gives pleasure.
-> Example: The park has many rides for amusement.""",
{"Boredom": "the opposite feeling.",
 "Entertainment": "correct — something that amuses and gives enjoyment.",
 "Anger": "a strong feeling of annoyance — unrelated.",
 "Confusion": "not knowing what to do — unrelated."},
r"Amusement ≈ entertainment ≈ fun.")
L(64, r"""-> “Hazardous” means risky or dangerous.
-> Example: Hazardous waste must be disposed of carefully.""",
{"Dangerous": "correct — the same meaning as hazardous.",
 "Safe": "the opposite of hazardous.",
 "Helpful": "useful — not related to danger.",
 "Easy": "not difficult — unrelated."},
r"Hazard = danger.")
L(65, r"""-> The correct spelling is “wainscoting” — wooden panelling on the lower part of a wall.
-> The /sk/ sound is spelt “sc” here, which is why “sk” is a common mistake.""",
{"Wainskoting": "misspelt — the correct form is “wainscoting”.",
 "Wholesome": "spelt correctly — good for health.",
 "Windbreaker": "spelt correctly — a light jacket that keeps out the wind.",
 "Wordsmith": "spelt correctly — a skilled user of words."},
r"wainSCoting — sc, not sk.")
L(66, r"""-> “Difference” means a way in which things are not the same.
-> Its antonym should mean being alike or identical.""",
{"Gap": "close in meaning to difference (a gap between two things).",
 "Sameness": "correct — the quality of being the same, the opposite of difference.",
 "Conceal": "a verb meaning to hide — unrelated.",
 "conflict": "a disagreement — related to difference, not opposite."},
r"Difference ↔ sameness / similarity.")
L(67, r"""-> A “spoiler” is information that reveals important plot details of a film, show or book before someone has seen it.
-> It “spoils” the surprise.""",
{"Teaser": "a short advertisement that creates interest without giving the plot away.",
 "spoiler": "correct — reveals crucial plot details.",
 "climax": "the most exciting point of the story itself, not revealing it.",
 "Twister": "a tornado, or a tricky puzzle — unrelated."},
r"Reveals the ending = spoiler.")
L(68, r"""-> “Uxorious” (from Latin “uxor”, wife) means having or showing great or excessive fondness for one's wife.
-> Example: He was an uxorious husband who never left his wife's side.""",
{"Uxorious": "correct — very fond of one's wife.",
 "Delirious": "confused and restless, often because of fever.",
 "Apathetic": "showing no interest or feeling.",
 "Feisty": "lively, determined and ready to argue."},
r"Uxor = wife → uxorious.")
L(69, r"""-> “Take something or someone for granted” is a fixed phrase meaning to fail to value it because it is always there.
-> So the blank needs the preposition “for”.""",
{"in": "“take in granted” is not used.",
 "by": "“take by granted” is not used.",
 "for": "correct — take (someone) for granted.",
 "about": "“take about granted” is not used."},
r"Take for granted — always “for”.")
L(70, r"""-> The sentence is a question in the past continuous tense: Were + subject + verb-ing.
-> Passive of past continuous: was/were + being + past participle; the plural object “experiments” takes “were”.""",
{"Was experiments being conducted by the students in the lab this morning?": "wrong — plural “experiments” needs “were”, not “was”.",
 "Were experiments being conducted by the students in the lab this morning?": "correct — were + being + conducted keeps the past continuous.",
 "Are experiments being conducted by the students in the lab this morning?": "wrong — changes the tense to present continuous.",
 "Were experiments conducted by the students in the lab this morning?": "wrong — drops “being”, so it becomes simple past."},
r"Past continuous passive = was/were + being + V3.")
L(71, r"""-> “is being prepared” is present continuous passive.
-> In the active voice the doer (“the scientists at the institute”) becomes the subject and the tense stays present continuous: are preparing.""",
{"The scientists at the institute prepare an elaborate report on climate change for the upcoming conference.": "wrong — simple present tense.",
 "The scientists at the institute are preparing an elaborate report on climate change for the upcoming conference.": "correct — present continuous, as in the passive sentence.",
 "The scientists at the institute have prepared an elaborate report on climate change for the upcoming conference.": "wrong — present perfect tense.",
 "The scientists at the institute will prepare an elaborate report on climate change for the upcoming conference.": "wrong — simple future tense."},
r"is/are being + V3 → is/are + V-ing.")
L(72, r"""-> The noun “interest” is followed by the preposition “in” when it means liking or curiosity.
-> Example: She has a keen interest in painting.""",
{"at": "not used after “interest”.",
 "for": "not the standard preposition for “interest” meaning liking.",
 "in": "correct — interest in music.",
 "on": "“interest on” is used for money (interest on a loan), not for a liking."},
r"Interest in (a subject); interest on (a loan).")
L(73, r"""-> “The higher …, the less …” is a parallel (proportional) comparison: both parts use the comparative degree.
-> With an uncountable noun like oxygen the comparative is “less”; “lesser” is used before a noun only in the sense of “smaller in importance”.""",
{"the less oxygen is available": "correct — comparative “less” matches “the higher”.",
 "the least oxygen is available": "wrong — superlative breaks the “the + comparative” pattern.",
 "the oxygen available is lesser": "wrong — “lesser” is not used for quantity, and the word order breaks the pattern.",
 "No improvement required": "wrong — “the lesser oxygen” is incorrect here."},
r"The more …, the less … (comparative + comparative).")
L(74, r"""-> S1 introduces an old man walking on a hot afternoon; C (“He was tired and thirsty”) describes him, so it follows S1.
-> D tells us he spotted a grocery store, B describes the store (“It had a tin roof …”), and A describes the shopkeeper inside; S2 then mentions the bench in front of the store.""",
{"ACDB": "wrong — A talks about “the shopkeeper” before any shop is mentioned.",
 "BADC": "wrong — “It” in B has nothing to refer to right after S1.",
 "CDBA": "correct — the man (C), the shop (D), its look (B), the shopkeeper (A).",
 "DBAC": "wrong — “He was tired and thirsty” cannot come after the shopkeeper sentence."},
r"Person → place → description → person inside.")
L(75, r"""-> The sentence mixes two pronouns: it starts with “one” and ends with “you”.
-> Pronouns must be consistent, so “If you are honest, people will respect you.” A real condition about the present takes the simple present (are), not “were”.""",
{"If one were honest": "wrong — keeps the clash of “one” with “you” and uses the unreal “were”.",
 "If you are honest": "correct — “you … you” is consistent and the tense fits.",
 "If you were honest": "wrong — “were” needs “would respect”, not “will respect”.",
 "No improvement required": "wrong — “one … you” is a pronoun shift."},
r"One … one / you … you — never mix.")
L(76, r"""-> “A nation with a rich legacy” — “with” shows that the nation has or possesses the legacy.
-> Example: a man with great courage.""",
{"with": "correct — “a nation with a rich … legacy”.",
 "in": "“a nation in a rich legacy” makes no sense.",
 "of": "“a nation of a rich legacy” is not idiomatic.",
 "by": "“by” shows the doer or a means — it does not fit."},
r"Having a quality → “with”.")
L(77, r"""-> The subject “the highest-ranking awards” is plural, and the passage is in the simple present.
-> A plural subject in the simple present takes the base form: “the awards hold special significance”.""",
{"holds": "wrong — singular verb with a plural subject.",
 "holding": "wrong — a participle cannot be the main verb of the clause.",
 "hold": "correct — plural subject + base verb.",
 "holed": "a different verb (to make a hole), and in the past tense."},
r"Plural subject → verb without -s.")
L(78, r"""-> “Gallantry” means courage and bravery, especially in battle.
-> The Param Vir Chakra is India's highest award for gallantry in war.""",
{"Intelligence in planning": "describes strategy or cleverness, not gallantry.",
 "Discipline and obedience": "qualities of a good soldier, but not the meaning of gallantry.",
 "Loyalty to the nation": "means patriotism, not gallantry.",
 "Courage and heroic bravery": "correct — gallantry is heroic courage."},
r"Gallantry = bravery (gallantry awards: PVC, Ashoka Chakra).")
L(79, r"""-> “Conspicuous” means clearly visible or attracting attention.
-> “Conspicuous bravery” is bravery that stands out clearly.""",
{"Noticeable": "correct — easy to see or notice.",
 "Hidden": "the opposite of conspicuous.",
 "Insignificant": "too small to matter — opposite in sense.",
 "Ordinary": "not special — opposite in sense."},
r"Conspicuous = noticeable, eye-catching.")
L(80, r"""-> “Not only … but also …” joins two parallel verbs with the same subject (“these awards”).
-> The first verb is “celebrate” (plural, present), so the second must be the same form: “but also inspire generations”.""",
{"inspires": "wrong — singular form with the plural subject “these awards”.",
 "inspired": "wrong — past tense breaks the parallel with “celebrate”.",
 "inspiring": "wrong — a participle is not parallel to “celebrate”.",
 "inspire": "correct — parallel with “celebrate”."},
r"Not only celebrate … but also inspire (same form).")
