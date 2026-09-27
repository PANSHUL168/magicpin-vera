"""Scripted conversations for phase 5, played against the real HTTP app (offline tools and tests only).

Each scenario starts clean (teardown), pushes the seed dataset through /v1/context, opens a
conversation with /v1/tick the way the judge's tick would, then plays the merchant's (or
customer's) side through /v1/reply and checks what Vera does at every turn. The judge-style
scenario sends to conversation ids the bot never opened, like judge_simulator.py does.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import timedelta

from .loader import iter_dataset
from .normalize import detect_language, iso_z, parse_dt
from .responder import QUALIFYING

REFERENCE_NOW = "2026-04-26T10:30:00Z"
CANNED = "Thank you for contacting us! Our team will respond shortly."


@dataclass
class Turn:
    message: str
    expect: str                        # allowed actions, "send", "wait|end", ...
    conversation_id: str | None = None # None = the conversation the tick opened
    language: str | None = None        # "hinglish" / "english": the reply should mirror it


@dataclass
class Scenario:
    name: str
    about: str
    turns: list[Turn]
    trigger_id: str | None = None      # opened by a tick for this trigger; None = judge-opened
    merchant_id: str | None = None     # for judge-opened conversations
    from_role: str = "merchant"
    tick_after: list[str] = field(default_factory=list)  # triggers a later tick must NOT send (opt-out)


SCENARIOS = [
    Scenario("wa_business_bot", "Dr. Meera's WhatsApp Business auto-reply answers four times in a row.",
             [Turn("Thank you for contacting Dr. Meera's Dental Clinic! Our team will get back to you shortly.",
                   "send"),
              Turn("Thank you for contacting Dr. Meera's Dental Clinic! Our team will get back to you shortly.",
                   "wait"),
              Turn("Thank you for contacting Dr. Meera's Dental Clinic! Our team will get back to you shortly.",
                   "end"),
              Turn("Thank you for contacting Dr. Meera's Dental Clinic! Our team will get back to you shortly.",
                   "end")],
             trigger_id="trg_002_compliance_dci_radiograph"),
    Scenario("assistant_then_owner", "Studio11's Hinglish bot answers twice, then the owner replies for real.",
             [Turn("Namaste! Main Studio11 ki automated assistant hoon. Aapka message team tak pahuncha diya gaya "
                   "hai.", "send"),
              Turn("Jaankari ke liye bahut shukriya. Hum jald hi sampark karenge.", "wait"),
              Turn("Haan boliye, main owner hoon. Kya plan hai?", "send", language="hinglish")],
             trigger_id="trg_008_curious_ask_studio11"),
    Scenario("intent_transition", "Mylari's owner warms up, asks a question, then commits: Vera must act, "
                                  "not keep qualifying.",
             [Turn("Sounds interesting, tell me more", "send"),
              Turn("How many offices are near us?", "send"),
              Turn("Ok lets do it. Whats next?", "send")],
             trigger_id="trg_013_corporate_thali_planning"),
    Scenario("join_intent", "Sunrise Pharmacy says yes in Hinglish: straight to the steps.",
             [Turn("Haan kar do, verify karna hai. Kitna time lagega?", "send", language="hinglish")],
             trigger_id="trg_021_unverified_gbp_sunrise"),
    Scenario("hostile_then_gst", "Bharat is annoyed, then asks about GST: one apology, then decline and "
                                 "steer back.",
             [Turn("Yeh sab bakwas hai, roz roz message aata hai", "send"),
              Turn("Accha ek baat batao, GST filing kaise karu?", "send"),
              Turn("Faltu hai sab", "end")],
             trigger_id="trg_004_perf_dip_bharat"),
    Scenario("opt_out", "Glamour Salon asks to stop: end now, and the next tick for them sends nothing.",
             [Turn("Please don't message me again", "end")],
             trigger_id="trg_025_dormancy_glamour", tick_after=["trg_009_winback_glamour"]),
    Scenario("busy_then_back", "Pizza Junction is busy on match day, then comes back with a question.",
             [Turn("Busy right now, match day rush. Baad mein baat karte hain", "wait"),
              Turn("Ok free now. What's the offer exactly?", "send")],
             trigger_id="trg_010_ipl_match_delhi"),
    Scenario("language_switch", "Zen Yoga replies in Hinglish, then switches to English: each reply mirrors.",
             [Turn("Arre wah, yeh toh accha hai! Aage kya karna chahiye?", "send", language="hinglish"),
              Turn("Can you send me the numbers in English please?", "send", language="english")],
             trigger_id="trg_024_perf_spike_zen"),
    Scenario("customer_slot", "Priya picks a recall slot, then says thanks.",
             [Turn("1", "send"), Turn("Thank you!", "end")],
             trigger_id="trg_003_recall_due_priya", from_role="customer"),
    Scenario("judge_style", "judge_simulator.py's own checks: conversations Vera never opened.",
             [Turn(CANNED, "send|wait", "conv_auto_1"), Turn(CANNED, "wait|end", "conv_auto_2"),
              Turn(CANNED, "end", "conv_auto_3"), Turn(CANNED, "end", "conv_auto_4"),
              Turn("Ok lets do it. Whats next?", "send", "conv_intent_1"),
              Turn("Stop messaging me. This is useless spam.", "end", "conv_hostile")],
             merchant_id="m_001_drmeera_dentist_delhi"),
]


@contextmanager
def _llm_off(off: bool):
    old = os.environ.get("VERA_LLM")
    if off:
        os.environ["VERA_LLM"] = "off"
    try:
        yield
    finally:
        if off:
            os.environ.pop("VERA_LLM", None) if old is None else os.environ.__setitem__("VERA_LLM", old)


def _push_dataset(client, dataset) -> None:
    for scope, context_id, payload in iter_dataset(dataset):
        response = client.post("/v1/context", json={"scope": scope, "context_id": context_id, "version": 1,
                                                     "payload": payload, "delivered_at": REFERENCE_NOW})
        if response.status_code != 200:
            raise RuntimeError(f"push {scope}/{context_id} failed: {response.status_code} {response.text}")


def _check(turn: Turn, response: dict, sent_before: list[str]) -> list[str]:
    problems = []
    action = response.get("action")
    if action not in turn.expect.split("|"):
        problems.append(f"expected {turn.expect}, got {action}")
    if not response.get("rationale"):
        problems.append("no rationale")
    if action == "send":
        body = response.get("body") or ""
        if not body or not response.get("cta"):
            problems.append("send without body or cta")
        if body in sent_before:
            problems.append("repeats an earlier message")
        low = body.lower()
        if "let" in turn.message.lower() and "do it" in turn.message.lower() and any(q in low for q in QUALIFYING):
            problems.append("still qualifying after a yes")
        got = detect_language(body)
        if turn.language == "hinglish" and got not in ("hi", "hi-en"):
            problems.append(f"reply not in Hinglish ({got})")
        if turn.language == "english" and got != "en":
            problems.append(f"reply not in English ({got})")
    return problems


def run_scenario(scenario: Scenario, dataset, *, client=None, ai_openers: bool = True) -> dict:
    """ai_openers=False keeps the opening tick on cached or plain messages (spend tokens on replies only)."""
    import bot
    from fastapi.testclient import TestClient

    client = client or TestClient(bot.app)
    client.post("/v1/teardown")
    _push_dataset(client, dataset)
    log, problems, sent = [], [], []
    conversation_id, merchant_id, customer_id = None, scenario.merchant_id, None
    if scenario.trigger_id:
        with _llm_off(not ai_openers):
            actions = client.post("/v1/tick", json={"now": REFERENCE_NOW,
                                                    "available_triggers": [scenario.trigger_id]}).json()["actions"]
        if len(actions) != 1:
            return {"name": scenario.name, "about": scenario.about, "log": [],
                    "problems": [f"tick sent {len(actions)} messages, expected 1"], "passed": 0,
                    "total": len(scenario.turns)}
        opener = actions[0]
        conversation_id, merchant_id, customer_id = (opener["conversation_id"], opener["merchant_id"],
                                                     opener["customer_id"])
        sent.append(opener["body"])
        log.append({"who": "vera", "action": "tick", "body": opener["body"], "cta": opener["cta"],
                    "rationale": opener["rationale"], "conversation_id": conversation_id})
    passed = 0
    for i, turn in enumerate(scenario.turns, start=1):
        received = iso_z(parse_dt(REFERENCE_NOW) + timedelta(minutes=5 * i))
        cid = turn.conversation_id or conversation_id
        response = client.post("/v1/reply", json={
            "conversation_id": cid, "merchant_id": merchant_id, "customer_id": customer_id,
            "from_role": scenario.from_role, "message": turn.message, "received_at": received,
            "turn_number": i + 1}).json()
        turn_problems = _check(turn, response, sent if turn.conversation_id is None else [])
        if response.get("action") == "send" and turn.conversation_id is None:
            sent.append(response["body"])
        passed += not turn_problems
        problems += [f"turn {i}: {p}" for p in turn_problems]
        log.append({"who": scenario.from_role, "body": turn.message, "conversation_id": cid})
        log.append({"who": "vera", **response, "expect": turn.expect, "problems": turn_problems})
    if scenario.tick_after:
        later = iso_z(parse_dt(REFERENCE_NOW) + timedelta(hours=2))
        actions = client.post("/v1/tick", json={"now": later, "available_triggers": scenario.tick_after}).json()
        sent_to = [a["trigger_id"] for a in actions["actions"]]
        log.append({"who": "tick", "body": f"later tick with {', '.join(scenario.tick_after)}: "
                                           f"{len(sent_to)} sent", "action": "tick"})
        if sent_to:
            problems.append(f"messaged an opted-out merchant again ({', '.join(sent_to)})")
    client.post("/v1/teardown")
    return {"name": scenario.name, "about": scenario.about, "log": log, "problems": problems, "passed": passed,
            "total": len(scenario.turns)}


def run_all(dataset, names: list[str] | None = None, *, ai_openers: bool = True) -> list[dict]:
    import bot
    from fastapi.testclient import TestClient

    client = TestClient(bot.app)
    return [run_scenario(s, dataset, client=client, ai_openers=ai_openers)
            for s in SCENARIOS if not names or s.name in names]


def to_markdown(result: dict) -> str:
    lines = [f"# {result['name']}", "", result["about"], "",
             f"**{result['passed']}/{result['total']} turns as expected**"
             + ("" if not result["problems"] else " · problems: " + "; ".join(result["problems"])), ""]
    for entry in result["log"]:
        if entry["who"] == "tick":
            lines += [f"*{entry['body']}*", ""]
        elif entry["who"] == "vera" and entry.get("action") == "tick":
            lines += [f"**Vera** (first message, cta `{entry['cta']}`):", f"> {entry['body']}", "",
                      f"<sub>{entry['rationale']}</sub>", ""]
        elif entry["who"] == "vera":
            mark = "✅" if not entry.get("problems") else "❌ " + "; ".join(entry["problems"])
            head = f"**Vera → {entry.get('action')}**"
            if entry.get("action") == "send":
                lines += [f"{head} (cta `{entry.get('cta')}`) {mark}", f"> {entry.get('body')}", ""]
            elif entry.get("action") == "wait":
                lines += [f"{head} {entry.get('wait_seconds')}s {mark}", ""]
            else:
                lines += [f"{head} {mark}", ""]
            lines += [f"<sub>{entry.get('rationale')}</sub>", ""]
        else:
            where = f" · `{entry['conversation_id']}`" if entry.get("conversation_id") else ""
            lines += [f"**{entry['who'].capitalize()}**{where}:", f"> {entry['body']}", ""]
    return "\n".join(lines)
