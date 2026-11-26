from base import opt_bullets as ob, Q_EN
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “Talk nineteen to the dozen” means to talk very fast and without stopping.
-> Example: The two friends met after years and talked nineteen to the dozen.""",
{"To speak slowly in a whispering tone": "the opposite — the idiom is about fast, nonstop talking.",
 "To whisper in the ear": "whispering is about a low voice, not speed.",
 "To speak in an angry manner": "anger is not part of the idiom's meaning.",
 "To speak very rapidly, hurriedly, and/or energetically": "correct — talking very fast and nonstop."},
r"Nineteen words where a dozen would do = talking too fast.")
L(62, r"""-> “Toffee-nosed” (British, informal) describes a snobbish person who thinks they are better than others.
-> It is linked with pride in social class, as if the person holds the nose up in the air.""",
{"Describing someone who believes they are superior to others, especially due to their social rank or class": "correct — snobbish and proud of social status.",
 "Describing someone who believes they are inferior to others, especially due to their social poverty.": "the opposite — this describes an inferiority complex.",
 "Describing something which is cheap due to its production quality": "the idiom describes a person's attitude, not a product.",
 "To be very bad at doing something": "unrelated — that would be “all thumbs”."},
r"Toffee-nosed = nose in the air = snobbish.")
L(63, r"""-> “Seldom” is an adverb meaning “not often” or “hardly ever”.
-> Example: He seldom eats outside.""",
{"Rarely": "correct — the same meaning as seldom.",
 "often": "the opposite of seldom.",
 "Always": "every time — the opposite idea.",
 "Never": "not at all — stronger than seldom, which still allows a few times."},
r"Seldom = rarely (not never).")
L(64, r"""-> The task is to find the word spelt wrongly.
-> The correct spelling is “unscrupulous” (u-n-s-c-r-u-p-u-l-o-u-s), meaning having no moral principles.""",
{"Unprecedented": "correctly spelt — never done or known before.",
 "Unconventional": "correctly spelt — not following the usual way.",
 "Unfathomable": "correctly spelt — impossible to understand fully.",
 "Unscrupilous": "misspelt — the correct form is “unscrupulous” (“-pulous”, not “-pilous”)."},
r"Scruple → unscrupulous (keep the “pu”).")
L(65, r"""-> The task is to find the misspelt word.
-> The vegetable is spelt “zucchini”, with a double c (an Italian word).""",
{"Zygote": "correctly spelt — the cell formed by fertilisation.",
 "zombie": "correctly spelt.",
 "zigzag": "correctly spelt — a line with sharp turns.",
 "zuchini": "misspelt — the correct spelling is “zucchini” (double c)."},
r"Zucchini has a double c.")
L(66, r"""-> “Efficient” means doing a task well without wasting time, money or effort.
-> Its antonym is formed with the prefix “in-”: inefficient.""",
{"Productive": "a near-synonym, not an antonym.",
 "Capable": "having the ability — close in meaning, not opposite.",
 "Effective": "producing the desired result — close in meaning.",
 "Inefficient": "correct — the opposite of efficient."},
r"Efficient ↔ inefficient.")
L(67, r"""-> The phrase is “an endless or abundant supply”.
-> A cornucopia (the “horn of plenty”) is a symbol of abundance, so the word means a plentiful supply.""",
{"Cornucopia": "correct — an abundant supply of something.",
 "Hullabaloo": "a noisy fuss or uproar.",
 "Labyrinth": "a complicated maze of paths.",
 "Maelstrom": "a powerful whirlpool or a confused, violent situation."},
r"Cornucopia = horn of plenty = abundance.")
L(68, r"""-> The sentence adds one activity to another: he writes novels and he also paints.
-> “In addition to” (+ noun or -ing form) means “besides” or “as well as”.""",
{"In addition to": "correct — “In addition to writing novels, he likes to paint.”",
 "For": "shows purpose or duration; “For writing novels, he likes to paint” makes no sense.",
 "Due to": "shows cause — painting is not caused by writing novels.",
 "Owing to": "also shows cause, so it gives the wrong meaning."},
r"Adding one activity to another → in addition to / besides.")
L(69, r"""-> “Will have been completed” is the future perfect passive.
-> In the active voice, the future perfect is “will have + past participle”: The research team will have completed the final report.""",
{"The research team will complete the final report before the board meeting begins.": "simple future — the “have completed” (perfect) idea is lost.",
 "The research team will have completed the final report before the board meeting begins.": "correct — future perfect active, the tense of the original.",
 "The research team completes the final report before the board meeting begins.": "simple present — wrong tense.",
 "The research team has completed the final report before the board meeting begins.": "present perfect — wrong tense."},
r"will have been + V3 (passive) → will have + V3 (active).")
L(70, r"""-> “The lights are to be switched off when you leave” is a passive instruction (is/are to be + V3).
-> Its active form is an imperative sentence addressed to “you”: Switch off the lights when you leave.""",
{"You will switch the lights off when you leave.": "simple future statement — the instruction becomes a prediction.",
 "The lights should be switched off before leaving.": "still passive, and the meaning changes to “should”.",
 "Switch off the lights when you leave.": "correct — the active imperative form.",
 "Switched off the lights when you leave.": "uses the past form “switched”, which is ungrammatical here."},
r"is/are to be + V3 (instruction) → imperative: V1 + object.")
L(71, r"""-> “Nice” takes the preposition “to” when it means kind towards a person.
-> Example: She was very nice to the new students.""",
{"with": "“nice with” is not the standard expression for being kind to someone.",
 "at": "“at” is used for a place or a skill (“good at”), not for kindness to a person.",
 "to": "correct — nice to someone.",
 "by": "“by” shows the doer or a means; it does not fit here."},
r"Kind / nice / polite / rude + to + person.")
L(72, r"""-> The diplomat wanted to calm tensions, but his remarks made things worse, so the remarks must have been unclear or open to misreading.
-> The idiom is “add fuel to the fire” (not “in the fire”).""",
{"antagonistic remarks only added fuel into the fire": "“into the fire” is wrong; the idiom uses “to”.",
 "ambiguous remarks only added fuel to the fire": "correct — unclear remarks made things worse; the idiom is correct.",
 "assiduous remarks only added fuel for the fire": "“assiduous” means hard-working, which does not suit remarks, and “for the fire” is wrong.",
 "No improvement required": "the sentence has two errors: “ambitious” does not fit and “in the fire” is wrong."},
r"Add fuel to the fire = make a bad situation worse.")
L(73, r"""-> S1 says the narrator was doing everything he could; B lists those efforts (stormed, scolded, hurled the sandwich case).
-> D continues the chase in the dusk; C is the climax (Esmé bounds into the bushes and the wail stops); A comments that this horrible part is always hurried over, which leads to S2 (the beast returns).""",
{"BACD": "A cannot come before the horrible event it refers to (C).",
 "BADC": "A again comes before the event (C) it describes.",
 "BDAC": "A (“this part of the story”) is placed before C, the part it refers to.",
 "BDCA": "correct — efforts (B), chase (D), climax (C), the narrator's comment (A), then the beast's return (S2)."},
r"A comment like “this part of the story” comes right after the event it refers to.")
L(74, r"""-> S1: babies were often exposed to polioviruses. D explains why these infants did not fall ill (mothers' antibodies), and B follows with “then” — they developed their own antibodies.
-> A begins the contrast with “Paradoxically” (better sanitation stopped early exposure) and C gives the result with “Consequently”.""",
{"BACD": "B (“The babies then …”) needs D before it.",
 "DBAC": "correct — protection (D), own antibodies (B), the paradox (A), the result (C).",
 "CBAD": "C (“Consequently”) cannot open the sequence.",
 "BDCA": "B cannot come first, and C must follow A."},
r"Link words decide the order: “then” after D, “Consequently” after A.")
L(75, r"""-> “All but none” is self-contradictory: “all but” means “all except”, and the next clause says one biscuit (“the last one”) was left for the dog.
-> So he ate all except one: “He ate all but one of the biscuits”.""",
{"He ate all but one of the biscuits": "correct — all except one, which matches “the last one” given to the dog.",
 "He ate all of the biscuits": "then nothing would be left for the dog.",
 "He ate none of the biscuits": "contradicts “the last one” — the plate would still be full.",
 "No improvement required": "“all but none” makes no sense."},
r"All but one = every one except one.")
L(76, r"""-> The subject “such content” is singular, and the sentence is in the present tense (“it also shapes”).
-> A singular subject in the simple present takes the verb with -s: provides.""",
{"provide": "plural form — does not agree with the singular subject “content”.",
 "provides": "correct — singular present, matching “shapes” in the same sentence.",
 "will providing": "ungrammatical — “will” must be followed by the base form.",
 "provided": "past tense — the passage is in the present."},
r"Singular subject + present tense → verb + s.")
L(77, r"""-> The sentence contrasts two possibilities: a child who watches violent cartoons “may become aggressive”, while one who watches educational programmes ___ develop problem-solving skills.
-> The parallel structure and the idea of possibility both call for “may”.""",
{"may": "correct — expresses possibility and matches “may become” earlier in the sentence.",
 "should": "expresses duty or advice, not possibility.",
 "shall": "used for future intention, mostly with I/we — it does not fit.",
 "must have": "refers to a past certainty and needs a past participle (must have developed)."},
r"Parallel possibility: may … may.")
L(78, r"""-> The phrasal verb “deal with” means to handle or manage a problem.
-> “They will struggle to deal with real-life challenges.”""",
{"by": "“deal by” is not used for handling problems.",
 "for": "“deal for” is not the right preposition here.",
 "with": "correct — deal with = handle.",
 "upon": "“deal upon” is not standard English."},
r"Deal with = cope with = handle.")
L(79, r"""-> The word in blank D is “restriction” — a rule or limit that controls what someone can do.
-> Its synonym is the word that also means stopping or forbidding something.""",
{"freedom": "the opposite idea — being free from limits.",
 "expansion": "growth or increase — unrelated.",
 "permission": "allowing something — the opposite of restriction.",
 "prohibition": "correct — forbidding something, a strong form of restriction."},
r"Restriction ≈ prohibition; opposite = permission/freedom.")
L(80, r"""-> The word in blank E is “illustrates”, meaning “shows clearly” or “makes clear with an example”.
-> Its antonym means to hide or make unclear.""",
{"obscures": "correct — makes something unclear or hidden, the opposite of illustrates.",
 "shows": "a synonym of illustrates.",
 "explains": "close in meaning to illustrates.",
 "demonstrates": "a synonym — shows clearly."},
r"Illustrate (make clear) ↔ obscure (make unclear).")
