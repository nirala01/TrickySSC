from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “A safe pair of hands” is someone who can be trusted to do a job well without making mistakes.
-> It began in cricket for a fielder who rarely drops a catch, and is now used for reliable people at work.
-> Example: The new captain is a safe pair of hands in a crisis.""",
{"A trustworthy and competent person": "correct — reliable and capable.",
 "One who has a lot of experience doing a particular task": "wrong — that is a veteran or old hand; the idiom stresses reliability, not years.",
 "Something of some value that is already acquired": "wrong — that is “a bird in the hand”.",
 "Additional help or assistance provided by another person": "wrong — that is “a helping hand”."},
r"Safe hands never drop the catch → a reliable person.")
L(62, r"""-> “Let sleeping dogs lie” means do not disturb a situation that is calm now, because stirring it up may cause trouble.
-> A sleeping dog is quiet; waking it may make it bite.
-> Example: The old quarrel was settled, so she decided to let sleeping dogs lie.""",
{"To experience a very deep and restful sleep; to sleep soundly": "wrong — that is “sleep like a log”.",
 "To leave a situation alone so as to avoid worsening it": "correct — avoid stirring up an old problem.",
 "To sleep easily and deeply, untroubled by one's conscience or satisfied with one's efforts": "wrong — that is “sleep the sleep of the just”.",
 "Refuse to rouse, provoke, or galvanize the enormous or unstoppable latent power of some person, group, or thing": "wrong — that is closer to “don't wake the sleeping giant”."},
r"Don't wake the dog → don't stir up trouble.")
L(63, r"""-> The question asks for the CORRECTLY spelt word.
-> The right spellings are gregarious (fond of company), garrulity (talkativeness), gluttony (over-eating) and gaffe (an embarrassing mistake).
-> Only “Gaffe” is written correctly among the options.""",
{"Gregarous": "wrong — the “i” is missing; correct: Gregarious.",
 "Garulity": "wrong — it needs double r; correct: Garrulity.",
 "Glutony": "wrong — it needs double t; correct: Gluttony.",
 "Gaffe": "correct — spelt correctly (double f, final e)."},
r"garRulity, gluTTony, gregarIous, gaFFe.")
L(64, r"""-> “Underneath” means directly below or under something.
-> Its closest synonym is “beneath”.
-> Example: The cat slept underneath (beneath) the table.""",
{"Above": "wrong — the opposite of underneath.",
 "Behind": "wrong — this means at the back of.",
 "Beneath": "correct — same meaning as underneath.",
 "Across": "wrong — this means from one side to the other."},
r"Under-neath = be-neath.")
L(65, r"""-> The question asks for the MISSPELT word.
-> A prosecutor (one who brings a criminal case in court) ends in -or, not -er.
-> Terminator, interloper and perpetrator are all spelt correctly.""",
{"Terminator": "wrong — spelt correctly.",
 "Prosecuter": "correct — this is misspelt; it should be “Prosecutor”.",
 "Interloper": "wrong — spelt correctly (an intruder).",
 "Perpetrator": "wrong — spelt correctly (one who commits a crime)."},
r"Legal agents end in -or: prosecutor, executor, solicitor.")
L(66, r"""-> “Extremism” means holding extreme political or religious views and pushing them hard.
-> Its antonym is “moderation” — avoiding extremes and keeping a balanced view.
-> The other three words are synonyms of extremism.""",
{"Radicalism": "wrong — a synonym (support for complete, extreme change).",
 "Zealotry": "wrong — a synonym (fanatical devotion to a cause).",
 "Fanaticism": "wrong — a synonym (excessive, unreasoning zeal).",
 "Moderation": "correct — the opposite of extremism."},
r"Extreme ↔ moderate.")
L(67, r"""-> A pantheist believes that God is everything and in everything, including nature.
-> “Pan” means all and “theos” means God.
-> The poet Wordsworth is often described as a pantheist for seeing God in nature.""",
{"Agnostic": "wrong — one who says we cannot know whether God exists.",
 "Pantheist": "correct — God is in everything, including nature.",
 "Polytheist": "wrong — one who believes in many gods.",
 "chiropodist": "wrong — a foot doctor (podiatrist)."},
r"Pan = all, theos = God → pantheist.")
L(68, r"""-> Active modal perfect: subject + must have + V3 + object. Passive: object + must have been + V3 (+ by agent).
-> “Somebody” is a vague agent, so “by somebody” is usually dropped in the passive.
-> Correct: The fire brigade must have been called.""",
{"The fire brigade must have to be called.": "wrong — “must have to be” changes the meaning to an obligation.",
 "The fire brigade must have been call by somebody.": "wrong — the past participle “called” is needed, not “call”.",
 "The fire brigade must have called by somebody.": "wrong — “been” is missing, so it is not passive.",
 "The fire brigade must have been called.": "correct — must have been + V3, vague agent dropped."},
r"must have + V3 → must have been + V3.")
L(69, r"""-> Active future: subject + will + V1 + object. Passive: object + will be + V3 + by agent.
-> “Sweets” becomes the subject, “distribute” becomes “will be distributed”, and “they” becomes “by them”.
-> Correct: Sweets will be distributed among the poor by them.""",
{"Sweets are to be distributed by them among the poor.": "wrong — “are to be” expresses a plan or duty, not the simple future.",
 "Sweets will be distribute among the poor by them.": "wrong — V3 “distributed” is needed.",
 "Sweets will be distributed among the poor by them.": "correct — will be + V3.",
 "Sweets will distributed among the poor by them.": "wrong — “be” is missing."},
r"will + V1 → will be + V3.")
L(70, r"""-> “Throw something to someone” means throwing it for them to catch; “throw something at someone” means aiming it to hit them.
-> Johnsy was angry and the sandals hurt the stranger, so she threw them AT him.
-> Correct: … that she threw her sandals at him, hurting him just above his right eyebrow.""",
{"Johnsy was so": "wrong — “so … that” is correct.",
 "angry with the": "wrong — “angry with” a person is correct.",
 "stranger that she threw her sandals to him": "correct — the error is here: “to him” should be “at him”.",
 "hurting just above his right eyebrow.": "wrong — no error in this part."},
r"Throw TO = to catch; throw AT = to hit.")
L(71, r"""-> “Affectionate” takes “with” (or “towards/to”) before the people one loves.
-> Example: She is very affectionate with her children.
-> Completed: My grandmother is affectionate with all our family members.""",
{"of": "wrong — “affectionate of” is not used.",
 "with": "correct — affectionate with someone.",
 "at": "wrong — “at” is not used after affectionate.",
 "by": "wrong — “by” shows the agent, not the people one loves."},
r"Affectionate with / towards a person.")
L(72, r"""-> “Put up with” means to tolerate or bear something unpleasant.
-> The NGO has been tolerating severe criticism for its methods, so the underlined phrase is correct.
-> Changing the particle changes the phrasal verb and spoils the meaning.""",
{"putting across with severe criticism": "wrong — “put across” means to communicate an idea; “with” does not follow it.",
 "putting out with severe criticism": "wrong — “put out” means to extinguish or publish.",
 "putting in with severe criticism": "wrong — “put in” means to install or submit.",
 "No improvement required": "correct — “putting up with” (tolerating) is right."},
r"Put up with = tolerate.")
L(73, r"""-> S1 says three years went by; B (“Three precious years.”) picks up “three years” at once.
-> Then each sister's state is described: A Carrie still taught school, D Eva kept house, C Stell was still the family beauty.
-> S2 about Emily's hair follows naturally after C, which also speaks of curls and looks. Order: B-A-D-C.""",
{"DBCA": "wrong — B must come right after S1.",
 "BACD": "wrong — C (curls and beauty) must lead into S2 about Emily's hair.",
 "BADC": "correct — B, A, D, C.",
 "ADBC": "wrong — B, which echoes S1, cannot be third."},
r"Echo first: 'three years' → 'Three precious years'.")
L(74, r"""-> S1 describes the tall, dried grass on either side; B continues with “These weeds”, which refers back to that grass.
-> D then moves to the river bank and the old waterline, and A describes the river itself, which bent so often you could never see far along it.
-> C “Only a mile or so” completes A, and S2 returns to the foliage. Order: B-D-A-C.""",
{"ABDC": "wrong — “These weeds” (B) must follow the grass in S1.",
 "CABD": "wrong — C completes A, so it cannot open.",
 "BDAC": "correct — B, D, A, C.",
 "DABC": "wrong — B (“These weeds”) must come right after S1."},
r"'These' points back: These weeds → the grass in S1.")
L(75, r"""-> “Will have the effect of increasing” is wordy; the simple verb “will increase” says the same thing.
-> It also matches the parallel verb in the sentence: exercise will increase … and help you feel refreshed.
-> Correct: Regular exercise will increase your energy levels and help you feel more refreshed.""",
{"will increase your energy levels": "correct — concise and parallel with “help”.",
 "will have the affect of increasing your energy levels": "wrong — “affect” is a verb; the noun is “effect”, and it stays wordy.",
 "will affect the increase of your energy levels": "wrong — awkward and changes the meaning.",
 "No improvement required": "wrong — the original is wordy and can be improved."},
r"Cut the padding: 'have the effect of increasing' → 'increase'.")
L(76, r"""-> The passage says poverty and unemployment are often blamed for creating feelings of hopelessness and desperation.
-> These feelings make young people open to extremist ideas.
-> So the link is the hopelessness and desperation they create.""",
{"They create feelings of hopelessness and desperation": "correct — stated in the second sentence.",
 "They reduce anger and resentment among young people": "wrong — the passage says they cause anger and resentment.",
 "They guarantee access to better education and jobs": "wrong — poverty limits opportunities.",
 "They eliminate the need for extremist organizations": "wrong — they help extremist groups recruit."},
r"Look for the sentence with 'often blamed for'.")
L(77, r"""-> The passage says poor economic conditions create limited opportunities and fewer options for gainful employment.
-> This leads to anger, despair and a sense of injustice — frustration that pushes youth towards extremism.
-> So they contribute by reducing opportunities and creating frustration.""",
{"By increasing options for gainful employment": "wrong — the passage says fewer options.",
 "By reducing opportunities and creating frustration": "correct — limited opportunities lead to despair.",
 "By promoting equality and social justice": "wrong — they create a sense of injustice.",
 "By discouraging extremist organizations from recruiting": "wrong — recruitment becomes easier."},
r"Poor economy → fewer opportunities → frustration.")
L(78, r"""-> The last sentence says extremist groups can more easily recruit young, educated people without jobs because of high unemployment and wider wealth gaps.
-> Unemployment and the wealth gap leave such youth frustrated, and that frustration makes them vulnerable.
-> Being attracted to extremist ideas is the RESULT of this vulnerability, not the factor behind it.""",
{"They have ample jobs to keep themselves busy": "wrong — they are unemployed.",
 "They may feel attracted towards extremist ideology": "wrong — this is the result, not the main factor that makes them vulnerable.",
 "They feel frustrated due to unemployment and wealth disparity": "correct — high unemployment and wider wealth gaps.",
 "They face different social and financial problems that can't be solved because of a lack of education": "wrong — the passage says even educated youth are recruited."},
r"Factor = cause (unemployment + wealth gap), not the effect.")
L(79, r"""-> The passage says individuals from higher-income groups are more likely to have a range of economic opportunities.
-> Because of this they are less likely to engage in extremist activities.
-> The reason given is economic opportunity and stability, nothing else.""",
{"They are less likely to feel marginalized by society.": "wrong — the passage does not speak of being marginalised.",
 "They are less frequently targeted by recruiters of extremist groups": "wrong — the passage says nothing about recruiters targeting them less.",
 "They enjoy more economic opportunities and stability.": "correct — a range of economic opportunities.",
 "Generally, they are better educated and more conscious about their social environments.": "wrong — education and awareness are not given as the reason."},
r"Answer only from the passage: 'range of economic opportunities'.")
L(80, r"""-> The passage says poverty and unemployment result in anger, resentment, despair and a sense of injustice.
-> It calls this a volatile (explosive) combination in the minds of young people.
-> That is what makes them dangerous.""",
{"They ensure peace and harmony in society.": "wrong — the opposite of the passage.",
 "They engender feelings of resentment, hopelessness, and injustice.": "correct — the volatile combination.",
 "They enjoy more economic opportunities and stability.": "wrong — this describes higher-income people, not poverty.",
 "Because they reduce the frustration and despair among the youth.": "wrong — they increase frustration and despair."},
r"'Volatile combination' = resentment + despair + injustice.")
