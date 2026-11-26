from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “When (or where) the rubber meets the road” comes from a tyre touching the road — the moment a car is really tested.
-> It means the point at which an effort, plan or idea is put to a real test, when things become truly challenging.
-> Example: The plan looks good on paper, but the launch day is when the rubber meets the road.""",
{"Good intentions do not matter if a person's actions lead to bad outcomes": "this is the meaning of “the road to hell is paved with good intentions”.",
 "A problem that arises and interferes with forward progress usually only temporary": "this describes a “bump in the road” or a hiccup.",
 "A town or city that is particularly small, unremarkable, or unpopulated": "this describes a “one-horse town”.",
 "The point at which someone's or something's efforts, resolve, or viability are put to the test; the point at which things become truly or meaningfully challenging": "correct — the moment of the real test."},
r"Rubber meets the road = the moment of the real test.")
L(62, r"""-> “Wiggle room” is the small space in which something can still move (wiggle).
-> As an idiom it means freedom, time or space to change a plan or decision if needed.
-> Example: The budget leaves us very little wiggle room.""",
{"A secluded, private place hidden from the knowledge of the public": "describes a hideaway, not wiggle room.",
 "The space, time, or freedom to make changes as needed": "correct — scope for change or adjustment.",
 "To move quickly; to hurry or hurry up; get a move on": "the meaning of “get a wiggle on”, a different phrase.",
 "A lavatory, restroom, or bathroom": "the meaning of informal words like “loo” or “restroom”."},
r"Wiggle room = room to adjust.")
L(63, r"""-> We must find the one word that is spelt correctly.
-> “Sanguine” (s-a-n-g-u-i-n-e) is correct; it means cheerfully hopeful.
-> The other three are wrong forms of salient, sentient and spurious.""",
{"seliant": "misspelt — the correct word is “salient” (most noticeable).",
 "Sanguine": "correctly spelt — optimistic, hopeful.",
 "Senteint": "misspelt — the correct word is “sentient” (able to feel).",
 "spurrious": "misspelt — the correct word is “spurious” (false), with one “r”."},
r"Salient, sentient, spurious, sanguine — learn the vowels: sal-, sent-ient, spur-ious.")
L(64, r"""-> “Special” means better or different from what is usual.
-> A word with the same meaning is “unique” — being the only one of its kind.
-> The other three mean the opposite idea.""",
{"common": "an antonym — found everywhere.",
 "ordinary": "an antonym — normal, not special.",
 "Unique": "correct — one of a kind, special.",
 "Usual": "an antonym — normal or expected."},
r"Special ≈ unique; common/ordinary/usual are its opposites.")
L(65, r"""-> We must find the misspelt word.
-> The correct spelling is “compatible” (c-o-m-p-a-t-i-b-l-e) — able to exist or work together.
-> Words ending in “-ible” and “-able” are often confused; “compatible” takes “-ible”.""",
{"Predictable": "correctly spelt.",
 "Valuable": "correctly spelt.",
 "Sociable": "correctly spelt.",
 "Compatable": "misspelt — the correct form is “compatible”."},
r"Compat-IBLE, but predict-ABLE, valu-ABLE, soci-ABLE.")
L(66, r"""-> “Facilitate” means to make an action or process easier.
-> Its opposite is a word meaning to make it harder or to block it.
-> So the antonym is “impede”.""",
{"impede": "correct — to delay or block, the opposite of facilitate.",
 "Assist": "a synonym — to help.",
 "Help": "a synonym — to make something easier.",
 "Aid": "a synonym — to help or support."},
r"Facilitate ↔ impede (hinder, obstruct).")
L(67, r"""-> “Phobia” means an extreme fear.
-> “Agora” is Greek for a market place or open public space.
-> So the fear of open spaces or crowds is “agoraphobia”.""",
{"Arachnophobia": "fear of spiders.",
 "Agoraphobia": "correct — fear of open spaces or crowds.",
 "Astraphobia": "fear of thunder and lightning.",
 "Pyrophobia": "fear of fire."},
r"Agora = open place; arachne = spider; astra = lightning; pyro = fire.")
L(68, r"""-> The active sentence has “needs to finish” (to + base verb) with the object “this task”.
-> In the passive, “to + verb” becomes “to be + past participle”: to be finished.
-> So the passive is “The task needs to be finished by him by evening.”""",
{"The task needs to finished by him by evening.": "wrong — “be” is missing before “finished”.",
 "The task needs to be finished by him by evening.": "correct — to be + past participle.",
 "The task needs to be finish by him by evening.": "wrong — the past participle “finished” is needed.",
 "The task needs to finish by him by evening.": "wrong — this is not passive."},
r"to + V1 → to be + V3 in the passive.")
L(69, r"""-> The active sentence is in the past perfect question form: Had + subject + V3 + object?
-> In the passive, the past perfect becomes “had been + V3”, and the object comes first.
-> So: “Had all the people been evacuated by the government before the tsunami?”""",
{"Were all the people evacuated by the government before the tsunami?": "wrong — past simple passive; the tense is changed.",
 "Are all the people evacuated by the government before the tsunami?": "wrong — present tense.",
 "Have all the people been evacuated by the government before the tsunami?": "wrong — present perfect.",
 "Had all the people been evacuated by the government before the tsunami?": "correct — past perfect passive (had been + V3)."},
r"Past perfect: had + V3 → had been + V3.")
L(70, r"""-> We paint something with a material; “by” shows the doer of the action.
-> Paint is the material used, not the doer, so “painted by white paint” is wrong.
-> Correct sentence: “Each wall must be painted with white paint.”""",
{"Each wall": "no error — “each” takes a singular noun.",
 "must be": "no error — modal + be for the passive.",
 "painted by": "error — use “painted with” for the material.",
 "white paint.": "no error."},
r"With → instrument/material; by → doer.")
L(71, r"""-> We invest money in something.
-> “Invest in” is the fixed combination: invest in education, invest in shares.
-> So the blank needs “in”.""",
{"in": "correct — invest in.",
 "with": "wrong preposition after “invest”.",
 "for": "wrong — we invest for a purpose, but invest money in a field.",
 "by": "wrong — “by” would show the doer."},
r"Invest IN, spend ON, deal WITH.")
L(72, r"""-> “Aggravate” means to make a problem worse; it is not followed by “into”.
-> “Escalate into” means to grow into something bigger or more serious — it fits “an uncontrollable crisis”.
-> So the underlined part should be “the problem would escalate into”.""",
{"the problem would alleviate": "wrong — alleviate means to reduce, the opposite idea, and it needs an object.",
 "the problem will retaliate with": "wrong — retaliate means to hit back, and “will” breaks the reported tense.",
 "the problem would escalate into": "correct — escalate into = grow into.",
 "No improvement required": "wrong — “aggravate into” is not correct English."},
r"Escalate into a crisis; aggravate a problem (no “into”).")
L(73, r"""-> S1 “They faced the afternoon.” is followed by the short sentences B “It was too hot.” and D “Too bright.” — D completes B.
-> A then describes the veranda walls glaring in the sun.
-> C “The bougainvillea hung about it” — “it” refers to the veranda in A; then S2 moves to the garden outside. Order: B D A C.""",
{"BDAC": "correct — heat, brightness, walls, bougainvillea, then the garden.",
 "ABCD": "wrong — D “Too bright.” cannot follow C.",
 "DBAC": "wrong — “Too bright.” needs “It was too hot.” before it.",
 "CABD": "wrong — “it” in C has nothing to refer to at the start."},
r"Find the pair first: “It was too hot. Too bright.”")
L(74, r"""-> S1 says a pigeon appeared in one of the holes; C describes it flying in and waiting there.
-> A: David aims his gun at the bird; D: the shot is fired but the pigeon does not fall.
-> B “Neither did it fly.” must follow D, and S2 “Instead it stuck…” follows B. Order: C A D B.""",
{"CADB": "correct — arrives, aimed at, shot, did not fly.",
 "ADBC": "wrong — the bird must arrive before David aims at it.",
 "BDAC": "wrong — “Neither did it fly” needs “did not fall” before it.",
 "ACBD": "wrong — B must come right after D."},
r"“Neither did it fly” follows “did not fall”.")
L(75, r"""-> “Revert” already means to go back to an earlier state.
-> So “revert back” is redundant (a tautology).
-> Correct: “she keeps reverting to her bad habits”.""",
{"keeps reverting to her bad habits": "correct — removes the extra “back”.",
 "keeps reverting backward to her bad habits": "wrong — “backward” is also redundant.",
 "keeps reverting forth to her bad habits": "wrong — “revert forth” is not used.",
 "No improvement required": "wrong — “revert back” is redundant."},
r"Revert, return, reply — never add “back”.")
L(76, r"""-> The first sentence says dehydration-related deaths of children are due to contaminated food and water.
-> The second sentence lists the causes: contaminated groundwater, hazardous farm chemicals, poor hygiene in storage and handling, and unsanitary preparation.
-> The answer must combine these reasons.""",
{"Eating food and drinking water that are contaminated because of poor sanitation, unsafe storage, and harmful agricultural chemicals.": "correct — this sums up the passage.",
 "Because packaged drinking water is scarce across the country, most families rely on processed drinks.": "not mentioned in the passage.",
 "Relying too much on home-cooked meals made only with filtered water.": "not mentioned; filtered water would be safe.",
 "Young children are not drinking enough water because they spend too much time on digital devices.": "not mentioned in the passage."},
r"Match the option with the first two sentences of the passage.")
L(77, r"""-> The passage names contaminated groundwater and hazardous farm chemicals as reasons for food and water contamination.
-> Contaminated food and water spread infection and toxins, which cause diarrhoea — the main cause of dehydration in children.
-> Only one option links them to dehydration in children; it is the best inference.""",
{"They mainly cause aesthetic effects on water sources and are not known to cause long-term health effects.": "wrong — the passage links them to deaths, not looks.",
 "Infection and toxins released by these pathogens contaminate food and drinking water, thus increasing risks of dehydration due to diarrhea, especially in children.": "correct — links contamination to diarrhoea and dehydration in children.",
 "They reduce the nutrient levels in packaged foods kept near the site of contamination.": "not mentioned in the passage.",
 "They mainly affect industrial systems of cooling rather than domestic water used in the household.": "wrong — the passage is about food and drinking water."},
r"Choose the option that joins the cause in the passage to its effect (dehydration).")
L(78, r"""-> The passage mentions “the lack of proper hygiene in the storage and handling of food”.
-> It also mentions preparing and serving food in unsanitary conditions.
-> This applies to homes as well as eating places, so the answer is the failure of basic hygiene.""",
{"Lack of advanced refrigeration systems in upmarket restaurants.": "not mentioned in the passage.",
 "The use of foreign detergent compounds that can be left as residues on the other utensils.": "not mentioned in the passage.",
 "Failure to undertake basic hygiene practices when storing, processing, and handling the food means that the germs are able to multiply.": "correct — matches “lack of proper hygiene in storage and handling”.",
 "Excessive regulation of street vendors by the health department.": "wrong — the passage asks for more training and monitoring, not less."},
r"Look for the key phrase “storage and handling of food”.")
L(79, r"""-> The passage says it is necessary to raise awareness of adulteration and of how to complain to the authorities.
-> This means consumers have a part to play: they should spot adulteration and report it.
-> It does not say consumers alone are responsible or that the process is meant to discourage them.""",
{"The passage suggests that ensuring food safety relies primarily on what consumers do, potentially downplaying the role of regulatory authorities.": "wrong — the passage also needs government departments.",
 "The passage claims that, in low-income communities, people must address adulteration issues themselves, supposedly because laws do not forbid it there.": "not stated in the passage.",
 "The passage implies that the complicated complaint process is intended to discourage people from submitting concerns.": "wrong — the passage wants people to complain.",
 "The passage highlights that consumers play a role in identifying food adulteration and should know the proper steps to report it, as a way to help reduce such risks.": "correct — awareness helps people spot and report adulteration."},
r"Awareness + complaint procedure = consumers help report adulteration.")
L(80, r"""-> The last sentence says many people depend on street food for their daily needs.
-> Because of this, training street vendors is “vital”.
-> Trained vendors handle food safely and reduce contamination for the whole community.""",
{"Food street vendors are mandated to ensure compliance with national food safety standards without any monitoring from the state.": "wrong — the passage stresses government monitoring.",
 "Dehydration affects all age groups and is traced back to unsafe food preparation by street-side food vendors.": "wrong — the passage speaks of children and many causes.",
 "Vendor training makes the presence of government inspection teams for public health protection redundant.": "wrong — the passage wants both trained personnel and trained vendors.",
 "Many people eat street food, and hence, educating vendors on health, handling, and control of contamination is important in ensuring health within the community.": "correct — matches the last sentence of the passage."},
r"Read the last sentence: many depend on street food → train vendors.")
