# T04 · appointment_tomorrow → Riya (Beauty Lounge by Renu)

**Final message** (sent as `merchant_on_behalf`, written by **ai**, ask type `binary_confirm_cancel`):

> Hi Riya
> Beauty Lounge by Renu se, kal ke appointment ke liye short confirmation bhej rahe hain. 1 Sep 2025 se aapki 2 visits ke liye dhanyavaad. Confirm karne ke liye YES reply kijiye, ya reschedule ke liye bataiye.

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_077_appointment_tomorrow_m_020_renu_salon_luc`

```json
{
  "id": "trg_077_appointment_tomorrow_m_020_renu_salon_luc",
  "scope": "customer",
  "kind": "appointment_tomorrow",
  "source": "internal",
  "merchant_id": "m_020_renu_salon_lucknow",
  "customer_id": "c_080_riya_for_m_020_renu_salon_lucknow",
  "payload": {
    "placeholder": true,
    "metric_or_topic": "appointment_tomorrow"
  },
  "urgency": 2,
  "suppression_key": "appointment_tomorrow:m_020_renu_salon_lucknow:gen_77",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_020_renu_salon_lucknow</code> (full record)</summary>

```json
{
  "merchant_id": "m_020_renu_salon_lucknow",
  "category_slug": "salons",
  "identity": {
    "name": "Beauty Lounge by Renu",
    "city": "Lucknow",
    "locality": "Gomti Nagar",
    "place_id": "ChIJ_GOMTI_NAGAR_SALONS_020",
    "verified": true,
    "languages": [
      "en",
      "hi"
    ],
    "owner_first_name": "Renu",
    "established_year": 2015
  },
  "subscription": {
    "status": "expired",
    "plan": "Pro",
    "days_remaining": 0,
    "days_since_expiry": 41
  },
  "performance": {
    "window_days": 30,
    "views": 2945,
    "calls": 33,
    "directions": 93,
    "ctr": 0.051,
    "leads": 29,
    "delta_7d": {
      "views_pct": 0.04,
      "calls_pct": -0.18
    }
  },
  "offers": [],
  "conversation_history": [],
  "customer_aggregate": {
    "total_unique_ytd": 1062
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

<details><summary>Customer <code>c_080_riya_for_m_020_renu_salon_lucknow</code></summary>

```json
{
  "customer_id": "c_080_riya_for_m_020_renu_salon_lucknow",
  "merchant_id": "m_020_renu_salon_lucknow",
  "identity": {
    "name": "Riya",
    "phone_redacted": "<phone>",
    "language_pref": "hi",
    "age_band": "20-25"
  },
  "relationship": {
    "first_visit": "2025-09-01",
    "last_visit": "2026-04-01",
    "visits_total": 2,
    "services_received": [],
    "lifetime_value": 1656
  },
  "state": "active",
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

- **Audience:** customer · **send as:** `merchant_on_behalf` · **greeting:** Hi Riya · **language:** Hindi

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "appointment tomorrow"}`

- **Data richness:** sparse

- **Digest item:** none

- **Slots:** none

- **Consent:** appointment_tomorrow needs one of appointment_reminders; customer consented only to promotional_offers

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

  - merchant_not_active: subscription is expired; this message goes out on their behalf

  - consent_gap: appointment_tomorrow needs one of appointment_reminders; customer consented only to promotional_offers

  - sparse_merchant: no offers, history, signals or review themes; anchor on performance, peers and category facts

<details><summary>All 39 facts</summary>

- **identity**: Beauty Lounge by Renu; Renu; Gomti Nagar, Lucknow; Google profile is verified; in business since 2015
- **performance**: 2,945 profile views in the last 30 days; 33 calls in the last 30 days; 93 direction requests in the last 30 days; 29 leads in the last 30 days; 5.1% CTR over the last 30 days; views +4% over the last 7 days; calls -18% over the last 7 days
- **peer**: CTR 5.1% vs 4.0% peer average, 27% above peers; Profile views 2,945 vs 2,400 peer average, 23% above peers; Calls 33 vs 28 peer average, 18% above peers; Direction requests 93 vs 62 peer average, 50% above peers
- **customers**: 1,062 unique clients this year
- **offers**: no active offers right now; category offers this merchant hasn't run: Haircut @ ₹99; Hair Spa @ ₹499; Threading + Waxing combo @ ₹299; Bridal Trial @ ₹999; Keratin Treatment @ ₹2,499
- **subscription**: subscription expired 41 days ago
- **category**: peer group: metro unisex salons 2026; peers average a 4.5★ rating; peers average 88 reviews; peers post on Google every 10 days on average; peers have 14 photos on average
- **season**: Apr-May: secondary bridal window + summer hair-care surge
- **trends**: "balayage near me" searches +45% year-on-year (age 25-40, skews female); "keratin treatment price" searches +18% year-on-year (age 25-45, skews female); "men's haircut delhi" searches +22% year-on-year (age 20-35, skews male); "bridal makeup artist" searches +31% year-on-year (age 22-32, skews female)
- **customer**: Riya; age group 20-25; customer status: active; 2 visits since 1 Sep 2025; last visit 1 Apr 2026; 25 days since the last visit; ₹1,656 spent so far
- **consent**: consented on 1 Sep 2025 to: promotional offers; opted in to reminders

</details>

## 2 · Phase 2: writing brief

- **Family:** customer · **angle:** a short, clear confirmation

- **Lead (why now):** appointment tomorrow (the trigger gives no time)

- **Supporting facts:**

  - 2 visits since 1 Sep 2025 *(from customer.relationship.visits_total)*

- **Ask:** confirm: Reply YES to confirm, or let us know if you need to reschedule.

- **Format:** pre-approved template (`merchant_appointment_tomorrow_v1`)

- **Allowed numbers:** 1, 2, 2025

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Riya, a customer of Beauty Lounge by Renu. Sent as: Beauty Lounge by Renu, on the shop's behalf (not Vera).
Greeting: Hi Riya
Language: Simple Hindi in Roman script; everyday English words are fine.
Why now: appointment tomorrow (the trigger gives no time)
Supporting facts (use only these):
- 2 visits since 1 Sep 2025
Angle: a short, clear confirmation. Levers: single binary commitment.
Ask, one only, as the last sentence (confirm): Confirm karne ke liye YES reply kijiye, ya reschedule ke liye bataiye.
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm, clear and respectful, like the shop's front desk writing to a regular customer.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Write as Beauty Lounge by Renu, not as Vera. No medical or guaranteed-result claims.
- The trigger (appointment tomorrow) gives no details: mention it only in general terms and build the message on the supporting facts.
- The customer only agreed to promotional offers: keep it to a brief, non-promotional note about their own booking.
- Their subscription is expired: don't promise platform features as if it were active.
- There's little merchant-specific data: lean on the comparisons and category facts listed.
- Numbers may only come from: 1, 2, 2025.
- Never use: guaranteed glow, permanent results, instant transformation, miracle, best in city.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Riya, Beauty Lounge by Renu here. Yaad dila dein, kal aapka appointment hai. 1 Sep 2025 se ab tak 2 visits ke liye shukriya. Confirm karne ke liye YES reply kijiye, ya reschedule ke liye bataiye.

## 3 · Phase 3: AI writer

> Hi Riya
> Beauty Lounge by Renu se, kal ke appointment ke liye short confirmation bhej rahe hain. 1 Sep 2025 se aapki 2 visits ke liye dhanyavaad. Confirm karne ke liye YES reply kijiye, ya reschedule ke liye bataiye.

**AI's rationale:** This keeps the note brief and personal, anchoring it on tomorrow’s appointment and Riya’s 2 visits since 1 Sep 2025. It ends with the requested single confirmation/rescheduling ask.

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
| Has a concrete number, date or price | ➖ customer message | ➖ customer message |
| Ends with the ask | ✅ | ✅ |
| Not copied from a case study | ✅ | ✅ |
| Under 600 characters | ✅ | ✅ |
| Language as expected *(advisory)* | ✅ | ✅ |