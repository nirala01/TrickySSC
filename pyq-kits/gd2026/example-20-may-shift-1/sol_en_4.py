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

L(61, r"""-> The idiom is said to come from ships' flags, whose height was set by pegs; lowering a flag “a peg” reduced the honour shown. So to take someone down a peg (or two) is to make a proud person feel less important.
-> The idiom is used when someone who thinks too highly of himself is shown that he is not as talented or important as he believes.
-> Example: "Losing to a junior player took the champion down a peg or two." """,
{"Peg away at": "wrong — it means to keep working hard and steadily at something.",
 "Take someone down a peg or two": "correct — to make someone realise they are less important or talented than they think.",
 "square peg": "wrong — “a square peg (in a round hole)” is a person who does not fit a job or situation.",
 "Peg back": "wrong — it means to stop an opponent from getting ahead, or to hold something at a level."},
r"Down a peg = pride brought down.")
L(62, r"""-> “Woe” means great sorrow or trouble, and “betide” is an old word meaning “happen to”.
-> So “woe betide somebody” is a warning that there will be trouble for a person, usually if he does something.
-> Example: "Woe betide anyone who arrives late for the parade." """,
{"Pleasant things will happen to someone": "wrong — this is the opposite; “woe” is sorrow, not joy.",
 "Unprecedented success to someone": "wrong — the idiom warns of trouble, not success.",
 "Unpleasant things will happen to someone": "correct — bad things or trouble will come to that person.",
 "Feeling jealous of someone": "wrong — the idiom has nothing to do with jealousy."},
r"Woe = sorrow, betide = befall → trouble will befall him.")
L(63, r"""-> The underlined word “trepidition” is wrongly spelt; the right word is “trepidation”, which means fear or nervousness about something that is going to happen.
-> It comes from the Latin “trepidare” (to tremble): tre-pi-da-tion, with “e” after tr and “a” before -tion.
-> The sentence means that she entered the interview room nervously.""",
{"tripidation": "wrong — the second letter should be “e” (tre-), not “i”.",
 "trepidetion": "wrong — it has “e” where “a” is needed (-dation).",
 "trepidation": "correct — the right spelling: t-r-e-p-i-d-a-t-i-o-n.",
 "No replacement required": "wrong — the word in the sentence (trepidition) is misspelt, so it must be replaced."},
r"Think of “intrepid” (fearless): in-TREPID → TREPID-ation.")
L(64, r"""-> To “grumble” is to complain about something in a quiet but bad-tempered way.
-> Its synonyms are complain, moan, grouse and mutter.
-> Example: "The passengers grumbled about the delay." """,
{"complain": "correct — to say that you are unhappy or not satisfied; same meaning as grumble.",
 "Whisper": "wrong — to speak very softly; it carries no sense of complaint.",
 "shout": "wrong — to speak very loudly; a grumble is low and muttered.",
 "Agree": "wrong — to have the same opinion; nearly the opposite idea."},
r"Grumble = complain in a low voice.")
L(65, r"""-> “Privilege” (a special right or advantage) has “i” after the v and ends in “-lege”: p-r-i-v-i-l-e-g-e.
-> There is no “a” in the word, so “Privilage” is the misspelt one.
-> The other three words are spelt correctly.""",
{"Occurrence": "correctly spelt — double c and double r.",
 "Apparent": "correctly spelt — double p, ending in -ent.",
 "Privilage": "misspelt — the correct spelling is “Privilege”.",
 "Parallel": "correctly spelt — double l in the middle, single l at the end."},
r"Privi-LEGE: it is a privilege to have two i's and two e's, no a.")
L(66, r"""-> “Expensive” means costing a lot of money.
-> Its antonym must mean not costing much — cheap, inexpensive, affordable or reasonable.
-> A “reasonable” price is one that is fair and not too high.""",
{"Reasonable": "correct — (of a price) fair and not too high; the opposite of expensive.",
 "Costly": "wrong — a synonym of expensive.",
 "Pricey": "wrong — an informal synonym of expensive.",
 "Valuable": "wrong — worth a lot of money; close in meaning, not opposite."},
r"Costly, pricey and valuable sit with expensive; reasonable stands apart.")
L(67, r"""-> A person who tells anecdotes (short amusing stories) skilfully is called a “raconteur”.
-> The word comes from the French “raconter”, meaning to tell or recount.
-> Example: "Her grandfather was a brilliant raconteur who kept everyone laughing." """,
{"Raconteur": "correct — a person who tells stories and anecdotes in a skilful and amusing way.",
 "Sybarite": "wrong — a person who loves luxury and pleasure.",
 "Martinet": "wrong — a very strict person who demands that rules be obeyed.",
 "Epicurean": "wrong — a person devoted to pleasure, especially fine food and drink."},
r"Raconteur “recounts” stories.")
L(68, r"""-> “Forfeiture” is the loss of property, money or a right as a punishment for a wrong act or for breaking a rule.
-> The verb is “forfeit”: "He forfeited his deposit by leaving early."
-> The other three words name quite different legal ideas.""",
{"Forfeiture": "correct — losing or giving up something as a penalty for wrongdoing.",
 "Embezzlement": "wrong — dishonestly taking money that one has been trusted with.",
 "Extradition": "wrong — handing over an accused person to another country or State for trial.",
 "Interdiction": "wrong — an official order forbidding something; also the stopping of smuggled goods."},
r"Forfeit = lose it as a fine.")
L(69, r"""-> The blank comes before the gerund “bringing”, so it needs a preposition.
-> The meaning required is “if you do not bring your identity proof, you cannot apply” — the preposition for “not having or not doing” is “without”.
-> Complete sentence: "Without bringing your identity proof, you cannot apply for the job." """,
{"Apart from": "wrong — it means “besides” or “except for”, which does not give the sense of a condition.",
 "Unless": "wrong — it is a conjunction and needs a clause (“unless you bring …”), not “bringing”.",
 "without": "correct — “without + -ing” means “if you do not …”.",
 "Except": "wrong — it means “leaving out”; “except bringing” does not make sense here."},
r"Unless + clause; without + -ing.")
L(70, r"""-> The active sentence is in the past perfect tense: “had rounded up”.
-> Passive of the past perfect = object + had been + past participle + by + subject.
-> The phrasal verb stays together: “had been rounded up by the police”; the phrase “before the press conference” does not change.""",
{"Eight suspects were": "wrong — “were rounded up” is simple past; the tense has changed.",
 "Eight suspects had rounded": "wrong — still active, and it reverses the meaning (the suspects round up the police).",
 "Eight suspects had been": "correct — had been + rounded up + by the police.",
 "Eight suspects had being": "wrong — “had being” is not a valid form; it must be “had been”."},
r"Had + V3 → had been + V3.")
L(71, r"""-> The passive question is in the simple future: “Will … be made by the volunteers?”
-> In the active voice the doer (the volunteers) becomes the subject: Will + subject + base verb + object.
-> So: "Will the volunteers make the necessary arrangements before the guests reach the venue?" """,
{"Do the": "wrong — “Do … make” is simple present, not future.",
 "Did the": "wrong — “Did … make” is simple past.",
 "Will the": "correct — it keeps the simple future and makes “the volunteers” the subject.",
 "Have the": "wrong — “Have … made” is present perfect."},
r"Will + be + V3 → Will + subject + V1.")
L(72, r"""-> The passive sentence is in the simple present: “are guarded”.
-> Active of the simple present = subject + first form of the verb (+ s/es for a singular subject) + object.
-> The doer “someone” is singular, so the verb is “guards”: "Someone guards the secret documents day and night." """,
{"Someone guards": "correct — simple present, matching “are guarded”.",
 "Someone has": "wrong — “has guarded” is present perfect (passive: have been guarded).",
 "Someone is": "wrong — “is guarding” is present continuous (passive: are being guarded).",
 "Someone was": "wrong — “was guarding” is past continuous (passive: were being guarded)."},
r"is/are + V3 → V1 (+ s/es).")
L(73, r"""-> “Crowded” takes the preposition “with”: a place is crowded with people.
-> So “crowded by millions of devotees” should be “crowded with millions of devotees”.
-> Correct sentence: "The Golden Temple was crowded with millions of devotees from all around the world on the day of Baisakhi." """,
{"The Golden Temple was": "no error — singular subject with “was”.",
 "crowded by millions of devotees": "error — “by” should be “with” (crowded with).",
 "from all around the world": "no error — a correct phrase.",
 "on the day of Baisakhi.": "no error — “on” is the right preposition for a day."},
r"Crowded with, filled with, packed with — never “by”.")
L(74, r"""-> To “dilate on/upon” a subject is to speak or write about it at length.
-> The verb in this sense always takes “on” or “upon”.
-> Complete sentence: "The student leaders dilated upon the political issues." """,
{"into": "wrong — “dilate into” is not an accepted expression.",
 "onto": "wrong — “onto” shows movement to a surface; it is not used with dilate.",
 "upon": "correct — “dilate upon” = speak at length about.",
 "over": "wrong — we say “talk over” or “go over”, but not “dilate over”."},
r"Dilate upon, dwell upon, expand upon — all mean “speak at length”.")
L(75, r"""-> The idiom is “to be on the same page”, meaning to have the same understanding or to be in agreement.
-> Its preposition is fixed as “on”; “in the same page” is wrong.
-> Improved sentence: "We must ensure that all the stakeholders are on the same page before beginning the negotiations." """,
{"on the same page": "correct — the standard idiom for being in agreement.",
 "on the same plate": "wrong — there is no such idiom.",
 "in the same boat": "wrong — a real idiom, but it means “in the same difficult situation”, which does not fit here.",
 "No improvement required": "wrong — “in the same page” needs to be corrected."},
r"Same page = same understanding (on); same boat = same trouble (in).")
L(76, r"""-> The passage says Einstein “imagined a very light slit that would recoil when a single photon passed through it”.
-> It adds: “If one could measure that recoil, one could, in principle, tell which path the photon took.”
-> The recoil is the push (momentum) the photon gives the slit, so the movable slit was meant to reveal the photon's path.""",
{"To eliminate": "wrong — he also wanted to look for the interference pattern, not remove it.",
 "To measure": "correct — measuring the recoil (the momentum passed on by the photon) would tell which path it took.",
 "To increase": "wrong — the idea involves a single photon; the number of photons is not discussed.",
 "To reduce": "wrong — the passage says nothing about reducing uncertainty in the photon's position."},
r"Movable slit → recoil → which path.")
L(77, r"""-> The passage says only that Bohr “argued that the plan would fail”; the reason has to be drawn from the rest of the passage and from physics.
-> The last part of the passage turns on “the uncertainty in the atom's momentum” — the recoil cannot be measured more finely than quantum physics allows.
-> This is Heisenberg's uncertainty principle: Bohr applied it to the slit itself, showing that measuring the recoil precisely would blur the slit's position and wash out the interference pattern.""",
{"The uncertainty principle": "correct — Bohr's reply rested on the uncertainty in the slit's momentum and position, the idea the passage itself points to.",
 "The principle of superposition": "wrong — the passage does not link Bohr's objection to superposition.",
 "The principle of complementarity": "wrong here — complementarity was the view Bohr was defending; the tool he used to show the plan would fail was the uncertainty principle.",
 "The exclusion principle": "wrong — Pauli's exclusion principle concerns electrons in atoms and has no role here."},
r"The passage's clue is the word “uncertainty” in the atom's momentum.")
L(78, r"""-> The passage says the researchers “cooled the atom close to its ground state, where its random motion was as small as quantum physics allowed”.
-> So cooling is done to bring the atom's random motion down to the smallest value that quantum physics permits.
-> The motion is reduced, not removed, because quantum physics does not allow it to become zero.""",
{"To eliminate": "wrong — the motion cannot be eliminated entirely; it is only made as small as quantum physics allows.",
 "To ensure": "wrong — nothing is said about the atom emitting photons consistently.",
 "To prevent": "wrong — the laser beam actually holds the atom in place, so the two must interact.",
 "To reduce": "correct — random motion is brought down to the quantum limit."},
r"“As small as quantum physics allowed” = reduced within quantum limits.")
L(79, r"""-> The last sentence gives the aim: to check whether the atom's recoil “could be used to say which way a photon went and how that information affected the interference pattern”.
-> So the experiment asks what happens to the interference when the photon's path becomes known.
-> This is the heart of the Einstein–Bohr argument described at the start of the passage.""",
{"Whether or not": "wrong — the experiment looks at wave behaviour (interference) too, not only at particle behaviour.",
 "Interference can": "wrong — the slit is replaced by an atom, but “interference without slits” is not what is being tested.",
 "Whether knowing": "correct — it tests how path (“which way”) information affects, and may remove, the interference pattern.",
 "Whether atoms": "wrong — the atom replaces the slit, not the photon."},
r"Which-way information versus interference pattern.")
L(80, r"""-> The passage says that in the ground state “the uncertainty in the atom's momentum is similar to the momentum of a single photon”.
-> The photon's path is to be read from the atom's recoil, which is a tiny change in the atom's momentum.
-> If the atom's own momentum is uncertain by about the same amount, the recoil cannot be measured with unlimited precision — this is why the uncertainty matters.""",
{"It determines": "wrong — the passage does not connect the atom's momentum uncertainty with the photon's wavelength.",
 "It keeps": "wrong — the focused laser beam holds the atom in place, not the uncertainty.",
 "It permits": "wrong — the passage makes no such claim.",
 "It limits": "correct — it sets a limit on how precisely the recoil can be measured."},
r"Uncertain momentum → fuzzy recoil reading.")
