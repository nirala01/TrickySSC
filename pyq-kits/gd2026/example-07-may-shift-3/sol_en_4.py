from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “The beau monde” (French: the beautiful world) means fashionable, wealthy high society.
-> The sentence says Rabina was not interested in high society and wanted to focus on acting.
-> Completed: Rabina had no interest in the beau monde, but she wanted to focus on acting.""",
{"the anima mundi": "wrong — Latin for “the world soul”, a philosophical idea.",
 "the beau monde": "correct — the rich and fashionable society.",
 "the spiritus mundi": "wrong — “spirit of the world”, a term from Yeats's poetry.",
 "the le monde": "wrong — “le” already means “the”, and “le monde” simply means “the world”."},
r"Beau = beautiful, monde = world → the fashionable world.")
L(62, r"""-> “Foe” means an enemy or opponent.
-> Example: He faced his old foe in the final.
-> Its antonyms are friend and ally.""",
{"ally": "wrong — an ally is a friend or supporter, the opposite of a foe.",
 "Friend": "wrong — this is the opposite of foe.",
 "Enemy": "correct — same meaning as foe.",
 "Guest": "wrong — a guest is a visitor."},
r"Foe = enemy; friend and ally are its opposites.")
L(63, r"""-> Check each underlined word: equitable, resources, discrmination, marginalised.
-> The correct spelling is “discrimination” — an “i” is missing after “discr”.
-> “Marginalised” is the correct British spelling (American: marginalized).""",
{"equitable": "wrong — spelt correctly (fair and just).",
 "resources": "wrong — spelt correctly.",
 "discrmination": "correct — this is the misspelt word; it should be “discrimination”.",
 "marginalised": "wrong — spelt correctly in British English."},
r"dis-CRI-mi-na-tion: four i's in all.")
L(64, r"""-> The correct spelling is “Ambience” (the character or mood of a place).
-> In “Ambeince” the letters e and i are swapped.
-> The other three words end correctly in -ence.""",
{"Ambeince": "correct — misspelt; it should be “Ambience”.",
 "Consequence": "wrong — spelt correctly.",
 "Convergence": "wrong — spelt correctly.",
 "Excellence": "wrong — spelt correctly."},
r"Ambi-ence: i before e here.")
L(65, r"""-> To “express” means to show or put feelings and thoughts into words.
-> Its opposite is to “suppress” — to hold back or hide them.
-> Example: She could not suppress her laughter.""",
{"convey": "wrong — a synonym of express.",
 "suppress": "correct — the opposite of express.",
 "Announce": "wrong — this means making something known, close to express.",
 "Declare": "wrong — this also means stating openly."},
r"Ex-press (push out) ↔ sup-press (push down).")
L(66, r"""-> A knight pledged loyalty to his lord — the noble or king he served.
-> The four options sound or look alike, so the meaning decides.
-> Completed: The knight pledged his loyalty to the lord.""",
{"lord": "correct — a noble master to whom loyalty is pledged.",
 "lured": "wrong — a verb meaning tempted; it cannot follow “the”.",
 "load": "wrong — a heavy thing being carried.",
 "laud": "wrong — a verb meaning to praise."},
r"Knights serve a lord; laud = praise.")
L(67, r"""-> A “neologism” is a newly coined word or expression (Greek: neo = new, logos = word).
-> Example: “selfie” was once a neologism.
-> The other words start with “neo” or sound wise but mean different things.""",
{"Neoplasm": "wrong — a new abnormal growth of tissue (a tumour).",
 "Neoteny": "wrong — keeping young features into adulthood (biology).",
 "Neologism": "correct — a newly coined word or expression.",
 "Maxim": "wrong — a short saying that states a rule of conduct."},
r"Neo (new) + logos (word) = neologism.")
L(68, r"""-> The verb “brood” takes the preposition “over” (or “on/about”) for thinking long and unhappily about something.
-> Completed: I don't like brooding over my past events and killing my present.
-> “Regarding” and “related” are not prepositions that go with “brood”.""",
{"over": "correct — “brood over” = keep worrying about.",
 "for": "wrong — “brood for” is not idiomatic.",
 "regarding": "wrong — not used with “brood”.",
 "related": "wrong — an adjective, not a preposition."},
r"Brood OVER, dwell ON.")
L(69, r"""-> Active: The early bird (subject) catches (simple present) the worm (object).
-> Passive in simple present: object + is/am/are + past participle + by + subject.
-> The worm is caught by the early bird.""",
{"The worm catches the early bird.": "wrong — this changes the meaning; it is still active.",
 "The worm is caught by the early bird.": "correct — is + caught (V3) + by.",
 "The worm is catch by the early bird.": "wrong — “catch” must be the past participle “caught”.",
 "The early bird catch the worm.": "wrong — still active, and the verb should be “catches”."},
r"Simple present passive: is/are + V3.")
L(70, r"""-> The passive “have been made by researchers” is present perfect.
-> In the active, the agent “researchers” becomes the subject and the verb becomes “have made”.
-> Researchers have made several important archaeological discoveries in the desert region.""",
{"Researchers make several important archaeological discoveries in the desert region.": "wrong — simple present; the tense changes.",
 "Researchers were making several important archaeological discoveries in the desert region.": "wrong — past continuous.",
 "Researchers have made several important archaeological discoveries in the desert region.": "correct — present perfect is kept.",
 "Researchers had made several important archaeological discoveries in the desert region.": "wrong — past perfect."},
r"have been + V3 (passive) ↔ have + V3 (active).")
L(71, r"""-> “Admit of” means to allow or leave room for (formal use).
-> “It admits of no delay” = it allows no delay at all.
-> Other prepositions do not give this meaning with “admit”.""",
{"in": "wrong — “admit in” means to let someone enter.",
 "of": "correct — “admit of” = allow, leave room for.",
 "by": "wrong — not idiomatic with “admit”.",
 "for": "wrong — not idiomatic here."},
r"Admits OF no delay / no doubt / no excuse.")
L(72, r"""-> S1 shows Frederick riding up and down; C follows: a thousand knights were behind him.
-> A describes those knights (“They were the flower of Germany”), so A comes right after C.
-> D and B then return to the emperor — his beard, then his sword waved above his head — leading to S2 (his voice as he turned in his saddle). The sequence is CADB.""",
{"ACBD": "wrong — “They” in A has no noun before it.",
 "BACD": "wrong — “They” in A would wrongly refer to the sword.",
 "CBAD": "wrong — B breaks the link between the knights (C) and “They” (A).",
 "CADB": "correct — knights, then “they”, then the emperor's beard and sword."},
r"A pronoun (They) must follow the noun it refers to (knights).")
L(73, r"""-> S1 mentions palaces and castles; D describes the palaces first.
-> A then turns to the castles with their gloomy prisons, and C names one prison castle on Sainte Marguerite.
-> B describes that place (“A dark and lonely place it was …”), leading to S2 about the prisoners. The sequence is DACB.""",
{"CBDA": "wrong — C names “these prison castles” before the prisons are mentioned.",
 "BDAC": "wrong — B's “it” has nothing to refer to.",
 "ACBD": "wrong — D (palaces) cannot come after the prison description.",
 "DACB": "correct — palaces → castles with prisons → one prison island → its description."},
r"Follow the order of S1: palaces first, then castles.")
L(74, r"""-> The idiom “cannot help” means cannot avoid; it takes a gerund (“can't help feeling”) or “but + base verb”.
-> “I can't help feel sorry” is wrong; “I can't help but feel sorry for her” is correct.
-> The second half of the sentence stays the same.""",
{"I can't help but feel sorry for her": "correct — “can't help but + base verb”.",
 "I can't feel sorry for her": "wrong — this reverses the meaning.",
 "I can't help and feel sorry for her": "wrong — “help and feel” is ungrammatical.",
 "No improvement required": "wrong — the original “help feel” is incorrect."},
r"Can't help + -ing, or can't help but + V1.")
L(75, r"""-> We say “in the evening” for a part of the day; “on” is used only with a specific day or date (“on the evening of 5 May”).
-> Here no date follows, so “on the evening” is wrong — it should be “in the evening”.
-> The other parts are correct.""",
{"However, on the": "correct — this part has the error; use “in the evening”.",
 "evening, he returned with": "wrong — no error in this part.",
 "one foot limping because": "wrong — no error in this part.",
 "his heel was wounded.": "wrong — no error in this part."},
r"In the morning/evening; on Monday evening.")
L(76, r"""-> Active (simple present): Governments (subject) emphasize (verb) strict traffic laws (object).
-> Passive: object + are + past participle + by + subject.
-> Strict traffic laws are emphasized by governments.""",
{"Strict traffic laws are emphasized by governments.": "correct — are + emphasized (V3) + by.",
 "Governments are emphasized by strict traffic laws.": "wrong — subject and object are reversed.",
 "Governments were emphasizing strict traffic laws.": "wrong — past continuous active, not passive.",
 "Strict traffic laws emphasize governments.": "wrong — active, and the meaning is reversed."},
r"Plural object → are + V3.")
L(77, r"""-> “Safer” (safe + -er) and “more intelligent” (more + adjective) both compare cars of the future with cars of today.
-> Such forms are the comparative degree.
-> Short adjectives add -er; long adjectives take “more”.""",
{"Positive degree": "wrong — that would be “safe” and “intelligent”.",
 "Comparative degree": "correct — safer, more intelligent.",
 "Superlative degree": "wrong — that would be “safest” and “most intelligent”.",
 "Past degree": "wrong — there is no such degree of comparison."},
r"-er / more = comparative; -est / most = superlative.")
L(78, r"""-> In the passage, “negligence” is the failure to take proper care (driving without seatbelts or helmets).
-> So its synonym is carelessness.
-> Attention and discipline are its opposites.""",
{"Carelessness": "correct — same meaning as negligence.",
 "Discipline": "wrong — near opposite.",
 "Attention": "wrong — the opposite of negligence.",
 "strictness": "wrong — means firmness, not lack of care."},
r"Neglect = not caring → carelessness.")
L(79, r"""-> A homonym here is a word that shares its sound with other words of different meaning and spelling.
-> “Right” sounds the same as “write” and “rite”, and also has several meanings (correct, the opposite of left, a legal claim).
-> The other three words have no such sound-alike partners.""",
{"Every": "wrong — no common word sounds the same.",
 "Essential": "wrong — no sound-alike word.",
 "Right": "correct — right / write / rite.",
 "Influence": "wrong — no sound-alike word."},
r"Right–write–rite: same sound, different meanings.")
L(80, r"""-> The passage says that even though cars will become safer, “no machine can replace human responsibility”.
-> It then asks drivers to follow rules sincerely, respect pedestrians and remain alert — moral choices that machines cannot make.
-> So the reason is that machines cannot make ethical decisions and drivers must remain alert.""",
{"Because machines are not allowed on all roads": "wrong — the passage says nothing like this.",
 "Because technology is always unsafe": "wrong — the passage says cars will become safer.",
 "Because pedestrians will not follow rules": "wrong — the passage asks drivers to respect pedestrians.",
 "Because machines cannot make ethical decisions and drivers must remain alert": "correct — the passage's point about human responsibility and moral duty."},
r"Technology helps, but responsibility stays human.")
