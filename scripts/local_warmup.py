#!/usr/bin/env python3
"""Push the dataset to a running bot over HTTP, the way the judge's warmup does, then check healthz.

judge_simulator.py only pushes 5 merchants and needs an LLM key. This pushes what the real
warmup sends (5 categories, 50 merchants, 200 customers) and needs nothing but the bot.

Usage:
    python3 scripts/local_warmup.py                      # http://localhost:8080, dataset/expanded
    python3 scripts/local_warmup.py --with-triggers      # also push all 100 triggers
    python3 scripts/local_warmup.py --check-versions     # also probe 409 / 400 handling

Exits 1 if any push fails or the healthz counts don't match.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from vera.loader import iter_dataset  # noqa: E402
from vera.normalize import iso_z  # noqa: E402


def call(url: str, method: str = "GET", body: object = None, raw: bytes | None = None) -> tuple[int, dict]:
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except error.HTTPError as exc:
        return exc.code, json.loads(exc.read() or b"{}")


def envelope(scope: str, context_id: str, version: int, payload: dict) -> dict:
    return {"scope": scope, "context_id": context_id, "version": version, "payload": payload,
            "delivered_at": iso_z()}


def check_versions(url: str, dataset: Path, version: int) -> list[str]:
    """Probe the status codes the judge relies on. Leaves one category at version+1."""
    scope, context_id, payload = next(iter_dataset(dataset, scopes=("category",)))
    target = f"{url}/v1/context"
    checks = [
        ("same version again -> 409", call(target, "POST", envelope(scope, context_id, version, payload))[0], 409),
        ("higher version -> 200", call(target, "POST", envelope(scope, context_id, version + 1, payload))[0], 200),
        ("older version -> 409", call(target, "POST", envelope(scope, context_id, version, payload))[0], 409),
        ("bad scope -> 400", call(target, "POST", envelope("order", "x", 1, {}))[0], 400),
        ("malformed JSON -> 400", call(target, "POST", raw=b"{not json")[0], 400),
    ]
    failures = []
    for label, got, expected in checks:
        ok = got == expected
        print(f"  [{'PASS' if ok else 'FAIL'}] {label} (got {got})")
        if not ok:
            failures.append(label)
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Local stand-in for the judge's warmup.")
    parser.add_argument("--url", default="http://localhost:8080")
    parser.add_argument("--dataset", default=str(ROOT / "dataset" / "expanded"))
    parser.add_argument("--version", type=int, default=1)
    parser.add_argument("--with-triggers", action="store_true")
    parser.add_argument("--check-versions", action="store_true")
    args = parser.parse_args()
    url, dataset = args.url.rstrip("/"), Path(args.dataset)

    try:
        status, health = call(f"{url}/v1/healthz")
    except error.URLError as exc:
        print(f"Bot not reachable at {url}: {exc.reason}", file=sys.stderr)
        return 1
    print(f"healthz before: {status} {health.get('contexts_loaded')}")

    scopes = ("category", "merchant", "customer") + (("trigger",) if args.with_triggers else ())
    expected, already, failed = Counter(), Counter(), []
    for scope, context_id, payload in iter_dataset(dataset, scopes=scopes):
        expected[scope] += 1
        status, body = call(f"{url}/v1/context", "POST", envelope(scope, context_id, args.version, payload))
        if status == 409 and body.get("current_version", -1) >= args.version:
            already[scope] += 1  # re-running against the same process; restart the bot for a clean warmup
        elif status != 200:
            failed.append(f"{scope}/{context_id}: {status} {body}")

    status, health = call(f"{url}/v1/healthz")
    loaded = health.get("contexts_loaded", {})
    print(f"pushed:         {dict(expected)}")
    if already:
        print(f"already stored: {dict(already)} (409 stale_version; restart the bot for a clean run)")
    print(f"healthz after:  {status} {loaded}")
    mismatched = [scope for scope, count in expected.items() if loaded.get(scope) != count]
    for scope in mismatched:
        failed.append(f"healthz reports {loaded.get(scope)} {scope} contexts, expected {expected[scope]}")

    if args.check_versions:
        print("version handling:")
        failed += check_versions(url, dataset, args.version)

    if failed:
        print("\nFAILED:")
        for line in failed[:20]:
            print(f"  {line}")
        return 1
    print("\nWarmup OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
