# T15 · customer_lapsed_soft → Reyansh (Daily Care Medicos)

**Final message** (sent as `merchant_on_behalf`, written by **ai**, ask type `binary_yes_no`):

> Hi Reyansh, Daily Care Medicos here. Aapse ek chhota sa check-in kar rahe hain—1 Sep 2025 se aapke 12 visits ke liye dhanyavaad. YES reply kijiye, hum aapka agla order pickup ya home delivery ke liye ready kar denge.

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_072_customer_lapsed_soft_m_049_komal_pharmaci`

```json
{
  "id": "trg_072_customer_lapsed_soft_m_049_komal_pharmaci",
  "scope": "customer",
  "kind": "customer_lapsed_soft",
  "source": "internal",
  "merchant_id": "m_049_komal_pharmacie_lucknow",
  "customer_id": "c_193_reyansh_for_m_049_komal_pharmacie_lucknow",
  "payload": {
    "placeholder": true,
    "metric_or_topic": "customer_lapsed_soft"
  },
  "urgency": 3,
  "suppression_key": "customer_lapsed_soft:m_049_komal_pharmacie_lucknow:gen_72",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_049_komal_pharmacie_lucknow</code> (full record)</summary>

```json
{
  "merchant_id": "m_049_komal_pharmacie_lucknow",
  "category_slug": "pharmacies",
  "identity": {
    "name": "Daily Care Medicos",
    "city": "Lucknow",
    "locality": "Alambagh",
    "place_id": "ChIJ_ALAMBAGH_PHARMACIES_049",
    "verified": true,
    "languages": [
      "en",
      "hi"
    ],
    "owner_first_name": "Komal",
    "established_year": 2023
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 278,
    "days_since_expiry": null
  },
  "performance": {
    "window_days": 30,
    "views": 3384,
    "calls": 34,
    "directions": 80,
    "ctr": 0.033,
    "leads": 34,
    "delta_7d": {
      "views_pct": 0.2,
      "calls_pct": -0.19
    }
  },
  "offers": [],
  "conversation_history": [],
  "customer_aggregate": {
    "total_unique_ytd": 1487
  },
  "signals": [],
  "review_themes": []
}
```

</details>

<details><summary>Category <code>pharmacies</code> (key fields)</summary>

```json
{
  "slug": "pharmacies",
  "voice": {
    "tone": "trustworthy_precise",
    "register": "neighbourhood_pharmacist",
    "code_mix": "hindi_english_natural",
    "vocab_allowed": [
      "OTC",
      "schedule H",
      "schedule X",
      "generic",
      "branded",
      "molecule",
      "MRP",
      "expiry",
      "batch",
      "PCR retail",
      "pharmacist counsel"
    ],
    "vocab_taboo": [
      "miracle cure",
      "guaranteed result",
      "100% safe",
      "doctor recommended (without disclosure)",
      "best price (without supporting data)"
    ],
    "salutation_examples": [
      "Hi {pharmacist_name}",
      "{pharmacy_name} team"
    ],
    "tone_examples": [
      "Quick check — your repeat-prescription customer count is up 18% this month",
      "Heads up: a generic alternative for {molecule} just got approved — likely 30% lower MRP"
    ]
  },
  "peer_stats": {
    "scope": "metro_neighbourhood_pharmacies_2026",
    "avg_rating": 4.6,
    "avg_review_count": 42,
    "avg_views_30d": 1400,
    "avg_calls_30d": 22,
    "avg_directions_30d": 58,
    "avg_ctr": 0.038,
    "avg_photos": 6,
    "avg_post_freq_days": 21,
    "delivery_share_pct": 0.35,
    "repeat_customer_pct": 0.62
  },
  "offer_catalog": [
    "Flat 20% OFF on medicines",
    "Free Home Delivery > ₹499",
    "Annual Health Card @ ₹399 (15% off all year)",
    "Free BP & Sugar Check",
    "Senior Citizen 15% OFF (60+ age)",
    "Diabetic Care Combo: Glucometer + 50 strips @ ₹999",
    "Free Pharmacist Consultation (10 min)",
    "Subscription refill reminder + delivery (chronic Rx)"
  ],
  "digest (titles)": [
    "Generic metformin SR price drop after 4 new approvals",
    "FDA enforcement audit on Schedule H1 antibiotic dispensing — Q2",
    "Summer demand shift: ORS, sunscreen, anti-fungal up 40%; cold/cough down 60%",
    "Chronic-Rx subscription retention 3.2x higher than walk-in",
    "Voluntary recall: Specific atorvastatin batches by manufacturer X"
  ],
  "seasonal_beats": [
    {
      "month_range": "Apr-Jun",
      "note": "summer surge — ORS, sunscreen, anti-fungal, deodorant"
    },
    {
      "month_range": "Jul-Aug",
      "note": "monsoon — anti-bacterial, anti-fungal, immunity supplements peak"
    },
    {
      "month_range": "Oct-Nov",
      "note": "festival sweets → blood sugar spike — diabetic monitoring needs surge"
    },
    {
      "month_range": "Dec-Jan",
      "note": "respiratory peak — cough/cold/anti-allergic 2x baseline"
    }
  ]
}
```

</details>

<details><summary>Customer <code>c_193_reyansh_for_m_049_komal_pharmacie_lucknow</code></summary>

```json
{
  "customer_id": "c_193_reyansh_for_m_049_komal_pharmacie_lucknow",
  "merchant_id": "m_049_komal_pharmacie_lucknow",
  "identity": {
    "name": "Reyansh",
    "phone_redacted": "<phone>",
    "language_pref": "hi-en mix",
    "age_band": "30-40"
  },
  "relationship": {
    "first_visit": "2025-09-01",
    "last_visit": "2026-04-01",
    "visits_total": 12,
    "services_received": [],
    "lifetime_value": 3012
  },
  "state": "active",
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

- **Audience:** customer · **send as:** `merchant_on_behalf` · **greeting:** Hi Reyansh · **language:** Hindi-English mix (Hinglish)

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "customer lapsed soft"}`

- **Data richness:** sparse

- **Digest item:** none

- **Slots:** none

- **Consent:** covered by consent: promotional_offers

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

  - state_conflict: trigger says customer lapsed soft but customer state is active

  - sparse_merchant: no offers, history, signals or review themes; anchor on performance, peers and category facts

<details><summary>All 39 facts</summary>

- **identity**: Daily Care Medicos; Komal; Alambagh, Lucknow; Google profile is verified; in business since 2023
- **performance**: 3,384 profile views in the last 30 days; 34 calls in the last 30 days; 80 direction requests in the last 30 days; 34 leads in the last 30 days; 3.3% CTR over the last 30 days; views +20% over the last 7 days; calls -19% over the last 7 days
- **peer**: CTR 3.3% vs 3.8% peer average, 13% below peers; Profile views 3,384 vs 1,400 peer average, 142% above peers; Calls 34 vs 22 peer average, 55% above peers; Direction requests 80 vs 58 peer average, 38% above peers
- **customers**: 1,487 unique customers this year
- **offers**: no active offers right now; category offers this merchant hasn't run: Diabetic Care Combo: Glucometer + 50 strips @ ₹999; Free BP & Sugar Check; Free Pharmacist Consultation (10 min); Subscription refill reminder + delivery (chronic Rx); Free Home Delivery > ₹499
- **subscription**: Pro plan active, 278 days left
- **category**: peer group: metro neighbourhood pharmacies 2026; peers average a 4.6★ rating; peers average 42 reviews; peers post on Google every 21 days on average; peers have 6 photos on average
- **season**: Apr-Jun: summer surge — ORS, sunscreen, anti-fungal, deodorant
- **trends**: "medicine home delivery" searches +42% year-on-year; "generic medicine" searches +34% year-on-year (age 30-65); "diabetes care kit" searches +28% year-on-year (age 40-65); "blood pressure monitor" searches +18% year-on-year (age 45-70)
- **customer**: Reyansh; age group 30-40; customer status: active; 12 visits since 1 Sep 2025; last visit 1 Apr 2026; 25 days since the last visit; ₹3,012 spent so far
- **consent**: consented on 1 Sep 2025 to: promotional offers; opted in to reminders

</details>

## 2 · Phase 2: writing brief

- **Family:** customer · **angle:** warm, no pressure: give them an easy reason to come back

- **Lead (why now):** customer lapsed soft (the trigger gives no details)

- **Supporting facts:**

  - 12 visits since 1 Sep 2025 *(from customer.relationship.visits_total)*

- **Ask:** yes/no: Reply YES and we'll get your next order ready for pickup or home delivery.

- **Format:** pre-approved template (`merchant_customer_lapsed_soft_v1`)

- **Allowed numbers:** 1, 12, 2025

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Reyansh, a customer of Daily Care Medicos. Sent as: Daily Care Medicos, on the shop's behalf (not Vera).
Greeting: Hi Reyansh
Language: Hindi-English mix (Hinglish), in Roman script.
Why now: customer lapsed soft (the trigger gives no details)
Supporting facts (use only these):
- 12 visits since 1 Sep 2025
Angle: warm, no pressure: give them an easy reason to come back. Levers: reciprocity, single binary commitment.
Ask, one only, as the last sentence (yes/no): YES reply kijiye, hum aapka agla order pickup ya home delivery ke liye ready kar denge.
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm, clear and respectful, like the shop's front desk writing to a regular customer.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Write as Daily Care Medicos, not as Vera. No medical or guaranteed-result claims.
- The trigger (customer lapsed soft) gives no details: mention it only in general terms and build the message on the supporting facts.
- The records disagree about when they last visited: don't mention how long they've been away.
- There's little merchant-specific data: lean on the comparisons and category facts listed.
- Numbers may only come from: 1, 12, 2025.
- Never use: miracle cure, guaranteed result, 100% safe, doctor recommended, best price.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Reyansh, Daily Care Medicos here. Aapke liye ek chhota sa update. 1 Sep 2025 se ab tak 12 visits ke liye shukriya. YES reply kijiye, hum aapka agla order pickup ya home delivery ke liye ready kar denge.

## 3 · Phase 3: AI writer

> Hi Reyansh, Daily Care Medicos here. Aapse ek chhota sa check-in kar rahe hain—1 Sep 2025 se aapke 12 visits ke liye dhanyavaad. YES reply kijiye, hum aapka agla order pickup ya home delivery ke liye ready kar denge.

**AI's rationale:** The message stays warm and pressure-free, acknowledges Reyansh’s 12 visits since 1 Sep 2025, and offers a simple pickup or home-delivery option. It uses one clear yes/no ask without repeating the offer.

## 4 · Phase 4: validator

The AI's first version was **rejected** (repeats itself: hum aapka agla order):

> Hi Reyansh, Daily Care Medicos se bol rahe hain. Aapki recent visit nahi hui, toh bas check-in kar rahe hain. 1 Sep 2025 se aapke 12 visits ke liye dhanyavaad—jab bhi zarurat ho, hum aapka agla order pickup ya home delivery ke liye ready kar denge. YES reply kijiye, hum aapka agla order pickup ya home delivery ke liye ready kar denge.

It was sent back once with this feedback:

- Say it once: don't repeat "hum aapka agla order"; each sentence should add something new.

The rewrite (shown above) passed every check.

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