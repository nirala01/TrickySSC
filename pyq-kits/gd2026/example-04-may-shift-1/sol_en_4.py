from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “Trials and tribulations” means the troubles and hardships a person goes through.
-> Example: After all the trials and tribulations of the move, they finally settled into their new home.""",
{"A situation in which one is placed under extreme pressure or stress and expected as a means of testing one's ability to learn or perform": "this describes being put to the test under pressure (“trial by fire”), not a series of hardships.",
 "Various difficulties, hardships, or problems, especially those that test one's courage, endurance, or resolve": "correct — this is exactly the meaning of the idiom.",
 "A preliminary or tentative execution of a plan or idea in order to gauge the interest or approval of someone else, especially the public.": "this is the meaning of “trial balloon”.",
 "A process of determining the correct way in which to do something by making multiple attempts and learning from any possible failures or mistakes": "this is “trial and error”."},
r"Tribulation = suffering; trials and tribulations = hardships.")
L(62, r"""-> “To fit the bill” means to be exactly what is needed or suitable.
-> Example: We needed a quiet place to study, and the library fitted the bill.""",
{"To become very or unreasonably angry or upset": "this is the meaning of “to throw a fit”.",
 "To cram too much into a small container or space": "no such meaning; this only plays on the word “fit”.",
 "To be helpful, useful, or what is needed in a certain situation": "correct — this is what “fit the bill” means.",
 "To occupy only a very small space when written down": "this has nothing to do with the idiom."},
r"Fit the bill = suit the purpose.")
L(63, r"""-> “Abhor” means to hate something very strongly.
-> Example: She abhors cruelty to animals.""",
{"Like": "opposite in feeling, so not a synonym.",
 "Adore": "means to love deeply — an antonym.",
 "Hate": "correct — the closest synonym of “abhor”.",
 "Love": "an antonym of “abhor”."},
r"Abhor ≈ detest ≈ loathe ≈ hate.")
L(64, r"""-> The correct spelling is “Telecommunication”, with a double “m”.
-> It comes from “tele” (far) + “communication”, and “communication” is always spelt with “mm”.""",
{"Transmutation": "spelt correctly.",
 "Temperamental": "spelt correctly.",
 "Telecomunication": "misspelt — one “m” is missing; correct form is “Telecommunication”.",
 "Transcontinental": "spelt correctly."},
r"Communication, community, commute — all take a double m.")
L(65, r"""-> The correct spelling is “Unanimous”, ending in “-ous”.
-> It means agreed by everyone, as in “a unanimous decision”.""",
{"Unanimos": "misspelt — the “u” before the final “s” is missing; correct form is “Unanimous”.",
 "Ubiquitous": "spelt correctly; it means present everywhere.",
 "utilitarian": "spelt correctly; it means designed to be useful rather than attractive.",
 "Unobtrusive": "spelt correctly; it means not noticeable."},
r"Adjectives of this type end in “-ous”: unanimous, ubiquitous.")
L(66, r"""-> “Edge” is the outer limit or border of something.
-> Its opposite is the middle point, the centre.""",
{"Border": "a synonym of edge.",
 "Rim": "the edge of a round object — a synonym.",
 "Center": "correct — the middle is the opposite of the edge.",
 "Margin": "the edge of a page or area — a synonym."},
r"Edge, border, rim, margin are all outer parts; the centre is the opposite.")
L(67, r"""-> A “doppelganger” is a double of a living person, often thought of as a ghostly look-alike.
-> The word comes from German, meaning “double-goer”.""",
{"Sybarite": "a person who loves luxury and pleasure.",
 "Doppelganger": "correct — a ghostly double of a living person.",
 "Deja-vu": "the feeling that you have already experienced something happening now.",
 "Neophyte": "a beginner in a subject or skill."},
r"Doppel = double.")
L(68, r"""-> The sentence says they did one thing and also another: they paid his salary and also paid his travel expenses.
-> “Besides” means “in addition to”, so it fits the meaning of adding one benefit to another.""",
{"Unless": "means “except if” — it shows a condition, not an addition.",
 "Notwithstanding": "means “in spite of” — it shows contrast, not addition.",
 "Besides": "correct — “besides paying him” means “in addition to paying him”.",
 "Inasmuch as": "means “because” — it gives a reason, not an addition."},
r"Besides = in addition to; beside = next to.")
L(69, r"""-> In the passive sentence, “will be inaugurated” is in the simple future tense.
-> In active voice the doer comes first and the tense stays the same: “will inaugurate”.""",
{"The President of the university inaugurates the newly constructed library next week.": "simple present tense — the tense has changed.",
 "The President of the university inaugurated the newly constructed library next week.": "past tense, which also clashes with “next week”.",
 "The President of the university will inaugurate the newly constructed library next week.": "correct — simple future tense kept, with the doer as subject.",
 "The President of the university has inaugurated the newly constructed library next week.": "present perfect tense — wrong tense."},
r"will be + V3 (passive) → will + V1 (active).")
L(70, r"""-> “Let + object + be + V3” is the passive form of an imperative (command) sentence.
-> Its active form is the plain command: verb + object.""",
{"Please vacate the premises immediately.": "adds “Please”, which turns the order into a request.",
 "Vacate the premises immediately.": "correct — the plain command is the active form.",
 "You are let to vacate the premises immediately.": "ungrammatical; “let” is not used this way.",
 "The premises is to be vacated immediately.": "still passive, and “premises” needs “are”."},
r"Let it be done → Do it.")
L(71, r"""-> We feel sorry “for” a person who is in trouble.
-> “Sorry about” is used for a situation or a mistake, not for the people affected.""",
{"for": "correct — “sorry for the flood victims”.",
 "about": "used with events or mistakes (“sorry about the delay”), not with people.",
 "at": "not used with “sorry”.",
 "in": "not used with “sorry”."},
r"Sorry for someone; sorry about something.")
L(72, r"""-> With “neither … nor”, the verb agrees with the subject closer to it.
-> Here the closer subject is “the members”, which is plural, so the verb must be “were”.""",
{"was able to find out a solution": "keeps the singular “was”, so the error stays.",
 "were able to find a solution": "correct — the plural verb agrees with “the members”.",
 "had been able to find for a solution": "wrong tense and adds an unnecessary “for”.",
 "No improvement required": "wrong, because “was” does not agree with “members”."},
r"Neither A nor B → verb follows B.")
L(73, r"""-> S1 sets the scene: a dull August afternoon with nothing to hunt.
-> C links to S1 through the Bristol Channel and brings in the guests; D adds that the guests were not bored; B says their attention was fixed on Mr. Cornelius Appin; A introduces him as the guest with the vaguest reputation, which leads to S2 (“Someone had said he was clever”).""",
{"DBCA": "starts with D, but “And, in spite of …” needs C before it to introduce the gathering.",
 "DCBA": "again opens with D, which cannot follow S1 directly.",
 "CDBA": "correct — C → D → B → A gives a smooth flow into S2.",
 "BDCA": "B names Mr. Appin before the gathering is described."},
r"Look for linking words (“And”, “he”) to find which sentence must come after which.")
L(74, r"""-> S1 states the aim — to conquer the fear of Red.
-> D tells what the writer did (wrote a poem); A says it was the first “journalism in verse”; C shows the whole street learnt it; B describes meeting Red one morning, which leads to S2 (“His eyes seemed to bore through me”).""",
{"BCDA": "puts the meeting with Red before the poem is written.",
 "DBCA": "places the meeting before the poem became famous, breaking the cause and effect.",
 "ACDB": "A (“This was my first piece …”) needs D before it to say what “this” is.",
 "DACB": "correct — D → A → C → B flows logically into S2."},
r"A pronoun like “This” needs the sentence it refers to placed before it.")
L(75, r"""-> The subject of the sentence is “he”, so the reflexive pronoun must be “himself”, not “oneself”.
-> The phrase “no one to blame but …” must be kept to keep the meaning.""",
{"there was nothing to blame but himself": "changes “no one” to “nothing”, which is wrong for a person.",
 "there was no one to blame himself": "drops “but”, so the meaning is lost.",
 "there was no one to blame but himself": "correct — “himself” agrees with “he”.",
 "No improvement required": "wrong, because “oneself” does not agree with “he”."},
r"Reflexive pronoun must match the subject: he → himself.")
L(76, r"""-> The action began thousands of years ago and continues today, so the present perfect tense is needed.
-> The subject “Horses” is plural, so the verb is “have been”.""",
{"was": "singular and past — does not fit “Horses” or “for thousands of years”.",
 "had": "not a complete verb here and does not show a continuing state.",
 "will be": "future tense, but the passage talks about the past up to now.",
 "have been": "correct — present perfect with a plural subject."},
r"“For + period up to now” → present perfect.")
L(77, r"""-> Carts were pulled from one side of the villages to the other.
-> “Across” means from one side to the other.""",
{"behind": "means at the back of — carts are not pulled “behind villages”.",
 "across": "correct — carts moved across villages.",
 "into": "means entering, which does not fit the idea of travelling through villages.",
 "onto": "means moving on top of a surface."},
r"Across = from one side to the other.")
L(78, r"""-> “Untamed” means not controlled or trained by people — wild.
-> In the passage it describes the free, wild spirit of a running horse.""",
{"Wild and uncontrolled": "correct — the exact meaning of “untamed”.",
 "Carefully trained": "the opposite of untamed.",
 "Polite and obedient": "describes a tamed animal, the opposite meaning.",
 "Weak and fragile": "has nothing to do with being untamed."},
r"Tame = trained; un-tamed = wild.")
L(79, r"""-> The subject “it” (the horse) is singular and the sentence states a general truth.
-> So the simple present tense with “-s” is needed: “depends”.""",
{"depend": "base form; does not agree with “it”.",
 "depended": "past tense, but the sentence gives a present general truth.",
 "depends": "correct — singular subject + simple present.",
 "depending": "a participle, not a complete verb."},
r"He/she/it + V1 + s.")
L(80, r"""-> “Incredible” means hard to believe because it is so amazing.
-> Its opposite is “ordinary”, meaning normal and not special.""",
{"Amazing": "a synonym of incredible.",
 "ordinary": "correct — the opposite of incredible.",
 "Wonderful": "a synonym of incredible.",
 "Extraordinary": "a synonym of incredible."},
r"Three options mean the same thing; the odd one out is the antonym.")
