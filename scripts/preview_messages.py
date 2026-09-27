#!/usr/bin/env python3
"""Print writing briefs (phase 2) and the plain messages rendered from them, for reading.

Usage:
    python3 scripts/preview_messages.py                  # the 30 canonical test pairs
    python3 scripts/preview_messages.py --brief          # ...with each full writing brief
    python3 scripts/preview_messages.py --trigger trg_014_seasonal_acquisition_dip_powerhouse --brief
    python3 scripts/preview_messages.py --all            # every trigger in the dataset
    python3 scripts/preview_messages.py --ai             # also the AI rewrite (uses the API, results saved)
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from vera import llm  # noqa: E402
from vera.bundle import build_bundle  # noqa: E402
from vera.compose import DEFAULT_REFERENCE_NOW, compose_bundle  # noqa: E402
from vera.loader import load_dataset, load_test_pairs  # noqa: E402
from vera.store import ContextStore  # noqa: E402
from vera.writer import default_cache_file, write_ai  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview phase 2 briefs and plain messages.")
    parser.add_argument("--dataset", default=str(ROOT / "dataset" / "expanded"))
    parser.add_argument("--now", default=DEFAULT_REFERENCE_NOW)
    parser.add_argument("--trigger", help="only this trigger id")
    parser.add_argument("--all", action="store_true", help="every trigger, not just the 30 test pairs")
    parser.add_argument("--brief", action="store_true", help="also print the full writing brief")
    parser.add_argument("--ai", action="store_true", help="also show the AI rewrite (calls the API)")
    args = parser.parse_args()
    os.environ.setdefault("VERA_LLM_TIMEOUT", "30")

    store = ContextStore()
    load_dataset(store, args.dataset)
    if args.trigger:
        rows = [("-", args.trigger)]
    elif args.all:
        rows = [("-", r.context_id) for r in sorted(store.records("trigger"), key=lambda r: r.context_id)]
    else:
        rows = [(p["test_id"], p["trigger_id"]) for p in load_test_pairs(args.dataset)]

    for label, trigger_id in rows:
        bundle = build_bundle(store, trigger_id, now=args.now)
        if bundle is None:
            print(f"unknown trigger {trigger_id}", file=sys.stderr)
            return 2
        message, sheet = compose_bundle(bundle, use_ai=False)
        to = sheet.address_as or sheet.recipient_id
        print(f"=== {label} {sheet.kind} [{sheet.family}] -> {to} ({sheet.sender_name}), "
              f"send_as={sheet.send_as}, cta={message['cta']}")
        if sheet.flags:
            print(f"    flags: {', '.join(sheet.flags)}")
        print(f"    {'PLAIN: ' if args.ai else ''}{message['body']}")
        if args.ai:
            ai, reason = write_ai(sheet, message, cache_file=default_cache_file())
            print(f"    AI:    {ai['body']}" if ai else f"    AI:    (kept the plain draft: {reason})")
        if args.brief:
            print("    --- brief ---")
            print("\n".join(f"    {line}" for line in sheet.to_prompt().splitlines()))
            print(f"    --- rationale ---\n    {message['rationale']}")
        print()
    if args.ai:
        print(f"API usage this run: {dict(llm.USAGE) or 'none (all answers came from the saved results)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
