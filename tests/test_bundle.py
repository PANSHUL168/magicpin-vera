import copy
import re

import pytest

from vera.bundle import build_bundle
from vera.derive import merchant_greeting
from vera.loader import load_dataset, load_test_pairs
from vera.state import RuntimeState
from vera.store import ContextStore

MEERA = "m_001_drmeera_dentist_delhi"


def test_every_trigger_builds_with_no_missing_references(loaded_store, brief_now):
    for record in loaded_store.records("trigger"):
        bundle = build_bundle(loaded_store, record.context_id, now=brief_now)
        assert bundle is not None and bundle.missing == [], record.context_id


@pytest.mark.parametrize("trigger_id, ref_key, item_id", [
    ("trg_001_research_digest_dentists", "top_item_id", "d_2026W17_jida_fluoride"),
    ("trg_018_supply_atorvastatin_recall", "alert_id", "d_2026W17_atorvastatin_recall"),
    ("trg_022_cde_webinar_dentists", "digest_item_id", "d_2026W17_ida_webinar")])
def test_digest_references_resolve_under_all_three_keys(loaded_store, brief_now, trigger_id, ref_key, item_id):
    bundle = build_bundle(loaded_store, trigger_id, now=brief_now)
    assert [(d["ref_key"], d["id"]) for d in bundle.digest_items] == [(ref_key, item_id)]
    assert bundle.digest_items[0]["item"]["title"]


def test_meera_research_digest_bundle(loaded_store, brief_now):
    bundle = build_bundle(loaded_store, "trg_001_research_digest_dentists", now=brief_now)
    assert (bundle.audience, bundle.send_as) == ("merchant", "vera")
    assert bundle.fact("ctr_vs_peer").display == "CTR 2.1% vs 3.0% peer average, 30% below peers"
    assert bundle.fact("views_vs_peer").value["position"] == "above"
    assert bundle.fact("high_risk_adult_count").display == "124 high-risk adult patients"
    untried = bundle.fact("catalog_offers_not_run").value
    assert "Teeth Whitening @ ₹1,499" in untried and "Dental Cleaning @ ₹299" not in untried
    assert (bundle.language["address_as"], bundle.language["style"]) == ("Dr. Meera", "hi-en")
    assert bundle.history["open_requests"][0]["message"] == "Yes please, focus on whitening and aligners"
    assert bundle.has("open_merchant_request")


def test_no_snake_case_codes_in_any_fact_display(loaded_store, brief_now):
    code = re.compile(r"\b[a-z0-9]+(?:_[a-z0-9]+)+\b")
    for record in loaded_store.records("trigger"):
        for fact in build_bundle(loaded_store, record.context_id, now=brief_now).facts:
            assert not code.search(fact.display), (record.context_id, fact.key, fact.display)


def test_greetings_never_double_the_title(loaded_store):
    for record in loaded_store.records("merchant"):
        category = loaded_store.data("category", record.data["category_slug"])
        greeting = merchant_greeting(record.data, category)
        assert "Dr. Dr." not in greeting["greeting"], record.context_id
        if record.data["category_slug"] == "dentists":
            assert greeting["address_as"].startswith("Dr. "), record.context_id


def test_priya_recall_bundle(loaded_store, brief_now):
    bundle = build_bundle(loaded_store, "trg_003_recall_due_priya", now=brief_now)
    assert bundle.send_as == "merchant_on_behalf" and bundle.consent["ok"]
    assert (bundle.language["greeting"], bundle.language["style"]) == ("Hi Priya", "hi-en")
    assert [s["safe_label"] for s in bundle.slots] == ["5 Nov, 6pm", "6 Nov, 5pm"]
    assert {"time_inconsistent", "slot_weekday_mismatch"} <= set(bundle.flags)
    assert not bundle.has("open_merchant_request")  # the merchant's pending ask is irrelevant to Priya
    assert bundle.fact("customer_days_since_last_visit") is None  # last visit is after `now`


def test_canonical_test_pair_problems(loaded_store, expanded_dir, brief_now):
    pairs = load_test_pairs(expanded_dir)
    flagged = {name: set() for name in ("placeholder_payload", "consent_gap", "state_conflict")}
    for pair in pairs:
        bundle = build_bundle(loaded_store, pair["trigger_id"], now=brief_now)
        for name in flagged:
            if bundle.has(name):
                flagged[name].add(pair["test_id"])
    assert len(pairs) == 30
    assert len(flagged["placeholder_payload"]) == 13
    assert flagged["consent_gap"] == {"T03", "T04", "T08", "T29"}
    assert flagged["state_conflict"] == {"T14", "T15"}


def test_sparse_generated_merchant_still_has_anchors(loaded_store, expanded_dir, brief_now):
    pair = next(p for p in load_test_pairs(expanded_dir) if p["test_id"] == "T25")  # perf_dip, generated salon
    bundle = build_bundle(loaded_store, pair["trigger_id"], now=brief_now)
    assert bundle.richness["level"] == "sparse"
    assert {"placeholder_payload", "sparse_merchant"} <= set(bundle.flags)
    assert bundle.fact("ctr_vs_peer") is not None


def test_expiry_follows_the_reference_time(loaded_store, monkeypatch):
    trigger = "trg_001_research_digest_dentists"
    assert not build_bundle(loaded_store, trigger, now="2026-04-26T10:30:00Z").has("expired")
    assert build_bundle(loaded_store, trigger, now="2026-09-26T12:00:00Z").has("expired")
    monkeypatch.setenv("VERA_REFERENCE_NOW", "2026-04-26T10:30:00Z")
    bundle = build_bundle(loaded_store, trigger, now="2026-09-26T12:00:00Z")
    assert bundle.now_source == "override" and not bundle.has("expired")


def test_24h_window_after_a_merchant_reply(loaded_store):
    trigger = "trg_013_corporate_thali_planning"  # Mylari replied 2026-04-25T11:30Z
    assert build_bundle(loaded_store, trigger, now="2026-04-26T10:30:00Z").history["session_window_open"]
    assert not build_bundle(loaded_store, trigger, now="2026-04-28T10:30:00Z").history["session_window_open"]


def test_references_resolve_in_any_push_order(brief_now):
    store = ContextStore()
    store.ingest({"scope": "trigger", "context_id": "trg_x", "version": 1,
                  "payload": {"id": "trg_x", "kind": "perf_dip", "merchant_id": "m_1", "payload": {}}})
    bundle = build_bundle(store, "trg_x", now=brief_now)
    assert bundle.missing == ["merchant:m_1"] and bundle.has("incomplete")
    store.ingest({"scope": "merchant", "context_id": "m_1", "version": 1,
                  "payload": {"merchant_id": "m_1", "category_slug": "dentists"}})
    assert build_bundle(store, "trg_x", now=brief_now).missing == ["category:dentists"]


def test_digest_item_pushed_mid_test_is_fresh(expanded_dir, brief_now):
    store = ContextStore()
    load_dataset(store, expanded_dir)
    dentists = copy.deepcopy(store.get("category", "dentists").payload)
    dentists["digest"].append({"id": "d_new_radiograph", "kind": "compliance",
                               "title": "DCI revised radiograph dose limits", "source": "DCI circular 2026-11-04"})
    store.ingest({"scope": "category", "context_id": "dentists", "version": 2, "payload": dentists})
    store.ingest({"scope": "trigger", "context_id": "trg_new", "version": 1, "payload": {
        "id": "trg_new", "kind": "regulation_change", "merchant_id": MEERA,
        "payload": {"top_item_id": "d_new_radiograph"}}})
    bundle = build_bundle(store, "trg_new", now=brief_now)
    assert bundle.digest_items[0]["fresh"] is True
    assert bundle.fresh["new_digest_items"] == ["d_new_radiograph"]


def test_runtime_state_feeds_history_and_flags(loaded_store, brief_now):
    state = RuntimeState()
    state.record_outbound("conv_1", "Drafts for whitening and aligners are ready.", merchant_id=MEERA,
                          suppression_key="research:dentists:2026-W17", now=brief_now)
    state.mark_opted_out(MEERA, reason="said stop")
    bundle = build_bundle(loaded_store, "trg_001_research_digest_dentists", now=brief_now, state=state)
    assert {"opted_out", "suppression_key_used"} <= set(bundle.flags)
    assert bundle.history["last_vera_message"]["origin"] == "live"
    assert bundle.history["unanswered_streak"] == 1
    assert not bundle.has("open_merchant_request")  # our live turn answered it
