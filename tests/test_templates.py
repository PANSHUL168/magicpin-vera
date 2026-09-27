import re

from vera.bundle import build_bundle
from vera.factsheet import build_fact_sheet
from vera.normalize import number_tokens
from vera.templates import render

CODE = re.compile(r"\b[a-z0-9]+(?:_[a-z0-9]+)+\b")


def rendered(store, now):
    for record in store.records("trigger"):
        sheet = build_fact_sheet(build_bundle(store, record.context_id, now=now))
        yield sheet, render(sheet)


def test_every_plain_message_is_clean(loaded_store, brief_now):
    for sheet, message in rendered(loaded_store, brief_now):
        body = message["body"]
        where = f"{sheet.trigger_id}: {body}"
        assert body and "{" not in body and "  " not in body, where
        assert not CODE.search(body), where                     # no internal codes (judge: -1)
        assert "http" not in body.lower(), where                 # no links (api-call-examples F.4)
        assert "Dr. Dr." not in body, where
        assert number_tokens(body) <= set(sheet.allowed_numbers), (where, number_tokens(body) - set(sheet.allowed_numbers))
        assert not [t for t in sheet.avoid if t.lower() in body.lower()], where
        assert body.endswith(message["template_params"][3]), where   # the ask is the last sentence
        assert message["cta"] == sheet.ask["cta"] and message["rationale"]


def test_rendering_is_deterministic(loaded_store, brief_now):
    first = [message for _, message in rendered(loaded_store, brief_now)]
    assert first == [message for _, message in rendered(loaded_store, brief_now)]


def test_powerhouse_plain_message(loaded_store, brief_now):
    sheet = build_fact_sheet(build_bundle(loaded_store, "trg_014_seasonal_acquisition_dip_powerhouse", now=brief_now))
    body = render(sheet)["body"]
    assert body.startswith("Hi Karthik, your views are down 30% over the last 7 days, but that's the expected")
    assert "5.2% vs 4.5%" in body


def test_customer_message_opens_as_the_shop(loaded_store, brief_now):
    sheet = build_fact_sheet(build_bundle(loaded_store, "trg_003_recall_due_priya", now=brief_now))
    message = render(sheet)
    assert message["body"].startswith("Hi Priya, Dr. Meera's Dental Clinic here.")
    assert message["send_as"] == "merchant_on_behalf" and message["template_name"] == "merchant_recall_due_v1"
    assert len(message["template_params"]) == 4
