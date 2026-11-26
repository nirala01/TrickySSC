from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> An idiom is a fixed phrase whose meaning differs from the meanings of its words.
-> “To leave someone to twist in the wind” means to leave a person alone in a difficult situation without help.
-> Sohan could not handle the situation, so he abandoned his friend to face it alone — the idiom fits exactly.""",
{"twist in the wind": "correct — the fixed idiom for leaving someone helpless in trouble.",
 "twist in the machine": "not an idiom (a mix-up with “a spanner in the works”).",
 "twist in the grate": "not a recognised English idiom.",
 "twist in the vice": "not an idiom; a vice is a tool that holds things tight."},
r"Twist in the wind = left hanging, alone, with no help.")
L(62, r"""-> “The heavens open” is an idiom meaning it suddenly starts to rain very heavily.
-> Example: We had just left home when the heavens opened.
-> The other options only replace “heavens” with other words, which breaks the fixed phrase.""",
{"The heavens open": "correct — means it starts to rain heavily.",
 "The stars open": "not an idiom.",
 "The lightening open": "not an idiom (and “lightening” means making lighter; the flash is “lightning”).",
 "Zeus' pitcher open": "not an idiom."},
r"Heavens open → sky pours rain.")
L(63, r"""-> “Aroma” means a pleasant, distinctive smell, especially of food or drink.
-> Example: the aroma of fresh coffee.
-> So its closest synonym is a word that also means a pleasant smell.""",
{"Noise": "a loud or unpleasant sound — unrelated.",
 "Fragrance": "correct — a pleasant smell, the same as aroma.",
 "Delight": "great pleasure — a feeling, not a smell.",
 "Insight": "deep understanding — unrelated."},
r"Aroma ≈ fragrance ≈ scent.")
L(64, r"""-> “Praise” means to express approval or admiration of someone or something.
-> Example: The coach praised the team for its effort.
-> Its synonym must also mean showing approval.""",
{"Criticize": "to find fault — the opposite of praise.",
 "Blame": "to hold someone responsible for a fault — opposite in spirit.",
 "Applaud": "correct — to praise or approve, often by clapping.",
 "complain": "to express dissatisfaction — opposite in spirit."},
r"Praise ≈ applaud ≈ commend.")
L(65, r"""-> The correct spelling is “Valedictory” (vale + dictory), meaning a farewell speech or address.
-> The option spells it “Validictory”, using i in place of e in the second syllable.
-> The other three words are spelt correctly.""",
{"Voracious": "correctly spelt — very eager or greedy (a voracious reader).",
 "Validictory": "misspelt — the correct form is Valedictory.",
 "Vivacious": "correctly spelt — lively and full of spirit.",
 "Vindictive": "correctly spelt — wanting revenge."},
r"Valedictory comes from Latin vale (farewell) — vale-, not vali-.")
L(66, r"""-> “Stay” means to remain in a place.
-> Its antonym must mean to leave a place.
-> Example: She decided to stay, but her brother departed early.""",
{"Depart": "correct — to leave, the opposite of stay.",
 "Settle": "to make a place one's home — close to stay.",
 "Delay": "to put off or make late — not an opposite.",
 "Reside": "to live in a place — similar to stay."},
r"Stay ↔ depart (remain ↔ leave).")
L(67, r"""-> The person who supervises the making of a film — guiding the actors, the camera work and the overall creative vision — is the director.
-> The producer arranges the money and the business side, not the actual making of the film.
-> Example: Satyajit Ray directed “Pather Panchali”.""",
{"Producer": "finances and manages the project, not the making itself.",
 "Editor": "cuts and arranges the recorded shots after filming.",
 "Director": "correct — supervises and controls the making of the film.",
 "Choreographer": "designs the dance movements."},
r"Director directs the film; producer pays for it.")
L(68, r"""-> “Welter” means a large, confused or disorderly mass of things.
-> Example: a welter of papers on his desk.
-> The other words have quite different meanings.""",
{"Peri": "a beautiful fairy in Persian folklore — unrelated.",
 "Welter": "correct — a large and confused mass of things.",
 "Jeopardy": "danger of loss or harm.",
 "Archetype": "a perfect or typical example of something."},
r"Welter = a jumble, a confused heap.")
L(69, r"""-> “Learn by heart” is a fixed expression meaning to memorise something completely.
-> So the poems are learnt “by heart”.
-> Other prepositions do not form this expression.""",
{"through": "wrong — “through heart” is not used.",
 "in": "wrong — “in heart” is not the idiom.",
 "on": "wrong — “on heart” is not used.",
 "by": "correct — learn by heart = memorise."},
r"Learn/know something by heart = memorise it.")
L(70, r"""-> The sentence is in the simple present tense: She stitches fine dresses for the queen.
-> Passive of the simple present: object + is/are + past participle + by + subject.
-> “Fine dresses” is plural, so: Fine dresses are stitched by her for the queen.""",
{"Fine dresses were stitched by her for the queen.": "wrong — “were” changes the tense to the past.",
 "Fine dresses for the queen were stitched by her.": "wrong — past tense again.",
 "Fine dresses are stitched by her for the queen.": "correct — present tense kept, plural verb “are”.",
 "Fine dresses are stitch for the queen by her.": "wrong — the passive needs the past participle “stitched”."},
r"Simple present passive = is/are + V3.")
L(71, r"""-> The passive sentence is in the present perfect: has been introduced.
-> In the active voice the doer comes first and the tense stays present perfect: has introduced.
-> Active: The aviation authority has introduced a new set of safety regulations across all domestic airports.""",
{"The aviation authority introduces a new set of safety regulations across all domestic airports.": "wrong — simple present, tense changed.",
 "The aviation authority introduced a new set of safety regulations across all domestic airports.": "wrong — simple past, tense changed.",
 "The aviation authority has introduced a new set of safety regulations across all domestic airports.": "correct — present perfect kept.",
 "The aviation authority will introduce a new set of safety regulations across all domestic airports.": "wrong — future tense."},
r"has been + V3 (passive) ↔ has + V3 (active).")
L(72, r"""-> The verb “enter” takes the preposition “into” when it means to begin or become part of an agreement, contract or discussion.
-> So: India has just entered into an agreement with Russia.
-> (Without a preposition, “enter” means to go into a place: enter the room.)""",
{"into": "correct — “enter into an agreement” is the fixed phrase.",
 "for": "wrong — “enter for” is used for competitions (enter for a race).",
 "in": "wrong — not used with agreement.",
 "to": "wrong — “enter to” is not standard."},
r"Enter INTO an agreement / a contract / a discussion.")
L(73, r"""-> With the present perfect continuous (have been waiting), a period of time takes “for”: for two hours.
-> “Since” is used with a point of time: since 10 a.m., since Monday.
-> So the correct part is “for the chief guest to arrive for two hours”.""",
{"to the chief guest's arrival since two hours": "wrong — “wait to” is wrong here and “since” is still used with a period.",
 "for the chief guest to arrive for two hours": "correct — “for” with the period of two hours.",
 "for the chief guest's arrival from two hours": "wrong — “from two hours” is incorrect.",
 "No improvement required": "wrong — “since two hours” is an error."},
r"Since + point of time; for + period of time.")
L(74, r"""-> S1 says they were close to land; C (“He looked at it with greedy eyes”) follows at once, because “it” refers to the land.
-> A then describes the land: a strip of silver beach and hills with vegetation.
-> B continues the description with the coconut trees, the houses and the church; D brings in Mrs Davidson, whom S2 describes (“She was dressed in black …”).
-> So the order is C, A, B, D.""",
{"ABCD": "wrong — C must come right after S1, since “it” means the land.",
 "CABD": "correct — land → he looks at it → the beach → the trees and church → Mrs Davidson.",
 "ADBC": "wrong — Mrs Davidson cannot come before the description ends; S2 follows her.",
 "BDAC": "wrong — B cannot open the description before A."},
r"Find the pronoun link: “it” in C needs the land from S1; “She” in S2 needs Mrs Davidson in D.")
L(75, r"""-> “Position” here is a singular countable noun (a job), so it needs an article.
-> The indefinite article “a” is used because no particular position has been mentioned before.
-> Correct: he was unable to secure a position at the prestigious university.""",
{"he was unable to secure a position": "correct — adds the needed article “a”.",
 "he was unable to secure some position": "wrong — “some position” sounds vague and unnatural here.",
 "he was unable to secure one position": "wrong — “one” stresses number, not a general job.",
 "No improvement required": "wrong — the countable noun “position” cannot stand without an article."},
r"Singular countable noun → needs a/an/the.")
L(76, r"""-> The blank describes the writing system: “the first known form of writing, ___ cuneiform”.
-> A past participle used like an adjective is needed: “called cuneiform” = which is called cuneiform.
-> Cuneiform is the wedge-shaped script of the Sumerians.""",
{"called": "correct — past participle meaning “which was named”.",
 "calling": "wrong — present participle; the writing does not call anything.",
 "call": "wrong — base verb does not fit after a comma here.",
 "have called": "wrong — a finite verb cannot sit in this phrase."},
r"Noun, called X = a noun that is named X.")
L(77, r"""-> The sentence says writing enabled the recording of events, laws and trade, ___ the foundation for future generations.
-> A participle meaning “setting up” or “laying down” is needed: establishing the foundation.
-> The writing system helped later generations understand their past.""",
{"establishing": "correct — creating or setting up the foundation.",
 "demolition": "wrong — a noun meaning destruction, the opposite idea.",
 "analyzing": "wrong — one does not analyse a foundation for future generations.",
 "strengthening": "wrong — you can only strengthen a foundation that already exists; this was the first."},
r"Something new → establish (set up) its foundation.")
L(78, r"""-> The phrase is “careful planning and ___ skilled workforce”.
-> “Workforce” is a singular countable noun mentioned for the first time, so the indefinite article is needed.
-> “Skilled” begins with a consonant sound, so the article is “a”: a skilled workforce.""",
{"the": "wrong — no particular workforce has been mentioned before.",
 "an": "wrong — “skilled” begins with a consonant sound.",
 "a": "correct — indefinite article before a consonant sound.",
 "No article": "wrong — a singular countable noun needs an article here."},
r"First mention + consonant sound → a.")
L(79, r"""-> Wealth was concentrated in the hands of the elite, which led to ___ between the ruling class and the common people.
-> The word must mean inequality or a big difference: disparity.
-> The question itself says the word describes inequality.""",
{"harmony": "wrong — agreement and peace, the opposite.",
 "disparity": "correct — a great difference or inequality.",
 "equality": "wrong — the opposite of the meaning needed.",
 "concord": "wrong — agreement, the opposite idea."},
r"Rich elite vs. common people → disparity.")
L(80, r"""-> The Indus Valley Civilization declined “for reasons that remain ___”.
-> The next sentence says scholars only argue about possible causes, so the reasons are not known for certain: unclear.
-> “Remain” is followed by an adjective here.""",
{"clear": "wrong — scholars still argue, so the reasons are not clear.",
 "cleared": "wrong — a past participle meaning removed or approved.",
 "unclear": "correct — not known or understood for certain.",
 "uncleared": "wrong — means not yet removed or approved (e.g. uncleared land)."},
r"Scholars still debate → reasons remain unclear.")
