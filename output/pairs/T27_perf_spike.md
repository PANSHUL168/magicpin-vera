# T27 · perf_spike → Vikas (Sunrise Medicos)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Hi Vikas, Sunrise Medicos ke calls pichhle 7 din mein 5% badhe hain. CTR 4.1% hai, jo peer average 3.8% se 8% upar hai—aur is saal 540 unique customers bhi aaye hain. Kya main isi tarah ke do aur posts plan kar doon?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_036_perf_spike_m_010_sunrisepharm_p`

```json
{
  "id": "trg_036_perf_spike_m_010_sunrisepharm_p",
  "scope": "merchant",
  "kind": "perf_spike",
  "source": "internal",
  "merchant_id": "m_010_sunrisepharm_pharmacy_lucknow",
  "customer_id": null,
  "payload": {
    "placeholder": true,
    "metric_or_topic": "perf_spike"
  },
  "urgency": 1,
  "suppression_key": "perf_spike:m_010_sunrisepharm_pharmacy_lucknow:gen_36",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_010_sunrisepharm_pharmacy_lucknow</code> (full record)</summary>

```json
{
  "merchant_id": "m_010_sunrisepharm_pharmacy_lucknow",
  "category_slug": "pharmacies",
  "identity": {
    "name": "Sunrise Medicos",
    "city": "Lucknow",
    "locality": "Gomti Nagar",
    "place_id": "ChIJ_GOMTINAGAR_PHARMACY_010",
    "verified": false,
    "languages": [
      "en",
      "hi"
    ],
    "owner_first_name": "Vikas",
    "established_year": 2020
  },
  "subscription": {
    "status": "active",
    "plan": "Basic",
    "days_remaining": 200
  },
  "performance": {
    "window_days": 30,
    "views": 720,
    "calls": 14,
    "directions": 32,
    "ctr": 0.041,
    "leads": 8,
    "delta_7d": {
      "views_pct": 0.02,
      "calls_pct": 0.05
    }
  },
  "offers": [],
  "conversation_history": [],
  "customer_aggregate": {
    "total_unique_ytd": 540,
    "repeat_customer_pct": 0.45,
    "chronic_rx_count": 60
  },
  "signals": [
    "unverified_gbp",
    "no_active_offers",
    "no_recent_conversation",
    "delivery_not_set_up"
  ],
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

**Customer:** none (merchant-facing trigger)

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** merchant · **send as:** `vera` · **greeting:** Hi Vikas · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "perf spike"}`

- **Data richness:** moderate

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

<details><summary>All 37 facts</summary>

- **identity**: Sunrise Medicos; Vikas; Gomti Nagar, Lucknow; Google profile is not verified; in business since 2020
- **performance**: 720 profile views in the last 30 days; 14 calls in the last 30 days; 32 direction requests in the last 30 days; 8 leads in the last 30 days; 4.1% CTR over the last 30 days; views +2% over the last 7 days; calls +5% over the last 7 days
- **peer**: CTR 4.1% vs 3.8% peer average, 8% above peers; Profile views 720 vs 1,400 peer average, 49% below peers; Calls 14 vs 22 peer average, 36% below peers; Direction requests 32 vs 58 peer average, 45% below peers; Repeat-customer share 45% vs 62% peer average, 17 points below peers
- **customers**: 540 unique customers this year; repeat-customer share 45%; 60 customers on chronic prescriptions
- **offers**: no active offers right now; category offers this merchant hasn't run: Diabetic Care Combo: Glucometer + 50 strips @ ₹999; Free BP & Sugar Check; Free Pharmacist Consultation (10 min); Subscription refill reminder + delivery (chronic Rx); Free Home Delivery > ₹499
- **subscription**: Basic plan active, 200 days left
- **signals**: Google Business Profile not verified; no active offers; no recent conversation with Vera; delivery not set up
- **category**: peer group: metro neighbourhood pharmacies 2026; peers average a 4.6★ rating; peers average 42 reviews; peers post on Google every 21 days on average; peers have 6 photos on average
- **season**: Apr-Jun: summer surge — ORS, sunscreen, anti-fungal, deodorant
- **trends**: "medicine home delivery" searches +42% year-on-year; "generic medicine" searches +34% year-on-year (age 30-65); "diabetes care kit" searches +28% year-on-year (age 40-65); "blood pressure monitor" searches +18% year-on-year (age 45-70)

</details>

## 2 · Phase 2: writing brief

- **Family:** performance · **angle:** celebrate the jump and build on what caused it

- **Lead (why now):** perf spike (the trigger gives no details)

- **Supporting facts:**

  - calls +5% over the last 7 days *(from merchant.performance.delta_7d.calls_pct)*

  - CTR 4.1% vs 3.8% peer average, 8% above peers *(from merchant.performance.ctr vs category.peer_stats.avg_ctr)*

  - 540 unique customers this year *(from merchant.customer_aggregate.total_unique_ytd)*

- **Ask:** yes/no: Want me to line up two more posts like the one that worked?

- **Format:** pre-approved template (`vera_perf_spike_v1`)

- **Allowed numbers:** 3.8, 4.1, 5, 7, 8, 540

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Vikas, owner of Sunrise Medicos. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Vikas
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: perf spike (the trigger gives no details)
Supporting facts (use only these):
- calls +5% over the last 7 days
- CTR 4.1% vs 3.8% peer average, 8% above peers
- 540 unique customers this year
Angle: celebrate the jump and build on what caused it. Levers: specificity, curiosity.
Ask, one only, as the last sentence (yes/no): Kya main isi tarah ke do aur posts plan kar doon?
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: trustworthy precise, neighbourhood pharmacist.
- Category words you can use (vocabulary only, not facts about this business): OTC, schedule H, schedule X, generic, branded, molecule.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- The trigger (perf spike) gives no details: mention it only in general terms and build the message on the supporting facts.
- Numbers may only come from: 3.8, 4.1, 5, 7, 8, 540.
- Never use: miracle cure, guaranteed result, 100% safe, doctor recommended, best price.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Vikas, your recent numbers show a jump. Calls +5% this week. Your CTR is 4.1% vs 3.8% for similar pharmacies. Kya main isi tarah ke do aur posts plan kar doon?

## 3 · Phase 3: AI writer

> Hi Vikas, Sunrise Medicos ke calls pichhle 7 din mein 5% badhe hain. CTR 4.1% hai, jo peer average 3.8% se 8% upar hai—aur is saal 540 unique customers bhi aaye hain. Kya main isi tarah ke do aur posts plan kar doon?

**AI's rationale:** The message opens with the greeting and current performance jump, then connects calls, CTR, and customer reach to support building on the momentum. It ends with the exact yes/no ask and uses no unsupported claims.

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
| Customer message speaks as the shop | ➖ merchant-facing | ➖ merchant-facing |
| Customer message names the shop | ➖ merchant-facing | ➖ merchant-facing |
| Addresses them by name | ✅ | ✅ |
| Has a concrete number, date or price | ✅ | ✅ |
| Ends with the ask | ✅ | ✅ |
| Not copied from a case study | ✅ | ✅ |
| Under 600 characters | ✅ | ✅ |
| Language as expected *(advisory)* | ✅ | ✅ |