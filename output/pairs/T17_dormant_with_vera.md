# T17 · dormant_with_vera → Anand (Chai Point Cafe)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Hi Anand, Zomato ke Apr 2026 partner update ke hisaab se ‘verified’ badge Tier-1 cities mein +24% impressions se correlate karta hai. Chai Point Cafe ke profile views 2,189 hain, jabki peer average 4,800 hai; Weekday Lunch Thali ₹149 aur Match-night Combo ₹399 jaise offers is gap par kaam aa sakte hain. Kya main 2 min mein bataun ki yeh aapke liye kaise kaam kar sakta hai?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_046_dormant_with_vera_m_029_anand_restaura`

```json
{
  "id": "trg_046_dormant_with_vera_m_029_anand_restaura",
  "scope": "merchant",
  "kind": "dormant_with_vera",
  "source": "internal",
  "merchant_id": "m_029_anand_restaurant_chandigarh",
  "customer_id": null,
  "payload": {
    "placeholder": true,
    "metric_or_topic": "dormant_with_vera"
  },
  "urgency": 2,
  "suppression_key": "dormant_with_vera:m_029_anand_restaurant_chandigarh:gen_46",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_029_anand_restaurant_chandigarh</code> (full record)</summary>

```json
{
  "merchant_id": "m_029_anand_restaurant_chandigarh",
  "category_slug": "restaurants",
  "identity": {
    "name": "Chai Point Cafe",
    "city": "Chandigarh",
    "locality": "Sector 8",
    "place_id": "ChIJ_SECTOR_8_RESTAURANTS_029",
    "verified": true,
    "languages": [
      "en",
      "hi"
    ],
    "owner_first_name": "Anand",
    "established_year": 2011
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 148,
    "days_since_expiry": null
  },
  "performance": {
    "window_days": 30,
    "views": 2189,
    "calls": 26,
    "directions": 82,
    "ctr": 0.025,
    "leads": 13,
    "delta_7d": {
      "views_pct": -0.08,
      "calls_pct": -0.21
    }
  },
  "offers": [],
  "conversation_history": [],
  "customer_aggregate": {
    "total_unique_ytd": 1525
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

- **Audience:** merchant · **send as:** `vera` · **greeting:** Hi Anand · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "dormant with vera"}`

- **Data richness:** sparse

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

  - sparse_merchant: no offers, history, signals or review themes; anchor on performance, peers and category facts

<details><summary>All 31 facts</summary>

- **identity**: Chai Point Cafe; Anand; Sector 8, Chandigarh; Google profile is verified; in business since 2011
- **performance**: 2,189 profile views in the last 30 days; 26 calls in the last 30 days; 82 direction requests in the last 30 days; 13 leads in the last 30 days; 2.5% CTR over the last 30 days; views -8% over the last 7 days; calls -21% over the last 7 days
- **peer**: CTR 2.5% vs 2.5% peer average, in line with peers; Profile views 2,189 vs 4,800 peer average, 54% below peers; Calls 26 vs 38 peer average, 32% below peers; Direction requests 82 vs 95 peer average, 14% below peers
- **customers**: 1,525 unique customers this year
- **offers**: no active offers right now; category offers this merchant hasn't run: Weekday Lunch Thali @ ₹149; Match-night Combo @ ₹399 (food + drink); Family Sunday Brunch @ ₹699/pax; Free Starter on orders > ₹1,200; Free Delivery > ₹500
- **subscription**: Pro plan active, 148 days left
- **category**: peer group: metro casual dining 2026; peers average a 4.2★ rating; peers average 142 reviews; peers post on Google every 7 days on average; peers have 22 photos on average
- **season**: Mar-Apr: IPL season — match-night promos on Tue/Wed/Thu; not weekends
- **trends**: "biryani near me" searches +18% year-on-year; "weekday lunch thali" searches +34% year-on-year (office 25-45); "sugar free dessert" searches +52% year-on-year (age 28-45); "match night offer" searches +65% year-on-year (age 20-40, skews male); "small party catering" searches +22% year-on-year (age 30-50, skews female)

</details>

## 2 · Phase 2: writing brief

- **Family:** account · **angle:** re-open with something genuinely useful; never mention the silence

- **Lead (why now):** Zomato 'verified' badge correlates with +24% impressions in Tier-1 cities (Zomato partner update, Apr 2026)

- **Supporting facts:**

  - popular category offers not on their profile: Weekday Lunch Thali @ ₹149; Match-night Combo @ ₹399 (food + drink) *(from category.offer_catalog minus merchant.offers)*

  - Profile views 2,189 vs 4,800 peer average, 54% below peers *(from merchant.performance.views vs category.peer_stats.avg_views_30d)*

- **Ask:** yes/no: Want me to show how this could work for your business, in 2 min?

- **Format:** pre-approved template (`vera_dormant_with_vera_v1`)

- **Allowed numbers:** 1, 2, 8, 24, 54, 149, 399, 2026, 2189, 4800

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Anand, owner of Chai Point Cafe. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Anand
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: Zomato 'verified' badge correlates with +24% impressions in Tier-1 cities (Zomato partner update, Apr 2026)
Supporting facts (use only these):
- popular category offers not on their profile: Weekday Lunch Thali @ ₹149; Match-night Combo @ ₹399 (food + drink)
- Profile views 2,189 vs 4,800 peer average, 54% below peers
Angle: re-open with something genuinely useful; never mention the silence. Levers: reciprocity, curiosity, loss aversion.
Ask, one only, as the last sentence (yes/no): Kya main 2 min mein bataun ki yeh aapke liye kaise kaam kar sakta hai?
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm busy practical, fellow operator.
- Category words you can use (vocabulary only, not facts about this business): footfall, covers, AOV, RPC, table turnover, reservations.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- The trigger (dormant with vera) gives no details: mention it only in general terms and build the message on the supporting facts.
- There's little merchant-specific data: lean on the comparisons and category facts listed.
- Numbers may only come from: 1, 2, 8, 24, 54, 149, 399, 2026, 2189, 4800.
- Never use: best food in city, guaranteed packed house, miracle marketing, viral guarantee.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Anand, thought you'd want to see this: Zomato 'verified' badge correlates with +24% impressions in Tier-1 cities (Zomato partner update, Apr 2026). One idea from the category catalog: a "Weekday Lunch Thali @ ₹149" offer. Your profile views are 2,189 vs 4,800 for similar restaurants. Kya main 2 min mein bataun ki yeh aapke liye kaise kaam kar sakta hai?

## 3 · Phase 3: AI writer

> Hi Anand, Zomato ke Apr 2026 partner update ke hisaab se ‘verified’ badge Tier-1 cities mein +24% impressions se correlate karta hai. Chai Point Cafe ke profile views 2,189 hain, jabki peer average 4,800 hai; Weekday Lunch Thali ₹149 aur Match-night Combo ₹399 jaise offers is gap par kaam aa sakte hain. Kya main 2 min mein bataun ki yeh aapke liye kaise kaam kar sakta hai?

**AI's rationale:** Anchors the message on the 24% Zomato partner-update figure and the 2,189 vs 4,800 profile-view gap. It uses the two relevant category offers to create practical curiosity and a clear reason to re-engage.

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