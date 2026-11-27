from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “Hamlet without the Prince” means an event or performance that takes place without its most important person.
-> In Shakespeare's play the Prince of Denmark, Hamlet, is the central character; staging it without him would leave out the heart of the play.
-> So the idiom describes something that goes on even though the key player is missing.""",
{"An actor with a small or insignificant part in a performance": "wrong — the idiom is about the absence of the main person, not a minor role.",
 "A tragedy where the prince dies": "wrong — a literal reading of the play, not the idiom's meaning.",
 "The dilemma of choosing between two important persons": "wrong — no choice between two people is involved.",
 "An event that happens despite the absence of a key player": "correct — the event goes on without its central figure."},
r"Hamlet without the Prince = the show without its star.")
L(62, r"""-> A “popcorn film” (popcorn movie) is a light, entertaining film watched mainly for fun, like eating popcorn.
-> It is usually action-packed or amusing but has little emotional or intellectual depth.
-> So the meaning is a film that is enjoyable to watch but not of very high quality.""",
{"A film that shows the actual murder or death of a person": "wrong — that describes a “snuff film”.",
 "A film that is entertaining to watch but is generally not of a very high quality or rich in emotional or intellectual depth": "correct — light entertainment with little depth.",
 "A film with a very large budget and production value that is meant to provide substantial revenue to the production company": "wrong — that is a “blockbuster”.",
 "A film that has a passionate fan base despite lacking critical acclaim, box office success, or mainstream interest": "wrong — that is a “cult film”."},
r"Popcorn film = fun to munch through, nothing deep.")
L(63, r"""-> The question asks for the CORRECTLY spelt word.
-> “Deference” (respect for someone's wishes or opinions) is spelt correctly.
-> The other three are misspellings of dalliance, dubious and depravity.""",
{"Daliance": "wrong — the correct spelling is “dalliance” (double l).",
 "Deference": "correct — spelt correctly (polite respect).",
 "Dubeous": "wrong — the correct spelling is “dubious”.",
 "Dipravity": "wrong — the correct spelling is “depravity”."},
r"Defer → deference; dally → dalliance; dubious ends in -ious.")
L(64, r"""-> “Amazing” means causing great surprise or wonder; extremely good.
-> Its closest synonym is “incredible”, which means so good or surprising that it is hard to believe.
-> Ordinary, boring and ugly suggest the opposite.""",
{"ordinary": "wrong — plain and common, the opposite of amazing.",
 "Incredible": "correct — hard to believe, wonderful; the same as amazing.",
 "Boring": "wrong — dull, the opposite idea.",
 "Ugly": "wrong — unpleasant to look at; not related to surprise or wonder."},
r"Amazing = incredible = astonishing.")
L(65, r"""-> The question asks for the MISSPELT word.
-> The correct spelling is “miscellaneous” (of various kinds) — with “-eous”, not “-ious”.
-> Vociferous, amalgamation and innocuous are spelt correctly.""",
{"Vociferous": "wrong — spelt correctly (loud and forceful).",
 "Amalgamation": "wrong — spelt correctly (joining together).",
 "Miscellanious": "correct answer — misspelt; the right spelling is “miscellaneous”.",
 "Innocuous": "wrong — spelt correctly (harmless)."},
r"Miscellaneous: “misc + ellan + eous” — like simultaneous.")
L(66, r"""-> “Entire” means whole or complete, with no part missing.
-> Its antonym is “partial”, meaning only a part, not the whole.
-> Whole, complete and total are synonyms of entire.""",
{"Whole": "wrong — a synonym of entire.",
 "complete": "wrong — a synonym of entire.",
 "Total": "wrong — a synonym of entire.",
 "Partial": "correct — only a part; the opposite of entire."},
r"Entire ≠ partial (part only).")
L(67, r"""-> “Bohemian” describes a person who lives an unconventional, free and artistic lifestyle, ignoring social rules.
-> The word comes from the free-living artists and writers of 19th-century Paris, who were linked with Bohemia.
-> So “an unconventional lifestyle” is best described as Bohemian.""",
{"Chauvinism": "wrong — extreme, unfair belief that one's own group is superior.",
 "Bohemian": "correct — an unconventional, free-spirited way of living.",
 "Hedonism": "wrong — the pursuit of pleasure as the main aim of life.",
 "Dogmatism": "wrong — stating opinions as if they were certain truths."},
r"Bohemian = artist's free, unconventional life.")
L(68, r"""-> The suffix “-cide” means killing; “fili-” comes from the Latin word for son or daughter.
-> So “filicide” is the killing of one's own son or daughter.
-> The other words name the killing of other relatives.""",
{"Filicide": "correct — killing of one's son or daughter.",
 "Fratricide": "wrong — killing of one's brother.",
 "Matricide": "wrong — killing of one's mother.",
 "Parricide": "wrong — killing of a parent or close relative."},
r"Filius = son → filicide; frater = brother; mater = mother.")
L(69, r"""-> The fixed phrase is “in disguise”, meaning dressed so as not to be recognised.
-> “Went out in disguise among the common people” is the correct usage.
-> On, by and for are not used with disguise in this sense.""",
{"on": "wrong — “on disguise” is not idiomatic.",
 "in": "correct — “in disguise” is the fixed phrase.",
 "by": "wrong — “by disguise” is not used here.",
 "for": "wrong — “for disguise” would mean for the purpose of disguise."},
r"Go about in disguise — always “in”.")
L(70, r"""-> The active sentence is in the simple past: “His grandmother looked after him.”
-> In the passive, the object “him” becomes the subject “He”, and the verb becomes was + past participle: “was looked after”.
-> The phrasal verb “look after” must stay together: “He was looked after by his grandmother all these years.”""",
{"He was looked by his grandmother after all these years.": "wrong — the phrasal verb “looked after” is split, changing the meaning.",
 "He looked after by his grandmother all these years.": "wrong — the helping verb “was” is missing.",
 "He was looked after by his grandmother all these years.": "correct — was + looked after, with the phrasal verb kept together.",
 "He was after looked by his grandmother all these years.": "wrong — wrong word order in the phrasal verb."},
r"Passive of a phrasal verb: keep it whole — was looked after by.")
L(71, r"""-> The passive sentence is in the simple future: “will be conducted by the board”.
-> In the active voice, the doer “the board” becomes the subject and “will be conducted” becomes “will conduct”.
-> The time phrase “next Monday” also needs the future tense: “The board will conduct the final round of interviews next Monday in the main auditorium.”""",
{"The board conducts the final round of interviews next Monday in the main auditorium.": "wrong — simple present instead of future.",
 "The board conducted the final round of interviews next Monday in the main auditorium.": "wrong — simple past clashes with “next Monday”.",
 "The board will conduct the final round of interviews next Monday in the main auditorium.": "correct — will be + V3 becomes will + V1.",
 "The board has conducted the final round of interviews next Monday in the main auditorium.": "wrong — present perfect clashes with “next Monday”."},
r"will be + V3 (passive) → will + V1 (active).")
L(72, r"""-> “Let the concert be arranged by the students” is an imperative sentence in the passive voice.
-> Its active form follows the pattern: Let + doer + V1 + object.
-> So it becomes “Let the students arrange the concert.”""",
{"The students let the concert arrange.": "wrong — changes the meaning and the word order.",
 "Let the students arrange the concert.": "correct — Let + students + arrange + the concert.",
 "The concert lets the students arrange it.": "wrong — makes the concert the doer.",
 "Arrange the students to let the concert.": "wrong — meaningless word order."},
r"Let + object + be + V3 + by + doer → Let + doer + V1 + object.")
L(73, r"""-> The verb “long” (to wish strongly for something) takes the preposition “for”, not “over”.
-> The correct sentence is: “The poet longed for the bygone days and mused over the time spent with friends and relatives.”
-> “Mused over” is correct, so the error is in the first part.""",
{"The poet longed over the": "correct answer — the error is here: “longed over” should be “longed for”.",
 "bygone days and mused over the": "wrong — “mused over” is correct usage.",
 "time spent with": "wrong — no error.",
 "friends and relatives.": "wrong — no error."},
r"Long FOR something; muse OVER something.")
L(74, r"""-> “Between” is used for two people or things, while “among” is used for more than two.
-> The teachers in private schools are many, so “among” is correct.
-> “There is no unity among the teachers in private schools.”""",
{"between": "wrong — used for two only.",
 "within": "wrong — means inside a group or limit, not idiomatic with unity here.",
 "in": "wrong — “unity in the teachers” is not idiomatic.",
 "among": "correct — used for more than two people."},
r"Two → between; many → among.")
L(75, r"""-> The correct idiom is “to run with the hare and hunt with the hounds”.
-> It means to try to support both sides in a conflict at the same time, which fits a “cunning minister”.
-> The underlined part has the animals swapped, so it must be replaced with “running with the hare and hunting with the hounds”.""",
{"dancing with the hare and hunting with the hounds": "wrong — “dancing” is not part of the idiom.",
 "dining with the hare and running with the hounds": "wrong — both verbs are wrong.",
 "running with the hare and hunting with the hounds": "correct — the exact form of the idiom.",
 "No improvement required": "wrong — the original has the hare and hounds swapped."},
r"Run with the hare, hunt with the hounds — be on both sides.")
L(76, r"""-> The passage says: “Opportunity and a strong belief in a better life are the two pillars of the American Dream.”
-> So the two pillars are opportunity and belief in a better life.
-> Wealth, political power and education are not named as pillars.""",
{"Opportunity and belief in a better life": "correct — stated in the passage as the two pillars.",
 "Achieve wealth and fame": "wrong — the passage says it is not just about money (motor cars and high wages).",
 "Champion equality and reach for political power": "wrong — political power is not mentioned.",
 "Pursue education and rise in social status": "wrong — education is not mentioned as a pillar."},
r"Look for the word “pillars” in the passage.")
L(77, r"""-> The passage says: “Immigrants also see it as a land where anyone can pursue their dreams.”
-> It begins by describing the Dream as the belief that America offers equal opportunities to every individual.
-> So for immigrants it symbolises a land of freedom and equal opportunities.""",
{"A guarantee of wealth and luxury": "wrong — the passage says it is not just a dream of motor cars and high wages.",
 "A promise of social recognition without effort": "wrong — the passage stresses hard work.",
 "A land of freedom and equal opportunities": "correct — a land where anyone can pursue their dreams.",
 "A system that favors only the privileged": "wrong — the passage says people are recognised regardless of birth or position."},
r"Immigrants: anyone can pursue their dreams = freedom + equal opportunity.")
L(78, r"""-> The question asks what the passage directly says about the material side of the Dream.
-> The passage says: “It is not just a dream of motor cars and high wages.”
-> So the dream is said to be beyond materialistic things like motor cars and high wages.""",
{"It insists that the dream is beyond materialistic things like motor cars and high wages.": "correct — this restates the passage's own words about material things.",
 "It tells of the importance of hope, merit, and social recognition to a person.": "wrong — true of the passage, but it is about what the Dream includes, not its material side.",
 "It also frames the dream as a vision of social order, enabling all to become what they could be.": "wrong — true of the passage, but it is not about material things.",
 "It advocates valuing people in relation to ability rather than birth or social position.": "wrong — about recognition, not about material things."},
r"“Motor cars and high wages” = the material side.")
L(79, r"""-> The passage says: “Each person should have an opportunity according to their ability or achievement.”
-> So achievement decides the opportunity a person should get.
-> The passage does not say achievement is the only factor, and it rejects birth and position as the basis.""",
{"Success should depend on birth and social position rather than merit": "wrong — the passage says the opposite.",
 "Luck matters more than ability or achievement": "wrong — luck is not mentioned; ability and achievement are stressed.",
 "Achievement is the only factor that determines social recognition in America": "wrong — too extreme; the passage does not say “only”.",
 "Each person should have an opportunity according to their ability or achievement": "correct — the passage's own statement."},
r"Find the line with “ability or achievement”.")
L(80, r"""-> The passage says: “Serving as a symbol of hope, the American Dream suggested that hard work could transform anyone from poverty to success.”
-> So it is a symbol of hope because people can rise from poverty to success through hard work and perseverance.
-> The passage does not say success comes without work or that all barriers have gone.""",
{"It asserts that everyone can become prosperous and comfortable without having to work": "wrong — the passage stresses hard work.",
 "It implies that all citizens should have equal access to employment and educational possibilities": "wrong — employment and education are not mentioned.",
 "It asserts that people may overcome poverty and achieve success through perseverance": "correct — hard work can take anyone from poverty to success.",
 "It claims that all social and economic barriers in America have been eliminated.": "wrong — the passage makes no such claim."},
r"Symbol of hope = poverty to success through hard work.")
