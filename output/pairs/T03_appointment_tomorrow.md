# T03 · appointment_tomorrow → Aditya (Karim's Salon)

**Final message** (sent as `merchant_on_behalf`, written by **ai**, ask type `binary_confirm_cancel`):

> Hi Aditya, your appointment at Karim's Salon is tomorrow. We’re looking forward to seeing you. Reply YES to confirm, or let us know if you need to reschedule.

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_076_appointment_tomorrow_m_019_karim_salon_lu`

```json
{
  "id": "trg_076_appointment_tomorrow_m_019_karim_salon_lu",
  "scope": "customer",
  "kind": "appointment_tomorrow",
  "source": "internal",
  "merchant_id": "m_019_karim_salon_lucknow",
  "customer_id": "c_075_aditya_for_m_019_karim_salon_lucknow",
  "payload": {
    "placeholder": true,
    "metric_or_topic": "appointment_tomorrow"
  },
  "urgency": 2,
  "suppression_key": "appointment_tomorrow:m_019_karim_salon_lucknow:gen_76",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_019_karim_salon_lucknow</code> (full record)</summary>

```json
{
  "merchant_id": "m_019_karim_salon_lucknow",
  "category_slug": "salons",
  "identity": {
    "name": "Karim's Salon",
    "city": "Lucknow",
    "locality": "Alambagh",
    "place_id": "ChIJ_ALAMBAGH_SALONS_019",
    "verified": true,
    "languages": [
      "en",
      "hi"
    ],
    "owner_first_name": "Karim",
    "established_year": 2013
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 9,
    "days_since_expiry": null
  },
  "performance": {
    "window_days": 30,
    "views": 756,
    "calls": 2,
    "directions": 31,
    "ctr": 0.038,
    "leads": 1,
    "delta_7d": {
      "views_pct": 0.26,
      "calls_pct": 0.23
    }
  },
  "offers": [],
  "conversation_history": [],
  "customer_aggregate": {
    "total_unique_ytd": 1509
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

<details><summary>Customer <code>c_075_aditya_for_m_019_karim_salon_lucknow</code></summary>

```json
{
  "customer_id": "c_075_aditya_for_m_019_karim_salon_lucknow",
  "merchant_id": "m_019_karim_salon_lucknow",
  "identity": {
    "name": "Aditya",
    "phone_redacted": "<phone>",
    "language_pref": "en",
    "age_band": "20-25"
  },
  "relationship": {
    "first_visit": "2025-09-01",
    "last_visit": "2026-04-01",
    "visits_total": 1,
    "services_received": [],
    "lifetime_value": 284
  },
  "state": "lapsed_hard",
  "preferences": {
    "channel": "whatsapp",
    "reminder_opt_in": true
  },
  "consent": {
    "opted_in_at": "2025-09-01",
    "scope": [
      "promotional_offers"
    ]
  }
}
```

</details>

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** customer · **send as:** `merchant_on_behalf` · **greeting:** Hi Aditya · **language:** English

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "appointment tomorrow"}`

- **Data richness:** sparse

- **Digest item:** none

- **Slots:** none

- **Consent:** appointment_tomorrow needs one of appointment_reminders; customer consented only to promotional_offers

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

  - consent_gap: appointment_tomorrow needs one of appointment_reminders; customer consented only to promotional_offers

  - sparse_merchant: no offers, history, signals or review themes; anchor on performance, peers and category facts

<details><summary>All 39 facts</summary>

- **identity**: Karim's Salon; Karim; Alambagh, Lucknow; Google profile is verified; in business since 2013
- **performance**: 756 profile views in the last 30 days; 2 calls in the last 30 days; 31 direction requests in the last 30 days; 1 leads in the last 30 days; 3.8% CTR over the last 30 days; views +26% over the last 7 days; calls +23% over the last 7 days
- **peer**: CTR 3.8% vs 4.0% peer average, in line with peers; Profile views 756 vs 2,400 peer average, 68% below peers; Calls 2 vs 28 peer average, 93% below peers; Direction requests 31 vs 62 peer average, 50% below peers
- **customers**: 1,509 unique clients this year
- **offers**: no active offers right now; category offers this merchant hasn't run: Haircut @ ₹99; Hair Spa @ ₹499; Threading + Waxing combo @ ₹299; Bridal Trial @ ₹999; Keratin Treatment @ ₹2,499
- **subscription**: Pro plan active, 9 days left
- **category**: peer group: metro unisex salons 2026; peers average a 4.5★ rating; peers average 88 reviews; peers post on Google every 10 days on average; peers have 14 photos on average
- **season**: Apr-May: secondary bridal window + summer hair-care surge
- **trends**: "balayage near me" searches +45% year-on-year (age 25-40, skews female); "keratin treatment price" searches +18% year-on-year (age 25-45, skews female); "men's haircut delhi" searches +22% year-on-year (age 20-35, skews male); "bridal makeup artist" searches +31% year-on-year (age 22-32, skews female)
- **customer**: Aditya; age group 20-25; customer status: lapsed for a long time; 1 visit since 1 Sep 2025; last visit 1 Apr 2026; 25 days since the last visit; ₹284 spent so far
- **consent**: consented on 1 Sep 2025 to: promotional offers; opted in to reminders

</details>

## 2 · Phase 2: writing brief

- **Family:** customer · **angle:** a short, clear confirmation

- **Lead (why now):** appointment tomorrow (the trigger gives no time)

- **Supporting facts:**

- **Ask:** confirm: Reply YES to confirm, or let us know if you need to reschedule.

- **Format:** pre-approved template (`merchant_appointment_tomorrow_v1`)

- **Allowed numbers:** none

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Aditya, a customer of Karim's Salon. Sent as: Karim's Salon, on the shop's behalf (not Vera).
Greeting: Hi Aditya
Language: English.
Why now: appointment tomorrow (the trigger gives no time)
Supporting facts (use only these):
Angle: a short, clear confirmation. Levers: single binary commitment.
Ask, one only, as the last sentence (confirm): Reply YES to confirm, or let us know if you need to reschedule.
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm, clear and respectful, like the shop's front desk writing to a regular customer.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Write as Karim's Salon, not as Vera. No medical or guaranteed-result claims.
- The trigger (appointment tomorrow) gives no details: mention it only in general terms and build the message on the supporting facts.
- The customer only agreed to promotional offers: keep it to a brief, non-promotional note about their own booking.
- There's little merchant-specific data: lean on the comparisons and category facts listed.
- Numbers may only come from: none.
- Never use: guaranteed glow, permanent results, instant transformation, miracle, best in city.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Aditya, Karim's Salon here. A quick reminder that your appointment with us is tomorrow. Reply YES to confirm, or let us know if you need to reschedule.

## 3 · Phase 3: AI writer

> Hi Aditya, your appointment at Karim's Salon is tomorrow. We’re looking forward to seeing you. Reply YES to confirm, or let us know if you need to reschedule.

**AI's rationale:** This keeps the message warm, brief, and focused on the customer’s appointment tomorrow. It ends with the single requested binary confirmation ask.

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
| Customer message speaks as the shop | ✅ | ✅ |
| Customer message names the shop | ✅ | ✅ |
| Addresses them by name | ✅ | ✅ |
| Has a concrete number, date or price | ➖ the brief has no numbers | ➖ the brief has no numbers |
| Ends with the ask | ✅ | ✅ |
| Not copied from a case study | ✅ | ✅ |
| Under 600 characters | ✅ | ✅ |
| Language as expected *(advisory)* | ✅ | ✅ |