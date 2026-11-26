from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “Walk the talk” means to do what you have said you would do — to match actions with words.
-> Completed sentence: Politicians ought to walk the talk to retain their dignity and popularity.""",
{"talk the walk": "the words are reversed; this is not the standard idiom.",
 "talk the wall": "not an idiom; it has no accepted meaning.",
 "walk the talk": "correct — it means acting on one's promises.",
 "wake the talk": "not an idiom; “wake” makes no sense here."},
r"Walk the talk = do what you say.")
L(62, r"""-> “A viper in the bosom” is a person who is treated kindly or trusted but then betrays that trust.
-> The sentence describes someone who ran away with all the speaker's belongings — a betrayal of trust.""",
{"snake in the orchestra": "not an idiom; it mixes up “snake in the grass”.",
 "cat on the lap": "suggests a pet or comfort, not treachery.",
 "viper in the bosom": "correct — an ungrateful person who betrays the one who helped him.",
 "mongoose in the manger": "not an idiom; it mixes up “dog in the manger” (a person who stops others from using what he cannot use)."},
r"Viper in the bosom = a trusted traitor.")
L(63, r"""-> “Expectation” means a strong belief or hope that something will happen.
-> Example: Her expectation of a good result kept her calm.""",
{"Surprise": "something unexpected — the opposite idea.",
 "Disappointment": "the feeling when an expectation is not met — opposite in sense.",
 "Hope": "correct — the closest synonym of “expectation”.",
 "Memory": "relates to the past, while expectation looks to the future."},
r"Expectation ≈ hope ≈ anticipation.")
L(64, r"""-> “Eager” means wanting to do or have something very much; full of keen interest.
-> Example: The students were eager to start the new project.""",
{"Enthusiastic": "correct — the closest synonym of “eager”.",
 "Reluctant": "unwilling — an antonym.",
 "Bored": "lacking interest — opposite in sense.",
 "Careless": "not taking care; unrelated to eagerness."},
r"Eager ≈ keen ≈ enthusiastic.")
L(65, r"""-> The correct spelling is “xerography” — the dry copying process used in photocopiers.
-> It comes from Greek “xeros” (dry) + “graphy” (writing), so the letters after “xero” are “graphy”, not “griphy”.""",
{"xenophobic": "spelt correctly — fearing or disliking foreigners.",
 "xylophone": "spelt correctly — a musical instrument with wooden bars.",
 "xerogriphy": "misspelt — the correct form is “xerography”.",
 "xenolithic": "spelt correctly — relating to a xenolith, a rock fragment enclosed in another rock."},
r"-graphy is always spelt g-r-a-p-h-y (photography, xerography).")
L(66, r"""-> “Perishable” means likely to decay or go bad quickly, like fresh fruit or milk.
-> Its opposite describes something that lasts a long time.""",
{"Durable": "correct — long-lasting, the opposite of perishable.",
 "Soft": "describes texture, not how long something lasts.",
 "Edible": "fit to be eaten; perishable foods are often edible, so it is not an opposite.",
 "Breakable": "easily broken — close to fragile, not an antonym of perishable."},
r"Perishable ↔ durable / lasting.")
L(67, r"""-> In film-making, a sequence of shots edited together to show a story, passage of time or idea is called a montage.
-> Example: A training montage shows weeks of practice in one minute.""",
{"Montage": "correct — a series of shots put together to narrate something.",
 "Trailer": "a short advertisement for a film, shown before it is released.",
 "Preview": "an early showing or look at something before its release.",
 "Flashback": "a scene that goes back to an earlier time in the story."},
r"Montage = shots stitched together to tell a story.")
L(68, r"""-> A person who can use both hands equally well is “ambidextrous”.
-> “Ambi” means both, and “dexter” means right hand (skilful).""",
{"Ambidextrous": "correct — able to use both hands well.",
 "Ambivert": "a person with both introvert and extrovert traits.",
 "Ambivalent": "having mixed or opposite feelings about something.",
 "Divergent": "moving apart or differing from each other."},
r"Ambi = both; dexter = hand skill.")
L(69, r"""-> “In keeping with” means in harmony with or consistent with.
-> Completed sentence: In keeping with our tradition, we should continue to celebrate the different festivals of Odisha.""",
{"Because of": "gives a reason; “because of our tradition, we should continue” is less natural than showing harmony with tradition.",
 "As far as": "needs a following clause such as “as far as … is concerned”.",
 "So as to": "must be followed by a verb (so as to celebrate), not a noun phrase.",
 "In keeping with": "correct — it means in line with our tradition."},
r"In keeping with = consistent with.")
L(70, r"""-> The sentence is a future-tense question: Will + subject + verb?
-> Its passive form is Will + subject + be + past participle: Will the new bridge be opened for traffic next week?""",
{"Will the new bridge be opened for traffic next week?": "correct — keeps the future tense with “be opened”.",
 "Is the new bridge opened for traffic next week?": "changes the tense to the present.",
 "Has the new bridge been opened for traffic next week?": "present perfect does not go with “next week”.",
 "Was the new bridge opened for traffic next week?": "past tense clashes with “next week”."},
r"Future passive: will + be + V3.")
L(71, r"""-> “Is … provided” is the simple present passive; its active form uses do/does + base verb.
-> The doer “the mentors” becomes the subject: Do the mentors provide proper guidance to all newly admitted students?""",
{"Do the mentors provide proper guidance to all newly admitted students?": "correct — simple present, plural subject takes “Do”.",
 "Did the mentors provide proper guidance to all newly admitted students?": "changes the tense to the past.",
 "Have the mentors provided proper guidance to all newly admitted students?": "changes the tense to the present perfect.",
 "Will the mentors provide proper guidance to all newly admitted students?": "changes the tense to the future."},
r"Is/Are + V3 (passive) → Do/Does + V1 (active).")
L(72, r"""-> “For” is used to show a period of time: for the summer, for a week.
-> Completed sentence: The politician is going to his rural estate for the summer.""",
{"for": "correct — shows the length of the stay.",
 "of": "shows belonging, not a period of time.",
 "since": "needs a starting point and a perfect tense (since May).",
 "from": "shows a starting point and needs “to/till”."},
r"For + period of time; since + point of time.")
L(73, r"""-> The adjective “conducive” always takes the preposition “to”: conducive to something.
-> So the underlined part should read “conducive to innovation and inclusivity”, keeping the two nouns parallel.""",
{"conducive to innovation and inclusivity": "correct — right preposition and two parallel nouns.",
 "conducive of innovations with inclusiveness": "keeps the wrong preposition “of” and changes the meaning with “with”.",
 "conducive to innovate and inclusivity": "mixes a verb (innovate) with a noun (inclusivity), breaking parallelism.",
 "No improvement required": "wrong — “conducive of” is incorrect."},
r"Conducive TO, not conducive of.")
L(74, r"""-> S1 sets the scene: night has fallen and it is snowing.
-> A continues the snow picture and introduces Elliot; C then moves to his feelings (his heart leaped up); D explains why (he had run away from a dream and found possibility); B sums up the feeling (a promise), which leads to S2, where he starts walking.""",
{"CBDA": "starts with Elliot's heart before he is introduced in A.",
 "ACDB": "correct — scene (A) → feeling (C) → reason (D) → result (B).",
 "BDAC": "opens with “He felt…” before any person is named.",
 "DABC": "puts the reason (D) before the scene and the feeling."},
r"Scene first, then feeling, reason and conclusion.")
L(75, r"""-> The possessive pronoun is “theirs”, with no apostrophe (like ours, yours, hers).
-> A comparison of two things uses the comparative “more sustainable … than”.""",
{"more sustainable than their": "“their” must be followed by a noun; “theirs” is needed.",
 "more sustainable than theirs": "correct — comparative degree with the correct possessive pronoun.",
 "most sustainable than theirs'": "“most … than” is wrong and “theirs'” is not a word.",
 "No improvement required": "wrong — “their's” is incorrect."},
r"Possessive pronouns never take an apostrophe: theirs, yours, its.")
L(76, r"""-> The blank needs a verb meaning “to set off” or “cause” asthma symptoms.
-> Dust, pollen and pollution are called triggers because they trigger symptoms.""",
{"relieve": "means to ease — the opposite of what triggers do.",
 "trigger": "correct — triggers set off asthma symptoms.",
 "prevent": "means to stop from happening — opposite in sense.",
 "treat": "means to give medical care, not what dust or pollen do."},
r"Triggers trigger symptoms.")
L(77, r"""-> The sentence says people should keep track of their ___ triggers and avoid them.
-> You can only keep track of and avoid triggers that you already know, so the word is “known”.""",
{"immediate": "means happening at once; it does not describe triggers one can track.",
 "known": "correct — known triggers can be listed and avoided.",
 "unknown": "a person cannot keep track of or avoid triggers he does not know.",
 "knowingly": "an adverb; the blank needs an adjective before “triggers”."},
r"An adjective is needed before a noun: known triggers.")
L(78, r"""-> The blank needs an intensifying adverb before the adjective “essential”.
-> “Very essential” is the form the question expects: early diagnosis and management are very essential.""",
{"more": "“more essential” needs a comparison with “than”.",
 "very": "correct — an intensifier placed before the adjective.",
 "much": "“much” is used before comparatives (much better), not before “essential”.",
 "too": "means more than needed, which gives the wrong sense."},
r"Very + adjective; much + comparative.")
L(79, r"""-> The blank describes the serious results of a lack of awareness.
-> “Life-threatening” means dangerous enough to cause death, which fits “serious consequences”.""",
{"recurrent": "means happening again and again; it does not mean serious.",
 "sporadic": "means happening now and then.",
 "rare": "means not common; it lessens the seriousness.",
 "life-threatening": "correct — it expresses grave consequences."},
r"Serious consequences → life-threatening.")
L(80, r"""-> The passage opens by calling asthma a chronic respiratory condition.
-> “Chronic” means long-lasting, which matches “requires long-term care and vigilance”.""",
{"chronic": "correct — long-lasting.",
 "acute": "means sudden and short-lived — the opposite.",
 "temporary": "means lasting only for a short time.",
 "preventable": "means it can be stopped from happening; it does not describe duration."},
r"Chronic = long-term; acute = sudden.")
