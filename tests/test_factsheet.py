import pytest

from vera.bundle import build_bundle
from vera.factsheet import CTA_LABELS, FAMILIES, KIND_FAMILY, build_fact_sheet
from vera.loader import load_dataset, load_test_pairs
from vera.normalize import number_tokens
from vera.store import ContextStore


def sheet_for(store, trigger_id, now):
    return build_fact_sheet(build_bundle(store, trigger_id, now=now))


def pair_sheet(store, expanded_dir, test_id, now):
    pair = next(p for p in load_test_pairs(expanded_dir) if p["test_id"] == test_id)
    return sheet_for(store, pair["trigger_id"], now)


def all_sheets(store, now):
    return [sheet_for(store, r.context_id, now) for r in store.records("trigger")]


def test_every_dataset_kind_has_a_family(loaded_store):
    kinds = {r.data["kind"] for r in loaded_store.records("trigger")}
    assert len(kinds) == 26
    assert kinds <= set(KIND_FAMILY)
    assert sum(len(k) for k in FAMILIES.values()) == 26


def test_every_trigger_gets_a_complete_sheet(loaded_store, brief_now):
    for sheet in all_sheets(loaded_store, brief_now):
        assert sheet.lead.text and sheet.lead.source and sheet.lead.key, sheet.trigger_id
        assert len(sheet.support) <= 3
        assert sheet.audience == "customer" or sheet.support, sheet.trigger_id
        assert all(line.text and line.source and line.key for line in sheet.support)
        assert sheet.ask["cta"] in CTA_LABELS and sheet.ask["text"]
        assert sheet.greeting and sheet.suppression_key


def test_allowed_numbers_cover_everything_the_sheet_says(loaded_store, brief_now):
    for sheet in all_sheets(loaded_store, brief_now):
        said = set()
        for line in [sheet.lead, *sheet.support]:
            said |= number_tokens(line.text) | number_tokens(line.phrase) | number_tokens(line.phrase_hi)
        assert said <= set(sheet.allowed_numbers), (sheet.trigger_id, said - set(sheet.allowed_numbers))


def test_powerhouse_seasonal_dip(loaded_store, brief_now):
    sheet = sheet_for(loaded_store, "trg_014_seasonal_acquisition_dip_powerhouse", brief_now)
    assert (sheet.family, sheet.send_as, sheet.greeting) == ("performance", "vera", "Hi Karthik")
    assert "-30%" in sheet.lead.text and "expected seasonal dip" in sheet.lead.text
    keys = [line.key for line in sheet.support]
    assert keys[0].startswith("season_") and "ctr_vs_peer" in keys
    assert sheet.language["instruction"].startswith("Mostly English")  # gyms: English first, some Hindi
    assert sheet.template["required"]  # no chat in the last 24 hours
    assert sheet.ask["cta"] == "binary_yes_no"


def test_research_digest_uses_the_named_item_and_its_cohort(loaded_store, brief_now):
    sheet = sheet_for(loaded_store, "trg_001_research_digest_dentists", brief_now)
    assert "JIDA Oct 2026, p.14" in sheet.lead.text and "2,100-patient trial" in sheet.lead.text
    assert "124 high-risk adult patients" in [line.text for line in sheet.support]
    assert {"2100", "38", "124"} <= set(sheet.allowed_numbers)
    assert not any("whitening" in rule for rule in sheet.instructions)  # old requests stay out of unrelated messages
    assert "guaranteed" in sheet.avoid


def test_priya_recall_is_customer_facing_with_safe_slots(loaded_store, brief_now):
    sheet = sheet_for(loaded_store, "trg_003_recall_due_priya", brief_now)
    assert (sheet.send_as, sheet.ask["cta"], sheet.recipient_id) == (
        "merchant_on_behalf", "multi_choice_slot", "c_001_priya_for_m001")
    assert "5 Nov, 6pm" in sheet.ask["text"] and "Wed" not in sheet.ask["text"]
    assert sheet.language["hinglish"]
    assert any("don't say how long ago" in rule for rule in sheet.instructions)


def test_placeholder_trigger_invents_no_event_details(loaded_store, expanded_dir, brief_now):
    sheet = pair_sheet(loaded_store, expanded_dir, "T19", brief_now)  # festival, no details
    assert sheet.lead.key == "payload:kind"
    assert "Diwali" not in sheet.to_prompt()
    assert any("gives no details" in rule for rule in sheet.instructions)


def test_consent_for_promotions_only_frames_it_as_an_offer(loaded_store, expanded_dir, brief_now):
    sheet = pair_sheet(loaded_store, expanded_dir, "T29", brief_now)  # recall, consent: promotional offers
    assert sheet.lead.key == "offer:first"
    assert any("frame this as an offer" in rule for rule in sheet.instructions)


def test_state_conflict_never_claims_they_have_been_away(loaded_store, expanded_dir, brief_now):
    sheet = pair_sheet(loaded_store, expanded_dir, "T14", brief_now)  # "lapsed" trigger, churned record
    assert sheet.lead.phrase == "a quick note from us"
    assert any("don't mention how long" in rule for rule in sheet.instructions)


def test_kind_that_doesnt_fit_the_business(loaded_store, expanded_dir, brief_now):
    sheet = pair_sheet(loaded_store, expanded_dir, "T08", brief_now)  # medicine refill at a dental clinic
    assert "medicine" not in sheet.lead.phrase
    assert any("doesn't fit" in note for note in sheet.notes)


def test_festival_uses_the_seasonal_note_for_its_own_month(loaded_store, brief_now):
    sheet = sheet_for(loaded_store, "trg_006_festival_diwali", brief_now)
    assert sheet.support[0].key == "season:Oct-Dec"


def test_ipl_brings_in_match_day_order_data(loaded_store, brief_now):
    sheet = sheet_for(loaded_store, "trg_010_ipl_match_delhi", brief_now)
    assert "digest:d_2026W17_ipl_window" in [line.key for line in sheet.support]


def test_dormant_merchant_gets_something_useful_not_a_guilt_trip(loaded_store, brief_now):
    sheet = sheet_for(loaded_store, "trg_025_dormancy_glamour", brief_now)
    assert "38" not in sheet.lead.phrase and sheet.lead.key.startswith("digest:")
    assert any("Don't reopen the last topic" in rule for rule in sheet.instructions)
    assert "Keratin" in " ".join(line.text for line in sheet.support)  # offer idea matches the trend


def test_prompt_carries_the_rules(loaded_store, brief_now):
    prompt = sheet_for(loaded_store, "trg_014_seasonal_acquisition_dip_powerhouse", brief_now).to_prompt()
    for part in ("Why now:", "Supporting facts (use only these):", "Numbers may only come from:", "Never use:"):
        assert part in prompt


def test_unknown_kind_falls_back_to_the_general_recipe(expanded_dir, brief_now):
    store = ContextStore()
    load_dataset(store, expanded_dir, scopes=("category", "merchant"))
    store.ingest({"scope": "trigger", "context_id": "trg_heat", "version": 1, "payload": {
        "id": "trg_heat", "kind": "weather_heatwave", "merchant_id": "m_001_drmeera_dentist_delhi",
        "payload": {"temperature_c": 42, "city": "Delhi"}}})
    sheet = sheet_for(store, "trg_heat", brief_now)
    assert sheet.family == "general"
    assert "42" in sheet.allowed_numbers and "Delhi" in sheet.lead.text


@pytest.mark.parametrize("trigger_id", ["trg_001_research_digest_dentists", "trg_003_recall_due_priya"])
def test_sheets_are_deterministic(loaded_store, brief_now, trigger_id):
    assert sheet_for(loaded_store, trigger_id, brief_now) == sheet_for(loaded_store, trigger_id, brief_now)
