"""Phase 5: sort an inbound message into a reply kind, with rules only (fast, free, predictable).

English and Hinglish patterns, matched on normalize.fingerprint() text (lowercase, punctuation
removed, so "don't" is "don t"). Order matters: an explicit stop always wins, auto-replies are
caught before anything reads them as engagement, and a clear "let's do it" beats a trailing
question ("Ok lets do it. Whats next?").
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .normalize import fingerprint


@dataclass
class ReplyKind:
    kind: str        # opt_out auto_reply hostile slot_pick commit off_topic thanks later decline question engaged empty
    reason: str
    detail: dict = field(default_factory=dict)


def _rx(*patterns: str) -> re.Pattern:
    return re.compile("|".join(f"(?:{p})" for p in patterns))


OPT_OUT = _rx(r"(?<!one )(?<!bus )\bstop\b(?! by)", r"\bunsubscribe\b", r"\bnot interested\b",
              r"\b(don t|do not) (message|text|contact|call|disturb)",
              r"\b(don t|do not) send (me )?(any ?more |these |such )?(messages|msgs|texts|stuff)\b",
              r"\bno more (messages|msgs|texts)\b", r"\bleave me alone\b", r"\bremove (me|my number)\b",
              r"\bmat bhej", r"\bband karo\b", r"\bbhejna band\b", r"\b(message|msg) mat\b", r"\bpareshan mat\b")
AUTO_REPLY = _rx(
    r"\bthank(s| you) for (contacting|reaching out|your message|messaging|writing|getting in touch)",
    r"\b(we|we ve|we have) received your (message|query|request)", r"\byour (message|query) (has been|is) received",
    r"\b(will|shall) (get back|respond|revert|reply)( to you)? (shortly|soon|as soon as)",
    r"\bour (team|executive|representative)s? will\b", r"\bautomated (message|reply|response|assistant)\b",
    r"\bauto ?reply\b", r"\bthis is an automated\b", r"\bvirtual assistant\b", r"\bi (am|m) (a|an) (bot|automated)",
    r"\bout of (the )?office\b", r"\bcurrently (unavailable|closed|away)\b", r"\b(business|working|office) hours\b",
    r"\bwe are closed\b", r"\bjaa?nkari ke liye\b.*\bshukriya\b", r"\bteam tak pahun?cha", r"\bautomated assistant hoon\b",
    r"\b(aapka|aapki) (sandesh|message) (mil gaya|prapt)", r"\bjald(i)? (hi )?(sampark|contact) kar")
HOSTILE = _rx(r"\buseless\b", r"\bwaste of (my )?time\b", r"\bspam(ming)?\b", r"\bbother(ing)?\b", r"\birritat",
              r"\bnonsense\b", r"\bbakwas\b", r"\bfaltu\b", r"\bshut up\b", r"\bidiot\b", r"\bstupid\b",
              r"\bscam\b", r"\bfraud\b", r"\bget lost\b", r"\bpagal\b")
STRONG_COMMIT = _rx(r"\blet ?s (do|go|start)\b", r"\bgo ahead\b", r"\bdo it\b", r"\bproceed\b", r"\bsign me up\b",
                    r"\bcount me in\b", r"\bi want to join\b", r"\bjud(r)?na (hai|chahta|chahti)\b",
                    r"\bkar (do|dijiye|dena)\b", r"\bkardo\b", r"\bconfirm(ed)?\b", r"\byes please\b",
                    r"\bshuru kar")
# Softer agreement words; inside a question ("Can you send me the price?") they are a request, not a yes.
SOFT_COMMIT = _rx(r"\bbhej (do|dijiye|dena)\b", r"\bsend (it|me|the|over)\b", r"\bbook (it|me)\b",
                  r"\bsounds good\b", r"\bchalo\b", r"\bstart (it|now)\b")
COMMIT = _rx(STRONG_COMMIT.pattern, SOFT_COMMIT.pattern)
# A negation right before the agreement words flips it ("do not go ahead", "don't send it"). Bare "no" is left
# out on purpose: "no problem, let's do it" and "no, go ahead" are both yeses.
NEGATED = re.compile(r"\b(not|don t|dont|never|mat|nahi|nahin)\s+(\w+\s+)?$")
# Business-voice auto-reply signatures: canned even when they end in a question ("How can we help you?").
CANNED_STRONG = _rx(r"\bthank(s| you) for (contacting|reaching out to|messaging|writing to) us\b",
                    r"\bhow (can|may) (we|i) (help|assist) you\b", r"\bour (team|executive|representative)s? will\b",
                    r"\bthis is an automated\b", r"\bautomated (message|reply|response|assistant)\b",
                    r"\bvirtual assistant\b", r"\bout of (the )?office\b", r"\bwe are (currently )?closed\b",
                    r"\bteam tak pahun?cha", r"\bautomated assistant hoon\b")
WEAK_YES = re.compile(r"^(yes|yeah|yep|yup|ok|okay|sure|haan|haa|ha|ji|bilkul|zaroor|done|theek|thik|fine|great|"
                      r"perfect|alright)\b")
OFF_TOPIC = _rx(r"\bgst\b", r"\bincome tax\b", r"\bitr\b", r"\btax (return|filing)", r"\bloan\b", r"\binsurance\b",
                r"\belectricity bill\b", r"\bbank account\b", r"\bpan card\b", r"\baadhaa?r\b", r"\bpassport\b",
                r"\bvisa\b", r"\blegal notice\b", r"\blawyer\b", r"\bcourt case\b", r"\bshare market\b", r"\bcrypto\b")
THANKS_ONLY = re.compile(r"^(ok |okay )?(thanks|thank you|thank u|thx|ty|shukriya|dhanyavad|dhanyawad)"
                         r"( so much| a lot| ji)?( ok)?$")
LATER = _rx(r"\bbusy\b", r"\blater\b", r"\bbaad (me|mein)\b", r"\babhi nahi\b", r"\bnot now\b", r"\bin a meeting\b",
            r"\bdriving\b", r"\bremind me\b", r"\btomorrow\b", r"\bkal\b")
TOMORROW = _rx(r"\btomorrow\b", r"\bkal\b")
DECLINE = re.compile(r"^(no|nope|nah|nahi|nahin|na|not needed|no thanks|no thank you|rehne do|mat karo)\b")
QUESTION_START = re.compile(r"^(what|how|when|which|why|where|who|can you|could you|will you|is it|are there|"
                            r"does it|kya|kaise|kitna|kitne|kitni|kab|kaun|kahan|kyun|kyon)\b")
_ORDINALS = {"1": 0, "one": 0, "first": 0, "pehla": 0, "pehli": 0, "2": 1, "two": 1, "second": 1,
             "doosra": 1, "dusra": 1, "doosri": 1, "3": 2, "three": 2, "third": 2}
_NOT_THIS_SLOT = re.compile(r"\b(not|nahi|nahin|don t)\s+(the\s+)?(" + "|".join(_ORDINALS) + r")\b")


def _slot_index(text: str, slot_labels: list[str]) -> int | None:
    """'1', 'the first one' or '5 nov' against offered slots like '5 Nov, 6pm'; 'not the first one' is no pick."""
    if _NOT_THIS_SLOT.search(text):
        return None
    words = text.split()
    if len(words) <= 4:
        for word in words:
            if _ORDINALS.get(word, 99) < len(slot_labels):
                return _ORDINALS[word]
    for i, label in enumerate(slot_labels):
        day_month = " ".join(fingerprint(label).split()[:2])
        if day_month and day_month in text:
            return i
    return None


def classify(message: str, *, repeats: int = 1, slot_labels: list[str] | None = None) -> ReplyKind:
    """What kind of reply this is. `repeats` = times this party has now sent this exact text."""
    raw = (message or "").strip()
    text = fingerprint(raw)
    if not text:
        return ReplyKind("empty", "blank message")
    if m := OPT_OUT.search(text):
        return ReplyKind("opt_out", f"asked to stop ({m.group(0)!r})")
    if m := CANNED_STRONG.search(text):
        return ReplyKind("auto_reply", f"canned text ({m.group(0)!r})")
    sounds_engaged = bool(WEAK_YES.match(text)) or "?" in raw
    if not sounds_engaged and (m := AUTO_REPLY.search(text)):
        return ReplyKind("auto_reply", f"canned text ({m.group(0)!r})")
    # short replies like "yes" repeat naturally, and a person may re-ask an unanswered question
    if repeats >= 2 and len(text.split()) >= 5 and "?" not in raw:
        return ReplyKind("auto_reply", f"same text {repeats} times")
    if slot_labels and (index := _slot_index(text, slot_labels)) is not None:
        return ReplyKind("slot_pick", f"picked slot {index + 1}", {"slot": index})
    if m := HOSTILE.search(text):
        return ReplyKind("hostile", f"frustrated ({m.group(0)!r})")
    if m := COMMIT.search(text):
        if NEGATED.search(text[:m.start()]):
            return ReplyKind("decline", f"said not to ({text[:m.end()].split()[-3:]!r})")
        asking = "?" in raw and QUESTION_START.match(text)
        if asking and not STRONG_COMMIT.search(text):
            return ReplyKind("question", "asked for something")
        if TOMORROW.search(text) or re.search(r"\b(later|next week|baad (me|mein))\b", text):
            return ReplyKind("commit", f"agreed, for later ({m.group(0)!r})",
                             {"later": "tomorrow" if TOMORROW.search(text) else "later"})
        return ReplyKind("commit", f"agreed ({m.group(0)!r})")
    if m := OFF_TOPIC.search(text):
        return ReplyKind("off_topic", f"outside Vera's scope ({m.group(0)!r})",
                         {"topic": "gst" if "gst" in m.group(0) else "other"})
    if THANKS_ONLY.match(text):
        return ReplyKind("thanks", "just saying thanks")
    if m := LATER.search(text):
        return ReplyKind("later", f"not now ({m.group(0)!r})",
                         {"wait_seconds": 86400 if TOMORROW.search(text) else 1800})
    if DECLINE.match(text) and "?" not in raw:
        return ReplyKind("decline", "said no")
    if "?" in raw or QUESTION_START.match(text):
        return ReplyKind("question", "asked a question")
    if WEAK_YES.match(text):
        return ReplyKind("commit", f"agreed ({text.split()[0]!r})", {"weak": True})
    return ReplyKind("engaged", "a normal reply")
