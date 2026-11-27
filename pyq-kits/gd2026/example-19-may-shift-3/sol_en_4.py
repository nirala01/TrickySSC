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

L(61, r"""-> A "squib" is a small firework; a damp one fails to go off with a bang and only fizzles.
-> So "a damp squib" is something that was expected to be exciting or impressive but turns out to be a disappointment.
-> Example: "The much-hyped final turned out to be a damp squib." """,
{"Someone or something that is pleasing": "wrong — this is almost the opposite meaning.",
 "Someone who has been dead": "wrong — a literal misreading of “damp”; the idiom has nothing to do with death.",
 "Someone who has been sick": "wrong — another literal misreading; it is not about illness.",
 "Someone or something that disappoints": "correct — an event or thing that fails to meet expectations."},
r"Damp firework = no bang = disappointment.")
L(62, r"""-> "Compel" means to make someone do something by using force, pressure or authority.
-> Its closest synonym is "force" (also oblige, coerce).
-> Example: "Heavy rain compelled us to cancel the match." """,
{"Invite": "wrong — to ask politely; there is no pressure.",
 "Force": "correct — same meaning as compel.",
 "Refuse": "wrong — to say no; close to an opposite idea.",
 "Encourage": "wrong — to give support or confidence, not to force."},
r"Compel = force (com-pel: “drive together”).")
L(63, r"""-> The four underlined words are experts, pandemic, zoonotick and transmitted.
-> A zoonotic disease is one that spreads from animals to humans; the adjective ends in "-ic", like "pandemic", not "-ick".
-> So "zoonotick" is the misspelt word; the correct form is "zoonotic".""",
{"experts": "correctly spelt.",
 "zoonotick": "misspelt — the correct spelling is “zoonotic”.",
 "pandemic": "correctly spelt.",
 "transmitted": "correctly spelt — the t is doubled before -ed because the stress falls on “-mit”."},
r"Adjectives end in -ic (zoonotic, pandemic), never -ick.")
L(64, r"""-> "Rambunctious" means noisy, energetic and hard to control.
-> It has a "c" after the "n": ram-bunc-tious; "Rambuntious" drops this c.
-> The other three words are spelt correctly.""",
{"Rambuntious": "misspelt — the correct spelling is “rambunctious”.",
 "Reconciliation": "correctly spelt — restoring friendly relations.",
 "Remuneration": "correctly spelt — payment for work (not “renumeration”).",
 "Repercussion": "correctly spelt — an unintended result of an action."},
r"Ram-BUNC-tious: keep the c.")
L(65, r"""-> "Persuade" means to make someone agree to do something by reasoning with them.
-> Its antonym is "dissuade" — to persuade someone NOT to do something.
-> Example: "Her friends dissuaded her from quitting the course." """,
{"convince": "wrong — a synonym of persuade.",
 "Dissuade": "correct — the opposite of persuade.",
 "Urge": "wrong — to try hard to persuade; similar meaning.",
 "Influence": "wrong — to affect someone's choice; close in meaning, not opposite."},
r"Per-suade = talk into; dis-suade = talk out of.")
L(66, r"""-> The sentence needs a verb meaning "to cut the wool off" a sheep.
-> "Shear" is that verb (shear, sheared, shorn); "sheer" sounds the same but means pure, complete or very steep.
-> So the farmer used a sharp tool to shear the sheep.""",
{"shear": "correct — to cut off the wool of a sheep.",
 "sheer": "wrong — a homophone meaning complete (sheer luck) or very steep (a sheer cliff).",
 "seer": "wrong — a person who can see the future, a prophet.",
 "seal": "wrong — to close tightly, or a sea animal."},
r"Shear the sheep (cut wool); sheer = pure/steep.")
L(67, r"""-> A "travesty" is a false, absurd or distorted copy of something, usually of something serious.
-> Example: "The trial was a travesty of justice."
-> The other words describe quite different ideas.""",
{"Travesty": "correct — a false, absurd or distorted representation.",
 "Solipsism": "wrong — the belief that only one's own mind is sure to exist; extreme self-centredness.",
 "Prevarication": "wrong — avoiding the truth by speaking evasively.",
 "Quiescence": "wrong — a state of being quiet, still or inactive."},
r"Travesty of justice = a mockery of it.")
L(68, r"""-> The active sentence is in the present continuous tense: "are decorating".
-> Its passive form uses is/am/are + being + past participle: the singular subject "the auditorium" takes "is being decorated".
-> So the passive is: "The auditorium is being decorated by the students for the function." """,
{"The auditorium is decorating": "wrong — active form of the verb; it says the auditorium is doing the decorating.",
 "The auditorium is been decorated": "wrong — “is been” is ungrammatical; “being” is needed.",
 "The auditorium is being decorated": "correct — is + being + past participle keeps the continuous tense.",
 "The auditorium is decorated": "wrong — this is simple present passive; the continuous sense is lost."},
r"Present continuous passive = is/are + being + V3.")
L(69, r"""-> The active sentence is in the present perfect tense: "has visited".
-> Its passive form is has/have + been + past participle; "almost every museum" is singular, so "has been visited".
-> So the passive is: "Almost every museum in the city has been visited by her." """,
{"Almost every museum in the city has been": "correct — has + been + V3 keeps the present perfect.",
 "Almost every museum in the city is": "wrong — simple present passive; the tense changes.",
 "Almost every museum in the city will": "wrong — future passive; the tense changes.",
 "Almost every museum in the city had": "wrong — past perfect passive; the tense changes."},
r"Present perfect passive = has/have + been + V3.")
L(70, r"""-> The fixed phrase is "with a view to" + -ing form, meaning "with the aim of".
-> "With a view of" is wrong, so the underlined part needs improvement.
-> "Between" is right for two countries, and "relations" (plural) should stay as it is.""",
{"with a view for promoting": "wrong — “with a view for” is not idiomatic.",
 "with a view to promoting": "correct — the standard phrase “with a view to + -ing”.",
 "with a view towards promoting": "wrong — “towards” is not used here, and “among” is wrong for two countries.",
 "No improvement required": "wrong — “with a view of” is an error."},
r"With a view TO doing something.")
L(71, r"""-> After a passive-type adjective like "terrified", the cause is introduced with "by" (or "of" for a general fear).
-> "Terrified by the roaring of a tiger" means the roaring caused the fear.
-> The other prepositions do not go with "terrified" here.""",
{"by": "correct — names the cause: terrified by the roaring.",
 "for": "wrong — “terrified for” means afraid on someone else's behalf, not of a sound.",
 "in": "wrong — “in” shows position, not cause.",
 "on": "wrong — “on” shows a surface or topic, not cause."},
r"Frightened/terrified BY a sound; afraid OF something.")
L(72, r"""-> S1 describes winter in the garden: Snow and Frost have covered everything.
-> D follows: "Then they invited the North Wind … and he came." C describes him ("He was wrapped in furs, and he roared …"). In B, "he" (the North Wind) says they must invite the Hail. A ends it: "So, the Hail came." S2 then describes the Hail rattling on the roof.
-> So the order is D, C, B, A.""",
{"DBCA": "wrong — B's “he” would come before C introduces the North Wind's behaviour.",
 "CABD": "wrong — C cannot start; “He” has no one to refer to yet.",
 "ABCD": "wrong — the Hail cannot arrive before he is invited.",
 "DCBA": "correct — invitation → description → plan to invite the Hail → Hail arrives."},
r"Invite North Wind (D) → describe him (C) → he invites Hail (B) → Hail comes (A).")
L(73, r"""-> S1 says Semyon's regiment was once on the firing line. B gives the setting: a week of skirmishing with the Turks across a deep ravine with steady crossfire.
-> A tells his job: thrice daily he carried the samovar and meals to the ravine. C describes the danger on the way (bullets humming about him), and D his reaction (terrified, but he kept on). S2 then says the officers were pleased with him.
-> So the order is B, A, C, D.""",
{"BACD": "correct — setting → his duty → the danger → his courage.",
 "ACBD": "wrong — the ravine and crossfire must be set up (B) before A.",
 "DCBA": "wrong — his fear (D) cannot come before the danger is described.",
 "CBDA": "wrong — “him” in C has no context without A."},
r"Setting (B) → duty (A) → danger (C) → courage (D).")
L(74, r"""-> With "neither … nor", the verb agrees with the subject nearer to it (the proximity rule).
-> The nearer subject is "his assistants" (plural), so the verb must be "were", not "was".
-> So "were able to attend the conference" is correct.""",
{"is able to attend": "wrong — singular and present tense; the sentence is in the past.",
 "was able to attended": "wrong — the agreement error stays, and “to attended” is wrong (to + base verb).",
 "were able to attend": "correct — plural verb to agree with “assistants”.",
 "No improvement required": "wrong — “was” does not agree with the plural “assistants”."},
r"Neither A nor B → verb agrees with B (assistants → were).")
L(75, r"""-> "Irregardless" is a non-standard word, a mix of "irrespective" and "regardless"; it is avoided in correct English.
-> The standard expression is "regardless of" (= without being stopped by), so the underlined part needs improvement.
-> The rest of the phrase, "the heavy rain and the muddy trails", is correct and should stay.""",
{"Irregardless of the heavy reins": "wrong — keeps “irregardless” and adds new errors (reins, trains).",
 "Regardless of the heavy rain": "correct — the standard word with the right nouns.",
 "Regardless of the heavenly rains": "wrong — “heavenly” and “mighty” change the meaning.",
 "No improvement required": "wrong — “irregardless” is non-standard."},
r"Say “regardless of”, never “irregardless”.")
L(76, r"""-> The passage opens by saying that sociological criticism regards a literary work as a product of the social factors and ideologies of its time.
-> It adds that a work is examined in its social context and that literature is "not created in a vacuum".
-> So its main focus is the literary work as a product of social factors.""",
{"Literary work as a product": "correct — stated in the second sentence of the passage.",
 "Literary work as an isolated": "wrong — the passage says literature is not created in a vacuum.",
 "Literary work as a record": "wrong — the passage studies the social context, not the author's private feelings.",
 "Literary work as a purely": "wrong — language structure is not discussed at all."},
r"Sociological criticism = literature + society.")
L(77, r"""-> The passage says that Hippolyte Adolphe Taine, a French thinker, pronounced that literature is extremely influenced by the moment, the race and the milieu.
-> Karl Marx is mentioned only for literature's role in social and economic revolution.
-> So the answer is Taine.""",
{"Karl Marx": "wrong — he linked literature to economic factors and revolution.",
 "Hippolyte Adolphe Taine": "correct — the French thinker named for “moment, race and milieu”.",
 "Friedrich Engels": "wrong — not mentioned in the passage.",
 "Matthew Arnold": "wrong — not mentioned in the passage."},
r"Moment–race–milieu = Taine.")
L(78, r"""-> The passage says Karl Marx sees the value of literature in promoting social and economic revolution.
-> It adds that literature can help overthrow the dominant capitalist ideology.
-> So, for Marx, literature can promote social and economic revolution.""",
{"Reinforcing capitalist ideology": "wrong — the opposite; literature can help overthrow it.",
 "Eliminating all forms of art": "wrong — never suggested.",
 "Promoting social and economic revolution": "correct — stated directly.",
 "Ignoring class struggles": "wrong — Marx's view is built on class struggle."},
r"Marx → literature as a tool for revolution.")
L(79, r"""-> The passage lists three basic factors in the author–society relation: the author's social status, the social content of the work (its values) and the role of the audience.
-> The author's psychological health is not one of them.
-> So it is the one that is NOT a factor.""",
{"Author's social status": "wrong — it is the first factor listed.",
 "Social content of the work": "wrong — it is the second factor listed.",
 "Role of the audience": "wrong — it is the third factor listed.",
 "Author's psychological health": "correct — not mentioned in the passage."},
r"Three factors: status, content, audience.")
L(80, r"""-> The passage says literature is not created in a vacuum, because the relation between the author and society is always at play.
-> Earlier it says that literary works are products of the times in which they are written, i.e. of social and historical conditions.
-> So it is shaped by social and historical conditions.""",
{"Literature is independent": "wrong — the opposite of the passage's view.",
 "Literature is shaped by social and historical": "correct — matches “products of the times in which they are written”.",
 "Literature ignores cultural": "wrong — the passage stresses social and economic factors.",
 "Literature exists only for aesthetic": "wrong — the passage stresses social purpose and effects."},
r"Not in a vacuum = shaped by society and history.")
