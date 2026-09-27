# T16 · dormant_with_vera → Anjali (Glamour Lounge Spa & Salon)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Hi Anjali, Salon India magazine (Apr 2026) ke hisaab se formaldehyde-free, citric-acid based smoothening alternatives share gain kar rahe hain. Aapke profile par Keratin Treatment ₹2,499 aur Haircut ₹99 offers nahi hain, aur CTR 2.2% hai versus peers ka 4.0%—inhe highlight karna worth trying lagta hai. Kya main 2 min mein bataun ki yeh aapke liye kaise kaam kar sakta hai?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_025_dormancy_glamour`

```json
{
  "id": "trg_025_dormancy_glamour",
  "scope": "merchant",
  "kind": "dormant_with_vera",
  "source": "internal",
  "merchant_id": "m_004_glamour_salon_pune",
  "customer_id": null,
  "payload": {
    "days_since_last_merchant_message": 38,
    "last_topic": "subscription_expiry"
  },
  "urgency": 2,
  "suppression_key": "dormant:m_004:30d",
  "expires_at": "2026-05-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_004_glamour_salon_pune</code> (full record)</summary>

```json
{
  "merchant_id": "m_004_glamour_salon_pune",
  "category_slug": "salons",
  "identity": {
    "name": "Glamour Lounge Spa & Salon",
    "city": "Pune",
    "locality": "Aundh",
    "place_id": "ChIJ_AUNDH_SALON_004",
    "verified": true,
    "languages": [
      "en",
      "hi",
      "mr"
    ],
    "owner_first_name": "Anjali",
    "established_year": 2021
  },
  "subscription": {
    "status": "expired",
    "plan": "Pro",
    "days_since_expiry": 38
  },
  "performance": {
    "window_days": 30,
    "views": 1200,
    "calls": 8,
    "directions": 22,
    "ctr": 0.022,
    "leads": 3,
    "delta_7d": {
      "views_pct": -0.12,
      "calls_pct": -0.3,
      "ctr_pct": -0.04
    }
  },
  "offers": [],
  "conversation_history": [
    {
      "ts": "2026-03-19T14:00:00Z",
      "from": "vera",
      "body": "Subscription expired. Profile maintenance paused...",
      "engagement": "merchant_no_reply"
    }
  ],
  "customer_aggregate": {
    "total_unique_ytd": 380,
    "lapsed_90d_plus": 180,
    "retention_3mo_pct": 0.32
  },
  "signals": [
    "winback_eligible",
    "perf_dip_post_expiry",
    "dormant_with_vera_38d"
  ],
  "review_themes": []
}
```

</details>

<details><summary>Category <code>salons</code> (key fields)</summary>

```json
{
  "slug": "salons",
  "voice": {
    "tone": "warm_practical",
    "register": "approachable_expert",
    "code_mix": "hindi_english_natural",
    "vocab_allowed": [
      "balayage",
      "highlights",
      "keratin",
      "smoothening",
      "hair spa",
      "manicure",
      "pedicure",
      "facial",
      "threading",
      "waxing",
      "extensions",
      "olaplex",
      "wella",
      "loreal",
      "schwarzkopf",
      "redken"
    ],
    "vocab_taboo": [
      "guaranteed glow",
      "permanent results",
      "instant transformation",
      "miracle",
      "best in city"
    ],
    "salutation_examples": [
      "Hi {first_name}",
      "{salon_name} team"
    ],
    "tone_examples": [
      "Bridal season is starting — bookings usually 2x normal in next 4 weeks",
      "Quick one — your Saturday 5-7pm slot has been the strongest this month"
    ]
  },
  "peer_stats": {
    "scope": "metro_unisex_salons_2026",
    "avg_rating": 4.5,
    "avg_review_count": 88,
    "avg_views_30d": 2400,
    "avg_calls_30d": 28,
    "avg_directions_30d": 62,
    "avg_ctr": 0.04,
    "avg_photos": 14,
    "avg_post_freq_days": 10,
    "retention_3mo_pct": 0.55
  },
  "offer_catalog": [
    "Haircut @ ₹99",
    "FREE head massage with Haircut",
    "Hair Spa @ ₹499",
    "Threading + Waxing combo @ ₹299",
    "Bridal Trial @ ₹999",
    "Keratin Treatment @ ₹2,499",
    "Mani+Pedi Combo @ ₹599",
    "Annual Membership: 12 services @ ₹4,999"
  ],
  "digest (titles)": [
    "Olaplex No.9 launches in India — bond protector for chemically-treated hair",
    "Formaldehyde-free smoothening alternatives gaining share — citric-acid based",
    "Wedding season opener — first lean April-May window before main Oct-Dec rush",
    "L'Oreal Professionnel India training: Advanced Balayage Masterclass",
    "'Walk-in available' tag on GBP boosting calls 23% in metros"
  ],
  "seasonal_beats": [
    {
      "month_range": "Oct-Dec",
      "note": "primary wedding/festival season — bridal package bookings 4x baseline"
    },
    {
      "month_range": "Apr-May",
      "note": "secondary bridal window + summer hair-care surge"
    },
    {
      "month_range": "Jul-Aug",
      "note": "monsoon haircare focus (anti-frizz, scalp treatments)"
    },
    {
      "month_range": "Mar",
      "note": "Holi colour-recovery surge — book hair spas the week after"
    }
  ]
}
```

</details>

**Customer:** none (merchant-facing trigger)

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** merchant · **send as:** `vera` · **greeting:** Hi Anjali · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"days_since_last_merchant_message": "38", "last_topic": "subscription expiry"}`

- **Data richness:** moderate

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** 

  - merchant_not_active: subscription is expired

<details><summary>All 37 facts</summary>

- **identity**: Glamour Lounge Spa & Salon; Anjali; Aundh, Pune; Google profile is verified; in business since 2021
- **performance**: 1,200 profile views in the last 30 days; 8 calls in the last 30 days; 22 direction requests in the last 30 days; 3 leads in the last 30 days; 2.2% CTR over the last 30 days; views -12% over the last 7 days; calls -30% over the last 7 days; CTR -4% over the last 7 days
- **peer**: CTR 2.2% vs 4.0% peer average, 45% below peers; Profile views 1,200 vs 2,400 peer average, 50% below peers; Calls 8 vs 28 peer average, 71% below peers; Direction requests 22 vs 62 peer average, 65% below peers; 3-month retention 32% vs 55% peer average, 23 points below peers
- **customers**: 380 unique clients this year; 180 clients not seen in 90+ days; 3-month retention 32%
- **offers**: no active offers right now; category offers this merchant hasn't run: Haircut @ ₹99; Hair Spa @ ₹499; Threading + Waxing combo @ ₹299; Bridal Trial @ ₹999; Keratin Treatment @ ₹2,499
- **subscription**: subscription expired 38 days ago
- **signals**: eligible for a win-back offer; performance dropped after the subscription expired; no message to Vera in 38 days
- **category**: peer group: metro unisex salons 2026; peers average a 4.5★ rating; peers average 88 reviews; peers post on Google every 10 days on average; peers have 14 photos on average
- **season**: Apr-May: secondary bridal window + summer hair-care surge
- **trends**: "balayage near me" searches +45% year-on-year (age 25-40, skews female); "keratin treatment price" searches +18% year-on-year (age 25-45, skews female); "men's haircut delhi" searches +22% year-on-year (age 20-35, skews male); "bridal makeup artist" searches +31% year-on-year (age 22-32, skews female)

</details>

## 2 · Phase 2: writing brief

- **Family:** account · **angle:** re-open with something genuinely useful; never mention the silence

- **Lead (why now):** Formaldehyde-free smoothening alternatives gaining share — citric-acid based (Salon India magazine, Apr 2026)

- **Supporting facts:**

  - popular category offers not on their profile: Keratin Treatment @ ₹2,499; Haircut @ ₹99 *(from category.offer_catalog minus merchant.offers)*

  - CTR 2.2% vs 4.0% peer average, 45% below peers *(from merchant.performance.ctr vs category.peer_stats.avg_ctr)*

- **Ask:** yes/no: Want me to show how this could work for your business, in 2 min?

- **Format:** pre-approved template (`vera_dormant_with_vera_v1`)

- **Allowed numbers:** 2, 2.2, 4, 45, 99, 2026, 2499

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Anjali, owner of Glamour Lounge Spa & Salon. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Anjali
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: Formaldehyde-free smoothening alternatives gaining share — citric-acid based (Salon India magazine, Apr 2026)
Supporting facts (use only these):
- popular category offers not on their profile: Keratin Treatment @ ₹2,499; Haircut @ ₹99
- CTR 2.2% vs 4.0% peer average, 45% below peers
Angle: re-open with something genuinely useful; never mention the silence. Levers: reciprocity, curiosity, loss aversion.
Ask, one only, as the last sentence (yes/no): Kya main 2 min mein bataun ki yeh aapke liye kaise kaam kar sakta hai?
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm practical, approachable expert.
- Category words you can use (vocabulary only, not facts about this business): balayage, highlights, keratin, smoothening, hair spa, manicure.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- Their subscription is expired: don't promise platform features as if it were active.
- Don't reopen the last topic (subscription expiry) or mention how long they've been quiet.
- Numbers may only come from: 2, 2.2, 4, 45, 99, 2026, 2499.
- Never use: guaranteed glow, permanent results, instant transformation, miracle, best in city.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Anjali, thought you'd want to see this: Formaldehyde-free smoothening alternatives gaining share — citric-acid based (Salon India magazine, Apr 2026). One idea from the category catalog: a "Keratin Treatment @ ₹2,499" offer. Your CTR is 2.2% vs 4.0% for similar salons. Kya main 2 min mein bataun ki yeh aapke liye kaise kaam kar sakta hai?

## 3 · Phase 3: AI writer

> Hi Anjali, Salon India magazine (Apr 2026) ke hisaab se formaldehyde-free, citric-acid based smoothening alternatives share gain kar rahe hain. Aapke profile par Keratin Treatment ₹2,499 aur Haircut ₹99 offers nahi hain, aur CTR 2.2% hai versus peers ka 4.0%—inhe highlight karna worth trying lagta hai. Kya main 2 min mein bataun ki yeh aapke liye kaise kaam kar sakta hai?

**AI's rationale:** The message opens with the timely category shift and anchors the recommendation in the cited source. It connects missing popular offers with the 2.2% versus 4.0% CTR gap, using a practical, low-pressure suggestion and the required yes/no ask.

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