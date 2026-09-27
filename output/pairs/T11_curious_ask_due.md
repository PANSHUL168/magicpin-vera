# T11 · curious_ask_due → Lakshmi (Studio11 Family Salon)

**Final message** (sent as `vera`, written by **ai**, ask type `open_ended`):

> Hi Lakshmi, is hafte calls 20% badhe hain, isliye weekly check-in kar rahi hoon. Haircut ₹99 aur Hair Spa ₹499 active offers ke saath, demand ko content mein turn karna useful rahega. Is hafte kis service ki sabse zyada demand rahi? Bataiye, main uska Google post aur price ke sawaalon ke liye ek ready WhatsApp reply bana doongi.

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_008_curious_ask_studio11`

```json
{
  "id": "trg_008_curious_ask_studio11",
  "scope": "merchant",
  "kind": "curious_ask_due",
  "source": "internal",
  "merchant_id": "m_003_studio11_salon_hyderabad",
  "customer_id": null,
  "payload": {
    "ask_template": "what_service_in_demand_this_week",
    "last_ask_at": null
  },
  "urgency": 1,
  "suppression_key": "curious_ask:m_003:2026-W17",
  "expires_at": "2026-05-03T00:00:00Z"
}
```

<details><summary>Merchant <code>m_003_studio11_salon_hyderabad</code> (full record)</summary>

```json
{
  "merchant_id": "m_003_studio11_salon_hyderabad",
  "category_slug": "salons",
  "identity": {
    "name": "Studio11 Family Salon",
    "city": "Hyderabad",
    "locality": "Kapra",
    "place_id": "ChIJ_KAPRA_SALON_003",
    "verified": true,
    "languages": [
      "en",
      "hi",
      "te"
    ],
    "owner_first_name": "Lakshmi",
    "established_year": 2019
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 145
  },
  "performance": {
    "window_days": 30,
    "views": 4980,
    "calls": 62,
    "directions": 142,
    "ctr": 0.048,
    "leads": 38,
    "delta_7d": {
      "views_pct": 0.14,
      "calls_pct": 0.2,
      "ctr_pct": 0.05
    }
  },
  "offers": [
    {
      "id": "o_studio11_001",
      "title": "Haircut @ ₹99",
      "status": "active",
      "started": "2026-03-01"
    },
    {
      "id": "o_studio11_002",
      "title": "Hair Spa @ ₹499",
      "status": "active",
      "started": "2026-03-15"
    }
  ],
  "conversation_history": [
    {
      "ts": "2026-04-22T15:00:00Z",
      "from": "vera",
      "body": "Spotted: bridal-trial searches in Kapra +28% this week. Want me to push your bridal package as a GBP post?",
      "engagement": "merchant_no_reply"
    }
  ],
  "customer_aggregate": {
    "total_unique_ytd": 1150,
    "lapsed_90d_plus": 220,
    "retention_3mo_pct": 0.62
  },
  "signals": [
    "high_engagement",
    "above_peer_median_calls",
    "growing_views_7d"
  ],
  "review_themes": [
    {
      "theme": "stylist_skill",
      "sentiment": "pos",
      "occurrences_30d": 12,
      "common_quote": "Priya is the best for balayage"
    },
    {
      "theme": "saturday_wait",
      "sentiment": "neg",
      "occurrences_30d": 2
    }
  ]
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

- **Audience:** merchant · **send as:** `vera` · **greeting:** Hi Lakshmi · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"ask_template": "what service in demand this week", "last_ask_at": null}`

- **Data richness:** rich

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** none

<details><summary>All 39 facts</summary>

- **identity**: Studio11 Family Salon; Lakshmi; Kapra, Hyderabad; Google profile is verified; in business since 2019
- **performance**: 4,980 profile views in the last 30 days; 62 calls in the last 30 days; 142 direction requests in the last 30 days; 38 leads in the last 30 days; 4.8% CTR over the last 30 days; views +14% over the last 7 days; calls +20% over the last 7 days; CTR +5% over the last 7 days
- **peer**: CTR 4.8% vs 4.0% peer average, 20% above peers; Profile views 4,980 vs 2,400 peer average, 108% above peers; Calls 62 vs 28 peer average, 121% above peers; Direction requests 142 vs 62 peer average, 129% above peers; 3-month retention 62% vs 55% peer average, 7 points above peers
- **customers**: 1,150 unique clients this year; 220 clients not seen in 90+ days; 3-month retention 62%
- **offers**: active offers: Haircut @ ₹99; Hair Spa @ ₹499; category offers this merchant hasn't run: Threading + Waxing combo @ ₹299; Bridal Trial @ ₹999; Keratin Treatment @ ₹2,499; Mani+Pedi Combo @ ₹599; FREE head massage with Haircut
- **subscription**: Pro plan active, 145 days left
- **reviews**: 12 reviews in the last 30 days mention stylist skill (positive): "Priya is the best for balayage"; 2 reviews in the last 30 days mention Saturday waits (negative)
- **signals**: high engagement; calls above the peer benchmark; growing views (7 days)
- **category**: peer group: metro unisex salons 2026; peers average a 4.5★ rating; peers average 88 reviews; peers post on Google every 10 days on average; peers have 14 photos on average
- **season**: Apr-May: secondary bridal window + summer hair-care surge
- **trends**: "balayage near me" searches +45% year-on-year (age 25-40, skews female); "keratin treatment price" searches +18% year-on-year (age 25-45, skews female); "men's haircut delhi" searches +22% year-on-year (age 20-35, skews male); "bridal makeup artist" searches +31% year-on-year (age 22-32, skews female)

</details>

## 2 · Phase 2: writing brief

- **Family:** followup · **angle:** ask one easy question anchored on their own momentum this week, and offer to turn the answer into content while the interest is there

- **Lead (why now):** weekly check-in question: what service in demand this week

- **Supporting facts:**

  - calls +20% over the last 7 days *(from merchant.performance.delta_7d.calls_pct)*

  - active offers: Haircut @ ₹99; Hair Spa @ ₹499 *(from merchant.offers (status=active))*

- **Ask:** open question: Tell me the most asked-for service this week, and I'll turn it into a Google post plus a ready WhatsApp reply for price questions.

- **Format:** pre-approved template (`vera_curious_ask_due_v1`)

- **Allowed numbers:** 7, 11, 20, 99, 499

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Lakshmi, owner of Studio11 Family Salon. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Lakshmi
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: weekly check-in question: what service in demand this week
Supporting facts (use only these):
- calls +20% over the last 7 days
- active offers: Haircut @ ₹99; Hair Spa @ ₹499
Angle: ask one easy question anchored on their own momentum this week, and offer to turn the answer into content while the interest is there. Levers: asking the merchant, reciprocity, curiosity.
Ask, one only, as the last sentence (open question): Is hafte kis service ki sabse zyada demand rahi? Bataiye, main uska Google post aur price ke sawaalon ke liye ek ready WhatsApp reply bana doongi.
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm practical, approachable expert.
- Category words you can use (vocabulary only, not facts about this business): balayage, highlights, keratin, smoothening, hair spa, manicure.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- Numbers may only come from: 7, 11, 20, 99, 499.
- Never use: guaranteed glow, permanent results, instant transformation, miracle, best in city.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Lakshmi, quick question for this week. Calls +20% this week. Is hafte kis service ki sabse zyada demand rahi? Bataiye, main uska Google post aur price ke sawaalon ke liye ek ready WhatsApp reply bana doongi.

## 3 · Phase 3: AI writer

> Hi Lakshmi, is hafte calls 20% badhe hain, isliye weekly check-in kar rahi hoon. Haircut ₹99 aur Hair Spa ₹499 active offers ke saath, demand ko content mein turn karna useful rahega. Is hafte kis service ki sabse zyada demand rahi? Bataiye, main uska Google post aur price ke sawaalon ke liye ek ready WhatsApp reply bana doongi.

**AI's rationale:** Anchors the message on the 20% increase in calls and connects it to the active offers. It uses that momentum to offer practical content support while ending with the required single open question.

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