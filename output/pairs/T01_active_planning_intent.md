# T01 · active_planning_intent → Suresh (Mylari South Indian Cafe)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Hi Suresh, aapne idea pasand kiya, toh 18 orders/day avg ko base maan kar first editable outline bhej rahi hoon:
> - Proposed corporate-bulk version: Weekday Lunch Thali @ ₹149 ko base rakhenge.
> - Order flow: covers, lunch slot aur delivery/pickup details lekar confirmation.
> - 45% orders delivery hain, isliye delivery option bhi include kar sakte hain.
> Kya main ise Google post aur share karne layak WhatsApp mein badal doon, 10 min mein ready?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_013_corporate_thali_planning`

```json
{
  "id": "trg_013_corporate_thali_planning",
  "scope": "merchant",
  "kind": "active_planning_intent",
  "source": "internal",
  "merchant_id": "m_006_southindiancafe_restaurant_bangalore",
  "customer_id": null,
  "payload": {
    "intent_topic": "corporate_bulk_thali_package",
    "merchant_last_message": "Yes good idea, what would it look like"
  },
  "urgency": 4,
  "suppression_key": "planning:m_006:corp_thali:2026-W17",
  "expires_at": "2026-04-29T00:00:00Z"
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

- **Event, made readable:** `{"intent_topic": "corporate bulk thali package", "merchant_last_message": "Yes good idea, what would it look like"}`

- **Data richness:** rich

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** 

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

- **Family:** followup · **angle:** they already said yes: answer 'what would it look like' with a concrete, editable outline in the message itself. Build it on what Vera suggested earlier in the chat when there is one (it's a suggestion, not something they approved, so call prices 'proposed'), plus the listed facts; add structure, timings or ordering steps that fit the idea; use listed offers only if they fit. Never invent facts: no statistics, percentages, named customers, offices or buildings; end by offering the next deliverable; no qualifying questions

- **Lead (why now):** merchant wants a plan for: corporate bulk thali package (their last message: "Yes good idea, what would it look like")

- **Supporting facts:**

  - earlier in this chat Vera said (a suggestion, not something they have approved): "Your weekday thali is doing well — 18 orders/day avg. Want me to add a corporate-bulk version?" *(from merchant.conversation_history)*

  - active offers: Weekday Lunch Thali @ ₹149 *(from merchant.offers (status=active))*

  - delivery share of orders 45% *(from merchant.customer_aggregate.delivery_share_pct)*

- **Ask:** yes/no: Want me to turn this into a Google post and a WhatsApp you can share, ready in 10 min?

- **Format:** free-form (`vera_active_planning_intent_v1`)

- **Allowed numbers:** 10, 18, 45, 149

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Suresh, owner of Mylari South Indian Cafe. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Suresh
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: merchant wants a plan for: corporate bulk thali package (their last message: "Yes good idea, what would it look like")
Supporting facts (use only these):
- earlier in this chat Vera said (a suggestion, not something they have approved): "Your weekday thali is doing well — 18 orders/day avg. Want me to add a corporate-bulk version?"
- active offers: Weekday Lunch Thali @ ₹149
- delivery share of orders 45%
Angle: they already said yes: answer 'what would it look like' with a concrete, editable outline in the message itself. Build it on what Vera suggested earlier in the chat when there is one (it's a suggestion, not something they approved, so call prices 'proposed'), plus the listed facts; add structure, timings or ordering steps that fit the idea; use listed offers only if they fit. Never invent facts: no statistics, percentages, named customers, offices or buildings; end by offering the next deliverable; no qualifying questions. Levers: effort externalization, single binary commitment.
Ask, one only, as the last sentence (yes/no): Kya main ise Google post aur share karne layak WhatsApp mein badal doon, 10 min mein ready?
Format: an editable outline: greeting and one short line of context, then 2-4 short lines starting with '- ', then the ask.
Rules:
- Voice: warm busy practical, fellow operator.
- Category words you can use (vocabulary only, not facts about this business): footfall, covers, AOV, RPC, table turnover, reservations.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- Numbers may only come from: 10, 18, 45, 149.
- Never use: best food in city, guaranteed packed house, miracle marketing, viral guarantee.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Suresh, here's a first cut of your corporate bulk thali package plan. 18 orders/day avg. Your Weekday Lunch Thali @ ₹149 offer is live. Kya main ise Google post aur share karne layak WhatsApp mein badal doon, 10 min mein ready?

## 3 · Phase 3: AI writer

> Hi Suresh, aapne idea pasand kiya, toh 18 orders/day avg ko base maan kar first editable outline bhej rahi hoon:
> - Proposed corporate-bulk version: Weekday Lunch Thali @ ₹149 ko base rakhenge.
> - Order flow: covers, lunch slot aur delivery/pickup details lekar confirmation.
> - 45% orders delivery hain, isliye delivery option bhi include kar sakte hain.
> Kya main ise Google post aur share karne layak WhatsApp mein badal doon, 10 min mein ready?

**AI's rationale:** The message turns the approved idea into an editable package outline, anchored on 18 daily orders, the ₹149 thali, and 45% delivery share. It uses a single yes/no commitment for the next deliverable.

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