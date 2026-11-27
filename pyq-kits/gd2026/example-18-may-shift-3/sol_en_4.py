from base import opt_bullets as ob, Q_EN
S = {}
def L(n, ctx, opt, trick):
    # keys may be the full option text or a unique prefix of it
    texts = [Q_EN[n][x] for x in "ABCD"]
    full = {}
    for k, v in opt.items():
        hits = [t for t in texts if t == k] or [t for t in texts if t.startswith(k)]
        assert len(hits) == 1, (n, k, hits)
        full[hits[0]] = v
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, full), trick=trick)

L(61, r"""-> The idiom needed must mean "wealthy or rich".
-> "Well heeled" means rich — originally, someone who could afford good shoes with sound heels.
-> Watch the spelling: "heeled" (from heel), not "healed" (from heal, to cure).""",
{"Well healed": "wrong — a misspelling; “healed” means cured, so the phrase has no idiomatic sense.",
 "Well groomed": "wrong — means neat and tidy in appearance.",
 "Well brought up": "wrong — means having good manners from a good upbringing.",
 "Well heeled": "correct — means wealthy or rich."},
r"Well heeled = rich (good heels on your shoes).")
L(62, r"""-> The idiom needed must mean "everything possible; all of something".
-> "The whole nine yards" means everything, the full extent of something.
-> Example: "They gave him the whole nine yards — a car, a house and a big salary." """,
{"The whole nine yards": "correct — means everything possible, the full lot.",
 "All wool and yard wide": "wrong — means genuine and of good quality.",
 "Thousand yard stare": "wrong — the blank, unfocused look of a person in shock.",
 "Hard yard": "wrong — hard yards are hard, unexciting work."},
r"Whole nine yards = the whole lot, everything.")
L(63, r"""-> Only one of the four words is spelt correctly.
-> "Apropos" (with reference to; appropriate) is spelt correctly — it comes from the French "à propos".
-> The other three have wrong letters.""",
{"Apropos": "correct — the right spelling, meaning concerning or fitting.",
 "Abrogiate": "wrong — the correct spelling is “Abrogate” (to cancel a law).",
 "Allacrity": "wrong — the correct spelling is “Alacrity” (eager readiness).",
 "Avarise": "wrong — the correct spelling is “Avarice” (greed)."},
r"Apropos ✓, Abrogate, Alacrity, Avarice.")
L(64, r"""-> "Fatal" means causing death.
-> Its synonym is "deadly"; for example, a fatal accident is a deadly accident.
-> Harmless and safe are its antonyms.""",
{"Deadly": "correct — means causing death, the same as fatal.",
 "Harmless": "wrong — an antonym; causing no harm.",
 "Safe": "wrong — an antonym; free from danger.",
 "Weak": "wrong — means lacking strength, not causing death."},
r"Fatal = deadly (fate → death).")
L(65, r"""-> One word in the list is misspelt.
-> The correct spelling is "Restaurant" — "-aur-" comes before "-ant".
-> The other three words are spelt correctly.""",
{"Disastrous": "spelt correctly — note there is no “e” after the “t”.",
 "Pungent": "spelt correctly — means having a sharp smell or taste.",
 "Benign": "spelt correctly — means gentle or harmless.",
 "Restuarant": "misspelt — the correct spelling is “Restaurant”."},
r"Rest-AU-rant: A before U is wrong, AU is right.")
L(66, r"""-> "Enveloped" means completely wrapped up, covered or surrounded.
-> Its antonym is "exposed" — uncovered and open to view.
-> Covered, wrapped and surrounded are synonyms of enveloped.""",
{"Exposed": "correct — uncovered, the opposite of enveloped.",
 "covered": "wrong — a synonym of enveloped.",
 "Wrapped": "wrong — a synonym of enveloped.",
 "Surrounded": "wrong — a synonym of enveloped."},
r"Envelope covers a letter → enveloped = covered; opposite = exposed.")
L(67, r"""-> A person who compiles (writes and edits) dictionaries is a lexicographer.
-> The word comes from "lexicon", meaning a dictionary or vocabulary.
-> Example: Samuel Johnson was a famous English lexicographer.""",
{"Linguist": "wrong — a person who studies languages or speaks many languages.",
 "Grammarian": "wrong — an expert in grammar.",
 "Lexicographer": "correct — a person who compiles dictionaries.",
 "Calligrapher": "wrong — a person skilled in beautiful handwriting."},
r"Lexicon = dictionary → lexicographer = dictionary-maker.")
L(68, r"""-> Using many words where a few would do is called circumlocution.
-> "Circum" means around, so it literally means "talking around" the point.
-> Example: saying "at this point in time" instead of "now".""",
{"Rhetoric": "wrong — the art of persuasive speaking or writing.",
 "Circumlocution": "correct — using too many words to say something simple.",
 "Hyperbole": "wrong — deliberate exaggeration.",
 "Eloquence": "wrong — fluent and persuasive speaking."},
r"Circum (around) + locution (speech) = talking around the point.")
L(69, r"""-> The sentence says she did not come to the shooting, so she broke her contract.
-> "In breach of" means breaking or not following a law, rule or agreement.
-> So the sentence reads: "… is in breach of her contract because she did not come to the shooting." """,
{"against": "wrong — “is against her contract” would mean she opposes it, not that she broke it.",
 "in accordance with": "wrong — means following the contract, the opposite of the sense.",
 "by force of": "wrong — means because of the power of something; it does not fit.",
 "in breach of": "correct — means breaking the terms of the contract."},
r"Break a contract = be in breach of it.")
L(70, r"""-> The sentence is an interrogative in the past continuous tense (were + tilling).
-> Passive of past continuous: was/were + being + past participle (V3).
-> Object "the fields" becomes the subject: "Were the fields being tilled by the farmers when the storm hit?" """,
{"Were the fields tilled": "wrong — past simple passive; “being” is missing.",
 "Had the fields been": "wrong — past perfect passive, a different tense.",
 "Are the fields being": "wrong — present continuous; the tense is changed.",
 "Were the fields being": "correct — past continuous passive with were + being + tilled."},
r"Past continuous passive: was/were + being + V3.")
L(71, r"""-> The sentence is passive in the future perfect tense (will have been + signed).
-> Active future perfect: will + have + past participle.
-> The agent "the partners" becomes the subject: "Will the partners have signed the legal documents before the deal is officially announced?" """,
{"Are the partners signing": "wrong — present continuous; the tense is changed.",
 "Did the partners sign": "wrong — past simple; the tense is changed.",
 "Have the partners signed": "wrong — present perfect; “will” is lost.",
 "Will the partners have signed": "correct — future perfect active, the same tense."},
r"Will have been + V3 (passive) → will have + V3 (active).")
L(72, r"""-> "You are requested to …" is the passive form of a polite request.
-> In the active voice a polite request is written as an imperative with "Please".
-> So the active form is: "Please send us a copy of your passport." """,
{"Let a copy of your passport be sent to us.": "wrong — this is itself a passive imperative.",
 "Send us a copy of your passport.": "wrong — an order; the polite request is lost.",
 "Please send us a copy of your passport.": "correct — the polite active imperative.",
 "We request your passport copy.": "wrong — changes the wording and the meaning (it does not ask them to send it)."},
r"You are requested to … → Please …")
L(73, r"""-> With adjectives that describe a person's behaviour (rude, kind, foolish, wise), we use "of", not "about".
-> Correct: "It was rude of the professor's daughter to have rejected the red rose …"
-> So the error is in the first part.""",
{"It was rude about the": "error — “rude about” should be “rude of”.",
 "professor's daughter to have": "no error — the perfect infinitive “to have rejected” is correct.",
 "rejected the red rose which was": "no error.",
 "being given by the young student.": "no error — past continuous passive is correct here."},
r"It is kind/rude/silly OF someone to do something.")
L(74, r"""-> "Take after" means to look or behave like an older family member.
-> Namrata resembles her mother, even in height, so "takes after" fits.
-> Correct: "Namrata takes after her mother, even with the same height." """,
{"by": "wrong — “take by” is not a phrasal verb with this sense.",
 "after": "correct — “take after” means to resemble a parent.",
 "for": "wrong — “take for” means to mistake someone for someone else.",
 "with": "wrong — “take with” does not mean to resemble."},
r"Take after = resemble a parent.")
L(75, r"""-> The fixed phrase is "in vain", meaning without success.
-> The verb that goes with "amends" is "make" — "make amends" means to do something to correct a wrong.
-> Correct: "The old man tried in vain to make amends with his estranged daughter …" """,
{"tried at vain to do amends": "wrong — “at vain” and “do amends” are both incorrect.",
 "tried on vain to fix amends": "wrong — “on vain” and “fix amends” are both incorrect.",
 "tried in vain to make amends": "correct — the right phrase “in vain” with “make amends”.",
 "No improvement required": "wrong — “for vain” is incorrect, so a change is needed."},
r"In vain = without success; make amends = put right a wrong.")
L(76, r"""-> The passage opens: inclusive education revolves around the concept of equity first and then equality.
-> Equity means giving each student what he or she needs; equality means giving everyone the same.
-> So the core principle is that equity comes before equality.""",
{"To guarantee equal chances": "wrong — it reverses the passage's order (equity comes first).",
 "Equity should come before equality": "correct — this is exactly the opening idea of the passage.",
 "It is important to prioritize": "wrong — the passage stresses individual needs, not uniform teaching.",
 "To uphold academic standards": "wrong — the passage is against segregation."},
r"Inclusive education = equity first, then equality.")
L(77, r"""-> The passage says inclusive education enables every student to feel protected, respected and confident.
-> This lets each student study and grow to the fullest.
-> So its main aim is respect and confidence for every learner.""",
{"Respect and confidence for every learner": "correct — the passage says every student should feel protected, respected and confident.",
 "Equal resources for all learners": "wrong — the passage stresses support according to individual needs (equity), not identical resources.",
 "Separate classes and resources for disabled learners": "wrong — students study together in general classrooms.",
 "Focus only on academics": "wrong — it also stresses belonging, social cohesion and well-being."},
r"Aim = every student protected, respected, confident.")
L(78, r"""-> The passage says communities and schools will share these ideals.
-> Inclusive education is implemented in school communities that celebrate diversity and support each member's well-being and academic excellence.
-> So schools and communities must share ideals that celebrate diversity and promote well-being.""",
{"They should place strong emphasis on competition": "wrong — the passage stresses positive interaction and diversity, not competition.",
 "They should only address": "wrong — inclusive education is for all students, with or without disabilities.",
 "They must share ideals": "correct — matches the last two sentences of the passage.",
 "They need to maintain strict uniformity": "wrong — the passage supports services suited to individual needs."},
r"Schools and communities share the ideals; they celebrate diversity and well-being.")
L(79, r"""-> The passage calls inclusive education "a combination of pedagogical approaches and philosophy".
-> It is founded on values that encourage positive interactions, belonging, active learning and a full school experience.
-> So its philosophy is to combine teaching strategies with inclusive values for the student's all-round development.""",
{"Providing students with equal opportunities without recognizing": "wrong — the passage stresses individual needs.",
 "Encouraging segregation": "wrong — students study together; segregation is the opposite.",
 "Integrating diverse teaching strategies": "correct — matches “a combination of pedagogical approaches and philosophy”.",
 "Limiting social interactions": "wrong — the passage encourages positive interactions with peers."},
r"Philosophy = teaching approaches + inclusive values → holistic growth.")
L(80, r"""-> The passage lists the values of inclusive education: social cohesion, belonging, active learning and a full school experience.
-> Students with or without disabilities study together in the same classrooms.
-> Segregation (separating students) goes against inclusive education, so it is NOT one of its values.""",
{"Social cohesion": "a value — named in the passage.",
 "Active learning": "a value — named in the passage.",
 "Sense of belonging": "a value — the passage names belonging.",
 "Segregation by ability": "NOT a value — inclusive education keeps all students together."},
r"Inclusion = together; segregation = the opposite.")
