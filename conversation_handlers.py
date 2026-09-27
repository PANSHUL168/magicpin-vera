"""Offline multi-turn contract (challenge-brief §7.4): respond(state, merchant_message) -> dict.

`state` is a dict with the dataset contexts and the turns so far:
    {"category": {...}, "merchant": {...}, "trigger": {...}, "customer": {...} or None,
     "turns": [{"from": "vera" | "merchant" | "customer", "body": "..."}, ...]}
It runs the same logic as the live /v1/reply on a throwaway store, so offline and live
replies behave the same. Returns {"action": "send" | "wait" | "end", ...}.
"""

from __future__ import annotations

from vera.compose import DEFAULT_REFERENCE_NOW, store_from_dicts
from vera.replies import classify
from vera.responder import handle_reply
from vera.state import RuntimeState
from vera.writer import default_cache_file

CONVERSATION_ID = "offline_conversation"


def respond(state: dict, merchant_message: str) -> dict:
    store, trigger_id = store_from_dicts(state["category"], state["merchant"], state["trigger"], state.get("customer"))
    trigger = store.data("trigger", trigger_id)
    merchant_id, customer_id = trigger["merchant_id"], trigger.get("customer_id")
    runtime = RuntimeState()
    runtime.open_conversation(CONVERSATION_ID, merchant_id=merchant_id, customer_id=customer_id,
                              trigger_id=trigger_id, now=DEFAULT_REFERENCE_NOW)
    party_role = "customer" if customer_id else "merchant"
    party_id = customer_id or merchant_id
    for turn in state.get("turns", []):
        if turn.get("from") == "vera":
            runtime.record_outbound(CONVERSATION_ID, turn.get("body", ""), now=DEFAULT_REFERENCE_NOW)
            continue
        # replay what each earlier reply meant, so a STOP or a bot's auto-reply still counts now
        conv, repeats = runtime.record_inbound(CONVERSATION_ID, turn.get("body", ""), from_role=party_role,
                                               now=DEFAULT_REFERENCE_NOW)
        kind = classify(turn.get("body", ""), repeats=repeats)
        conv.turns[-1].meta["kind"] = kind.kind
        party = runtime.party(party_id, party_role)
        if kind.kind == "opt_out":
            runtime.mark_opted_out(party_id, reason=kind.reason, role=party_role)
        elif kind.kind == "auto_reply":
            party.auto_replies += 1
        else:
            if party.opted_out and (kind.kind == "question" or (kind.kind == "commit" and not kind.detail.get("weak"))):
                party.opted_out = False  # they came back with a real request
            runtime.mark_replied(party_id, now=DEFAULT_REFERENCE_NOW, role=party_role)
    return handle_reply(store, runtime, {
        "conversation_id": CONVERSATION_ID, "merchant_id": merchant_id, "customer_id": customer_id,
        "from_role": party_role, "message": merchant_message, "received_at": DEFAULT_REFERENCE_NOW,
        "turn_number": len(state.get("turns", [])) + 1}, cache_file=default_cache_file())
