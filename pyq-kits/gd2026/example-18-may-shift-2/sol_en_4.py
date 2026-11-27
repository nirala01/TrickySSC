from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> The idiom asked for must mean "with the backing, support or patronage of someone".
-> "Under the auspices of" means exactly that: under the protection or sponsorship of a person or body.
-> The bridge is being built with the chief minister's backing, so "under the auspices of" fits.""",
{"under the supervision of": "wrong — means being watched over or checked, not backed or sponsored.",
 "under the guidance of": "wrong — means being advised or directed, not supported or patronised.",
 "under the auspices of": "correct — with the support and patronage of the chief minister.",
 "under the direction of": "wrong — means being ordered or managed by someone."},
r"Auspices = patronage/sponsorship (from the Latin for omens taken by a patron).")
L(62, r"""-> "Vulnerable" means easily hurt or attacked; exposed to harm.
-> Its closest synonym is "defenceless" (US spelling "defenseless").
-> Strong, secure and protected are its opposites.""",
{"strong": "wrong — an antonym; strong things are hard to harm.",
 "Defenseless": "correct — without defence, easily harmed, the same as vulnerable.",
 "secure": "wrong — an antonym; safe from harm.",
 "Protected": "wrong — an antonym; kept safe from harm."},
r"Vulnerable = open to wounds (Latin vulnus = wound) = defenceless.")
L(63, r"""-> Of the four underlined words, one is spelt wrongly.
-> The correct spelling is "governance" (govern + -ance); the sentence has "governence".
-> Emissions, accountable and deployments are all spelt correctly.""",
{"emissions": "wrong — spelt correctly (double s).",
 "accountable": "wrong — spelt correctly (double c, -able).",
 "governence": "correct — this is the misspelt word; the right form is “governance”.",
 "deployments": "wrong — spelt correctly."},
r"Govern + -ance = governance, like guidance and assistance.")
L(64, r"""-> The question asks for the MISSPELT word.
-> The correct spelling is "inevitable" (-able), meaning certain to happen; "Inevitible" is wrong.
-> Credible, Invisible and Plausible correctly take -ible.""",
{"Credible": "wrong — spelt correctly (believable).",
 "Inevitible": "correct — misspelt; the right spelling is “inevitable”.",
 "Invisible": "wrong — spelt correctly (cannot be seen).",
 "Plausible": "wrong — spelt correctly (seeming reasonable)."},
r"Inevitable ends in -able; credible, visible, plausible take -ible.")
L(65, r"""-> "Increase" means to become or make larger in amount or size.
-> Its opposite is "decrease", to become or make smaller.
-> Grow, expand and raise are all synonyms of increase.""",
{"GROW": "wrong — a synonym; to grow is to increase.",
 "Expand": "wrong — a synonym; to become larger.",
 "Decrease": "correct — the exact opposite of increase.",
 "Raise": "wrong — a synonym; to lift or increase."},
r"In-crease ↔ de-crease.")
L(66, r"""-> The villagers prayed for rain, so the summer must have been without rain.
-> "Drought" is a long period with little or no rain — the word needed.
-> Draught, draft and drift sound or look similar but mean different things.""",
{"draught": "wrong — a current of cold air (or a drink); not dry weather.",
 "draft": "wrong — a first version of a writing, or an order of money.",
 "drift": "wrong — to move slowly with a current.",
 "drought": "correct — a long spell without rain."},
r"Drought (rhymes with out) = no rain out there.")
L(67, r"""-> The definition is a mental condition with an uncontrollable urge to steal.
-> That condition is "kleptomania" (Greek kleptes = thief + mania).
-> The other words are manias for other things.""",
{"Pyromania": "wrong — an uncontrollable urge to set fire to things.",
 "kleptomania": "correct — an uncontrollable urge to steal.",
 "Bibliomania": "wrong — an extreme passion for collecting books.",
 "Anglomania": "wrong — excessive admiration of England and English ways."},
r"Klepto = thief (as in kleptocracy, rule by thieves).")
L(68, r"""-> "Made of" is used when the material can still be seen in the finished thing (a table made of wood).
-> "Made from" is used when the raw material is changed and cannot be seen (paper made from bamboo pulp).
-> Bamboo is pulped and changed to make paper, so "made from" is correct.""",
{"of": "wrong — used when the material stays visible, which bamboo does not in paper.",
 "from": "correct — the raw material is changed in the process.",
 "by": "wrong — “made by” names the maker, not the material.",
 "out": "wrong — “made out” has a different meaning; the material needs “from” here."},
r"Material changed → made from; material still visible → made of.")
L(69, r"""-> The sentence is a future simple question: Will + subject + base verb (inaugurate) + object.
-> Its passive form is: Will + object + be + past participle (inaugurated) + by + subject?
-> So: “Will the new park be inaugurated by the mayor next week?”""",
{"Is the new park inaugurated by the mayor next week?": "wrong — present simple passive; the tense changes.",
 "Will the new park be inaugurated by the mayor next week?": "correct — future simple passive with “will be + past participle”.",
 "Has the new park been inaugurated by the mayor next week?": "wrong — present perfect passive; tense changes.",
 "Was the new park inaugurated by the mayor next week?": "wrong — past simple passive, which also clashes with “next week”."},
r"Will + V1 → Will + be + V3.")
L(70, r"""-> The sentence is future perfect passive: "will have been finalised by the secretary".
-> In the active voice it becomes: subject (the secretary) + will have + past participle (finalised) + object (the report).
-> The time clause "before the chairman arrives for the meeting" stays unchanged.""",
{"The secretary will have finalised the report before the chairman arrives for the meeting.": "correct — future perfect active, the same tense as the passive.",
 "The secretary finalises the report before the chairman arrives for the meeting.": "wrong — present simple; the tense changes.",
 "The secretary had finalised the report before the chairman arrives for the meeting.": "wrong — past perfect, which also clashes with “arrives”.",
 "The secretary was finalising the report before the chairman arrives for the meeting.": "wrong — past continuous; the tense changes."},
r"Will have been + V3 (passive) ↔ will have + V3 (active).")
L(71, r"""-> The error is in the part "among an organism, its habitat,".
-> "Between" is used for a relationship of each item with each other one, even when there are more than two items; "among" is for a group seen as a whole.
-> A relationship between an organism, its habitat and its predators is one-to-one, so it should be "the relationship between an organism, its habitat, and the predators".""",
{"In their study, they tried to": "wrong — this part has no error.",
 "find out the relationship": "wrong — this part has no error.",
 "among an organism, its habitat,": "correct — “among” should be “between” for a relationship between named items.",
 "and the predators present there.": "wrong — this part has no error."},
r"Relationship/difference/treaty between named items — not among.")
L(72, r"""-> The adjective "absorbed" (fully interested in something) takes the preposition "in".
-> So: "Mahasweta is completely absorbed in reading scriptures."
-> "Absorbed with", "absorbed at" and "absorbed on" are not standard.""",
{"at": "wrong — “absorbed at” is not used.",
 "with": "wrong — “absorbed with” is not the standard pairing.",
 "in": "correct — “absorbed in” = deeply interested in.",
 "on": "wrong — “absorbed on” is not used."},
r"Absorbed in, engrossed in, immersed in.")
L(73, r"""-> S1 introduces the time when the writer was eleven and lived on the family farm in Cape Breton.
-> D follows S1: the family had been there a long, long time; C then says much of that time seems like the proverbial yesterday.
-> A ("Yet when I speak on this Christmas 1977 …") doubts which voice he speaks with, and B ("And I am not sure how many liberties …") adds to that doubt, leading to S2 about past and present blending at Christmas. So the order is DCAB.""",
{"CBDA": "wrong — B cannot come before A, and D must follow S1 about the farm.",
 "DCAB": "correct — farm (D) → seems like yesterday (C) → yet unsure of the voice (A) → and unsure of liberties (B).",
 "BACD": "wrong — B's “And I am not sure” needs A before it.",
 "BADC": "wrong — starts with B, which needs A before it."},
r"Find the pair first: A (“I am not sure …”) → B (“And I am not sure …”).")
L(74, r"""-> S1: sometimes you hear it through the pillow at night.
-> D ("But I know there is a place where you can hear it even better") contrasts with S1, then A ("Here is what you do") introduces the steps.
-> C (ease into a tub of water) comes before B (lie back and wait for the ripples to smooth away), and S2 (take a deep breath and slide your head under) ends it. So the order is DACB.""",
{"DACB": "correct — better place (D) → here is what you do (A) → get into the tub (C) → wait for the ripples (B).",
 "CDBA": "wrong — the tub step cannot come before the place is mentioned.",
 "DCBA": "wrong — “Here is what you do” must come before the steps.",
 "CABD": "wrong — the steps cannot come before D introduces the place."},
r"Contrast (But) → announce (Here is what you do) → steps in order.")
L(75, r"""-> The fixed phrase is "with a view to" + -ing form, meaning "with the aim of".
-> "In a view to" is wrong, so the underlined part needs improving.
-> "With a view to providing their children with" corrects it while keeping the rest of the sentence.""",
{"with a view to providing their children with": "correct — the right idiom “with a view to + -ing”.",
 "in view to providing their children with": "wrong — the article “a” is missing; the phrase is “with a view to”.",
 "with a view to provide their children with": "wrong — “to” in “with a view to” is a preposition, so it takes the -ing form “providing”.",
 "No improvement required": "wrong — “in a view to” is incorrect."},
r"With a view to + -ing (never “in a view to”).")
L(76, r"""-> In the sentence, the subject "Scammers" does the action "design".
-> The object "fake job postings" receives the action.
-> When the subject performs the action, the sentence is in the active voice.""",
{"Active voice": "correct — the doer (scammers) is the subject.",
 "Passive voice": "wrong — a passive would read “Fake job postings are designed by scammers”.",
 "Reflexive voice": "wrong — no reflexive pronoun (themselves) is used.",
 "Causative voice": "wrong — there is no “have/get something done” structure."},
r"Doer first → active; receiver first with be + V3 → passive.")
L(77, r"""-> In "Scammers masquerade as hiring managers", the word comes right after the subject "Scammers".
-> It tells us what the scammers do, so it is the main verb of the sentence.
-> "Masquerade" can also be a noun (a masked ball), but here it is a verb.""",
{"Noun": "wrong — here it is not a thing or event; it is the action.",
 "Verb": "correct — it is the action done by the subject “Scammers”.",
 "Adjective": "wrong — it does not describe a noun.",
 "Adverb": "wrong — it does not describe a verb, adjective or adverb."},
r"Subject + masquerade as … → verb.")
L(78, r"""-> In the passage, scammers "masquerade as hiring managers" to cheat job seekers.
-> To masquerade as someone is to pretend to be that person, to put on a false show.
-> So in the passage it means "to pretend to be someone else".""",
{"To dress up for a party": "wrong — that is the noun sense (a masked party), not its use in the passage.",
 "To pretend to be someone else": "correct — the scammers pretend to be hiring managers.",
 "To disappear suddenly": "wrong — not a meaning of masquerade.",
 "To ask for a favor": "wrong — not a meaning of masquerade."},
r"Masquerade = mask + parade: pretend to be someone you are not.")
L(79, r"""-> The passage advises "avoidance of suspicious upfront payments".
-> "Suspicious" means causing doubt or a feeling that something is wrong or dishonest.
-> So the closest meaning is "doubtful or questionable".""",
{"trustworthy and clear": "wrong — the opposite of suspicious.",
 "common and usual": "wrong — nothing about being ordinary.",
 "doubtful or questionable": "correct — the same as suspicious.",
 "fast and efficient": "wrong — not related to suspicion."},
r"Suspicious = raises suspicion = doubtful.")
L(80, r"""-> The passage names fake job postings, sham interviews, fake staffing agencies asking for upfront payments and similar false promises.
-> It says these cause financial loss and expose victims to identity theft and legal trouble.
-> So the main frauds are fake job postings and false promises, causing financial loss and identity theft.""",
{"Fake job postings and false promises, causing financial loss and identity theft.": "correct — matches both the frauds and their effects given in the passage.",
 "Government job alerts and verified recruitment, ensuring job security.": "wrong — these are genuine processes, not frauds.",
 "Real job offers with transparent processes, helping job seekers find employment.": "wrong — the passage is about fake offers.",
 "Online training programs providing free certifications to all applicants.": "wrong — the passage says scammers ask for training fees, not free certificates."},
r"Frauds = fake postings + false promises; harm = money lost + identity theft.")
