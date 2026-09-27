#!/usr/bin/env python3
"""Write submission.jsonl: one compose() result per canonical test pair (challenge-brief §7.2).

Goes through bot.compose(), the same function the judge can call, reading each pair's
category, merchant, trigger and (if any) customer straight from the expanded dataset.
The AI writer is used when OPENAI_API_KEY is set; results are saved in .cache/, so a rerun
of unchanged briefs spends no tokens.

Usage:
    python3 scripts/write_submission.py                      # -> submission.jsonl
    python3 scripts/write_submission.py --plain              # plain writer only, no API calls
    python3 scripts/write_submission.py --out /tmp/check.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from vera import llm, writer  # noqa: E402
from vera.compose import compose  # noqa: E402
from vera.loader import load_test_pairs  # noqa: E402


def _read(path: Path) -> dict:
    with open(path, encoding="utf-8") as fp:
        return json.load(fp)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write submission.jsonl from the 30 test pairs.")
    parser.add_argument("--dataset", default=str(ROOT / "dataset" / "expanded"))
    parser.add_argument("--out", default=str(ROOT / "submission.jsonl"))
    parser.add_argument("--plain", action="store_true", help="don't call the AI writer")
    args = parser.parse_args()
    if args.plain:
        os.environ["VERA_LLM"] = "off"
    os.environ.setdefault("VERA_LLM_TIMEOUT", "30")  # offline: no tick deadline to meet

    dataset = Path(args.dataset)
    pairs = load_test_pairs(dataset)
    if not pairs:
        print(f"No test_pairs.json in {dataset}. Generate the dataset with:\n"
              "  python3 dataset/generate_dataset.py --seed-dir dataset --out dataset/expanded", file=sys.stderr)
        return 2

    lines, ctas = [], Counter()
    for pair in pairs:
        trigger = _read(dataset / "triggers" / f"{pair['trigger_id']}.json")
        merchant = _read(dataset / "merchants" / f"{pair['merchant_id']}.json")
        category = _read(dataset / "categories" / f"{merchant['category_slug']}.json")
        customer_id = pair.get("customer_id")
        customer = _read(dataset / "customers" / f"{customer_id}.json") if customer_id else None
        result = compose(category, merchant, trigger, customer)
        lines.append({"test_id": pair["test_id"], **result})
        ctas[result["cta"]] += 1

    out = Path(args.out)
    out.write_text("".join(json.dumps(line, ensure_ascii=False) + "\n" for line in lines), encoding="utf-8")
    lengths = [len(line["body"]) for line in lines]
    print(f"Wrote {len(lines)} lines to {out}")
    print(f"Body length: min {min(lengths)}, avg {sum(lengths) // len(lengths)}, max {max(lengths)} characters")
    print(f"CTAs: {dict(ctas)}")
    print(f"Writer: {dict(writer.STATS) or 'plain only'}")
    if llm.USAGE:
        print(f"API usage this run: {dict(llm.USAGE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
