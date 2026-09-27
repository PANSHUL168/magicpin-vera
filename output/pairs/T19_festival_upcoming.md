# T19 · festival_upcoming → Pooja (Bend & Burn)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Hi Pooja, festival season aa raha hai—plan early karna smart rahega. Category mein First Month @ ₹499 aur Personal Training Demo @ ₹199 jaise clear offers profile par nahi hain, while your CTR is 4.2% vs 4.5% peer average (7% lower). Want me to draft a festive offer, a Google post and a WhatsApp blast for you?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_061_festival_upcoming_m_037_pooja_gym_bang`

```json
{
  "id": "trg_061_festival_upcoming_m_037_pooja_gym_bang",
  "scope": "merchant",
  "kind": "festival_upcoming",
  "source": "external",
  "merchant_id": "m_037_pooja_gym_bangalore",
  "customer_id": null,
  "payload": {
    "placeholder": true,
    "metric_or_topic": "festival_upcoming"
  },
  "urgency": 1,
  "suppression_key": "festival_upcoming:m_037_pooja_gym_bangalore:gen_61",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_037_pooja_gym_bangalore</code> (full record)</summary>

```json
{
  "merchant_id": "m_037_pooja_gym_bangalore",
  "category_slug": "gyms",
  "identity": {
    "name": "Bend & Burn",
    "city": "Bangalore",
    "locality": "Koramangala",
    "place_id": "ChIJ_KORAMANGALA_GYMS_037",
    "verified": true,
    "languages": [
      "en",
      "hi",
      "kn"
    ],
    "owner_first_name": "Pooja",
    "established_year": 2019
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 162,
    "days_since_expiry": null
  },
  "performance": {
    "window_days": 30,
    "views": 5934,
    "calls": 65,
    "directions": 148,
    "ctr": 0.042,
    "leads": 31,
    "delta_7d": {
      "views_pct": -0.07,
      "calls_pct": 0.06
    }
  },
  "offers": [],
  "conversation_history": [],
  "customer_aggregate": {
    "total_unique_ytd": 387
  },
  "signals": [],
  "review_themes": []
}
```

</details>

<details><summary>Category <code>gyms</code> (key fields)</summary>

```json
{
  "slug": "gyms",
  "voice": {
    "tone": "energetic_disciplined",
    "register": "coach_to_member",
    "code_mix": "english_primary_some_hindi",
    "vocab_allowed": [
      "footfall",
      "membership churn",
      "PT sessions",
      "PR (personal record)",
      "1RM",
      "EMOM",
      "AMRAP",
      "split",
      "cut",
      "bulk",
      "BMR",
      "VO2max",
      "functional",
      "HIIT",
      "CrossFit",
      "yoga",
      "pilates"
    ],
    "vocab_taboo": [
      "guaranteed weight loss",
      "shred in 7 days",
      "miracle transformation",
      "fastest results"
    ],
    "salutation_examples": [
      "Hi {first_name}",
      "{gym_name} team",
      "Coach"
    ],
    "tone_examples": [
      "Quick check — your weekday 7-9pm slot has been at 90%+ capacity all month",
      "Footfall pattern: April drop-off is normal; bookings recover by 2nd week May"
    ]
  },
  "peer_stats": {
    "scope": "metro_neighbourhood_gyms_2026",
    "avg_rating": 4.5,
    "avg_review_count": 56,
    "avg_views_30d": 1100,
    "avg_calls_30d": 18,
    "avg_directions_30d": 42,
    "avg_ctr": 0.045,
    "avg_photos": 16,
    "avg_post_freq_days": 12,
    "monthly_churn_pct": 0.08,
    "trial_to_paid_pct": 0.32
  },
  "offer_catalog": [
    "3 FREE Trial Classes",
    "First Month @ ₹499",
    "Personal Training Demo @ ₹199",
    "Annual Membership @ ₹14,999 (save ₹6,000)",
    "Couple/Family Plan @ ₹999/month",
    "Free Body Composition Analysis",
    "Refer-a-friend: 1 month free for both",
    "Yoga + Strength Combo @ ₹1,499/month"
  ],
  "digest (titles)": [
    "Post-Jan resolution window closing — last 2 weeks of high trial-walk-ins",
    "Personal Training inquiries +38% YoY in 30-50 corporate cohort",
    "Boutique yoga/pilates studios opening fast in metro neighbourhoods",
    "ICMR creatine supplementation safety bulletin — adolescent guidance",
    "Schedule density study — peak slots underutilized in mornings"
  ],
  "seasonal_beats": [
    {
      "month_range": "Jan",
      "note": "resolution surge — trial walk-ins 4x baseline; convert window"
    },
    {
      "month_range": "Apr-Jun",
      "note": "lowest acquisition window — focus on retention, not acquisition"
    },
    {
      "month_range": "Aug-Oct",
      "note": "wedding-prep + festival window — repeat clients return to shape up"
    },
    {
      "month_range": "Nov-Dec",
      "note": "holiday slowdown — class density drops 25%; right time to renovate or pilot new programs"
    }
  ]
}
```

</details>

**Customer:** none (merchant-facing trigger)

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** merchant · **send as:** `vera` · **greeting:** Hi Pooja · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "festival upcoming"}`

- **Data richness:** sparse

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

  - sparse_merchant: no offers, history, signals or review themes; anchor on performance, peers and category facts

<details><summary>All 30 facts</summary>

- **identity**: Bend & Burn; Pooja; Koramangala, Bangalore; Google profile is verified; in business since 2019
- **performance**: 5,934 profile views in the last 30 days; 65 calls in the last 30 days; 148 direction requests in the last 30 days; 31 leads in the last 30 days; 4.2% CTR over the last 30 days; views -7% over the last 7 days; calls +6% over the last 7 days
- **peer**: CTR 4.2% vs 4.5% peer average, 7% below peers; Profile views 5,934 vs 1,100 peer average, 439% above peers; Calls 65 vs 18 peer average, 261% above peers; Direction requests 148 vs 42 peer average, 252% above peers
- **customers**: 387 unique members this year
- **offers**: no active offers right now; category offers this merchant hasn't run: First Month @ ₹499; Personal Training Demo @ ₹199; Annual Membership @ ₹14,999 (save ₹6,000); Couple/Family Plan @ ₹999/month; Yoga + Strength Combo @ ₹1,499/month
- **subscription**: Pro plan active, 162 days left
- **category**: peer group: metro neighbourhood gyms 2026; peers average a 4.5★ rating; peers average 56 reviews; peers post on Google every 12 days on average; peers have 16 photos on average
- **season**: Apr-Jun: lowest acquisition window — focus on retention, not acquisition
- **trends**: "gym near me" searches +5% year-on-year; "personal trainer cost" searches +38% year-on-year (age 30-50); "yoga classes near me" searches +42% year-on-year (age 25-55, skews female); "weight loss program" searches +28% year-on-year (age 30-50, skews female)

</details>

## 2 · Phase 2: writing brief

- **Family:** event · **angle:** plan early for the festival with a concrete offer

- **Lead (why now):** festival upcoming (the trigger gives no details)

- **Supporting facts:**

  - popular category offers not on their profile: First Month @ ₹499; Personal Training Demo @ ₹199 *(from category.offer_catalog minus merchant.offers)*

  - CTR 4.2% vs 4.5% peer average, 7% below peers *(from merchant.performance.ctr vs category.peer_stats.avg_ctr)*

- **Ask:** yes/no: Want me to draft a festive offer, a Google post and a WhatsApp blast for you?

- **Format:** pre-approved template (`vera_festival_upcoming_v1`)

- **Allowed numbers:** 4.2, 4.5, 7, 199, 499

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Pooja, owner of Bend & Burn. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Pooja
Language: Mostly English; a little Hindi is fine.
Why now: festival upcoming (the trigger gives no details)
Supporting facts (use only these):
- popular category offers not on their profile: First Month @ ₹499; Personal Training Demo @ ₹199
- CTR 4.2% vs 4.5% peer average, 7% below peers
Angle: plan early for the festival with a concrete offer. Levers: specificity, loss aversion.
Ask, one only, as the last sentence (yes/no): Want me to draft a festive offer, a Google post and a WhatsApp blast for you?
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: energetic disciplined, coach to member.
- Category words you can use (vocabulary only, not facts about this business): footfall, membership churn, PT sessions, PR (personal record), 1RM, EMOM.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- The trigger (festival upcoming) gives no details: mention it only in general terms and build the message on the supporting facts.
- There's little merchant-specific data: lean on the comparisons and category facts listed.
- Numbers may only come from: 4.2, 4.5, 7, 199, 499.
- Never use: guaranteed weight loss, shred in 7 days, miracle transformation, fastest results.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Pooja, the festival season is coming up. One idea from the category catalog: a "First Month @ ₹499" offer. Your CTR is 4.2% vs 4.5% for similar gyms. Want me to draft a festive offer, a Google post and a WhatsApp blast for you?

## 3 · Phase 3: AI writer

> Hi Pooja, festival season aa raha hai—plan early karna smart rahega. Category mein First Month @ ₹499 aur Personal Training Demo @ ₹199 jaise clear offers profile par nahi hain, while your CTR is 4.2% vs 4.5% peer average (7% lower). Want me to draft a festive offer, a Google post and a WhatsApp blast for you?

**AI's rationale:** The message anchors on the upcoming festival, the missing ₹499/₹199 offers, and the 4.2% versus 4.5% CTR gap. It uses specificity and loss aversion by suggesting clear offers to address the below-peer comparison.

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