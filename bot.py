"""Vera: HTTP surface for the magicpin judge harness (challenge-testing-brief.md §2).

/v1/context stores what the judge pushes (phase 1). /v1/tick picks triggers (policy), builds
fact sheets (phase 2) and has the AI writer (phase 3) rewrite them in parallel, falling back
to the plain templates. /v1/reply classifies each reply and answers send / wait / end (phase 5).
compose() below is the offline contract from challenge-brief §7.

Run: uvicorn bot:app --host 0.0.0.0 --port 8080
"""

from __future__ import annotations

import asyncio
import logging
import os
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from vera import __version__, llm, writer
from vera.bundle import build_bundle
from vera.compose import compose, compose_bundle, compose_many  # noqa: F401  (compose: challenge-brief §7)
from vera.normalize import iso_z
from vera.policy import new_conversation_id, plan_tick, recipient_of
from vera.responder import handle_reply
from vera.state import RuntimeState
from vera.store import ContextStore

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"),
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("vera.api")

START = time.time()
STARTED_AT = iso_z()
store = ContextStore()
state = RuntimeState()
app = FastAPI(title="Vera", version=__version__)

if os.getenv("VERA_REFERENCE_NOW"):
    log.warning("VERA_REFERENCE_NOW=%s overrides the judge's clock; unset it for the real test",
                os.getenv("VERA_REFERENCE_NOW"))


async def _read_json(request: Request, error_body: dict) -> tuple[object, JSONResponse | None]:
    try:
        return await request.json(), None
    except Exception as exc:  # malformed JSON or wrong encoding
        return None, JSONResponse({**error_body, "details": f"invalid JSON: {exc}"}, status_code=400)


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception) -> JSONResponse:
    log.exception("unhandled error on %s", request.url.path)
    return JSONResponse({"error": "internal_error", "details": str(exc)}, status_code=500)


@app.get("/v1/healthz")
async def healthz() -> dict:
    return {"status": "ok", "uptime_seconds": int(time.time() - START), "contexts_loaded": store.counts()}


@app.get("/v1/metadata")
async def metadata() -> dict:
    return {
        "team_name": os.getenv("TEAM_NAME", "Team Vera"),
        "team_members": [m.strip() for m in os.getenv("TEAM_MEMBERS", "").split(",") if m.strip()],
        "model": os.getenv("VERA_MODEL") or (llm.model_name() if llm.enabled() else "templates only"),
        "approach": os.getenv("VERA_APPROACH",
                              "versioned context store -> fact sheet -> LLM composer -> validator -> template fallback"),
        "contact_email": os.getenv("CONTACT_EMAIL", ""),
        "version": __version__,
        "submitted_at": os.getenv("SUBMITTED_AT", STARTED_AT),
    }


@app.post("/v1/context")
async def push_context(request: Request) -> JSONResponse:
    body, error = await _read_json(request, {"accepted": False, "reason": "invalid_json"})
    if error:
        return error
    status, response = store.ingest(body)
    if status != 200:
        log.info("context push refused (%s): %s", status, response)
    return JSONResponse(response, status_code=status)


@app.post("/v1/tick")
async def tick(request: Request) -> JSONResponse:
    body, error = await _read_json(request, {"actions": []})
    if error:
        return error
    body = body if isinstance(body, dict) else {}
    triggers = body.get("available_triggers") or []
    triggers = [t for t in triggers if isinstance(t, str)] if isinstance(triggers, list) else []
    state.note_tick(body.get("now"), triggers)
    plan = plan_tick(store, state, triggers, now=body.get("now"))
    try:
        written = await compose_many(plan.chosen, state=state)
    except Exception:  # never let the writer sink the whole tick
        log.exception("compose_many failed; sending nothing this tick")
        written = []
    actions, ai_count = [], 0
    for bundle, (message, _sheet) in zip(plan.chosen, written):
        ai_count += message.get("writer") == "ai"
        conversation_id = new_conversation_id(state, bundle)
        merchant_id = bundle.trigger.get("merchant_id") or (bundle.merchant or {}).get("merchant_id")
        customer_id = bundle.trigger.get("customer_id") if bundle.audience == "customer" else None
        actions.append({
            "conversation_id": conversation_id,
            "merchant_id": merchant_id,
            "customer_id": customer_id,
            "send_as": message["send_as"],
            "trigger_id": bundle.trigger_id,
            "template_name": message["template_name"],
            "template_params": message["template_params"],
            "body": message["body"],
            "cta": message["cta"],
            "suppression_key": message["suppression_key"],
            "rationale": message["rationale"],
        })
        state.record_outbound(conversation_id, message["body"], now=plan.now, merchant_id=merchant_id,
                              customer_id=customer_id, trigger_id=bundle.trigger_id, send_as=message["send_as"],
                              suppression_key=message["suppression_key"],
                              meta={"template_name": message["template_name"], "cta": message["cta"]})
    log.info("tick %s: %d available, %d sent (%d AI-written), %d skipped%s", plan.now, len(triggers),
             len(actions), ai_count, len(plan.skipped), "".join(f"\n  skip {s['trigger_id']}: {s['reason']}" for s in plan.skipped))
    return JSONResponse({"actions": actions})


@app.post("/v1/reply")
async def reply(request: Request) -> JSONResponse:
    body, error = await _read_json(request, {"action": "end", "rationale": "unreadable request"})
    if error:
        return error
    body = body if isinstance(body, dict) else {}
    conversation_id = body.get("conversation_id")
    if not isinstance(conversation_id, str) or not conversation_id:
        return JSONResponse({"action": "end", "rationale": "missing conversation_id"}, status_code=400)
    try:  # in a thread: an AI reply can take seconds, and healthz must keep answering meanwhile
        response = await asyncio.to_thread(handle_reply, store, state, body)
    except Exception:
        log.exception("reply handling failed for %s", conversation_id)
        response = {"action": "wait", "wait_seconds": 1800, "rationale": "Internal error; backing off."}
    return JSONResponse(response)


@app.post("/v1/teardown")
async def teardown() -> dict:
    store.wipe()
    state.wipe()
    writer.CACHE.clear()
    log.info("teardown: all contexts and conversation state wiped")
    return {"status": "ok", "wiped": True}


if os.getenv("VERA_DEBUG") == "1":
    @app.get("/debug/bundle/{trigger_id}")
    async def debug_bundle(trigger_id: str, now: str | None = None) -> JSONResponse:
        """Local-only: the ContextBundle the composer would get for this trigger."""
        bundle = build_bundle(store, trigger_id, now=now or state.last_tick_now, state=state)
        if bundle is None:
            return JSONResponse({"error": f"unknown trigger {trigger_id}"}, status_code=404)
        return JSONResponse(bundle.to_dict())

    @app.get("/debug/sheet/{trigger_id}")
    async def debug_sheet(trigger_id: str, now: str | None = None) -> JSONResponse:
        """Local-only: the phase 2 writing brief and the plain message it renders to."""
        bundle = build_bundle(store, trigger_id, now=now or state.last_tick_now, state=state)
        if bundle is None:
            return JSONResponse({"error": f"unknown trigger {trigger_id}"}, status_code=404)
        message, sheet = compose_bundle(bundle, state=state)
        return JSONResponse({"message": message, "prompt": sheet.to_prompt(), "sheet": sheet.to_dict(),
                             "recipient": recipient_of(bundle)})

    @app.get("/debug/state")
    async def debug_state() -> dict:
        return {"contexts": store.counts(), "runtime": state.summary(),
                "last_tick": {"now": state.last_tick_now, "triggers": state.last_tick_triggers}}
