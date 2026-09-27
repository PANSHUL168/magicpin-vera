"""Plain, AI-free rendering of a FactSheet into a WhatsApp message.

This is the fallback writer, and phase 2's working bot: greeting, the lead, up to two
supporting facts, then the single ask. Every word comes from the sheet, so every number
in the body is in sheet.allowed_numbers.
"""

from __future__ import annotations

from .factsheet import CTA_LABELS, FactSheet, Line
from .normalize import humanize


def _sentence(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    text = text[0].upper() + text[1:]
    return text if text[-1] in ".?!" else text + "."


def _words(line: Line, hinglish: bool) -> str:
    return (line.phrase_hi if hinglish and line.phrase_hi else line.phrase).strip()


def _rationale(sheet: FactSheet, used: list[Line]) -> str:
    kind = humanize(sheet.kind)
    parts = [f"{kind[:1].upper()}{kind[1:]}: {sheet.lead.text}."]
    if used:
        parts.append("Backed by " + "; ".join(line.text for line in used) + ".")
    parts.append(f"Angle: {sheet.angle}; one {CTA_LABELS.get(sheet.ask['cta'], sheet.ask['cta'])} ask.")
    if sheet.language["hinglish"]:
        parts.append("Hinglish where their language preference calls for it.")
    parts.extend(note[:1].upper() + note[1:] + "." for note in sheet.notes if not note.startswith("digest item"))
    return " ".join(parts)


def render(sheet: FactSheet) -> dict:
    """The message fields /v1/tick and compose() return, plus template name and params."""
    hinglish = sheet.language["hinglish"]
    lead = _words(sheet.lead, hinglish) or sheet.lead.text
    if sheet.audience == "customer":
        opener = f"{sheet.greeting}, {sheet.sender_name} here." if sheet.sender_name else _sentence(sheet.greeting)
        lead_sentence = _sentence(lead)
        head = f"{opener} {lead_sentence}"
    else:
        lead_sentence = _sentence(lead)
        head = _sentence(f"{sheet.greeting}, {lead}")

    used, support = [], []
    for line in sheet.support:
        words = _words(line, hinglish)
        if words:
            support.append(_sentence(words))
            used.append(line)
        if len(support) >= sheet.render_support:
            break
    ask = sheet.ask["text_hi"] if hinglish and sheet.ask.get("text_hi") else sheet.ask["text"]

    return {
        "body": " ".join(part for part in (head, *support, ask) if part),
        "cta": sheet.ask["cta"],
        "send_as": sheet.send_as,
        "suppression_key": sheet.suppression_key,
        "rationale": _rationale(sheet, used),
        "template_name": sheet.template["name"],
        # {{1}} greeting, {{2}} why now, {{3}} supporting facts, {{4}} the ask
        "template_params": [sheet.greeting, lead_sentence, " ".join(support), ask],
    }
