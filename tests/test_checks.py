from vera.bundle import build_bundle
from vera.checks import case_study_overlap, run_checks
from vera.factsheet import build_fact_sheet

# Case study 2 in examples/case-studies.md, verbatim
CASE_2 = ("Hi Priya, Dr. Meera's clinic here 🦷 It's been 5 months since your last visit — your 6-month cleaning "
          "recall is due. Apke liye 2 slots ready hain: Wed 5 Nov, 6pm ya Thu 6 Nov, 5pm. ₹299 cleaning + "
          "complimentary fluoride. Reply 1 for Wed, 2 for Thu, or tell us a time that works.")


def rows(body, store, trigger_id, now):
    sheet = build_fact_sheet(build_bundle(store, trigger_id, now=now))
    return {c.name: c for c in run_checks(body, sheet)}


def test_a_good_customer_message_passes(loaded_store, brief_now):
    body = ("Hi Priya, Dr. Meera's Dental Clinic here. Aapki 6-month cleaning 12 Nov 2026 tak due hai. "
            "5 Nov, 6pm ke liye 1 ya 6 Nov, 5pm ke liye 2 reply kijiye.")
    checks = rows(body, loaded_store, "trg_003_recall_due_priya", brief_now)
    assert all(c.ok is not False for c in checks.values()), [(c.name, c.detail) for c in checks.values() if c.ok is False]


def test_pure_english_for_a_hinglish_customer_is_flagged(loaded_store, brief_now):
    body = "Hi Priya, Dr. Meera's Dental Clinic here. Your cleaning is due by 12 Nov 2026. Reply 1 or 2."
    assert rows(body, loaded_store, "trg_003_recall_due_priya", brief_now)["Language as expected"].ok is False


def test_copying_a_case_study_is_caught(loaded_store, brief_now):
    share, name = case_study_overlap(CASE_2)
    assert share > 0.9 and name == "case study 2"
    assert rows(CASE_2, loaded_store, "trg_003_recall_due_priya", brief_now)["Not copied from a case study"].ok is False


def test_merchant_messages_skip_the_shop_name_rule(loaded_store, brief_now):
    checks = rows("Dr. Bharat, calls fell 50%. Want two fixes?", loaded_store, "trg_004_perf_dip_bharat", brief_now)
    assert checks["Customer message names the shop"].ok is None
