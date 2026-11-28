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

L(61, r"""-> The idiom “a flash in the pan” describes something or someone that shows sudden promise or success but fails to last.
-> It comes from old flintlock guns, in which the priming powder in the “pan” flashed brightly but did not fire the gun — a brief show with no result.
-> Example: "His first novel was a bestseller, but it proved a flash in the pan." """,
{"To abruptly": "wrong — this describes suddenly switching something on, like lights; it has nothing to do with the idiom.",
 "Someone or something": "correct — short-lived success or popularity, the exact meaning of the idiom.",
 "To look at": "wrong — this is the sense of “flash a glance”, not of this idiom.",
 "To be thought": "wrong — this is the sense of an idea that “flashes through one's mind”."},
r"Flash in the pan = bright for a moment, then gone.")
L(62, r"""-> “Expand” means to become larger or to make something larger in size, number or scope.
-> Its synonyms are enlarge, extend, increase and grow.
-> Example: "The company plans to expand its business to new cities." """,
{"Reduce": "wrong — an antonym; it means to make smaller.",
 "Enlarge": "correct — to make bigger, the same sense as expand.",
 "Hide": "wrong — to put out of sight; no link with size.",
 "Destroy": "wrong — to ruin completely; the opposite of building up."},
r"Expand = Enlarge (make bigger).")
L(63, r"""-> The misspelt word is “Serendepity”; the correct spelling is “Serendipity”, with an “i” in the middle: se-ren-DIP-i-ty.
-> Serendipity means the luck of finding something good by accident; the word was coined by Horace Walpole in 1754 from the Persian tale “The Three Princes of Serendip” (Serendip was an old name for Sri Lanka).
-> Example: "Meeting her old teacher at the station was pure serendipity." """,
{"Sanctimonious": "correctly spelt — it means making a show of being morally better than others.",
 "Scintillating": "correctly spelt — sparkling or brilliantly clever, with “sc” at the start and double “l”.",
 "Serendepity": "misspelt — it should be “Serendipity”, with “dip” not “dep”.",
 "Spontaneous": "correctly spelt — happening naturally without planning."},
r"Serendi-P-ity: remember “dip” (dip into luck).")
L(64, r"""-> To “encourage” someone is to give them support, confidence or hope to do something.
-> Its antonym should mean to take away confidence or hope, which is “dishearten” (also discourage or dispirit).
-> Example: "The repeated failures disheartened the team." """,
{"Inspire": "wrong — a synonym; it means to fill someone with the urge to do something.",
 "Praise": "wrong — to express approval; closer in meaning to encourage than opposite.",
 "Dishearten": "correct — to make someone lose confidence or hope, the opposite of encourage.",
 "Motivate": "wrong — a synonym; it means to give a reason or push to act."},
r"En-courage gives courage; Dis-hearten takes the heart away.")
L(65, r"""-> “Escape” means to get free from a place or from danger.
-> Its antonym should mean to catch or hold someone so that he cannot get away, which is “capture”.
-> Example: "The police managed to capture the thief before he could escape." """,
{"Liberation": "wrong — setting free; close in meaning to escape, not opposite.",
 "Breakout": "wrong — an escape, especially from a prison; a synonym.",
 "Capture": "correct — to seize or take prisoner, the opposite of escape.",
 "Flight": "wrong — the act of running away, so close to escape in meaning."},
r"Escape = get free; Capture = get caught.")
L(66, r"""-> To name the means of transport we use “by” without an article: by bus, by train, by air, by road.
-> “On” is used only with a particular vehicle (“on the bus”) or with fixed phrases such as “on foot”.
-> Correct sentence: "The teachers are going on a tour by bus." """,
{"on": "wrong — “on bus” is not used without an article; it would need “on the bus”.",
 "by": "correct — “by bus” is the standard phrase for the means of travel.",
 "in": "wrong — “in bus” is not used; we say “in a car” or “in a taxi” for small vehicles only.",
 "through": "wrong — “through” shows passing from one side to another, not the vehicle used."},
r"Means of transport takes “by” (by bus, by train, by air); “on foot” is the exception.")
L(67, r"""-> “Acumen” means the ability to make good judgements and quick decisions, especially in business or a particular field.
-> It comes from the Latin “acumen”, meaning sharpness; it is often used in phrases such as “business acumen” and “political acumen”.
-> Example: "Her financial acumen helped the firm grow." """,
{"Contrition": "wrong — a feeling of deep regret for having done wrong.",
 "Candor": "wrong — the quality of being open and honest in what one says.",
 "Acumen": "correct — a sharp ability to judge and decide quickly.",
 "Abnegation": "wrong — giving up or denying oneself something, such as comforts or beliefs."},
r"Acumen = sharp sense (acute) in judging and deciding.")
L(68, r"""-> The active sentence is in the simple present tense: “plays”.
-> The passive of the simple present is object + is/am/are + past participle + by + doer, so “plays” becomes “is played”.
-> Correct passive: "Classical music is played by the orchestra at the concert hall every weekend." """,
{"Classical music is played": "correct — simple present passive, the same tense as the active sentence.",
 "Classical music was played": "wrong — “was played” is simple past, so the tense changes.",
 "Classical music has been": "wrong — “has been played” is present perfect.",
 "Classical music is being": "wrong — “is being played” is present continuous."},
r"Simple present → is/are + V3.")
L(69, r"""-> The active question is in the present continuous tense: “Are you preparing …?”
-> The passive of the present continuous is is/am/are + being + past participle, and the object becomes the subject.
-> The object “a science quiz” is singular, so the helping verb is “is”: "Is a science quiz being prepared by you for the children?" """,
{"Was a science quiz": "wrong — “Was … being prepared” is past continuous.",
 "Are a science quiz": "wrong — the singular subject “a science quiz” cannot take “are”.",
 "Has a science quiz": "wrong — “Has … being prepared” mixes a perfect auxiliary with “being” and is ungrammatical.",
 "Is a science quiz": "correct — present continuous passive with a singular subject."},
r"Are + V-ing → Is/Are + being + V3 (agree with the new subject).")
L(70, r"""-> The passive sentence is in the past continuous tense: “were being painted”.
-> To change it to active, the doer “the workers” becomes the subject and the verb becomes was/were + V-ing, so “were being painted” becomes “were painting”.
-> Correct active sentence: "The workers were painting the gates all afternoon." """,
{"The workers painted": "wrong — “painted” is simple past; the continuous sense of “all afternoon” is lost.",
 "The workers had": "wrong — “had painted” is past perfect.",
 "The workers were painting": "correct — past continuous, the same tense as the passive.",
 "The workers will": "wrong — “will paint” is future."},
r"were being + V3 → were + V-ing.")
L(71, r"""-> After an adjective such as “proud”, the fixed preposition is “of”: proud of someone or something.
-> Similar fixed pairs are afraid of, fond of, jealous of and capable of.
-> Correct sentence: "The French are very proud of their valour." """,
{"of": "correct — “proud of” is the standard collocation.",
 "in": "wrong — we do not say “proud in”.",
 "at": "wrong — “at” goes with words like “good at” or “surprised at”.",
 "about": "wrong — “proud about” is not idiomatic; “proud of” is used."},
r"Proud OF, afraid OF, fond OF.")
L(72, r"""-> “Replete” takes the preposition “with”: replete with means full of, well supplied with.
-> The sentence is in the past tense (“was found”), so the clause must use “could have” in place of “can have”.
-> “That” is the better relative word for a defining clause: "…replete with loopholes that could have far-reaching consequences." """,
{"replete of": "wrong — “replete of” uses the wrong preposition.",
 "replete with loopholes that could": "correct — the right preposition and the correct past-tense form.",
 "replete in": "wrong — “replete in” uses the wrong preposition and “can have” does not match the past tense.",
 "No improvement": "wrong — “can have” does not agree with “was found”, so the sentence needs correction."},
r"Replete WITH; past sentence → could have.")
L(73, r"""-> S1 compares “he” to a philanthropist who finds that his good deed paid well, so the sentence that continues this idea comes next: D (“He cannot prevent the satisfaction … ten percent”).
-> Then A names Bateman Hunter and speaks of his pure heart, and it ends with “Isabel Longstaffe's cool grey eyes”, which C picks up (“They were far-seeing and wise”).
-> B then moves to her strict standards, which lead on to S2 (“no appeal from her judgement”), so the order is D, A, C, B.""",
{"CBAD": "wrong — C (“They were far-seeing and wise”) cannot follow S1 because “they” has no referent yet.",
 "BDAC": "wrong — B begins with “She”, but no woman has been mentioned after S1.",
 "ACDB": "wrong — A cannot come straight after S1, and D does not fit after C (the “eyes” comment).",
 "DACB": "correct — S1, then D, A, C, B, then S2 gives a clear and logical flow."},
r"S1 → D (philanthropist idea) → A (Hunter) → C (her eyes) → B (her standards) → S2.")
L(74, r"""-> S1 says the writer learnt La Fontaine's fables as a boy, so the next line should name one of them: D (“Among those I learnt was The Ant and The Grasshopper …”).
-> A then retells the fable: the ant works hard in summer and the grasshopper sings.
-> B describes winter and the grasshopper's begging, C gives the ant's “classic answer”, and S2 is that very answer (“What were you doing in the summertime?”), so the order is D, A, B, C.""",
{"BDAC": "wrong — B (winter comes) cannot come straight after S1, because the fable has not been introduced yet.",
 "CABD": "wrong — C (“Then the ant gives him her classic answer”) cannot open the sequence after S1.",
 "ABCD": "wrong — A (“In this admirable fable”) has no fable to refer to until D names it.",
 "DABC": "correct — S1, then D, A, B, C, then S2 follows the story in order."},
r"S1 (fables) → D (this fable named) → A (summer) → B (winter) → C (ant's answer) → S2.")
L(75, r"""-> “Not entirely wrong” gives a balanced view that matches the following “but it overlooked several key points”.
-> The word “but” signals a contrast, so a mild first part (“not entirely wrong”) followed by a fault in the second part makes a smooth, logical sentence.
-> The given part is already correct in meaning and grammar, so no change is needed.""",
{"His argument was entirely wrong": "wrong — it contradicts the sense, because the sentence goes on to say that the argument had some merit.",
 "His argument was wrong": "wrong — it removes the contrast with “but” and is too harsh.",
 "His argument was not so wrong": "wrong — “not so wrong” is less natural and slightly changes the meaning.",
 "No improvement": "correct — the original part is already accurate and well formed."},
r"“Not entirely wrong, but …” is already balanced; no change.")
L(76, r"""-> The very first sentence of the passage says that environments of poverty, social injustice and inadequate sanitation contribute to the spread of infectious diseases.
-> So the risk is higher where poverty and poor sanitation are found.
-> The other options describe healthy or well-developed settings, which the passage links to lower, not higher, disease.""",
{"Areas with poverty": "correct — the passage directly names poverty and inadequate sanitation as causes.",
 "Regions with advanced": "wrong — the passage does not link advanced healthcare to more disease.",
 "Communities with high": "wrong — literacy is not mentioned as a risk.",
 "Cities with modern": "wrong — modern infrastructure and clean water are described as helping reduce disease."},
r"Poverty + poor sanitation = more infection (first sentence).")
L(77, r"""-> The passage says that the most well-known strategy for lowering infectious diseases is personal hygiene.
-> The three levels of hygiene named are community, household and personal, but only personal hygiene is called the best-known.
-> The words “most common” in the question match “most well-known” in the passage.""",
{"Community hygiene": "wrong — it is one of the three levels but is not the most familiar strategy.",
 "Household hygiene": "wrong — another level of hygiene, not the most well-known.",
 "Personal hygiene": "correct — the passage calls it the most well-known strategy.",
 "Environmental hygiene": "wrong — improving the environment is described as more effective, but not as the most common strategy."},
r"“Most well-known strategy” = personal hygiene.")
L(78, r"""-> The passage says commercialisation of hygiene, helped by heavy advertising, has created a false sense of security.
-> The concern is that people focus on personal hygiene alone and think they are safe, while larger causes such as water and sanitation are overlooked.
-> The concern is therefore a false sense of security, not a loss of jobs or lower costs.""",
{"It encourages balanced": "wrong — the passage says the opposite: the focus is one-sided, not balanced.",
 "It creates a false": "correct — the passage names a false sense of security from advertising.",
 "Neglects the water": "wrong — the passage does not say that commercialisation itself neglects these sectors.",
 "Decreases the standard": "wrong — operational costs and job losses are never mentioned."},
r"Commercialisation → false sense of security.")
L(79, r"""-> The passage says evidence from Western Europe shows that better general environmental conditions, namely clean water, proper sanitation and food security, greatly reduced infant and child deaths and infections.
-> It adds that this effect went beyond personal hygiene.
-> So the factor that most reduced child mortality was better access to clean water and sanitation.""",
{"Increased handwashing": "wrong — the passage says improved environment, not hand hygiene campaigns, made the difference.",
 "Use of antibiotics": "wrong — antibiotics are mentioned only in the worry about resistance.",
 "Commercial hygiene": "wrong — the passage criticises commercial hygiene products.",
 "Better access": "correct — clean water and sanitation are named as the key improvements."},
r"Western Europe → clean water, sanitation, food security.")
L(80, r"""-> The last sentence says an emphasis on hand hygiene shows how business interests influence individual health behaviour, often at the expense of concerns about environmental damage and antibiotic resistance.
-> So the business influence keeps the focus on hand hygiene and pushes aside the wider problems.
-> This matches the idea that commercial influence ignores wider health issues.""",
{"It promotes balanced": "wrong — the passage says concern for the environment is sacrificed, not promoted.",
 "It focuses on hand": "correct — the focus on hand hygiene comes at the cost of wider health and environmental worries.",
 "It encourages antibiotic": "wrong — the passage says worry about antibiotic resistance is pushed aside.",
 "It reduces environmental": "wrong — no innovation or reduction in environmental damage is mentioned."},
r"Business influence → hand hygiene focus, wider issues ignored.")
