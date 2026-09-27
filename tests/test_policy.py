from vera.bundle import build_bundle
from vera.policy import new_conversation_id, plan_tick
from vera.state import RuntimeState
from vera.store import ContextStore

MEERA = "m_001_drmeera_dentist_delhi"
RESEARCH, RULE_CHANGE, PRIYA_RECALL = ("trg_001_research_digest_dentists", "trg_002_compliance_dci_radiograph",
                                       "trg_003_recall_due_priya")


def reasons(plan):
    return {s["trigger_id"]: s["reason"] for s in plan.skipped}


def test_one_message_per_recipient_most_urgent_first(loaded_store, brief_now):
    # judge_simulator.py's phase2_short sends exactly these three
    plan = plan_tick(loaded_store, RuntimeState(), [RESEARCH, RULE_CHANGE, PRIYA_RECALL], now=brief_now)
    assert [b.trigger_id for b in plan.chosen] == [RULE_CHANGE, PRIYA_RECALL]  # Priya is a different person
    assert "ranked higher" in reasons(plan)[RESEARCH]


def test_recently_messaged_recipient_waits_for_a_later_tick(loaded_store, brief_now):
    state = RuntimeState()
    state.record_outbound("c1", "hello", merchant_id=MEERA, now=brief_now)
    soon = plan_tick(loaded_store, state, [RESEARCH], now="2026-04-26T10:40:00Z")
    assert not soon.chosen and "cooldown" in reasons(soon)[RESEARCH]
    later = plan_tick(loaded_store, state, [RESEARCH], now="2026-04-26T11:30:00Z")
    assert [b.trigger_id for b in later.chosen] == [RESEARCH]


def test_opted_out_already_sent_and_unknown_are_skipped(loaded_store, brief_now):
    state = RuntimeState()
    state.mark_opted_out(MEERA, reason="said stop")
    bharat_key = loaded_store.data("trigger", "trg_004_perf_dip_bharat")["suppression_key"]
    state.record_outbound("c2", "hi", merchant_id="m_002_bharat_dentist_mumbai", suppression_key=bharat_key,
                          now="2026-04-25T10:00:00Z")
    plan = plan_tick(loaded_store, state, [RESEARCH, "trg_004_perf_dip_bharat", "trg_nope"], now=brief_now)
    why = reasons(plan)
    assert not plan.chosen
    assert why[RESEARCH] == "recipient opted out"
    assert why["trg_004_perf_dip_bharat"].startswith("already sent")
    assert why["trg_nope"].startswith("unknown trigger")


def test_missing_context_waits(brief_now):
    store = ContextStore()
    store.ingest({"scope": "trigger", "context_id": "trg_x", "version": 1,
                  "payload": {"id": "trg_x", "kind": "perf_dip", "merchant_id": "m_1", "payload": {}}})
    plan = plan_tick(store, RuntimeState(), ["trg_x"], now=brief_now)
    assert not plan.chosen and reasons(plan)["trg_x"].startswith("waiting for data")


def test_limit_and_stable_ordering(loaded_store, brief_now):
    every = [r.context_id for r in loaded_store.records("trigger")]
    first = plan_tick(loaded_store, RuntimeState(), every, now=brief_now, limit=5)
    again = plan_tick(loaded_store, RuntimeState(), list(reversed(every)), now=brief_now, limit=5)
    assert len(first.chosen) == 5
    assert [b.trigger_id for b in first.chosen] == [b.trigger_id for b in again.chosen]
    urgencies = [b.trigger["urgency"] for b in first.chosen]
    assert urgencies == sorted(urgencies, reverse=True)
    assert len({(b.audience, b.trigger.get("customer_id") or b.trigger["merchant_id"]) for b in first.chosen}) == 5


def test_conversation_ids_are_readable_and_unique(loaded_store, brief_now):
    state = RuntimeState()
    bundle = build_bundle(loaded_store, PRIYA_RECALL, now=brief_now)
    first = new_conversation_id(state, bundle)
    state.record_outbound(first, "x", merchant_id=MEERA, customer_id="c_001_priya_for_m001")
    assert first == "conv_c_001_priya_for_m001_recall_due"
    assert new_conversation_id(state, bundle) == f"{first}_2"
