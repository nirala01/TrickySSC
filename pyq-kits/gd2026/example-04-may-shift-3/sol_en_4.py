from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “A cut above” is an idiom used to praise someone or something as clearly better than others of the same kind.
-> Example: As a speaker, she is a cut above the rest.
-> So the meaning is “noticeably superior to others within the same category”.""",
{"Suited to or capable of doing some activity or task": "this is the meaning of “cut out for”, not “a cut above”.",
 "To cause a lot of damage or suffering in a specific area or population.": "this describes “wreak havoc”.",
 "Noticeably superior to others within the same category": "correct — “a cut above” = better than the others.",
 "To garner attention": "this is “catch the eye” / “steal the limelight”."},
r"A cut above = one level higher than the rest.")
L(62, r"""-> “Until the wheels fall off” means to keep going with something until it is no longer possible to continue.
-> It comes from driving a vehicle until it breaks down completely.
-> Example: We will keep fighting for this cause until the wheels fall off.""",
{"To use something until it is destroyed": "too literal — the idiom is about continuing an activity, not destroying an object.",
 "Play a toy till it is broken": "a literal, childish reading — not the idiom's sense.",
 "Do until one is exhausted": "close, but the idiom is about the activity becoming impossible, not just tiredness.",
 "Until it is no longer possible to continue with some activity or pursuit": "correct — the accepted meaning."},
r"Wheels fall off → the vehicle (activity) cannot go on any more.")
L(63, r"""-> “Fortunate” means lucky, having good things happen to you.
-> Example: We were fortunate to get the last two tickets.
-> A synonym should also mean lucky or blessed.""",
{"Unlucky": "the opposite (antonym) of fortunate.",
 "Favoured": "correct — favoured by luck or fortune, i.e. lucky.",
 "Sad": "a feeling of unhappiness — unrelated.",
 "Common": "ordinary — unrelated."},
r"Fortunate ≈ lucky ≈ favoured; opposite = unlucky.")
L(64, r"""-> We must find the word with the wrong spelling.
-> The correct spelling is “treacherous” (t-r-e-a-c-h-e-r-o-u-s), meaning disloyal or dangerous.
-> The option adds an extra “a” before “-rous”.""",
{"Treachearous": "misspelt — the correct form is “treacherous”.",
 "Transcendent": "correct spelling — going beyond ordinary limits.",
 "Triumphant": "correct spelling — having won a victory.",
 "Transgression": "correct spelling — an act that breaks a law or rule."},
r"Treacher + ous → treacherous (no second “a”).")
L(65, r"""-> We must find the word with the wrong spelling.
-> The correct spelling is “tutelage” (one “t” in the middle, one “l”), meaning protection or guidance by a teacher or guardian.
-> The option doubles the “t” and puts the vowels in the wrong order.""",
{"Territorial": "correct spelling — relating to territory.",
 "Tenacious": "correct spelling — holding firmly, determined.",
 "Tuttelage": "misspelt — the correct form is “tutelage”.",
 "Tranquillity": "correct (British) spelling — calmness; “tranquility” is the American form."},
r"Tutelage comes from “tutor” — keep a single “t”.")
L(66, r"""-> “Aching” means having a continuous dull pain.
-> Example: My legs were aching after the long march.
-> The antonym must mean free from pain.""",
{"sore": "painful — a synonym, not an antonym.",
 "Hurting": "feeling pain — a synonym.",
 "Painless": "correct — without pain, the opposite of aching.",
 "Throbbing": "beating with pain — a synonym."},
r"Aching ↔ painless.")
L(67, r"""-> The phrase means being excluded or shut out from a society or group.
-> “Ostracism” is exactly this — the act of excluding someone from a group or society.
-> Example: He faced ostracism after the scandal.""",
{"Dichotomy": "a division into two opposite parts.",
 "Ostracism": "correct — exclusion from a society or group.",
 "Abnegation": "giving up or denying oneself something (self-denial).",
 "Solipsism": "the belief that only one's own mind is sure to exist."},
r"Ostracise = to shut someone out of a group.")
L(68, r"""-> “On” is used before a gerund or noun to mean “immediately after / at the moment of”.
-> “On hearing the news, Mrs. White fell to the ground” = as soon as she heard the news.
-> The preposition begins the sentence, so it is written “On” with a capital letter.""",
{"In": "“in hearing” does not give the sense of “as soon as”.",
 "on": "correct — “On hearing the news” = immediately after hearing it.",
 "Under": "shows position below — does not fit.",
 "For": "shows purpose or duration — does not fit."},
r"On + -ing = immediately after doing it (On reaching home…).")
L(69, r"""-> The given sentence is a passive question in the past perfect tense: Had + object + been + V3 + by + subject?
-> In the active voice it becomes: Had + subject + V3 + object?
-> So: “Had the software team corrected the technical errors before the product launch?” — the tense stays past perfect.""",
{"Did the software team correct the technical errors before the product launch?": "wrong tense — this is simple past, not past perfect.",
 "Had the software team corrected the technical errors before the product launch?": "correct — same tense (past perfect), subject and object exchanged.",
 "Has the software team corrected the technical errors before the product launch?": "wrong tense — present perfect.",
 "Was the software team correcting the technical errors before the product launch?": "wrong tense — past continuous."},
r"Had been + V3 (passive) → Had + V3 (active).")
L(70, r"""-> “The injured man must be taken to the hospital at once” is a passive sentence that expresses an urgent order or duty.
-> When a passive sentence states a command, its active form is an imperative sentence beginning with the main verb.
-> So the active form is “Take the injured man to the hospital at once.”""",
{"You must be taken the injured man to the hospital at once.": "grammatically wrong — it mixes active and passive (“must be taken” with an object).",
 "The hospital must take the injured man at once.": "changes the meaning — the hospital is not the doer.",
 "Take the injured man to the hospital at once.": "correct — the imperative active form of the order.",
 "Let the injured man be taken to the hospital at once.": "this is still passive (the passive form of an imperative)."},
r"Passive order (must be + V3) → imperative active: V1 + object.")
L(71, r"""-> The adjective “responsible” takes the preposition “for” before the duty or task.
-> “Responsible to” is used for the person or authority one reports to (responsible to the manager).
-> Here the servants had a duty — keeping the house clean — so “responsible for” is correct.""",
{"to": "used for the person one answers to, not the task.",
 "for": "correct — responsible for a task or duty.",
 "about": "not used with “responsible”.",
 "on": "not used with “responsible”."},
r"Responsible FOR the work, responsible TO the boss.")
L(72, r"""-> The correct idiom is “hang by a thread”, meaning to be in a very dangerous or uncertain state.
-> The underlined part uses the wrong preposition “on”.
-> “The economy would hang by a thin thread” is correct; “thin” only adds emphasis.""",
{"hang by a thin thread": "correct — the idiom uses the preposition “by”.",
 "hang upon a thin thread": "wrong preposition — “upon” is not used in this idiom.",
 "hang with a thin thread": "wrong preposition.",
 "No improvement required": "wrong — “hang on a thread” is not the correct idiom."},
r"Hang BY a thread = in great danger.")
L(73, r"""-> S1: the narrator goes out again on his errand. D describes the weather that has changed (sleet and mist) — it must come before he fights the storm.
-> A: he wraps himself in his jacket and fights through the storm. C: he enters (the chapel) and finds a small congregation of sailors and widows.
-> B: a muffled silence reigns inside, broken by the storm's shrieks — this leads to S2 about the silent worshippers.""",
{"DABC": "puts B (silence inside) before C (entering) — he cannot hear the silence inside before he goes in.",
 "DBAC": "B (silence inside) before A (fighting the storm outside) breaks the order.",
 "DACB": "correct — weather (D) → fighting the storm (A) → entering (C) → silence inside (B) → silent worshippers (S2).",
 "DCAB": "C (entering) before A (on the way) breaks the time order."},
r"Outside → on the way → entering → inside. Look for the word that shows movement in (“Entering”).")
L(74, r"""-> S1: the widow had no blood relatives left. C (“One by one they had died”) explains why — it follows S1 directly.
-> A (“In her husband's family, too, …”) adds that she had no one there either. D (“But there was a little boy …”) introduces the exception.
-> B gives the boy's background (his aunt Kadambini brought him up), which leads to S2 about bringing up someone else's son.""",
{"ADCB": "A cannot come first — “too” needs the earlier idea of losing her own relatives (C).",
 "CADB": "correct — relatives died (C) → no one in husband's family too (A) → but a little boy (D) → aunt brought him up (B).",
 "BDCA": "B (“His mother…”) cannot open — “his” has no noun before it.",
 "DABC": "D begins with “But”, which needs a contrast already stated."},
r"Pronoun and linker clues: “too” after the first loss, “But” for the exception, “His” after the boy is named.")
L(75, r"""-> “None” is a pronoun meaning “not any”; it cannot be used before an adjective like “uncommon”.
-> The correct expression is “not uncommon”, a double negative that means “fairly common”.
-> So: “It's not uncommon to find street musicians playing in the park …”.""",
{"nothing uncommon to find street musicians": "wrong — “nothing” is a noun-pronoun; “It's nothing uncommon to find” is not idiomatic.",
 "not uncommon to find street musicians": "correct — “not uncommon” = quite common.",
 "never uncommon to find streets of musicians": "wrong — “never” changes the sense and “streets of musicians” changes the meaning.",
 "No improvement required": "wrong — “none uncommon” is ungrammatical."},
r"Use “not” before an adjective: not uncommon, not unusual.")
L(76, r"""-> The blank describes how Ananya checked into the guesthouse while she was “eager to rehearse her debate speech”.
-> Someone eager to start rehearsing would complete the check-in fast.
-> At this point she has not yet discovered any problem, so worry or nervousness does not fit yet.""",
{"calmly": "does not match her eagerness to get started.",
 "silently": "says nothing about her eagerness; no reason for silence is given.",
 "nervously": "her worry begins only later, after she finds the suitcase locked.",
 "quickly": "correct — eager to rehearse, she checked in quickly."},
r"Match the adverb with the mood just around the blank (eager → quickly).")
L(77, r"""-> The story is told in the past tense (she realized, the key was missing).
-> The suitcase was in a locked state at that moment, so a past passive form is needed: was + locked.
-> “her suitcase was locked, and the key was missing” — both clauses in the past.""",
{"is locked": "present tense — does not match the past narration.",
 "was locked": "correct — past tense, passive, matches “the key was missing”.",
 "has locked": "active present perfect — a suitcase cannot lock something.",
 "will be locked": "future — does not fit the past narration."},
r"Keep the tense of the narration: realized … was locked … was missing.")
L(78, r"""-> Ananya is speaking to herself, so the object refers back to the subject “she”.
-> When the subject and the object are the same person, a reflexive pronoun is used.
-> For a female subject the reflexive pronoun is “herself”.""",
{"him": "a male pronoun — wrong person.",
 "her": "would mean some other woman, not Ananya herself.",
 "itself": "used for things or animals, not a person.",
 "herself": "correct — reflexive pronoun for “she”."},
r"Talking to oneself → reflexive: myself, himself, herself.")
L(79, r"""-> To “pace” a room or hall means to walk up and down in it, usually because one is worried or impatient.
-> The passage says “her mind filled with worry” while she waited — a typical moment for pacing.
-> So “pacing” = walking back and forth repeatedly.""",
{"Running quickly in fear": "pacing is walking, not running, and she is worried, not afraid.",
 "Walking back and forth repeatedly": "correct — the meaning of pacing.",
 "Standing still with patience": "the opposite of what she was doing.",
 "Moving luggage around": "unrelated — her suitcase was locked."},
r"Pace up and down = walk to and fro restlessly.")
L(80, r"""-> The locksmith “examined” the lock — he looked at it carefully to find out how to open it.
-> A synonym must also mean to look at something closely and carefully.
-> “Inspected” has exactly this meaning.""",
{"Ignored": "paid no attention — the opposite.",
 "Avoided": "kept away from — the opposite.",
 "Neglected": "failed to take care of — the opposite.",
 "Inspected": "correct — looked at closely, the same as examined."},
r"Examine ≈ inspect ≈ scrutinise.")
