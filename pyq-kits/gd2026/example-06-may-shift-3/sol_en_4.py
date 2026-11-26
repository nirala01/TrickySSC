from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> The idiom “at the drop of a hat” means immediately, without delay or hesitation.
-> It suggests doing something at the slightest signal, without needing a reason or warning.
-> Example: He is ready to help his friends at the drop of a hat.""",
{"To suddenly make sense": "wrong — that is “to fall into place” or “to click”.",
 "A sudden feeling of excitement or anger that causes one to act in unexpected ways": "wrong — that describes acting “on the spur of the moment” or “in the heat of the moment”.",
 "immediately or very suddenly, with little to no provocation or forewarning": "correct — the exact meaning of the idiom.",
 "To hastily and forcefully remove someone from a place": "wrong — that is “to give someone the boot” or “to throw someone out”."},
r"Drop of a hat = at once, without a second thought.")
L(62, r"""-> “Let things play out” means to allow events to develop naturally without stepping in.
-> It is used when one waits patiently to see how a situation ends.
-> Example: Don't interfere now; let things play out and then decide.""",
{"Contrary to the pace or flow of a game or situation, usually in the context of sports": "wrong — that is “against the run of play”.",
 "To be skillfully manipulated by someone to suit their own needs, ends, or benefits": "wrong — that is “to be played like a fiddle”.",
 "To depict or present something in a grandiose or ostentatious manner so as to draw attention to it and make it seem very important.": "wrong — that is “to play something up”.",
 "To allow something to progress, without interfering in it": "correct — the meaning of “let things play out”."},
r"Play out = unfold; let it play out = don't interfere.")
L(63, r"""-> The question asks for the one word that is spelt correctly.
-> “Imbue” (to fill or inspire with a feeling or quality) is spelt correctly.
-> The other three words have spelling mistakes.""",
{"Incepient": "misspelt — the correct spelling is “Incipient” (just beginning).",
 "Impetous": "misspelt — the correct spelling is “Impetuous” (acting quickly without thinking).",
 "Imbue": "correct spelling.",
 "Ignomany": "misspelt — the correct spelling is “Ignominy” (public shame)."},
r"Incip-ient, Impetu-ous, Ignomin-y — three tricky endings.")
L(64, r"""-> “Generous” means ready to give freely — money, time or help.
-> The sentence confirms it: he “donates often”.
-> So the synonym must mean kind and giving.""",
{"Mean": "the opposite — unwilling to give or share.",
 "Greedy": "the opposite — wanting more for oneself.",
 "kind hearted": "correct — a generous person is kind and giving.",
 "Proud": "unrelated — it means having self-respect or arrogance."},
r"Generous = giving, kind-hearted; opposite = mean, stingy.")
L(65, r"""-> The question asks for the misspelt word.
-> “Propel” (to push forward) has a single “l” and a single “p” in the middle: p-r-o-p-e-l.
-> “Proppel” has a wrong double “p”, so it is misspelt.""",
{"Carousel": "correctly spelt (a merry-go-round or a revolving belt).",
 "Proppel": "misspelt — the correct spelling is “Propel”.",
 "Apparel": "correctly spelt (clothing).",
 "Laurel": "correctly spelt (a leaf wreath; a symbol of honour)."},
r"Propel → propeller, propulsion — only one p after “pro”.")
L(66, r"""-> “Extra” means more than what is needed or usual.
-> Its antonym must mean something that is needed — necessary.
-> “Essential” means absolutely necessary.""",
{"Additional": "a synonym of extra, not an antonym.",
 "surplus": "a synonym — more than is needed.",
 "Spare": "a synonym — kept in addition, not in use.",
 "Essential": "correct — necessary is the opposite of extra."},
r"Extra = more than needed; essential = cannot do without.")
L(67, r"""-> An irrational and intense fear of flying is called aerophobia (also aviophobia).
-> It comes from the Greek “aero” (air) and “phobos” (fear).
-> People with aerophobia feel great anxiety about travelling by air.""",
{"Aerophobia": "correct — fear of flying.",
 "Acrophobia": "fear of heights.",
 "Claustrophobia": "fear of closed or narrow spaces.",
 "ophidiophobia": "fear of snakes."},
r"Aero = air (flying), Acro = height, Claustro = closed space, Ophidio = snake.")
L(68, r"""-> The active sentence is in the simple past: The judge advised them …
-> In the passive, the object “them” becomes the subject “They”, and the verb becomes “were advised”.
-> The infinitive “to settle the matter amicably” stays as it is: They were advised by the judge to settle the matter amicably.""",
{"They were advised by the judge to settle the matter amicably.": "correct — right subject, tense and form.",
 "They were advise to settle the matter amicably by the judge.": "wrong — it needs the past participle “advised”, and “by the judge” is misplaced.",
 "They were advising by the judge to settle the matter amicably.": "wrong — “were advising” is active continuous, not passive.",
 "The judge advised settling the matter amicably.": "wrong — it is still in the active voice and drops “them”."},
r"Simple past passive: was/were + V3 (advised).")
L(69, r"""-> The sentence is a question in the simple past: Did + subject + V1 + object?
-> In the passive it becomes: Was/Were + object + V3 + by + subject?
-> “the old temple” is singular, so: Was the old temple damaged by the earthquake?""",
{"Was the old temple damaged by the earthquake?": "correct — simple past passive question.",
 "Has the old temple been damaged by the earthquake?": "wrong — present perfect tense.",
 "Is the old temple damaged by the earthquake?": "wrong — simple present tense.",
 "Will the old temple be damaged by the earthquake?": "wrong — simple future tense."},
r"Did … V1? → Was/Were … V3 … by …?")
L(70, r"""-> The correct phrase for payment in money is “paid in cash”, not “paid on cash”.
-> The error is in the part “on cash and with”.
-> Correct sentence: The painters want to be paid immediately in cash and with no questions asked.""",
{"The painters want": "no error.",
 "to be paid immediately": "no error.",
 "on cash and with": "error — it should be “in cash”.",
 "no questions asked.": "no error — a fixed phrase meaning without any enquiry."},
r"Pay in cash, by cheque, by card, on credit.")
L(71, r"""-> The verb “invest” in the sense of giving someone power or a duty takes the preposition “with”.
-> “invested with the charge” means given the responsibility.
-> Correct sentence: The commanding officer was invested with the charge of bringing all the troops back whole.""",
{"in": "wrong — “invest in” is used for putting money into something (invest in shares).",
 "with": "correct — invested with power, authority or a charge.",
 "for": "wrong — not used with “invested” in this sense.",
 "by": "wrong — “by” would show who did the investing, not what was given."},
r"Invest IN shares (money); invest someone WITH power (authority).")
L(72, r"""-> The phrase “in the country” compares him with all the leaders in the country.
-> A comparison with more than two needs the superlative degree: “the most influential”.
-> “the more influential” is used only when comparing two.""",
{"a most influential leader": "wrong — “a most” means “a very”, and the superlative needs “the”.",
 "the most influential leader": "correct — superlative with “the”.",
 "most influential leader": "wrong — the article “the” is missing.",
 "No improvement required": "wrong — “the more influential” is a comparative and needs “than”."},
r"Among many → the + superlative (the most …); between two → the comparative.")
L(73, r"""-> S1 says poverty has a home in Africa like a “quiet second skin”.
-> D continues the image: it is “worn” with unconscious dignity — so D comes first.
-> A says people do not look down at your torn shoes; C says they look into your eyes instead; B (“That is all that matters”) closes the idea before S2 talks about this “eye-looking”. Order: DACB.""",
{"ACBD": "wrong — A cannot follow S1 directly; D must explain the “second skin” first.",
 "DACB": "correct — S1, D, A, C, B, S2 flows logically.",
 "CBDA": "wrong — “They look straight” has no subject to refer to after S1.",
 "BDAC": "wrong — “That is all that matters” makes no sense right after S1."},
r"Follow the pronoun and image links: skin → worn (D), shoes (A) → eyes (C) → that matters (B).")
L(74, r"""-> S1 introduces the two children, Dorothea and Robert.
-> C follows (“A few months after Robert …”), D continues Marian's job and Ralph at the high school.
-> B mentions one serious disturbance two years ago, A says they never talked about “it”, and S2 describes that scene. Order: CDBA.""",
{"ADBC": "wrong — “It” in A has nothing to refer to after S1.",
 "DABC": "wrong — “The position” in D needs C to introduce it.",
 "CDBA": "correct — S1, C, D, B, A, S2 is logical.",
 "DBCA": "wrong — D must come after C, which first mentions the position."},
r"Find the sentence that introduces a noun (C: position) and the one that uses it (D: The position).")
L(75, r"""-> “Proceed” already means “to go forward”, so “proceed forward” is redundant.
-> The correct expression is simply “proceed with the project”.
-> Similarly, avoid “return back”, “repeat again”, “revert back”.""",
{"the team decided to proceed forth with the project": "wrong — “proceed forth” is also redundant.",
 "the team decided to proceed with the project": "correct — no redundant word.",
 "the team decided to proceed onward with the project": "wrong — “onward” repeats the meaning of “proceed”.",
 "No improvement required": "wrong — “proceed forward” is redundant."},
r"Proceed = go forward; never add forward/onward/forth.")
L(76, r"""-> The passage says Husserl viewed the act of consciousness, the thinking subject and the object it intends as inseparable.
-> So for Husserl, consciousness and objects cannot be separated in perception.
-> The other options contradict this view.""",
{"They are inseparable in the act of perception": "correct — stated directly in the passage.",
 "They exist independently without interaction": "wrong — the opposite of “inseparable”.",
 "Objects create meaning without human awareness": "wrong — meaning needs consciousness.",
 "Consciousness is irrelevant to understanding reality": "wrong — consciousness is central to phenomenology."},
r"Husserl: subject + consciousness + object = inseparable.")
L(77, r"""-> The passage says art is not a means of securing pleasure but a revelation of being.
-> It adds that the work is the phenomenon by which we come to know the world.
-> So art is more than pleasure — it helps us understand the world.""",
{"Art is mainly a form of entertainment and something we enjoy looking at.": "wrong — the passage says art is not just for pleasure.",
 "Art is more than just for pleasure; it helps us understand the world.": "correct — matches “revelation of being”.",
 "Art exists on its own, separate from how people think about or interpret it.": "wrong — meaning is created when the reader and text interact.",
 "Art matters only because of its historical and cultural importance.": "wrong — that is closer to Jauss's view, and “only” is too strong."},
r"Phenomenology: art = revelation of being, not just pleasure.")
L(78, r"""-> Jauss says the social history of a text must be considered before interpreting it.
-> He adds that each historical period has its own “horizon of expectations”.
-> So the meaning of a text changes as readers' expectations change over time.""",
{"A fixed and universal meaning that remains constant over time": "wrong — he says meaning is not fixed or universal.",
 "Keeping the text completely separate from its historical and cultural background": "wrong — he insists on social history.",
 "The social history of a text and how readers' expectations change over time": "correct — this is his main point.",
 "Giving more importance to what the author meant than to how readers understand the text": "wrong — the passage stresses readers, not the author."},
r"Jauss = social history + horizon of expectations.")
L(79, r"""-> Iser says a text does not achieve meaning until a consciousness recognises or registers it.
-> In other words, meaning comes only when a reader becomes aware of the text.
-> So object and human consciousness are inseparable.""",
{"When the author writes with a clear goal and purpose": "wrong — Iser does not tie meaning to the author's aim.",
 "When critics agree on a single interpretation of the text": "wrong — the passage says nothing about critics agreeing.",
 "When the text is separated from its readers and its historical background": "wrong — the opposite of Iser's view.",
 "Only when someone becomes aware of the text": "correct — meaning needs a consciousness to register the text."},
r"Iser: no reader's awareness → no meaning.")
L(80, r"""-> Jauss says each historical period establishes its own horizon of expectations.
-> Because of this, the overall meaning of a text keeps changing from one period to another.
-> Since meaning never stays fixed, a final assessment of any literary work becomes impossible.""",
{"Because each historical period creates its own horizon of expectations, making meaning change over time": "correct — the reason given in the passage.",
 "Because texts have fixed and universal meanings that remain constant across all eras": "wrong — the passage says meaning is not fixed.",
 "Because interpretation depends solely on authorial intention without considering readers or context": "wrong — the passage stresses readers and history.",
 "Because literature is disconnected from social history and cultural influences": "wrong — Jauss links literature to social history."},
r"Changing horizons → changing meaning → no final verdict.")
