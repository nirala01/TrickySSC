from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> “As plain as day” means extremely clear and obvious.
-> Daylight shows everything clearly, so something “plain as day” needs no explanation.
-> Example: It was as plain as day that he was lying.""",
{"Very different from the other": "wrong — that describes “as different as chalk and cheese”.",
 "In very good spirits": "wrong — that is “in high spirits”.",
 "Something is very clear, obvious, and easy to understand": "correct — the exact meaning of the idiom.",
 "Very happy in thought": "wrong — the idiom says nothing about happiness."},
r"Plain as day = clear as daylight.")
L(62, r"""-> To “dangle a carrot in front of someone” means to tempt them with the promise of a reward.
-> The image is of a donkey made to move forward by a carrot held just in front of it.
-> Example: The company dangled a carrot of a big bonus in front of its sales team.""",
{"To try to entice one with the promise of a reward": "correct — the exact meaning.",
 "To be very compatible and congenial together": "wrong — that is “to get on like a house on fire”.",
 "An incentivization method in which a reward and a punishment are simultaneously offered/threatened as a motivation to complete some task": "wrong — this is the “carrot and stick” approach, which also threatens punishment.",
 "A person with red orange hair": "wrong — that is the slang “carrot-top”, not this idiom."},
r"Carrot alone = reward; carrot and stick = reward plus punishment.")
L(63, r"""-> We need the one word that is spelt correctly.
-> “Heinous” (utterly wicked, e.g. a heinous crime) is the correct spelling.
-> The others drop or add letters.""",
{"Happless": "wrong — the correct spelling is “Hapless” (one p).",
 "Heinous": "correct — spelt correctly.",
 "Hystiria": "wrong — the correct spelling is “Hysteria”.",
 "Hubries": "wrong — the correct spelling is “Hubris”."},
r"HEI-nous: the h-e-i order is the trap.")
L(64, r"""-> “Reckless” means acting without thinking about danger or results.
-> Example: reckless driving.
-> The synonym must also mean hasty and careless.""",
{"Careful": "wrong — it is the opposite of reckless.",
 "Rash": "correct — it means acting hastily without thought, the same as reckless.",
 "Thoughtful": "wrong — it means considerate or careful, an antonym.",
 "Wise": "wrong — it means sensible, the opposite of reckless."},
r"Reckless = rash; careful, thoughtful and wise are its opposites.")
L(65, r"""-> We need the one word that is spelt wrongly.
-> “Professional” has double s and single f: pro-fess-ion-al.
-> The other three words are spelt correctly.""",
{"Essential": "correct spelling.",
 "Industrial": "correct spelling.",
 "Profesional": "misspelt — the correct form is “Professional” (double s).",
 "Sensational": "correct spelling."},
r"Profession comes from profess → keep the double s.")
L(66, r"""-> “Extraordinary” means very unusual or remarkable — beyond the ordinary.
-> Its antonym is a word meaning common or normal.
-> “extra-” means “beyond”, so removing it gives the opposite.""",
{"Remarkable": "wrong — it is a synonym.",
 "Exceptional": "wrong — it is a synonym.",
 "ordinary": "correct — it means common or normal, the opposite of extraordinary.",
 "Unusual": "wrong — it is a synonym."},
r"Extra-ordinary ↔ ordinary.")
L(67, r"""-> The event has ten different athletic events: the Greek prefix “deca-” means ten.
-> A decathlon is held over two days and includes running, jumping and throwing events.
-> The other words count a different number of events.""",
{"Decathlon": "correct — deca = 10 events.",
 "Pentathlon": "wrong — penta = 5 events.",
 "Tetratlon": "wrong — this points to “tetrathlon”, 4 events (and it is misspelt).",
 "Heptathlon": "wrong — hepta = 7 events (the women's combined event)."},
r"Tetra 4, penta 5, hepta 7, deca 10.")
L(68, r"""-> The active sentence is a question in the future perfect tense: Will we have shipped …?
-> Future perfect passive: will + have been + past participle.
-> As a question: Will + object + have been + shipped + by us …?""",
{"Will all the orders be shipped by us by the end of the day?": "wrong — simple future passive; “have been” is missing.",
 "Will all the orders had been shipped by us by the end of the day?": "wrong — “will” is never followed by “had”.",
 "Will all the orders have been shipped by us by the end of the day?": "correct — future perfect passive in question form.",
 "Will all the orders shipped by us by the end of the day?": "wrong — the helping verbs are missing."},
r"Future perfect passive = will have been + V3.")
L(69, r"""-> “will have completed” is the future perfect tense.
-> Its passive form is “will have been + past participle”.
-> The object “the tower” becomes the subject; “by next summer” stays.""",
{"The tower has been completed by the builders by next summer.": "wrong — present perfect, the tense has changed.",
 "The tower will be completed by the builders by next summer.": "wrong — simple future; “have been” is missing.",
 "The tower will have been completed by the builders by next summer.": "correct — future perfect passive.",
 "The tower was completed by the builders by next summer.": "wrong — past tense cannot go with “next summer”."},
r"will have + V3 (active) → will have been + V3 (passive).")
L(70, r"""-> “Pass” in this sense means spending time: we pass time doing something.
-> “forest passing with trees” leaves out the object “time”, so the phrase makes no sense.
-> Correct sentence: I want to spend some time in the forest, passing time with the trees and enjoying the natural beauty.""",
{"I want to spend": "no error.",
 "some time in the": "no error.",
 "forest passing with trees": "error — “passing” needs its object (“passing time with the trees”).",
 "and enjoying the natural beauty.": "no error — it parallels “passing”."},
r"Pass time, spend time — 'pass' needs 'time' after it.")
L(71, r"""-> The noun “genius” in the sense of a natural talent is followed by “for”.
-> We say: a genius for music, a genius for organisation.
-> So: Alexander had a genius for tactical warfare.""",
{"for": "correct — “a genius for something” = a special talent for it.",
 "in": "wrong — “genius in” is not the idiomatic pattern for a talent.",
 "of": "wrong — “a genius of” means a great person of a time or field, not a talent for something.",
 "to": "wrong — “genius to” is not used."},
r"Have a genius FOR, a flair FOR, a knack FOR.")
L(72, r"""-> The adjective “conducive” is always followed by “to”: conducive to growth.
-> After the preposition “to” we use the -ing form: conducive to bringing.
-> We bring stability TO something, so the full phrase is “conducive to bringing stability to the financial system”.""",
{"conducive of bringing stability in": "wrong — “conducive of” is incorrect.",
 "conducive for bringing stability into": "wrong — “conducive for” is incorrect.",
 "conducive to bringing stability to": "correct — right preposition and the -ing form.",
 "No improvement required": "wrong — “in bring” is ungrammatical."},
r"Conducive TO + -ing.")
L(73, r"""-> S1 tells us the writer went into hospital to have the appendix out.
-> A comes next: after two days there was food, but it would not stay down. D then adds a new problem: a fever.
-> B says no one could find the bacteria or what went wrong, and C (“No one ever did.”) closes that thought; S2 then describes the IV treatment.""",
{"CBDA": "wrong — “No one ever did” cannot come before what no one could do.",
 "ABCD": "wrong — the fever (D) must come before the search for its cause (B).",
 "DBAC": "wrong — the fever cannot come before the food two days after the operation.",
 "ADBC": "correct — food, fever, search for the cause, no answer."},
r"C answers B, so B–C must be together and in that order.")
L(74, r"""-> S1 asks when the heat had ever bothered her father before — so a memory of the father in the heat must follow.
-> C starts the memory (taking water to the farthest field); A describes him drinking it; B shows him strong and refreshed.
-> D (“The vision pleased and confused her …”) brings us back to the present, leading to S2 where she stares at the man beside her.""",
{"ABDC": "wrong — A's “the jug” needs C to bring in the water first.",
 "CABD": "correct — memory begins, he drinks, he grows strong, back to the present.",
 "ACBD": "wrong — A cannot come before C introduces the water.",
 "BCAD": "wrong — B's “And his chest would swell” must follow him drinking in A."},
r"Introduce the scene (C) before using 'the jug' (A).")
L(75, r"""-> “Since” already joins the two clauses, so adding “so” doubles the connector.
-> Use one linking word only: Since …, I had to take a bus home.
-> The tense “had to take” is correct for a past necessity.""",
{"so I had taken a bus home": "wrong — it keeps the extra “so” and the past perfect changes the meaning.",
 "I had to take a bus home": "correct — removes the extra “so”.",
 "so I had to get a bus home": "wrong — the extra “so” is still there.",
 "No improvement required": "wrong — “Since … so …” is a double conjunction."},
r"Since/because … (no 'so'); although … (no 'but').")
L(76, r"""-> The passage says India has grown fast but can grow even faster and spread the benefits widely.
-> Its key idea is inclusive growth: growth whose gains reach the whole population.
-> So the central idea is a call for faster growth that is also widely shared.""",
{"Demanding more rapid and widely shared economic growth": "correct — faster growth plus wider sharing, the passage's core.",
 "Focusing only on achieving substantial economic growth": "wrong — the passage says growth is not an end in itself.",
 "Improving India's global standing for economic growth": "wrong — global comparison is only mentioned in passing.",
 "Ensuring equitable distribution of wealth by the government": "wrong — redistribution alone is too narrow; growth is also demanded."},
r"Central idea = faster growth + benefits for all.")
L(77, r"""-> The passage defines inclusive growth as distributing the economic gains to the entire population, not to a specific group.
-> Growth must be an instrument for spreading prosperity to all.
-> So inclusive growth improves society as a whole.""",
{"Growth that serves only the wealthiest": "wrong — that is the opposite of inclusive growth.",
 "Growth that improves society as a whole": "correct — gains reach the entire population.",
 "Growth that sidelines the poorest in pursuit of economic progress": "wrong — the passage wants the poor to share the gains.",
 "Growth oriented on creating industries and increasing infrastructure": "wrong — the passage does not define it by industry or infrastructure."},
r"Inclusive = everyone included.")
L(78, r"""-> The passage says growth is necessary for eradicating poverty but not sufficient.
-> Policies must let the poor segment participate, with mechanisms to pass the gains to the vulnerable.
-> So growth must be combined with the participation of the poor.""",
{"Eradicating poverty only by achieving high economic growth": "wrong — growth alone is “not a sufficient condition”.",
 "Redistributing wealth to only the richest segments": "wrong — the gains must go to the vulnerable.",
 "Combining economic growth with the participation of the poor": "correct — exactly what the passage asks for.",
 "Addressing poverty exclusively through market-driven policies": "wrong — the passage wants redistribution mechanisms too."},
r"Necessary but not sufficient → growth + something more.")
L(79, r"""-> The passage first asks for faster growth (“develop even faster”).
-> It then asks that the gains reach the poorest and most vulnerable segment.
-> These two ideas — high growth and benefits for the weakest — together make inclusive growth.""",
{"Low inflation and high employment": "wrong — the passage does not discuss inflation.",
 "Privatization and foreign investment": "wrong — not mentioned in the passage.",
 "Market reforms and tax reduction": "wrong — not mentioned in the passage.",
 "High growth and benefits for the weakest segments": "correct — the two pillars of the passage."},
r"Grow fast + share with the poorest.")
L(80, r"""-> The passage proposes measuring progress by the progress of the poorest segment.
-> It names the bottom 20 per cent (the bottom quintile) as the example.
-> One would measure the per capita income of this bottom quintile and its growth rate.""",
{"By GDP growth rate": "wrong — overall GDP growth hides how the poor are doing.",
 "By total exports and imports in a fiscal year": "wrong — trade figures are not mentioned.",
 "Per capita income of the bottom 20%": "correct — the measure the passage proposes.",
 "By the growth in the urban employment rate": "wrong — urban jobs are not mentioned."},
r"Bottom quintile = bottom 20% of the population.")
