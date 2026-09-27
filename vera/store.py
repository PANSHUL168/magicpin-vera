"""Versioned in-memory store for everything pushed to /v1/context.

Rules (challenge-testing-brief §2.1, api-call-examples 1.5 and 2.8):
- Keyed by (scope, context_id). A higher version replaces the stored one.
- The same or a lower version is refused with 409 stale_version.
- A new version that omits a top-level key keeps the previous value for it.
  Example 2.8 shows a partial category update; replacing outright would wipe the
  offer catalog and peer stats. Keys sent explicitly (even as [] or {}) replace.
"""

from __future__ import annotations

import copy
import json
import logging
import threading
from dataclasses import dataclass
from typing import Any

from .normalize import DECLARED_ID_FIELD, canonicalize, is_number, iso_z

log = logging.getLogger("vera.store")

SCOPES = ("category", "merchant", "customer", "trigger")

# List fields whose items get first-seen tracking, so later phases can tell
# "arrived after warmup" (worth mentioning) from "was always there".
TRACKED_LISTS = ("digest", "offer_catalog", "patient_content_library", "trend_signals",
                 "seasonal_beats", "offers", "conversation_history", "review_themes", "signals")
NUMERIC_SECTIONS = ("performance", "customer_aggregate", "peer_stats", "subscription")


def item_identity(item: Any) -> str:
    """Stable identity for a list item, used by diffs and first-seen tracking."""
    if isinstance(item, dict):
        for key in ("id", "title", "query", "month_range", "theme"):
            if item.get(key):
                return f"{key}:{item[key]}"
        if item.get("ts"):
            return f"turn:{item['ts']}:{item.get('from', '')}"
        return json.dumps(item, sort_keys=True, ensure_ascii=False, default=str)
    return str(item)


def _flatten_numbers(section: Any, prefix: str = "") -> dict[str, float]:
    out: dict[str, float] = {}
    if isinstance(section, dict):
        for key, value in section.items():
            if is_number(value):
                out[prefix + key] = value
            elif isinstance(value, dict):
                out.update(_flatten_numbers(value, f"{prefix}{key}."))
    return out


def diff_contexts(old: dict, new: dict) -> dict:
    """What changed between two normalized payloads of the same context."""
    changed = sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))
    if not changed:
        return {}
    changes: dict[str, Any] = {"changed_keys": changed}
    for key in changed:
        before, after = old.get(key), new.get(key)
        if key in TRACKED_LISTS and isinstance(after, list):
            before_list = before if isinstance(before, list) else []
            before_ids = {item_identity(i) for i in before_list}
            after_ids = [item_identity(i) for i in after]
            added = [i for i in after_ids if i not in before_ids]
            removed = sorted(before_ids - set(after_ids))
            if added or removed:
                changes.setdefault("lists", {})[key] = {"added": added, "removed": removed}
            if key == "offers":
                old_status = {item_identity(o): o.get("status") for o in before_list if isinstance(o, dict)}
                for offer in after:
                    identity = item_identity(offer)
                    if identity in old_status and old_status[identity] != offer.get("status"):
                        changes.setdefault("offer_status", {})[identity] = {
                            "from": old_status[identity], "to": offer.get("status")}
        elif key in NUMERIC_SECTIONS:
            b, a = _flatten_numbers(before), _flatten_numbers(after)
            numbers = {path: {"from": b.get(path), "to": a.get(path)}
                       for path in sorted(set(b) | set(a)) if b.get(path) != a.get(path)}
            if numbers:
                changes.setdefault("numbers", {})[key] = numbers
        elif not isinstance(before, (dict, list)) and not isinstance(after, (dict, list)):
            changes.setdefault("values", {})[key] = {"from": before, "to": after}
    return changes


@dataclass(frozen=True)
class ContextRecord:
    scope: str
    context_id: str
    version: int
    payload: dict                   # as stored: pushed payload plus any inherited top-level keys
    data: dict                      # canonical shape used downstream (normalize.canonicalize)
    delivered_at: str | None
    stored_at: str
    first_version: int              # first version this process saw for the context
    base_data: dict                 # data as of first_version, for "changed since warmup"
    changes: dict                   # vs the previous stored version
    changes_since_base: dict        # vs first_version
    inherited_keys: tuple[str, ...]
    item_first_seen: dict           # list name -> {item identity -> version it first appeared in}
    warnings: tuple[str, ...]

    @property
    def is_update(self) -> bool:
        return self.version != self.first_version


def _parse_version(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value >= 0 else None
    if isinstance(value, float) and value.is_integer() and value >= 0:
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def _validate(envelope: Any) -> tuple[str, str] | None:
    if not isinstance(envelope, dict):
        return "invalid_body", "request body must be a JSON object"
    if envelope.get("scope") not in SCOPES:
        return "invalid_scope", f"scope must be one of {', '.join(SCOPES)}; got {envelope.get('scope')!r}"
    context_id = envelope.get("context_id")
    if not isinstance(context_id, str) or not context_id.strip():
        return "invalid_context_id", "context_id must be a non-empty string"
    if _parse_version(envelope.get("version")) is None:
        return "invalid_version", f"version must be a non-negative integer; got {envelope.get('version')!r}"
    if not isinstance(envelope.get("payload"), dict):
        return "invalid_payload", "payload must be a JSON object"
    return None


def _build_record(scope: str, context_id: str, version: int, payload: dict,
                  delivered_at: Any, previous: ContextRecord | None) -> ContextRecord:
    merged = dict(payload)
    inherited = []
    if previous:
        for key, value in previous.payload.items():
            if key not in merged:
                merged[key] = value
                inherited.append(key)
    merged = copy.deepcopy(merged)
    data, warnings = canonicalize(scope, merged, context_id)

    first_seen = {name: dict(ids) for name, ids in previous.item_first_seen.items()} if previous else {}
    for name in TRACKED_LISTS:
        items = data.get(name)
        if isinstance(items, list):
            bucket = first_seen.setdefault(name, {})
            for item in items:
                bucket.setdefault(item_identity(item), version)

    base = previous.base_data if previous else data
    return ContextRecord(
        scope=scope,
        context_id=context_id,
        version=version,
        payload=merged,
        data=data,
        delivered_at=delivered_at if isinstance(delivered_at, str) else None,
        stored_at=iso_z(),
        first_version=previous.first_version if previous else version,
        base_data=base,
        changes=diff_contexts(previous.data, data) if previous else {},
        changes_since_base=diff_contexts(base, data) if previous else {},
        inherited_keys=tuple(inherited),
        item_first_seen=first_seen,
        warnings=tuple(warnings),
    )


class ContextStore:
    """Thread-safe store. Records are never mutated after creation; updates swap in a new one."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: dict[tuple[str, str], ContextRecord] = {}
        # payload-declared id -> context_id, for when the judge keys a context differently
        self._declared: dict[tuple[str, str], str] = {}

    def ingest(self, envelope: Any) -> tuple[int, dict]:
        """Validate and store one /v1/context envelope. Returns (http_status, response_body)."""
        problem = _validate(envelope)
        if problem:
            reason, details = problem
            return 400, {"accepted": False, "reason": reason, "details": details}
        scope = envelope["scope"]
        context_id = envelope["context_id"].strip()
        version = _parse_version(envelope["version"])
        with self._lock:
            previous = self._records.get((scope, context_id))
            if previous and version <= previous.version:
                return 409, {"accepted": False, "reason": "stale_version", "current_version": previous.version}
            record = _build_record(scope, context_id, version, envelope["payload"],
                                   envelope.get("delivered_at"), previous)
            self._records[(scope, context_id)] = record
            declared = record.data.get(DECLARED_ID_FIELD[scope])
            if isinstance(declared, str) and declared != context_id:
                self._declared[(scope, declared)] = context_id
        _log_ingest(record)
        return 200, {"accepted": True, "ack_id": f"ack_{context_id}_v{version}", "stored_at": record.stored_at}

    def get(self, scope: str, ref: Any) -> ContextRecord | None:
        """Look up by context_id, falling back to the id declared inside the payload."""
        if not isinstance(ref, str):
            return None
        record = self._records.get((scope, ref))
        if record is None and (scope, ref) in self._declared:
            record = self._records.get((scope, self._declared[(scope, ref)]))
        return record

    def data(self, scope: str, ref: Any) -> dict | None:
        record = self.get(scope, ref)
        return record.data if record else None

    def records(self, scope: str) -> list[ContextRecord]:
        return [record for (s, _), record in list(self._records.items()) if s == scope]

    def counts(self) -> dict[str, int]:
        counts = dict.fromkeys(SCOPES, 0)
        for scope, _ in list(self._records):
            counts[scope] += 1
        return counts

    def wipe(self) -> None:
        with self._lock:
            self._records.clear()
            self._declared.clear()


def _log_ingest(record: ContextRecord) -> None:
    label = f"{record.scope}/{record.context_id} v{record.version}"
    if not (record.is_update or record.warnings):
        log.debug("stored %s", label)
        return
    parts = [label]
    if record.inherited_keys:
        parts.append(f"kept from previous version: {list(record.inherited_keys)}")
    if record.changes:
        parts.append(f"changed: {record.changes.get('changed_keys')}")
    if record.warnings:
        parts.append(f"warnings: {list(record.warnings)}")
    log.info("stored %s", "; ".join(parts))
