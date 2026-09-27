# T12 · curious_ask_due → Suresh (Mylari South Indian Cafe)

**Final message** (sent as `vera`, written by **ai**, ask type `open_ended`):

> Hi Suresh, weekly check-in: Mylari South Indian Cafe ke views pichhle 7 din mein 5% badhe hain, aur Weekday Lunch Thali ₹149 par active hai. Interest bana hua hai—kis dish ki sabse zyada demand rahi? Bataiye, main uska Google post aur price ke sawaalon ke liye ek ready WhatsApp reply bana doongi.

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_096_curious_ask_due_m_006_southindiancaf`

```json
{
  "id": "trg_096_curious_ask_due_m_006_southindiancaf",
  "scope": "merchant",
  "kind": "curious_ask_due",
  "source": "internal",
  "merchant_id": "m_006_southindiancafe_restaurant_bangalore",
  "customer_id": null,
  "payload": {
    "placeholder": true,
    "metric_or_topic": "curious_ask_due"
  },
  "urgency": 1,
  "suppression_key": "curious_ask_due:m_006_southindiancafe_restaurant_bangalore:gen_96",
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

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "curious ask due"}`

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

- **Family:** followup · **angle:** ask one easy question anchored on their own momentum this week, and offer to turn the answer into content while the interest is there

- **Lead (why now):** weekly check-in question

- **Supporting facts:**

  - views +5% over the last 7 days *(from merchant.performance.delta_7d.views_pct)*

  - active offers: Weekday Lunch Thali @ ₹149 *(from merchant.offers (status=active))*

- **Ask:** open question: Tell me the most asked-for dish this week, and I'll turn it into a Google post plus a ready WhatsApp reply for price questions.

- **Format:** free-form (`vera_curious_ask_due_v1`)

- **Allowed numbers:** 5, 7, 149

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Suresh, owner of Mylari South Indian Cafe. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Suresh
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: weekly check-in question
Supporting facts (use only these):
- views +5% over the last 7 days
- active offers: Weekday Lunch Thali @ ₹149
Angle: ask one easy question anchored on their own momentum this week, and offer to turn the answer into content while the interest is there. Levers: asking the merchant, reciprocity, curiosity.
Ask, one only, as the last sentence (open question): Is hafte kis dish ki sabse zyada demand rahi? Bataiye, main uska Google post aur price ke sawaalon ke liye ek ready WhatsApp reply bana doongi.
Format: free-form reply allowed.
Rules:
- Voice: warm busy practical, fellow operator.
- Category words you can use (vocabulary only, not facts about this business): footfall, covers, AOV, RPC, table turnover, reservations.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- The trigger (curious ask due) gives no details: mention it only in general terms and build the message on the supporting facts.
- Numbers may only come from: 5, 7, 149.
- Never use: best food in city, guaranteed packed house, miracle marketing, viral guarantee.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Suresh, quick question for this week. Views +5% this week. Is hafte kis dish ki sabse zyada demand rahi? Bataiye, main uska Google post aur price ke sawaalon ke liye ek ready WhatsApp reply bana doongi.

## 3 · Phase 3: AI writer

> Hi Suresh, weekly check-in: Mylari South Indian Cafe ke views pichhle 7 din mein 5% badhe hain, aur Weekday Lunch Thali ₹149 par active hai. Interest bana hua hai—kis dish ki sabse zyada demand rahi? Bataiye, main uska Google post aur price ke sawaalon ke liye ek ready WhatsApp reply bana doongi.

**AI's rationale:** Anchors the check-in on the 5% seven-day view increase and the active ₹149 offer, then connects that momentum to a practical content follow-up. Ends with the single requested open question and deliverable.

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