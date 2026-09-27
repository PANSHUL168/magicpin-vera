#!/usr/bin/env python3
"""Build a ContextBundle for every trigger in a dataset and report problems.

Usage:
    python3 scripts/audit_contexts.py                                  # dataset/expanded at the brief's "now"
    python3 scripts/audit_contexts.py --now 2026-09-26T12:00:00Z       # see what wall-clock time does
    python3 scripts/audit_contexts.py --trigger trg_003_recall_due_priya   # dump one bundle as JSON

Exits 1 if any bundle fails to build or has unresolved references.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from vera.bundle import build_bundle  # noqa: E402
from vera.loader import load_dataset, load_test_pairs  # noqa: E402
from vera.store import ContextStore  # noqa: E402

BRIEF_NOW = "2026-04-26T10:30:00Z"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit context bundles for every trigger.")
    parser.add_argument("--dataset", default=str(ROOT / "dataset" / "expanded"))
    parser.add_argument("--now", default=BRIEF_NOW, help=f"reference time (default {BRIEF_NOW})")
    parser.add_argument("--trigger", help="print this trigger's bundle as JSON and exit")
    args = parser.parse_args()

    dataset = Path(args.dataset)
    if not dataset.exists():
        print(f"{dataset} not found. Generate it with:\n"
              "  python3 dataset/generate_dataset.py --seed-dir dataset --out dataset/expanded", file=sys.stderr)
        return 2
    store = ContextStore()
    report = load_dataset(store, dataset)
    print(f"Loaded {report['layout']} dataset: {report['accepted']}")
    for rejection in report["rejected"]:
        print(f"  rejected: {rejection}")

    if args.trigger:
        bundle = build_bundle(store, args.trigger, now=args.now)
        if bundle is None:
            print(f"unknown trigger {args.trigger}", file=sys.stderr)
            return 2
        print(json.dumps(bundle.to_dict(), indent=2, ensure_ascii=False, default=str))
        return 0

    bundles, failures, flag_counts = {}, [], Counter()
    started = time.perf_counter()
    for record in sorted(store.records("trigger"), key=lambda r: r.context_id):
        try:
            bundle = build_bundle(store, record.context_id, now=args.now)
        except Exception as exc:  # the audit exists to surface these
            failures.append(f"{record.context_id}: {exc!r}")
            continue
        bundles[record.context_id] = bundle
        flag_counts.update(bundle.flags)
        if bundle.missing:
            failures.append(f"{record.context_id}: missing {bundle.missing}")
    elapsed_ms = (time.perf_counter() - started) * 1000
    print(f"Built {len(bundles)} bundles in {elapsed_ms:.0f} ms (now={args.now})\n")

    print("Flags across all triggers:")
    for name, count in flag_counts.most_common():
        print(f"  {name:<24} {count}")

    pairs = load_test_pairs(dataset)
    if pairs:
        print(f"\nCanonical test pairs ({len(pairs)}):")
        for pair in pairs:
            bundle = bundles.get(pair["trigger_id"])
            if bundle:
                flags = ", ".join(bundle.flags) or "-"
                print(f"  {pair['test_id']}  {bundle.trigger['kind']:<25} {bundle.audience:<8} "
                      f"{bundle.richness['level']:<8} {flags}")

    if failures:
        print("\nFAILURES:")
        for failure in failures:
            print(f"  {failure}")
        return 1
    print("\nNo build errors, no unresolved references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
