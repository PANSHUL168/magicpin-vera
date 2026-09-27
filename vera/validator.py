"""Phase 4: the validator. Every rule a message must pass before it is sent, plus the fix text for a retry.

problems() is the hard gate for AI-written first messages and replies. Each problem it returns
is phrased so that fixes() can turn it into one instruction for the model's second attempt
(writer.generate_checked retries once). The rules come from the brief (§5, §8, §11):
facts only, no links or taboo words, one ask as the last sentence, the recipient's name,
a concrete number, no preamble or self-introduction, customer messages speak as the shop,
and no copying of the case studies. Category vocabulary may be used as words but never
pitched as a service the business doesn't list (T25: a salon with no keratin offer).
"""

from __future__ import annotations

import re
from collections import Counter
from functools import lru_cache

from .config import ROOT
from .factsheet import FactSheet
from .normalize import fingerprint, number_tokens

MAX_BODY_CHARS = 600
PROPOSAL_KINDS = frozenset({"active_planning_intent"})  # first messages that carry a draft plan with proposed numbers
CASE_STUDY_LIMIT = 0.5  # share of a message's word triples also found in one case study

_URL_RE = re.compile(r"https?://|www\.", re.I)
_CODE_RE = re.compile(r"\b[a-z0-9]+(?:_[a-z0-9]+)+\b")
_SENTENCE_RE = re.compile(r"(?<=[.?!])\s+")
_EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
ASK_WORDS = ("reply", "confirm", "bataiye", "bataye", "batayiye", "tell us", "tell me", "let us know", "kijiye")
PREAMBLE = re.compile(
    r"\b(hope (you|u) (are|re|r) (doing )?(well|good|fine|great)|hope you (are|re) having|hope this (message )?finds you"
    r"|trust (you are|you re) (doing )?well|i am vera|i m vera|this is vera|vera here|my name is vera|main vera"
    r"|greetings from)\b")
# Category words that are metrics or trade terms, never a service someone could be missing.
GENERIC_VOCAB = frozenset(fingerprint(w) for w in (
    "footfall", "membership churn", "PR (personal record)", "split", "cut", "bulk", "functional",
    "covers", "AOV", "RPC", "table turnover", "reservations", "GRO",
    "OTC", "schedule H", "schedule X", "generic", "branded", "molecule", "MRP", "expiry", "batch", "PCR retail",
    "pharmacist counsel"))


def _triples(text: str) -> set[tuple[str, ...]]:
    words = fingerprint(text).split()
    return {tuple(words[i:i + 3]) for i in range(len(words) - 2)}


@lru_cache(maxsize=1)
def _case_studies() -> tuple[tuple[str, frozenset], ...]:
    path = ROOT / "examples" / "case-studies.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    blocks = re.findall(r"```\n(.*?)```", text, re.S)
    return tuple((f"case study {i}", frozenset(_triples(b))) for i, b in enumerate(blocks, start=1))


def case_study_overlap(body: str) -> tuple[float, str]:
    """Highest share of this message's word triples that also appear in a single case study."""
    mine = _triples(body)
    best = (0.0, "")
    for name, theirs in _case_studies():
        if mine:
            best = max(best, (len(mine & theirs) / len(mine), name))
    return best


def repeated_phrases(body: str, size: int = 4) -> list[str]:
    """Word runs said twice in one message ("...Google post bana doongi. ...Google post bana doongi.")."""
    words = fingerprint(body).split()
    runs = Counter(" ".join(words[i:i + size]) for i in range(len(words) - size + 1))
    return [run for run, count in runs.items() if count > 1]


def last_sentence(body: str) -> str:
    parts = [p for p in _SENTENCE_RE.split(body.strip()) if p]
    return parts[-1] if parts else ""


def ends_with_ask(body: str) -> bool:
    last = last_sentence(body).lower()
    return last.endswith("?") or any(word in last for word in ASK_WORDS)


def fact_text(sheet: FactSheet) -> str:
    """Everything the brief states as a fact about this business (what a service mention must rest on),
    including names: "Zen Yoga Studio" may say "yoga"."""
    lines = [sheet.lead, *sheet.support]
    parts = [part for line in lines for part in (line.text, line.phrase, line.phrase_hi) if part]
    return " ".join([*parts, sheet.ask.get("text", ""), sheet.ask.get("text_hi", ""), sheet.sender_name or "",
                     sheet.greeting or ""])


def unsupported_services(body: str, sheet: FactSheet, context_text: str = "") -> list[str]:
    """Category vocabulary in the body that nothing in the brief (or the chat) backs up."""
    text, basis = fingerprint(body), fingerprint(f"{fact_text(sheet)} {context_text}")
    found = []
    for term in sheet.vocabulary:
        key = fingerprint(term)
        if not key or key in GENERIC_VOCAB:
            continue
        pattern = re.compile(rf"\b{re.escape(key)}s?\b")
        if pattern.search(text) and not pattern.search(basis):
            found.append(term)
    return found


def problems(body: str, sheet: FactSheet | None, *, extra_numbers: set[str] | frozenset = frozenset(),
             mid_conversation: bool = False, max_chars: int = MAX_BODY_CHARS, context_text: str = "") -> list[str]:
    """Everything that stops an AI message from being sent. Replies (mid_conversation) may also use numbers
    and service words already said in the conversation (`extra_numbers`, `context_text`) and skip the
    first-message rules (greeting by name, a number, the ask last, naming the shop)."""
    if not body.strip():
        return ["empty body"]
    issues = []
    if sheet and sheet.kind in PROPOSAL_KINDS and not mid_conversation:
        max_chars = max(max_chars, 700)  # a plan outline needs a few lines
    if len(body) > max_chars:
        issues.append(f"too long ({len(body)} characters)")
    invented = number_tokens(body) - set(sheet.allowed_numbers if sheet else ()) - set(extra_numbers)
    if invented and sheet and sheet.kind in PROPOSAL_KINDS and not mid_conversation:
        # a plan draft may propose quantities, prices and timings; a new percentage is still a made-up statistic
        invented = {n for n in invented if re.search(rf"(?<![\d.,]){re.escape(n)}\s*%", body.replace(",", ""))}
    if invented:
        issues.append(f"numbers not in the brief: {', '.join(sorted(invented))}")
    if _URL_RE.search(body):
        issues.append("contains a link")
    taboo = [t for t in (sheet.avoid if sheet else []) if t.lower() in body.lower()]
    if taboo:
        issues.append(f"taboo words: {', '.join(taboo)}")
    if _CODE_RE.search(body):
        issues.append("internal code in the text")
    if "{" in body or "}" in body:
        issues.append("template braces")
    if body.count("?") > 1:
        issues.append("more than one question")
    if body.count("!") > 1 or len(_EMOJI_RE.findall(body)) > 1:
        issues.append("too many exclamation marks or emoji")
    if m := PREAMBLE.search(fingerprint(body)):
        issues.append(f"preamble or self-introduction ({m.group(0)!r})")
    if repeats := repeated_phrases(body):
        issues.append(f"repeats itself: {repeats[0]}")
    if not sheet:
        return issues
    if services := unsupported_services(body, sheet, context_text):
        issues.append(f"service words not in the brief: {', '.join(services)}")
    if sheet.audience == "customer" and re.search(r"\bvera\b", body, re.I):
        issues.append("customer message mentions Vera")
    if mid_conversation:
        return issues
    if sheet.audience == "customer" and sheet.sender_name:
        shop = fingerprint(" ".join(sheet.sender_name.split()[:2]))
        if shop not in fingerprint(body):
            issues.append("doesn't say which shop is writing")
    if sheet.address_as and fingerprint(sheet.address_as) not in fingerprint(body):
        issues.append("doesn't address them by name")
    if sheet.audience == "merchant" and sheet.allowed_numbers and not number_tokens(body):  # customers: no padding
        issues.append("no concrete number")
    if sheet.ask.get("cta") not in (None, "none") and not ends_with_ask(body):
        issues.append("doesn't end with the ask")
    share, closest = case_study_overlap(body)
    if share >= CASE_STUDY_LIMIT:
        issues.append(f"copies {closest} ({share:.0%} overlap)")
    return issues


def _ask(sheet: FactSheet | None) -> str:
    if not sheet:
        return "the ask"
    hinglish = sheet.language.get("hinglish") and sheet.ask.get("text_hi")
    return f'"{sheet.ask["text_hi"] if hinglish else sheet.ask["text"]}"'


# (text the problem starts with, instruction for the retry); {detail} is what follows the first ": "
_FIXES = (
    ("empty body", lambda d, s: "Write the message; the body was empty."),
    ("too long", lambda d, s: "Make it shorter: 2-4 short sentences, under 450 characters."),
    ("numbers not in the brief", lambda d, s: f"Remove {d}: not in the brief. Numbers may only come from: "
                                              f"{', '.join(s.allowed_numbers) if s else 'the conversation'}."),
    ("contains a link", lambda d, s: "Remove the link; no URLs."),
    ("taboo words", lambda d, s: f"Don't use: {d}."),
    ("internal code", lambda d, s: "Replace internal codes (words_with_underscores) with plain words."),
    ("template braces", lambda d, s: "Remove the {braces}; write the actual words."),
    ("more than one question", lambda d, s: "Ask only one question: the final ask."),
    ("too many exclamation", lambda d, s: "Use at most one exclamation mark and at most one emoji."),
    ("preamble", lambda d, s: "Drop the pleasantries and self-introduction; open with the greeting and the reason "
                              "for writing."),
    ("repeats itself", lambda d, s: f"Say it once: don't repeat \"{d}\"; each sentence should add something new."),
    ("service words not in the brief", lambda d, s: f"Don't mention {d}: the brief doesn't list them as this "
                                                    "business's services or offers. Use only the listed facts."),
    ("customer message mentions Vera", lambda d, s: f"Write as {s.sender_name if s else 'the shop'}; never mention "
                                                    "Vera."),
    ("doesn't say which shop", lambda d, s: f"Name the shop ({s.sender_name}) in the first sentence."),
    ("doesn't address them by name", lambda d, s: f"Open with the greeting: {s.greeting}."),
    ("no concrete number", lambda d, s: "Include at least one number, price or date from the brief."),
    ("doesn't end with the ask", lambda d, s: f"End with the ask as the last sentence: {_ask(s)}."),
    ("copies", lambda d, s: "Rewrite in your own words; don't copy example messages."),
    ("qualifying question", lambda d, s: "They already said yes: deliver it now; ask no qualifying questions "
                                         "(no 'would you', 'do you', 'how about')."),
    ("internal jargon", lambda d, s: "Don't mention the brief or internal terms; if something isn't known, say you "
                                     "don't have that detail."),
    ("repeats an earlier message", lambda d, s: "Write something new; don't repeat an earlier message."),
    ("reuses an earlier sentence", lambda d, s: "Don't reuse sentences from earlier messages; move the conversation "
                                                "forward."),
)


def fixes(issues: list[str], sheet: FactSheet | None) -> list[str]:
    """One instruction per problem, for the retry prompt."""
    out = []
    for issue in issues:
        detail = issue.split(": ", 1)[1] if ": " in issue else ""
        fix = next((make(detail, sheet) for marker, make in _FIXES if issue.startswith(marker)), f"Fix: {issue}.")
        if fix not in out:
            out.append(fix)
    return out


def retry_prompt(prompt: str, body: str, instructions: list[str]) -> str:
    fix_lines = "\n".join(f"- {line}" for line in instructions)
    return (f"{prompt}\n\nYour previous version:\n{body}\n\nIt can't be sent because:\n{fix_lines}\n"
            "Write it again with these fixed; keep everything else that was right.")
