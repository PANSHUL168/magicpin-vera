# T14 · customer_lapsed_soft → Reyansh (Asha Dental Care)

**Final message** (sent as `merchant_on_behalf`, written by **ai**, ask type `binary_yes_no`):

> Hi Reyansh, Asha Dental Care here. We wanted to check in and thank you for your 5 visits since 1 Sep 2025. We’d be happy to welcome you back whenever it suits you. Reply YES and we'll book a time that suits you.

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_071_customer_lapsed_soft_m_014_dr_asha_dentis`

```json
{
  "id": "trg_071_customer_lapsed_soft_m_014_dr_asha_dentis",
  "scope": "customer",
  "kind": "customer_lapsed_soft",
  "source": "internal",
  "merchant_id": "m_014_dr_asha_dentist_chandigarh",
  "customer_id": "c_055_reyansh_for_m_014_dr_asha_dentist_chandigarh",
  "payload": {
    "placeholder": true,
    "metric_or_topic": "customer_lapsed_soft"
  },
  "urgency": 3,
  "suppression_key": "customer_lapsed_soft:m_014_dr_asha_dentist_chandigarh:gen_71",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_014_dr_asha_dentist_chandigarh</code> (full record)</summary>

```json
{
  "merchant_id": "m_014_dr_asha_dentist_chandigarh",
  "category_slug": "dentists",
  "identity": {
    "name": "Asha Dental Care",
    "city": "Chandigarh",
    "locality": "Sector 17",
    "place_id": "ChIJ_SECTOR_17_DENTISTS_014",
    "verified": false,
    "languages": [
      "en",
      "hi"
    ],
    "owner_first_name": "Dr. Asha",
    "established_year": 2023
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 97,
    "days_since_expiry": null
  },
  "performance": {
    "window_days": 30,
    "views": 3722,
    "calls": 33,
    "directions": 96,
    "ctr": 0.029,
    "leads": 31,
    "delta_7d": {
      "views_pct": -0.22,
      "calls_pct": -0.26
    }
  },
  "offers": [],
  "conversation_history": [],
  "customer_aggregate": {
    "total_unique_ytd": 88
  },
  "signals": [],
  "review_themes": []
}
```

</details>

<details><summary>Category <code>dentists</code> (key fields)</summary>

```json
{
  "slug": "dentists",
  "voice": {
    "tone": "peer_clinical",
    "register": "respectful_collegial",
    "code_mix": "hindi_english_natural",
    "vocab_allowed": [
      "fluoride varnish",
      "scaling",
      "caries",
      "occlusion",
      "bruxism",
      "endodontic",
      "periodontal",
      "implant",
      "aligner",
      "veneer",
      "OPG",
      "IOPA",
      "RCT",
      "CAD/CAM",
      "zirconia",
      "PFM"
    ],
    "vocab_taboo": [
      "guaranteed",
      "100% safe",
      "completely cure",
      "miracle",
      "best in city",
      "doctor approved",
      "FDA-approved (use only when actually applicable)"
    ],
    "salutation_examples": [
      "Dr. {first_name}",
      "Doc"
    ],
    "tone_examples": [
      "Worth a look — JIDA Oct 2026 p.14",
      "This one likely affects your high-risk adult cohort",
      "If your case-mix is mostly cosmetic, may not be relevant"
    ]
  },
  "peer_stats": {
    "scope": "metro_solo_practices_2026",
    "avg_rating": 4.4,
    "avg_review_count": 62,
    "avg_views_30d": 1820,
    "avg_calls_30d": 12,
    "avg_directions_30d": 38,
    "avg_ctr": 0.03,
    "avg_photos": 9,
    "avg_post_freq_days": 14,
    "retention_6mo_pct": 0.42
  },
  "offer_catalog": [
    "Dental Cleaning @ ₹299",
    "Free Consultation",
    "Teeth Whitening @ ₹1,499",
    "Root Canal @ ₹2,999 (single rooted)",
    "Free Smile Analysis + Digital Scan",
    "Aligner Consultation @ ₹499",
    "Pediatric Dental Checkup @ ₹199",
    "Annual Family Dental Plan @ ₹4,999"
  ],
  "digest (titles)": [
    "3-month fluoride varnish recall outperforms 6-month for high-risk adult caries",
    "DCI revised radiograph dose limits effective 2026-12-15",
    "IDA Delhi: Digital impressions — 2026 state of the art",
    "Clear aligner consultations searches +62% YoY in metros",
    "Dentsply launches IPS e.max Press for zirconia crowns in India at ₹3,200/unit (Delhi labs)"
  ],
  "seasonal_beats": [
    {
      "month_range": "Nov-Feb",
      "note": "exam-stress bruxism spike — ortho consults rise 30% in 18-24 cohort"
    },
    {
      "month_range": "Oct-Dec",
      "note": "wedding whitening peak — bookings 2x baseline; ladies' segment dominant"
    },
    {
      "month_range": "Jan",
      "note": "new-year resolution surge — annual check-up bookings +40%"
    },
    {
      "month_range": "Apr-Jun",
      "note": "school holiday window — pediatric appointments +50%"
    }
  ]
}
```

</details>

<details><summary>Customer <code>c_055_reyansh_for_m_014_dr_asha_dentist_chandigarh</code></summary>

```json
{
  "customer_id": "c_055_reyansh_for_m_014_dr_asha_dentist_chandigarh",
  "merchant_id": "m_014_dr_asha_dentist_chandigarh",
  "identity": {
    "name": "Reyansh",
    "phone_redacted": "<phone>",
    "language_pref": "en",
    "age_band": "25-35"
  },
  "relationship": {
    "first_visit": "2025-09-01",
    "last_visit": "2026-04-01",
    "visits_total": 5,
    "services_received": [],
    "lifetime_value": 4390
  },
  "state": "churned",
  "preferences": {
    "channel": "whatsapp",
    "reminder_opt_in": true
  },
  "consent": {
    "opted_in_at": "2025-09-01",
    "scope": [
      "promotional_offers"
    ]
  }
}
```

</details>

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** customer · **send as:** `merchant_on_behalf` · **greeting:** Hi Reyansh · **language:** English

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "customer lapsed soft"}`

- **Data richness:** sparse

- **Digest item:** none

- **Slots:** none

- **Consent:** covered by consent: promotional_offers

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

  - state_conflict: trigger says customer lapsed soft but customer state is churned

  - sparse_merchant: no offers, history, signals or review themes; anchor on performance, peers and category facts

<details><summary>All 39 facts</summary>

- **identity**: Asha Dental Care; Asha; Sector 17, Chandigarh; Google profile is not verified; in business since 2023
- **performance**: 3,722 profile views in the last 30 days; 33 calls in the last 30 days; 96 direction requests in the last 30 days; 31 leads in the last 30 days; 2.9% CTR over the last 30 days; views -22% over the last 7 days; calls -26% over the last 7 days
- **peer**: CTR 2.9% vs 3.0% peer average, in line with peers; Profile views 3,722 vs 1,820 peer average, 105% above peers; Calls 33 vs 12 peer average, 175% above peers; Direction requests 96 vs 38 peer average, 153% above peers
- **customers**: 88 unique patients this year
- **offers**: no active offers right now; category offers this merchant hasn't run: Dental Cleaning @ ₹299; Teeth Whitening @ ₹1,499; Root Canal @ ₹2,999 (single rooted); Aligner Consultation @ ₹499; Pediatric Dental Checkup @ ₹199
- **subscription**: Pro plan active, 97 days left
- **category**: peer group: metro solo practices 2026; peers average a 4.4★ rating; peers average 62 reviews; peers post on Google every 14 days on average; peers have 9 photos on average
- **season**: Apr-Jun: school holiday window — pediatric appointments +50%
- **trends**: "clear aligners delhi" searches +62% year-on-year (age 28-45, skews female); "teeth whitening price" searches +41% year-on-year; "dental implants near me" searches +18% year-on-year (age 45-65, skews male); "kids first dental visit" searches +27% year-on-year (parents 25-40, skews female)
- **customer**: Reyansh; age group 25-35; customer status: churned; 5 visits since 1 Sep 2025; last visit 1 Apr 2026; 25 days since the last visit; ₹4,390 spent so far
- **consent**: consented on 1 Sep 2025 to: promotional offers; opted in to reminders

</details>

## 2 · Phase 2: writing brief

- **Family:** customer · **angle:** warm, no pressure: give them an easy reason to come back

- **Lead (why now):** customer lapsed soft (the trigger gives no details)

- **Supporting facts:**

  - 5 visits since 1 Sep 2025 *(from customer.relationship.visits_total)*

- **Ask:** yes/no: Reply YES and we'll book a time that suits you.

- **Format:** pre-approved template (`merchant_customer_lapsed_soft_v1`)

- **Allowed numbers:** 1, 5, 17, 2025

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Reyansh, a customer of Asha Dental Care. Sent as: Asha Dental Care, on the shop's behalf (not Vera).
Greeting: Hi Reyansh
Language: English.
Why now: customer lapsed soft (the trigger gives no details)
Supporting facts (use only these):
- 5 visits since 1 Sep 2025
Angle: warm, no pressure: give them an easy reason to come back. Levers: reciprocity, single binary commitment.
Ask, one only, as the last sentence (yes/no): Reply YES and we'll book a time that suits you.
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm, clear and respectful, like the shop's front desk writing to a regular customer.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Write as Asha Dental Care, not as Vera. No medical or guaranteed-result claims.
- The trigger (customer lapsed soft) gives no details: mention it only in general terms and build the message on the supporting facts.
- The records disagree about when they last visited: don't mention how long they've been away.
- There's little merchant-specific data: lean on the comparisons and category facts listed.
- Numbers may only come from: 1, 5, 17, 2025.
- Never use: guaranteed, 100% safe, completely cure, miracle, best in city, doctor approved, FDA-approved.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Reyansh, Asha Dental Care here. A quick note from us. Thanks for your 5 visits since 1 Sep 2025. Reply YES and we'll book a time that suits you.

## 3 · Phase 3: AI writer

> Hi Reyansh, Asha Dental Care here. We wanted to check in and thank you for your 5 visits since 1 Sep 2025. We’d be happy to welcome you back whenever it suits you. Reply YES and we'll book a time that suits you.

**AI's rationale:** This keeps the tone warm and low-pressure, anchoring on Reyansh’s 5 visits since 1 Sep 2025. It uses gratitude as reciprocity and ends with the requested single YES/no commitment.

## 4 · Phase 4: validator

The AI's first version passed every check.

## Checks

| Check | Plain message | AI message |
|---|---|---|
| Not empty | ✅ | ✅ |
| Numbers all from the brief | ✅ | ✅ |
| No links | ✅ | ✅ |
| No taboo words | ✅ | ✅ |
| No internal codes | ✅ | ✅ |
| No template braces | ✅ | ✅ |
| At most one question | ✅ | ✅ |
| At most one ! and one emoji | ✅ | ✅ |
| No preamble or self-introduction | ✅ | ✅ |
| Doesn't repeat itself | ✅ | ✅ |
| No services the brief doesn't list | ✅ | ✅ |
| Customer message speaks as the shop | ✅ | ✅ |
| Customer message names the shop | ✅ | ✅ |
| Addresses them by name | ✅ | ✅ |
| Has a concrete number, date or price | ➖ customer message | ➖ customer message |
| Ends with the ask | ✅ | ✅ |
| Not copied from a case study | ✅ | ✅ |
| Under 600 characters | ✅ | ✅ |
| Language as expected *(advisory)* | ✅ | ✅ |