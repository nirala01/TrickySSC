from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “Throw in the towel” means to give up or admit defeat.
-> It comes from boxing, where a trainer throws a towel into the ring to stop the fight.
-> In the sentence, after studying the pattern and the difficulty level, Rahul gave up on the examination — so “threw in the towel” fits.""",
{"threw in the kerchief": "not an idiom — the fixed expression uses “towel”.",
 "threw in the gloves": "not the idiom; “hang up one's gloves” means to retire.",
 "threw in the pen": "not an idiom.",
 "threw in the towel": "correct — it means gave up."},
r"Boxing: towel in the ring = surrender = give up.")
L(62, r"""-> We must pick the correctly spelt word.
-> The correct spelling is “committee” — double m, double t, double e (c-o-m-m-i-t-t-e-e).
-> It means a group of people chosen to do a particular job.""",
{"Committie": "misspelt — ends in “-ie” instead of “-ee”.",
 "Commitee": "misspelt — only one “t”.",
 "Committee": "correct spelling.",
 "Comittee": "misspelt — only one “m”."},
r"Committee: double m, double t, double e.")
L(63, r"""-> We must pick the correctly spelt word.
-> “Rescind” (r-e-s-c-i-n-d) is correct; it means to cancel or withdraw officially (a law, an order or an offer).
-> Example: The government rescinded the controversial order.""",
{"Reproch": "misspelt — the correct form is “reproach”.",
 "Rescind": "correct spelling.",
 "Raucus": "misspelt — the correct form is “raucous” (harsh, noisy).",
 "Rebucke": "misspelt — the correct form is “rebuke”."},
r"Re-S-C-ind: the silent “c” after “s”, as in “scissors”.")
L(64, r"""-> “Agony” means extreme physical or mental pain or suffering.
-> In the sentence, he was in great pain after injuring his leg.
-> So the synonym is “pain”.""",
{"Joy": "the opposite — great happiness.",
 "Comfort": "the opposite — a state of ease, free from pain.",
 "Pain": "correct — agony is severe pain.",
 "Peace": "calmness; not related to suffering."},
r"Agony = severe pain.")
L(65, r"""-> “Reluctant” means unwilling or hesitant to do something.
-> Example: She was reluctant to leave her old school.
-> So the closest synonym is “unwilling”.""",
{"Eager": "the opposite — keen and wanting to do something.",
 "Unwilling": "correct — not ready or wanting to do something.",
 "Joyful": "means very happy; not related.",
 "Brave": "means courageous; not related."},
r"Reluctant = unwilling; opposite = eager.")
L(66, r"""-> “Bury” means to put something under the ground or to hide it from view.
-> Its antonym is a word meaning to uncover or bring into view.
-> “Expose” means to uncover or reveal, so it is the opposite.""",
{"Conceal": "a synonym — to hide.",
 "Hide": "a synonym — to keep out of sight.",
 "Expose": "correct — to uncover or reveal, the opposite of bury.",
 "Inter": "a synonym — to bury a dead body."},
r"Bury / conceal / hide / inter ↔ expose / unearth.")
L(67, r"""-> The art or technique of motion-picture (film) photography is “cinematography”.
-> The person who does it is a cinematographer.
-> It comes from “cinema” + “-graphy” (writing or recording).""",
{"Calligraphy": "the art of beautiful handwriting.",
 "Cinematography": "correct — the art of motion-picture photography.",
 "Lithography": "printing from a flat stone or metal plate.",
 "Photography": "taking still pictures, not motion pictures."},
r"Cinema (moving pictures) + graphy = cinematography.")
L(68, r"""-> The sentence is in the past continuous tense and is a question: Were + subject + verb-ing + object?
-> Passive of past continuous: was/were + being + past participle.
-> “The tank” is singular, so: “Was the tank being cleaned in the afternoon?” (the agent “by them” is usually dropped).""",
{"Was the tank been cleaned in the afternoon?": "wrong — “was … been” is not a valid form.",
 "Was the tank being cleaned in the afternoon?": "correct — was + being + cleaned keeps the past continuous.",
 "Were the tank being cleaned in the afternoon?": "wrong — singular “tank” needs “was”.",
 "Was the tank cleaned in the afternoon?": "wrong tense — this is simple past passive."},
r"Past continuous passive = was/were + being + V3.")
L(69, r"""-> The sentence is present continuous passive: is + being + trained.
-> In the active voice the doer comes first and the verb becomes is/am/are + verb-ing.
-> So: “A former Olympian is training the young athlete.”""",
{"A former Olympian trains the young athlete.": "wrong tense — simple present.",
 "A former Olympian is training the young athlete.": "correct — present continuous active.",
 "A former Olympian is being trained the young athlete.": "wrong — this is still passive and has no sense.",
 "A former Olympian is been training the young athlete.": "wrong — “is been” is not a valid form."},
r"is being + V3 (passive) → is + V-ing (active).")
L(70, r"""-> “On the way (from … to …)” means situated along the route between two places.
-> Arpita's house lies along the road from Sambalpur to Bargarh.
-> So the correct preposition is “on”.""",
{"by": "“by the way” means incidentally — a different meaning.",
 "at": "not used with “the way” in this sense.",
 "on": "correct — “on the way” = along the route.",
 "in": "“in the way” means blocking someone — a different meaning."},
r"On the way = en route; in the way = blocking; by the way = incidentally.")
L(71, r"""-> “Fraught” is always followed by the preposition “with”.
-> “Fraught with” means full of something bad (problems, danger, challenges).
-> The underlined part “fraught with numerous challenges” is already correct, so no improvement is needed.""",
{"fraught in numerous challenges": "wrong preposition.",
 "fraught of numerous challenges": "wrong preposition.",
 "fraught by numerous challenges": "wrong preposition.",
 "No improvement required": "correct — “fraught with” is the right usage."},
r"Fraught WITH (danger, problems, challenges).")
L(72, r"""-> The noun “dependence” (like the verb “depend”) takes the preposition “on” (or “upon”).
-> Example: India's dependence on imported oil.
-> So: “The old man's dependence on coffee is really surprising.”""",
{"in": "wrong preposition.",
 "with": "wrong preposition.",
 "on": "correct — dependence on.",
 "about": "wrong preposition."},
r"Depend / dependent / dependence → ON.")
L(73, r"""-> S1 sets the scene: the festival of spring. C follows, telling how crowds came out of the narrow lanes and alleys.
-> B then says “They” (the crowd) entered the sunshine outside the city gates and sped towards the fair; A describes how they travelled (walked, rode, carts).
-> D narrows down to one little boy, and S2 closes with the joyous morning. Order: C, B, A, D.""",
{"CBAD": "correct — crowd emerges, goes out to the fair, ways of travelling, then the boy.",
 "DABC": "wrong — D (one little boy) cannot open the description.",
 "ABDC": "wrong — A's “some walked …” needs the crowd from C first.",
 "CBDA": "wrong — A describes the whole crowd, so it must come before the focus shifts to the boy in D."},
r"General crowd first (C → B → A), then one person (D).")
L(74, r"""-> S1: Vladimir drove on but the wood never ended. C follows: he realised with horror he was in an unknown forest.
-> A (despair took hold of him) is his reaction, and B shows what he did — whipped the horse, which soon tired.
-> D (the trees thinned and he came out, but Jadrino was not seen) leads to S2 (it must now be midnight). Order: C, A, B, D.""",
{"ADBC": "wrong — despair needs the cause (C) before it.",
 "ABCD": "wrong — C (discovering the unknown forest) must come before A.",
 "CABD": "correct — realisation, despair, whipping the horse, coming out of the forest.",
 "CDAB": "wrong — D (leaving the forest) cannot come before his struggle in the forest (A, B)."},
r"Cause → feeling → action → result (C → A → B → D).")
L(75, r"""-> “Mistakes” is a countable plural noun, so it takes “fewer”, not “less” (“less” is for uncountable nouns like water or time).
-> The sentence compares with an earlier time, so “fewer” (comparative) is needed.
-> Correct: “She made fewer mistakes this time …”.""",
{"she made lesser mistakes this time": "wrong — “lesser” means less important, and it is not used for number.",
 "she made fewer mistakes this time": "correct — “fewer” with a countable plural noun.",
 "She made few mistakes this time": "wrong — “few” is not comparative; the sentence shows improvement over before.",
 "No improvement required": "wrong — “less mistakes” is incorrect."},
r"Fewer for things you can count (mistakes); less for things you cannot (water).")
L(76, r"""-> Blank A: “However, ___ social media landscape has changed …”
-> We mean the particular, known landscape of social media, so the definite article “the” is needed.
-> “The social media landscape has changed” is the natural phrase.""",
{"a": "wrong — refers to any one landscape, not the specific one.",
 "the": "correct — the definite article for the specific landscape.",
 "an": "wrong — used before a vowel sound; also indefinite.",
 "one": "wrong — makes no sense here."},
r"Specific, already known thing → “the”.")
L(77, r"""-> Blank B: “Friendster, an early social networking site, ___ the way for platforms …”
-> The passage tells of the past (Friendster's user base declined), and “pave the way” means to prepare the ground for something later.
-> So the simple past “paved” is needed.""",
{"pave": "wrong — base form; the subject is singular and the time is past.",
 "paves": "wrong — present tense; Friendster's role is in the past.",
 "paved": "correct — simple past: it prepared the ground for later platforms.",
 "are paving": "wrong — plural and present continuous."},
r"Past story → past tense: paved the way.")
L(78, r"""-> Blank C: “… leaving older apps ___.”
-> The apps are acted upon — people forgot them — so a past participle with passive sense is needed: “leave something forgotten”.
-> So “forgotten” fits.""",
{"forgotten": "correct — past participle: the apps were forgotten.",
 "forgetting": "wrong — would mean the apps themselves are forgetting.",
 "to forget": "wrong — gives the sense of purpose, which does not fit.",
 "forgot": "wrong — simple past cannot follow “leaving older apps” here."},
r"Leave + object + past participle (left forgotten).")
L(79, r"""-> “Reminisce” means to think or talk about pleasant past experiences with fondness.
-> In the passage, some people still remember the old platforms warmly.
-> So the meaning is “reflect fondly”.""",
{"Forget": "the opposite.",
 "Reflect fondly": "correct — to remember the past with pleasure.",
 "Ignore": "wrong — to pay no attention.",
 "Complain": "wrong — to express dissatisfaction."},
r"Reminisce = remember happily (reminiscence = a happy memory).")
L(80, r"""-> “Evolves” means changes or develops gradually over time.
-> The passage says old apps are replaced quickly by new ones, i.e. technology keeps changing.
-> So the closest meaning is “changes”.""",
{"Remains": "the opposite — stays the same.",
 "Slows": "wrong — evolving says nothing about slowing down.",
 "Changes": "correct — technology keeps changing.",
 "Repeat": "wrong — doing the same again; not change."},
r"Evolve = change gradually (evolution).")
