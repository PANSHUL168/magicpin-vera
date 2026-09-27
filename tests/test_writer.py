import asyncio
import time

import pytest

from vera import llm, writer
from vera.bundle import build_bundle
from vera.compose import compose, compose_bundle, compose_many
from vera.factsheet import build_fact_sheet

BHARAT = "trg_004_perf_dip_bharat"         # calls -50%, CTR 1.8% vs 3.0%, profile not verified
POWERHOUSE = "trg_014_seasonal_acquisition_dip_powerhouse"
GOOD = ("Dr. Bharat, calls fell 50% this week and your CTR is 1.8% vs 3.0% for similar clinics. "
        "Verifying your Google profile is the quickest fix. Kya main is hafte ke liye do quick fixes bhej doon?")


@pytest.fixture
def fake_llm(monkeypatch):
    """A stand-in model. Set .reply to a body, a callable(prompt) -> body, or an exception."""
    class Fake:
        reply: object = GOOD
        calls: list = []

    fake = Fake()
    fake.calls = []

    def complete_json(instructions, prompt, schema, *, name, max_output_tokens=1200):
        fake.calls.append(prompt)
        reply = fake.reply(prompt) if callable(fake.reply) else fake.reply
        if isinstance(reply, Exception):
            raise reply
        return llm.LLMResult({"body": reply, "rationale": "fake rationale"}, "fake-model", 100, 50, 10, 0.01)

    monkeypatch.setenv("VERA_LLM", "on")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(llm, "complete_json", complete_json)
    return fake


def bundle(store, trigger_id, now):
    return build_bundle(store, trigger_id, now=now)


def test_accepted_rewrite_keeps_the_contract_fields(loaded_store, brief_now, fake_llm):
    message, sheet = compose_bundle(bundle(loaded_store, BHARAT, brief_now))
    assert message["writer"] == "ai" and message["body"] == GOOD
    assert (message["cta"], message["send_as"], message["suppression_key"]) == (
        sheet.ask["cta"], "vera", sheet.suppression_key)
    assert message["rationale"] == "fake rationale"
    assert message["template_params"][-1].endswith("?")
    prompt = fake_llm.calls[0]
    assert "Why now:" in prompt and "Plain draft" in prompt  # the brief and the draft both go to the model


def test_invented_number_is_retried_once_then_falls_back(loaded_store, brief_now, fake_llm):
    fake_llm.reply = "Dr. Bharat, calls fell 50% and 37 patients went elsewhere. Kya main fixes bhej doon?"
    first, _ = compose_bundle(bundle(loaded_store, BHARAT, brief_now))
    again, _ = compose_bundle(bundle(loaded_store, BHARAT, brief_now))
    assert first["writer"] == "template" and again["writer"] == "template"
    assert len(fake_llm.calls) == 2  # one retry; both rejections are remembered, so reruns spend nothing
    assert "Remove 37" in fake_llm.calls[1]


@pytest.mark.parametrize("body, problem", [
    ("Dr. Bharat, details at https://example.com. Want them?", "link"),
    ("Dr. Bharat, this is guaranteed to fix it. Want it?", "taboo"),
    ("Dr. Bharat, calls fell 50%. Seen it? Want fixes?", "more than one question"),
    ("Dr. Bharat, your perf_dip needs work. Want fixes?", "internal code"),
    ("   ", "empty"),
])
def test_safety_check_catches_problems(loaded_store, brief_now, body, problem):
    sheet = build_fact_sheet(bundle(loaded_store, BHARAT, brief_now))
    assert any(problem in issue for issue in writer.problems(body, sheet))
    assert writer.problems(GOOD, sheet) == []


def test_customer_message_must_name_the_shop(loaded_store, brief_now):
    sheet = build_fact_sheet(bundle(loaded_store, "trg_003_recall_due_priya", brief_now))
    assert "doesn't say which shop is writing" in writer.problems("Hi Priya, your cleaning is due. Reply 1 or 2.", sheet)
    assert writer.problems("Hi Priya, Dr Meera's clinic here. Your cleaning is due. Reply 1 or 2.", sheet) == []


def test_api_errors_fall_back_to_the_plain_draft(loaded_store, brief_now, fake_llm):
    fake_llm.reply = llm.LLMError("APITimeoutError: timed out")
    message, _ = compose_bundle(bundle(loaded_store, BHARAT, brief_now))
    assert message["writer"] == "template"


def test_same_brief_is_answered_once(loaded_store, brief_now, fake_llm):
    first, _ = compose_bundle(bundle(loaded_store, BHARAT, brief_now))
    second, _ = compose_bundle(bundle(loaded_store, BHARAT, brief_now))
    assert first["body"] == second["body"] == GOOD and len(fake_llm.calls) == 1


def test_off_switch_never_calls_the_model(loaded_store, brief_now, fake_llm, monkeypatch):
    monkeypatch.setenv("VERA_LLM", "off")
    message, _ = compose_bundle(bundle(loaded_store, BHARAT, brief_now))
    assert message["writer"] == "template" and fake_llm.calls == []


def test_parallel_writing_sends_the_plain_draft_when_the_ai_is_late(loaded_store, brief_now, fake_llm):
    def slow(prompt):  # answers with the plain draft itself, which passes every check
        time.sleep(0.5)
        return prompt.split("Rewrite it:\n", 1)[1].split("\n\n")[0]
    fake_llm.reply = slow
    bundles = [bundle(loaded_store, BHARAT, brief_now), bundle(loaded_store, POWERHOUSE, brief_now)]
    late = asyncio.run(compose_many(bundles, deadline=0.1))
    assert [m["writer"] for m, _ in late] == ["template", "template"]
    writer.CACHE.clear()
    on_time = asyncio.run(compose_many(bundles, deadline=5))
    assert [m["writer"] for m, _ in on_time] == ["ai", "ai"]


def test_offline_compose_reuses_saved_results(expanded_dir, fake_llm, tmp_path):
    import json
    read = lambda *parts: json.loads(expanded_dir.joinpath(*parts).read_text(encoding="utf-8"))
    args = (read("categories", "dentists.json"), read("merchants", "m_002_bharat_dentist_mumbai.json"),
            read("triggers", f"{BHARAT}.json"), None)
    first = compose(*args)
    writer.CACHE.clear()  # simulate a fresh process: only the file remains
    second = compose(*args)
    assert first == second and first["body"] == GOOD and len(fake_llm.calls) == 1
    assert (tmp_path / "ai_messages.json").exists()


def test_llm_needs_a_key(monkeypatch):
    monkeypatch.setenv("VERA_LLM", "on")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert not llm.enabled()
    with pytest.raises(llm.LLMError):
        llm.complete_json("x", "y", writer.SCHEMA, name="t")
