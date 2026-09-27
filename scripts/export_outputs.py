#!/usr/bin/env python3
"""Export every pipeline stage for the 30 test pairs into output/, with checks and a test run.

For each pair: the raw input, the phase 1 briefing, the phase 2 writing brief and plain
message, the phase 3 AI message, checks on both messages, and whether the final message
matches submission.jsonl. Also a demo of the tick choosing step and the pytest output.

Makes no API calls: AI messages come from the saved results (.cache/ai_messages.json)
written by write_submission.py. A brief with no saved result is reported, not generated.

Usage:
    python3 scripts/export_outputs.py               # -> output/
    python3 scripts/export_outputs.py --skip-tests  # faster: don't run pytest
"""

from __future__ import annotations

import os

os.environ["VERA_LLM"] = "off"  # export only reads saved AI results; it never calls the API

import argparse  # noqa: E402
import json  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402
from collections import Counter  # noqa: E402
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from vera.checks import run_checks  # noqa: E402
from vera.compose import CONTRACT_KEYS, DEFAULT_REFERENCE_NOW, bundle_from_dicts  # noqa: E402
from vera.factsheet import CTA_LABELS, build_fact_sheet  # noqa: E402
from vera.loader import load_dataset, load_test_pairs  # noqa: E402
from vera.policy import new_conversation_id, plan_tick  # noqa: E402
from vera.state import RuntimeState  # noqa: E402
from vera.store import ContextStore  # noqa: E402
from vera.templates import render  # noqa: E402
from vera.validator import fixes  # noqa: E402
from vera.writer import CACHE, build_prompt, default_cache_file, fingerprint, write_ai  # noqa: E402

MARK = {True: "✅", False: "❌", None: "➖"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fence(obj, lang: str = "json") -> str:
    text = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, indent=2)
    return f"```{lang}\n{text}\n```"


def details(summary: str, body: str) -> str:
    return f"<details><summary>{summary}</summary>\n\n{body}\n\n</details>"


def quote(text: str) -> str:
    return "\n".join(f"> {line}" for line in text.splitlines())


def phase4_note(result: dict) -> str:
    first, sheet = result["first_attempt"], result["sheet"]
    if result["ai_reason"] == "ok":
        return "The AI's first version passed every check."
    if result["ai_reason"] == "retried" and first:
        from vera.validator import problems
        issues = problems(first["body"], sheet)
        return "\n\n".join([
            f"The AI's first version was **rejected** ({'; '.join(issues)}):", quote(first["body"]),
            "It was sent back once with this feedback:", "\n".join(f"- {line}" for line in fixes(issues, sheet)),
            "The rewrite (shown above) passed every check."])
    return f"No AI message passed ({result['ai_reason']}), so the plain message is sent; it passes every check."


def run_pair(dataset: Path, pair: dict) -> dict:
    trigger = read_json(dataset / "triggers" / f"{pair['trigger_id']}.json")
    merchant = read_json(dataset / "merchants" / f"{pair['merchant_id']}.json")
    category = read_json(dataset / "categories" / f"{merchant['category_slug']}.json")
    customer = read_json(dataset / "customers" / f"{pair['customer_id']}.json") if pair.get("customer_id") else None

    bundle = bundle_from_dicts(category, merchant, trigger, customer)       # phase 1
    sheet = build_fact_sheet(bundle)                                         # phase 2
    plain = {**render(sheet), "writer": "template"}
    ai, ai_reason = write_ai(sheet, plain, cache_file=default_cache_file())  # phases 3+4 (saved results only)
    first = CACHE.get(fingerprint(build_prompt(sheet, plain)), default_cache_file())  # the first AI attempt
    final = ai or plain
    return {"pair": pair, "input": {"trigger": trigger, "merchant": merchant, "category": category,
                                     "customer": customer},
            "bundle": bundle, "sheet": sheet, "plain": plain, "ai": ai, "ai_reason": ai_reason, "final": final,
            "first_attempt": first,
            "checks_plain": run_checks(plain["body"], sheet),
            "checks_ai": run_checks(ai["body"], sheet) if ai else None}


def checks_table(result: dict) -> str:
    rows = ["| Check | Plain message | AI message |", "|---|---|---|"]
    ai_rows = result["checks_ai"] or [None] * len(result["checks_plain"])
    for plain, ai in zip(result["checks_plain"], ai_rows):
        def cell(c):
            if c is None:
                return "(no AI message)"
            return MARK[c.ok] + (f" {c.detail}" if c.detail and c.ok is not True else "")
        kind = "" if plain.hard else " *(advisory)*"
        rows.append(f"| {plain.name}{kind} | {cell(plain)} | {cell(ai)} |")
    return "\n".join(rows)


def pair_markdown(result: dict, submitted: dict | None) -> str:
    pair, b, sheet = result["pair"], result["bundle"], result["sheet"]
    inp, plain, ai, final = result["input"], result["plain"], result["ai"], result["final"]
    to = sheet.address_as or sheet.recipient_id
    matches = submitted is not None and all(submitted.get(k) == final[k] for k in CONTRACT_KEYS)
    category = inp["category"]
    category_view = {"slug": category.get("slug"), "voice": category.get("voice"),
                     "peer_stats": category.get("peer_stats"),
                     "offer_catalog": [o.get("title") for o in category.get("offer_catalog", [])],
                     "digest (titles)": [d.get("title") for d in category.get("digest", [])],
                     "seasonal_beats": category.get("seasonal_beats")}
    facts_by_group = {}
    for fact in b.facts:
        facts_by_group.setdefault(fact.group, []).append(fact)
    facts_md = "\n".join(f"- **{group}**: " + "; ".join(f.display for f in facts)
                         for group, facts in facts_by_group.items())

    parts = [
        f"# {pair['test_id']} · {sheet.kind} → {to} ({sheet.sender_name})",
        f"**Final message** (sent as `{sheet.send_as}`, written by **{final['writer']}**, "
        f"ask type `{final['cta']}`):",
        quote(final["body"]),
        f"Matches `submission.jsonl`: {MARK[matches]}",
        "## 0 · Input (what the judge sends)",
        f"**Trigger** `{pair['trigger_id']}`", fence(inp["trigger"]),
        details(f"Merchant <code>{pair['merchant_id']}</code> (full record)", fence(inp["merchant"])),
        details(f"Category <code>{category.get('slug')}</code> (key fields)", fence(category_view)),
        (details(f"Customer <code>{pair['customer_id']}</code>", fence(inp["customer"]))
         if inp["customer"] else "**Customer:** none (merchant-facing trigger)"),
        "## 1 · Phase 1: briefing (join, clean, compare, warn)",
        f"- **Audience:** {b.audience} · **send as:** `{b.send_as}` · **greeting:** {b.language.get('greeting')} "
        f"· **language:** {b.language.get('display')}",
        f"- **Event, made readable:** `{json.dumps(b.payload_display, ensure_ascii=False)}`",
        f"- **Data richness:** {b.richness.get('level')}",
        f"- **Digest item:** {b.digest_items[0]['id'] if b.digest_items else 'none'}",
        f"- **Slots:** " + ("; ".join(f"{s['label']} → {s['safe_label']}" for s in b.slots) if b.slots else "none"),
        f"- **Consent:** {b.consent['reason'] if b.consent else 'n/a (merchant-facing)'}",
        "- **Warnings:** " + ("none" if not b.warnings else ""),
        *[f"  - {w}" for w in b.warnings],
        details(f"All {len(b.facts)} facts", facts_md),
        "## 2 · Phase 2: writing brief",
        f"- **Family:** {sheet.family} · **angle:** {sheet.angle}",
        f"- **Lead (why now):** {sheet.lead.text}",
        "- **Supporting facts:**", *[f"  - {line.text} *(from {line.source})*" for line in sheet.support],
        f"- **Ask:** {CTA_LABELS.get(sheet.ask['cta'], sheet.ask['cta'])}: {sheet.ask['text']}",
        f"- **Format:** {'pre-approved template' if sheet.template['required'] else 'free-form'} "
        f"(`{sheet.template['name']}`)",
        f"- **Allowed numbers:** {', '.join(sheet.allowed_numbers) or 'none'}",
        details("The prompt the AI receives", fence(sheet.to_prompt(), "text")),
        "**Plain message (fill-in-the-blanks writer):**", quote(plain["body"]),
        "## 3 · Phase 3: AI writer",
        (quote(ai["body"]) + f"\n\n**AI's rationale:** {ai['rationale']}") if ai
        else f"No AI message: {result['ai_reason']}. The plain message is what gets sent.",
        "## 4 · Phase 4: validator",
        phase4_note(result),
        "## Checks",
        checks_table(result),
    ]
    return "\n\n".join(part for part in parts if part)


def tick_demo(dataset: Path) -> str:
    store, state = ContextStore(), RuntimeState()
    load_dataset(store, dataset)
    available = ["trg_001_research_digest_dentists", "trg_002_compliance_dci_radiograph", "trg_003_recall_due_priya"]
    lines = ["# The choosing step on a real tick", "",
             "The judge calls `/v1/tick` with three active triggers: two for Dr. Meera and one for her patient "
             "Priya. The bot sends at most one message per person, most urgent first.", "",
             "## Tick 1 at 10:30", "", f"Available: `{', '.join(available)}`", ""]
    plan = plan_tick(store, state, available, now="2026-04-26T10:30:00Z")
    for bundle in plan.chosen:
        sheet = build_fact_sheet(bundle, state=state)
        plain = render(sheet)
        ai, _ = write_ai(sheet, {**plain, "writer": "template"}, cache_file=default_cache_file())
        body = (ai or plain)["body"]
        conv = new_conversation_id(state, bundle)
        state.record_outbound(conv, body, now=plan.now, merchant_id=bundle.trigger.get("merchant_id"),
                              customer_id=bundle.trigger.get("customer_id") if bundle.audience == "customer" else None,
                              trigger_id=bundle.trigger_id, send_as=sheet.send_as,
                              suppression_key=sheet.suppression_key)
        lines += [f"**Sent** `{bundle.trigger_id}` (urgency {bundle.trigger['urgency']}) to "
                  f"{sheet.address_as}, conversation `{conv}`, written by {'AI' if ai else 'plain writer'}:",
                  "", quote(body), ""]
    lines += [f"**Held** `{s['trigger_id']}`: {s['reason']}" for s in plan.skipped]
    plan2 = plan_tick(store, state, available, now="2026-04-26T10:35:00Z")
    lines += ["", "## Tick 2 at 10:35, same three triggers", "",
              f"Sent: {len(plan2.chosen)} message(s).", ""]
    lines += [f"- `{s['trigger_id']}`: {s['reason']}" for s in plan2.skipped]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export pipeline stages, checks and tests to output/.")
    parser.add_argument("--dataset", default=str(ROOT / "dataset" / "expanded"))
    parser.add_argument("--out", default=str(ROOT / "output"))
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args()
    dataset, out = Path(args.dataset), Path(args.out)

    pairs = load_test_pairs(dataset)
    if not pairs:
        print("No test_pairs.json. Run: python3 dataset/generate_dataset.py --seed-dir dataset --out dataset/expanded",
              file=sys.stderr)
        return 2
    submission_path = ROOT / "submission.jsonl"
    submitted = {}
    if submission_path.exists():
        for line in submission_path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            submitted[row["test_id"]] = row

    if out.exists():
        shutil.rmtree(out)
    (out / "pairs").mkdir(parents=True)

    results = [run_pair(dataset, pair) for pair in pairs]
    summary_rows, tallies, match_count = [], {"plain": Counter(), "ai": Counter()}, 0
    names = [c.name for c in results[0]["checks_plain"]]
    for r in results:
        pair, sheet, final = r["pair"], r["sheet"], r["final"]
        slug = f"{pair['test_id']}_{sheet.kind}"
        (out / "pairs" / f"{slug}.md").write_text(pair_markdown(r, submitted.get(pair["test_id"])), encoding="utf-8")
        (out / "pairs" / f"{slug}.json").write_text(json.dumps({
            "pair": pair, "input": r["input"], "phase1_briefing": r["bundle"].to_dict(),
            "phase2_writing_brief": r["sheet"].to_dict(), "phase2_prompt": r["sheet"].to_prompt(),
            "phase2_plain_message": r["plain"], "phase3_ai_message": r["ai"], "phase3_note": r["ai_reason"],
            "final": {k: final[k] for k in (*CONTRACT_KEYS, "writer")},
            "checks": {"plain": [vars(c) for c in r["checks_plain"]],
                       "ai": [vars(c) for c in r["checks_ai"]] if r["checks_ai"] else None},
        }, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        for which in ("plain", "ai"):
            checks = r["checks_plain"] if which == "plain" else r["checks_ai"]
            for c in checks or []:
                if c.ok is not None:
                    tallies[which][(c.name, c.ok)] += 1
        ai_checks = r["checks_ai"] or r["checks_plain"]
        failed = [c.name for c in ai_checks if c.ok is False]
        matches = pair["test_id"] in submitted and all(
            submitted[pair["test_id"]].get(k) == final[k] for k in CONTRACT_KEYS)
        match_count += matches
        summary_rows.append(
            f"| [{pair['test_id']}](pairs/{slug}.md) | {sheet.kind} | {sheet.address_as or sheet.recipient_id} "
            f"| {final['writer']} | {MARK[not failed]} {', '.join(failed)} | {MARK[matches]} "
            f"| {final['body'][:90].replace('|', '/')}… |")

    tests_line = "not run (--skip-tests)"
    if not args.skip_tests:
        run = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT, capture_output=True, text=True)
        (out / "tests.txt").write_text(run.stdout + run.stderr, encoding="utf-8")
        tests_line = next((l for l in reversed(run.stdout.splitlines()) if "passed" in l or "failed" in l),
                          "see tests.txt")

    (out / "tick_demo.md").write_text(tick_demo(dataset), encoding="utf-8")

    check_rows = ["| Check | Plain messages passing | AI messages passing |", "|---|---|---|"]
    ai_total = sum(1 for r in results if r["ai"])
    for name in names:
        p_ok, p_all = tallies["plain"][(name, True)], tallies["plain"][(name, True)] + tallies["plain"][(name, False)]
        a_ok, a_all = tallies["ai"][(name, True)], tallies["ai"][(name, True)] + tallies["ai"][(name, False)]
        check_rows.append(f"| {name} | {p_ok}/{p_all} | {a_ok}/{a_all} |")

    readme = "\n".join([
        "# Output: what the pipeline produces", "",
        "Generated by `scripts/export_outputs.py` (no API calls: AI messages come from the saved results).",
        "", "## How to read this folder", "",
        "- `pairs/<test>_<kind>.md`: one file per test pair showing **input → phase 1 briefing → phase 2 writing "
        "brief + plain message → phase 3 AI message → phase 4 validator → checks**. Start with any of them.",
        "- `pairs/<test>_<kind>.json`: the same, as full JSON (every fact, flag and field).",
        "- `tick_demo.md`: the choosing step on a real tick (who gets a message, who waits, and why).",
        "- `tests.txt`: the full test-suite run.", "",
        "## Results at a glance", "",
        f"- Test pairs: **{len(results)}**; AI-written: **{ai_total}** "
        f"({sum(1 for r in results if r['ai_reason'] == 'retried')} after a phase 4 retry); "
        f"plain fallback: **{len(results) - ai_total}**",
        f"- Final messages matching `submission.jsonl`: "
        f"**{match_count}/{len(results)}**",
        f"- Test suite: **{tests_line}**", "",
        "### Checks (hard ones block an AI message and trigger one retry; advisory ones only report)", "",
        *check_rows, "",
        "## All 30 pairs", "",
        "| Test | Trigger | To | Written by | Checks on the final message | Matches submission | Message |",
        "|---|---|---|---|---|---|---|",
        *summary_rows, "",
    ])
    (out / "README.md").write_text(readme, encoding="utf-8")
    print(f"Wrote {out}/README.md, {len(results)} pairs (x2 files), tick_demo.md"
          + ("" if args.skip_tests else ", tests.txt"))
    print(f"AI-written: {ai_total}/{len(results)}; tests: {tests_line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
