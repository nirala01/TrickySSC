from base import opt_bullets as ob, Q_EN
S = {}
def L(n, ctx, opt, trick):
    S[n] = dict(raw=ctx.strip() + "\n" + ob(n, opt), trick=trick)
def byL(n, d):
    return {Q_EN[n][k]: v for k, v in d.items()}

L(61, r"""-> “Think the world of someone” means to like, love or admire a person very much.
-> Example: The students think the world of their coach.""",
{"To like and admire them very much, or to have a very high opinion of them": "correct — this is the meaning of the idiom.",
 "To hate and reject someone and refuse to talk to them": "the opposite feeling; the idiom shows deep admiration.",
 "Interfere in the life of someone and try to trouble him": "describes meddling, which the idiom does not mean.",
 "Think of destroying the world of someone": "a literal and wrong reading of “world”."},
r"Think the world of = admire greatly.")
L(62, r"""-> “A dime a dozen” means very common and therefore of little value.
-> A dime is a small US coin, so getting twelve for a dime suggests something cheap and plentiful.""",
{"So scarce as to hold high value": "the opposite of the idiom.",
 "Produced in large quantity": "partly close, but it misses the key idea of having little value.",
 "So abundant or common as to hold little or no value": "correct — common and therefore cheap.",
 "Sold only in exchange of a dime": "a literal reading; the idiom is not about a real sale."},
r"A dime a dozen = cheap because common.")
L(63, r"""-> “Mend” means to repair something that is broken or damaged.
-> Example: He mended the torn shirt.""",
{"Break": "the opposite of mend.",
 "CUT": "means to divide with a sharp tool — not a synonym.",
 "Destroy": "to ruin completely — opposite in sense.",
 "FIX": "correct — fix means to repair, the same as mend."},
r"Mend ≈ fix ≈ repair.")
L(64, r"""-> The correct spelling is “unrelenting” — with a single L after “re” (un + relent + ing).
-> It means not becoming weaker or less severe.""",
{"Underprivileged": "spelt correctly — lacking the rights or advantages others have.",
 "Unrellenting": "misspelt — the correct form is “unrelenting”.",
 "Unmitigated": "spelt correctly — absolute, not lessened.",
 "Unravelling": "spelt correctly (British spelling) — coming undone."},
r"relent → unrelenting (one L).")
L(65, r"""-> The correct spelling is “lieutenant”, an army or police rank.
-> It is pronounced “lef-ten-ant” in British English, which causes the spelling “Leftinant”.""",
{"Leftinant": "misspelt — the correct form is “lieutenant”.",
 "Allegiance": "spelt correctly — loyalty to a person, group or country.",
 "Boulevard": "spelt correctly — a wide street.",
 "Vacuum": "spelt correctly — one C and two Us."},
r"Lieutenant = lieu + tenant (holding a place).")
L(66, r"""-> “Engaging” means charming, attractive or interesting enough to hold attention.
-> Its antonym describes something dull that fails to hold interest.""",
{"charming": "a synonym of engaging.",
 "Attractive": "a synonym of engaging.",
 "Appealing": "a synonym of engaging.",
 "Boring": "correct — dull and uninteresting, the opposite of engaging."},
r"Engaging ↔ boring.")
L(67, r"""-> “Mysophobia” (from Greek “mysos”, filth) is an extreme fear of dirt and germs.
-> People with it may wash their hands again and again.""",
{"Trypanophobia": "fear of needles or injections.",
 "Hemophobia": "fear of blood.",
 "Mysophobia": "correct — fear of dirt, germs and contamination.",
 "Dentophobia": "fear of dentists or dental treatment."},
r"Myso = dirt → mysophobia.")
L(68, r"""-> “On behalf of” means as the representative of someone, or in place of them.
-> Completed sentence: On behalf of my family, I thank you for your support and timely help to my father.""",
{"According to": "means as stated by — it does not fit thanking someone.",
 "Due to": "means because of — the sentence does not give a cause.",
 "on behalf of": "correct — the speaker thanks you as a representative of the family.",
 "within": "means inside a limit — makes no sense here."},
r"Thanking or speaking for a group → on behalf of.")
L(69, r"""-> The passive sentence “are organised by the council” is in the simple present tense.
-> In the active voice the doer (the council) becomes the subject and the verb stays in the simple present: organises.""",
byL(69, {'A': "correct — simple present active: “The council organises …”.",
 'B': "changes the tense to simple past (organised).",
 'C': "changes the tense to present continuous (is organising).",
 'D': "changes the tense to simple future (will organise)."}),
r"Passive am/is/are + V3 → active simple present (V1/V1+s).")
L(70, r"""-> “Let + object + not be + V3” is the passive form of a negative command.
-> Its active form is a negative imperative: “Don't / Do not + V1 + object”.""",
{"Don't delay the work any further.": "correct — the negative imperative in the active voice.",
 "The work not be delay any further.": "ungrammatical — it is neither active nor a correct passive.",
 "You cannot delay the work any further.": "a statement about ability, not a command.",
 "The work shouldn't be delayed any further.": "still passive, and it gives advice rather than a command."},
r"Let … not be + V3 → Don't + V1.")
L(71, r"""-> We translate a text from one language to (or into) another.
-> Completed sentence: Sir Charles Wilkins translated the Bhagavad Geeta from Sanskrit to English.""",
{"through": "means passing via something — wrong here.",
 "to": "correct — “from … to …” marks the language the text is changed into.",
 "in": "“in English” describes the state, not the change from Sanskrit.",
 "onto": "means moving on top of a surface — wrong here."},
r"translate from X to/into Y.")
L(72, r"""-> “Believe” is not used in the continuous form here; the passive “was believed” is needed because people believed it.
-> “To have reduced” (perfect infinitive) shows that the reduction happened before the time of believing.""",
{"is believed to reduce": "changes the past tense of the sentence to present.",
 "was believed to have reduced": "correct — past passive with a perfect infinitive.",
 "is being believed to reduce": "“believe” is a stative verb and is not used in the continuous.",
 "No improvement required": "wrong — “was believing” is incorrect."},
r"It was believed to have + V3 (earlier action).")
L(73, r"""-> S1 shows the couple at the station in Havre. C (“Then, in the third-class carriage …”) continues the journey in the train.
-> A shows children frightened by her in the carriage; D (“Everything went off well, however …”) sums up the journey; B (“But when the train slackened … near Yvetot”) leads to S2, where Antoine sees his parents waiting.""",
{"CADB": "correct — station → carriage → reactions → calm journey → arrival.",
 "CABD": "puts the arrival (B) before “everything went off well … up to their arrival” (D).",
 "CDAB": "D's “however” needs the reactions in A before it.",
 "CDBA": "A (children crying in the train) cannot come after the train reaches Yvetot."},
r"Follow the journey: station → carriage → arrival.")
L(74, r"""-> S1 “Mackintosh gave a gasp” is followed by his feeling — C “His heart seemed wrenched.”
-> He then holds the old man's hand (B), sits like that until a rattle breaks the silence (A), and D describes that rattle as terrible — leading to S2 “Walker was dead.”""",
{"ADBC": "A's “thus he sat” needs the action of B before it.",
 "BADC": "C (his emotion) belongs right after the gasp, not at the end.",
 "BACD": "D must describe the rattle in A, so it comes right after A.",
 "CBAD": "correct — gasp → feeling → holding the hand → rattle → its description → death."},
r"Link pronouns and reactions: “thus he sat” follows the hand-holding; “It was terrible” follows the rattle.")
L(75, r"""-> “Did nothing but” is followed by the base form of the verb (bare infinitive), not the past form.
-> Correct sentence: … as the parties did nothing but accuse each other.""",
{"did anything but accuse each other": "means they did not accuse each other — the opposite meaning.",
 "did not accuse each other": "changes the meaning and does not explain why mediation failed.",
 "did nothing but accuse each other": "correct — “did nothing but” + base verb.",
 "No improvement required": "wrong — “accused” after “did nothing but” is incorrect."},
r"do nothing but + V1.")
L(76, r"""-> The subject “The company” is singular and the action is a regular habit (“year after year”).
-> So the simple present with -s is needed: The company introduces new technology year after year.""",
{"introduce": "plural form — does not agree with the singular subject.",
 "introduced": "past tense clashes with the present-tense passage and “year after year”.",
 "will introducing": "ungrammatical — “will” takes the base form.",
 "introduces": "correct — singular, simple present for a habit."},
r"Singular subject + habit → V1 + s.")
L(77, r"""-> “Inspire” takes a direct object followed by “to + verb”: inspire someone to do something.
-> Here the “to” comes after the object: “Just Do It” inspires millions of athletes to push their limits.""",
{"inspires to": "adds an extra “to” before the object.",
 "inspires at": "“inspire at” is not idiomatic.",
 "inspires": "correct — inspires + object + to push.",
 "inspires over": "“inspire over” is not idiomatic."},
r"inspire somebody to do something.")
L(78, r"""-> The advertisements are linked with happiness by people — the subject receives the action, so the passive is needed.
-> “Be associated with” is the fixed pattern: Advertisements of the brand are associated with happiness, friendship and celebration.""",
{"associated": "lacks the helping verb and the preposition “with”.",
 "are associated with": "correct — plural passive + with.",
 "associating": "an -ing form cannot be the main verb on its own.",
 "will associated": "ungrammatical — “will” needs the base form."},
r"be associated with something.")
L(79, r"""-> The sentence is a first conditional: If + simple present (continue), … will + base verb.
-> Completed: If companies continue like this, they will lose customer trust in the future.""",
{"shall": "with “they” it sounds like a command or a promise and is not used for a simple prediction.",
 "will": "correct — first conditional result.",
 "should": "means duty or advice (ought to), which does not suit losing trust.",
 "would": "belongs to the second conditional (If they continued …)."},
r"If + present → will + V1.")
L(80, r"""-> “Not built overnight” comes from the proverb “Rome was not built in a day”.
-> It means something important takes a long time and steady effort to develop, as the next sentence says (“years of consistency”).""",
byL(80, {'A': "the opposite — the idiom stresses slowness.",
 'B': "the passage says brands are built through effort, not chance.",
 'C': "the idiom is about building, not destruction.",
 'D': "correct — it takes time and effort to develop."}),
r"Not built overnight = takes time and effort.")
