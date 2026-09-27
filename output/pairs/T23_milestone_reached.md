# T23 · milestone_reached → Mukesh (Pizza Spot)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Hi Mukesh, milestone reach hua—nice progress. Aapka CTR 5.3% hai vs peers ke 2.5% average, yani 112% above peers; peers average 142 reviews, so review momentum par focus karna sensible hai. Kya main aapke happy customers ke liye 2-line review request draft kar doon?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_041_milestone_reached_m_032_mukesh_restaur`

```json
{
  "id": "trg_041_milestone_reached_m_032_mukesh_restaur",
  "scope": "merchant",
  "kind": "milestone_reached",
  "source": "internal",
  "merchant_id": "m_032_mukesh_restaurant_pune",
  "customer_id": null,
  "payload": {
    "placeholder": true,
    "metric_or_topic": "milestone_reached"
  },
  "urgency": 1,
  "suppression_key": "milestone_reached:m_032_mukesh_restaurant_pune:gen_41",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_032_mukesh_restaurant_pune</code> (full record)</summary>

```json
{
  "merchant_id": "m_032_mukesh_restaurant_pune",
  "category_slug": "restaurants",
  "identity": {
    "name": "Pizza Spot",
    "city": "Pune",
    "locality": "Aundh",
    "place_id": "ChIJ_AUNDH_RESTAURANTS_032",
    "verified": true,
    "languages": [
      "en",
      "hi"
    ],
    "owner_first_name": "Mukesh",
    "established_year": 2010
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 90,
    "days_since_expiry": null
  },
  "performance": {
    "window_days": 30,
    "views": 787,
    "calls": 5,
    "directions": 13,
    "ctr": 0.053,
    "leads": 0,
    "delta_7d": {
      "views_pct": 0.14,
      "calls_pct": -0.24
    }
  },
  "offers": [],
  "conversation_history": [],
  "customer_aggregate": {
    "total_unique_ytd": 889
  },
  "signals": [],
  "review_themes": []
}
```

</details>

<details><summary>Category <code>restaurants</code> (key fields)</summary>

```json
{
  "slug": "restaurants",
  "voice": {
    "tone": "warm_busy_practical",
    "register": "fellow_operator",
    "code_mix": "hindi_english_natural",
    "vocab_allowed": [
      "footfall",
      "covers",
      "AOV",
      "RPC",
      "table turnover",
      "reservations",
      "GRO",
      "weekend brunch",
      "happy hour",
      "thali",
      "biryani",
      "tandoor"
    ],
    "vocab_taboo": [
      "best food in city",
      "guaranteed packed house",
      "miracle marketing",
      "viral guarantee"
    ],
    "salutation_examples": [
      "Hi {chef_or_owner_first_name}",
      "{restaurant_name} team"
    ],
    "tone_examples": [
      "Quick one — IPL match nights have been 1.5x your weekday avg this season",
      "Spotted: 'biryani delivery' searches in your sublocality up 28% this week"
    ]
  },
  "peer_stats": {
    "scope": "metro_casual_dining_2026",
    "avg_rating": 4.2,
    "avg_review_count": 142,
    "avg_views_30d": 4800,
    "avg_calls_30d": 38,
    "avg_directions_30d": 95,
    "avg_ctr": 0.025,
    "avg_photos": 22,
    "avg_post_freq_days": 7,
    "retention_30d_pct": 0.18
  },
  "offer_catalog": [
    "Flat 30% OFF on total bill (limit ₹500)",
    "Buy 1 Pizza Get 1 Free (Tue-Thu)",
    "Weekday Lunch Thali @ ₹149",
    "Free Starter on orders > ₹1,200",
    "Match-night Combo @ ₹399 (food + drink)",
    "Family Sunday Brunch @ ₹699/pax",
    "Free Delivery > ₹500",
    "Birthday: Free Cake on parties of 6+"
  ],
  "digest (titles)": [
    "IPL home-match Saturdays underperformed weeknight matches across metros",
    "GST council clarifies 5% rate for restaurant takeaway packaging from 2026-06-01",
    "Zomato 'verified' badge correlates with +24% impressions in Tier-1 cities",
    "Swiggy iCare: AI complaint summarizer launching Apr 2026",
    "'Sugar-free dessert' searches +52% YoY across Indian metros"
  ],
  "seasonal_beats": [
    {
      "month_range": "Mar-Apr",
      "note": "IPL season — match-night promos on Tue/Wed/Thu; not weekends"
    },
    {
      "month_range": "Oct-Nov",
      "note": "Diwali corporate gifting + family-feast bookings"
    },
    {
      "month_range": "Dec",
      "note": "Christmas + New Year — set menu sales 3x baseline"
    },
    {
      "month_range": "Jul-Aug",
      "note": "monsoon delivery surge; rain-day discount window"
    },
    {
      "month_range": "Feb 14",
      "note": "Valentine's prix-fixe — book starting 2 weeks prior"
    }
  ]
}
```

</details>

**Customer:** none (merchant-facing trigger)

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** merchant · **send as:** `vera` · **greeting:** Hi Mukesh · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "milestone reached"}`

- **Data richness:** sparse

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

  - sparse_merchant: no offers, history, signals or review themes; anchor on performance, peers and category facts

<details><summary>All 31 facts</summary>

- **identity**: Pizza Spot; Mukesh; Aundh, Pune; Google profile is verified; in business since 2010
- **performance**: 787 profile views in the last 30 days; 5 calls in the last 30 days; 13 direction requests in the last 30 days; 0 leads in the last 30 days; 5.3% CTR over the last 30 days; views +14% over the last 7 days; calls -24% over the last 7 days
- **peer**: CTR 5.3% vs 2.5% peer average, 112% above peers; Profile views 787 vs 4,800 peer average, 84% below peers; Calls 5 vs 38 peer average, 87% below peers; Direction requests 13 vs 95 peer average, 86% below peers
- **customers**: 889 unique customers this year
- **offers**: no active offers right now; category offers this merchant hasn't run: Weekday Lunch Thali @ ₹149; Match-night Combo @ ₹399 (food + drink); Family Sunday Brunch @ ₹699/pax; Free Starter on orders > ₹1,200; Free Delivery > ₹500
- **subscription**: Pro plan active, 90 days left
- **category**: peer group: metro casual dining 2026; peers average a 4.2★ rating; peers average 142 reviews; peers post on Google every 7 days on average; peers have 22 photos on average
- **season**: Mar-Apr: IPL season — match-night promos on Tue/Wed/Thu; not weekends
- **trends**: "biryani near me" searches +18% year-on-year; "weekday lunch thali" searches +34% year-on-year (office 25-45); "sugar free dessert" searches +52% year-on-year (age 28-45); "match night offer" searches +65% year-on-year (age 20-40, skews male); "small party catering" searches +22% year-on-year (age 30-50, skews female)

</details>

## 2 · Phase 2: writing brief

- **Family:** performance · **angle:** celebrate and help them over the line

- **Lead (why now):** milestone reached (the trigger gives no details)

- **Supporting facts:**

  - peers average 142 reviews *(from category.peer_stats.avg_review_count)*

  - CTR 5.3% vs 2.5% peer average, 112% above peers *(from merchant.performance.ctr vs category.peer_stats.avg_ctr)*

- **Ask:** yes/no: Want me to draft a 2-line review request for your happy customers?

- **Format:** pre-approved template (`vera_milestone_reached_v1`)

- **Allowed numbers:** 2, 2.5, 5.3, 112, 142

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Mukesh, owner of Pizza Spot. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Mukesh
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: milestone reached (the trigger gives no details)
Supporting facts (use only these):
- peers average 142 reviews
- CTR 5.3% vs 2.5% peer average, 112% above peers
Angle: celebrate and help them over the line. Levers: specificity, social proof, effort externalization.
Ask, one only, as the last sentence (yes/no): Kya main aapke happy customers ke liye 2-line review request draft kar doon?
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm busy practical, fellow operator.
- Category words you can use (vocabulary only, not facts about this business): footfall, covers, AOV, RPC, table turnover, reservations.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- The trigger (milestone reached) gives no details: mention it only in general terms and build the message on the supporting facts.
- There's little merchant-specific data: lean on the comparisons and category facts listed.
- Numbers may only come from: 2, 2.5, 5.3, 112, 142.
- Never use: best food in city, guaranteed packed house, miracle marketing, viral guarantee.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Mukesh, you've hit a milestone worth marking. Peers average 142 reviews. Your CTR is 5.3% vs 2.5% for similar restaurants. Kya main aapke happy customers ke liye 2-line review request draft kar doon?

## 3 · Phase 3: AI writer

> Hi Mukesh, milestone reach hua—nice progress. Aapka CTR 5.3% hai vs peers ke 2.5% average, yani 112% above peers; peers average 142 reviews, so review momentum par focus karna sensible hai. Kya main aapke happy customers ke liye 2-line review request draft kar doon?

**AI's rationale:** The message celebrates the milestone and anchors on the strong 5.3% CTR versus the 2.5% peer average, while using the 142-review benchmark to suggest a practical next step.

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