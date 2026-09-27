from vera.state import RuntimeState

AUTO_REPLY = "Thank you for contacting us! Our team will respond shortly."


def test_auto_reply_repeats_are_counted_per_party_across_conversations():
    # judge_simulator.py's auto_reply_hell uses a new conversation_id every turn
    state = RuntimeState()
    counts = [state.record_inbound(f"conv_auto_{i}", AUTO_REPLY, merchant_id="m_1")[1] for i in range(1, 5)]
    assert counts == [1, 2, 3, 4]
    assert state.conversation("conv_auto_1").opened_by == "judge"


def test_repeat_detection_ignores_case_and_punctuation():
    state = RuntimeState()
    state.record_inbound("c1", "Thank you for contacting us!", merchant_id="m_1")
    assert state.record_inbound("c2", "thank you for contacting us", merchant_id="m_1")[1] == 2


def test_outbound_ledgers():
    state = RuntimeState()
    body = "Dr. Meera, JIDA's Oct issue landed."
    state.record_outbound("c1", body, merchant_id="m_1", suppression_key="research:dentists:W17",
                          now="2026-04-26T10:30:00Z")
    assert state.already_sent("c1", "dr meera, jida's oct issue landed")
    assert not state.already_sent("c2", body)
    assert state.sent_to_party_before("m_1", body)
    assert state.is_suppressed("research:dentists:W17") and not state.is_suppressed("other")
    assert state.party("m_1").unanswered_outbound == 1


def test_real_reply_resets_unanswered_and_opens_the_window():
    state = RuntimeState()
    state.record_outbound("c1", "hi", merchant_id="m_1", now="2026-04-26T10:00:00Z")
    state.record_inbound("c1", "yes", merchant_id="m_1", now="2026-04-26T10:05:00Z")
    assert state.party("m_1").unanswered_outbound == 1  # not a reply until mark_replied()
    state.mark_replied("m_1", now="2026-04-26T10:05:00Z")
    assert state.party("m_1").unanswered_outbound == 0
    assert state.session_window_open("m_1", "2026-04-27T10:04:00Z")
    assert not state.session_window_open("m_1", "2026-04-27T10:06:00Z")


def test_conversation_lifecycle():
    state = RuntimeState()
    state.record_outbound("c1", "hi", merchant_id="m_1")
    state.set_waiting("c1", until="2026-04-26T14:00:00Z")
    assert state.conversation("c1").status == "waiting"
    state.record_outbound("c1", "following up", merchant_id="m_1")
    assert state.conversation("c1").status == "open"
    state.end_conversation("c1", reason="not interested")
    state.set_waiting("c1", until="2026-04-26T15:00:00Z")
    assert state.conversation("c1").status == "ended"


def test_customer_conversations_stay_out_of_merchant_history():
    state = RuntimeState()
    state.record_outbound("c_merchant", "to merchant", merchant_id="m_1")
    state.record_outbound("c_customer", "to customer", merchant_id="m_1", customer_id="c_9")
    assert [t.body for t in state.turns_for_merchant("m_1")] == ["to merchant"]
    assert state.party("c_9").role == "customer"


def test_opt_out_and_wipe():
    state = RuntimeState()
    state.mark_opted_out("m_1", reason="stop")
    assert state.is_opted_out("m_1")
    state.wipe()
    assert not state.is_opted_out("m_1") and state.summary()["conversations"] == 0
