from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “Throw a wrench (spanner) in the works” means to do something that spoils or disrupts a plan or activity.
-> The image is of a tool dropped into a running machine, jamming it.
-> Example: The sudden rain threw a wrench in the works of our picnic.""",
{"To disrupt, foil, or cause problems to a plan, activity, or project": "correct — the accepted meaning of the idiom.",
 "To have a severe effect on one's feelings": "this is closer to “tug at the heartstrings” or “hit hard”.",
 "Use of a tool to trick someone who is new to a field or industry": "an invented, literal reading — not the idiom's sense.",
 "To take someone or something away from someone or something by pulling in a violent, wrenching manner.": "the literal meaning of the verb “wrench”, not the idiom."},
r"Wrench in the machine → the work stops → plan disrupted.")
L(62, r"""-> “Tug at the heartstrings” means to make someone feel strong emotions such as pity, sadness or sympathy.
-> Heartstrings stand for one's deepest feelings.
-> Example: The story of the lost puppy tugged at everyone's heartstrings.""",
{"To keep someone awaiting a decision": "this is “keep someone on tenterhooks / hanging”.",
 "To evoke strong emotions, usually feelings of sadness, pity, or sympathy, by causing deep emotional stirring.": "correct — the accepted meaning.",
 "To have great influence over someone": "this is “pull the strings” or “have someone wrapped around one's finger”.",
 "To stretch, unwind, or extend something, typically a string or cord of some kind.": "a literal reading of “tug” and “string” — not the idiom."},
r"Heartstrings = deep feelings; tugging them = stirring emotions.")
L(63, r"""-> We must pick the correctly spelt word.
-> The correct spelling is “exaggerate” — double “g”, single “r”, ending “-ate” (e-x-a-g-g-e-r-a-t-e).
-> It means to describe something as larger or more important than it really is.""",
{"Exaggeratte": "misspelt — doubled “t” at the end.",
 "Ecaxaggerate": "misspelt — extra letters “ca” after “E”.",
 "Exagerate": "misspelt — only one “g”.",
 "Exaggerate": "correct spelling."},
r"Ex-AGG-er-ate: two g's, one r, one t.")
L(64, r"""-> “Confine” means to keep someone or something within certain limits; to restrict.
-> Example: The patient was confined to bed for a week.
-> So the synonym is a word that means restrict.""",
{"Free": "the opposite — to release from restriction.",
 "Release": "the opposite — to set free.",
 "Limit": "correct — to limit is to keep within bounds, the same as to confine.",
 "Expand": "the opposite — to make larger or wider."},
r"Confine ≈ limit ≈ restrict; opposite = free.")
L(65, r"""-> We must find the misspelt word.
-> The correct spelling is “yachtsman” (y-a-c-h-t-s-m-a-n), a person who sails a yacht.
-> The option swaps the order of “c” and “t” in “yacht”.""",
{"Yammering": "correct spelling — talking loudly and continuously.",
 "Yearningly": "correct spelling — in a longing way.",
 "Youthfulness": "correct spelling — the quality of being young.",
 "Yatchsman": "misspelt — the correct form is “yachtsman”."},
r"Yacht = y-a-c-h-t → yachtsman.")
L(66, r"""-> An “expert” is a person with great skill or knowledge in a particular field.
-> The antonym is a person who is new to a field and lacks experience.
-> Example: She is an expert at chess, while her brother is a novice.""",
{"skilled": "a synonym of expert, not an antonym.",
 "Master": "a synonym — a person with great skill.",
 "Professional": "close in meaning to expert (a trained, skilled person).",
 "Novice": "correct — a beginner, the opposite of an expert."},
r"Expert ↔ novice (beginner).")
L(67, r"""-> “Blasphemy” is the act of speaking or acting disrespectfully about God or sacred things, religious customs or beliefs.
-> Example: In the play, his remarks about the temple were seen as blasphemy.
-> So the one-word substitute is “blasphemy”.""",
{"obeisance": "the opposite idea — a gesture of deep respect such as bowing.",
 "Alchemy": "medieval chemistry that tried to turn base metals into gold.",
 "Blasphemy": "correct — disrespect towards God or sacred beliefs.",
 "Syllogism": "a form of logical reasoning with two premises and a conclusion."},
r"Blasphemy = insulting the sacred.")
L(68, r"""-> “Ambiguous” describes something that can be understood in more than one way.
-> Example: His ambiguous reply left us unsure whether he agreed.
-> So the one-word substitute is “ambiguous”.""",
{"Repatriate": "to send someone back to their own country.",
 "Vivacious": "lively and full of energy.",
 "Profane": "showing disrespect for religion; not sacred.",
 "Ambiguous": "correct — open to more than one interpretation."},
r"Ambi- = both → ambiguous = with two (or more) meanings.")
L(69, r"""-> The sentence is in the present perfect tense: subject + have/has + past participle (“have built”).
-> In the passive, present perfect becomes object + has/have been + past participle.
-> So “They have built a new library” → “A new library has been built in the town by them.”""",
{"A new library has been built in the town by them.": "correct — present perfect passive (has been built).",
 "A new library is built in the town by them.": "simple present passive — wrong tense.",
 "A new library was built in the town by them.": "simple past passive — wrong tense.",
 "A new library will be built in the town by them.": "simple future passive — wrong tense."},
r"have/has + V3 → has/have been + V3.")
L(70, r"""-> The sentence is a present perfect passive question: Have + subject (sculptures) + been + V3 + by + agent (curators).
-> In the active form the agent becomes the subject and the tense stays present perfect: Have + the curators + installed + the sculptures?
-> The plural subject “curators” takes “have”, not “has”.""",
{"Did the curators install the sculptures in the newly established museum wing?": "simple past — the tense has changed.",
 "Has the curators installed the sculptures in the newly established museum wing?": "wrong agreement — plural “curators” needs “have”.",
 "Will the curators install the sculptures in the newly established museum wing?": "simple future — the tense has changed.",
 "Have the curators installed the sculptures in the newly established museum wing?": "correct — present perfect active, with “have” for the plural subject."},
r"Have … been + V3 (passive) → Have + subject + V3 (active).")
L(71, r"""-> We “spend money on” something; “in” is the wrong preposition with “spend … money” here.
-> Correct sentence: Mr. Barik was a millionaire and he wanted to spend a lot of money on his daughter's marriage to make it a memorable event.
-> So the error is in the part containing “in his”.""",
{"Mr. Barik was a millionaire and he": "no error.",
 "wanted to spend a lot of money in his": "error — it should be “spend a lot of money on his”.",
 "daughter's marriage to make": "no error.",
 "it a memorable event.": "no error."},
r"Spend money/time ON something.")
L(72, r"""-> The fixed phrase is “from now on”, meaning starting at this moment and continuing into the future.
-> Correct sentence: From now on, we are not going to fight over trifles.
-> No other preposition forms this phrase.""",
{"since": "“since now” is not idiomatic; since is used with a past point (since 2010).",
 "Hence": "an adverb meaning “therefore” or “from here”, not part of this phrase.",
 "From": "correct — “from now on”.",
 "For": "“for now” means “for the present time”, and “for now on” is wrong."},
r"From now on = from this moment onwards.")
L(73, r"""-> S1 says there was a discussion in class; the children's questions must come next.
-> C opens with their question “where did they go?” and D gives the narrator's reply “I don't know”.
-> B continues the exchange (“who knows?” — “nobody knows”), and A asks the deeper question about death, which S2 answers.
-> So the order is C, D, B, A.""",
{"CABD": "A (about death) cannot come right after C; the reply in D is missing.",
 "ABDC": "starts with “And they said”, which needs an earlier question.",
 "DBAC": "D is a reply and cannot come before the question in C.",
 "CDBA": "correct — question, reply, follow-up, then the question about death answered in S2."},
r"Question → answer → follow-up → final question answered by S2.")
L(74, r"""-> S1 describes the dark streets of the journey; C continues with the deepening dusk and the difficulty of knowing their direction.
-> D adds the inspector's certainty about Hampstead Heath, keeping the focus on the route.
-> A then breaks the scene with a lighted sweet-shop window where Valentin stops, and B shows him going in to buy chocolate cigars, which S2 comments on.
-> So the order is C, D, A, B.""",
{"CBAD": "B (he went in) cannot come before A introduces the shop.",
 "CABD": "D (about the route) breaks the link between B and S2's comment on his purchase.",
 "CADB": "D splits A (the shop) from B (going into it).",
 "CDAB": "correct — dusk, direction, the shop window, then going in."},
r"Setting → direction → shop appears → he enters → S2.")
L(75, r"""-> In the original sentence, “with a gilded frame” comes after “flea market”, so it seems that the flea market has the gilded frame.
-> A modifier should stand next to the noun it describes: the mirror had the gilded frame.
-> Correct sentence: We bought an antique mirror with a gilded frame from the flea market.""",
{"with the flea market from a gilded frame": "makes no sense — buying a mirror from a frame.",
 "with a gilded frame from the flea market": "correct — the modifier now sits next to “mirror”.",
 "from a gilded frame with the flea market": "jumbled and meaningless.",
 "No improvement required": "wrong — the original has a misplaced modifier."},
r"Keep the describing phrase next to the noun it describes.")
L(76, r"""-> The passage says the novel explores human behaviour in a lawless land and asks whether civilization is natural or imposed.
-> Golding argues that humans are naturally savage and that civilization only hides the evil inside them.
-> So the main idea is the struggle between savage instincts and the rules of civilization.""",
{"The story explores the struggle between humanity's savage instincts and the rules of civilization.": "correct — this sums up the passage's central idea.",
 "The story shows how law and order can overcome chaos and disorder among individuals.": "the passage says the opposite — order breaks down.",
 "The story suggests that when societies are cut off, peace will always result.": "not stated; the boys' isolation leads to savagery, not peace.",
 "The story argues that humans rely mainly on reason to guide their actions.": "the passage stresses instinct and violence, not reason."},
r"Main idea = savage instincts vs civilization.")
L(77, r"""-> The passage states: “Golding argues in his text that human beings are naturally savage.”
-> It adds: “They get attracted towards violence and find pleasure in it.”
-> So Golding portrays humans as naturally drawn to violence and savagery.""",
{"Humans instinctively uphold law and morality": "contradicts “human beings are naturally savage”.",
 "Humans are naturally drawn to violence and savagery": "correct — directly stated in the passage.",
 "Humans prioritize cooperation over conflict": "not supported by the passage.",
 "Humans reject all forms of aggression and brutality": "the opposite of what the passage says."},
r"“Naturally savage … attracted towards violence.”")
L(78, r"""-> The passage says civilization “works like a façade and hides the evil that is deeply rooted inside every individual”.
-> It adds that even when civilization flourishes, humans are only hiding their beast, not destroying it.
-> So civilization is shown as a façade hiding inner brutality.""",
{"Civilization completely eradicates human aggression": "wrong — it hides the beast but does not destroy it.",
 "Civilization naturally emerges without effort": "the passage asks whether it is imposed, and Freud links it to suppressing desires.",
 "Civilization acts as a façade hiding inner brutality": "correct — the passage's own words.",
 "Civilization guarantees moral perfection in society": "not supported; evil remains inside every individual."},
r"Façade = a false front that hides what is behind it.")
L(79, r"""-> The passage says that, according to Freud, civilization would never have happened without the human ability to suppress desires.
-> So civilization depends on people controlling or repressing their basic instincts.
-> The novel shows what happens when that control is lost.""",
{"Civilization develops on its own, even if people do not restrain their instincts.": "contradicts Freud's view in the passage.",
 "Civilization flourishes if individuals openly express aggressive impulses.": "the opposite — aggression must be suppressed.",
 "Civilization has no connection to human instincts or desires.": "wrong — Freud links civilization directly to suppressing desires.",
 "Civilization is maintained when people control or repress their most basic and instinctive urges.": "correct — this is Freud's view as stated."},
r"Freud: civilization = suppression of desires.")
L(80, r"""-> The passage mentions “the fragility of moral restraint”, i.e. how easily moral control breaks down.
-> In the novel, boys stranded on an island quickly slide into savagery without the rules of society.
-> So the vulnerability of moral restraint is shown through their swift decline into chaos.""",
{"Through the boys' very swift decline into chaos and loss of order.": "correct — this shows how fragile moral restraint is.",
 "By portraying characters who interact straightforwardly and cooperate without violence.": "the opposite of what happens in the novel.",
 "In establishing rules and consistently showing all characters follow them.": "the rules break down; they are not consistently followed.",
 "By describing an environment completely devoid of conflict and violence.": "the island is full of conflict and violence."},
r"Fragile restraint → quick fall into chaos.")
