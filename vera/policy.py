"""Choose which triggers to act on at a /v1/tick.

Rules only, no scoring: drop what can't be sent, group what's left by recipient (the
merchant, or the customer for customer-facing triggers), keep the most urgent trigger
per recipient and cap the total. Triggers not picked are not marked as used, so they
stay eligible for later ticks.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from .bundle import ContextBundle, build_bundle, resolve_now
from .normalize import iso_z, parse_dt
from .state import RuntimeState
from .store import ContextStore

MAX_ACTIONS = 20                    # challenge-testing-brief §5: action cap per tick
UNANSWERED_LIMIT = 3                # challenge-brief §12: stop after 3 unanswered nudges
REMINDER_KINDS = {"recall_due", "appointment_tomorrow", "chronic_refill_due"}
_FAR_FUTURE = datetime.max.replace(tzinfo=timezone.utc)


def _cooldown() -> timedelta:
    """Minimum gap between two bot-started messages to the same recipient (VERA_COOLDOWN_MINUTES)."""
    try:
        return timedelta(minutes=float(os.getenv("VERA_COOLDOWN_MINUTES", "30")))
    except ValueError:
        return timedelta(minutes=30)


@dataclass
class TickPlan:
    now: str
    chosen: list[ContextBundle] = field(default_factory=list)
    skipped: list[dict] = field(default_factory=list)   # [{"trigger_id", "reason"}]


def recipient_of(bundle: ContextBundle) -> str | None:
    if bundle.audience == "customer":
        return bundle.trigger.get("customer_id")
    return bundle.trigger.get("merchant_id") or (bundle.merchant or {}).get("merchant_id")


def _skip_reason(bundle: ContextBundle, state: RuntimeState | None, now: datetime,
                 cooldown: timedelta) -> str | None:
    if bundle.missing:
        return "waiting for data: " + ", ".join(bundle.missing)
    if bundle.has("opted_out"):
        return "recipient opted out"
    if bundle.has("suppression_key_used"):
        return "already sent (suppression key used)"
    if bundle.has("category_not_relevant"):
        return "event doesn't apply to this category"
    recipient = recipient_of(bundle)
    if not recipient:
        return "no recipient"
    if bundle.audience == "customer":
        consent = bundle.consent or {}
        if consent.get("checked") and not consent.get("scopes"):
            return "customer has no messaging consent"
        if bundle.has("reminders_opted_out") and bundle.trigger["kind"] in REMINDER_KINDS:
            return "customer hasn't opted in to reminders"
    elif bundle.history.get("unanswered_streak", 0) >= UNANSWERED_LIMIT:
        return f"{UNANSWERED_LIMIT} messages already unanswered"
    if state is None:
        return None
    party = state.parties.get(recipient)
    if party:
        if bundle.audience == "customer" and party.unanswered_outbound >= UNANSWERED_LIMIT:
            return f"{UNANSWERED_LIMIT} messages already unanswered"
        last = parse_dt(party.last_outbound_at)
        if last and timedelta(0) <= now - last < cooldown:
            return f"messaged {int((now - last).total_seconds() // 60)} min ago (cooldown)"
    for conv in list(state.conversations.values()):
        until = parse_dt(conv.wait_until)
        if conv.party_id == recipient and conv.status == "waiting" and until and until > now:
            return f"conversation {conv.conversation_id} is waiting until {conv.wait_until}"
    return None


def _rank(bundle: ContextBundle) -> tuple:
    """Unexpired before expired (never blocked: the judge's clock may not match the data's); then most urgent;
    then the one expiring soonest; then by id, so ties break the same way every time."""
    expires = parse_dt(bundle.trigger.get("expires_at")) or _FAR_FUTURE
    return (bundle.has("expired"), -int(bundle.trigger.get("urgency") or 1), expires, bundle.trigger_id)


def plan_tick(store: ContextStore, state: RuntimeState | None, trigger_ids: list[Any], *,
              now: Any = None, limit: int = MAX_ACTIONS) -> TickPlan:
    """Which of the judge's available_triggers to act on right now."""
    now_dt, _ = resolve_now(now)
    cooldown = _cooldown()
    plan = TickPlan(now=iso_z(now_dt))
    by_recipient: dict[str, list[ContextBundle]] = {}
    for trigger_id in dict.fromkeys(t for t in trigger_ids if isinstance(t, str)):
        bundle = build_bundle(store, trigger_id, now=now_dt, state=state)
        if bundle is None:
            plan.skipped.append({"trigger_id": trigger_id, "reason": "unknown trigger (never pushed)"})
            continue
        reason = _skip_reason(bundle, state, now_dt, cooldown)
        if reason:
            plan.skipped.append({"trigger_id": trigger_id, "reason": reason})
            continue
        by_recipient.setdefault(recipient_of(bundle), []).append(bundle)

    winners = []
    for recipient, bundles in by_recipient.items():
        bundles.sort(key=_rank)
        winners.append(bundles[0])
        plan.skipped += [{"trigger_id": b.trigger_id, "reason": f"{bundles[0].trigger_id} ranked higher for {recipient}"}
                         for b in bundles[1:]]
    winners.sort(key=_rank)
    limit = max(0, min(limit, MAX_ACTIONS))
    plan.chosen = winners[:limit]
    plan.skipped += [{"trigger_id": b.trigger_id, "reason": f"over the {limit}-action limit for one tick"}
                     for b in winners[limit:]]
    return plan


def new_conversation_id(state: RuntimeState | None, bundle: ContextBundle) -> str:
    """Readable and unique, e.g. conv_c_001_priya_for_m001_recall_due (the judge rejects reused ids)."""
    base = f"conv_{recipient_of(bundle) or 'unknown'}_{bundle.trigger['kind']}"
    if state is None or state.conversation(base) is None:
        return base
    n = 2
    while state.conversation(f"{base}_{n}"):
        n += 1
    return f"{base}_{n}"
