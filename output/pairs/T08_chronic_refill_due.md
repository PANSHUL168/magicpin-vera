# T08 · chronic_refill_due → Vivaan (Bright Smile Dental)

**Final message** (sent as `merchant_on_behalf`, written by **ai**, ask type `binary_yes_no`):

> Hi Vivaan, Bright Smile Dental here. We’re reaching out about your next visit, following your last visit on 1 Apr 2026, 25 days ago. Thank you for visiting us 5 times since 1 Sep 2025. Reply YES and we’ll book a time that suits you.

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_081_chronic_refill_due_m_011_dr_sameer_dent`

```json
{
  "id": "trg_081_chronic_refill_due_m_011_dr_sameer_dent",
  "scope": "customer",
  "kind": "chronic_refill_due",
  "source": "internal",
  "merchant_id": "m_011_dr_sameer_dentist_bangalore",
  "customer_id": "c_044_vivaan_for_m_011_dr_sameer_dentist_bangalore",
  "payload": {
    "placeholder": true,
    "metric_or_topic": "chronic_refill_due"
  },
  "urgency": 2,
  "suppression_key": "chronic_refill_due:m_011_dr_sameer_dentist_bangalore:gen_81",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_011_dr_sameer_dentist_bangalore</code> (full record)</summary>

```json
{
  "merchant_id": "m_011_dr_sameer_dentist_bangalore",
  "category_slug": "dentists",
  "identity": {
    "name": "Bright Smile Dental",
    "city": "Bangalore",
    "locality": "Indiranagar",
    "place_id": "ChIJ_INDIRANAGAR_DENTISTS_011",
    "verified": true,
    "languages": [
      "en",
      "hi",
      "kn"
    ],
    "owner_first_name": "Dr. Sameer",
    "established_year": 2013
  },
  "subscription": {
    "status": "expired",
    "plan": "Pro",
    "days_remaining": 0,
    "days_since_expiry": 28
  },
  "performance": {
    "window_days": 30,
    "views": 4792,
    "calls": 55,
    "directions": 138,
    "ctr": 0.046,
    "leads": 27,
    "delta_7d": {
      "views_pct": -0.2,
      "calls_pct": 0.16
    }
  },
  "offers": [],
  "conversation_history": [],
  "customer_aggregate": {
    "total_unique_ytd": 1905
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

<details><summary>Customer <code>c_044_vivaan_for_m_011_dr_sameer_dentist_bangalore</code></summary>

```json
{
  "customer_id": "c_044_vivaan_for_m_011_dr_sameer_dentist_bangalore",
  "merchant_id": "m_011_dr_sameer_dentist_bangalore",
  "identity": {
    "name": "Vivaan",
    "phone_redacted": "<phone>",
    "language_pref": "en",
    "age_band": "30-40"
  },
  "relationship": {
    "first_visit": "2025-09-01",
    "last_visit": "2026-04-01",
    "visits_total": 5,
    "services_received": [],
    "lifetime_value": 4900
  },
  "state": "new",
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

- **Audience:** customer · **send as:** `merchant_on_behalf` · **greeting:** Hi Vivaan · **language:** English

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "chronic refill due"}`

- **Data richness:** sparse

- **Digest item:** none

- **Slots:** none

- **Consent:** chronic_refill_due needs one of refill_reminders; customer consented only to promotional_offers

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

  - merchant_not_active: subscription is expired; this message goes out on their behalf

  - consent_gap: chronic_refill_due needs one of refill_reminders; customer consented only to promotional_offers

  - sparse_merchant: no offers, history, signals or review themes; anchor on performance, peers and category facts

<details><summary>All 39 facts</summary>

- **identity**: Bright Smile Dental; Sameer; Indiranagar, Bangalore; Google profile is verified; in business since 2013
- **performance**: 4,792 profile views in the last 30 days; 55 calls in the last 30 days; 138 direction requests in the last 30 days; 27 leads in the last 30 days; 4.6% CTR over the last 30 days; views -20% over the last 7 days; calls +16% over the last 7 days
- **peer**: CTR 4.6% vs 3.0% peer average, 53% above peers; Profile views 4,792 vs 1,820 peer average, 163% above peers; Calls 55 vs 12 peer average, 358% above peers; Direction requests 138 vs 38 peer average, 263% above peers
- **customers**: 1,905 unique patients this year
- **offers**: no active offers right now; category offers this merchant hasn't run: Dental Cleaning @ ₹299; Teeth Whitening @ ₹1,499; Root Canal @ ₹2,999 (single rooted); Aligner Consultation @ ₹499; Pediatric Dental Checkup @ ₹199
- **subscription**: subscription expired 28 days ago
- **category**: peer group: metro solo practices 2026; peers average a 4.4★ rating; peers average 62 reviews; peers post on Google every 14 days on average; peers have 9 photos on average
- **season**: Apr-Jun: school holiday window — pediatric appointments +50%
- **trends**: "clear aligners delhi" searches +62% year-on-year (age 28-45, skews female); "teeth whitening price" searches +41% year-on-year; "dental implants near me" searches +18% year-on-year (age 45-65, skews male); "kids first dental visit" searches +27% year-on-year (parents 25-40, skews female)
- **customer**: Vivaan; age group 30-40; customer status: new; 5 visits since 1 Sep 2025; last visit 1 Apr 2026; 25 days since the last visit; ₹4,900 spent so far
- **consent**: consented on 1 Sep 2025 to: promotional offers; opted in to reminders

</details>

## 2 · Phase 2: writing brief

- **Family:** customer · **angle:** a short, relevant note from the shop

- **Lead (why now):** chronic refill due (doesn't fit this business)

- **Supporting facts:**

  - 5 visits since 1 Sep 2025 *(from customer.relationship.visits_total)*

  - last visit 1 Apr 2026 (25 days ago) *(from customer.relationship.last_visit)*

- **Ask:** yes/no: Reply YES and we'll book a time that suits you.

- **Format:** pre-approved template (`merchant_chronic_refill_due_v1`)

- **Allowed numbers:** 1, 5, 25, 2025, 2026

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Vivaan, a customer of Bright Smile Dental. Sent as: Bright Smile Dental, on the shop's behalf (not Vera).
Greeting: Hi Vivaan
Language: English.
Why now: chronic refill due (doesn't fit this business)
Supporting facts (use only these):
- 5 visits since 1 Sep 2025
- last visit 1 Apr 2026 (25 days ago)
Angle: a short, relevant note from the shop. Levers: single binary commitment.
Ask, one only, as the last sentence (yes/no): Reply YES and we'll book a time that suits you.
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm, clear and respectful, like the shop's front desk writing to a regular customer.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Write as Bright Smile Dental, not as Vera. No medical or guaranteed-result claims.
- The trigger (chronic refill due) gives no details: mention it only in general terms and build the message on the supporting facts.
- The customer only agreed to promotional offers: keep it to a brief, non-promotional note about their own booking.
- Their subscription is expired: don't promise platform features as if it were active.
- There's little merchant-specific data: lean on the comparisons and category facts listed.
- This trigger type (chronic refill due) doesn't fit a dentists business: keep it to a general, friendly visit note.
- Numbers may only come from: 1, 5, 25, 2025, 2026.
- Never use: guaranteed, 100% safe, completely cure, miracle, best in city, doctor approved, FDA-approved.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Vivaan, Bright Smile Dental here. It's time for your next visit. Thanks for your 5 visits since 1 Sep 2025. Your last visit was on 1 Apr 2026, 25 days ago. Reply YES and we'll book a time that suits you.

## 3 · Phase 3: AI writer

> Hi Vivaan, Bright Smile Dental here. We’re reaching out about your next visit, following your last visit on 1 Apr 2026, 25 days ago. Thank you for visiting us 5 times since 1 Sep 2025. Reply YES and we’ll book a time that suits you.

**AI's rationale:** This keeps the note warm and personal while anchoring it in Vivaan’s visit history and the 25-day gap since the last visit. It ends with the required single yes/no booking ask.

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