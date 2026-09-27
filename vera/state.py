"""Runtime state the bot writes itself: conversations, send ledgers and per-party flags.

Kept apart from ContextStore on purpose: the store holds what the judge told us,
this holds what we did and what we saw happen.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any

from .normalize import fingerprint, iso_z, parse_dt

SESSION_WINDOW_SECONDS = 24 * 3600  # WhatsApp: free-form allowed within 24h of the party's last reply


@dataclass
class Turn:
    ts: str
    sender: str                         # "bot", "merchant" or "customer"
    body: str
    turn_number: int | None = None
    meta: dict = field(default_factory=dict)


@dataclass
class Conversation:
    conversation_id: str
    merchant_id: str | None
    customer_id: str | None = None
    trigger_id: str | None = None
    send_as: str | None = None
    opened_by: str = "bot"              # "judge" when the first thing we saw was an inbound reply
    opened_at: str = ""
    status: str = "open"                # open | waiting | ended
    wait_until: str | None = None
    ended_reason: str | None = None
    turns: list[Turn] = field(default_factory=list)

    @property
    def party_id(self) -> str | None:
        return self.customer_id or self.merchant_id

    def bot_bodies(self) -> list[str]:
        return [t.body for t in self.turns if t.sender == "bot"]


@dataclass
class PartyState:
    """A merchant or customer we talk to, keyed by merchant_id / customer_id."""

    party_id: str
    role: str                                   # "merchant" or "customer"
    opted_out: bool = False
    opted_out_reason: str | None = None
    last_inbound_at: str | None = None          # last real reply; opens the 24h free-form window
    last_outbound_at: str | None = None
    unanswered_outbound: int = 0                # bot sends since the last real reply
    auto_replies: int = 0                       # canned/bot replies seen from this party
    inbound_fingerprints: dict[str, int] = field(default_factory=dict)  # repeated text = auto-reply
    sent_fingerprints: set[str] = field(default_factory=set)            # repetition across conversations


def _ts(now: Any) -> str:
    dt = parse_dt(now)
    return iso_z(dt) if dt else iso_z()


class RuntimeState:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.conversations: dict[str, Conversation] = {}
        self.parties: dict[str, PartyState] = {}
        self.suppression: dict[str, str] = {}   # suppression_key -> when it was used
        self.last_tick_now: str | None = None
        self.last_tick_triggers: list[str] = []

    def wipe(self) -> None:
        with self._lock:
            self.conversations.clear()
            self.parties.clear()
            self.suppression.clear()
            self.last_tick_now = None
            self.last_tick_triggers = []

    # --- lookups -------------------------------------------------------------

    def conversation(self, conversation_id: str) -> Conversation | None:
        return self.conversations.get(conversation_id)

    def party(self, party_id: str, role: str = "merchant") -> PartyState:
        with self._lock:
            state = self.parties.get(party_id)
            if state is None:
                state = self.parties[party_id] = PartyState(party_id=party_id, role=role)
            return state

    def turns_for_merchant(self, merchant_id: str) -> list[Turn]:
        """Chronological turns of merchant-facing conversations (customer chats excluded)."""
        turns = [t for c in list(self.conversations.values())
                 if c.merchant_id == merchant_id and c.customer_id is None for t in c.turns]
        return sorted(turns, key=lambda t: t.ts)

    # --- writes --------------------------------------------------------------

    def note_tick(self, now: Any, available_triggers: list[str]) -> None:
        with self._lock:
            self.last_tick_now = _ts(now)
            self.last_tick_triggers = [t for t in available_triggers if isinstance(t, str)]

    def _open(self, conversation_id: str, *, merchant_id: str | None, customer_id: str | None,
              trigger_id: str | None, send_as: str | None, opened_by: str, ts: str) -> Conversation:
        conv = Conversation(conversation_id=conversation_id, merchant_id=merchant_id,
                            customer_id=customer_id, trigger_id=trigger_id, send_as=send_as,
                            opened_by=opened_by, opened_at=ts)
        self.conversations[conversation_id] = conv
        return conv

    def open_conversation(self, conversation_id: str, *, merchant_id: str | None, customer_id: str | None = None,
                          trigger_id: str | None = None, send_as: str | None = None, now: Any = None) -> Conversation:
        with self._lock:
            return self.conversations.get(conversation_id) or self._open(
                conversation_id, merchant_id=merchant_id, customer_id=customer_id, trigger_id=trigger_id,
                send_as=send_as, opened_by="bot", ts=_ts(now))

    def record_outbound(self, conversation_id: str, body: str, *, now: Any = None,
                        merchant_id: str | None = None, customer_id: str | None = None,
                        trigger_id: str | None = None, send_as: str | None = None,
                        suppression_key: str | None = None, meta: dict | None = None) -> Conversation:
        ts = _ts(now)
        with self._lock:
            conv = self.conversations.get(conversation_id) or self._open(
                conversation_id, merchant_id=merchant_id, customer_id=customer_id,
                trigger_id=trigger_id, send_as=send_as, opened_by="bot", ts=ts)
            conv.turns.append(Turn(ts=ts, sender="bot", body=body, meta=dict(meta or {})))
            if conv.status == "waiting":
                conv.status, conv.wait_until = "open", None
            if conv.party_id:
                party = self.party(conv.party_id, "customer" if conv.customer_id else "merchant")
                party.last_outbound_at = ts
                party.unanswered_outbound += 1
                party.sent_fingerprints.add(fingerprint(body))
            if suppression_key:
                self.suppression.setdefault(suppression_key, ts)
            return conv

    def record_inbound(self, conversation_id: str, message: str, *, from_role: str = "merchant",
                       now: Any = None, merchant_id: str | None = None, customer_id: str | None = None,
                       turn_number: int | None = None) -> tuple[Conversation, int]:
        """Log an inbound message. Returns the conversation and how many times this party
        has now sent this exact text.

        The count is kept per party, not per conversation: the local simulator's
        auto-reply check opens a new conversation_id every turn. This does not count as
        a reply for the 24h window; call mark_replied() once it's known to be a real reply
        and not an auto-reply.
        """
        ts = _ts(now)
        with self._lock:
            conv = self.conversations.get(conversation_id) or self._open(
                conversation_id, merchant_id=merchant_id, customer_id=customer_id,
                trigger_id=None, send_as=None, opened_by="judge", ts=ts)
            conv.merchant_id = conv.merchant_id or merchant_id
            conv.customer_id = conv.customer_id or customer_id
            conv.turns.append(Turn(ts=ts, sender=from_role, body=message, turn_number=turn_number))
            party_id = (conv.customer_id if from_role == "customer" else conv.merchant_id)
            if not party_id:
                return conv, 1
            party = self.party(party_id, from_role)
            key = fingerprint(message)
            party.inbound_fingerprints[key] = party.inbound_fingerprints.get(key, 0) + 1
            return conv, party.inbound_fingerprints[key]

    def mark_replied(self, party_id: str, *, now: Any = None, role: str = "merchant") -> None:
        with self._lock:
            party = self.party(party_id, role)
            party.last_inbound_at = _ts(now)
            party.unanswered_outbound = 0
            party.auto_replies = 0      # a person answered; their bot's count starts over

    def set_waiting(self, conversation_id: str, *, until: Any) -> None:
        with self._lock:
            conv = self.conversations.get(conversation_id)
            if conv and conv.status != "ended":
                conv.status, conv.wait_until = "waiting", _ts(until)

    def end_conversation(self, conversation_id: str, *, reason: str) -> None:
        with self._lock:
            conv = self.conversations.get(conversation_id)
            if conv:
                conv.status, conv.ended_reason, conv.wait_until = "ended", reason, None

    def mark_opted_out(self, party_id: str, *, reason: str, role: str = "merchant") -> None:
        with self._lock:
            party = self.party(party_id, role)
            party.opted_out, party.opted_out_reason = True, reason

    # --- checks --------------------------------------------------------------

    def is_opted_out(self, party_id: str) -> bool:
        party = self.parties.get(party_id)
        return bool(party and party.opted_out)

    def is_suppressed(self, suppression_key: str | None) -> bool:
        return bool(suppression_key) and suppression_key in self.suppression

    def already_sent(self, conversation_id: str, body: str) -> bool:
        """Same body already sent in this conversation (the judge's -2 anti-repetition rule)."""
        conv = self.conversations.get(conversation_id)
        key = fingerprint(body)
        return bool(conv) and any(fingerprint(b) == key for b in conv.bot_bodies())

    def sent_to_party_before(self, party_id: str, body: str) -> bool:
        party = self.parties.get(party_id)
        return bool(party) and fingerprint(body) in party.sent_fingerprints

    def session_window_open(self, party_id: str, now: Any) -> bool:
        party = self.parties.get(party_id)
        last, current = parse_dt(party.last_inbound_at) if party else None, parse_dt(now)
        if last is None or current is None:
            return False
        return 0 <= (current - last).total_seconds() <= SESSION_WINDOW_SECONDS

    def summary(self) -> dict:
        statuses = [c.status for c in list(self.conversations.values())]
        return {"conversations": len(statuses),
                "by_status": {s: statuses.count(s) for s in ("open", "waiting", "ended")},
                "parties": len(self.parties),
                "opted_out": sum(1 for p in list(self.parties.values()) if p.opted_out),
                "suppression_keys": len(self.suppression)}
