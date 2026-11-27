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

L(61, r"""-> "Talk a blue streak" means to talk very fast, a lot and without stopping.
-> A "blue streak" is a flash of lightning, so the idiom pictures words coming out as fast as lightning.
-> Example: "Once she gets excited, she talks a blue streak." """,
{"To speak with great rapidity": "correct — speaking very fast and intensely is the meaning.",
 "To use profane language": "wrong — that is closer to “swear a blue streak” or “curse like a sailor”.",
 "Enjoying a series": "wrong — that describes being “on a lucky streak”.",
 "To have a series": "wrong — that is also the sense of a winning or lucky streak, not talking."},
r"Blue streak = lightning → talk as fast as lightning.")
L(62, r"""-> "Dreadful" means extremely bad, causing fear or great unpleasantness.
-> Its synonym is "terrible"; for example, a dreadful accident is a terrible accident.
-> Wonderful, pleasant and happy are the opposite in sense.""",
{"Wonderful": "wrong — an antonym; extremely good.",
 "Pleasant": "wrong — an antonym; giving pleasure.",
 "Terrible": "correct — means very bad or causing fear, the same as dreadful.",
 "Happy": "wrong — describes a feeling of joy, the opposite in tone."},
r"Dreadful = full of dread = terrible.")
L(63, r"""-> Three of the four words are spelt correctly; one is misspelt.
-> The correct spelling is "subterranean" (sub = under + terra = earth), with a double "r".
-> "subteranean" drops one "r", so it is the misspelt word.""",
{"succession": "spelt correctly — a series of things coming one after another.",
 "Superfluous": "spelt correctly — more than is needed.",
 "Sycophantic": "spelt correctly — flattering someone powerful to gain favour.",
 "subteranean": "misspelt — the correct spelling is “subterranean” (double r)."},
r"Sub + terra (earth) → subTERRanean, double r.")
L(64, r"""-> To "deposit" means to put money or things somewhere for safe keeping, such as money into a bank.
-> Its antonym is "withdraw", which means to take money or things out.
-> Store and save are close in meaning to deposit, not opposite.""",
{"Drop": "wrong — means to let fall; not the opposite of deposit.",
 "store": "wrong — a near-synonym; to keep for later use.",
 "Withdraw": "correct — to take out, the opposite of putting in.",
 "Save": "wrong — a near-synonym; to keep money aside."},
r"Deposit (put in) ↔ withdraw (take out).")
L(65, r"""-> "Disturbance" means an interruption of peace or a state of disorder.
-> Its antonym is "tranquility" (also spelt tranquillity), which means calm and peace.
-> Disorder, chaos and interruption all mean nearly the same as disturbance.""",
{"Tranquility": "correct — calmness and peace, the opposite of disturbance.",
 "Disorder": "wrong — a synonym; lack of order.",
 "chaos": "wrong — a synonym; complete confusion.",
 "Interruption": "wrong — a synonym; a break in continuity."},
r"Disturbance ↔ tranquility (calm).")
L(66, r"""-> The phrase describes a sudden, intuitive flash of understanding about something.
-> The word for this is "epiphany", from the Greek for "manifestation".
-> Example: "He had an epiphany and suddenly understood the whole problem." """,
{"Umbrage": "wrong — means offence or annoyance (to take umbrage).",
 "ignominy": "wrong — means public shame or disgrace.",
 "Antipathy": "wrong — means a strong dislike.",
 "Epiphany": "correct — a sudden insight or realisation."},
r"Sudden insight = epiphany.")
L(67, r"""-> The sentence gives an instruction for a possible situation: if there is a fire, call the fire brigade.
-> "In case of" means "if something happens" and is used for emergencies and possibilities.
-> So the sentence reads: "In case of fire, you must call the fire brigade at once." """,
{"By dint of": "wrong — means “by means of” (by dint of hard work).",
 "According to": "wrong — means “as stated by” or “in line with”.",
 "In case of": "correct — means “if there is”, fitting an emergency instruction.",
 "On the occasion of": "wrong — used for celebrations or events, not emergencies."},
r"Emergency instruction → “In case of fire …”")
L(68, r"""-> The active sentence is in the present continuous tense: "is preparing".
-> In the passive voice, present continuous becomes "is/are + being + past participle": "is being prepared".
-> The object "a gourmet meal" becomes the subject, and "the chef" follows "by".""",
{"A gourmet meal was being": "wrong — past continuous (“was being”), the tense has changed.",
 "A gourmet meal is being": "correct — present continuous passive with the right agent.",
 "A gourmet meal has been": "wrong — present perfect passive (“has been”).",
 "A gourmet meal is prepared": "wrong — simple present passive; “being” is missing."},
r"is + V-ing → is being + V3.")
L(69, r"""-> The active sentence is a present continuous question: "Are the publishers organising …?"
-> Its passive form is "Is + object + being + past participle + by + agent?"
-> Since the object "a book signing event" is singular, "Are" becomes "Is", and "by the publishers for the new author" keeps the original roles.""",
{"Was a book signing": "wrong — “Was” changes the tense to the past.",
 "Is a book signing event being organised by the new author": "wrong — the roles are swapped; the publishers are the doers.",
 "Is a book signing event being organised by the publishers": "correct — right tense, right helping verb and right roles.",
 "Is a book signing event been": "wrong — “been” cannot follow “Is”; it must be “being”."},
r"Are … organising? → Is … being organised by …?")
L(70, r"""-> "Let this mistake not be repeated" is a passive imperative (an order or advice).
-> Its active form is a direct command: "Don't repeat this mistake." (or "Do not repeat this mistake.")
-> The active form of an imperative is not changed into a statement about the future.""",
{"Don't repeat this mistake.": "correct — the active imperative form.",
 "No one will repeat": "wrong — a future statement, not a command.",
 "You won't repeat": "wrong — a future statement, not a command.",
 "This mistake let not": "wrong — still passive and the word order is wrong."},
r"Let + object + not be + V3 → Don't + V1 + object.")
L(71, r"""-> "Anxious about" means worried about something, while "anxious for" means eagerly wanting something.
-> The sentence speaks of a very happy and enjoyable weekend, which people wish for, not worry about.
-> So the correct preposition is "for": "They are anxious for a very happy and enjoyable weekend." """,
{"about": "wrong — “anxious about” shows worry, which does not suit a happy weekend.",
 "to": "wrong — “anxious to” is followed by a verb (anxious to leave), not a noun phrase.",
 "for": "correct — “anxious for” means eager to have.",
 "at": "wrong — “anxious at” is not idiomatic."},
r"Anxious about = worried; anxious for = eager to have.")
L(72, r"""-> The adjective "consistent" takes the preposition "with": consistent with the facts.
-> "Consistent to" is an error of preposition.
-> The verb form "presented" must stay, because the facts were presented earlier.""",
{"consistent with the facts presented earlier": "correct — right preposition and right verb form.",
 "consistent on the facts": "wrong — “consistent on” is not correct usage.",
 "consistent of the facts present earlier": "wrong — wrong preposition and “present” for “presented”.",
 "No improvement required": "wrong — “consistent to” is an error, so improvement is needed."},
r"Consistent WITH, compatible WITH.")
L(73, r"""-> S1 says she could not find in what direction his cleverness lay, so the next sentences list what he was not: B (not a wit, not a croquet champion …).
-> D continues with "Neither did his exterior suggest …", which follows B's "He was neither …".
-> A concludes that he had become "mere Mr. Appin", and C ("And now he was claiming …") leads into S2 about the miraculous discovery. So the order is B D A C.""",
{"BDAC": "correct — B → D (neither … neither) → A (conclusion) → C (the claim).",
 "DBAC": "wrong — D begins with “Neither did”, which needs B before it.",
 "ABDC": "wrong — A is a conclusion and cannot come before the list of what he was not.",
 "BADC": "wrong — A breaks the “neither … neither” link between B and D."},
r"Neither … (B) → Neither did … (D) → so he was mere Mr. Appin (A) → And now (C).")
L(74, r"""-> S1 says Bateman Hunter slept badly; B explains he had been planning the story on the boat and train.
-> A ("But in a few hours now he would be in Chicago, and doubts assailed him") turns to his doubts, and D says his conscience was not at ease.
-> C explains why (he was uncertain he had done all that was possible), which leads into S2 about self-sacrifice. So the order is B A D C.""",
{"CABD": "wrong — C explains a doubt that has not been mentioned yet.",
 "ADBC": "wrong — A's “But” needs B's planning before it.",
 "BADC": "correct — planning (B) → doubts (A) → uneasy conscience (D) → reason (C).",
 "BCAD": "wrong — C's uncertainty must come after the doubts in A and D."},
r"Story planned (B) → But doubts (A) → conscience (D) → why (C).")
L(75, r"""-> "Fully tired" is not natural English; "fully" does not go with "tired" to show a high degree.
-> The single word "exhausted" means extremely tired, which suits a long, steep hike with no energy left.
-> "Too much exhausted" and "very much tired" are also wrong forms.""",
{"exhausted after the long hike up the steep hill": "correct — the natural, correct expression.",
 "too much exhausted": "wrong — “exhausted” is not used with “too much”, and the meaning changes.",
 "very much tired": "wrong — “very much tired” is not standard; we say “very tired”.",
 "No improvement required": "wrong — “fully tired” is incorrect, so improvement is needed."},
r"Extremely tired = exhausted (not “fully tired”).")
L(76, r"""-> The passage defines disaster risk reduction as the "systematic creation and deployment of policies, strategies, and practices to limit vulnerabilities, hazards" and their effects.
-> "Systematic" means planned, and "limit vulnerabilities, hazards" means lower risks and dangers.
-> So disaster risk reduction is a planned way to lower risks and dangers.""",
{"A planned way to lower risks and dangers": "correct — matches “systematic … to limit vulnerabilities, hazards”.",
 "A short-term action taken after disasters happen": "wrong — it is a preventive, constant process, not a short-term reaction.",
 "A plan that only rebuilds": "wrong — the definition is about limiting risk, not only rebuilding.",
 "A way to get rid of all natural disasters forever": "wrong — it limits consequences; it cannot remove all disasters."},
r"Systematic + limit hazards = planned risk lowering.")
L(77, r"""-> The passage says: "Lack of coordinated disaster reduction measures and the absence of a 'culture of prevention' are the key causes of increased catastrophe-related casualties."
-> So the major reason for high casualties is the lack of coordinated efforts and of a culture of prevention.
-> The passage does not blame investment, traditional knowledge or international aid.""",
{"Excessive investment": "wrong — the passage never mentions too much investment.",
 "Lack of coordinated efforts and a culture of prevention": "correct — stated directly in the passage.",
 "Overdependence on traditional knowledge alone": "wrong — the passage wants traditional wisdom used, along with research.",
 "Complete reliance on international aid programs": "wrong — international aid is not mentioned."},
r"Key causes = no coordination + no culture of prevention.")
L(78, r"""-> The passage first lists assessing the probability and severity of hazards and the community's vulnerabilities.
-> It then says: "Building institutional capacity and community preparation is the next phase."
-> So the next step is building institutional capacity and community preparedness.""",
{"Reducing education and training": "wrong — the passage says education and training have a crucial effect.",
 "Limiting disaster planning to government agencies only": "wrong — the passage stresses community preparation too.",
 "Building institutional capacity and community preparedness": "correct — the passage calls this the next phase.",
 "Avoiding the use of traditional knowledge": "wrong — the passage says traditional wisdom must be used."},
r"After assessment → institutional capacity + community preparedness.")
L(79, r"""-> The passage calls the development of a 'safety culture' crucial to all these efforts.
-> It adds that inputs such as education, training and capacity building have a crucial effect, and that readiness is a constant process.
-> So a safety culture is essential because it ensures readiness through education and training.""",
{"It reduces the importance": "wrong — community participation is important in the passage.",
 "It focuses only on technological solutions": "wrong — technology is not mentioned as the only solution.",
 "It eliminates the need for any preventive measures": "wrong — the passage supports preventive measures.",
 "It ensures readiness through education and training": "correct — matches the passage's inputs of education and training."},
r"Safety culture = constant readiness via education and training.")
L(80, r"""-> The last lines of the passage say knowledge is crucial to reduce disasters.
-> They add: "Traditional wisdom accessible to the community must be used alongside knowledge gained through research and past experience."
-> So the best use of knowledge is to combine community wisdom with research and experience.""",
{"Ignore past experiences": "wrong — the passage values past experience.",
 "Integrate traditional community wisdom with research and experience": "correct — matches “used alongside” in the passage.",
 "Rely completely on technology": "wrong — the passage does not rely on technology alone.",
 "The knowledge sharing should be among experts": "wrong — the passage includes the community, not only experts and agencies."},
r"Traditional wisdom + research + experience together.")
