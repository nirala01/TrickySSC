from base import opt_bullets as ob, Q_EN
S = {}
def L(n, ctx, opt, trick):
    # keys may be the full option text or a unique prefix of it
    texts = [Q_EN[n][x] for x in "ABCD"]
    full = {}
    for k, v in opt.items():
        hits = [t for t in texts if t == k] or [t for t in texts if t.startswith(k)]
        assert len(hits) == 1, (n, k, hits)
        full[hits[0]] = v
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, full), trick=trick)

L(61, r"""-> The meaning describes losing something valuable by mistake while getting rid of something useless.
-> The idiom for this is "throw the baby out with the bathwater" — like emptying a tub and carelessly throwing the baby away with the dirty water.
-> Example: "Scrapping the whole plan because of one weak point would be throwing the baby out with the bathwater." """,
{"Throw somebody for a loop": "wrong — means to confuse or shock someone.",
 "Throw the baby out": "correct — an avoidable mistake of discarding the good along with the bad.",
 "Throw the first stone": "wrong — means to be the first to criticise or attack someone.",
 "Lock someone up": "wrong — means to imprison someone for a very long time, for ever."},
r"Bad bathwater out, baby (the good part) lost with it.")
L(62, r"""-> In accounts, debts and losses were traditionally written in red ink, so "in the red" means owing money or making a loss.
-> "Out of the red" therefore means no longer in debt — back to having no money owed, especially of a company.
-> Example: "After two good years the company is finally out of the red." """,
{"Go into the red": "wrong — the opposite; to start owing money or making a loss.",
 "Red in the face": "wrong — means embarrassed or very angry.",
 "Out of the red": "correct — no longer in debt.",
 "Take the red eye": "wrong — means to take a late-night flight."},
r"In the red = in debt; out of the red = debt-free.")
L(63, r"""-> Only one of the four words is spelt correctly.
-> "Juvenile" (young; meant for young people) is the correct spelling.
-> The other three drop or change letters of jettison, jaundice and jocular.""",
{"Jetison": "misspelt — the correct spelling is “jettison” (double t).",
 "Juvenile": "correct — spelt correctly; means young or youthful.",
 "Jondice": "misspelt — the correct spelling is “jaundice”.",
 "Jokular": "misspelt — the correct spelling is “jocular” (with c)."},
r"Juve-nile: j-u-v-e-n-i-l-e.")
L(64, r"""-> "Liberty" means the state of being free, especially from control, prison or slavery.
-> Its synonym is "freedom".
-> Captivity, punishment and arrest all take freedom away, so they are opposite in sense.""",
{"Captivity": "wrong — an antonym; the state of being kept as a prisoner.",
 "Punishment": "wrong — a penalty for wrongdoing, not liberty.",
 "Freedom": "correct — the state of being free, the same as liberty.",
 "Arrest": "wrong — taking someone into custody; opposite in sense."},
r"Liberty = freedom.")
L(65, r"""-> Three of the four words are spelt correctly; one is misspelt.
-> The correct spelling is "acknowledge" — it keeps the "d" before "ge" (acknow-LEDGE, like "knowledge").
-> "Acknowlege" drops the "d", so it is the misspelt word.""",
{"Acknowlege": "misspelt — the correct spelling is “acknowledge”.",
 "Bureaucracy": "spelt correctly — government by officials.",
 "Recommend": "spelt correctly — one c, double m.",
 "Dilemma": "spelt correctly — a difficult choice; double m."},
r"Acknowledge = ac + knowledge.")
L(66, r"""-> "Occupied" means being used or filled, or (of a person) busy.
-> Its antonym is "vacant", which means empty or not being used, as in a vacant seat.
-> Taken, engaged and busy are all close in meaning to occupied.""",
{"Vacant": "correct — empty or unused, the opposite of occupied.",
 "Taken": "wrong — a synonym; already in use.",
 "Engaged": "wrong — a synonym; in use (a phone line) or busy.",
 "Busy": "wrong — a synonym when used of a person."},
r"Occupied ↔ vacant.")
L(67, r"""-> The phrase describes a person who quickly notices, understands and responds to what is happening.
-> The best word is "perceptive" — having quick insight and understanding.
-> Example: "A perceptive teacher notices at once when a student is confused." """,
{"Perceptive": "correct — quick to notice and understand.",
 "Pliable": "wrong — easily bent or easily influenced.",
 "obtuse": "wrong — slow to understand; the opposite.",
 "Effusive": "wrong — showing feelings in an unrestrained, gushing way."},
r"Perceive (notice) → perceptive.")
L(68, r"""-> The phrase describes a large, confused and turbulent mass or whirl.
-> "Maelstrom" originally means a powerful whirlpool, and is used for a situation or crowd in violent, confused movement.
-> Example: "He was lost in the maelstrom of people at the railway station." """,
{"Convocation": "wrong — a formal assembly, such as a degree ceremony; orderly, not confused.",
 "Maelstrom": "correct — a confused, turbulent mass or situation.",
 "Vicissitude": "wrong — a change of circumstances, usually unwelcome.",
 "Machination": "wrong — a secret plot or scheme."},
r"Maelstrom = whirlpool → confused, swirling mass.")
L(69, r"""-> The sentence tells us what to use to cover the face — the palms are the instrument.
-> The preposition "with" shows the instrument used to do something: cover your face with your palms.
-> Example: "She covered the dish with a lid." """,
{"behind": "wrong — shows position at the back of something.",
 "under": "wrong — shows position below something.",
 "with": "correct — shows the instrument used (the palms).",
 "in": "wrong — “cover your face in your palms” is not idiomatic; “bury your face in your hands” is a different expression."},
r"Cover something WITH the thing you use.")
L(70, r"""-> The active sentence is an interrogative in the simple past: Did + subject + V1 + object?
-> In the passive, simple past becomes was/were + V3: Was + object + repaired + by + subject?
-> The object "the machinery" becomes the subject, and the time clause "before the factory resumed operations" stays unchanged.""",
{"Was the machinery repaired": "correct — simple past passive (was + V3).",
 "Was the machinery being repaired": "wrong — past continuous passive; the active is not continuous.",
 "Has the machinery been repaired": "wrong — present perfect passive; changes the tense.",
 "Did the machinery repair": "wrong — keeps “did” with V1, which is not a passive form."},
r"Did + V1 → Was/Were + V3.")
L(71, r"""-> The passive sentence is in the past continuous: was + being + V3 (was being evaluated).
-> In the active, past continuous is was/were + V-ing: Was + subject + evaluating + object?
-> The agent "the panel" becomes the subject, and "the project presentation" becomes the object.""",
{"Did the panel evaluate": "wrong — simple past; the original is continuous.",
 "Is the panel evaluating": "wrong — present continuous; changes the tense.",
 "Was the panel evaluating": "correct — past continuous active.",
 "Had the panel evaluated": "wrong — past perfect; changes the tense."},
r"was being + V3 → was + V-ing.")
L(72, r"""-> "Is known to" is the passive of the simple present verb "know"; the agent is introduced with "to" instead of "by".
-> In the active, the agent "everybody in the class" becomes the subject and the tense stays simple present: Everybody in the class knows the solution.
-> "Know" is a stative verb, so it is not normally used in the continuous form.""",
{"Everybody in the class is knowing": "wrong — continuous form of a stative verb, and a change of tense.",
 "Everybody in the class knew": "wrong — simple past; changes the tense.",
 "Everybody in the class knows": "correct — simple present active.",
 "Everybody in the class has known": "wrong — present perfect; changes the tense."},
r"is known to X → X knows.")
L(73, r"""-> In the pattern "It is/was + adjective + of + person + to-infinitive", the adjective describes the person's behaviour.
-> With adjectives like stupid, kind, foolish, wise and careless, we use "of", not "about": It was very stupid of the boy to have spent …
-> So the error is in the part "stupid about the boy to".""",
{"It was very": "no error — correct opening.",
 "stupid about the boy to": "error — “about” should be “of” (stupid of the boy).",
 "have spent five thousand": "no error — perfect infinitive for a past action.",
 "rupees on that dictionary.": "no error — “spend money on something” is correct."},
r"Kind/stupid/wise OF someone to do something.")
L(74, r"""-> The verb "boast" (to talk with too much pride) is followed by "of" or "about".
-> "Boasts of his European descent" is the standard prepositional use.
-> Example: "He boasts of his wealth." """,
{"with": "wrong — “boast with” is not used.",
 "of": "correct — boast of something.",
 "at": "wrong — “boast at” is not used.",
 "for": "wrong — “boast for” is not used."},
r"Boast OF (or about) something.")
L(75, r"""-> "Come to terms with something" is a fixed phrase meaning to accept a sad or difficult situation.
-> The underlined part "come to terms with the fact" is already correct and fits the sentence.
-> Changing the prepositions breaks the fixed phrase.""",
{"come at terms of the fact": "wrong — the phrase is “to terms with”, not “at terms of”.",
 "come on terms with the facts": "wrong — “on terms” is wrong, and “facts” does not agree with “the fact that”.",
 "come in terms to the fact": "wrong — “in terms to” is not a phrase.",
 "No improvement required": "correct — “come to terms with the fact” is already right."},
r"Come TO terms WITH = accept.")
L(76, r"""-> The passage says giving food or shelter gives only temporary relief.
-> It explains why: "as long as human nature remains the same, physical needs and suffering will persist" — new suffering keeps arising.
-> So material help is inadequate because human nature ensures that new suffering will emerge.""",
{"Physical needs are transient": "wrong — the passage says needs will continue, not that they are easily satisfied.",
 "Because human nature ensures": "correct — matches “as long as human nature remains the same … suffering will persist”.",
 "Because charitable institutions": "wrong — the passage never says charities do not function properly.",
 "These are attributed to poor hospital": "wrong — the passage says even more hospitals would not end misery."},
r"Same human nature → same suffering.")
L(77, r"""-> The passage clearly states: "The fundamental remedy consists in cultivating moral purity in mankind."
-> It adds that misery reduces only when people become enlightened, morally steadfast and spiritually strong.
-> So the fundamental remedy is cultivating moral purity and enlightenment.""",
{"Building more hospitals": "wrong — the passage says hospitals cannot fully end misery.",
 "Increasing charitable donations": "wrong — even every house as a charity would not end suffering.",
 "Cultivating moral purity": "correct — stated as the fundamental remedy.",
 "Expanding government welfare": "wrong — the passage does not mention government welfare."},
r"Fundamental remedy = moral purity.")
L(78, r"""-> The passage says, "Ignorance is the root cause of evil and all the misery seen in society."
-> It links the cure to people becoming "enlightened, morally steadfast", i.e. ignorance leads to moral weakness and wrong conduct.
-> So the author sees ignorance as the root of evil because it leads to moral weakness and unethical behaviour.""",
{"Ignorance leads to moral weakness": "correct — the remedy is enlightenment and moral steadfastness.",
 "Ignorance prevents people from accessing": "wrong — the passage plays down material resources.",
 "Ignorance makes people dependent": "wrong — dependence on charity is not discussed.",
 "Ignorance increases physical suffering": "wrong — the passage stresses moral, not physical, causes."},
r"Ignorance → moral weakness → evil.")
L(79, r"""-> The last sentence imagines that every house in every village is turned into a charitable institution and the whole country is covered with hospitals.
-> Even then, the author says, suffering would not end until human character changes.
-> So the imaginary situation is a nation where every house is a charitable institution.""",
{"A country rich in natural resources": "wrong — not mentioned.",
 "A society of universal employment": "wrong — not mentioned.",
 "A world where civilization has collapsed": "wrong — not mentioned.",
 "A nation where every house": "correct — the author's own imagined example."},
r"Every house a charity, every place a hospital — still misery.")
L(80, r"""-> The whole passage argues that material aid gives only temporary relief.
-> Lasting relief comes only from moral purity, enlightenment and spiritual strength — a change in human character.
-> So the underlying principle is that spiritual and moral development is essential for lasting change.""",
{"Spiritual and moral development": "correct — the central idea of the passage.",
 "Social welfare programs": "wrong — the passage says material help is not enough.",
 "Economic growth automatically": "wrong — economic growth is not discussed.",
 "Technological progress": "wrong — technology is not mentioned."},
r"Lasting change = moral and spiritual change.")
