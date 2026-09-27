"""Compose messages: the brief's offline compose() and the live tick path.

Each trigger gets a fact sheet (phase 2) and a plain draft (templates.render). The AI
writer (phase 3) rewrites the draft; if it's off, slow, fails or breaks a check, the
plain draft goes out instead.
"""

from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path

from .bundle import ContextBundle, build_bundle
from .factsheet import FactSheet, build_fact_sheet
from .state import RuntimeState
from .store import ContextStore
from .templates import render
from .writer import default_cache_file, write_ai

# The briefs' simulated "now". compose() must be deterministic (challenge-brief §7.1), so it
# never reads the clock; VERA_REFERENCE_NOW still overrides it (see bundle.resolve_now).
DEFAULT_REFERENCE_NOW = "2026-04-26T10:30:00Z"
CONTRACT_KEYS = ("body", "cta", "send_as", "suppression_key", "rationale")


def _draft(sheet: FactSheet) -> dict:
    return {**render(sheet), "writer": "template"}


def compose_bundle(bundle: ContextBundle, *, state: RuntimeState | None = None, use_ai: bool = True,
                   cache_file: Path | str | None = None) -> tuple[dict, FactSheet]:
    """One message for one bundle: the AI rewrite when it passes the validator (after at most one retry),
    else the plain draft. No deadline here, so offline compose() always gets the same answer from the cache."""
    sheet = build_fact_sheet(bundle, state=state)
    draft = _draft(sheet)
    if use_ai:
        message, _reason = write_ai(sheet, draft, cache_file=cache_file)
        if message:
            return message, sheet
    return draft, sheet


def tick_deadline() -> float:
    """Seconds the tick waits for AI rewrites (VERA_TICK_DEADLINE); the judge allows 10-30."""
    try:
        return float(os.getenv("VERA_TICK_DEADLINE", "8"))
    except ValueError:
        return 8.0


async def compose_many(bundles: list[ContextBundle], *, state: RuntimeState | None = None,
                       deadline: float | None = None) -> list[tuple[dict, FactSheet]]:
    """Write every chosen trigger's message in parallel. Anything not back by the deadline goes out as
    its plain draft; the late call still finishes in the background and is cached for next time. A
    retry (phase 4) only starts if it can finish before the deadline."""
    sheets = [build_fact_sheet(b, state=state) for b in bundles]
    drafts = [_draft(s) for s in sheets]
    if not sheets:
        return []
    limit = tick_deadline() if deadline is None else deadline
    ends = time.monotonic() + limit
    tasks = [asyncio.ensure_future(asyncio.to_thread(write_ai, s, d, deadline=ends)) for s, d in zip(sheets, drafts)]
    done, _late = await asyncio.wait(tasks, timeout=limit)
    results = []
    for task, sheet, draft in zip(tasks, sheets, drafts):
        message = task.result()[0] if task in done and task.exception() is None else None
        results.append((message or draft, sheet))
    return results


def store_from_dicts(category: dict, merchant: dict, trigger: dict,
                     customer: dict | None = None) -> tuple[ContextStore, str]:
    """A throwaway store holding just these dataset dicts, and the trigger's context id."""
    trigger = {**trigger, "merchant_id": trigger.get("merchant_id") or merchant.get("merchant_id")}
    if customer and not trigger.get("customer_id"):
        trigger["customer_id"] = customer.get("customer_id")
    trigger_id = trigger.get("id") or "trg_input"
    pushes = [("category", category.get("slug") or merchant.get("category_slug") or "category", category),
              ("merchant", merchant.get("merchant_id") or "merchant", merchant),
              ("trigger", trigger_id, trigger)]
    if customer:
        pushes.append(("customer", customer.get("customer_id") or "customer", customer))

    store = ContextStore()
    for scope, context_id, payload in pushes:
        status, body = store.ingest({"scope": scope, "context_id": context_id, "version": 1, "payload": payload})
        if status != 200:
            raise ValueError(f"{scope} context rejected: {body}")
    return store, trigger_id


def bundle_from_dicts(category: dict, merchant: dict, trigger: dict, customer: dict | None = None, *,
                      now: str | None = None) -> ContextBundle:
    """The phase 1 briefing for raw dataset dicts, built exactly as compose() builds it."""
    store, trigger_id = store_from_dicts(category, merchant, trigger, customer)
    return build_bundle(store, trigger_id, now=now or DEFAULT_REFERENCE_NOW)


def compose(category: dict, merchant: dict, trigger: dict, customer: dict | None = None, *,
            now: str | None = None) -> dict:
    """challenge-brief §7.1: dataset dicts in, {body, cta, send_as, suppression_key, rationale} out."""
    # Saved results make repeat calls identical even though model output can vary between calls.
    message, _ = compose_bundle(bundle_from_dicts(category, merchant, trigger, customer, now=now),
                                cache_file=default_cache_file())
    return {key: message[key] for key in CONTRACT_KEYS}
