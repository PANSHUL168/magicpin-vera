#!/usr/bin/env python3
"""Play the scripted reply scenarios (vera/harness.py) against the bot and write the transcripts.

Runs the FastAPI app in-process; no server needed. The AI is off unless --ai is given; first
messages then come from the saved AI cache where one exists, otherwise from the plain templates.
With --ai, the AI replies are saved to the same cache, so a re-run costs nothing.

Usage:
    .venv/bin/python scripts/simulate_conversations.py               # all scenarios, no API calls
    .venv/bin/python scripts/simulate_conversations.py intent_transition hostile_then_gst
    .venv/bin/python scripts/simulate_conversations.py --ai          # real AI replies (costs tokens)

Writes output/conversations/<scenario>.md and README.md. Exits 1 if any turn misbehaves.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("names", nargs="*", help="scenario names (default: all)")
    parser.add_argument("--ai", action="store_true", help="let the AI write replies (real API calls)")
    parser.add_argument("--dataset", default=str(ROOT / "dataset"))
    parser.add_argument("--out", default=str(ROOT / "output" / "conversations"))
    args = parser.parse_args()

    from vera.config import load_env
    load_env()
    if not args.ai:
        os.environ["VERA_LLM"] = "off"
    os.environ.pop("VERA_REFERENCE_NOW", None)  # the harness sends the reference time itself
    os.environ.setdefault("VERA_REPLY_DEADLINE", "30")  # offline: wait for the model instead of falling back

    from vera import harness, llm, responder, writer
    cache_file = writer.default_cache_file()
    writer.CACHE.get("", cache_file)  # load saved AI first messages into memory

    responder.CACHE_FILE = cache_file  # AI replies saved too, so a re-run is free (never on the live server)
    import bot  # noqa: F401  (sets up logging; quiet the per-request lines)
    for name in ("httpx2", "vera.api", "vera.replies"):
        logging.getLogger(name).setLevel(logging.WARNING)

    results = harness.run_all(args.dataset, args.names or None, ai_openers=False)  # tokens go to replies only
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    mode = f"on ({llm.model_name()})" if args.ai and llm.enabled() else "off (fixed wording)"
    for result in results:
        text = harness.to_markdown(result).replace("\n\n", f"\n\nAI replies: {mode}.\n\n", 1)
        (out / f"{result['name']}.md").write_text(text + "\n", encoding="utf-8")
        print(f"{'✅' if not result['problems'] else '❌'} {result['name']}: {result['passed']}/{result['total']}"
              + "".join(f"\n     {p}" for p in result["problems"]))
    # the index covers every transcript on disk, so running a few scenarios keeps the others listed
    rows = ["# Conversation scenarios", "", "Each scenario starts clean, pushes the seed dataset, opens the chat "
            "with a tick and plays the other side through /v1/reply.", "",
            "| Scenario | Turns OK | AI replies | What it checks |", "|---|---|---|---|"]
    for scenario in harness.SCENARIOS:
        path = out / f"{scenario.name}.md"
        if path.exists():
            lines = path.read_text(encoding="utf-8").splitlines()
            ai = next((l.split(": ", 1)[1].rstrip(".") for l in lines if l.startswith("AI replies:")), "?")
            status = next((l for l in lines if l.startswith("**") and "turns as expected" in l), "")
            ok = "✅" if "problems:" not in status else "❌"
            count = status.split(" turns")[0].strip("*")
            rows.append(f"| [{scenario.name}]({scenario.name}.md) | {ok} {count} | {ai} | {scenario.about} |")
    (out / "README.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    if args.ai:
        print(f"API usage: {llm.USAGE}")
    print(f"Transcripts: {out}")
    return 0 if all(not r["problems"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
