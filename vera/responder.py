"""Phase 5: answer /v1/reply. Log the message, classify it, decide send / wait / end, write the reply.

Most decisions are rules (replies.classify). Only real conversation turns (a yes, a question,
a normal reply) go to the AI; if it's off, late or fails a check, fixed wording goes out.
Auto-replies are counted per party (merchant or customer), not per conversation: the local
simulator's auto-reply test opens a new conversation_id every turn. Nothing is ever sent twice
in one conversation (the judge's -2 anti-repetition rule).
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import logging
import os
import re
import time
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path

from . import llm, validator, writer
from .bundle import build_bundle
from .factsheet import FactSheet, build_fact_sheet
from .normalize import detect_language, fingerprint, iso_z, number_tokens, parse_dt
from .replies import ReplyKind, classify
from .state import Conversation, PartyState, RuntimeState
from .store import ContextStore

log = logging.getLogger("vera.replies")

REPLY_PROMPT_VERSION = "r4"
MAX_REPLY_CHARS = 700
# Asking these after a "yes" is the brief's intent-handoff failure (Pattern D).
QUALIFYING = ("would you", "do you", "can you tell", "what if", "how about", "could you tell")
JARGON = re.compile(r"\b(brief|fact sheet|payload|trigger|the facts (given|provided)|given facts)\b", re.I)
_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=8, thread_name_prefix="vera-reply")
CACHE_FILE: Path | None = None  # offline tools may set this; the live server keeps AI replies in memory only

REPLY_INSTRUCTIONS = """\
You write the next WhatsApp reply in an ongoing conversation: Vera (magicpin's assistant for Indian \
local businesses) talking to a merchant, or a shop talking to its own customer.

Rules:
1. Facts: use only the brief and the conversation. Never invent offers, services, prices, numbers, dates, \
names, results or promises. Never mention the brief or "the facts"; if something isn't known, just say you \
don't have that detail.
2. Follow the goal. After a yes, deliver the thing itself (a short draft, checklist or confirmation) and \
never ask qualifying questions ("would you", "do you", "how about", "what if").
3. Reply in the language given. Hinglish means natural Roman-script Hindi-English, always in respectful \
"aap" forms ("kijiye", "rakhiye", never "karo", "rakho"); Vera uses feminine verb forms ("bhej rahi hoon").
4. Move the conversation forward: never reuse sentences from earlier messages, and don't repeat the first \
message's ask once they've answered it. Don't greet again or introduce yourself. No links, no markdown.
5. 1-4 short sentences; a delivered draft may add up to 3 short lines. Under 600 characters.
6. End with at most one question or a single clear next step.

Return JSON: "body" is the reply; "rationale" is one English sentence on what it does and why."""

_KIND_LABELS = {"commit": "agreed to go ahead", "question": "asked a question", "engaged": "replied"}
_GOALS = {
    "commit": "Deliver what was offered right now: the draft, checklist, steps or confirmation itself, built only "
              "from the brief's facts. End with one simple next step such as 'Reply CONFIRM to publish'. "
              "No qualifying questions.",
    "question": "Answer the question directly from the brief's facts. If the facts don't cover it, say so briefly "
                "and offer the next step.",
    "engaged": "Respond to what they said and move one step forward, ending with one simple next step.",
}
# A conversation the judge opened itself has no offer to say yes to: pick one next step from the facts.
_GOAL_NO_OFFER = ("They agreed, but nothing specific was offered in this chat yet. Pick the single most useful next "
                  "step the brief's facts support, deliver a short draft of it now, and end with one simple next step "
                  "such as 'Reply CONFIRM to publish'. No qualifying questions.")
# First-message lines that don't apply mid-conversation (the ask is shown separately, as history).
_SKIP_BRIEF_LINES = ("Write one WhatsApp message.", "Greeting:", "Format:", "Angle:", "Ask, one only",
                     "- One ask only")
# The stand-in brief's trigger is made up, so its "why now" means nothing either.
_SKIP_STAND_IN_LINES = ("Why now:", "- The trigger (")

# (English, Hinglish) variants; the first one not already sent in the conversation is used.
FIXED = {
    "owner_note": [("Looks like an auto-reply. When the owner sees this, just reply YES and I'll take it from there.",
                    "Lagta hai yeh auto-reply hai. Owner jab dekhein, bas YES reply kar dijiye, main aage sambhal "
                    "loongi.")],
    "apology": [("Sorry for the bother. I'll keep messages to a minimum; reply STOP anytime and I won't message "
                 "again.", "Pareshani ke liye maafi. Main messages kam rakhoongi; kabhi bhi STOP reply kijiye, phir "
                           "message nahi aayega.")],
    "apology_customer": [("Sorry for the bother. Reply STOP anytime and we won't message again.",
                          "Pareshani ke liye maafi. Kabhi bhi STOP reply kijiye, phir message nahi aayega.")],
    "off_topic_gst": [("GST filing is best handled by your CA; it's outside what I can help with.",
                       "GST filing ke liye aapke CA sabse sahi rahenge; yeh mere scope se bahar hai.")],
    "off_topic": [("That's outside what I can help with, sorry.", "Yeh mere scope se bahar hai, maaf kijiye.")],
    "off_topic_customer": [("Sorry, that's not something we can help with here.",
                            "Maaf kijiye, is baare mein hum yahan help nahi kar paayenge.")],
    "steer_back": [("Coming back to our chat: {ask}", "Wapas apni baat par: {ask}")],
    "steer_back_generic": [("I'm here whenever you want help with your Google profile, offers or posts.",
                            "Google profile, offers ya posts mein help chahiye ho toh main yahin hoon.")],
    "steer_back_generic_customer": [("We're here if you need anything else.", "Aur kuch chahiye ho toh hum yahin hain.")],
    "slot_booked": [("Done, you're booked for {slot}. See you then!",
                     "Ho gaya, aapka slot {slot} ke liye book hai. Milte hain!")],
    "action_after_draft": [("Done, going ahead with the draft above. I'll confirm here once it's live.",
                            "Ho gaya, upar wale draft ke saath aage badh rahi hoon. Live hote hi yahin confirm "
                            "karungi.")],
    "action_later": [("Noted, I'll pick this up {when} and send it here.",
                      "Theek hai, main ise {when_hi} aage badhaungi aur yahin bhejungi.")],
    "action": [("Great, I'm on it. Sending the first draft here shortly for you to check.",
                "Badhiya, main shuru kar rahi hoon. First draft thodi der mein yahin bhej rahi hoon."),
               ("Done, I'm starting now. You'll have the draft here shortly.",
                "Ho gaya, main abhi shuru kar rahi hoon. Draft jald hi yahin milega.")],
    "action_customer": [("Great, we'll take care of it and confirm here shortly.",
                         "Badhiya, hum ise sambhal lenge aur yahin confirm kar denge."),
                        ("Noted, we're on it and will confirm here soon.",
                         "Note kar liya, hum jald hi yahin confirm karte hain.")],
    "answer": [("Good question. I'll put the details together and send them here shortly.",
                "Achha sawaal hai. Main details tayyar karke thodi der mein yahin bhej rahi hoon."),
               ("Let me check that and come back to you here with the details.",
                "Main yeh check karke details ke saath yahin wapas aati hoon.")],
    "answer_customer": [("Thanks for asking. We'll check and reply here shortly.",
                         "Poochne ke liye shukriya. Hum check karke yahin batate hain."),
                        ("Good question, we'll get back to you here soon.",
                         "Achha sawaal hai, hum jald hi yahin batate hain.")],
    "engaged": [("Thanks! I'll send the next step here shortly.",
                 "Shukriya! Agla step thodi der mein yahin bhej rahi hoon."),
                ("Got it. I'll share the next step here soon.", "Samajh gayi. Agla step jald hi yahin share karti hoon.")],
    "engaged_customer": [("Thanks for letting us know!", "Batane ke liye shukriya!"),
                         ("Noted, thank you!", "Note kar liya, shukriya!")],
}


@dataclass
class ReplyContext:
    sheet: FactSheet | None          # the brief behind this conversation, or a stand-in built from merchant data
    own_trigger: bool                # True when we started this conversation from a trigger
    audience: str                    # "merchant" or "customer"
    hinglish: bool                   # the recipient's usual language
    shop: str | None
    slot_labels: list[str] = field(default_factory=list)


def reply_deadline() -> float:
    try:
        return float(os.getenv("VERA_REPLY_DEADLINE", "8"))
    except ValueError:
        return 8.0


def _stand_in_sheet(store: ContextStore, conv: Conversation, now: str) -> FactSheet:
    """A brief for a conversation the judge opened itself: the merchant's facts, no trigger."""
    temp = ContextStore()
    merchant = store.get("merchant", conv.merchant_id)
    temp.ingest({"scope": "merchant", "context_id": merchant.context_id, "version": 1, "payload": merchant.payload})
    category = store.get("category", merchant.data.get("category_slug"))
    if category:
        temp.ingest({"scope": "category", "context_id": category.context_id, "version": 1, "payload": category.payload})
    customer = store.get("customer", conv.customer_id) if conv.customer_id else None
    if customer:
        temp.ingest({"scope": "customer", "context_id": customer.context_id, "version": 1, "payload": customer.payload})
    temp.ingest({"scope": "trigger", "context_id": "reply_context", "version": 1, "payload": {
        "id": "reply_context", "kind": "conversation_followup", "scope": "customer" if customer else "merchant",
        "merchant_id": merchant.context_id, "customer_id": customer.context_id if customer else None, "payload": {}}})
    return build_fact_sheet(build_bundle(temp, "reply_context", now=now))


def _context(store: ContextStore, state: RuntimeState, conv: Conversation, now: str) -> ReplyContext:
    if conv.trigger_id and store.get("trigger", conv.trigger_id):
        bundle = build_bundle(store, conv.trigger_id, now=now, state=state)
        sheet = build_fact_sheet(bundle, state=state)
        slots = [s["safe_label"] for s in bundle.slots] if sheet.ask["cta"] == "multi_choice_slot" else []
        return ReplyContext(sheet, True, sheet.audience, bool(sheet.language.get("hinglish")), sheet.sender_name, slots)
    if conv.merchant_id and store.get("merchant", conv.merchant_id):
        sheet = _stand_in_sheet(store, conv, now)
        return ReplyContext(sheet, False, sheet.audience, bool(sheet.language.get("hinglish")), sheet.sender_name)
    return ReplyContext(None, False, "customer" if conv.customer_id else "merchant", False, None)


def _hinglish_now(message: str, ctx: ReplyContext) -> bool:
    """Mirror the language of this message (brief §12.4); short or unclear ones keep the usual language."""
    got = detect_language(message)
    if got in ("hi", "hi-en"):
        return True
    if got == "en" and len(fingerprint(message).split()) >= 3:
        return False
    return ctx.hinglish


def _fixed(key: str, ctx: ReplyContext, hinglish: bool, conv: Conversation, state: RuntimeState, **fmt) -> str | None:
    variants = FIXED.get(f"{key}_customer") if ctx.audience == "customer" else None
    for english, hindi in variants or FIXED[key]:
        text = (hindi if hinglish else english).format(**fmt)
        if not state.already_sent(conv.conversation_id, text):
            return text
    return None


def _reply_prompt(ctx: ReplyContext, conv: Conversation, message: str, kind: ReplyKind, hinglish: bool) -> str:
    lines = []
    if ctx.sheet:
        skip = _SKIP_BRIEF_LINES if ctx.own_trigger else _SKIP_BRIEF_LINES + _SKIP_STAND_IN_LINES
        brief = [line for line in ctx.sheet.to_prompt().splitlines() if not line.startswith(skip)]
        lines += ["Background brief (facts you may use):", *brief, ""]
        if ctx.own_trigger:
            ask = ctx.sheet.ask["text_hi"] if ctx.hinglish and ctx.sheet.ask.get("text_hi") else ctx.sheet.ask["text"]
            lines += [f"Our first message asked: {ask}", ""]
    else:
        lines += ["No business data is available: state no facts, numbers or offers; keep to the next step.", ""]
    lines.append("Conversation so far (oldest first):")
    for turn in conv.turns[:-1][-8:]:
        who = (ctx.shop or "Shop") if turn.sender == "bot" and ctx.audience == "customer" else \
            "Vera" if turn.sender == "bot" else turn.sender.capitalize()
        lines.append(f"{who}: {turn.body}")
    offered = ctx.own_trigger or any(turn.sender == "bot" for turn in conv.turns)
    goal = _GOAL_NO_OFFER if kind.kind == "commit" and not offered else _GOALS[kind.kind]
    lines += ["", f'Latest message: "{message}"', f"They {_KIND_LABELS[kind.kind]}.", f"Goal: {goal}",
              f"Language for this reply: {'Hinglish (Roman-script Hindi-English)' if hinglish else 'English'}."]
    if ctx.audience == "customer":
        lines.append(f"Write as {ctx.shop or 'the shop'}, not as Vera.")
    return "\n".join(lines)


def _reply_problems(body: str, ctx: ReplyContext, conv: Conversation, kind: ReplyKind,
                    state: RuntimeState) -> list[str]:
    said = set()
    for turn in conv.turns:  # numbers the merchant or we already used are fair to repeat
        said |= number_tokens(turn.body)
    chat = " ".join(turn.body for turn in conv.turns)  # service words they or we already used are fair game
    issues = validator.problems(body, ctx.sheet, extra_numbers=said, mid_conversation=True, max_chars=MAX_REPLY_CHARS,
                                context_text=chat)
    if kind.kind == "commit":
        hits = [q for q in QUALIFYING if q in body.lower()]
        if hits:
            issues.append(f"qualifying question after a yes ({hits[0]!r})")
    if state.already_sent(conv.conversation_id, body):
        issues.append("repeats an earlier message")
    if m := JARGON.search(body):
        issues.append(f"internal jargon ({m.group(0)!r})")
    earlier = [fingerprint(turn.body) for turn in conv.turns if turn.sender == "bot"]
    for sentence in re.split(r"[.!?\n]+", body):
        words = fingerprint(sentence)
        if len(words.split()) >= 8 and any(words in old for old in earlier):
            issues.append(f"reuses an earlier sentence ({sentence.strip()[:40]!r})")
            break
    return issues


def _reply_key(prompt: str) -> str:
    raw = f"{REPLY_PROMPT_VERSION}\n{llm.model_name()}\n{REPLY_INSTRUCTIONS}\n{prompt}"
    return "reply:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def _ai_reply(ctx: ReplyContext, conv: Conversation, message: str, kind: ReplyKind, hinglish: bool,
              state: RuntimeState, cache_file: Path | None) -> tuple[str, str] | None:
    """The AI's reply if it passes the checks (after at most one retry with feedback) within the deadline."""
    prompt = _reply_prompt(ctx, conv, message, kind, hinglish)
    ends = time.monotonic() + reply_deadline()
    future = _POOL.submit(
        writer.generate_checked, REPLY_INSTRUCTIONS, prompt, key=_reply_key,
        check=lambda body: _reply_problems(body, ctx, conv, kind, state),
        fix=lambda issues: validator.fixes(issues, ctx.sheet), name="vera_reply", cache_file=cache_file,
        deadline=ends, label=conv.conversation_id, meta={"conversation_id": conv.conversation_id})
    try:
        entry, reason = future.result(timeout=max(0.0, ends - time.monotonic()))
    except concurrent.futures.TimeoutError:
        log.warning("AI reply for %s took too long; using fixed wording", conv.conversation_id)
        return None
    if entry is None:
        log.info("AI reply for %s not used (%s); using fixed wording", conv.conversation_id, reason)
        return None
    return entry["body"], entry["rationale"]


def _cta_of(body: str) -> str:
    """The CTA the body actually ends with, so the label never disagrees with the text."""
    if re.search(r"\bCONFIRM\b", body):
        return "binary_confirm_cancel"
    if re.search(r"\bYES\b", body):
        return "binary_yes_no"
    return "open_ended" if body.rstrip().endswith("?") else "none"


def _send(state: RuntimeState, conv: Conversation, text: str, cta: str, rationale: str, now: str, kind: str) -> dict:
    if conv.status == "ended":
        conv.status = "open"  # they came back; the conversation is live again
    state.record_outbound(conv.conversation_id, text, now=now, merchant_id=conv.merchant_id,
                          customer_id=conv.customer_id, meta={"cta": cta, "reply_to": kind})
    return {"action": "send", "body": text, "cta": cta, "rationale": rationale}


def _wait(state: RuntimeState, conv: Conversation, seconds: int, rationale: str, now: str) -> dict:
    state.set_waiting(conv.conversation_id, until=iso_z(parse_dt(now) + timedelta(seconds=seconds)))
    return {"action": "wait", "wait_seconds": seconds, "rationale": rationale}


def _end(state: RuntimeState, conv: Conversation, rationale: str) -> dict:
    state.end_conversation(conv.conversation_id, reason=rationale)
    return {"action": "end", "rationale": rationale}


def _decide(state: RuntimeState, conv: Conversation, ctx: ReplyContext, party: PartyState | None, kind: ReplyKind,
            message: str, hinglish: bool, now: str, cache_file: Path | None) -> dict:
    k = kind.kind
    if party and party.opted_out:
        if k != "question" and (k != "commit" or kind.detail.get("weak")):  # a bare "ok" isn't a comeback
            return _end(state, conv, "They asked us to stop earlier; staying quiet.")
        party.opted_out = False  # they came back with a real request

    if k == "opt_out":
        if party:
            state.mark_opted_out(party.party_id, reason=kind.reason, role=party.role)
        return _end(state, conv, f"They {kind.reason}; closing and not messaging again.")
    if k == "auto_reply":
        count = 1
        if party:
            party.auto_replies += 1
            count = party.auto_replies
        if count == 1 and ctx.audience == "merchant":
            text = _fixed("owner_note", ctx, hinglish, conv, state)
            if text:
                return _send(state, conv, text, "binary_yes_no",
                             f"Auto-reply detected ({kind.reason}); one note for the owner, then back off.", now, k)
        if count <= 2:
            return _wait(state, conv, 86400, f"Auto-reply again ({kind.reason}); the owner isn't at the phone, "
                                             "so waiting a day.", now)
        return _end(state, conv, f"Auto-reply {count} times with no real reply; closing the conversation.")
    if k == "empty":
        return _wait(state, conv, 1800, "Empty message; checking back in 30 minutes.", now)
    if k == "later":
        seconds = kind.detail["wait_seconds"]
        return _wait(state, conv, seconds, f"They're busy ({kind.reason}); backing off {seconds // 60} minutes.", now)
    if k == "decline":
        return _end(state, conv, "They said no; closing politely without pushing.")
    if k == "thanks":
        return _end(state, conv, "They said thanks; nothing more to add.")
    if k == "hostile":
        if any(t.meta.get("kind") == "hostile" for t in conv.turns[:-1]):
            return _end(state, conv, "Frustrated a second time; closing.")
        text = _fixed("apology", ctx, hinglish, conv, state)
        if text:
            return _send(state, conv, text, "none",
                         f"They're frustrated ({kind.reason}); one apology and an easy way to stop.", now, k)
        return _end(state, conv, "Frustrated; closing.")
    if k == "slot_pick":
        slot = ctx.slot_labels[kind.detail["slot"]]
        text = _fixed("slot_booked", ctx, hinglish, conv, state, slot=slot)
        if text:
            return _send(state, conv, text, "none", f"Booked the slot they picked ({slot}).", now, k)
        return _end(state, conv, "Slot already confirmed.")
    if k == "off_topic":
        decline = _fixed("off_topic_gst" if kind.detail.get("topic") == "gst" else "off_topic",
                         ctx, hinglish, conv, state) or ""
        if ctx.own_trigger and ctx.sheet:
            ask = ctx.sheet.ask["text_hi"] if hinglish and ctx.sheet.ask.get("text_hi") else ctx.sheet.ask["text"]
            back, cta = _fixed("steer_back", ctx, hinglish, conv, state, ask=ask), ctx.sheet.ask["cta"]
        else:
            back, cta = _fixed("steer_back_generic", ctx, hinglish, conv, state), "none"
        text = f"{decline} {back or ''}".strip()
        if text and not state.already_sent(conv.conversation_id, text):
            return _send(state, conv, text, cta, f"Out-of-scope ask ({kind.reason}); declined politely and steered "
                                                 "back to the topic.", now, k)
        return _wait(state, conv, 1800, "Out-of-scope ask again; not repeating myself.", now)

    if k == "commit" and kind.detail.get("later"):  # "go ahead tomorrow": acknowledge the timing, don't act now
        when = kind.detail["later"]
        text = _fixed("action_later", ctx, hinglish, conv, state, when=when,
                      when_hi="kal" if when == "tomorrow" else "thodi der baad")
        if text:
            return _send(state, conv, text, "none", f"They agreed but asked for {when}; confirmed the timing.", now, k)
    # commit / question / engaged: the AI writes it; fixed wording if it can't
    ai = _ai_reply(ctx, conv, message, kind, hinglish, state, cache_file)
    if ai:
        body, rationale = ai
        return _send(state, conv, body, _cta_of(body), rationale or f"They {_KIND_LABELS[k]}; answered.", now, k)
    key = {"commit": "action", "question": "answer", "engaged": "engaged"}[k]
    if k == "commit" and ctx.audience == "merchant" and any(
            turn.sender == "bot" and "draft" in turn.body.lower() for turn in conv.turns[1:]):
        key = "action_after_draft"  # a draft is already on the table: go ahead with it
    text = _fixed(key, ctx, hinglish, conv, state) or (
        _fixed("action", ctx, hinglish, conv, state) if key == "action_after_draft" else None)
    if text:
        return _send(state, conv, text, "none", f"{_KIND_LABELS[k].capitalize()}: "
                                                f"{'moving straight to action' if k == 'commit' else 'acknowledged'}"
                                                " (fixed wording).", now, k)
    return _wait(state, conv, 1800, "Nothing new to say without repeating myself; checking back later.", now)


def handle_reply(store: ContextStore, state: RuntimeState, body: dict, *, cache_file: Path | str | None = None) -> dict:
    """One /v1/reply request in, the {action: send | wait | end, ...} response out.

    `cache_file` keeps AI replies on disk (offline tools only; the live server keeps them in memory).
    """
    conversation_id = body["conversation_id"]
    from_role = body.get("from_role") if body.get("from_role") in ("merchant", "customer") else "merchant"
    message = str(body.get("message") or "")
    received = parse_dt(body.get("received_at"))
    now = iso_z(received) if received else iso_z()
    conv, repeats = state.record_inbound(conversation_id, message, from_role=from_role, now=now,
                                        merchant_id=body.get("merchant_id"), customer_id=body.get("customer_id"),
                                        turn_number=body.get("turn_number"))
    ctx = _context(store, state, conv, now)
    kind = classify(message, repeats=repeats, slot_labels=ctx.slot_labels or None)
    conv.turns[-1].meta["kind"] = kind.kind
    party_id = conv.customer_id if from_role == "customer" else conv.merchant_id
    party = state.party(party_id, from_role) if party_id else None
    if party_id and kind.kind != "auto_reply":  # a bot's canned text doesn't open the 24h window
        state.mark_replied(party_id, now=now, role=from_role)
    response = _decide(state, conv, ctx, party, kind, message, _hinglish_now(message, ctx), now,
                       Path(cache_file) if cache_file else CACHE_FILE)
    log.info("reply %s [%s: %s] -> %s", conversation_id, kind.kind, kind.reason, response["action"])
    return response
