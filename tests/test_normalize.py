import pytest

from vera.normalize import (canonicalize, check_slot_label, detect_language, fmt_datetime,
                            fmt_indian_int, fmt_inr, fmt_pct, humanize, humanize_payload,
                            months_in_range, offer_key, parse_dt, parse_language_pref,
                            parse_person_name, parse_signal, parse_trend, signal_display,
                            split_honorific)


@pytest.mark.parametrize("value, expected", [
    (299, "299"), (2410, "2,410"), (124000, "1,24,000"), (10000000, "1,00,00,000"), (-4999, "-4,999")])
def test_indian_digit_grouping(value, expected):
    assert fmt_indian_int(value) == expected


def test_rupees():
    assert fmt_inr(4999) == "₹4,999"
    assert fmt_inr(1420.5) == "₹1,420.50"
    assert fmt_inr("free_for_members") == "free_for_members"


@pytest.mark.parametrize("fraction, kwargs, expected", [
    (0.021, {}, "2.1%"), (0.03, {}, "3%"), (0.38, {}, "38%"), (-0.5, {}, "-50%"), (-0.05, {}, "-5%"),
    (0.18, {"signed": True}, "+18%"), (0.03, {"decimals": 1}, "3.0%"), (0.0, {"signed": True}, "0%")])
def test_percentages_from_fractions(fraction, kwargs, expected):
    assert fmt_pct(fraction, **kwargs) == expected


@pytest.mark.parametrize("raw, name, value, unit", [
    ("stale_posts:22d", "stale_posts", 22, "d"),
    ("dormant_with_vera_14d", "dormant_with_vera", 14, "d"),
    ("engaged_in_last_48h", "engaged_in_last", 48, "h"),
    ("seasonal_dip_apr_may", "seasonal_dip_apr_may", None, None),
    ("ctr_below_peer_median", "ctr_below_peer_median", None, None)])
def test_both_signal_formats(raw, name, value, unit):
    signal = parse_signal(raw)
    assert (signal["name"], signal["value"], signal["unit"]) == (name, value, unit)


def test_signal_display_is_plain_words():
    assert signal_display(parse_signal("stale_posts:22d")) == "last Google post was 22 days ago"
    assert signal_display(parse_signal("some_new_flag_7d")) == "some new flag (7 days)"


def test_trend_strings_carry_whole_percents():
    trend = parse_trend("ORS_demand_+40")
    assert trend["delta"] == pytest.approx(0.4)
    assert trend["display"] == "ORS demand +40%"
    assert parse_trend("cold_cough_demand_-60")["display"] == "cold cough demand -60%"
    assert parse_trend("AT2024-1102") is None


@pytest.mark.parametrize("token, expected", [
    ("6_month_cleaning", "6-month cleaning"),
    ("skin_prep_program_30day", "30-day skin prep program"),
    ("post_resolution_window_apr_jun", "post resolution window Apr-Jun"),
    ("unverified_gbp", "unverified GBP"),
    ("chronic_rx_metformin", "chronic Rx metformin"),
    ("weekday_evening", "weekday evening"),
    ("7d", "7 days"),
    ("hi-en mix", "hi-en mix")])
def test_humanize(token, expected):
    assert humanize(token) == expected


def test_honorifics_are_split_off():
    assert split_honorific("Dr. Asha") == ("Dr.", "Asha")
    assert split_honorific("Meera") == (None, "Meera")
    assert split_honorific("Drishti") == (None, "Drishti")


def test_customer_name_forms():
    child = parse_person_name("Aanya (parent: Sneha)")
    assert (child["subject"], child["addressee"], child["relation"]) == ("Aanya", "Sneha", "parent")
    senior = parse_person_name("Mr. Sharma")
    assert (senior["honorific"], senior["bare_name"]) == ("Mr.", "Sharma")
    assert parse_person_name("(walk-in, no profile)")["anonymous"]


@pytest.mark.parametrize("pref, codes, mix", [
    ("hi-en mix", ["hi", "en"], True), ("english", ["en"], False), ("en", ["en"], False),
    ("hi", ["hi"], False), ("ta-en mix", ["ta", "en"], True)])
def test_language_preferences(pref, codes, mix):
    parsed = parse_language_pref(pref)
    assert (parsed["codes"], parsed["mix"]) == (codes, mix)


def test_detect_language():
    assert detect_language("Yes please, focus on whitening and aligners") == "en"
    assert detect_language("Mujhe magicpin judrna hai.") == "hi-en"
    assert detect_language("मुझे जुड़ना है") == "hi"


def test_parse_dt_handles_z_offsets_and_dates():
    assert parse_dt("2026-04-26T10:30:00Z").utcoffset().total_seconds() == 0
    assert parse_dt("2026-04-26T23:59:59+05:30") < parse_dt("2026-04-26T18:30:00Z")
    assert parse_dt("2026-11-12").utcoffset().total_seconds() == 5.5 * 3600  # Indian local date
    assert parse_dt("not a date") is None and parse_dt(None) is None


def test_fmt_datetime_uses_the_real_weekday():
    assert fmt_datetime("2026-04-26T19:30:00+05:30") == "Sun 26 Apr, 7:30pm"
    assert fmt_datetime("2026-04-28T00:00:00+05:30") == "Tue 28 Apr"


@pytest.mark.parametrize("label, months", [
    ("Nov-Feb", {11, 12, 1, 2}), ("Feb 14", {2}), ("Apr-Jun", {4, 5, 6}), ("Dec-Jan", {12, 1}), ("", set())])
def test_seasonal_month_ranges(label, months):
    assert months_in_range(label) == months


def test_offer_titles_match_loosely():
    assert offer_key("Senior Citizen 15% OFF (60+ age)") == offer_key("Senior Citizen 15% OFF")
    assert offer_key("Dental Cleaning @ ₹299") != offer_key("Deep Cleaning @ ₹499")


def test_slot_labels_with_wrong_weekdays_get_a_safe_label():
    bad = check_slot_label({"iso": "2026-11-05T18:00:00+05:30", "label": "Wed 5 Nov, 6pm"})
    assert (bad["weekday_ok"], bad["actual_weekday"], bad["safe_label"]) == (False, "Thu", "5 Nov, 6pm")
    good = check_slot_label({"iso": "2026-11-05T18:00:00+05:30", "label": "Thu 5 Nov, 6pm"})
    assert (good["weekday_ok"], good["safe_label"]) == (True, "Thu 5 Nov, 6pm")


def test_humanize_payload():
    shown = humanize_payload({
        "service_due": "6_month_cleaning", "delta_pct": -0.5, "renewal_amount": 4999,
        "top_item_id": "d_2026W17_jida_fluoride", "trends": ["ORS_demand_+40"],
        "match_time_iso": "2026-04-26T19:30:00+05:30", "due_date": "2026-11-12", "window": "7d",
        "distance_km": 1.3, "estimated_uplift_pct": 0.3, "is_weeknight": False})
    assert shown == {
        "service_due": "6-month cleaning", "delta_pct": "-50%", "renewal_amount": "₹4,999",
        "top_item_id": "d_2026W17_jida_fluoride", "trends": ["ORS demand +40%"],
        "match_time_iso": "Sun 26 Apr, 7:30pm", "due_date": "12 Nov 2026", "window": "7 days",
        "distance_km": "1.3 km", "estimated_uplift_pct": "+30%", "is_weeknight": False}


def test_canonicalize_accepts_the_briefs_field_names():
    data, warnings = canonicalize(
        "category", {"slug": "dentists", "voice": {"taboos": ["cure"]}, "peer_stats": {"avg_reviews": 62}}, "dentists")
    assert data["voice"]["vocab_taboo"] == ["cure"]
    assert data["peer_stats"]["avg_review_count"] == 62
    assert data["digest"] == [] and data["offer_catalog"] == []
    assert warnings


def test_canonicalize_trigger_reads_ids_from_payload():
    data, _ = canonicalize("trigger", {"kind": "perf_dip", "payload": {"merchant_id": "m_1"}}, "trg_x")
    assert (data["id"], data["merchant_id"], data["scope"], data["urgency"]) == ("trg_x", "m_1", "merchant", 1)
    assert data["suppression_key"] == "perf_dip:m_1:trg_x"


def test_canonicalize_coerces_wrong_types():
    data, warnings = canonicalize(
        "merchant", {"merchant_id": "m_1", "offers": "none", "identity": {"languages": "hi"}}, "m_1")
    assert data["offers"] == [] and data["identity"]["languages"] == ["hi"]
    assert data["performance"] == {"delta_7d": {}}
    assert warnings
