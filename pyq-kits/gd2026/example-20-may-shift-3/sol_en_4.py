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

L(61, r"""-> The idiom “turn over a new leaf” means to make a fresh start and begin to behave in a better way.
-> “Leaf” here is an old word for a page of a book: turning to a new, blank page means leaving past mistakes behind.
-> Example: "After the warning from his coach, he turned over a new leaf and never missed practice again." """,
{"To change one's behaviour, usually in a negative": "wrong — the change is for the better, not for the worse.",
 "Not to change": "wrong — the idiom is all about changing; this is the opposite.",
 "To change one's behaviour, usually in a positive": "correct — to reform oneself and start behaving better.",
 "Search something": "wrong — a literal reading of “leaf”; the idiom has nothing to do with searching."},
r"New leaf = new page = a fresh, better start.")
L(62, r"""-> “Dog eat dog” describes a situation of fierce competition in which people will harm one another to get ahead.
-> It is mostly used as an adjective: “a dog-eat-dog world”, “a dog-eat-dog industry”.
-> Example: "The film business is dog eat dog; nobody waits for you to succeed." """,
{"To fail": "wrong — this describes not trying hard enough, which is unrelated to the idiom.",
 "To stay": "wrong — this is the sense of “dog someone” (follow closely), not of this idiom.",
 "Characterized": "correct — ruthless, merciless competition is exactly what the idiom means.",
 "Make something": "wrong — this has no connection with the idiom."},
r"Dog eat dog = ruthless competition, everyone for himself.")
L(63, r"""-> The correctly spelt word is “Labyrinth”: l-a-b-y-r-i-n-t-h, with a “y” after the “b”.
-> A labyrinth is a maze, a confusing network of paths or passages.
-> The other three words are common spelling traps built by doubling, dropping or changing a letter.""",
{"Labyrinth": "correctly spelt — a maze of confusing paths.",
 "Lacconic": "misspelt — the right spelling is “Laconic” (using very few words), with a single “c”.",
 "Lenguish": "misspelt — the right spelling is “Languish” (to grow weak), with “a” after “L”.",
 "Lasitude": "misspelt — the right spelling is “Lassitude” (tiredness), with double “s”."},
r"Laby-rinth has a “y”; Laconic one c, Languish with a, Lassitude double s.")
L(64, r"""-> “Sturdy” means strongly built, solid and not easily damaged or broken.
-> Its synonyms are strong, robust, tough and solid; its antonyms are fragile, weak and flimsy.
-> Example: "She bought a sturdy pair of boots for the trek." """,
{"Fragile": "wrong — an antonym; it means easily broken.",
 "Weak": "wrong — an antonym; it means lacking strength.",
 "Brittle": "wrong — an antonym; it means hard but likely to snap.",
 "strong": "correct — having strength and firmness, the same sense as sturdy."},
r"Sturdy = strong; the other three are all opposites.")
L(65, r"""-> The misspelt word is “Pronounciation”; the correct spelling is “Pronunciation”.
-> The verb is “pronounce” (with “ou”), but the noun drops the “o”: pro-NUN-ci-a-tion. This is why the word is so often misspelt.
-> The other three words are well-known double-letter words and are all spelt correctly here.""",
{"Occasionally": "correctly spelt — double “c”, single “s”, double “l”.",
 "Embarrassment": "correctly spelt — double “r” and double “s”.",
 "Exaggeration": "correctly spelt — double “g”, single “r”.",
 "Pronounciation": "misspelt — it should be “Pronunciation”, with “nun”, not “noun”."},
r"Pronounce → pronunciation: the noun has “nun”, not “noun”.")
L(66, r"""-> “Existence” means the state of being real or of being present.
-> Its antonym must mean the state of not being, which is “nonexistence” (also absence or nothingness).
-> Example: "Scientists debate the existence of life on other planets." """,
{"Reality": "wrong — a near synonym; what exists is real.",
 "Being": "wrong — a synonym; “being” means existence.",
 "Presence": "wrong — close in meaning; the state of being present.",
 "Nonexistence": "correct — the state of not existing, the direct opposite."},
r"The prefix non- makes the opposite: existence ↔ nonexistence.")
L(67, r"""-> A “fallacy” is a mistaken belief, especially one based on unsound reasoning.
-> It comes from the Latin “fallere”, to deceive; the adjective is “fallacious”.
-> Example: "It is a fallacy that money always brings happiness." """,
{"Largesse": "wrong — it means generosity in giving money or gifts.",
 "Fallacy": "correct — a false belief resting on a faulty argument.",
 "Malaise": "wrong — it means a general feeling of illness or unease.",
 "Equanimity": "wrong — it means calmness of mind, especially in difficulty."},
r"Fallacy = false belief (think “false-acy”).")
L(68, r"""-> Age-group words are built from Latin numbers plus “-genarian”: nonaginta is ninety.
-> A “nonagenarian” is a person aged from 90 to 99.
-> Example: "The nonagenarian still walks two kilometres every morning." """,
{"Octogenarian": "wrong — a person in the eighties (80 to 89).",
 "Nonagenarian": "correct — a person in the nineties (90 to 99).",
 "Centenarian": "wrong — a person who is 100 years old or more.",
 "Septuagenarian": "wrong — a person in the seventies (70 to 79)."},
r"Septua- 70s, Octo- 80s, Nona- 90s, Centen- 100.")
L(69, r"""-> The preposition “by” is used with units of measurement to show the rate at which something is sold or paid for.
-> The pattern is “by + the + unit”: cloth is sold by the metre, eggs by the dozen, petrol by the litre, workers are paid by the hour.
-> So the sentence reads: "Cloth is sold by the metre everywhere." """,
{"in": "wrong — “in the metre” is not used for a rate of sale.",
 "of": "wrong — “of” shows belonging or quantity, not a unit of sale.",
 "by": "correct — “by the metre” gives the unit by which cloth is sold.",
 "out": "wrong — “sold out” means nothing is left, and it cannot be followed by “the metre”."},
r"Rate or unit of sale → by the (metre, dozen, kilo).")
L(70, r"""-> The main clause is in the past continuous tense (were mapping), with the subject “the explorers” and the object “uncharted territories”.
-> Passive of the past continuous: object + was/were + being + past participle + by + subject.
-> The clause “when they went missing” has no object, so it stays unchanged.""",
{"Uncharted territories were being mapped": "correct — “were being mapped” keeps the past continuous tense.",
 "Uncharted territories were mapped": "wrong — “were mapped” is simple past; the continuous sense is lost.",
 "Uncharted territories had been": "wrong — “had been mapped” is past perfect, a different tense.",
 "Uncharted territories are being": "wrong — “are being mapped” is present continuous and clashes with “went missing”."},
r"Were + -ing → were being + past participle.")
L(71, r"""-> The given sentence is a question in the past perfect passive: Had + object + been + past participle + by + doer.
-> Active form: Had + doer + past participle + object. The doer is “the committee” and the object is “the financial proposal”.
-> The second clause “before it was forwarded to the higher authorities” stays as it is.""",
{"Did the committee": "wrong — “did … review” is simple past; the past perfect is lost.",
 "Was the committee": "wrong — “was reviewing” is past continuous.",
 "Had the committee": "correct — “Had the committee reviewed” keeps the past perfect and the question form.",
 "Does the committee": "wrong — “does … review” is simple present and does not match “was forwarded”."},
r"Had + object + been + V3 → Had + doer + V3 + object.")
L(72, r"""-> The sentence is in the present perfect passive (has been defeated) and no doer is mentioned.
-> In the active voice a suitable subject must be supplied. With a negative such as “never”, the subject becomes “no one” and “never” becomes “ever”.
-> “She” (the receiver of the action) becomes the object “her”, and “in any debate” is kept.""",
{"Anyone has never": "wrong — “anyone … never” is not acceptable English; “no one … ever” is required.",
 "No one has defeated her in every": "wrong — “in every debate” changes the meaning; she may still have lost some.",
 "She never defeated": "wrong — it makes her the doer and reverses the meaning.",
 "No one has ever": "correct — present perfect active with “no one … ever” and the same meaning."},
r"Never + no doer → “No one has ever …”.")
L(73, r"""-> The verb “protect” takes the preposition “from” (or “against”) before the danger: protect someone from the cold.
-> “By” after a passive verb names the doer of the action, so “protected by the chilling weather” would mean that the weather did the protecting.
-> Correct sentence: "Before going to bed, the mother ensured that the child was protected from the chilling weather." """,
{"Before going to bed,": "no error — a correct introductory phrase followed by a comma.",
 "the mother ensured": "no error — subject and simple past verb are correct.",
 "that the child was": "no error — the that-clause and the verb “was” are correct.",
 "protected by": "error — “by” should be “from”: protected from the chilling weather."},
r"Protect FROM danger; BY names the doer.")
L(74, r"""-> “Charge” in the legal sense takes the preposition “with”: to be charged with a crime.
-> Compare “accused of” a crime and “convicted of” a crime; “charged” alone pairs with “with”.
-> So the sentence reads: "Veerappan was charged with the murder of several officers." """,
{"with": "correct — “charged with” is the fixed expression for a formal accusation.",
 "out": "wrong — “charged out” gives no meaning here.",
 "from": "wrong — “from” is not used after “charged” for an offence.",
 "by": "wrong — “by” would introduce the authority that charged him, not the offence."},
r"Charged WITH, accused OF, convicted OF.")
L(75, r"""-> The underlined part is in the passive voice, which needs “be + past participle”.
-> “Implement” is the base form; after “was” the past participle “implemented” is required.
-> Correct sentence: "The new policy was implemented by the government after extensive consultations with experts from various fields." """,
{"was implemented by": "correct — “was + implemented” is the proper simple past passive.",
 "was implementing by": "wrong — “was implementing” is active continuous and cannot take “by the government” as doer.",
 "implemented by": "wrong — without “was” the sentence has no finite verb.",
 "No improvement": "wrong — “was implement” is ungrammatical, so an improvement is needed."},
r"Passive = be + V3 → was implemented.")
L(76, r"""-> The first sentence of the passage says that cultural development “first builds on a social level, then on a psychological level”.
-> The next sentence explains it: children first learn from others before they can use that knowledge on their own.
-> So the order is social first, psychological afterwards.""",
{"Cultural development starts socially": "correct — it restates the first sentence of the passage.",
 "Cultural development starts psychologically": "wrong — this reverses the order given in the passage.",
 "Cultural development occurs without": "wrong — the theory rests on social interaction.",
 "Cultural development is due only": "wrong — biological growth is not mentioned in the passage."},
r"Social level first, psychological level next.")
L(77, r"""-> The second paragraph opens with the answer: according to Vygotsky's theory, “the core idea is that thought is shaped by social interactions and culture”.
-> He stressed the roles of parents, relatives, friends and society in developing advanced thinking skills in children.
-> The question asks for the core idea, so the option must repeat this line.""",
{"Thought develops independently": "wrong — the passage says the opposite.",
 "Thought is shaped": "correct — the passage states this in the same words.",
 "Learning is secondary": "wrong — biological growth is not discussed, and learning is called necessary.",
 "Development always precedes": "wrong — that is Piaget's belief, which Vygotsky's view opposes."},
r"Core idea = thought is shaped by society and culture.")
L(78, r"""-> The passage quotes Vygotsky: learning is “a necessary and universal aspect” of developing human psychological functions.
-> “Necessary” rules out anything optional, and “universal” means it applies to everyone.
-> The passage adds that this view opposes the belief that development comes before learning.""",
{"Learning is optional": "wrong — the quotation calls learning necessary.",
 "Learning occurs only after": "wrong — this is the Piaget-style view that Vygotsky opposed.",
 "Learning is a universal": "correct — it mirrors the quoted words “necessary and universal”.",
 "Learning depends solely": "wrong — Vygotsky stressed help from parents, society and peers."},
r"Vygotsky's quote: learning is “necessary and universal”.")
L(79, r"""-> The passage describes the zone of proximal development as the zone of what a child cannot do alone, or can do only with great effort, but can do with assistance and adult guidance or with help from more capable peers.
-> So the ZPD covers skills that lie just beyond independent ability but within reach with help.
-> Mastery in this zone lets children internalise new skills, which later become independent achievements.""",
{"Skills a child can perform independently": "wrong — these are already mastered and lie below the zone.",
 "Skills a child cannot learn": "wrong — the zone is about skills that can be learnt with help.",
 "Skills unrelated": "wrong — the zone depends on social interaction with adults and peers.",
 "Skills a child can achieve with guidance": "correct — it matches “with assistance and adult guidance”."},
r"ZPD = can do with help, not yet alone.")
L(80, r"""-> The passage says Vygotsky's view of learning “opposes Piaget's belief that development precedes learning”.
-> So for Piaget, development comes first; for Vygotsky, learning comes first and leads development.
-> The passage does not say that the two agreed on anything.""",
{"Vygotsky believed learning precedes": "correct — the opposite of Piaget's “development precedes learning”.",
 "Vygotsky believed development precedes": "wrong — that is Piaget's position.",
 "Both agreed": "wrong — the passage presents their views as opposed.",
 "Both emphasized": "wrong — Vygotsky emphasised social factors, and biology is not mentioned."},
r"Piaget: development → learning. Vygotsky: learning → development.")
