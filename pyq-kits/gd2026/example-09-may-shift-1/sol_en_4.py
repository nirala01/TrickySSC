from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> In old medicine the spleen was thought to be the seat of anger and bad temper.
-> To "vent one's spleen" is to release or express all one's anger, often on someone who is not to blame.
-> Example: Suhani vented her spleen on her son after being reprimanded by Raghubeer.""",
{"vented her spleen": "correct — the idiom for pouring out anger.",
 "rented her spleen": "wrong — “rent” (to hire out) makes no sense here.",
 "threw her liver": "wrong — not an English idiom.",
 "fried her liver": "wrong — not an English idiom."},
r"Vent = let out (like air through a vent); spleen = anger.")
L(62, r"""-> “Grin” means a broad smile that shows the teeth.
-> So its closest synonym is “smile”.
-> Cry, shout and yawn are other actions of the face or voice, but none means a smile.""",
{"Cry": "wrong — to shed tears, nearly the opposite of a grin.",
 "shout": "wrong — to speak very loudly.",
 "smile": "correct — a grin is a broad smile.",
 "Yawn": "wrong — to open the mouth wide when tired."},
r"Grin = broad smile.")
L(63, r"""-> The four underlined words are “indigenious”, “fauna”, “flora” and “intervention”.
-> The correct spelling is “indigenous” (native to a place) — there is no “i” before “-ous”.
-> Fauna (animals), flora (plants) and intervention are spelt correctly.""",
{"indigenious": "correct answer — misspelt; the right spelling is “indigenous”.",
 "fauna": "wrong — spelt correctly.",
 "flora": "wrong — spelt correctly.",
 "intervention": "wrong — spelt correctly."},
r"indigen-OUS: no extra 'i' (like 'numerous', not 'numerious').")
L(64, r"""-> The question asks for the MISSPELT word.
-> The correct spelling is “opulence” (great wealth or luxury), ending in -ence.
-> Brilliance, defiance and tolerance are spelt correctly.""",
{"Brilliance": "wrong — spelt correctly.",
 "Defiance": "wrong — spelt correctly.",
 "opulance": "correct answer — misspelt; the right spelling is “opulence”.",
 "Tolerance": "wrong — spelt correctly."},
r"Opulent → opulence (-ent → -ence).")
L(65, r"""-> “Explain” means to make something clear and easy to understand.
-> Its antonym is “obscure” — to make something unclear or hard to understand.
-> Clarify, describe and define all have meanings close to explain.""",
{"clarify": "wrong — a synonym of explain.",
 "Describe": "wrong — close in meaning to explain.",
 "obscure": "correct — to make unclear, the opposite of explain.",
 "Define": "wrong — to state the meaning, close to explain."},
r"Explain = make clear; obscure = make unclear.")
L(66, r"""-> “Altar” is the holy table or raised place in a church or temple where prayers and offerings are made.
-> “Alter” sounds the same but is a verb meaning to change.
-> A couple kneels before the church altar to pray, so “altar” fits.""",
{"alter": "wrong — a verb meaning to change; it cannot follow “the church”.",
 "altar": "correct — the holy table in a church.",
 "alder": "wrong — a kind of tree.",
 "alert": "wrong — watchful or a warning; it does not fit."},
r"altAR = a place of prAyer; altER = changE.")
L(67, r"""-> “Calligraphy” is the art of beautiful, decorative handwriting.
-> It comes from the Greek “kallos” (beauty) and “graphein” (to write).
-> The other words are about printing type, word origins and stone printing.""",
{"Typography": "wrong — the art of arranging printed type.",
 "Calligraphy": "correct — the art of beautiful handwriting.",
 "Etymology": "wrong — the study of the origin of words.",
 "Lithography": "wrong — printing from a flat stone or metal plate."},
r"Calli = beautiful, graphy = writing.")
L(68, r"""-> We are dismissed FROM a job, a post or the service.
-> “Dismiss from” is the fixed preposition: He was dismissed from the job because of his laziness.
-> “Off”, “out” and “away” do not follow “dismissed” in this sense.""",
{"from": "correct — dismissed from the job.",
 "off": "wrong — “dismissed off” is not standard English.",
 "out": "wrong — “dismissed out the job” is ungrammatical.",
 "away": "wrong — “dismissed away the job” is ungrammatical."},
r"Dismissed from, removed from, sacked from.")
L(69, r"""-> The active sentence is in the past perfect tense: “She had sold the house …”.
-> Past perfect passive = object + had been + past participle + by + subject.
-> So: The house had been sold by her years before the real estate boom.""",
{"The house has been sold by her years before the real estate boom.": "wrong — present perfect; the tense changes.",
 "The house was sold by her years before the real estate boom.": "wrong — simple past; the tense changes.",
 "The house had been sold by her years before the real estate boom.": "correct — past perfect passive.",
 "The house had sold by her years before the real estate boom.": "wrong — “been” is missing, so it is not passive."},
r"had + V3 → had been + V3.")
L(70, r"""-> The passive sentence is in the simple present tense: “… are organised by the school authorities …”.
-> In the active voice the doer becomes the subject and the verb stays in the simple present: “organise”.
-> So: The school authorities organise the annual science exhibitions with great enthusiasm.""",
{"The school authorities organise the annual science exhibitions with great enthusiasm.": "correct — simple present active.",
 "The annual science exhibitions have been organised by the school authorities with great enthusiasm.": "wrong — still passive, and the tense changes.",
 "The school authorities had organised the annual science exhibitions with great enthusiasm.": "wrong — past perfect; the tense changes.",
 "The school authorities will organise the annual science exhibitions with great enthusiasm.": "wrong — future tense; the tense changes."},
r"are + V3 (passive) → V1 (active), same tense.")
L(71, r"""-> The books are taken from one shelf and put on another, so the sentence shows movement to a place.
-> Movement to a place needs “to” (or “onto”), not “on”: move the books to the upper one.
-> The correct part is “shelf to the upper one and”.""",
{"Let's move all the books kept on this": "wrong — “kept on this shelf” is correct, since the books are resting there.",
 "shelf on the upper one and": "correct answer — “on” should be “to” (movement).",
 "make space for the new books": "wrong — correct.",
 "purchased from the market today.": "wrong — correct."},
r"Rest on a place → on; move to a place → to / onto.")
L(72, r"""-> The verb “lack” takes a direct object: They lack courtesy.
-> But the adjective “lacking” is followed by “in”: They are lacking in courtesy.
-> So the blank needs “in”.""",
{"at": "wrong — “lacking at” is not used.",
 "in": "correct — lacking in minimum courtesy.",
 "by": "wrong — “lacking by” is not used.",
 "of": "wrong — “lack of” is used with the noun, not with “are lacking”."},
r"lack + object; lacking IN + quality; a lack OF + noun.")
L(73, r"""-> S1 says Poirot became connected with the Styles Case. D follows: “His success” (in that case) brought him notoriety.
-> A then brings in the narrator, who took up quarters with him in London.
-> C says the narrator knows most of his cases and will record some; B (“In doing so …”) says where he will begin, and S2 names that case — the Victory Ball. Order: D A C B.""",
{"ACBD": "wrong — A cannot follow S1; “His success” in D must come right after the Styles Case.",
 "BDAC": "wrong — “In doing so” in B needs C (placing cases on record) before it.",
 "DACB": "correct — S1 → D → A → C → B → S2.",
 "CDBA": "wrong — C (“his cases”) cannot come before D introduces his new career."},
r"Look for pronoun links: 'His success' → after the case; 'In doing so' → after the plan.")
L(74, r"""-> S1 describes the wild, rough country. D follows: alone and quietly he made his way through woods, not daring to tell who he was.
-> A gives the reason (“For in those rude times no stranger was safe …”), so A comes after D.
-> C (“So, as a poor pilgrim …”) is the result, and B describes his journey day by day, which leads to S2. Order: D A C B.""",
{"DACB": "correct — S1 → D → A → C → B → S2.",
 "ACBD": "wrong — A explains why he hid his name, so it must follow D.",
 "CBDA": "wrong — “So” in C needs the reason (A) before it.",
 "BDAC": "wrong — B (food and lodging on the way) cannot open the journey."},
r"'For …' gives a reason → it follows the action; 'So …' gives a result → it follows the reason.")
L(75, r"""-> “The reason why … is because” is a redundancy: “reason” and “because” say the same thing twice.
-> The simplest correct form is “I am confused because they are giving me mixed signals.”
-> “The reason I am confused is that …” would also be correct, but it is not among the options.""",
{"Why am I confused is because": "wrong — a question order inside a statement, and still “is because”.",
 "The reason for my confusion is because": "wrong — still uses “reason … because”.",
 "I am confused because": "correct — clear and without redundancy.",
 "No improvement required": "wrong — the underlined part is redundant."},
r"Never 'the reason … is because'; use 'because' alone or 'the reason is that'.")
L(76, r"""-> The subject “Scientists” is plural and the sentence is in the simple present (“often”).
-> A plural subject in the simple present takes the base form of the verb: scientists grapple.
-> The passage itself says: “Scientists who work on spaceship development often grapple with challenges …”.""",
{"grappled": "wrong — past tense; the passage is in the present.",
 "grappling": "wrong — an -ing form cannot stand alone as the verb.",
 "grapple": "correct — plural subject + base verb.",
 "grapples": "wrong — the -s form is for a singular subject."},
r"Plural subject → verb without -s.")
L(77, r"""-> The subject is “The absence of gravity”; the main noun is “absence”, which is singular.
-> A singular subject in the simple present takes the -s form: absence affects.
-> The passage says: “The absence of gravity affects both the mechanical operations …”.""",
{"affects": "correct — singular subject “absence” + verb with -s.",
 "affect": "wrong — the base form is for plural subjects.",
 "were affecting": "wrong — plural and past continuous.",
 "affected": "wrong — past tense; the passage is in the present."},
r"Ignore 'of gravity' — the subject is 'absence' (singular).")
L(78, r"""-> In the passage, spaceships “require a confluence of various scientific disciplines”.
-> The next sentences list aerospace engineers, astrophysicists and biologists working together.
-> So “confluence” means a gathering or coming together (literally, the place where two rivers meet).""",
{"Separation": "wrong — the opposite meaning.",
 "Gathering or coming together": "correct — many disciplines come together.",
 "conflict": "wrong — the passage shows cooperation, not conflict.",
 "Expansion": "wrong — not the meaning of confluence."},
r"Confluence = where rivers meet = coming together.")
L(79, r"""-> The passage says: “Despite these formidable obstacles, the collective efforts … have repeatedly demonstrated triumph over adversity.”
-> The obstacles are zero gravity and communication delays — serious problems.
-> So in this context “formidable” means difficult to deal with.""",
{"Easy to overcome": "wrong — the opposite meaning.",
 "Inspiring wonder or respect": "wrong — a sense of the word for people or rivals, not for obstacles here.",
 "Difficult to deal with": "correct — the obstacles are hard to overcome.",
 "Small or insignificant": "wrong — the opposite meaning."},
r"'Despite these formidable obstacles' → the obstacles are hard ones.")
L(80, r"""-> The passage says spaceships need a confluence of scientific disciplines — engineers, astrophysicists and biologists.
-> It describes extraordinary challenges such as zero gravity and communication delays.
-> It ends with the need for worldwide collaboration. So its main idea is a complex, collaborative effort across many fields.""",
{"Spaceships are simple machines designed only by aerospace engineers.": "wrong — the passage calls them intricate systems built by many disciplines.",
 "The challenges faced by spaceship scientists are minimal due to advanced tech.": "wrong — the passage calls the challenges formidable.",
 "The development of spaceships is a complex, collaborative effort involving multiple scientific fields to overcome extraordinary challenges.": "correct — it covers all the main points.",
 "Human space exploration is limited and has not progressed due to difficulties.": "wrong — the passage says the boundaries of exploration have been pushed."},
r"The main idea covers the whole passage: many fields + big challenges + collaboration.")
