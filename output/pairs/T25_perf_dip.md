# T25 · perf_dip → Sushma (The Beauty Bar)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Hi Sushma, recent performance mein dip dikh raha hai—calls 22 hain, jabki peers ka average 28 hai, yani 21% neeche. Is gap ko address karne ke liye profile par Haircut @ ₹99 aur Hair Spa @ ₹499 jaise popular category offers clearly dikhana practical fix ho sakta hai. Kya main is hafte ke liye do quick fixes bhej doon, 5 min mein?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_031_perf_dip_m_023_sushma_salon_p`

```json
{
  "id": "trg_031_perf_dip_m_023_sushma_salon_p",
  "scope": "merchant",
  "kind": "perf_dip",
  "source": "internal",
  "merchant_id": "m_023_sushma_salon_pune",
  "customer_id": null,
  "payload": {
    "placeholder": true,
    "metric_or_topic": "perf_dip"
  },
  "urgency": 3,
  "suppression_key": "perf_dip:m_023_sushma_salon_pune:gen_31",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_023_sushma_salon_pune</code> (full record)</summary>

```json
{
  "merchant_id": "m_023_sushma_salon_pune",
  "category_slug": "salons",
  "identity": {
    "name": "The Beauty Bar",
    "city": "Pune",
    "locality": "Baner",
    "place_id": "ChIJ_BANER_SALONS_023",
    "verified": true,
    "languages": [
      "en",
      "hi"
    ],
    "owner_first_name": "Sushma",
    "established_year": 2016
  },
  "subscription": {
    "status": "expired",
    "plan": "Pro",
    "days_remaining": 0,
    "days_since_expiry": 39
  },
  "performance": {
    "window_days": 30,
    "views": 2547,
    "calls": 22,
    "directions": 50,
    "ctr": 0.058,
    "leads": 10,
    "delta_7d": {
      "views_pct": 0.08,
      "calls_pct": 0.02
    }
  },
  "offers": [],
  "conversation_history": [],
  "customer_aggregate": {
    "total_unique_ytd": 1454
  },
  "signals": [],
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

- **Audience:** merchant · **send as:** `vera` · **greeting:** Hi Sushma · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "perf dip"}`

- **Data richness:** sparse

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

  - merchant_not_active: subscription is expired

  - sparse_merchant: no offers, history, signals or review themes; anchor on performance, peers and category facts

<details><summary>All 30 facts</summary>

- **identity**: The Beauty Bar; Sushma; Baner, Pune; Google profile is verified; in business since 2016
- **performance**: 2,547 profile views in the last 30 days; 22 calls in the last 30 days; 50 direction requests in the last 30 days; 10 leads in the last 30 days; 5.8% CTR over the last 30 days; views +8% over the last 7 days; calls +2% over the last 7 days
- **peer**: CTR 5.8% vs 4.0% peer average, 45% above peers; Profile views 2,547 vs 2,400 peer average, 6% above peers; Calls 22 vs 28 peer average, 21% below peers; Direction requests 50 vs 62 peer average, 19% below peers
- **customers**: 1,454 unique clients this year
- **offers**: no active offers right now; category offers this merchant hasn't run: Haircut @ ₹99; Hair Spa @ ₹499; Threading + Waxing combo @ ₹299; Bridal Trial @ ₹999; Keratin Treatment @ ₹2,499
- **subscription**: subscription expired 39 days ago
- **category**: peer group: metro unisex salons 2026; peers average a 4.5★ rating; peers average 88 reviews; peers post on Google every 10 days on average; peers have 14 photos on average
- **season**: Apr-May: secondary bridal window + summer hair-care surge
- **trends**: "balayage near me" searches +45% year-on-year (age 25-40, skews female); "keratin treatment price" searches +18% year-on-year (age 25-45, skews female); "men's haircut delhi" searches +22% year-on-year (age 20-35, skews male); "bridal makeup artist" searches +31% year-on-year (age 22-32, skews female)

</details>

## 2 · Phase 2: writing brief

- **Family:** performance · **angle:** name the drop plainly, then offer a concrete fix

- **Lead (why now):** perf dip (the trigger gives no details)

- **Supporting facts:**

  - Calls 22 vs 28 peer average, 21% below peers *(from merchant.performance.calls vs category.peer_stats.avg_calls_30d)*

  - popular category offers not on their profile: Haircut @ ₹99; Hair Spa @ ₹499 *(from category.offer_catalog minus merchant.offers)*

- **Ask:** yes/no: Want two quick fixes you can try this week, drafted in 5 min?

- **Format:** pre-approved template (`vera_perf_dip_v1`)

- **Allowed numbers:** 5, 21, 22, 28, 99, 499

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Sushma, owner of The Beauty Bar. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Sushma
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: perf dip (the trigger gives no details)
Supporting facts (use only these):
- Calls 22 vs 28 peer average, 21% below peers
- popular category offers not on their profile: Haircut @ ₹99; Hair Spa @ ₹499
Angle: name the drop plainly, then offer a concrete fix. Levers: specificity, loss aversion, effort externalization.
Ask, one only, as the last sentence (yes/no): Kya main is hafte ke liye do quick fixes bhej doon, 5 min mein?
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm practical, approachable expert.
- Category words you can use (vocabulary only, not facts about this business): balayage, highlights, keratin, smoothening, hair spa, manicure.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- The trigger (perf dip) gives no details: mention it only in general terms and build the message on the supporting facts.
- Their subscription is expired: don't promise platform features as if it were active.
- There's little merchant-specific data: lean on the comparisons and category facts listed.
- Numbers may only come from: 5, 21, 22, 28, 99, 499.
- Never use: guaranteed glow, permanent results, instant transformation, miracle, best in city.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Sushma, your recent numbers show a dip. Your calls are 22 vs 28 for similar salons. One idea from the category catalog: a "Haircut @ ₹99" offer. Kya main is hafte ke liye do quick fixes bhej doon, 5 min mein?

## 3 · Phase 3: AI writer

> Hi Sushma, recent performance mein dip dikh raha hai—calls 22 hain, jabki peers ka average 28 hai, yani 21% neeche. Is gap ko address karne ke liye profile par Haircut @ ₹99 aur Hair Spa @ ₹499 jaise popular category offers clearly dikhana practical fix ho sakta hai. Kya main is hafte ke liye do quick fixes bhej doon, 5 min mein?

**AI's rationale:** The message plainly names the performance gap and anchors it in the 22 vs 28 peer comparison and 21% figure. It uses specificity and effort externalization by suggesting two concrete profile fixes and offering to prepare them.

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