from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> The “blue code of silence” (also called the blue wall of silence) comes from the blue uniforms of police officers.
-> It is an unwritten rule among police officers not to report or speak about the wrongdoing of fellow officers.
-> Example: The inquiry failed because of the blue code of silence — no officer would testify against a colleague.""",
{"A silence that unnerves one": "wrong — that is just an uncomfortable silence.",
 "An absence of speech or sound that creates or communicates an especially effective or poignant message": "wrong — this describes a meaningful or “eloquent” silence.",
 "An unspoken policy or concealment by police regarding the wrongdoing or illicit activity of other officers.": "correct — the meaning of the idiom.",
 "A very tense, awkward, or uncomfortable atmosphere among a group of people": "wrong — that is “an awkward silence” or “you could cut the air with a knife”."},
r"Blue = police uniform; code of silence = no one tells.")
L(62, r"""-> When children colour a picture, they are told to stay within the lines and not go outside them.
-> So to “stay within the lines” is to follow the set rules and not do anything unusual or unexpected.
-> Example: In this office you must stay within the lines; new ideas are not welcomed.""",
{"Stay present during some event or timeframe": "wrong — that is “stick around”.",
 "Be in a place as near as possible": "wrong — has nothing to do with rules.",
 "A strict and inflexible view of or position on something": "wrong — that is “a hard line”.",
 "To think or act in accordance with set rules": "correct — the meaning of the idiom."},
r"Stay within the lines = follow the rules (opposite of 'think outside the box').")
L(63, r"""-> The question asks for the CORRECTLY spelt word.
-> “Cryptic” (mysterious, with a hidden meaning) is spelt correctly.
-> The correct spellings of the others are “cajole”, “capitulate” and “charlatan”.""",
{"Cryptic": "correct answer — spelt correctly.",
 "cajoule": "wrong — the right spelling is “cajole” (to persuade by flattery).",
 "Capitalate": "wrong — the right spelling is “capitulate” (to surrender).",
 "Charletan": "wrong — the right spelling is “charlatan” (a fraud)."},
r"Crypt → cryptic; char-LA-tan, ca-JOLE, capit-U-late.")
L(64, r"""-> “Withdraw” means to move back or pull out from a place or position.
-> Its closest synonym is “retreat”.
-> Advance and attack are opposite in meaning, and offer is unrelated.""",
{"Advance": "wrong — to move forward, the opposite of withdraw.",
 "Retreat": "correct — to move back, the same as withdraw.",
 "offer": "wrong — to present something; unrelated.",
 "Attack": "wrong — to move against an enemy, the opposite idea."},
r"Withdraw troops = retreat troops.")
L(65, r"""-> The question asks for the MISSPELT word.
-> The correct spelling is “ludicrous” (absurd, laughably foolish) — there is no “u” after “-cr”.
-> Cemetery, punctuate and indolence (laziness) are spelt correctly.""",
{"Cemetery": "wrong — spelt correctly (three e's, no a).",
 "Punctuate": "wrong — spelt correctly.",
 "Ludicurous": "correct answer — misspelt; the right spelling is “ludicrous”.",
 "Indolence": "wrong — spelt correctly."},
r"Ludi-CROUS (like 'crust'), not ludi-curous.")
L(66, r"""-> “Elevated” means raised to a higher position or level.
-> Its antonym is “lowered” — brought down to a lower position.
-> Raised, upright and lifted are close in meaning to elevated.""",
{"Raised": "wrong — a synonym of elevated.",
 "Lowered": "correct — the opposite of elevated.",
 "Upright": "wrong — standing straight up; not an opposite.",
 "LIFTED": "wrong — a synonym of elevated."},
r"Elevator goes up (elevated); down = lowered.")
L(67, r"""-> A person who does an activity for pleasure, not as a paid profession, is an “amateur”.
-> The word comes from the Latin “amator”, a lover — someone who does it for the love of it.
-> Example: He is an amateur photographer; he earns his living as a teacher.""",
{"Novice": "wrong — a beginner who is new to an activity.",
 "Apprentice": "wrong — a person learning a trade under a skilled worker.",
 "Amateur": "correct — one who takes part for pleasure, not professionally.",
 "Veteran": "wrong — a person with long experience."},
r"Amateur = for the love of it (Latin amator = lover).")
L(68, r"""-> The active sentence is in the future perfect tense: “will have renovated”.
-> In the passive, the future perfect becomes “will have been + past participle”.
-> The object “the bungalow” becomes the subject: “The bungalow will have been renovated by him by next month.”""",
{"The bungalow will have renovate by him by next month.": "wrong — “been” is missing and “renovate” is not the past participle.",
 "The bungalow will renovated by him by next month.": "wrong — “have been” is missing.",
 "The bungalow will have been renovated by him by next month.": "correct — future perfect passive.",
 "The bungalow has been renovated by him by next month.": "wrong — present perfect; the tense is changed."},
r"Future perfect passive = will have been + V3.")
L(69, r"""-> The active sentence is a past continuous question: “Were the musicians playing …?”
-> In the passive, the past continuous becomes “was/were + being + past participle”.
-> “Classical music” is singular, so the question becomes “Was classical music being played at the concert by the musicians?”""",
{"Was classical music played at the concert by the musicians?": "wrong — simple past passive; “being” is missing.",
 "Was classical music being played at the concert by the musicians?": "correct — past continuous passive.",
 "Has classical music been played at the concert by the musicians?": "wrong — present perfect; the tense is changed.",
 "Is classical music being played at the concert by the musicians?": "wrong — present continuous; the tense is changed."},
r"Past continuous passive = was/were + being + V3.")
L(70, r"""-> The noun “disadvantage” takes the preposition “of” (or “to”), not “with”.
-> Correct: “The only disadvantage of teaching is repeating the same curriculum again and again.”
-> So the error is in the part “disadvantage with teaching”.""",
{"The only": "wrong — no error in this part.",
 "disadvantage with teaching": "correct answer — “with” should be “of”.",
 "is repeating the same": "wrong — no error in this part.",
 "curriculum again and again.": "wrong — no error in this part."},
r"Advantage OF / disadvantage OF something.")
L(71, r"""-> The sentence says the police wanted evidence to prove him guilty.
-> Evidence that shows a person is guilty is evidence “against” that person.
-> Correct: “The police could not collect sufficient evidence against him to prove him guilty.”""",
{"for": "wrong — “evidence for him” would support him, not prove him guilty.",
 "about": "wrong — “evidence about him” does not show it is used to prove guilt.",
 "against": "correct — evidence against a person proves the charge.",
 "of": "wrong — we say “evidence of a crime”, not “evidence of him”."},
r"Evidence AGAINST the accused, evidence OF the crime.")
L(72, r"""-> The adjective “replete” (full of) always takes the preposition “with”: replete with something.
-> The past tense “required” matches “concluded” and “was”, so it must stay in the past.
-> Correct: “… the policy was replete with inconsistencies and therefore required immediate revision.”""",
{"replete with inconsistencies and therefore required": "correct — right preposition and right tense.",
 "replete of inconsistencies and therefore requiring": "wrong — “replete of” is wrong and “requiring” leaves the clause without a verb.",
 "replete by inconsistencies and therefore requires": "wrong — “replete by” is wrong and “requires” breaks the past tense.",
 "No improvement required": "wrong — “replete in” is incorrect, so improvement is needed."},
r"Replete WITH = full of.")
L(73, r"""-> S1 says “I remember once out at St. Cloud”, so the next sentence should name the event there: C (a big race with Kzar the favourite).
-> D follows (the narrator went to the paddock to see the horses), then A introduces Kzar (“This Kzar is a great big yellow horse”).
-> B (“I never saw such a horse”) reacts to A, and S2 (he was being led round the paddock) completes the picture. So the order is C-D-A-B.""",
{"DABC": "wrong — the race (C) must come before the visit to the paddock (D).",
 "ADBC": "wrong — “This Kzar” (A) cannot come before Kzar is named in C.",
 "CDAB": "correct — event → paddock → Kzar described → reaction.",
 "BADC": "wrong — “such a horse” (B) needs the horse to be described first."},
r"Look for the sentence that introduces a name (C: Kzar) before the one that says 'This Kzar'.")
L(74, r"""-> S1 says that in the dream the narrator's mother was still alive; D explains in brackets that she had actually died years earlier.
-> B (“Sometimes I would find myself in our old kitchen…”) and C (“But other times I would run into her on the street…”) give the two kinds of dream.
-> A (a hotel lobby or an airport) gives examples of the unexpected places in C, and S2 (“She would be looking quite well”) follows. So the order is D-B-C-A.""",
{"DBCA": "correct — fact → home dream → street dream → examples of places.",
 "CBDA": "wrong — “But other times” (C) must come after “Sometimes” (B).",
 "ADBC": "wrong — the places in A are examples of C, so A must follow C.",
 "BDAC": "wrong — A cannot come before C, whose examples it gives."},
r"'Sometimes …' is followed by 'But other times …'.")
L(75, r"""-> After “decided” we use the to-infinitive: decide to do something.
-> “decided to for hire” wrongly puts “for” between “to” and the verb.
-> Correct: “They have decided to hire a cruise ship for their anniversary celebration.”""",
{"decided for hiring a cruise ship": "wrong — “decide for hiring” is not correct English.",
 "decided to hire a cruise ship": "correct — decide + to + verb.",
 "decided for a cruise ship": "wrong — “decided for” changes the meaning and drops “hire”.",
 "No improvement required": "wrong — “to for hire” is incorrect."},
r"Decide TO do (decide + to-infinitive).")
L(76, r"""-> The first sentence of the passage gives the location of Pacific Salmon.
-> They are found on the western shores of North America, from California to southern Alaska.
-> The passage does not mention the Gulf of Mexico, the North Atlantic or the eastern shores.""",
{"Gulf of Mexico": "wrong — not mentioned in the passage.",
 "Northern Atlantic Ocean": "wrong — these are Pacific salmon.",
 "Eastern shores of North America": "wrong — the passage says western, not eastern.",
 "Western shores of North America": "correct — stated in the first sentence."},
r"Pacific Ocean is on the WEST coast of North America.")
L(77, r"""-> The passage calls their life cycle “astonishingly complex” and “migratory”.
-> They travel from their home (natal) freshwater rivers to the sea and later return to the river where they were born to spawn and die.
-> So their defining feature is migration from river to sea and back to spawn.""",
{"They migrate from rivers to the sea and return to spawn.": "correct — exactly what the passage describes.",
 "They spend their entire lives in freshwater environments.": "wrong — they go to the sea.",
 "They reproduce exclusively in marine environments.": "wrong — they spawn in rivers.",
 "They do not return to their place of origin.": "wrong — they return to the river they were born in."},
r"Salmon: river → sea → back to the same river.")
L(78, r"""-> A keystone species is one on which the whole ecosystem depends.
-> The passage says that after their death the salmon “contribute nutrients back into the streams”, playing a large role in the food web and ecological systems.
-> So, according to the passage, the nutrients they provide on death keep the ecosystem in balance.""",
{"Pacific Salmon support biodiversity through their role as a food source for many animals (e.g., bears and birds).": "wrong — bears and birds are not mentioned in the passage.",
 "Pacific Salmon influence food-web structures and processes only within marine ecosystems.": "wrong — the passage speaks of streams, not only the sea.",
 "Nutrient cycling from Pacific Salmon contributes significantly to the health of river systems and enhances habitat quality.": "wrong — habitat quality is mentioned only under conservation efforts, not as the reason they are a keystone species.",
 "The death of Pacific Salmon provides nutrients to the ecosystem, which plays a key role in maintaining ecological balance.": "correct — this is what the passage says."},
r"Keystone because their bodies feed the streams after death.")
L(79, r"""-> The second paragraph lists the threats to Pacific Salmon.
-> They are over-fishing, habitat degradation and climate change.
-> Pollution, predators and hatchery practices are not mentioned in the passage.""",
{"Pollution from industrial waste and urban runoff": "wrong — not mentioned in the passage.",
 "Over-fishing, habitat degradation, and climate change": "correct — the three threats named in the passage.",
 "Increased predation by marine mammals and birds": "wrong — not mentioned in the passage.",
 "Loss of genetic diversity due to hatchery practices": "wrong — not mentioned in the passage."},
r"Threats: fishing, habitat, climate (F-H-C).")
L(80, r"""-> The passage says Pacific Salmon have spiritual and dietary importance to many Native American and First Nation communities.
-> It also mentions their economic importance to commercial and recreational fisheries.
-> Among the options, only the statement about spiritual and dietary importance matches the passage.""",
{"Pacific Salmon, during their migration, create a safe pathway for fishermen": "wrong — not mentioned in the passage.",
 "Pacific Salmon does not have any cultural or economic significance": "wrong — the passage says the opposite.",
 "Pacific Salmon have spiritual and dietary importance for Native American and First Nation communities.": "correct — stated in the passage.",
 "Pacific salmon symbolizes laziness and procrastination, and the natives follow that symbolism to the core": "wrong — not in the passage, and the salmon's long migration suggests the opposite."},
r"Culture = spiritual + dietary; economy = fisheries.")
