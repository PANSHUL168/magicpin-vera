import pytest

from vera.store import SCOPES, ContextStore


def envelope(scope="merchant", context_id="m_1", version=1, payload=None):
    return {"scope": scope, "context_id": context_id, "version": version,
            "payload": payload if payload is not None else {"merchant_id": context_id},
            "delivered_at": "2026-04-26T10:00:00Z"}


def test_first_push_is_accepted():
    status, body = ContextStore().ingest(envelope())
    assert status == 200
    assert body["accepted"] is True and body["ack_id"] == "ack_m_1_v1" and body["stored_at"].endswith("Z")


@pytest.mark.parametrize("second_version", [1, 0])
def test_same_or_lower_version_is_409(second_version):
    store = ContextStore()
    store.ingest(envelope(version=1))
    status, body = store.ingest(envelope(version=second_version))
    assert status == 409
    assert body == {"accepted": False, "reason": "stale_version", "current_version": 1}


def test_higher_version_replaces():
    store = ContextStore()
    store.ingest(envelope(payload={"merchant_id": "m_1", "performance": {"views": 2410}}))
    status, _ = store.ingest(envelope(version=2, payload={"merchant_id": "m_1", "performance": {"views": 2580}}))
    record = store.get("merchant", "m_1")
    assert status == 200 and record.version == 2 and record.data["performance"]["views"] == 2580
    assert record.changes["numbers"]["performance"]["views"] == {"from": 2410, "to": 2580}
    assert store.counts()["merchant"] == 1


def test_partial_update_keeps_omitted_keys():
    store = ContextStore()
    store.ingest(envelope("category", "dentists", payload={
        "slug": "dentists", "offer_catalog": [{"title": "Dental Cleaning @ ₹299"}], "digest": [{"id": "d1"}]}))
    store.ingest(envelope("category", "dentists", version=2, payload={
        "slug": "dentists", "digest": [{"id": "d1"}, {"id": "d2"}]}))
    record = store.get("category", "dentists")
    assert record.data["offer_catalog"] == [{"title": "Dental Cleaning @ ₹299"}]
    assert record.inherited_keys == ("offer_catalog",)
    assert record.item_first_seen["digest"] == {"id:d1": 1, "id:d2": 2}


def test_explicit_empty_value_replaces():
    store = ContextStore()
    store.ingest(envelope(payload={"merchant_id": "m_1", "offers": [{"id": "o1", "status": "active"}]}))
    store.ingest(envelope(version=2, payload={"merchant_id": "m_1", "offers": []}))
    assert store.data("merchant", "m_1")["offers"] == []


@pytest.mark.parametrize("bad, reason", [
    ([], "invalid_body"),
    (envelope(scope="order"), "invalid_scope"),
    (envelope(context_id="  "), "invalid_context_id"),
    (envelope(version=-1), "invalid_version"),
    (envelope(version="v2"), "invalid_version"),
    (envelope(version=True), "invalid_version"),
    (envelope(version=None), "invalid_version"),
    (envelope(payload=["x"]), "invalid_payload")])
def test_malformed_envelopes_are_400(bad, reason):
    status, body = ContextStore().ingest(bad)
    assert status == 400 and body["accepted"] is False and body["reason"] == reason


def test_numeric_string_version_is_accepted():
    status, body = ContextStore().ingest(envelope(version="3"))
    assert status == 200 and body["ack_id"] == "ack_m_1_v3"


def test_counts_and_wipe():
    store = ContextStore()
    store.ingest(envelope())
    store.ingest(envelope("category", "dentists", payload={"slug": "dentists"}))
    assert store.counts() == {"category": 1, "merchant": 1, "customer": 0, "trigger": 0}
    store.wipe()
    assert store.counts() == dict.fromkeys(SCOPES, 0)


def test_lookup_by_id_declared_in_payload():
    store = ContextStore()
    store.ingest(envelope(context_id="m_001_drmeera", payload={"merchant_id": "m_001_drmeera_dentist_delhi"}))
    assert store.get("merchant", "m_001_drmeera_dentist_delhi").context_id == "m_001_drmeera"


def test_stored_data_is_isolated_from_the_caller():
    payload = {"merchant_id": "m_1", "offers": [{"id": "o1", "status": "active"}]}
    store = ContextStore()
    store.ingest(envelope(payload=payload))
    payload["offers"][0]["status"] = "expired"
    assert store.data("merchant", "m_1")["offers"][0]["status"] == "active"


def test_changes_since_first_version_accumulate():
    store = ContextStore()
    store.ingest(envelope(payload={"merchant_id": "m_1", "performance": {"views": 100}, "offers": []}))
    store.ingest(envelope(version=2, payload={"merchant_id": "m_1", "performance": {"views": 150}, "offers": []}))
    store.ingest(envelope(version=3, payload={"merchant_id": "m_1", "performance": {"views": 150},
                                              "offers": [{"id": "o1", "status": "active"}]}))
    record = store.get("merchant", "m_1")
    assert record.changes["changed_keys"] == ["offers"]
    assert record.changes_since_base["numbers"]["performance"]["views"] == {"from": 100, "to": 150}
    assert record.changes_since_base["lists"]["offers"]["added"] == ["id:o1"]
