"""Phase 3: the AI writer. Rewrites a FactSheet's plain draft into a natural message.

write_ai() only returns a message that passes the validator (phase 4, validator.problems);
a message that fails gets one retry with the problems as feedback, and if that fails too
the caller keeps the plain draft. Results, rejections included, are cached by a fingerprint
of model + instructions + prompt: the same brief always gives the same answer, and reruns
cost no tokens. Cached results are checked again when read, so a new rule applies to them too.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import threading
import time
from collections import Counter
from collections.abc import Callable
from pathlib import Path

from . import llm
from .factsheet import FactSheet
from .validator import MAX_BODY_CHARS, fixes, problems, retry_prompt  # noqa: F401  (problems is re-exported)

log = logging.getLogger("vera.writer")

PROMPT_VERSION = "v4"
STATS: Counter[str] = Counter()     # ai / cached / rejected / error / off / retried / retry_ok, for reporting
RETRY_ESTIMATE = 4.0                # seconds a retry is assumed to take when the first answer came from the cache

INSTRUCTIONS = """\
You write one WhatsApp message for Vera, magicpin's assistant for Indian local businesses, \
or for a shop writing to its own customer.

You get a writing brief and a plain draft whose facts are correct but whose wording is stiff. \
Rewrite the draft into the message a sharp, friendly account manager would send.

Rules:
1. Facts: use only facts from the brief. Every number, price, date, name and source must come from it. \
Never invent offers, services, statistics, competitors, deadlines, results or promises, and don't claim \
causes the brief doesn't state. Don't promise outcomes the facts don't show (not "renewal keeps your visibility", \
not "this reaches all 4,200 customers"): say what the data shows and what you suggest.
2. Open with the brief's greeting and the reason for writing now (its "Why now"). A customer message \
names the shop in its first sentence ("<shop> here").
3. Include at least one concrete number, price, date or source from the brief, and connect the facts: \
say why they matter to this reader. Use only the supporting facts that make the point; skip any that don't fit. \
Add judgment where the facts support it: what you'd do or skip, and why (e.g. skip ad spend in a seasonal lull, \
push delivery on a weekend match night).
4. Follow the brief's voice and language lines. Hinglish means natural Roman-script Hindi-English, \
the way Indian business owners text; Vera uses feminine Hindi verb forms ("bhej rahi hoon"). \
No hype, no ALL CAPS, at most one emoji.
5. 2-4 short sentences, under 450 characters, plain text with no markdown or links. When the brief's Format line \
asks for an outline, use up to 4 short lines starting with "- ", under 650 characters.
6. End with exactly one ask, as the last sentence, of the type the brief gives (yes/no, confirm, \
pick a slot, or an open question), worded naturally in the message's language. Keep the ask's concrete deliverable \
and any time estimate ("ready in 5 min"): it shows exactly what Vera will do for them. Ask no other questions.
7. No preamble ("hope you're well") and no self-introduction. Customer messages speak as the shop, never as Vera.

Return JSON: "body" is the message; "rationale" is one or two English sentences on why this message, \
the fact it anchors on and the lever it uses."""

SCHEMA = {
    "type": "object",
    "properties": {"body": {"type": "string"}, "rationale": {"type": "string"}},
    "required": ["body", "rationale"],
    "additionalProperties": False,
}

_SENTENCES_RE = re.compile(r"(?<=[.?!])\s+")


class MessageCache:
    """In memory always; also on disk when given a file (offline tools only, never the live server)."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._memory: dict[str, dict] = {}
        self._loaded: set[Path] = set()

    def _load(self, path: Path | None) -> None:
        if path and path not in self._loaded:
            self._loaded.add(path)
            if path.exists():
                self._memory.update(json.loads(path.read_text(encoding="utf-8")))

    def get(self, key: str, path: Path | None = None) -> dict | None:
        with self._lock:
            self._load(path)
            return self._memory.get(key)

    def put(self, key: str, value: dict, path: Path | None = None) -> None:
        with self._lock:
            self._load(path)
            self._memory[key] = value
            if path:
                path.parent.mkdir(parents=True, exist_ok=True)
                tmp = path.with_suffix(".tmp")
                tmp.write_text(json.dumps(self._memory, ensure_ascii=False, indent=1, sort_keys=True),
                               encoding="utf-8")
                tmp.replace(path)

    def clear(self) -> None:
        with self._lock:
            self._memory.clear()
            self._loaded.clear()


CACHE = MessageCache()


def build_prompt(sheet: FactSheet, draft: dict) -> str:
    return f"{sheet.to_prompt()}\n\nPlain draft (correct facts, stiff wording). Rewrite it:\n{draft['body']}"


def fingerprint(prompt: str) -> str:
    raw = f"{PROMPT_VERSION}\n{llm.model_name()}\n{INSTRUCTIONS}\n{prompt}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def _template_params(greeting: str, body: str) -> list[str]:
    """{{1}} greeting, {{2}} opening sentence, {{3}} middle, {{4}} the ask (last sentence)."""
    sentences = [s for s in _SENTENCES_RE.split(body.strip()) if s]
    if len(sentences) == 1:
        return [greeting, sentences[0], "", ""]
    return [greeting, sentences[0], " ".join(sentences[1:-1]), sentences[-1]]


def _cached_call(instructions: str, prompt: str, key: str, *, name: str, path: Path | None, label: str,
                 meta: dict) -> tuple[dict | None, str, float | None]:
    """(entry, reason, seconds the call took or None if cached) for one prompt; errors are not cached."""
    entry = CACHE.get(key, path)
    if entry is not None:
        STATS["cached"] += 1
        return entry, "cached", None
    if not llm.enabled():
        STATS["off"] += 1
        return None, "llm off", None
    try:
        result = llm.complete_json(instructions, prompt, SCHEMA, name=name)
    except llm.LLMError as exc:
        STATS["error"] += 1
        log.warning("AI call for %s failed: %s", label, exc)
        return None, str(exc), None
    entry = {**meta, "model": result.model, "body": str(result.data.get("body", "")).strip(),
             "rationale": str(result.data.get("rationale", "")).strip(), "rejected": []}
    return entry, "new", result.seconds


def generate_checked(instructions: str, prompt: str, *, key: Callable[[str], str], check: Callable[[str], list[str]],
                     fix: Callable[[list[str]], list[str]], name: str, cache_file: Path | str | None = None,
                     deadline: float | None = None, label: str = "", meta: dict | None = None
                     ) -> tuple[dict | None, str]:
    """Write, check, and retry once with the problems as feedback (phase 4).

    Returns (entry, "ok" | "retried") for a body that passed `check`, else (None, reason). Both attempts are
    cached (with what was wrong), so reruns cost nothing. `deadline` is a time.monotonic() value: a retry
    that can't finish before it isn't started.
    """
    path = Path(cache_file) if cache_file else None
    entry, reason, took = _cached_call(instructions, prompt, key(prompt), name=name, path=path, label=label,
                                       meta=meta or {})
    if entry is None:
        return None, reason
    issues = check(entry["body"])
    if reason == "new":
        CACHE.put(key(prompt), {**entry, "rejected": issues}, path)
        STATS["rejected" if issues else "ai"] += 1
    if not issues:
        return entry, "ok"
    log.warning("AI message for %s rejected: %s", label, "; ".join(issues))
    if deadline is not None and time.monotonic() + 1.2 * (took or RETRY_ESTIMATE) > deadline:
        return None, "; ".join(issues) + " (no time to retry)"
    second_prompt = retry_prompt(prompt, entry["body"], fix(issues))
    STATS["retried"] += 1
    second, reason, _ = _cached_call(instructions, second_prompt, key(second_prompt), name=name, path=path,
                                     label=label, meta={**(meta or {}), "retry_of": key(prompt)})
    if second is None:
        return None, reason
    again = check(second["body"])
    if reason == "new":
        CACHE.put(key(second_prompt), {**second, "rejected": again}, path)
    if again:
        log.warning("AI retry for %s rejected too: %s", label, "; ".join(again))
        return None, "; ".join(again)
    STATS["retry_ok"] += 1
    return second, "retried"


def write_ai(sheet: FactSheet, draft: dict, *, cache_file: Path | str | None = None,
             deadline: float | None = None) -> tuple[dict | None, str]:
    """(message, "ok" | "retried") for an AI rewrite that passed the validator, else (None, reason)."""
    entry, reason = generate_checked(
        INSTRUCTIONS, build_prompt(sheet, draft), key=fingerprint, check=lambda body: problems(body, sheet),
        fix=lambda issues: fixes(issues, sheet), name="vera_message", cache_file=cache_file, deadline=deadline,
        label=sheet.trigger_id, meta={"trigger_id": sheet.trigger_id})
    if entry is None:
        return None, reason
    return {**draft, "body": entry["body"], "rationale": entry["rationale"] or draft["rationale"],
            "template_params": _template_params(sheet.greeting, entry["body"]), "writer": "ai",
            "retried": reason == "retried"}, reason


def default_cache_file() -> Path:
    from .config import ROOT
    return Path(os.getenv("VERA_AI_CACHE_FILE") or ROOT / ".cache" / "ai_messages.json")
