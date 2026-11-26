from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> An idiom is a fixed phrase whose meaning differs from the meanings of its words.
-> “Water under the bridge” means past events or problems that are over and no longer important.
-> Example: We argued last year, but that is water under the bridge now.""",
{"Water under the ocean": "not an idiom — just a literal phrase.",
 "Water under the soil": "a literal description of groundwater, not an idiom.",
 "Water under the tunnel": "not a recognised English idiom.",
 "Water under the bridge": "correct — an idiom meaning past matters that no longer matter."},
r"Water that has flowed under the bridge cannot come back — the past is past.")
L(62, r"""-> “Top banana” (informal) means the most important person in a group — the leader or boss.
-> It comes from American comedy shows, where the lead comedian was called the top banana.""",
{"A person whose hands are very thin": "unrelated to the idiom.",
 "A beggar or a very poor person": "the opposite idea — a top banana is powerful.",
 "A person whose neck is long": "unrelated to the idiom.",
 "A leader, boss, chief person in a group": "correct — the chief person."},
r"Top banana = top dog = boss.")
L(63, r"""-> “Considerable” means large in amount, size or importance.
-> “A considerable amount of money” = a large or important amount of money.""",
{"Tiny": "very small — the opposite meaning.",
 "significant": "correct — large or important, the same as considerable.",
 "Limited": "restricted or small — nearly opposite.",
 "Differentiate": "a verb meaning to tell apart — not even the same part of speech."},
r"Considerable ≈ significant ≈ substantial.")
L(64, r"""-> “Confess” means to admit that you have done something wrong or that something is true.
-> Example: He confessed his mistake to the teacher.""",
{"Admit": "correct — the same meaning as confess.",
 "Deny": "the opposite — to say something is not true.",
 "Refuse": "to say no to something — a different meaning.",
 "Ignore": "to pay no attention — unrelated."},
r"Confess = admit; opposite = deny.")
L(65, r"""-> The task is to find the word spelt wrongly.
-> The correct spelling is “wretchedness” (w-r-e-t-c-h-e-d-n-e-s-s), meaning a state of misery or unhappiness.""",
{"whimsical": "correctly spelt — playful or fanciful.",
 "whistleblower": "correctly spelt — a person who exposes wrongdoing.",
 "Wrechedness": "misspelt — the “t” before “ch” is missing; the correct form is “wretchedness”.",
 "Wilderness": "correctly spelt — a wild, uninhabited area."},
r"Wretch + ed + ness — keep the “tch”.")
L(66, r"""-> “Developed” means advanced, grown or modern (a developed country, a developed mind).
-> Its antonym describes something not advanced or lagging behind.""",
{"Advanced": "a synonym of developed.",
 "Evolved": "developed gradually — a synonym.",
 "Backward": "correct — not developed, lagging behind, the opposite.",
 "Modern": "close to developed in meaning, not opposite."},
r"Developed ↔ backward / underdeveloped.")
L(67, r"""-> A screenplay is the script of a film or TV show.
-> A person who writes it is called a scriptwriter (also screenwriter).""",
{"Scriptwriter": "correct — one who writes scripts and screenplays.",
 "screenplayer": "not a real English word.",
 "Playwright": "a person who writes plays for the theatre, not screenplays.",
 "Ghostwriter": "a person who writes for someone else who is credited as the author."},
r"Screenplay → scriptwriter/screenwriter; stage play → playwright.")
L(68, r"""-> A fugitive is a person who has escaped or is running away, especially from the police or the law.
-> Example: The police caught the fugitive at the border.""",
{"Inmate": "a person kept in a prison or hospital — not escaping.",
 "suspect": "a person thought to be guilty — not necessarily running away.",
 "Fugitive": "correct — one who is escaping from the law.",
 "Criminal": "a person who has committed a crime — escaping is not part of the meaning."},
r"Fugitive = on the run from the law.")
L(69, r"""-> “In token of” means as a sign or symbol of something.
-> The friends wore white shirts as a symbol of their friendship, so “in token of” fits.""",
{"in token of": "correct — as a sign of their friendship.",
 "in lieu of": "means “instead of” — the shirts did not replace the friendship.",
 "by dint of": "means “by means of” effort — wrong sense.",
 "with respect to": "means “concerning” — does not fit."},
r"In token of = as a sign of; in lieu of = instead of.")
L(70, r"""-> The active sentence is a question in the simple past: “Did + subject + V1 + object?”
-> In the passive, the simple past question becomes “Was/Were + object + V3 + by + subject?”. “Tricks” is plural, so “Were”.""",
{"Were amazing tricks performed at the fair by the magician?": "correct — simple past passive with plural “were”.",
 "Have amazing tricks been performed at the fair by the magician?": "present perfect — the tense has changed.",
 "Are amazing tricks performed at the fair by the magician?": "simple present — the tense has changed.",
 "Will amazing tricks be performed at the fair by the magician?": "simple future — the tense has changed."},
r"Did … V1? → Was/Were … V3 by …?")
L(71, r"""-> The passive sentence is future perfect: “Will + object + have been + V3 + by + subject?”
-> In the active voice it becomes “Will + subject + have + V3 + object?” — the government becomes the subject.""",
{"Will the government complete the infrastructure projects before the deadline set by the council?": "simple future — the perfect tense is lost.",
 "Will the government have completed the infrastructure projects before the deadline set by the council?": "correct — future perfect active.",
 "Will have the government completed the infrastructure projects before the deadline set by the council?": "wrong word order — the subject must come right after “Will”.",
 "Will the government completed the infrastructure projects before the deadline set by the council?": "“will” must be followed by a base verb or “have”, not V2/V3 alone."},
r"Will … have been V3 by X? → Will X have V3 …?")
L(72, r"""-> We act in a film or play, so “acted in several movies” is correct.
-> “Act in” is used for taking part in a movie, play or show.""",
{"on": "“acted on” means took action because of something — wrong sense.",
 "in": "correct — acted in several Hindi movies.",
 "at": "used for places or points, not for films.",
 "with": "would name co-actors, not the movies."},
r"Act in a film/play; act on advice.")
L(73, r"""-> “Each of the representatives” takes a singular verb because the subject is “each”.
-> So “have presented” must become “has presented”; “their reports” is acceptable.""",
{"have presented their report": "keeps the plural verb “have” — still wrong.",
 "has presented their reports": "correct — singular verb agrees with “each”.",
 "were presented their reports": "changes the meaning to passive and keeps a plural verb.",
 "No improvement required": "wrong — the original has a subject–verb agreement error."},
r"Each / every / either / neither + of + plural noun → singular verb.")
L(74, r"""-> S1 shows the herdsman seeing young snakes; the next sentence should describe them — D (they looked thin and miserable).
-> C (he felt sorry and fed them milk) follows, then B (they grew strong and met their mother, who exclaimed), then A (the rest of her words), and S2 closes the story.""",
{"DCBA": "correct — S1, D, C, B, A, S2.",
 "CDAB": "the herdsman cannot feel sorry before we know how they looked.",
 "BDCA": "the snakes cannot grow strong before they are fed.",
 "ACBD": "A continues the mother's speech, so it cannot come first."},
r"Description → reaction → result → speech.")
L(75, r"""-> The sentence is in the past tense: “she was unable to answer”.
-> “She didn't study for the test” uses “did not + base verb” correctly, so no change is needed.""",
{"She didn't studied for the test": "wrong — after “did not” the base verb “study” is used.",
 "She don't study for the test": "wrong — “don't” does not agree with “she” and the tense is wrong.",
 "She doesn't study for the test": "present tense — does not match “was unable”.",
 "No improvement required": "correct — the underlined part is already right."},
r"Did/didn't + base verb (V1), never V2.")
L(76, r"""-> “With all electricity and heating ___ from geothermal and hydroelectric sources” is a “with + noun + -ing” phrase.
-> In this structure the verb takes the -ing form: “with all electricity and heating coming from …”.""",
{"comes": "a finite verb cannot follow “with + noun” here.",
 "coming": "correct — with + noun + present participle.",
 "come": "a base verb does not fit after “with + noun”.",
 "came": "a past finite verb does not fit this phrase."},
r"With + noun + -ing (with prices rising, with all heating coming …).")
L(77, r"""-> Blank B qualifies the noun “trust”, so it needs an adjective.
-> “High level of education and strong trust in public institutions.”""",
{"strong": "correct — adjective describing trust.",
 "strongly": "an adverb — cannot describe a noun.",
 "strength": "a noun — “strength trust” is ungrammatical.",
 "strengthening": "a verb form — wrong sense and grammar here."},
r"Before a noun → adjective (strong trust).")
L(78, r"""-> The passage says summer brings daylight that can last 24 hours.
-> This natural event in the Arctic is called the “midnight sun” — the sun is visible even at midnight.""",
{"always shining": "too general and not the fixed term.",
 "midnight": "correct — the midnight sun.",
 "continuing": "does not form a natural phrase with “sun”.",
 "forever": "not an adjective for “sun” here and exaggerates."},
r"24-hour summer daylight = midnight sun (Iceland, Norway).")
L(79, r"""-> In the passage, (D) is “vibrant” in “vibrant Reykjavik culture”.
-> Vibrant means full of energy, life and excitement.""",
{"Quiet": "the opposite — calm, not lively.",
 "Dull": "boring — opposite of vibrant.",
 "Simple": "plain — not the meaning of vibrant.",
 "Lively": "correct — full of energy, the same as vibrant."},
r"Vibrant ≈ lively; opposite = dull.")
L(80, r"""-> In the passage, (E) is “heritage” in “deeply rooted in both heritage and innovation”.
-> Here heritage means a country's history, culture and traditions passed down over time, contrasted with innovation.""",
{"Property": "physical possessions — not the sense here.",
 "Ancestors": "people from the past, not the culture they left.",
 "Inheritance": "money or property received from someone who has died — the legal sense, not the cultural one used here.",
 "History and traditions": "correct — the cultural heritage of Iceland."},
r"Heritage (cultural) = history + traditions; inheritance = property received.")
