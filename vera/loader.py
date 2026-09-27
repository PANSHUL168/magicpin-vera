"""Read dataset files and feed them through the same ingest path as /v1/context.

Handles both layouts: the shipped seeds (dataset/*_seed.json) and the per-file
dataset written by dataset/generate_dataset.py. Offline tools (audit, submission
writer) use this; the live server never preloads, or the judge's warmup pushes
would come back 409.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from .normalize import iso_z
from .store import SCOPES, ContextStore

_EXPANDED = (("merchant", "merchants", "merchant_id"), ("customer", "customers", "customer_id"),
             ("trigger", "triggers", "id"))
_SEEDS = (("merchant", "merchants_seed.json", "merchants", "merchant_id"),
          ("customer", "customers_seed.json", "customers", "customer_id"),
          ("trigger", "triggers_seed.json", "triggers", "id"))


def _read(path: Path) -> Any:
    with open(path, encoding="utf-8") as fp:
        return json.load(fp)


def dataset_layout(root: str | Path) -> str:
    return "expanded" if (Path(root) / "merchants").is_dir() else "seeds"


def iter_dataset(root: str | Path, *, scopes: tuple[str, ...] = SCOPES) -> Iterator[tuple[str, str, dict]]:
    """Yield (scope, context_id, payload) in warmup order: categories, merchants, customers, triggers."""
    root = Path(root)
    if "category" in scopes:
        for path in sorted((root / "categories").glob("*.json")):
            data = _read(path)
            yield "category", data.get("slug", path.stem), data
    if dataset_layout(root) == "expanded":
        for scope, folder, id_key in _EXPANDED:
            if scope in scopes:
                for path in sorted((root / folder).glob("*.json")):
                    data = _read(path)
                    yield scope, data.get(id_key, path.stem), data
    else:
        for scope, filename, container, id_key in _SEEDS:
            if scope in scopes and (root / filename).exists():
                for item in _read(root / filename).get(container, []):
                    if isinstance(item, dict) and item.get(id_key):
                        yield scope, item[id_key], item


def load_dataset(store: ContextStore, root: str | Path, *, version: int = 1,
                 scopes: tuple[str, ...] = SCOPES) -> dict:
    """Ingest every context under root. Returns counts per scope and any rejections."""
    accepted: Counter[str] = Counter()
    rejected = []
    delivered_at = iso_z()
    for scope, context_id, payload in iter_dataset(root, scopes=scopes):
        status, body = store.ingest({"scope": scope, "context_id": context_id, "version": version,
                                     "payload": payload, "delivered_at": delivered_at})
        if status == 200:
            accepted[scope] += 1
        else:
            rejected.append({"scope": scope, "context_id": context_id, "status": status, "response": body})
    return {"layout": dataset_layout(root), "accepted": dict(accepted), "rejected": rejected}


def load_test_pairs(root: str | Path) -> list[dict]:
    """The 30 canonical (merchant, trigger) pairs; only the expanded dataset has them."""
    path = Path(root) / "test_pairs.json"
    return _read(path).get("pairs", []) if path.exists() else []
