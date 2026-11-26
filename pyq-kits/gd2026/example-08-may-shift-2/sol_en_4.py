from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “Weather the storm” means to come safely through a difficult period or situation.
-> A ship that weathers a storm survives it without sinking — the idiom uses that picture.
-> Example: The small shop weathered the storm of the lockdown and is doing well again.""",
{"surpassed the storm": "wrong — not an idiom; “surpass” means to do better than.",
 "weathered the storm": "correct — survived the difficult period.",
 "crossed the boarder": "wrong — a literal phrase (and “boarder” means a lodger); it does not mean surviving hardship.",
 "immigrated here": "wrong — means came to live in another country; it does not mean surviving a famine."},
r"Weather the storm = survive the hard time.")
L(62, r"""-> The question asks for the MISSPELT underlined word.
-> The correct spelling is “resilience” — one l before -ience (the ability to recover quickly).
-> The other three underlined words are spelt correctly.""",
{"resillience": "correct — this is misspelt; it should be “resilience” (single l).",
 "targeted": "wrong — spelt correctly (single t before -ed).",
 "investments": "wrong — spelt correctly.",
 "diversification": "wrong — spelt correctly."},
r"reSILIence: one l, like “silly” with one l.")
L(63, r"""-> The question asks for the MISSPELT word.
-> “Endurance” ends in -ance (from endure), not -ence.
-> Providence, convergence and competence are all correct -ence words.""",
{"Providence": "wrong — spelt correctly (divine care or protection).",
 "Endurence": "correct — this is misspelt; it should be “Endurance”.",
 "Convergence": "wrong — spelt correctly (meeting at a point).",
 "Competence": "wrong — spelt correctly (ability to do something well)."},
r"Endure → endurANCE; converge → convergENCE.")
L(64, r"""-> “Remember” means to keep something in the mind or bring it back to mind.
-> Its opposite is “forget”.
-> Example: I always remember her birthday; my brother always forgets it.""",
{"Remind": "wrong — means to make someone remember; it is related in meaning, not opposite.",
 "Forget": "correct — the opposite of remember.",
 "Memorize": "wrong — means to learn by heart; close to remember.",
 "Recognize": "wrong — means to identify someone or something seen before."},
r"Remember ↔ Forget.")
L(65, r"""-> The blank needs a word meaning a religious or solemn ceremony.
-> That word is “rite”; the villagers lit candles to honour an ancient ceremony.
-> Right, rite, wright and write sound the same but differ in meaning (homonyms).""",
{"right": "wrong — means correct, or a just claim.",
 "rite": "correct — a ceremony or ritual.",
 "wright": "wrong — means a maker or builder (as in playwright, shipwright).",
 "write": "wrong — a verb meaning to put words on paper."},
r"Rite → ritual (both start with r-i-t).")
L(66, r"""-> Philology is the study of language in written historical sources.
-> It combines the study of literature, language history and the meaning of old texts.
-> It comes from Greek philo- (love) and logos (word).""",
{"Philology": "correct — study of language in historical texts.",
 "Linguistics": "wrong — the scientific study of language in general (sounds, grammar, meaning), not only written history.",
 "Anthropology": "wrong — the study of human societies and cultures.",
 "Etymology": "wrong — the study of the origin of individual words."},
r"Philo (love) + logy (words) = love of old written words.")
L(67, r"""-> The fixed phrase is “in difficulty”, meaning facing a problem.
-> “If you're in difficulty” = if you are having trouble.
-> Other examples: in trouble, in danger, in need.""",
{"for": "wrong — “for difficulty” is not used in this sense.",
 "in": "correct — “in difficulty”.",
 "from": "wrong — “from difficulty” would mean coming out of it.",
 "by": "wrong — “by difficulty” is not idiomatic."},
r"In trouble, in danger, in difficulty — use “in”.")
L(68, r"""-> The sentence is a question in the future perfect tense: Will + subject + have + past participle.
-> In the passive it becomes Will + object + have been + past participle + by + agent.
-> So: Will the machine have been repaired by the engineer before the shift starts?""",
{"Has the machine been repaired by the engineer before the shift starts?": "wrong — present perfect, not future perfect.",
 "Will the machine be repaired by the engineer before the shift starts?": "wrong — simple future; “have been” is missing.",
 "Will the machine have been repaired by the engineer before the shift starts?": "correct — future perfect passive.",
 "Was the machine repaired by the engineer before the shift starts?": "wrong — simple past."},
r"Will have + V3 → Will have been + V3.")
L(69, r"""-> The passive question is in the present perfect: Have + subject + been + past participle.
-> In the active, the agent (the office clerk) becomes the subject; a singular subject takes “has”.
-> So: Has the office clerk already located the missing documents?""",
{"Has the office clerk already located the missing documents?": "correct — present perfect active.",
 "Is the office clerk already locating the missing documents?": "wrong — present continuous.",
 "Did the office clerk already locate the missing documents?": "wrong — simple past.",
 "Will the office clerk already locate the missing documents?": "wrong — simple future."},
r"Have been + V3 (passive) → Has/Have + V3 (active).")
L(70, r"""-> The error is in “in arrival”.
-> The correct phrase is “on arrival” — meaning as soon as one arrives.
-> Correct sentence: The guest asked for a glass of water to drink on arrival.""",
{"The guest": "wrong — no error here.",
 "asked for a": "wrong — “ask for” is correct.",
 "glass of water to": "wrong — no error here.",
 "drink in arrival.": "correct — this part has the error; it should be “on arrival”."},
r"On arrival, on reaching, on hearing — use “on”.")
L(71, r"""-> “By dint of” means by means of, as a result of.
-> We achieved freedom as a result of the sacrifice and devotion of our freedom fighters.
-> Example: She topped the exam by dint of hard work.""",
{"along with": "wrong — means together with; it does not show the cause.",
 "by dint of": "correct — shows the means or cause.",
 "in accordance with": "wrong — means following a rule or law.",
 "in addition to": "wrong — means as well as."},
r"By dint of = because of (effort).")
L(72, r"""-> S1 says the air suddenly went out of his suit. The natural next step is what he did: C — he had enough air to twist a knob and seal the leak.
-> B then comments on it (“It had happened so quickly that he was not surprised”) and A follows from B (“Nothing surprised him anymore”).
-> D (“The air came back … now that the leak was sealed”) needs C before it, and leads into S2 about tightening the knob further. So the order is CBAD.""",
{"ACBD": "wrong — A cannot come first; it follows B's “not surprised”.",
 "BCAD": "wrong — B's comment needs the action (C) before it, and A then breaks the link between B and its idea.",
 "CBAD": "correct — action → reaction → general remark → result.",
 "DCAB": "wrong — D says the leak was sealed before C seals it."},
r"Find the action first, then the reaction to it.")
L(73, r"""-> S1 asks what the prince could do. B tells the problem: some of his men went over to the king's army.
-> A continues with “the rest”: with the rest of his men he shut himself up in the town and defended it.
-> D (“But one night … soldiers climbed over the walls”) turns the story, and C (“Before the alarm could be given, they were masters of the place”) follows before S2. So the order is BADC.""",
{"ADBC": "wrong — “the rest” in A needs B first.",
 "BADC": "correct — betrayal → defence → night attack → capture.",
 "DBAC": "wrong — the night attack cannot come before the defence.",
 "BACD": "wrong — C (“they were masters”) needs D's soldiers first."},
r"“The rest” needs the part already mentioned.")
L(74, r"""-> “Captivated the audience” and “drawing them into his every word” show the voice was pleasing.
-> “Discordant” means harsh and unpleasant, which cannot captivate anyone.
-> The fitting word is “mellifluous” (sweet and smooth to hear).""",
{"His discordant voice repelled the audience": "wrong — “repelled” clashes with “drawing them into his every word”.",
 "His mellifluous voice captivated the audience": "correct — a sweet voice draws the audience in.",
 "His mellifluous voice repelled the audience": "wrong — a sweet voice does not repel; it also clashes with the rest of the sentence.",
 "No improvement required": "wrong — “discordant” does not fit “captivated”."},
r"Mellifluous = honey-sweet sound (melli = honey).")
L(75, r"""-> “Irrevocable” means that cannot be changed, reversed or taken back.
-> Its synonym is “final”.
-> Example: The decision is irrevocable — it is final.""",
{"changeable": "wrong — the opposite meaning.",
 "Reversible": "wrong — the opposite meaning.",
 "Temporary": "wrong — means lasting a short time.",
 "Final": "correct — cannot be changed."},
r"Ir-revoke-able = cannot be revoked = final.")
L(76, r"""-> “It began in 2006” — the verb “began” is the simple past (a finished action at a past time).
-> “has now grown” — has + past participle is the present perfect (a past action with a result now).
-> So the sentence uses Simple Past + Present Perfect.""",
{"Simple Past + Present Perfect": "correct — began / has grown.",
 "Past Perfect + Present Continuous": "wrong — that would be “had begun … is growing”.",
 "Present Simple + Present Perfect": "wrong — “began” is past, not present.",
 "Future Simple + Past Continuous": "wrong — there is no will or was/were + -ing."},
r"Past time word (2006) → simple past; “has + V3” → present perfect.")
L(77, r"""-> The active sentence is in the simple present: “visitors attend the festival”.
-> In the passive the simple present becomes is/are + past participle: “the festival is attended by thousands of visitors”.
-> Moving “every year” to the front is fine; the tense must stay present.""",
{"The festival was attended by thousands of visitors from India and abroad every year.": "wrong — “was attended” is past tense.",
 "Thousands of visitors are attending the festival every year from India and abroad.": "wrong — still active, and changed to present continuous.",
 "Every year the festival is attended by thousands of visitors from India and abroad.": "correct — simple present passive.",
 "The festival had been attended by thousands of visitors from India and abroad every year.": "wrong — past perfect."},
r"Attend → is attended (simple present passive).")
L(78, r"""-> The passage says JLF has “democratized literature by making it accessible to all”.
-> To democratize something is to make it open and available to everyone.
-> So the synonym given in the passage itself is “made accessible”.""",
{"Restricted": "wrong — the opposite meaning.",
 "Made accessible": "correct — opened to all.",
 "Controlled": "wrong — opposite in spirit.",
 "Privatized": "wrong — means put in private hands."},
r"Democratize → for the people → accessible to all.")
L(79, r"""-> In the passage, literary festivals were once “exclusive events for scholars” — open only to a few.
-> The opposite of exclusive is “inclusive” — open to everyone.
-> JLF changed festivals from exclusive to inclusive.""",
{"private": "wrong — close to exclusive in meaning.",
 "elite": "wrong — a synonym of exclusive.",
 "limited": "wrong — close to exclusive in meaning.",
 "inclusive": "correct — the opposite of exclusive."},
r"EXclusive keeps out; INclusive lets in.")
L(80, r"""-> The passage says Jaipur remains the most iconic venue and that the setting of Diggi Palace, with its vibrant decorations, adds charm and grandeur to the intellectual exchange.
-> So the reason given is the charm of Diggi Palace.
-> The passage says nothing about the size of halls or where Nobel laureates live, and it says JLF has expanded to other cities.""",
{"Because it has the largest halls": "wrong — not mentioned.",
 "Because Diggi Palace adds charm and grandeur to the exchange of ideas": "correct — stated in the passage.",
 "Because most Nobel laureates live there": "wrong — not mentioned.",
 "Because other cities do not host it anymore": "wrong — the passage says JLF has expanded to cities across the world."},
r"Look for the sentence that follows “Jaipur remains its most iconic venue”.")
