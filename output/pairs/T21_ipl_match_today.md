# T21 · ipl_match_today → Suresh (SK Pizza Junction)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Hi Suresh, aaj Sun 26 Apr ko 7:30pm DC vs MI hai Arun Jaitley Stadium mein. Weekend match ke liye dine-in promo skip karna better rahega—magicpin order data (Apr 2026) mein Saturday IPL matches par covers Saturday average se 12% down rahe; isliye existing Buy 1 Pizza Get 1 Free ko aaj delivery-only exception bana sakte hain. Kya main aaj raat ke liye delivery-only match special, banner aur Insta story ke saath, draft kar doon?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_010_ipl_match_delhi`

```json
{
  "id": "trg_010_ipl_match_delhi",
  "scope": "merchant",
  "kind": "ipl_match_today",
  "source": "external",
  "merchant_id": "m_005_pizzajunction_restaurant_delhi",
  "customer_id": null,
  "payload": {
    "match": "DC vs MI",
    "venue": "Arun Jaitley Stadium",
    "city": "Delhi",
    "match_time_iso": "2026-04-26T19:30:00+05:30",
    "is_weeknight": false
  },
  "urgency": 3,
  "suppression_key": "ipl:m_005:2026-04-26",
  "expires_at": "2026-04-26T23:59:59+05:30"
}
```

<details><summary>Merchant <code>m_005_pizzajunction_restaurant_delhi</code> (full record)</summary>

```json
{
  "merchant_id": "m_005_pizzajunction_restaurant_delhi",
  "category_slug": "restaurants",
  "identity": {
    "name": "SK Pizza Junction",
    "city": "Delhi",
    "locality": "Sant Nagar",
    "place_id": "ChIJ_SANTNAGAR_RESTAURANT_005",
    "verified": false,
    "languages": [
      "en",
      "hi"
    ],
    "owner_first_name": "Suresh",
    "established_year": 2022
  },
  "subscription": {
    "status": "trial",
    "plan": "Trial",
    "days_remaining": 7
  },
  "performance": {
    "window_days": 30,
    "views": 2200,
    "calls": 12,
    "directions": 38,
    "ctr": 0.02,
    "leads": 4,
    "delta_7d": {
      "views_pct": 0.08,
      "calls_pct": 0.1
    }
  },
  "offers": [
    {
      "id": "o_skpz_001",
      "title": "Buy 1 Pizza Get 1 Free (Tue-Thu)",
      "status": "active",
      "started": "2026-04-15"
    }
  ],
  "conversation_history": [
    {
      "ts": "2026-04-25T18:00:00Z",
      "from": "vera",
      "body": "Quick check — IPL match nights driving any extra footfall?",
      "engagement": "merchant_no_reply"
    }
  ],
  "customer_aggregate": {
    "total_unique_ytd": 0,
    "delivery_orders_30d": 180,
    "dine_in_orders_30d": 95
  },
  "signals": [
    "new_merchant",
    "trial_ending_soon",
    "ipl_eligible_locality"
  ],
  "review_themes": [
    {
      "theme": "delivery_late",
      "sentiment": "neg",
      "occurrences_30d": 4
    },
    {
      "theme": "pizza_quality",
      "sentiment": "pos",
      "occurrences_30d": 8
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

- **Event, made readable:** `{"match": "DC vs MI", "venue": "Arun Jaitley Stadium", "city": "Delhi", "match_time_iso": "Sun 26 Apr, 7:30pm", "is_weeknight": false}`

- **Data richness:** rich

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** 

  - merchant_not_active: subscription is trial

<details><summary>All 38 facts</summary>

- **identity**: SK Pizza Junction; Suresh; Sant Nagar, Delhi; Google profile is not verified; in business since 2022
- **performance**: 2,200 profile views in the last 30 days; 12 calls in the last 30 days; 38 direction requests in the last 30 days; 4 leads in the last 30 days; 2% CTR over the last 30 days; views +8% over the last 7 days; calls +10% over the last 7 days
- **peer**: CTR 2.0% vs 2.5% peer average, 20% below peers; Profile views 2,200 vs 4,800 peer average, 54% below peers; Calls 12 vs 38 peer average, 68% below peers; Direction requests 38 vs 95 peer average, 60% below peers
- **customers**: 0 unique customers this year; 180 delivery orders in the last 30 days; 95 dine-in orders in the last 30 days
- **offers**: active offers: Buy 1 Pizza Get 1 Free (Tue-Thu); category offers this merchant hasn't run: Weekday Lunch Thali @ ₹149; Match-night Combo @ ₹399 (food + drink); Family Sunday Brunch @ ₹699/pax; Free Starter on orders > ₹1,200; Free Delivery > ₹500
- **subscription**: on a trial, 7 days left
- **reviews**: 4 reviews in the last 30 days mention late delivery (negative); 8 reviews in the last 30 days mention pizza quality (positive)
- **signals**: new on magicpin; trial ending soon; IPL eligible locality
- **category**: peer group: metro casual dining 2026; peers average a 4.2★ rating; peers average 142 reviews; peers post on Google every 7 days on average; peers have 22 photos on average
- **season**: Mar-Apr: IPL season — match-night promos on Tue/Wed/Thu; not weekends
- **trends**: "biryani near me" searches +18% year-on-year; "weekday lunch thali" searches +34% year-on-year (office 25-45); "sugar free dessert" searches +52% year-on-year (age 28-45); "match night offer" searches +65% year-on-year (age 20-40, skews male); "small party catering" searches +22% year-on-year (age 30-50, skews female)

</details>

## 2 · Phase 2: writing brief

- **Family:** event · **angle:** a weekend match: the category's IPL guidance says match-night promos work Tue-Thu, not weekends, so skip dine-in promos tonight; propose running their existing offer as a delivery-only special for the match, as an exception for them to approve (it normally runs Tue-Thu)

- **Lead (why now):** DC vs MI at Arun Jaitley Stadium, Sun 26 Apr, 7:30pm; not a weeknight match

- **Supporting facts:**

  - Mar-Apr: IPL season — match-night promos on Tue/Wed/Thu; not weekends *(from category.seasonal_beats)*

  - IPL home-match Saturdays underperformed weeknight matches across metros (magicpin order data, Apr 2026): Saturday IPL matches shift orders to home-watch parties; restaurant covers down 12% vs Saturday average *(from category.digest[d_2026W17_ipl_window])*

  - active offers: Buy 1 Pizza Get 1 Free (Tue-Thu) (doesn't run on Sunday, the match day) *(from merchant.offers (status=active))*

- **Ask:** yes/no: Want me to draft a delivery-only match-night special, with a banner and an Insta story?

- **Format:** pre-approved template (`vera_ipl_match_today_v1`)

- **Allowed numbers:** 1, 7, 12, 26, 30, 2026

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Suresh, owner of SK Pizza Junction. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Suresh
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: DC vs MI at Arun Jaitley Stadium, Sun 26 Apr, 7:30pm; not a weeknight match
Supporting facts (use only these):
- Mar-Apr: IPL season — match-night promos on Tue/Wed/Thu; not weekends
- IPL home-match Saturdays underperformed weeknight matches across metros (magicpin order data, Apr 2026): Saturday IPL matches shift orders to home-watch parties; restaurant covers down 12% vs Saturday average
- active offers: Buy 1 Pizza Get 1 Free (Tue-Thu) (doesn't run on Sunday, the match day)
Angle: a weekend match: the category's IPL guidance says match-night promos work Tue-Thu, not weekends, so skip dine-in promos tonight; propose running their existing offer as a delivery-only special for the match, as an exception for them to approve (it normally runs Tue-Thu). Levers: specificity, curiosity.
Ask, one only, as the last sentence (yes/no): Kya main aaj raat ke liye delivery-only match special, banner aur Insta story ke saath, draft kar doon?
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm busy practical, fellow operator.
- Category words you can use (vocabulary only, not facts about this business): footfall, covers, AOV, RPC, table turnover, reservations.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- Their subscription is trial: don't promise platform features as if it were active.
- This is a weekend match, not a weeknight one: steer them away from dine-in promos and toward delivery for tonight.
- The order data is about Saturday matches and this match is on a Sunday: quote it as Saturday data (both are weekend matches), not as a figure for today.
- Numbers may only come from: 1, 7, 12, 26, 30, 2026.
- Never use: best food in city, guaranteed packed house, miracle marketing, viral guarantee.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Suresh, DC vs MI is on at Arun Jaitley Stadium today (Sun 26 Apr, 7:30pm). The usual Mar-Apr pattern: IPL season — match-night promos on Tue/Wed/Thu; not weekends. Saturday IPL matches shift orders to home-watch parties; restaurant covers down 12% vs Saturday average (magicpin order data, Apr 2026). Kya main aaj raat ke liye delivery-only match special, banner aur Insta story ke saath, draft kar doon?

## 3 · Phase 3: AI writer

> Hi Suresh, aaj Sun 26 Apr ko 7:30pm DC vs MI hai Arun Jaitley Stadium mein. Weekend match ke liye dine-in promo skip karna better rahega—magicpin order data (Apr 2026) mein Saturday IPL matches par covers Saturday average se 12% down rahe; isliye existing Buy 1 Pizza Get 1 Free ko aaj delivery-only exception bana sakte hain. Kya main aaj raat ke liye delivery-only match special, banner aur Insta story ke saath, draft kar doon?

**AI's rationale:** The message anchors on the Sunday match and the 12% Saturday IPL covers decline from magicpin’s April 2026 data. It uses the practical lever of shifting the existing Tue-Thu offer to a delivery-only exception instead of pushing dine-in.

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