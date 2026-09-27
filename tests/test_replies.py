import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import bot
from conversation_handlers import respond
from vera import llm
from vera.loader import load_dataset
from vera.policy import plan_tick
from vera.replies import classify
from vera.responder import handle_reply
from vera.state import RuntimeState
from vera.store import ContextStore

ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-04-26T10:30:00Z"
MEERA = "m_001_drmeera_dentist_delhi"
CANNED = "Thank you for contacting us! Our team will respond shortly."


@pytest.fixture(scope="module")
def seeds() -> ContextStore:
    """Seed dataset; handle_reply only reads the store."""
    store = ContextStore()
    load_dataset(store, ROOT / "dataset")
    return store


@pytest.fixture
def fake_llm(monkeypatch):
    class Fake:
        reply: object = "Done. Here is the draft: 'Radiograph safety update for our patients.' Reply CONFIRM to post."
        calls: list = []

    fake = Fake()
    fake.calls = []

    def complete_json(instructions, prompt, schema, *, name, max_output_tokens=1200):
        fake.calls.append(prompt)
        reply = fake.reply(prompt) if callable(fake.reply) else fake.reply
        return llm.LLMResult({"body": reply, "rationale": "fake rationale"}, "fake-model", 100, 50, 10, 0.01)

    monkeypatch.setenv("VERA_LLM", "on")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(llm, "complete_json", complete_json)
    return fake


def reply(store, state, message, *, conv="conv_x", merchant=MEERA, customer=None, role="merchant", minute=5):
    return handle_reply(store, state, {"conversation_id": conv, "merchant_id": merchant, "customer_id": customer,
                                       "from_role": role, "message": message,
                                       "received_at": f"2026-04-26T10:{30 + minute:02d}:00Z"})


def opened(state, trigger_id, conv="conv_x", merchant=MEERA, customer=None, body="Opening message."):
    """A conversation the bot started from a trigger, like /v1/tick does."""
    state.record_outbound(conv, body, now=NOW, merchant_id=merchant, customer_id=customer, trigger_id=trigger_id)
    return conv


@pytest.mark.parametrize("message, kind", [
    ("STOP", "opt_out"),
    ("Please don't message me again", "opt_out"),
    ("Mat bhejo yeh sab", "opt_out"),
    (CANNED, "auto_reply"),
    ("Namaste! Main Studio11 ki automated assistant hoon. Aapka message team tak pahuncha diya gaya hai.",
     "auto_reply"),
    ("Jaankari ke liye bahut shukriya. Hum jald hi sampark karenge.", "auto_reply"),
    ("Ok lets do it. Whats next?", "commit"),
    ("Mujhe magicpin judna hai", "commit"),
    ("Haan kar do", "commit"),
    ("Yes", "commit"),
    ("What's the price per plate?", "question"),
    ("Is there a bus stop near the clinic?", "question"),
    ("Busy right now", "later"),
    ("No thanks", "decline"),
    ("Thanks!", "thanks"),
    ("This is useless", "hostile"),
    ("GST kaise file karu?", "off_topic"),
    ("Sounds interesting, tell me more", "engaged"),
    ("", "empty"),
    ("No, do not go ahead", "decline"),
    ("Don't send it", "decline"),
    ("No problem, let's do it", "commit"),
    ("Can you send me the price?", "question"),
    ("Thank you for contacting us! How can we help you?", "auto_reply"),
])
def test_classify(message, kind):
    assert classify(message).kind == kind


def test_classify_details():
    assert classify("Kal baat karte hain").detail["wait_seconds"] == 86400
    assert classify("Busy, later").detail["wait_seconds"] == 1800
    assert classify("GST kaise file karu?").detail["topic"] == "gst"
    # the same longer text again is a bot; a repeated "yes" is just a person
    assert classify("Please call the clinic number for bookings", repeats=2).kind == "auto_reply"
    assert classify("yes", repeats=3).kind == "commit"
    slots = ["5 Nov, 6pm", "6 Nov, 5pm"]
    assert classify("2", slot_labels=slots).detail == {"slot": 1}
    assert classify("6 nov works for me", slot_labels=slots).detail == {"slot": 1}
    assert classify("Yes, thank you for contacting me about this").kind != "auto_reply"


def test_auto_reply_counts_per_party_across_conversations(seeds):
    state = RuntimeState()
    first = reply(seeds, state, CANNED, conv="conv_auto_1")
    assert first["action"] == "send" and first["cta"] == "binary_yes_no" and "auto-reply" in first["body"]
    assert reply(seeds, state, CANNED, conv="conv_auto_2")["action"] == "wait"
    assert reply(seeds, state, CANNED, conv="conv_auto_3")["action"] == "end"
    assert state.party(MEERA).last_inbound_at is None  # a bot's text doesn't open the 24h window


def test_real_reply_resets_the_auto_reply_count(seeds):
    state = RuntimeState()
    reply(seeds, state, CANNED, conv="c1")
    reply(seeds, state, CANNED, conv="c1", minute=6)
    assert reply(seeds, state, "Haan boliye, kya plan hai?", conv="c1", minute=7)["action"] == "send"
    assert state.party(MEERA).auto_replies == 0 and state.party(MEERA).last_inbound_at


def test_opt_out_ends_and_blocks_the_next_tick(seeds):
    state = RuntimeState()
    conv = opened(state, "trg_025_dormancy_glamour", merchant="m_004_glamour_salon_pune")
    assert reply(seeds, state, "Please don't message me again", conv=conv,
                 merchant="m_004_glamour_salon_pune")["action"] == "end"
    assert state.is_opted_out("m_004_glamour_salon_pune")
    plan = plan_tick(seeds, state, ["trg_009_winback_glamour"], now=NOW)
    assert not plan.chosen and plan.skipped
    # a later "ok" stays quiet; a clear request brings them back
    assert reply(seeds, state, "ok", conv=conv, merchant="m_004_glamour_salon_pune", minute=8)["action"] == "end"
    assert reply(seeds, state, "Actually go ahead, let's do it", conv=conv, merchant="m_004_glamour_salon_pune",
                 minute=9)["action"] == "send"
    assert not state.is_opted_out("m_004_glamour_salon_pune")


def test_hostile_gets_one_apology_then_end(seeds):
    state = RuntimeState()
    conv = opened(state, "trg_004_perf_dip_bharat", merchant="m_002_bharat_dentist_mumbai")
    first = reply(seeds, state, "This is useless", conv=conv, merchant="m_002_bharat_dentist_mumbai")
    assert first["action"] == "send" and "sorry" in first["body"].lower() and first["cta"] == "none"
    assert reply(seeds, state, "Nonsense", conv=conv, merchant="m_002_bharat_dentist_mumbai",
                 minute=6)["action"] == "end"


def test_off_topic_declines_and_steers_back_to_our_ask(seeds):
    state = RuntimeState()
    conv = opened(state, "trg_004_perf_dip_bharat", merchant="m_002_bharat_dentist_mumbai")
    out = reply(seeds, state, "Can you help me file GST?", conv=conv, merchant="m_002_bharat_dentist_mumbai")
    assert out["action"] == "send" and "CA" in out["body"] and "Coming back to our chat" in out["body"]
    assert out["cta"] == "binary_yes_no"


def test_never_repeats_itself_in_a_conversation(seeds):
    state = RuntimeState()
    conv = opened(state, "trg_002_compliance_dci_radiograph")
    bodies = [reply(seeds, state, "Interesting, go on", conv=conv, minute=m).get("body") for m in (5, 6)]
    assert bodies[0] and bodies[1] and bodies[0] != bodies[1]
    assert reply(seeds, state, "Interesting, go on", conv=conv, minute=7)["action"] == "wait"


def test_slot_pick_books_the_offered_slot(seeds):
    state = RuntimeState()
    conv = opened(state, "trg_003_recall_due_priya", customer="c_001_priya_for_m001")
    out = reply(seeds, state, "2", conv=conv, customer="c_001_priya_for_m001", role="customer")
    assert out["action"] == "send" and "6 Nov, 5pm" in out["body"] and "Thu" not in out["body"]
    assert reply(seeds, state, "Thank you!", conv=conv, customer="c_001_priya_for_m001", role="customer",
                 minute=6)["action"] == "end"


def test_unknown_merchant_still_gets_a_valid_answer(seeds):
    out = reply(seeds, RuntimeState(), "Yes please", merchant="m_nobody")
    assert out["action"] == "send" and out["body"] and out["rationale"]


def test_commit_uses_the_ai_and_the_conversation(seeds, fake_llm):
    state = RuntimeState()
    conv = opened(state, "trg_002_compliance_dci_radiograph", body="Dr. Meera, DCI has new radiograph rules.")
    out = reply(seeds, state, "Ok lets do it. Whats next?", conv=conv)
    assert out["action"] == "send" and out["body"] == fake_llm.reply and out["cta"] == "binary_confirm_cancel"
    prompt = fake_llm.calls[0]
    assert "Vera: Dr. Meera, DCI has new radiograph rules." in prompt and "no qualifying questions" in prompt.lower()
    assert "Language for this reply: English" in prompt and "Our first message asked:" in prompt
    assert "Ask, one only" not in prompt and "Format:" not in prompt


def test_qualifying_question_after_yes_is_rejected(seeds, fake_llm):
    fake_llm.reply = "Great! Would you like me to draft it for weekdays or weekends?"
    state = RuntimeState()
    conv = opened(state, "trg_002_compliance_dci_radiograph")
    out = reply(seeds, state, "Ok lets do it", conv=conv)
    assert out["action"] == "send" and "would you" not in out["body"].lower()  # fixed wording instead


def test_invented_numbers_are_rejected(seeds, fake_llm):
    fake_llm.reply = "Done. This will bring you 37 new patients. Reply CONFIRM."
    state = RuntimeState()
    conv = opened(state, "trg_002_compliance_dci_radiograph")
    assert "37" not in reply(seeds, state, "Go ahead", conv=conv)["body"]


def test_hinglish_message_gets_a_hinglish_prompt(seeds, fake_llm):
    state = RuntimeState()
    conv = opened(state, "trg_021_unverified_gbp_sunrise", merchant="m_010_sunrisepharm_pharmacy_lucknow")
    reply(seeds, state, "Haan kar do, kitna time lagega?", conv=conv, merchant="m_010_sunrisepharm_pharmacy_lucknow")
    assert "Language for this reply: Hinglish" in fake_llm.calls[0]


def test_slow_ai_falls_back_in_time(seeds, fake_llm, monkeypatch):
    monkeypatch.setenv("VERA_REPLY_DEADLINE", "0.2")
    fake_llm.reply = lambda prompt: time.sleep(1) or "late reply"
    state = RuntimeState()
    conv = opened(state, "trg_002_compliance_dci_radiograph")
    start = time.monotonic()
    out = reply(seeds, state, "Go ahead", conv=conv)
    assert time.monotonic() - start < 0.9 and out["action"] == "send" and out["body"] != "late reply"


def test_offline_respond_contract(seeds):
    merchant, trigger = seeds.data("merchant", MEERA), seeds.data("trigger", "trg_002_compliance_dci_radiograph")
    category = seeds.data("category", merchant["category_slug"])
    state = {"category": category, "merchant": merchant, "trigger": trigger, "customer": None,
             "turns": [{"from": "vera", "body": "Dr. Meera, DCI has new radiograph rules. Want a checklist?"}]}
    out = respond(state, "Ok lets do it. Whats next?")
    assert out["action"] == "send" and out["body"] and out["rationale"]
    assert respond(state, "STOP")["action"] == "end"


def test_reply_endpoint_survives_an_internal_error(monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(bot, "handle_reply", boom)
    with TestClient(bot.app) as client:
        out = client.post("/v1/reply", json={"conversation_id": "c", "merchant_id": "m", "message": "hi"})
        client.post("/v1/teardown")
    assert out.status_code == 200 and out.json()["action"] == "wait"


def test_reused_draft_is_rejected_and_the_yes_goes_ahead_with_it(seeds, fake_llm):
    draft = "Here is a draft: Our clinic now follows the updated DCI radiograph safety rules for every patient."
    state = RuntimeState()
    conv = opened(state, "trg_002_compliance_dci_radiograph")
    state.record_outbound(conv, draft, now=NOW)
    fake_llm.reply = "Great. " + draft + " Reply CONFIRM to publish."
    out = reply(seeds, state, "Ok lets do it", conv=conv)
    assert out["action"] == "send" and "draft above" in out["body"]


def test_internal_jargon_is_rejected(seeds, fake_llm):
    fake_llm.reply = "The brief doesn't give a timeline, sorry."
    state = RuntimeState()
    conv = opened(state, "trg_002_compliance_dci_radiograph")
    assert "brief" not in reply(seeds, state, "How long will it take?", conv=conv)["body"]


def test_timing_negation_and_repeats_are_read_correctly():
    later = classify("Please go ahead tomorrow")
    assert later.kind == "commit" and later.detail["later"] == "tomorrow"
    assert classify("Not the first one", slot_labels=["5 Nov, 6pm", "6 Nov, 5pm"]).kind != "slot_pick"
    assert classify("What is the price for this plan?", repeats=2).kind == "question"  # a person re-asking


def test_go_ahead_tomorrow_confirms_the_timing(seeds):
    state = RuntimeState()
    conv = opened(state, "trg_002_compliance_dci_radiograph")
    out = reply(seeds, state, "Please go ahead tomorrow", conv=conv)
    assert out["action"] == "send" and "tomorrow" in out["body"]


def test_offline_respond_remembers_an_earlier_stop(seeds):
    merchant, trigger = seeds.data("merchant", MEERA), seeds.data("trigger", "trg_002_compliance_dci_radiograph")
    state = {"category": seeds.data("category", "dentists"), "merchant": merchant, "trigger": trigger, "customer": None,
             "turns": [{"from": "vera", "body": "Dr. Meera, DCI has new radiograph rules."},
                       {"from": "merchant", "body": "STOP"}]}
    assert respond(state, "ok")["action"] == "end"
