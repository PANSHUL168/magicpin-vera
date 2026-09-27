import pytest
from fastapi.testclient import TestClient

import bot
from vera.loader import iter_dataset


@pytest.fixture
def client():
    with TestClient(bot.app) as test_client:
        test_client.post("/v1/teardown")
        yield test_client
        test_client.post("/v1/teardown")


def push(client, scope="merchant", context_id="m_1", version=1, payload=None):
    return client.post("/v1/context", json={
        "scope": scope, "context_id": context_id, "version": version,
        "payload": payload if payload is not None else {"merchant_id": context_id},
        "delivered_at": "2026-04-26T10:00:00Z"})


def test_healthz_and_metadata(client):
    health = client.get("/v1/healthz").json()
    assert health["status"] == "ok"
    assert health["contexts_loaded"] == {"category": 0, "merchant": 0, "customer": 0, "trigger": 0}
    assert set(client.get("/v1/metadata").json()) == {
        "team_name", "team_members", "model", "approach", "contact_email", "version", "submitted_at"}


def test_context_status_codes(client):
    assert push(client).status_code == 200
    stale = push(client)
    assert stale.status_code == 409 and stale.json()["current_version"] == 1
    assert push(client, version=2).status_code == 200
    bad = client.post("/v1/context", json={"scope": "order", "context_id": "x", "version": 1, "payload": {}})
    assert bad.status_code == 400 and bad.json()["reason"] == "invalid_scope"
    broken = client.post("/v1/context", content=b"{not json", headers={"Content-Type": "application/json"})
    assert broken.status_code == 400 and broken.json()["reason"] == "invalid_json"
    assert client.get("/v1/healthz").json()["contexts_loaded"]["merchant"] == 1


def test_full_warmup_push_reports_255_contexts(client, expanded_dir):
    for scope, context_id, payload in iter_dataset(expanded_dir, scopes=("category", "merchant", "customer")):
        assert push(client, scope, context_id, 1, payload).status_code == 200, context_id
    assert client.get("/v1/healthz").json()["contexts_loaded"] == {
        "category": 5, "merchant": 50, "customer": 200, "trigger": 0}


def test_teardown_wipes_everything(client):
    push(client)
    client.post("/v1/reply", json={"conversation_id": "c1", "merchant_id": "m_1", "from_role": "merchant",
                                   "message": "hi", "received_at": "2026-04-26T10:45:00Z", "turn_number": 2})
    client.post("/v1/teardown")
    assert client.get("/v1/healthz").json()["contexts_loaded"]["merchant"] == 0
    assert bot.state.summary()["conversations"] == 0


REQUIRED_ACTION_FIELDS = {"conversation_id", "merchant_id", "customer_id", "send_as", "trigger_id", "template_name",
                          "template_params", "body", "cta", "suppression_key", "rationale"}


def test_tick_sends_one_message_per_recipient_then_holds_back(client, expanded_dir):
    for scope, context_id, payload in iter_dataset(expanded_dir):
        if scope != "trigger" or context_id in ("trg_001_research_digest_dentists",
                                                "trg_002_compliance_dci_radiograph", "trg_003_recall_due_priya"):
            assert push(client, scope, context_id, 1, payload).status_code == 200
    available = ["trg_001_research_digest_dentists", "trg_002_compliance_dci_radiograph", "trg_003_recall_due_priya"]
    actions = client.post("/v1/tick", json={"now": "2026-04-26T10:30:00Z", "available_triggers": available}).json()["actions"]
    assert [a["trigger_id"] for a in actions] == ["trg_002_compliance_dci_radiograph", "trg_003_recall_due_priya"]
    for action in actions:
        assert set(action) == REQUIRED_ACTION_FIELDS and action["body"]
    assert len({a["conversation_id"] for a in actions}) == 2
    assert actions[1]["send_as"] == "merchant_on_behalf" and actions[1]["customer_id"] == "c_001_priya_for_m001"
    # five minutes later: two already sent, and Meera was just messaged
    again = client.post("/v1/tick", json={"now": "2026-04-26T10:35:00Z", "available_triggers": available}).json()
    assert again == {"actions": []}


def test_tick_and_reply_with_unknown_ids_return_valid_shapes(client):
    tick = client.post("/v1/tick", json={"now": "2026-04-26T10:30:00Z", "available_triggers": ["trg_1"]})
    assert tick.json() == {"actions": []}
    reply = client.post("/v1/reply", json={"conversation_id": "conv_1", "merchant_id": "m_1",
                                           "from_role": "merchant", "message": "Yes please",
                                           "received_at": "2026-04-26T10:45:00Z", "turn_number": 2})
    assert reply.status_code == 200 and reply.json()["action"] in {"send", "wait", "end"}
    turns = bot.state.conversation("conv_1").turns
    assert [t.body for t in turns if t.sender == "merchant"] == ["Yes please"]
    if reply.json()["action"] == "send":
        assert turns[-1].sender == "bot" and turns[-1].body == reply.json()["body"]


def test_debug_routes_are_off_by_default(client):
    assert client.get("/debug/state").status_code == 404
