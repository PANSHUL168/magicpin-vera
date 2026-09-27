import json
import time

import pytest

from vera import llm, writer
from vera.bundle import build_bundle
from vera.compose import _draft, bundle_from_dicts, compose_bundle
from vera.factsheet import build_fact_sheet
from vera.loader import load_test_pairs
from vera.validator import fixes, problems, unsupported_services

BHARAT = "trg_004_perf_dip_bharat"
SUSHMA = "trg_031_perf_dip_m_023_sushma_salon_p"   # T25: a salon with no offers on file
GOOD = ("Dr. Bharat, calls fell 50% this week and your CTR is 1.8% vs 3.0% for similar clinics. "
        "Verifying your Google profile is the quickest fix. Kya main is hafte ke liye do quick fixes bhej doon?")


def sheet_for(store, trigger_id, now):
    return build_fact_sheet(build_bundle(store, trigger_id, now=now))


@pytest.fixture
def fake_llm(monkeypatch):
    """Answers from a list, one per call (the last one repeats)."""
    class Fake:
        replies: list = [GOOD]
        calls: list = []
        seconds: float = 0.01   # how long each fake call claims it took

    fake = Fake()
    fake.calls = []

    def complete_json(instructions, prompt, schema, *, name, max_output_tokens=1200):
        fake.calls.append(prompt)
        reply = fake.replies[min(len(fake.calls), len(fake.replies)) - 1]
        reply = reply(prompt) if callable(reply) else reply
        return llm.LLMResult({"body": reply, "rationale": f"attempt {len(fake.calls)}"}, "fake-model", 100, 50, 10,
                             fake.seconds)

    monkeypatch.setenv("VERA_LLM", "on")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(llm, "complete_json", complete_json)
    return fake


def test_services_the_business_doesnt_list_are_caught(loaded_store, brief_now):
    sheet = sheet_for(loaded_store, SUSHMA, brief_now)
    body = "Hi Sushma, calls are down. Highlight balayage, highlights ya keratin services. Kya main fixes bhej doon?"
    assert unsupported_services(body, sheet) == ["balayage", "highlights", "keratin"]
    assert "service words not in the brief: balayage, highlights, keratin" in problems(body, sheet)
    # trade words are fine, and so is a service the conversation already mentioned
    assert unsupported_services("More footfall this week.", sheet_for(loaded_store, BHARAT, brief_now)) == []
    assert unsupported_services("Keratin slots are open.", sheet, "Can we push keratin?") == []


@pytest.mark.parametrize("body, problem", [
    ("Hope you're doing well! Dr. Bharat, calls fell 50%. Kya main fixes bhej doon?", "preamble"),
    ("Hi Dr. Bharat, this is Vera. Calls fell 50%. Kya main fixes bhej doon?", "preamble"),
    ("Calls fell 50% this week. Kya main fixes bhej doon?", "doesn't address them by name"),
    ("Dr. Bharat, calls fell this week. Kya main fixes bhej doon?", "no concrete number"),
    ("Dr. Bharat, kya main fixes bhej doon? Calls fell 50%.", "doesn't end with the ask"),
    ("Dr. Bharat, calls fell 50%!! Huge drop! Kya main fixes bhej doon?", "too many exclamation marks"),
    ("Dr. Bharat, calls fell 50%; main do quick fixes bhej doon. Kya main do quick fixes bhej doon?", "repeats itself"),
])
def test_first_message_rules(loaded_store, brief_now, body, problem):
    sheet = sheet_for(loaded_store, BHARAT, brief_now)
    assert any(issue.startswith(problem) for issue in problems(body, sheet)), problems(body, sheet)
    assert problems(GOOD, sheet) == []


def test_customer_message_never_speaks_as_vera(loaded_store, brief_now):
    sheet = sheet_for(loaded_store, "trg_003_recall_due_priya", brief_now)
    body = "Hi Priya, Dr Meera's clinic here, with Vera. Your cleaning is due 12 Nov 2026. Reply 1 or 2."
    assert "customer message mentions Vera" in problems(body, sheet)


def test_replies_skip_the_first_message_rules(loaded_store, brief_now):
    sheet = sheet_for(loaded_store, BHARAT, brief_now)
    assert problems("Done, sending the checklist now.", sheet, mid_conversation=True) == []


def test_every_problem_gets_a_specific_fix(loaded_store, brief_now):
    sheet = sheet_for(loaded_store, SUSHMA, brief_now)
    lines = fixes(["numbers not in the brief: 37", "service words not in the brief: keratin",
                   "doesn't end with the ask"], sheet)
    assert lines[0].startswith("Remove 37") and "keratin" in lines[1] and sheet.ask["text_hi"] in lines[2]


def test_plain_drafts_always_pass(loaded_store, expanded_dir):
    """The fallback must be sendable: every canonical pair's plain draft passes the validator."""
    read = lambda *parts: json.loads(expanded_dir.joinpath(*parts).read_text(encoding="utf-8"))
    for pair in load_test_pairs(expanded_dir):
        merchant = read("merchants", f"{pair['merchant_id']}.json")
        customer = read("customers", f"{pair['customer_id']}.json") if pair.get("customer_id") else None
        sheet = build_fact_sheet(bundle_from_dicts(read("categories", f"{merchant['category_slug']}.json"), merchant,
                                                   read("triggers", f"{pair['trigger_id']}.json"), customer))
        assert problems(_draft(sheet)["body"], sheet) == [], pair["test_id"]


def test_a_rejected_message_is_retried_with_feedback(loaded_store, brief_now, fake_llm):
    bad = "Hi Sushma, calls are down. Push balayage and keratin. Kya main is hafte ke liye do quick fixes bhej doon?"
    fake_llm.replies = [bad, lambda prompt: prompt.split("Rewrite it:\n", 1)[1].split("\n\n")[0]]
    message, _ = compose_bundle(build_bundle(loaded_store, SUSHMA, now=brief_now))
    assert message["writer"] == "ai" and message["retried"] and "keratin" not in message["body"]
    assert message["rationale"] == "attempt 2"
    retry = fake_llm.calls[1]
    assert "Your previous version:\n" + bad in retry and "Don't mention balayage, keratin" in retry
    again, _ = compose_bundle(build_bundle(loaded_store, SUSHMA, now=brief_now))
    assert again["body"] == message["body"] and len(fake_llm.calls) == 2  # both attempts are cached


def test_a_saved_message_that_breaks_a_new_rule_is_retried(loaded_store, brief_now, fake_llm):
    """Cached results are checked again when read (how T25's saved message gets fixed)."""
    sheet = sheet_for(loaded_store, SUSHMA, brief_now)
    draft = _draft(sheet)
    key = writer.fingerprint(writer.build_prompt(sheet, draft))
    writer.CACHE.put(key, {"body": "Hi Sushma, try keratin offers. Kya main is hafte ke liye do quick fixes bhej doon?",
                           "rationale": "old", "rejected": []})
    fake_llm.replies = [draft["body"]]
    message, reason = writer.write_ai(sheet, draft)
    assert reason == "retried" and message["body"] == draft["body"] and len(fake_llm.calls) == 1


def test_no_retry_when_the_deadline_is_too_close(loaded_store, brief_now, fake_llm):
    fake_llm.replies = ["Dr. Bharat, 37 patients left. Kya main fixes bhej doon?"]
    fake_llm.seconds = 5.0  # a slow first call: another one wouldn't make a 3s deadline
    sheet = sheet_for(loaded_store, BHARAT, brief_now)
    message, reason = writer.write_ai(sheet, _draft(sheet), deadline=time.monotonic() + 3)
    assert message is None and "no time to retry" in reason and len(fake_llm.calls) == 1


def test_plan_drafts_may_propose_numbers_but_not_statistics(loaded_store, brief_now):
    sheet = sheet_for(loaded_store, "trg_013_corporate_thali_planning", brief_now)
    draft = ("Hi Suresh, starter version: 10+ thalis @ ₹139 each, order by 5pm the day before, delivery 12:30-1pm. "
             "CONFIRM reply kijiye, main ise final kar doongi, ya bataiye kya badalna hai.")
    assert not any(i.startswith("numbers not in the brief") for i in problems(draft, sheet))
    assert "numbers not in the brief: 40" in problems(draft.replace("starter version:", "offices order 40% more:"), sheet)
