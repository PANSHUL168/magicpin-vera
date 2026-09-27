"""Everything the fact-sheet phase needs for one trigger, joined and checked.

build_bundle() resolves references at read time (pushes can arrive in any order),
gathers entity-level facts and raises flags for problems later phases must handle:
placeholder payloads, consent gaps, state conflicts, expired triggers and so on.
"""

from __future__ import annotations

import copy
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from .derive import (Fact, category_facts, customer_facts, history_summary, language_profile,
                     merchant_facts, richness)
from .normalize import check_slot_label, humanize, humanize_payload, iso_z, parse_dt, parse_person_name
from .state import RuntimeState
from .store import ContextRecord, ContextStore

# Payload keys that point at category digest items. The seeds use all three singular forms.
DIGEST_REF_KEYS = ("top_item_id", "alert_id", "digest_item_id", "item_id")
DIGEST_REF_LIST_KEYS = ("top_item_ids", "alert_ids", "digest_item_ids", "item_ids")

# Consent scopes that cover each customer-facing trigger kind. Unknown kinds aren't checked.
CONSENT_FOR_KIND = {
    "recall_due": {"recall_reminders", "appointment_reminders"},
    "appointment_tomorrow": {"appointment_reminders"},
    "chronic_refill_due": {"refill_reminders"},
    "customer_lapsed_soft": {"winback_offers", "promotional_offers", "recall_reminders"},
    "customer_lapsed_hard": {"winback_offers", "promotional_offers", "recall_reminders"},
    "trial_followup": {"program_updates", "kids_program_updates", "appointment_reminders", "promotional_offers"},
    "wedding_package_followup": {"bridal_package_followup", "appointment_reminders"},
}
# Trigger kinds that assert a customer state; the generated data sometimes disagrees.
STATE_FOR_KIND = {"customer_lapsed_soft": {"lapsed_soft"}, "customer_lapsed_hard": {"lapsed_hard", "churned"}}
# Payload dates that describe the past; one after `now` means the data's timeline is off.
PAST_DATE_KEYS = ("last_service_date", "last_refill", "trial_date", "trial_completed", "opened_date")
SLOT_LIST_KEYS = ("available_slots", "next_session_options")


def resolve_now(now: Any = None) -> tuple[datetime, str]:
    """Reference time and where it came from.

    VERA_REFERENCE_NOW overrides everything: the local simulator sends wall-clock
    time, which makes most seed triggers look expired.
    """
    override = parse_dt(os.getenv("VERA_REFERENCE_NOW"))
    if override:
        return override, "override"
    given = parse_dt(now)
    if given:
        return given, "given"
    return datetime.now(timezone.utc), "wall_clock"


@dataclass
class ContextBundle:
    trigger_id: str
    now: str
    now_source: str                 # "override", "given" or "wall_clock"
    audience: str                   # "merchant" or "customer"
    send_as: str                    # "vera" or "merchant_on_behalf"
    trigger: dict
    payload_display: dict           # trigger payload made readable: codes humanized, %, ₹, dates
    merchant: dict | None
    category: dict | None
    customer: dict | None
    digest_items: list[dict]        # [{"id", "ref_key", "category", "fresh", "item"}]
    facts: list[Fact]
    history: dict
    language: dict
    richness: dict
    consent: dict | None            # customer-facing only
    slots: list[dict]               # slot labels checked against their ISO dates
    fresh: dict                     # what changed since each context's first version
    flags: list[str]
    warnings: list[str]
    missing: list[str]

    def fact(self, key: str) -> Fact | None:
        return next((f for f in self.facts if f.key == key), None)

    def facts_in(self, group: str) -> list[Fact]:
        return [f for f in self.facts if f.group == group]

    def has(self, flag: str) -> bool:
        return flag in self.flags

    def to_dict(self) -> dict:
        return asdict(self)


def _resolve_digest(store: ContextStore, payload: dict,
                    category_rec: ContextRecord | None) -> tuple[list[dict], list[str]]:
    refs = [(key, payload[key]) for key in DIGEST_REF_KEYS if isinstance(payload.get(key), str)]
    for key in DIGEST_REF_LIST_KEYS:
        if isinstance(payload.get(key), list):
            refs += [(key, ref) for ref in payload[key] if isinstance(ref, str)]
    if not refs:
        return [], []
    # Merchant's own category first, then any other (an alert can live elsewhere).
    candidates = ([category_rec] if category_rec else []) + [
        r for r in store.records("category") if r is not category_rec]
    items, unresolved = [], []
    for key, ref in refs:
        hit = next(((rec, item) for rec in candidates for item in rec.data["digest"]
                    if isinstance(item, dict) and item.get("id") == ref), None)
        if hit is None:
            unresolved.append(ref)
            continue
        rec, item = hit
        first_seen = rec.item_first_seen.get("digest", {}).get(f"id:{ref}")
        items.append({"id": ref, "ref_key": key, "category": rec.context_id,
                      "fresh": bool(first_seen and first_seen > rec.first_version),
                      "item": copy.deepcopy(item)})
    return items, unresolved


def _consent(trigger: dict, customer: dict | None) -> dict:
    empty = {"checked": False, "scopes": [], "accepted": None, "matched": []}
    if customer is None:
        return {**empty, "ok": False, "reason": "customer context not loaded"}
    scopes = [s for s in customer["consent"]["scope"] if isinstance(s, str)]
    accepted = CONSENT_FOR_KIND.get(trigger["kind"])
    if not scopes:
        return {**empty, "ok": False, "checked": True, "reason": "customer has no messaging consent on file"}
    if accepted is None:
        return {**empty, "ok": True, "scopes": scopes,
                "reason": f"no consent rule for {trigger['kind']}; customer consented to {', '.join(scopes)}"}
    matched = sorted(accepted & set(scopes))
    reason = (f"covered by consent: {', '.join(matched)}" if matched else
              f"{trigger['kind']} needs one of {', '.join(sorted(accepted))}; "
              f"customer consented only to {', '.join(scopes)}")
    return {"ok": bool(matched), "checked": True, "scopes": scopes, "accepted": sorted(accepted),
            "matched": matched, "reason": reason}


def _freshness(records: dict[str, ContextRecord | None]) -> dict:
    fresh: dict[str, Any] = {}
    for label, rec in records.items():
        if rec and rec.is_update and rec.changes_since_base:
            fresh[label] = {"version": rec.version, "first_version": rec.first_version,
                            "changes": rec.changes_since_base}
    category = records.get("category")
    if category:
        current = {f"id:{d.get('id')}" for d in category.data["digest"] if isinstance(d, dict)}
        new = [identity[3:] for identity, version in category.item_first_seen.get("digest", {}).items()
               if version > category.first_version and identity in current]
        if new:
            fresh["new_digest_items"] = new
    return fresh


def _customer_flags(flag: Callable[[str, str], None], trigger: dict, customer: dict | None,
                    consent: dict | None, merchant_id: str | None) -> None:
    if not trigger.get("customer_id"):
        flag("scope_mismatch", "customer-scope trigger has no customer_id")
        return
    if customer is None:
        return  # already reported as missing
    if customer.get("merchant_id") and merchant_id and customer["merchant_id"] != merchant_id:
        flag("scope_mismatch", f"customer belongs to {customer['merchant_id']}, trigger names {merchant_id}")
    if consent and not consent["ok"]:
        flag("consent_gap", consent["reason"])
    if customer["preferences"].get("reminder_opt_in") is False:
        flag("reminders_opted_out", "customer has not opted in to reminders")
    expected = STATE_FOR_KIND.get(trigger["kind"])
    if expected and customer.get("state") not in expected:
        flag("state_conflict", f"trigger says {humanize(trigger['kind'])} but customer state is {customer.get('state')}")
    if parse_person_name(customer["identity"].get("name"))["anonymous"]:
        flag("customer_anonymous", "no customer name on file")


def build_bundle(store: ContextStore, trigger_id: str, *, now: Any = None,
                 state: RuntimeState | None = None) -> ContextBundle | None:
    """Join and check everything for one trigger. None if the trigger isn't stored."""
    trigger_rec = store.get("trigger", trigger_id)
    if trigger_rec is None:
        return None
    now_dt, now_source = resolve_now(now)
    trigger = copy.deepcopy(trigger_rec.data)
    payload = trigger["payload"]
    flags: list[str] = []
    warnings: list[str] = []
    missing: list[str] = []

    def flag(name: str, why: str) -> None:
        if name not in flags:
            flags.append(name)
        warnings.append(f"{name}: {why}")

    # --- resolve references (customer first: it can supply the merchant id) ---
    customer_id = trigger.get("customer_id")
    customer_rec = store.get("customer", customer_id) if customer_id else None
    if customer_id and customer_rec is None:
        missing.append(f"customer:{customer_id}")
    merchant_id = trigger.get("merchant_id") or (customer_rec.data.get("merchant_id") if customer_rec else None)
    merchant_rec = store.get("merchant", merchant_id) if merchant_id else None
    if not merchant_id:
        missing.append("merchant:(trigger names none)")
    elif merchant_rec is None:
        missing.append(f"merchant:{merchant_id}")
    slug = (merchant_rec.data.get("category_slug") if merchant_rec else None) or payload.get("category")
    category_rec = store.get("category", slug) if isinstance(slug, str) else None
    if isinstance(slug, str) and category_rec is None:
        missing.append(f"category:{slug}")

    merchant = copy.deepcopy(merchant_rec.data) if merchant_rec else None
    category = copy.deepcopy(category_rec.data) if category_rec else None
    customer = copy.deepcopy(customer_rec.data) if customer_rec else None
    digest_items, unresolved = _resolve_digest(store, payload, category_rec)
    missing += [f"digest:{ref}" for ref in unresolved]

    # --- facts and summaries ---
    audience = "customer" if trigger["scope"] == "customer" else "merchant"
    facts: list[Fact] = []
    if merchant:
        facts += merchant_facts(merchant, category)
    if category:
        facts += category_facts(category, merchant, now_dt)
    if customer:
        facts += customer_facts(customer, now_dt)
    live_turns = state.turns_for_merchant(merchant_id) if state and merchant_id else []
    history = history_summary(merchant, live_turns, now_dt)
    language = language_profile(merchant, category, customer, audience)
    rich = richness(merchant) if merchant else {"level": "unknown", "score": 0, "max": 5,
                                                "present": [], "missing": []}
    consent = _consent(trigger, customer) if audience == "customer" else None
    slots = [checked for key in SLOT_LIST_KEYS if isinstance(payload.get(key), list)
             for checked in (check_slot_label(s) for s in payload[key]) if checked]

    # --- flags ---
    if payload.get("placeholder"):
        flag("placeholder_payload", "trigger payload has no event details; anchor on merchant and "
                                    "category facts and invent nothing about the event")
    expires = parse_dt(trigger.get("expires_at"))
    if expires and expires <= now_dt:
        flag("expired", f"expired {trigger['expires_at']} (now {iso_z(now_dt)})")
    if missing:
        flag("incomplete", "missing " + ", ".join(missing))
    status = str((merchant or {}).get("subscription", {}).get("status") or "").lower()
    if merchant and status and status != "active":
        flag("merchant_not_active", f"subscription is {status}"
             + ("; this message goes out on their behalf" if audience == "customer" else ""))
    relevance = payload.get("category_relevance")
    if isinstance(relevance, list) and slug and slug not in relevance:
        flag("category_not_relevant", f"payload targets {', '.join(map(str, relevance))}; merchant is {slug}")
    if audience == "customer":
        _customer_flags(flag, trigger, customer, consent, merchant_id)
    for key in PAST_DATE_KEYS:
        when = parse_dt(payload.get(key))
        if when and when > now_dt:
            flag("time_inconsistent", f"payload.{key} {payload[key]} is after now")
    last_visit = parse_dt((customer or {}).get("relationship", {}).get("last_visit"))
    if last_visit and last_visit > now_dt:
        flag("time_inconsistent", f"customer last_visit {customer['relationship']['last_visit']} is after now")
    if any(not s["weekday_ok"] for s in slots):
        flag("slot_weekday_mismatch", "slot labels name the wrong weekday for their dates; use safe_label")
    if rich["level"] == "sparse":
        flag("sparse_merchant", "no offers, history, signals or review themes; "
                                "anchor on performance, peers and category facts")
    if audience == "merchant" and history["open_requests"]:
        flag("open_merchant_request", "merchant is waiting on: "
             + " | ".join(r["message"] for r in history["open_requests"]))
    if state:
        party = customer_id if audience == "customer" else merchant_id
        if party and state.is_opted_out(party):
            flag("opted_out", f"{party} asked us to stop")
        if state.is_suppressed(trigger["suppression_key"]):
            flag("suppression_key_used", f"already sent for {trigger['suppression_key']}")

    return ContextBundle(
        trigger_id=trigger_rec.context_id,
        now=iso_z(now_dt),
        now_source=now_source,
        audience=audience,
        send_as="merchant_on_behalf" if audience == "customer" else "vera",
        trigger=trigger,
        payload_display=humanize_payload(payload),
        merchant=merchant,
        category=category,
        customer=customer,
        digest_items=digest_items,
        facts=facts,
        history=history,
        language=language,
        richness=rich,
        consent=consent,
        slots=slots,
        fresh=_freshness({"trigger": trigger_rec, "merchant": merchant_rec,
                          "category": category_rec, "customer": customer_rec}),
        flags=flags,
        warnings=warnings,
        missing=missing,
    )
