# T05 · category_seasonal → Ramesh (Apollo Health Plus Pharmacy)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Hi Ramesh, summer 2026 mein ORS +40%, sunscreen +38% aur antifungal +45% demand badh rahi hai, jabki cold/cough -60% hai. Isliye ORS aur sunscreen counter par, cold/cough back shelf par rakhna sahi rahega; aapke Free Home Delivery > ₹499 aur Senior Citizen 15% OFF offers bhi highlight kar sakte hain. Kya main iske liye ek quick shelf aur offer plan bana doon, 10 min mein ready?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_020_summer_demand_shift`

```json
{
  "id": "trg_020_summer_demand_shift",
  "scope": "merchant",
  "kind": "category_seasonal",
  "source": "external",
  "merchant_id": "m_009_apollo_pharmacy_jaipur",
  "customer_id": null,
  "payload": {
    "season": "summer_2026",
    "trends": [
      "ORS_demand_+40",
      "sunscreen_demand_+38",
      "antifungal_demand_+45",
      "cold_cough_demand_-60"
    ],
    "shelf_action_recommended": true
  },
  "urgency": 2,
  "suppression_key": "season:summer:m_009:2026",
  "expires_at": "2026-06-30T00:00:00Z"
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

**Customer:** none (merchant-facing trigger)

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** merchant · **send as:** `vera` · **greeting:** Hi Ramesh · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"season": "summer 2026", "trends": ["ORS demand +40%", "sunscreen demand +38%", "antifungal demand +45%", "cold cough demand -60%"], "shelf_action_recommended": true}`

- **Data richness:** rich

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** 

  - open_merchant_request: merchant is waiting on: Yes send me the list please

<details><summary>All 38 facts</summary>

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

</details>

## 2 · Phase 2: writing brief

- **Family:** news · **angle:** get ahead of the seasonal shift

- **Lead (why now):** summer 2026: ORS demand +40%, sunscreen demand +38%, antifungal demand +45%, cold cough demand -60%

- **Supporting facts:**

  - Summer demand shift: ORS, sunscreen, anti-fungal up 40%; cold/cough down 60% (Multi-pharmacy aggregate Apr 2026): Move ORS + sunscreen to counter visibility; cold/cough to back shelf *(from category.digest[d_2026W17_summer_demand].actionable)*

  - active offers: Free Home Delivery > ₹499; Senior Citizen 15% OFF *(from merchant.offers (status=active))*

  - popular category offers not on their profile: Diabetic Care Combo: Glucometer + 50 strips @ ₹999; Free BP & Sugar Check *(from category.offer_catalog minus merchant.offers)*

- **Ask:** yes/no: Want a quick shelf-and-offer plan for this, ready in 10 min?

- **Format:** pre-approved template (`vera_category_seasonal_v1`)

- **Allowed numbers:** 10, 15, 38, 40, 45, 50, 60, 499, 999, 2026

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Ramesh, owner of Apollo Health Plus Pharmacy. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Ramesh
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: summer 2026: ORS demand +40%, sunscreen demand +38%, antifungal demand +45%, cold cough demand -60%
Supporting facts (use only these):
- Summer demand shift: ORS, sunscreen, anti-fungal up 40%; cold/cough down 60% (Multi-pharmacy aggregate Apr 2026): Move ORS + sunscreen to counter visibility; cold/cough to back shelf
- active offers: Free Home Delivery > ₹499; Senior Citizen 15% OFF
- popular category offers not on their profile: Diabetic Care Combo: Glucometer + 50 strips @ ₹999; Free BP & Sugar Check
Angle: get ahead of the seasonal shift. Levers: specificity, loss aversion.
Ask, one only, as the last sentence (yes/no): Kya main iske liye ek quick shelf aur offer plan bana doon, 10 min mein ready?
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: trustworthy precise, neighbourhood pharmacist.
- Category words you can use (vocabulary only, not facts about this business): OTC, schedule H, schedule X, generic, branded, molecule.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- Numbers may only come from: 10, 15, 38, 40, 45, 50, 60, 499, 999, 2026.
- Never use: miracle cure, guaranteed result, 100% safe, doctor recommended, best price.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Ramesh, the summer 2026 demand shift is here: ORS demand +40%, sunscreen demand +38%, antifungal demand +45%, cold cough demand -60%. The practical takeaway: move ORS + sunscreen to counter visibility; cold/cough to back shelf. Your Free Home Delivery > ₹499 and Senior Citizen 15% OFF offers are live. Kya main iske liye ek quick shelf aur offer plan bana doon, 10 min mein ready?

## 3 · Phase 3: AI writer

> Hi Ramesh, summer 2026 mein ORS +40%, sunscreen +38% aur antifungal +45% demand badh rahi hai, jabki cold/cough -60% hai. Isliye ORS aur sunscreen counter par, cold/cough back shelf par rakhna sahi rahega; aapke Free Home Delivery > ₹499 aur Senior Citizen 15% OFF offers bhi highlight kar sakte hain. Kya main iske liye ek quick shelf aur offer plan bana doon, 10 min mein ready?

**AI's rationale:** The message anchors on the summer 2026 multi-pharmacy demand shift and turns it into a specific shelf-placement recommendation. It also uses the existing offers without inventing new claims, ending with the required single yes/no ask.

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