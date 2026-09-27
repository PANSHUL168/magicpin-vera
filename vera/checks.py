"""Message checks as a report: one pass/fail row per rule, for any body against its FactSheet.

The hard rows are validator.problems() (phase 4), which blocks an AI message and triggers the
retry. The one soft row (language) is advisory: the briefs allow plain English everywhere.
"""

from __future__ import annotations

from dataclasses import dataclass

from .factsheet import FactSheet
from .normalize import detect_language
from .validator import CASE_STUDY_LIMIT, case_study_overlap, problems  # noqa: F401  (re-exported)

# (row name, what validator.problems() starts that failure with, when the row applies)
HARD_ROWS = (
    ("Not empty", "empty body", None),
    ("Numbers all from the brief", "numbers not in the brief", None),
    ("No links", "contains a link", None),
    ("No taboo words", "taboo words", None),
    ("No internal codes", "internal code", None),
    ("No template braces", "template braces", None),
    ("At most one question", "more than one question", None),
    ("At most one ! and one emoji", "too many exclamation", None),
    ("No preamble or self-introduction", "preamble", None),
    ("Doesn't repeat itself", "repeats itself", None),
    ("No services the brief doesn't list", "service words not in the brief", None),
    ("Customer message speaks as the shop", "customer message mentions Vera", "customer"),
    ("Customer message names the shop", "doesn't say which shop", "customer"),
    ("Addresses them by name", "doesn't address them by name", "name"),
    ("Has a concrete number, date or price", "no concrete number", "numbers"),
    ("Ends with the ask", "doesn't end with the ask", "ask"),
    ("Not copied from a case study", "copies", None),
    ("Under 600 characters", "too long", None),
)


@dataclass
class Check:
    name: str
    ok: bool | None          # None = not applicable
    detail: str = ""
    hard: bool = True


def _not_applicable(when: str | None, sheet: FactSheet) -> str:
    if when == "customer" and sheet.audience != "customer":
        return "merchant-facing"
    if when == "name" and not sheet.address_as:
        return "no name on file"
    if when == "numbers" and (not sheet.allowed_numbers or sheet.audience == "customer"):
        return "the brief has no numbers" if not sheet.allowed_numbers else "customer message"
    if when == "ask" and sheet.ask.get("cta") in (None, "none"):
        return "no ask for this trigger"
    return ""


def run_checks(body: str, sheet: FactSheet) -> list[Check]:
    issues = problems(body, sheet)
    rows = []
    for name, marker, when in HARD_ROWS:
        skip = _not_applicable(when, sheet)
        if skip:
            rows.append(Check(name, None, skip))
            continue
        hit = next((i for i in issues if i.startswith(marker)), "")
        if name == "Not copied from a case study" and not hit:
            share, closest = case_study_overlap(body)
            rows.append(Check(name, True, f"{share:.0%} overlap with {closest}" if closest else "no overlap"))
            continue
        rows.append(Check(name, not hit, hit))

    got = detect_language(body)
    if sheet.language.get("hinglish"):
        ok, want = got in ("hi-en", "hi"), "Hinglish"
    elif "a little Hindi" in sheet.language.get("instruction", ""):
        ok, want = True, "mostly English"
    else:
        ok, want = got in ("en", "unknown"), "English"
    rows.append(Check("Language as expected", ok, f"wanted {want}, looks {got}", hard=False))
    return rows
