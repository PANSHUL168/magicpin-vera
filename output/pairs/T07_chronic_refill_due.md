# T07 · chronic_refill_due → Sharma ji (Apollo Health Plus Pharmacy)

**Final message** (sent as `merchant_on_behalf`, written by **ai**, ask type `binary_confirm_cancel`):

> Namaste Sharma ji, Apollo Health Plus Pharmacy se—metformin, atorvastatin aur telmisartan ka refill Tue 28 Apr ko due hai. Aapka delivery address saved hai; ₹499 se upar Free Home Delivery aur Senior Citizen 15% OFF active hai. CONFIRM reply kijiye, hum saved address par deliver kar denge.

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_019_chronic_refill_grandfather`

```json
{
  "id": "trg_019_chronic_refill_grandfather",
  "scope": "customer",
  "kind": "chronic_refill_due",
  "source": "internal",
  "merchant_id": "m_009_apollo_pharmacy_jaipur",
  "customer_id": "c_013_grandfather_for_m009",
  "payload": {
    "molecule_list": [
      "metformin",
      "atorvastatin",
      "telmisartan"
    ],
    "last_refill": "2026-03-26",
    "stock_runs_out_iso": "2026-04-28T00:00:00+05:30",
    "delivery_address_saved": true
  },
  "urgency": 3,
  "suppression_key": "refill:c_013_grandfather_for_m009:2026-04",
  "expires_at": "2026-04-28T00:00:00+05:30"
}
```

<details><summary>Merchant <code>m_009_apollo_pharmacy_jaipur</code> (full record)</summary>

```json
{
  "merchant_id": "m_009_apollo_pharmacy_jaipur",
  "category_slug": "pharmacies",
  "identity": {
    "name": "Apollo Health Plus Pharmacy",
    "city": "Jaipur",
    "locality": "Malviya Nagar",
    "place_id": "ChIJ_MALVIYA_PHARMACY_009",
    "verified": true,
    "languages": [
      "en",
      "hi"
    ],
    "owner_first_name": "Ramesh",
    "established_year": 2016
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 60
  },
  "performance": {
    "window_days": 30,
    "views": 1850,
    "calls": 38,
    "directions": 95,
    "ctr": 0.045,
    "leads": 24,
    "delta_7d": {
      "views_pct": 0.06,
      "calls_pct": 0.08
    }
  },
  "offers": [
    {
      "id": "o_apollo_001",
      "title": "Free Home Delivery > ₹499",
      "status": "active",
      "started": "2026-01-01"
    },
    {
      "id": "o_apollo_002",
      "title": "Senior Citizen 15% OFF",
      "status": "active",
      "started": "2026-01-01"
    }
  ],
  "conversation_history": [
    {
      "ts": "2026-04-24T08:00:00Z",
      "from": "vera",
      "body": "Heads up: voluntary recall on atorvastatin batches X/Y by Mfr Z. Want the customer list filtered for that molecule?",
      "engagement": "merchant_replied"
    },
    {
      "ts": "2026-04-24T08:30:00Z",
      "from": "merchant",
      "body": "Yes send me the list please",
      "engagement": "intent_action"
    }
  ],
  "customer_aggregate": {
    "total_unique_ytd": 1820,
    "repeat_customer_pct": 0.68,
    "chronic_rx_count": 240
  },
  "signals": [
    "above_peer_calls",
    "compliance_aware",
    "high_repeat_rate"
  ],
  "review_themes": [
    {
      "theme": "delivery_speed",
      "sentiment": "pos",
      "occurrences_30d": 11
    },
    {
      "theme": "medicine_availability",
      "sentiment": "pos",
      "occurrences_30d": 8
    }
  ]
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

<details><summary>Customer <code>c_013_grandfather_for_m009</code></summary>

```json
{
  "customer_id": "c_013_grandfather_for_m009",
  "merchant_id": "m_009_apollo_pharmacy_jaipur",
  "identity": {
    "name": "Mr. Sharma",
    "phone_redacted": "<phone>",
    "language_pref": "hi",
    "age_band": "65-75",
    "senior_citizen": true
  },
  "relationship": {
    "first_visit": "2024-08-10",
    "last_visit": "2026-04-22",
    "visits_total": 24,
    "services_received": [
      "chronic_rx_metformin",
      "chronic_rx_atorvastatin",
      "chronic_rx_telmisartan",
      "..."
    ],
    "lifetime_value": 24600,
    "chronic_conditions": [
      "diabetes_t2",
      "hypertension",
      "dyslipidemia"
    ]
  },
  "state": "active",
  "preferences": {
    "preferred_slots": "morning_delivery",
    "channel": "whatsapp_via_son",
    "reminder_opt_in": true,
    "delivery_address": "saved"
  },
  "consent": {
    "opted_in_at": "2024-08-10",
    "scope": [
      "refill_reminders",
      "delivery_notifications",
      "recall_alerts"
    ]
  }
}
```

</details>

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** customer · **send as:** `merchant_on_behalf` · **greeting:** Namaste Sharma ji · **language:** Hindi

- **Event, made readable:** `{"molecule_list": ["metformin", "atorvastatin", "telmisartan"], "last_refill": "26 Mar 2026", "stock_runs_out_iso": "Tue 28 Apr", "delivery_address_saved": true}`

- **Data richness:** rich

- **Digest item:** none

- **Slots:** none

- **Consent:** covered by consent: refill_reminders

- **Warnings:** none

<details><summary>All 52 facts</summary>

- **identity**: Apollo Health Plus Pharmacy; Ramesh; Malviya Nagar, Jaipur; Google profile is verified; in business since 2016
- **performance**: 1,850 profile views in the last 30 days; 38 calls in the last 30 days; 95 direction requests in the last 30 days; 24 leads in the last 30 days; 4.5% CTR over the last 30 days; views +6% over the last 7 days; calls +8% over the last 7 days
- **peer**: CTR 4.5% vs 3.8% peer average, 18% above peers; Profile views 1,850 vs 1,400 peer average, 32% above peers; Calls 38 vs 22 peer average, 73% above peers; Direction requests 95 vs 58 peer average, 64% above peers; Repeat-customer share 68% vs 62% peer average, 6 points above peers
- **customers**: 1,820 unique customers this year; repeat-customer share 68%; 240 customers on chronic prescriptions
- **offers**: active offers: Free Home Delivery > ₹499; Senior Citizen 15% OFF; category offers this merchant hasn't run: Diabetic Care Combo: Glucometer + 50 strips @ ₹999; Free BP & Sugar Check; Free Pharmacist Consultation (10 min); Subscription refill reminder + delivery (chronic Rx); Annual Health Card @ ₹399 (15% off all year)
- **subscription**: Pro plan active, 60 days left
- **reviews**: 11 reviews in the last 30 days mention delivery speed (positive); 8 reviews in the last 30 days mention medicine availability (positive)
- **signals**: calls above the peer benchmark; compliance aware; high repeat rate
- **category**: peer group: metro neighbourhood pharmacies 2026; peers average a 4.6★ rating; peers average 42 reviews; peers post on Google every 21 days on average; peers have 6 photos on average
- **season**: Apr-Jun: summer surge — ORS, sunscreen, anti-fungal, deodorant
- **trends**: "medicine home delivery" searches +42% year-on-year; "generic medicine" searches +34% year-on-year (age 30-65); "diabetes care kit" searches +28% year-on-year (age 40-65); "blood pressure monitor" searches +18% year-on-year (age 45-70)
- **customer**: Mr. Sharma; age group 65-75; senior citizen; customer status: active; 24 visits since 10 Aug 2024; last visit 22 Apr 2026; 4 days since the last visit; services so far include: chronic Rx metformin, chronic Rx atorvastatin, chronic Rx telmisartan; ₹24,600 spent so far; prefers morning delivery slots; delivery address saved
- **customer_sensitive**: chronic conditions on file: diabetes T2, hypertension, dyslipidemia
- **consent**: consented on 10 Aug 2024 to: refill reminders, delivery notifications, recall alerts; opted in to reminders

</details>

## 2 · Phase 2: writing brief

- **Family:** customer · **angle:** precise and respectful: make the refill effortless

- **Lead (why now):** refill due: metformin, atorvastatin and telmisartan; stock runs out Tue 28 Apr

- **Supporting facts:**

  - delivery address saved *(from trigger.payload.delivery_address_saved)*

  - active offers: Free Home Delivery > ₹499; Senior Citizen 15% OFF *(from merchant.offers)*

- **Ask:** confirm: Reply CONFIRM and we'll deliver to your saved address.

- **Format:** pre-approved template (`merchant_chronic_refill_due_v1`)

- **Allowed numbers:** 15, 28, 499

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Sharma ji, a customer of Apollo Health Plus Pharmacy. Sent as: Apollo Health Plus Pharmacy, on the shop's behalf (not Vera).
Greeting: Namaste Sharma ji
Language: Simple Hindi in Roman script; everyday English words are fine.
Why now: refill due: metformin, atorvastatin and telmisartan; stock runs out Tue 28 Apr
Supporting facts (use only these):
- delivery address saved
- active offers: Free Home Delivery > ₹499; Senior Citizen 15% OFF
Angle: precise and respectful: make the refill effortless. Levers: specificity, effort externalization, single binary commitment.
Ask, one only, as the last sentence (confirm): CONFIRM reply kijiye, hum saved address par deliver kar denge.
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm, clear and respectful, like the shop's front desk writing to a regular customer.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Write as Apollo Health Plus Pharmacy, not as Vera. No medical or guaranteed-result claims.
- Numbers may only come from: 15, 28, 499.
- Never use: miracle cure, guaranteed result, 100% safe, doctor recommended, best price.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Namaste Sharma ji, Apollo Health Plus Pharmacy here. Aapki dawaiyan (metformin, atorvastatin aur telmisartan) Tue 28 Apr ko khatam ho jayengi. Free Home Delivery > ₹499 aur Senior Citizen 15% OFF dono lagu hain. CONFIRM reply kijiye, hum saved address par deliver kar denge.

## 3 · Phase 3: AI writer

> Namaste Sharma ji, Apollo Health Plus Pharmacy se—metformin, atorvastatin aur telmisartan ka refill Tue 28 Apr ko due hai. Aapka delivery address saved hai; ₹499 se upar Free Home Delivery aur Senior Citizen 15% OFF active hai. CONFIRM reply kijiye, hum saved address par deliver kar denge.

**AI's rationale:** Names the pharmacy in the first sentence and keeps the message precise, respectful, and effortless. It anchors on the refill date and uses the saved address and active offers to support one binary confirmation.

## 4 · Phase 4: validator

The AI's first version was **rejected** (doesn't say which shop is writing):

> Namaste Sharma ji, metformin, atorvastatin aur telmisartan ka refill Tue 28 Apr ko due hai. Aapka saved delivery address hai; ₹499 se upar Free Home Delivery aur Senior Citizen 15% OFF active hai. CONFIRM reply kijiye, hum saved address par deliver kar denge.

It was sent back once with this feedback:

- Name the shop (Apollo Health Plus Pharmacy) in the first sentence.

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