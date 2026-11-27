from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> The idiom asked for means to wait and hope for something that has very little chance of happening.
-> In a drought hardly any rain falls, so waiting for a raindrop then is waiting for something very unlikely.
-> The sentence says a government job has become so hard to get that hoping for one is like that.""",
{"raining cats and dogs": "wrong — means raining very heavily.",
 "waiting for a raindrop in the drought": "correct — hoping for something that is very unlikely to happen.",
 "make hay while the sun shines": "wrong — means to make good use of a chance while it lasts.",
 "a drop in the ocean": "wrong — means a very small amount compared with what is needed."},
r"Drought = no rain; waiting for a raindrop then = hoping against the odds.")
L(62, r"""-> “Fragile” means easily broken or damaged.
-> Its closest synonym is “delicate”.
-> Strong, heavy and solid suggest the opposite qualities.""",
{"strong": "wrong — the opposite of fragile.",
 "Delicate": "correct — easily broken, the same as fragile.",
 "Heavy": "wrong — about weight, not about breaking easily.",
 "Solid": "wrong — firm and hard, the opposite idea."},
r"'Fragile — handle with care' = delicate.")
L(63, r"""-> The question asks for the MISSPELT word among the four underlined words.
-> The correct spelling is “prompting” (causing someone to do something) — the “p” after “m” has been left out.
-> Prolonged, cereals and diversified are spelt correctly.""",
{"prolonged": "wrong — spelt correctly (lasting a long time).",
 "cereals": "wrong — spelt correctly (grain crops such as wheat and rice).",
 "promting": "correct answer — misspelt; the right spelling is “prompting”.",
 "diversified": "wrong — spelt correctly (varied, spread across many kinds)."},
r"Prompt + ing = prom-P-ting; keep the p.")
L(64, r"""-> The question asks for the MISSPELT word.
-> The correct spelling is “indelible” (that cannot be removed or forgotten), ending in “-ible”, not “-able”.
-> Noticeable, portable and memorable are spelt correctly.""",
{"Indelable": "correct answer — misspelt; the right spelling is “indelible”.",
 "Noticeable": "wrong — spelt correctly (the “e” of notice is kept before -able).",
 "Portable": "wrong — spelt correctly.",
 "Memorable": "wrong — spelt correctly."},
r"Indelible ink (election ink) — '-ible', like 'edible'.")
L(65, r"""-> “Produce” means to make, create or bring into existence.
-> Its antonym is “destroy” — to put an end to something or ruin it.
-> Manufacture, generate and construct all mean making something, so they are synonyms.""",
{"Manufacture": "wrong — to make goods, a synonym of produce.",
 "Generate": "wrong — to produce or create, a synonym.",
 "Destroy": "correct — the opposite of produce.",
 "construct": "wrong — to build, close in meaning to produce."},
r"Produce = create; the opposite of creating is destroying.")
L(66, r"""-> Homonyms are words with the same spelling or sound but different meanings.
-> “Well” can mean in good health, a filler word, in a good way, or a deep hole dug to get water.
-> Only the sentence about drawing water uses “well” as a source of water.""",
{"She is not feeling well today.": "wrong — here “well” means in good health.",
 "Well, that's an interesting idea.": "wrong — here “well” is a filler word (interjection).",
 "They drew water from the old village well.": "correct — here “well” is a source of water.",
 "He did well in his exams.": "wrong — here “well” is an adverb meaning in a good way."},
r"You draw water FROM a well — the noun.")
L(67, r"""-> The category or type to which a film, book, song or series belongs is called its “genre”.
-> Examples: comedy, thriller, horror and science fiction are film genres.
-> Phylum and genus are categories used in biology, not for films.""",
{"Family": "wrong — a group of related people, or a biological rank.",
 "Genre": "correct — the category of a film or series.",
 "Phylum": "wrong — a major group in the classification of animals.",
 "Genus": "wrong — a biological rank above species."},
r"Genre (zhon-ruh) — the type of a story: thriller, comedy, drama.")
L(68, r"""-> The verb “believe” takes the preposition “in” when it means to be sure that something exists.
-> “Believe in ghosts / God / magic” is the correct usage.
-> So the sentence reads: “Have you ever believed in ghosts in your life?”""",
{"on": "wrong — “believe on” is not standard English.",
 "in": "correct — believe in = think that something exists.",
 "to": "wrong — “believe to” is not used here.",
 "for": "wrong — “believe for” is not idiomatic."},
r"Believe IN something that may or may not exist.")
L(69, r"""-> The active sentence is in the past continuous tense: “was pruning”.
-> Its passive form is “was/were + being + past participle”.
-> The plural subject “the hedges” takes “were”: “The hedges were being pruned by the gardener when the fog rolled in.” The clause “when the fog rolled in” stays the same.""",
{"The hedges were been pruning by the gardener when the fog rolled in.": "wrong — “were been pruning” is not a correct verb form.",
 "The hedges was pruning the gardener when the fog rolled in.": "wrong — wrong verb form and it changes the meaning.",
 "The hedges were pruned by the gardener when the fog rolled in.": "wrong — this is the simple past passive; the continuous sense is lost.",
 "The hedges were being pruned by the gardener when the fog rolled in.": "correct — past continuous passive."},
r"was/were + -ing (active) → was/were + being + V3 (passive).")
L(70, r"""-> The passive question “Is the public library often visited by students …?” is in the simple present tense.
-> Its active form uses “Do/Does + subject + base verb”: “Do students … often visit the public library?”
-> So the answer keeps the simple present: “Do students often visit the public library while preparing for examinations?”""",
{"Do students often visit the public library while preparing for examinations?": "correct — simple present active question.",
 "Are students often visiting the public library while preparing for examinations?": "wrong — present continuous; the tense changes.",
 "Did students often visit the public library while preparing for examinations?": "wrong — simple past; the tense changes.",
 "Will students often visit the public library while preparing for examinations?": "wrong — simple future; the tense changes."},
r"Is/Am/Are + V3 (passive) → Do/Does + V1 (active).")
L(71, r"""-> “Between” is used for two people or things; “among” is used for three or more.
-> The advantages of being an Indian citizen are many, so the sentence should begin “Among the advantages of …”.
-> The other parts of the sentence are correct.""",
{"Between the advantages of": "correct answer — this part has the error; use “Among”.",
 "being an Indian citizen,": "wrong — this part is correct.",
 "freedom to worship one's own god is": "wrong — this part is correct.",
 "of utmost importance for the orthodox.": "wrong — this part is correct."},
r"Between two, among many.")
L(72, r"""-> The adjective “acquainted” is followed by the preposition “with”.
-> To be acquainted with someone or something means to know them or to be familiar with them.
-> So the sentence reads: “Rishabh was hardly acquainted with such a pace bowler in his life.”""",
{"to": "wrong — “acquainted to” is not correct.",
 "with": "correct — acquainted with = familiar with.",
 "for": "wrong — “acquainted for” is not used.",
 "by": "wrong — “acquainted by” is not used."},
r"Acquainted WITH, familiar WITH.")
L(73, r"""-> S1 says religion begins with fear, so the next sentence (D) gives the saying that shows this: “The fear of the Lord is the beginning of wisdom.”
-> B follows with “But later comes the higher idea” — perfect love casts out fear.
-> C says traces of fear remain until we know God; A then contrasts Christ (who denounced impurity) with God (who cannot be angry), which leads to S2: “Denunciation is never the highest.” Sequence: DBCA.""",
{"DBAC": "wrong — A must come just before S2, which picks up its idea of denouncing.",
 "BDAC": "wrong — B's “But later” cannot come before the first idea (D).",
 "BDCA": "wrong — B cannot open the paragraph after S1.",
 "DBCA": "correct — fear → higher idea of love → traces of fear → denunciation."},
r"Look for linking words: 'But later' (B) follows D; 'denounce' (A) links to S2.")
L(74, r"""-> S1 shows a man standing on a railroad bridge, so the next sentence describes him: his hands were tied behind his back (C).
-> B then mentions the rope round his neck, and A (“It was attached …”) must come straight after B, because “It” is the rope.
-> D describes the boards on which he and his executioners stood, which leads to S2, the officer on the same platform. Sequence: CBAD.""",
{"ACDB": "wrong — A's “It” has nothing to refer to at the start.",
 "BACD": "wrong — the man's tied hands (C) should come right after S1 describes him.",
 "BADC": "wrong — C about his hands cannot come after D about the platform.",
 "CBAD": "correct — hands → rope → rope's fixing → platform."},
r"Pronoun 'It' (A) must follow the noun it refers to — the rope in B.")
L(75, r"""-> “Having completing” is wrong: a perfect participle phrase is “having + past participle” — “having completed”.
-> A participle phrase at the start of a sentence must be followed by the noun that does the action — “the employees”.
-> So the correct sentence is: “Having completed the rigorous training program, the employees felt well prepared for the upcoming challenges.”""",
{"The rigorous training program, having been completed by the employees": "wrong — makes the training program the subject of “felt”.",
 "Having completed the employees rigorous training program,": "wrong — confused word order and the subject is missing.",
 "Having completed the rigorous training program, the employees": "correct — right participle form and the right subject.",
 "No improvement required": "wrong — “having completing” is incorrect."},
r"Having + V3 (having completed), followed by the doer.")
L(76, r"""-> The subject “Startups” is plural, so it takes a plural verb in the simple present.
-> A plural subject takes the base form of the verb without “s”: startups drive.
-> The passage itself says “Startups are driving a cultural shift …”, which has the same meaning.""",
{"drives": "wrong — “drives” goes with a singular subject.",
 "drive": "correct — plural subject, plural verb.",
 "driving": "wrong — an -ing form cannot be the main verb without “are”.",
 "driven": "wrong — a past participle needs a helping verb."},
r"Plural subject → verb without 's' (startups drive).")
L(77, r"""-> The subject “This ecosystem” is singular.
-> The present perfect tense with a singular subject uses “has” + past participle: “has produced”.
-> The passage says: “This ecosystem has produced over a hundred unicorns.”""",
{"has": "correct — singular subject + has + produced.",
 "have": "wrong — “have” goes with a plural subject.",
 "had": "wrong — the past perfect does not fit the passage's present-time description.",
 "having": "wrong — “having produced” leaves the sentence without a main verb."},
r"Singular subject → has + V3.")
L(78, r"""-> The passage says the synergy among incubators, accelerators, investors and the government fuels India's ambition.
-> “Synergy” means the combined working of different groups that produces a greater effect than each could alone.
-> So it means cooperation that leads to a greater effect.""",
{"conflict": "wrong — a disagreement, the opposite idea.",
 "Cooperation that leads to a greater effect": "correct — the meaning of synergy.",
 "Separation": "wrong — keeping apart, the opposite of working together.",
 "Competition": "wrong — rivalry, not combined effort."},
r"Synergy: 1 + 1 > 2 when people work together.")
L(79, r"""-> The passage says sectors like fintech, edtech, healthtech and e-commerce are flourishing while gaining global recognition.
-> “Flourishing” means growing well, developing successfully or thriving.
-> So it most nearly means “thriving and growing”.""",
{"declining": "wrong — getting smaller or weaker, the opposite.",
 "ignoring": "wrong — not paying attention; unrelated.",
 "struggling": "wrong — having difficulty, the opposite idea.",
 "thriving and growing": "correct — the meaning of flourishing."},
r"A flourishing garden is full of healthy, growing plants.")
L(80, r"""-> The passage describes rapid growth: the third-largest startup hub, over 1.5 lakh startups and more than a hundred unicorns.
-> It credits government initiatives (Startup India), tech-savvy youth and internet penetration, and collaboration among incubators, investors and the government.
-> It also says this growth boosts economic growth and employment, so the option that covers all these is the main idea.""",
{"India's startup growth is mostly centered in a few large cities with little government support.": "wrong — the passage stresses strong government support and growth in tier-2 and tier-3 cities.",
 "The startup ecosystem in India is shrinking due to lack of innovation.": "wrong — the passage describes remarkable growth.",
 "India's startup ecosystem is expanding rapidly due to government initiatives, technology adoption, and widespread collaboration, contributing significantly to economic and employment growth.": "correct — it sums up every part of the passage.",
 "Startups in India only focus on local markets without global ambitions.": "wrong — the passage mentions global recognition and a global powerhouse ambition."},
r"The main idea covers the whole passage — growth, its causes and its effects.")
