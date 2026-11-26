from base import opt_bullets as ob
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)

L(61, r"""-> A quandary is a state of doubt about what to do — a difficult choice.
-> To "throw one into a quandary" is to put someone into such a state, so that they are unsure or confused about the best course of action.
-> Example: The sudden change of plan threw us into a quandary.""",
{"To plead with someone, especially a figure of authority, to show one lenience and mercy": "wrong — that is “throw oneself on someone's mercy”.",
 "To cause one to become unsure, confused, or perplexed about the best course of action": "correct — the meaning of the idiom.",
 "To shock, surprise, astonish, or bewilder one": "wrong — that is closer to “throw one for a loop”; a quandary is about choosing, not shock.",
 "To put one in the position to be the recipient of blame, trouble, or criticism, often that which was intended for oneself.": "wrong — that is “throw someone under the bus”."},
r"Quandary = 'which way now?' — doubt about what to do.")
L(62, r"""-> The phrase comes from horse racing, where a horse may win by a "head" — the length of its head.
-> "By a short head" means by less than a head — an extremely small margin.
-> Example: She won the election by a short head.""",
{"By an extremely slim or narrow margin": "correct — the meaning of the idiom.",
 "To lack enough people to do something easily, efficiently, or effectively, usually because some of the usual participants are unavailable": "wrong — that is “be short-handed”.",
 "A hangover": "wrong — that is “a thick head” or “a sore head”.",
 "By a particular amount of something, especially points in a game or contest, over or below another amount": "wrong — that is the general use of “by” with a number (by 10 points), not this idiom."},
r"Short head = smaller than a head's length = tiny margin.")
L(63, r"""-> The question asks for the CORRECTLY spelt word.
-> “Egregious” (shockingly bad) is spelt correctly: e-g-r-e-g-i-o-u-s.
-> The other three are misspelt.""",
{"Exemplery": "wrong — the correct spelling is “Exemplary” (-ary).",
 "Effervesent": "wrong — the correct spelling is “Effervescent” (-scent).",
 "Egregious": "correct — spelt correctly.",
 "Emmanate": "wrong — the correct spelling is “Emanate” (one m)."},
r"Effervescent has the 'sc' of 'scent'; emanate has one m.")
L(64, r"""-> “Victory” means success in a contest or a battle.
-> “Triumph” means a great victory or success — it has the same meaning.
-> Defeat, loss and failure all mean the opposite.""",
{"Defeat": "wrong — an antonym of victory.",
 "LOSS": "wrong — an antonym of victory.",
 "Triumph": "correct — a synonym of victory.",
 "Failure": "wrong — an antonym of victory."},
r"Victory = triumph = win.")
L(65, r"""-> The question asks for the MISSPELT word.
-> The correct spelling is “Criticism” — critic + -ism, with a c, not an s.
-> The other three words are spelt correctly.""",
{"Critisism": "correct — this is misspelt; it should be “Criticism”.",
 "optimism": "wrong — spelt correctly.",
 "Pessimism": "wrong — spelt correctly (double s).",
 "Egotism": "wrong — spelt correctly."},
r"Criticism = CRITIC + ISM.")
L(66, r"""-> “Embarrassed” means feeling awkward, ashamed or self-conscious in front of others.
-> Its opposite is “confident” — sure of oneself and at ease.
-> The other three words have almost the same meaning as embarrassed.""",
{"Ashamed": "wrong — close in meaning to embarrassed.",
 "Humiliated": "wrong — a stronger form of embarrassed.",
 "Self-conscious": "wrong — close in meaning to embarrassed.",
 "confident": "correct — the opposite of embarrassed."},
r"Embarrassed (ill at ease) ↔ confident (at ease).")
L(67, r"""-> A person who behaves in an odd or unconventional way is called “eccentric”.
-> The word comes from Greek “ekkentros” — “out of the centre”.
-> Example: The eccentric professor wore a cap in every season.""",
{"Reticent": "wrong — means quiet, not revealing one's thoughts.",
 "Egotist": "wrong — a person who thinks and talks too much about himself.",
 "stickler": "wrong — a person who insists strictly on rules.",
 "Eccentric": "correct — a person with unconventional behaviour."},
r"Eccentric = ex + centre = away from the normal.")
L(68, r"""-> The sentence is in the simple future (will + invite), as a question.
-> In the passive, the object “the whole team” becomes the subject and the verb becomes will + be + past participle (invited).
-> The question form is: Will + subject + be + invited + by + agent?""",
{"Will the whole team invite to the party by the sponsors?": "wrong — “invite” is active; “be invited” is needed.",
 "Will the whole team invite the sponsors to the party?": "wrong — this reverses the meaning and is still active.",
 "Will the whole team been invited to the party by the sponsors?": "wrong — “been” cannot follow “will” directly.",
 "Will the whole team be invited to the party by the sponsors?": "correct — simple future passive question."},
r"Will + invite → will + be + invited.")
L(69, r"""-> The sentence is in the past continuous tense (were felicitating).
-> In the passive, past continuous becomes was/were + being + past participle.
-> So “war veterans” becomes the subject: War veterans were being felicitated at the event. (The agent “by them” is dropped.)""",
{"War veterans were felicitated at the event.": "wrong — this is simple past; “being” is missing.",
 "War veterans are being felicitated at the event.": "wrong — the tense has changed to present.",
 "War veterans were felicitating at the event.": "wrong — still active; the veterans are now doing the felicitating.",
 "War veterans were being felicitated at the event.": "correct — past continuous passive."},
r"Were + V-ing → were + being + V3.")
L(70, r"""-> The noun “passion” takes the preposition “for”: a passion for something.
-> So “a passion in writing” is wrong; it should be “a passion for writing”.
-> Correct sentence: Nirmala has a passion for writing one-act plays based on realities, and she is really adept at it.""",
{"Nirmala has a passion in writing": "correct — the error: “passion in” should be “passion for”.",
 "one-act plays based on realities,": "wrong — this part is correct.",
 "and she is really": "wrong — this part is correct.",
 "adept at it.": "wrong — “adept at” is the right preposition."},
r"Passion FOR, adept AT.")
L(71, r"""-> The sentence has a contrast: he was in great trouble, yet he came forward to help.
-> A contrast is shown by “in spite of” (= despite), followed by a noun or -ing form.
-> “Due to”, “owing to” and “according to” show cause or reference, not contrast.""",
{"Due to": "wrong — shows cause, which does not fit the contrast.",
 "According to": "wrong — means as stated by; it does not fit.",
 "In spite of": "correct — shows contrast: trouble, yet help.",
 "Owing to": "wrong — shows cause, like “due to”."},
r"Trouble + still helped = contrast → in spite of.")
L(72, r"""-> In a verb group like “would be overcome”, an adverb such as “soon” goes after the first helping verb.
-> So “would be soon overcome by” should be “would soon be overcome by”.
-> “Would” is also right because the main verb “assured” is in the past (reported speech).""",
{"will soon be overcome for": "wrong — “will” does not match the past tense, and “for” is the wrong preposition.",
 "would soon be overcome by": "correct — adverb after the first auxiliary.",
 "was soon overcome due to": "wrong — changes the meaning to a past event.",
 "No improvement required": "wrong — the adverb is in the wrong place."},
r"Adverb sits after the first helping verb: would SOON be.")
L(73, r"""-> S1 says the man is possessed by a notion; D explains it — he picks up a name from a newspaper and his mind plays with it.
-> C gives the first example (“One morning … a cousin to the man named Cox”) and B gives the next (“On another morning … Caruso”).
-> A gives his words about the little dog, which leads to S2 (his eyes looked appealingly up to me). So the order is DCBA.""",
{"CDBA": "wrong — the example C cannot come before D explains the notion.",
 "DCBA": "correct — explanation, first example, second example, his words.",
 "BCDA": "wrong — “On another morning” cannot come before “One morning”.",
 "ADCB": "wrong — A must come last, just before S2."},
r"“One morning” comes before “On another morning”.")
L(74, r"""-> S1 announces an affecting sight; D begins describing it — families reunited “nearby”.
-> C follows: he understood all these relationships without being told.
-> A (“What was most moving, however, were the old people”) turns to the old people, and B describes them gazing into one another's eyes; S2 then speaks of tears of joy. So the order is DCAB.""",
{"DCAB": "correct — the sight, his understanding, the old people, their gaze.",
 "CADB": "wrong — C (“all the relationships”) needs D's list before it.",
 "ADBC": "wrong — “however” in A needs an earlier description to contrast with.",
 "BCDA": "wrong — B's “them” has no clear reference at the start."},
r"Find the sentence with 'however' — it needs something before it.")
L(75, r"""-> The fixed phrase is “once-in-a-lifetime” — happening only once in a person's life.
-> The phrase uses “a lifetime”, not “the lifetime”.
-> It begins with the sound /w/ (“once”), so the article before it is “a”, not “an”.""",
{"the once-in-a-lifetime": "wrong — the noun “opportunity” is not specific here; “a” is needed.",
 "an once-in-a-lifetime": "wrong — “once” starts with a /w/ sound, so “a” is used.",
 "a once-in-a-lifetime": "correct — the right article and the fixed phrase.",
 "No improvement required": "wrong — “the lifetime” is not the idiom."},
r"A once-in-a-lifetime (like 'a one-day match').")
L(76, r"""-> The passage says the policy creates cultural ties and enhances economic cooperation, while developing relationships with Asia-Pacific countries.
-> So its main aim is to build cultural and economic links in the Asia-Pacific region.
-> The passage does not limit it to trade or tourism.""",
{"To develop the cultural and economic connections in the Asia-Pacific region": "correct — stated in the passage.",
 "To focus only on trade agreements with South-East Asian nations": "wrong — the policy also covers culture, science and security.",
 "To limit India's presence in the West and, at the same time, promote domestic trade": "wrong — not mentioned.",
 "To facilitate the travel of people and promote tourism in the North-East region": "wrong — too narrow; tourism is not mentioned."},
r"Look for the sentence that says what the policy 'paves the way for'.")
L(77, r"""-> The passage calls the North-East “not just a gateway to South-East Asia but also an extended corridor for growth, progress, and prosperity”.
-> It adds that the region, especially Manipur, enhances connectivity by land, air and sea.
-> So it is important as a gateway and a corridor for connectivity and growth.""",
{"It serves as a gateway and corridor for connectivity and growth": "correct — the passage's own description.",
 "It is the lone area with a way into the cutting-edge tech centers": "wrong — not mentioned.",
 "It is the center for the cultures of both Buddhism and Hinduism": "wrong — Buddhist and Hindu links are mentioned for the region as a whole, not as the reason for the North-East's importance.",
 "It is primarily a military base for strategic operations and nothing else": "wrong — not mentioned."},
r"Gateway + corridor = the North-East.")
L(78, r"""-> The passage names the major projects supporting the policy.
-> They are the Kaladan Multi-modal Transit Transport Project, the India-Myanmar-Thailand Trilateral Highway, the Rhi-Tiddim Road Projects and Border Haats.
-> The other options list domestic projects that the passage does not mention.""",
{"The Golden Quadrilateral Highway, the Delhi-Mumbai Industrial Corridor, and the Smart Cities Mission.": "wrong — domestic projects, not in the passage.",
 "The Bharatmala Project, the Sagarmala Project, and the Inland Waterways Development initiative.": "wrong — not mentioned in the passage.",
 "The Kaladan Multi-modal Transit project, the Trilateral Highway, the Rhi-Tiddim Road, and the Border Haats.": "correct — the projects named in the passage.",
 "The East-West Metro Corridor, the Bullet Train Project, and the Coastal Road Development program.": "wrong — not mentioned."},
r"Match the exact project names given in the passage.")
L(79, r"""-> On the cultural front, the passage says Buddhist and Hindu links could be strengthened to foster new connections among people.
-> So the policy strengthens cultural ties by promoting Buddhist and Hindu links.
-> Sports events, Western festivals and language exchange are not mentioned.""",
{"Organizing international sports events in the North-East": "wrong — not mentioned.",
 "Introducing Western cultural festivals in Asia-Pacific countries": "wrong — not mentioned.",
 "Focusing only on language exchange programs": "wrong — not mentioned.",
 "Promoting Buddhist and Hindu links across the region": "correct — stated in the passage."},
r"'On the cultural front' → Buddhist and Hindu links.")
L(80, r"""-> On strategic issues, the passage says India is increasing convergence with key partners on security interests.
-> It adds that this happens both bilaterally and multilaterally.
-> So India aligns with partners on security interests.""",
{"Aligning with partners on security interests": "correct — convergence = coming together on shared interests.",
 "Limiting defense ties to bilateral deals": "wrong — the passage says bilaterally AND multilaterally.",
 "Avoiding multilateral forums for neutrality": "wrong — the opposite of the passage.",
 "Cutting back on regional security engagement": "wrong — the passage says engagement is increasing."},
r"Convergence = moving together = aligning.")
