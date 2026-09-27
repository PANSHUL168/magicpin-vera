# T10 · competitor_opened → Suresh (Mylari South Indian Cafe)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Hi Suresh, competitor open hua hai, par panic ki zaroorat nahi—apni strengths ko clearly dikhate hain. Weekday Lunch Thali ₹149 par live hai, CTR 3.2% hai vs 2.5% peer average, aur last 30 days mein 22 reviews ne thali quality mention ki hai. Kya main ek Google post draft kar doon jo dikhaye ki aap alag kyun hain, 10 min mein ready?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_056_competitor_opened_m_006_southindiancaf`

```json
{
  "id": "trg_056_competitor_opened_m_006_southindiancaf",
  "scope": "merchant",
  "kind": "competitor_opened",
  "source": "external",
  "merchant_id": "m_006_southindiancafe_restaurant_bangalore",
  "customer_id": null,
  "payload": {
    "placeholder": true,
    "metric_or_topic": "competitor_opened"
  },
  "urgency": 2,
  "suppression_key": "competitor_opened:m_006_southindiancafe_restaurant_bangalore:gen_56",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_006_southindiancafe_restaurant_bangalore</code> (full record)</summary>

```json
{
  "merchant_id": "m_006_southindiancafe_restaurant_bangalore",
  "category_slug": "restaurants",
  "identity": {
    "name": "Mylari South Indian Cafe",
    "city": "Bangalore",
    "locality": "Indiranagar",
    "place_id": "ChIJ_INDIRANAGAR_RESTAURANT_006",
    "verified": true,
    "languages": [
      "en",
      "hi",
      "kn"
    ],
    "owner_first_name": "Suresh",
    "established_year": 2014
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 240
  },
  "performance": {
    "window_days": 30,
    "views": 12400,
    "calls": 88,
    "directions": 320,
    "ctr": 0.032,
    "leads": 145,
    "delta_7d": {
      "views_pct": 0.05,
      "calls_pct": 0.02
    }
  },
  "offers": [
    {
      "id": "o_mylari_001",
      "title": "Weekday Lunch Thali @ ₹149",
      "status": "active",
      "started": "2026-01-10"
    }
  ],
  "conversation_history": [
    {
      "ts": "2026-04-25T11:00:00Z",
      "from": "vera",
      "body": "Your weekday thali is doing well — 18 orders/day avg. Want me to add a corporate-bulk version?",
      "engagement": "merchant_replied"
    },
    {
      "ts": "2026-04-25T11:30:00Z",
      "from": "merchant",
      "body": "Yes good idea, what would it look like",
      "engagement": "intent_question"
    }
  ],
  "customer_aggregate": {
    "total_unique_ytd": 4200,
    "repeat_customer_pct": 0.42,
    "delivery_share_pct": 0.45
  },
  "signals": [
    "high_volume",
    "stable_growth",
    "engaged_in_last_24h"
  ],
  "review_themes": [
    {
      "theme": "thali_quality",
      "sentiment": "pos",
      "occurrences_30d": 22
    },
    {
      "theme": "weekend_busy",
      "sentiment": "neg",
      "occurrences_30d": 3
    }
  ]
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

- **Audience:** merchant · **send as:** `vera` · **greeting:** Hi Suresh · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "competitor opened"}`

- **Data richness:** rich

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

  - open_merchant_request: merchant is waiting on: Yes good idea, what would it look like

<details><summary>All 38 facts</summary>

- **identity**: Mylari South Indian Cafe; Suresh; Indiranagar, Bangalore; Google profile is verified; in business since 2014
- **performance**: 12,400 profile views in the last 30 days; 88 calls in the last 30 days; 320 direction requests in the last 30 days; 145 leads in the last 30 days; 3.2% CTR over the last 30 days; views +5% over the last 7 days; calls +2% over the last 7 days
- **peer**: CTR 3.2% vs 2.5% peer average, 28% above peers; Profile views 12,400 vs 4,800 peer average, 158% above peers; Calls 88 vs 38 peer average, 132% above peers; Direction requests 320 vs 95 peer average, 237% above peers
- **customers**: 4,200 unique customers this year; repeat-customer share 42%; delivery share of orders 45%
- **offers**: active offers: Weekday Lunch Thali @ ₹149; category offers this merchant hasn't run: Match-night Combo @ ₹399 (food + drink); Family Sunday Brunch @ ₹699/pax; Free Starter on orders > ₹1,200; Free Delivery > ₹500; Birthday: Free Cake on parties of 6+
- **subscription**: Pro plan active, 240 days left
- **reviews**: 22 reviews in the last 30 days mention thali quality (positive); 3 reviews in the last 30 days mention weekend crowding (negative)
- **signals**: high volume; stable growth; engaged with Vera in the last 24 hours
- **category**: peer group: metro casual dining 2026; peers average a 4.2★ rating; peers average 142 reviews; peers post on Google every 7 days on average; peers have 22 photos on average
- **season**: Mar-Apr: IPL season — match-night promos on Tue/Wed/Thu; not weekends
- **trends**: "biryani near me" searches +18% year-on-year; "weekday lunch thali" searches +34% year-on-year (office 25-45); "sugar free dessert" searches +52% year-on-year (age 28-45); "match night offer" searches +65% year-on-year (age 20-40, skews male); "small party catering" searches +22% year-on-year (age 30-50, skews female)

</details>

## 2 · Phase 2: writing brief

- **Family:** event · **angle:** stay calm and competitive: lean on their strengths, not on price

- **Lead (why now):** competitor opened (the trigger gives no details)

- **Supporting facts:**

  - active offers: Weekday Lunch Thali @ ₹149 *(from merchant.offers (status=active))*

  - CTR 3.2% vs 2.5% peer average, 28% above peers *(from merchant.performance.ctr vs category.peer_stats.avg_ctr)*

  - 22 reviews in the last 30 days mention thali quality (positive) *(from merchant.review_themes)*

- **Ask:** yes/no: Want me to draft a Google post on what sets you apart, ready in 10 min?

- **Format:** free-form (`vera_competitor_opened_v1`)

- **Allowed numbers:** 2.5, 3.2, 10, 22, 28, 30, 149

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Suresh, owner of Mylari South Indian Cafe. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Suresh
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: competitor opened (the trigger gives no details)
Supporting facts (use only these):
- active offers: Weekday Lunch Thali @ ₹149
- CTR 3.2% vs 2.5% peer average, 28% above peers
- 22 reviews in the last 30 days mention thali quality (positive)
Angle: stay calm and competitive: lean on their strengths, not on price. Levers: specificity, loss aversion, social proof.
Ask, one only, as the last sentence (yes/no): Kya main ek Google post draft kar doon jo dikhaye ki aap alag kyun hain, 10 min mein ready?
Format: free-form reply allowed.
Rules:
- Voice: warm busy practical, fellow operator.
- Category words you can use (vocabulary only, not facts about this business): footfall, covers, AOV, RPC, table turnover, reservations.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- The trigger (competitor opened) gives no details: mention it only in general terms and build the message on the supporting facts.
- Numbers may only come from: 2.5, 3.2, 10, 22, 28, 30, 149.
- Never use: best food in city, guaranteed packed house, miracle marketing, viral guarantee.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Suresh, a new competitor has opened nearby. Your Weekday Lunch Thali @ ₹149 offer is live. Your CTR is 3.2% vs 2.5% for similar restaurants. Kya main ek Google post draft kar doon jo dikhaye ki aap alag kyun hain, 10 min mein ready?

## 3 · Phase 3: AI writer

> Hi Suresh, competitor open hua hai, par panic ki zaroorat nahi—apni strengths ko clearly dikhate hain. Weekday Lunch Thali ₹149 par live hai, CTR 3.2% hai vs 2.5% peer average, aur last 30 days mein 22 reviews ne thali quality mention ki hai. Kya main ek Google post draft kar doon jo dikhaye ki aap alag kyun hain, 10 min mein ready?

**AI's rationale:** The message acknowledges the competitor without speculation and anchors on the 3.2% CTR, 28% stronger peer comparison, ₹149 thali, and 22 recent quality mentions. It recommends leaning on specificity and social proof rather than price cuts, ending with the requested yes/no ask.

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