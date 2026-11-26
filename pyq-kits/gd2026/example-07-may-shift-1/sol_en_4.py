from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> The idiom “to take something with a pinch of salt” means not to believe it completely, or to doubt that it is fully accurate or true.
-> Rohan likes Mohan, so he does not take Mohan's harsh words too seriously — he does not accept them as entirely true.
-> Complete sentence: Rohan … takes the latter's harsh words with a pinch of salt.""",
{"with a jar of sugar": "wrong — not an English idiom.",
 "with a sheet of paper": "wrong — not an idiom; it has no figurative meaning.",
 "with a pinch of salt": "correct — the idiom meaning to doubt or not fully believe something.",
 "with a bar of chocolate": "wrong — not an idiom."},
r"A pinch of salt = a little doubt; don't swallow it whole.")
L(62, r"""-> “Absurd” means wildly unreasonable, foolish or ridiculous.
-> Example: It is absurd to wear a winter coat in May.
-> The synonym must also mean foolish or senseless.""",
{"sensible": "wrong — it means wise or reasonable, the opposite of absurd.",
 "Logical": "wrong — it means reasonable and well-argued, an antonym.",
 "silly": "correct — it means foolish or ridiculous, the same as absurd.",
 "Smart": "wrong — it means clever, nearly the opposite."},
r"Absurd = silly / ridiculous; sensible and logical are its opposites.")
L(63, r"""-> We must find the underlined word that is spelt wrongly.
-> “Illegal” + “-ly” keeps both l's: the correct spelling is “illegally”.
-> The other three underlined words are spelt correctly.""",
{"tribunal": "correct spelling (a court or body that judges disputes).",
 "breaching": "correct spelling (breaking a law or agreement).",
 "illegaly": "misspelt — the correct spelling is “illegally”.",
 "suppressing": "correct spelling (double p, double s)."},
r"Adjective ending in -l + ly → -lly: illegally, usually, finally.")
L(64, r"""-> We must find the one word that is spelt wrongly.
-> Nouns from verbs ending in -d usually take -sion: suspend → suspension.
-> “Suspention” is therefore misspelt.""",
{"Innovation": "correct spelling (introducing new ideas).",
 "Invention": "correct spelling (something newly created).",
 "suspention": "misspelt — the correct spelling is “suspension”.",
 "Revelation": "correct spelling (something revealed)."},
r"suspend → suspension, extend → extension, comprehend → comprehension.")
L(65, r"""-> As a verb, “reserve” means to keep something back or hold it for later use.
-> Example: The seats are reserved for senior citizens.
-> Its opposite means to let something go or set it free.""",
{"withhold": "wrong — it means to hold back, a synonym of reserve.",
 "Allocate": "wrong — it means to set aside for a purpose, close to reserve.",
 "Release": "correct — to let go or set free, the opposite of keeping back.",
 "Accumulate": "wrong — it means to collect or pile up, which is also keeping, not letting go."},
r"Reserve = keep back; release = let go.")
L(66, r"""-> “Did not” must be followed by the base form of a verb.
-> The sentence is about noticing a car with the eyes, so the verb “see” fits.
-> Sea / see and scene / seen are homophones — they sound alike but mean different things.""",
{"sea": "wrong — a noun meaning a large body of salt water.",
 "scene": "wrong — a noun meaning a place or view; it is not a verb.",
 "see": "correct — the verb meaning to notice with the eyes: “did not see the car”.",
 "sin": "wrong — a noun or verb meaning a wrong act; it does not fit the meaning."},
r"After did / does / do → base verb: did not see.")
L(67, r"""-> A word formed by rearranging the letters of another word is an anagram.
-> Examples: listen → silent, earth → heart.
-> The other options are other kinds of words.""",
{"Acronym": "wrong — a word made from the first letters of other words, like NASA.",
 "Anagram": "correct — a word made by rearranging the letters of another word.",
 "Homonym": "wrong — a word with the same spelling or sound but a different meaning.",
 "Synonym": "wrong — a word with the same or similar meaning."},
r"Ana-GRAM = letters (grammata) rearranged.")
L(68, r"""-> The phrasal verb “knock someone down” means to hit someone so that they fall to the ground.
-> In boxing it means flooring the opponent: Tyson knocked Holmes down in 1988.
-> Complete sentence: Mike Tyson knocked Larry Holmes down in 1988 in a boxing match.""",
{"Up": "wrong — “knock up” means to make something quickly or to wake someone; it does not suit a punch.",
 "into": "wrong — “knock into” means to bump into someone by accident.",
 "down": "correct — “knocked … down” means hit him to the floor.",
 "away": "wrong — “knock away” means to hit something aside; it is not used for flooring a boxer."},
r"Knock down = hit to the ground (boxing knockdown).")
L(69, r"""-> The active sentence is in the present perfect tense: “People have celebrated”.
-> Present perfect passive = has/have + been + past participle; the subject “this festival” is singular, so “has been”.
-> The agent “people” is general, so it can be dropped.""",
{"This festival has been celebrated for centuries.": "correct — singular subject + has been + celebrated keeps the present perfect.",
 "This festival have been celebrated for centuries.": "wrong — “have” does not agree with the singular subject “this festival”.",
 "This festival is celebrated for centuries.": "wrong — present simple passive; the tense changes.",
 "This festival was celebrated for centuries.": "wrong — past simple passive; the tense changes."},
r"Present perfect: have/has + V3 → has/have been + V3.")
L(70, r"""-> The passive question is in the present continuous: “Is the road being repaired by …?”
-> In active form the doer (the municipal workers) becomes the subject: Are + subject + V-ing + object?
-> The subject is plural, so “Are … repairing”.""",
{"Are the municipal workers repairing the road after last week's heavy rains?": "correct — present continuous active with a plural subject.",
 "Do the municipal workers repair the road after last week's heavy rains?": "wrong — present simple; the tense changes.",
 "Have the municipal workers repaired the road after last week's heavy rains?": "wrong — present perfect; the tense changes.",
 "Did the municipal workers repair the road after last week's heavy rains?": "wrong — past simple; the tense changes."},
r"is/are being + V3 → is/am/are + V-ing.")
L(71, r"""-> The verb “experiment” takes the preposition “with” when we try out new things or ideas.
-> “Experiment on” is used for testing on a subject (animals, patients), not for trying new hairstyles.
-> Complete sentence: The urban girls are experimenting with new types of hairstyles.""",
{"of": "wrong — “experiment of” is not used.",
 "in": "wrong — “experiment in” refers to a field of study (an experiment in physics), not to trying things out.",
 "for": "wrong — “experiment for” is not idiomatic here.",
 "with": "correct — “experimenting with new hairstyles” means trying them out."},
r"Experiment WITH ideas / styles; experiment ON subjects.")
L(72, r"""-> S1 says Balboa decided to go in search of the sea; the next step is that he set off — D.
-> B describes the journey (short distance but rough country, slow progress), and A tells us that after many days they reached the highest ridge.
-> C (he climbed the loftiest peak and looked around) leads to S2, where he sees the great sea. Order: D, B, A, C.""",
{"CBAD": "wrong — C (climbing the peak) cannot come before setting off.",
 "DBAC": "correct — set off, journey, ridge, peak.",
 "BDCA": "wrong — B describes the journey before D starts it.",
 "DABC": "wrong — A (reaching the ridge) cannot come before B (the slow journey)."},
r"Set out → journey → arrive → look: follow the time order.")
L(73, r"""-> S1 tells us what she cooked that evening; D (“Then, after …”) continues with getting into bed.
-> A says the doorbell rang while she was reading; C gives her first reaction (a mistake, they will go away).
-> B (“But it rang and rang”) contrasts with C and leads to S2, where she looks at the clock. Order: D, A, C, B.""",
{"BDAC": "wrong — B (“But it rang and rang”) cannot open before the bell has rung.",
 "CBDA": "wrong — C mentions “whoever it was” before the bell rings in A.",
 "DACB": "correct — bed, bell, first thought, persistent ringing.",
 "ACBD": "wrong — D (getting into bed) must come before she reads in bed."},
r"Look for link words: “Then”, “At first”, “But”.")
L(74, r"""-> The sentence lists three activities after “enjoys”: hiking, swimming and …
-> Items in a list must be parallel: enjoys + V-ing, so the third must also be an -ing form.
-> Correct sentence: She enjoys hiking in the mountains, swimming in the ocean, and riding her bike in the park every weekend.""",
{"and ride her bike in the park": "wrong — “ride” is not parallel with “hiking” and “swimming”.",
 "and to ride her bike around the park": "wrong — the infinitive “to ride” still breaks the parallel structure.",
 "and riding her bike in the park": "correct — the -ing form matches “hiking” and “swimming”.",
 "No improvement required": "wrong — the underlined part breaks the parallel structure."},
r"enjoy + V-ing, and keep every item in the list in the same form.")
L(75, r"""-> The error is in the last part: an event “takes place”; “gives place” means makes way for something else.
-> A flea market is held on weekends, so it “usually takes place on weekends”.
-> Correct sentence: … a large flea market that is in a major city and usually takes place on weekends.""",
{"He figured that to find a decent": "no error — the subject and verb are correct.",
 "drum he had to go to a large flea": "no error — “had to go” is correct in the past.",
 "market that is in a major city and": "no error — the relative clause is correct.",
 "usually gives place on weekends.": "error — it should be “usually takes place on weekends”."},
r"Events TAKE place; “give place to” = make way for.")
L(76, r"""-> The sentence is “The narrative unfolds as characters seek to discover who committed the crime.”
-> Its subjects (“the narrative”, “characters”) are the doers of the actions “unfolds” and “seek”.
-> There is no “be + past participle” form, so the sentence is in the active voice.""",
{"Causative voice": "wrong — a causative needs have/get/make someone do something; there is none here.",
 "Reflexive voice": "wrong — there is no reflexive pronoun such as “itself” or “themselves”.",
 "Active voice": "correct — the subjects perform the actions “unfolds” and “seek”.",
 "Passive voice": "wrong — there is no be + past participle (such as “is unfolded”)."},
r"No be + V3 and the subject does the action → active voice.")
L(77, r"""-> The passage says the proletarian novel “represents the working class's daily life”.
-> It also says such novels offer social or moral commentary without fantasy elements.
-> So “proletarian” here means related to working-class life and its social issues.""",
{"Related to science and technology": "wrong — that describes the science fiction novel.",
 "Focused on romantic relationships": "wrong — that describes the romance novel.",
 "Involving working-class life and social issues": "correct — the passage links it to working-class life and social commentary.",
 "Concentrating on futuristic imagination": "wrong — the passage says it has no fantasy elements."},
r"Proletariat = the working class.")
L(78, r"""-> The passage says science fiction explores human experience “in speculative contexts” — in futuristic or imaginative worlds.
-> “Speculative” means based on guessing or theory rather than on known facts.
-> So it means imaginary or theoretical, not yet proven.""",
{"based on facts and reality": "wrong — this is the opposite of speculative.",
 "involving careful financial investments": "wrong — that is the financial sense of speculation, not the sense used here.",
 "detailed and comprehensive research": "wrong — speculative ideas are guesses, not detailed research.",
 "imaginary or theoretical, not yet proven": "correct — the meaning in “speculative contexts”."},
r"Speculate = guess; speculative = imagined, not proven.")
L(79, r"""-> In “Both genres intrigue readers …”, “both genres” is the subject and “readers” is the object.
-> “Intrigue” is the action the subject performs on the object — it means to arouse curiosity or interest.
-> So “intrigue” is used here as a verb.""",
{"Noun": "wrong — “intrigue” can be a noun (a secret plot), but here it is the action of the sentence.",
 "Verb": "correct — it is the main verb: genres intrigue (interest) readers.",
 "Adjective": "wrong — it does not describe a noun.",
 "Pronoun": "wrong — it does not stand for a noun."},
r"Subject + ___ + object → the blank word is the verb.")
L(80, r"""-> The passage says a mystery novel centres on a crime committed at the beginning, and characters try to find out who did it.
-> A thriller, in contrast, focuses on preventing a future crime as the heroes race against time.
-> So mysteries look back at a past crime; thrillers look ahead to stop one.""",
{"Mysteries look back at a crime already committed; thrillers look forward to preventing a future crime.": "correct — exactly the contrast in the passage.",
 "Mysteries focus on romance; thrillers focus on technology.": "wrong — romance and technology belong to other genres.",
 "Both genres are concerned with romance and happy endings.": "wrong — that describes the romance novel.",
 "Thrillers always feature aliens and futuristic settings, mysteries do not.": "wrong — aliens and futuristic worlds belong to science fiction."},
r"Mystery = whodunit (past); thriller = race to stop it (future).")
