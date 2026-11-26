from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “Toot (or blow) one's own horn” means to boast about one's own achievements and abilities.
-> The sentence says Radhika does not boast — she simply goes on working and succeeding.
-> So the blank needs “toot her own horn”.""",
{"sharpen her own horn": "not an idiom.",
 "toot her own horn": "correct — it means to boast about oneself.",
 "colour her own horn": "not an idiom.",
 "anoint her own horn": "not an idiom."},
r"Toot/blow your own horn (trumpet) = boast.")
L(62, r"""-> “Reliable” means that can be trusted or depended upon.
-> Example: He is a reliable friend who always keeps his word.
-> So the synonym is “trustworthy”.""",
{"Trustworthy": "correct — able to be trusted.",
 "Uncertain": "nearly opposite — not sure or not dependable.",
 "Untrue": "means false or not faithful; not a synonym.",
 "False": "means not true or not loyal; the opposite idea."},
r"Reliable = trustworthy = dependable.")
L(63, r"""-> We must find the one underlined word that is spelt wrongly.
-> “Musician's”, “profound” and “symbolism” are spelt correctly.
-> The correct spelling is “melodies” (m-e-l-o-d-i-e-s); the sentence has “meloudies”, with an extra “u”.""",
{"musician": "correctly spelt.",
 "profound": "correctly spelt.",
 "symbolism": "correctly spelt.",
 "meloudies": "misspelt — the correct form is “melodies”."},
r"Melody → melodies (y → ies); no “u” after the “o”.")
L(64, r"""-> We must find the misspelt word.
-> The correct spelling is “silhouette” (s-i-l-h-o-u-e-t-t-e) — a dark outline seen against a light background.
-> The option leaves out the silent “h”.""",
{"silouette": "misspelt — the silent “h” after “sil” is missing.",
 "Etiquette": "correctly spelt — rules of polite behaviour.",
 "Corvette": "correctly spelt — a small fast warship.",
 "Cassette": "correctly spelt — a small case holding tape."},
r"Sil-H-ouette: silent h, double t, ends in -ette.")
L(65, r"""-> “Filled” means made full.
-> Its opposite is a word meaning made empty.
-> So the antonym is “emptied”.""",
{"Packed": "a synonym — full of things or people.",
 "Crowded": "a synonym — full of people.",
 "Loaded": "a synonym — filled with a load.",
 "Emptied": "correct — made empty, the opposite of filled."},
r"Filled ↔ emptied.")
L(66, r"""-> These four words sound alike but have different meanings and spellings (homophones).
-> A tailor joins cloth with needle and thread before (or while) stitching it — that is “sew”.
-> So the blank needs “sew”.""",
{"sow": "means to plant seeds.",
 "sew": "correct — to join cloth with a needle and thread.",
 "so": "a conjunction or adverb (therefore / very).",
 "saw": "past tense of “see”, or a tool for cutting wood."},
r"Sow seeds, sew cloth, saw wood.")
L(67, r"""-> A word with the same spelling or the same sound as another word but a different meaning is a “homonym”.
-> Example: “bank” (of a river) and “bank” (for money).
-> “Homo-” means same and “-nym” means name.""",
{"Homonym": "correct — same spelling or sound, different meaning.",
 "Synonym": "a word with the same or similar meaning.",
 "Antonym": "a word with the opposite meaning.",
 "Acronym": "a word formed from first letters, such as NASA."},
r"Homonym = same name, different meaning.")
L(68, r"""-> The teachers worked on a holiday, so they were allowed two days' leave instead of that holiday.
-> “In lieu of” means “instead of” or “in place of”.
-> So the blank needs “in lieu of”.""",
{"in addition to": "means “as well as”; leave is given instead of the holiday work, not besides it.",
 "because of": "would need “because of working”, but the idea is compensation, i.e. in place of the holiday.",
 "in lieu of": "correct — instead of / in exchange for.",
 "regarding": "means “about”; it does not fit."},
r"In lieu of = instead of (compensatory leave).")
L(69, r"""-> The active sentence is in the simple past: “The two kings signed the treaty.”
-> Passive of the simple past = was/were + past participle: “The treaty was signed by the two kings.”
-> The rest of the sentence (“just before the battle began”) stays the same.""",
{"The treaty had been signed by the two kings just before the battle began.": "wrong — “had been signed” is past perfect, but the active verb is simple past.",
 "The treaty was signed by the two kings just before the battle began.": "correct — simple past passive.",
 "The treaty is signed by the two kings just before the battle began.": "wrong — “is signed” is present tense.",
 "The treaty will signed by the two kings just before the battle began.": "wrong — future and ungrammatical (“will be signed” would be needed)."},
r"Simple past: V2 → was/were + V3.")
L(70, r"""-> The passive sentence is in the simple past: “were attended by”.
-> In the active voice the doer (thousands of enthusiastic supporters) becomes the subject and the verb becomes simple past: “attended”.
-> So: “Thousands of enthusiastic supporters attended the victory celebrations.”""",
{"Thousands of enthusiastic supporters attend the victory celebrations.": "wrong — simple present.",
 "Thousands of enthusiastic supporters attended the victory celebrations.": "correct — simple past, as in the passive.",
 "Thousands of enthusiastic supporters are attending the victory celebrations.": "wrong — present continuous.",
 "Thousands of enthusiastic supporters had attended the victory celebrations.": "wrong — past perfect."},
r"was/were + V3 → V2 in the active voice.")
L(71, r"""-> “Go under the knife” is an idiom meaning to have a surgical operation.
-> The patient is in the ICU after yesterday's operation.
-> So the blank needs “under”.""",
{"over": "“go over” means to examine or review; it does not fit.",
 "under": "correct — “went under the knife” = had surgery.",
 "below": "not used in this idiom.",
 "after": "“go after” means to chase; it does not fit."},
r"Under the knife = surgery.")
L(72, r"""-> S1 says the doves flew into the net and were caught. The natural next sentence is the question “What was to be done?” (C).
-> A follows with the question of escape (“How could they escape from certain death?”), and D answers it — there was no escape, no hope.
-> B then shows the sudden turn — they flew off together with the net — leading to S2, where they escape and the fowler is surprised. Order: C A D B.""",
{"CDBA": "wrong — B (flying away) cannot come before A (asking how to escape).",
 "CADB": "correct — trouble → question → hopelessness → escape.",
 "DCAB": "wrong — “no escape” (D) must answer the question in A, so it cannot open.",
 "DBCA": "wrong — the escape in B cannot come before the questions C and A."},
r"Problem → question → no hope → sudden escape.")
L(73, r"""-> S1 introduces a hawker who carried goods on an ass. D comes next — it explains his habit of dressing the ass in a lion's skin at every place.
-> A then narrows to “one day” in a village, and C follows: the watchmen thought it was a lion and spread the news.
-> B — the villagers came out with weapons and drums — leads to S2, where the ass brays in fear. Order: D A C B.""",
{"BDCA": "wrong — the villagers (B) cannot come out before the story of the ass is told.",
 "ACBD": "wrong — the general habit (D) must come before “one day” (A).",
 "CDBA": "wrong — C mentions “him” (the disguised ass) before he is introduced.",
 "DACB": "correct — habit → one day → news spreads → villagers come."},
r"General habit first, then “one day …”, then the result.")
L(74, r"""-> The idiom is “take the bull by the horns” — to face a difficult situation boldly and directly.
-> “Take the bull by the head” is not the idiom, so the sentence needs improvement.
-> Correct sentence: We must take the bull by the horns and resolve all pending issues if we want progress.""",
{"take the bull by the tail": "not the idiom.",
 "pull the bull by its ears": "not the idiom.",
 "take the bull by the horns": "correct — to deal with a problem boldly.",
 "No improvement required": "wrong — “by the head” is not the idiom."},
r"Take the bull by the horns = face the problem head-on.")
L(75, r"""-> “Hour” is a countable noun, so it cannot stand alone after “for”; it needs “an hour” or the plural “hours”.
-> Here the sense is a long time, so the correct phrase is “might drive on for hours”.
-> Correct sentence: If you are looking for a free parking space, you might drive on for hours until you find one.""",
{"If you are looking for": "no error — present continuous in the if-clause.",
 "a free parking space, you": "no error — article “a” before a singular countable noun.",
 "might drive on for hour": "error — “for hour” should be “for hours” (or “for an hour”).",
 "until you find one.": "no error — “one” correctly replaces “a parking space”."},
r"A singular countable noun needs a/an/the — or make it plural.")
L(76, r"""-> The subject “Calcium” is a singular, uncountable noun.
-> The passage describes a general fact, so the verb is in the simple present.
-> So the sentence needs “is”: Calcium … is primarily associated with …""",
{"are": "wrong — plural verb with a singular subject.",
 "had": "wrong — “had associated” does not fit the passive meaning or the present-tense fact.",
 "Was": "wrong — past tense for a general truth (and wrongly capitalised).",
 "is": "correct — singular, simple present."},
r"Scientific facts → simple present; singular subject → is.")
L(77, r"""-> A declarative sentence makes a statement and ends with a full stop.
-> “A deficiency of iron often leads to anemia.” states a fact.
-> So it is a declarative sentence.""",
{"Exclamatory": "shows strong feeling and ends with “!”.",
 "Interrogative": "asks a question and ends with “?”.",
 "Declarative": "correct — it makes a statement.",
 "Imperative": "gives a command or request."},
r"Statement = declarative; question = interrogative; command = imperative; feeling = exclamatory.")
L(78, r"""-> “Indispensable” means absolutely necessary — something one cannot do without.
-> The passage says iron and calcium are needed for healthy growth.
-> So the meaning is “essential”.""",
{"harmful": "wrong — the passage says these minerals are needed, not harmful.",
 "essential": "correct — absolutely necessary.",
 "temporary": "wrong — lasting only a short time.",
 "avoidable": "the opposite — something that can be done without."},
r"In-dispens-able = cannot be dispensed with = essential.")
L(79, r"""-> “Fragile” means easily broken or damaged.
-> In osteoporosis the bones become porous and break easily.
-> The opposite of fragile is “strong”.""",
{"weak": "a synonym — lacking strength.",
 "delicate": "a synonym — easily damaged.",
 "brittle": "a synonym — hard but easily broken.",
 "strong": "correct — the opposite of fragile."},
r"Fragile = brittle = weak ↔ strong.")
L(80, r"""-> The second paragraph says pregnant and lactating mothers require additional calcium.
-> The reason given is that their bodies support not only their own needs but also those of the growing child.
-> The answer must repeat this reason.""",
{"Because they eat less food": "not stated in the passage.",
 "Because of their role in household work": "not stated in the passage.",
 "Because their bodies support both their own needs and those of the growing child": "correct — this is the reason given in the passage.",
 "Because they avoid dairy products": "not stated; the passage mentions poor diets only as a general cause."},
r"Find the sentence in the passage and match its reason.")
