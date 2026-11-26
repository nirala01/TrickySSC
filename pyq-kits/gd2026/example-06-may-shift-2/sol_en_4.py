from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> The idiom “think the sun rises and sets on someone” means to consider that person the most wonderful person in the world.
-> It shows great love or admiration, often for a family member.
-> Example: Her grandfather thinks the sun rises and sets on her.""",
{"the sun rises and sets on him": "correct — the real idiom with exactly this meaning.",
 "the river originates and mixes on him": "not an idiom; the words make no sense together.",
 "the day starts and ends with him": "sounds close but is not the fixed idiom.",
 "the sweets is made and eaten by him": "not an idiom, and “sweets is” is also ungrammatical."},
r"Sun rises and sets on someone = you adore that person.")
L(62, r"""-> “Brisk” means quick, active and energetic.
-> Example: We went for a brisk walk in the morning.
-> So the synonym must also mean fast or lively.""",
{"slow": "the opposite of brisk.",
 "Weak": "unrelated — it means lacking strength.",
 "quick": "correct — brisk and quick both mean fast and active.",
 "Lazy": "close to the opposite of brisk."},
r"Brisk walk = quick walk.")
L(63, r"""-> Among the four underlined words, one is misspelt.
-> The sentence prints “inconsistant”; the correct spelling is “inconsistent”, ending in -ent.
-> The other three underlined words are spelt correctly.""",
{"bureaucratic": "correctly spelt (b-u-r-e-a-u-c-r-a-t-i-c).",
 "inconsistant": "misspelt — the correct form is “inconsistent”.",
 "approach": "correctly spelt, with double “p”.",
 "contractors": "correctly spelt, ending in -or."},
r"consistent, inconsistent, persistent — all end in -ent.")
L(64, r"""-> We must find the word with the wrong spelling.
-> The correct word is “aberration” (a departure from what is normal), spelt with -tion, not -sion.
-> Confession, Dimension and Precision are all spelt correctly.""",
{"Confession": "correctly spelt.",
 "Dimension": "correctly spelt.",
 "Precision": "correctly spelt.",
 "Aberrasion": "misspelt — the correct spelling is “aberration”."},
r"Aberrate → aberration (-tion); verbs ending in -ate usually take -ation.")
L(65, r"""-> “Understand” means to grasp the correct meaning of something.
-> Its opposite is to understand something wrongly.
-> “Misconstrue” means to interpret wrongly, so it is the antonym.""",
{"Misconstrue": "correct — to understand wrongly, the opposite of understand.",
 "Interpret": "a near-synonym — to explain or understand meaning.",
 "Perceive": "a near-synonym — to notice or understand.",
 "Grasp": "a synonym — to understand fully."},
r"mis- + construe (understand) = understand wrongly.")
L(66, r"""-> “Fair” has several meanings: just and honest, light in colour, reasonable, and a public event with stalls and rides.
-> We need the sentence where it means a public event with entertainment.
-> Words like “rides” and “village” point to that meaning.""",
{"The judge gave a fair judgment in the case.": "here fair means just and impartial.",
 "She has a fair complexion.": "here fair means light in colour.",
 "It's only fair that he gets another chance.": "here fair means reasonable or right.",
 "We enjoyed rides at the village fair last Sunday.": "correct — a public event with rides and stalls."},
r"Fair (noun) = mela; fair (adjective) = just / light-coloured.")
L(67, r"""-> A false name used by an author instead of the real name is a “pseudonym” (pen name).
-> Example: Munshi Premchand was the pseudonym of Dhanpat Rai Srivastava.
-> The other words name kinds of nicknames or titles, not an author's false name.""",
{"Sobriquet": "a nickname, often a humorous one.",
 "Pseudonym": "correct — a pen name used by an author.",
 "Epithet": "a descriptive word or phrase added to a name (e.g. “the Great”).",
 "Cognomen": "a family name or surname; also a nickname."},
r"Pseudo = false + nym = name → pseudonym.")
L(68, r"""-> “Failing” can be used as a preposition meaning “in the absence of” or “if not”.
-> “Failing a permanent solution …” means “if there is no permanent solution …”.
-> The sentence then means: if no permanent solution is found, the farmers may go on strike.""",
{"Failing": "correct — means “in the absence of”.",
 "For": "“For a permanent solution, the farmers may go on strike” changes the meaning to a purpose.",
 "Because": "a conjunction; it would need “because of” and still gives the wrong meaning.",
 "since": "a conjunction of time or reason; it cannot take a noun phrase here."},
r"Failing + noun = if there is no …")
L(69, r"""-> The active sentence is in the simple past: “They discovered a cure”.
-> Passive of simple past = was/were + past participle.
-> Object “a cure for the disease” becomes the subject; “last year” stays.""",
{"A cure for the disease will be discovered by them last year.": "future tense — and it clashes with “last year”.",
 "A cure for the disease is discovered by them last year.": "present tense — wrong tense.",
 "A cure for the disease was discovered by them last year.": "correct — simple past passive.",
 "A cure for the disease has been discovered by them last year.": "present perfect — cannot be used with “last year”."},
r"Simple past active → was/were + V3.")
L(70, r"""-> “was being rehearsed” is the past continuous passive.
-> Its active form uses was/were + verb-ing.
-> The doer “the drama group” becomes the subject: “The drama group was rehearsing the play”.""",
{"The drama group rehearsed the play in the school auditorium.": "simple past — the continuous sense is lost.",
 "The drama group is rehearsing the play in the school auditorium.": "present continuous — wrong tense.",
 "The drama group was rehearsing the play in the school auditorium.": "correct — past continuous active.",
 "The drama group has been rehearsing the play in the school auditorium.": "present perfect continuous — wrong tense."},
r"was being + V3 (passive) ↔ was + V-ing (active).")
L(71, r"""-> The adjective “backward” takes the preposition “in” when we name the area of weakness.
-> Example: He is backward in studies.
-> So: “Sanskriti is rather backward in her painting skills.”""",
{"for": "“backward for” is not used.",
 "in": "correct — backward in something.",
 "of": "“backward of” is not standard here.",
 "about": "we may be shy about something, not backward about a skill."},
r"Backward in / weak in / good at.")
L(72, r"""-> S1: he pulls into the driveway; S2: the telephone keeps ringing while he unlocks the door.
-> C (still sitting in the car) follows S1; A gives the reason for his shock (the child's accident).
-> D (he gets out and goes to the door) comes next, and B (dog barking, telephone ringing) leads to S2's “It kept ringing”.""",
{"ADCB": "A cannot come straight after S1 — first he must sit in the car (C).",
 "CADB": "correct — S1, C, A, D, B, S2.",
 "CDBA": "puts A after B, breaking the link between B's ringing telephone and S2.",
 "DBCA": "he cannot sit in the car (C) after going up to the door (D)."},
r"Car → thought → door → phone ringing → “It kept ringing”.")
L(73, r"""-> S1: Sulpicia goes to visit a friend; S2: her husband weeps at the serious situation.
-> D says she came home half dead and threw herself on the bed; B asks whether her circulation had stopped.
-> A (her clothes were loosened and three pairs of hands helped) is answered by C (“None too many, forsooth!”).""",
{"DBAC": "correct — S1, D, B, A, C, S2.",
 "BCAD": "B cannot open the paragraph — we do not yet know she is ill.",
 "ADCB": "A cannot come before D, which first tells us she fell ill.",
 "BDCA": "B before D asks about her circulation before we know anything is wrong."},
r"Event (D) → worry (B) → help (A) → comment on the help (C).")
L(74, r"""-> The sentence is a hypothetical (unreal) condition about the future: “If I …, I would …”.
-> In such a sentence “would” is not used in the if-clause.
-> “If I were to be laid off again” is the correct form for an imagined future event.""",
{"will be laid off again": "“will” is not used in the if-clause with “would” in the main clause.",
 "had been laid off again": "past perfect needs “would have considered” in the main clause.",
 "were to be laid off again": "correct — “were to” expresses an imagined future condition.",
 "No improvement required": "wrong — “would be” in the if-clause is an error."},
r"If I were to …, I would … (no “would” after “if”).")
L(75, r"""-> The article “an” is used before a vowel sound.
-> “air” begins with the vowel sound /e/, so it must be “an air pump”, not “a air pump”.
-> The other parts of the sentence are correct.""",
{"Our bicycles are fully": "no error.",
 "equipped, with head and": "no error.",
 "tail lights, gear shifts, a bell,": "no error — “a bell” is correct.",
 "and even a air pump.": "error — it should be “and even an air pump”."},
r"Vowel sound → an (an air pump, an hour); consonant sound → a (a bell, a uniform).")
L(76, r"""-> In the sentence, “such as” comes before a list: critical thinking, clear communication, close reading and research.
-> These are examples of “the skills acquired in these fields”.
-> “Such as” is used to introduce examples.""",
{"To introduce a comparison": "a comparison would use “like … than” or “as … as”; nothing is compared here.",
 "To introduce examples": "correct — it lists examples of the skills.",
 "To show cause and effect": "that needs “because” or “so”.",
 "To indicate contrast": "that needs “but” or “however”."},
r"such as / for example / like → examples.")
L(77, r"""-> In the sentence, “find” has an object: “fulfilling jobs”.
-> A verb that takes a direct object is a transitive verb.
-> Graduates find (what?) — fulfilling jobs.""",
{"Linking verb": "a linking verb (is, seem, become) joins the subject to a description; “find jobs” is an action on an object.",
 "Auxiliary verb": "a helping verb (is, has, will); “find” is the main verb here.",
 "Intransitive verb": "an intransitive verb has no object, but “find” has the object “jobs”.",
 "Transitive verb": "correct — it takes the object “fulfilling jobs”."},
r"Ask “what?” after the verb — if there is an answer, the verb is transitive.")
L(78, r"""-> The passage says editors make sure written materials are “polished” and meet high standards of quality.
-> So “polished” here means refined, carefully improved.
-> The words “high standards of quality” confirm this meaning.""",
{"rough and unfinished": "the opposite of polished.",
 "removed completely": "unrelated — nothing is removed.",
 "broken or damaged": "the opposite of the meaning in the passage.",
 "improved to a high standard": "correct — refined and of high quality."},
r"Polished writing = refined, error-free writing.")
L(79, r"""-> The last paragraph says the degree gives “versatile, transferable skills” that help people adapt to a changing job market.
-> “Versatile” means able to adapt or be used in many different ways.
-> The word “transferable” next to it supports this meaning.""",
{"Limited to one skill": "the opposite of versatile.",
 "Able to adapt or be used in many ways": "correct — the meaning in the passage.",
 "Difficult to learn": "unrelated to the word.",
 "Very simple and plain": "unrelated — versatile means many-sided, not plain."},
r"Versatile = many-sided, adaptable.")
L(80, r"""-> The passage begins by saying literature and language studies open careers far beyond teaching.
-> It then lists publishing, writing, editing, law, journalism, media and digital marketing.
-> It ends by saying the degree gives versatile, transferable skills for a competitive job market.""",
{"Studying literature develops skills that have broad applications in many careers including publishing, writing, law, and digital media.": "correct — this sums up the whole passage.",
 "Literature and language degrees limit career options primarily to teaching.": "the passage says the opposite — careers go far beyond teaching.",
 "Only writers and editors find good jobs after studying literature.": "too narrow — law, media, marketing and others are also named.",
 "Careers in literature do not contribute much to society or the economy.": "contradicts the passage, which says they add to culture and employment."},
r"Main idea = what the first and last paragraphs agree on.")
