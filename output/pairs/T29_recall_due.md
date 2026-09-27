# T29 · recall_due → Diya (Zen Yoga Studio)

**Final message** (sent as `merchant_on_behalf`, written by **ai**, ask type `binary_yes_no`):

> Hi Diya, Zen Yoga Studio here—our First Month @ ₹499 offer is on right now. It’s been 25 days since your last visit on 1 Apr 2026, after your 9 visits since 1 Sep 2025. Reply YES and we’ll find you a slot.

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_066_recall_due_m_008_zenyoga_gym_ch`

```json
{
  "id": "trg_066_recall_due_m_008_zenyoga_gym_ch",
  "scope": "customer",
  "kind": "recall_due",
  "source": "internal",
  "merchant_id": "m_008_zenyoga_gym_chennai",
  "customer_id": "c_034_diya_for_m_008_zenyoga_gym_chennai",
  "payload": {
    "placeholder": true,
    "metric_or_topic": "recall_due"
  },
  "urgency": 3,
  "suppression_key": "recall_due:m_008_zenyoga_gym_chennai:gen_66",
  "expires_at": "2026-06-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_008_zenyoga_gym_chennai</code> (full record)</summary>

```json
{
  "merchant_id": "m_008_zenyoga_gym_chennai",
  "category_slug": "gyms",
  "identity": {
    "name": "Zen Yoga Studio",
    "city": "Chennai",
    "locality": "Mylapore",
    "place_id": "ChIJ_MYLAPORE_GYM_008",
    "verified": true,
    "languages": [
      "en",
      "ta",
      "hi"
    ],
    "owner_first_name": "Padma",
    "established_year": 2017
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 180
  },
  "performance": {
    "window_days": 30,
    "views": 880,
    "calls": 18,
    "directions": 38,
    "ctr": 0.062,
    "leads": 12,
    "delta_7d": {
      "views_pct": 0.1,
      "calls_pct": 0.15
    }
  },
  "offers": [
    {
      "id": "o_zen_001",
      "title": "First Month @ ₹499",
      "status": "active",
      "started": "2026-03-01"
    },
    {
      "id": "o_zen_002",
      "title": "Free Body Composition Analysis",
      "status": "active",
      "started": "2026-03-01"
    }
  ],
  "conversation_history": [
    {
      "ts": "2026-04-23T09:00:00Z",
      "from": "merchant",
      "body": "Hi I want to add a kids yoga program — what should it look like?",
      "engagement": "intent_planning"
    },
    {
      "ts": "2026-04-23T09:05:00Z",
      "from": "vera",
      "body": "Great idea — kids yoga summer camps are peaking now. Suggest 4-week program, 3 classes/week, age 7-12, ₹2,499. Want me to draft the GBP post + Insta carousel?",
      "engagement": "merchant_replied"
    }
  ],
  "customer_aggregate": {
    "total_active_members": 95,
    "monthly_churn_pct": 0.05,
    "trial_to_paid_pct": 0.55
  },
  "signals": [
    "high_retention",
    "active_planning",
    "boutique_segment"
  ],
  "review_themes": [
    {
      "theme": "instructor_quality",
      "sentiment": "pos",
      "occurrences_30d": 9
    },
    {
      "theme": "small_classes",
      "sentiment": "pos",
      "occurrences_30d": 6
    }
  ]
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

<details><summary>Customer <code>c_034_diya_for_m_008_zenyoga_gym_chennai</code></summary>

```json
{
  "customer_id": "c_034_diya_for_m_008_zenyoga_gym_chennai",
  "merchant_id": "m_008_zenyoga_gym_chennai",
  "identity": {
    "name": "Diya",
    "phone_redacted": "<phone>",
    "language_pref": "en",
    "age_band": "20-25"
  },
  "relationship": {
    "first_visit": "2025-09-01",
    "last_visit": "2026-04-01",
    "visits_total": 9,
    "services_received": [],
    "lifetime_value": 6183
  },
  "state": "lapsed_soft",
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

- **Audience:** customer · **send as:** `merchant_on_behalf` · **greeting:** Hi Diya · **language:** English

- **Event, made readable:** `{"placeholder": true, "metric_or_topic": "recall due"}`

- **Data richness:** rich

- **Digest item:** none

- **Slots:** none

- **Consent:** recall_due needs one of appointment_reminders, recall_reminders; customer consented only to promotional_offers

- **Warnings:** 

  - placeholder_payload: trigger payload has no event details; anchor on merchant and category facts and invent nothing about the event

  - consent_gap: recall_due needs one of appointment_reminders, recall_reminders; customer consented only to promotional_offers

<details><summary>All 48 facts</summary>

- **identity**: Zen Yoga Studio; Padma; Mylapore, Chennai; Google profile is verified; in business since 2017
- **performance**: 880 profile views in the last 30 days; 18 calls in the last 30 days; 38 direction requests in the last 30 days; 12 leads in the last 30 days; 6.2% CTR over the last 30 days; views +10% over the last 7 days; calls +15% over the last 7 days
- **peer**: CTR 6.2% vs 4.5% peer average, 38% above peers; Profile views 880 vs 1,100 peer average, 20% below peers; Calls 18 vs 18 peer average, in line with peers; Direction requests 38 vs 42 peer average, 10% below peers; Monthly churn 5% vs 8% peer average, 3 points below peers; Trial-to-paid conversion 55% vs 32% peer average, 23 points above peers
- **customers**: 95 active members; monthly churn 5%; trial-to-paid conversion 55%
- **offers**: active offers: First Month @ ₹499; Free Body Composition Analysis; category offers this merchant hasn't run: Personal Training Demo @ ₹199; Annual Membership @ ₹14,999 (save ₹6,000); Couple/Family Plan @ ₹999/month; Yoga + Strength Combo @ ₹1,499/month; 3 FREE Trial Classes
- **subscription**: Pro plan active, 180 days left
- **reviews**: 9 reviews in the last 30 days mention instructor quality (positive); 6 reviews in the last 30 days mention small classes (positive)
- **signals**: high retention; active planning; boutique segment
- **category**: peer group: metro neighbourhood gyms 2026; peers average a 4.5★ rating; peers average 56 reviews; peers post on Google every 12 days on average; peers have 16 photos on average
- **season**: Apr-Jun: lowest acquisition window — focus on retention, not acquisition
- **trends**: "gym near me" searches +5% year-on-year; "personal trainer cost" searches +38% year-on-year (age 30-50); "yoga classes near me" searches +42% year-on-year (age 25-55, skews female); "weight loss program" searches +28% year-on-year (age 30-50, skews female)
- **customer**: Diya; age group 20-25; customer status: recently lapsed; 9 visits since 1 Sep 2025; last visit 1 Apr 2026; 25 days since the last visit; ₹6,183 spent so far
- **consent**: consented on 1 Sep 2025 to: promotional offers; opted in to reminders

</details>

## 2 · Phase 2: writing brief

- **Family:** customer · **angle:** a friendly, useful reminder with an easy way to book

- **Lead (why now):** active offer: First Month @ ₹499

- **Supporting facts:**

  - last visit 1 Apr 2026 (25 days ago) *(from customer.relationship.last_visit)*

  - 9 visits since 1 Sep 2025 *(from customer.relationship.visits_total)*

- **Ask:** yes/no: Reply YES and we'll find you a slot.

- **Format:** pre-approved template (`merchant_recall_due_v1`)

- **Allowed numbers:** 1, 9, 25, 499, 2025, 2026

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Diya, a customer of Zen Yoga Studio. Sent as: Zen Yoga Studio, on the shop's behalf (not Vera).
Greeting: Hi Diya
Language: English.
Why now: active offer: First Month @ ₹499
Supporting facts (use only these):
- last visit 1 Apr 2026 (25 days ago)
- 9 visits since 1 Sep 2025
Angle: a friendly, useful reminder with an easy way to book. Levers: specificity, effort externalization, single binary commitment.
Ask, one only, as the last sentence (yes/no): Reply YES and we'll find you a slot.
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm, clear and respectful, like the shop's front desk writing to a regular customer.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Write as Zen Yoga Studio, not as Vera. No medical or guaranteed-result claims.
- The trigger (recall due) gives no details: mention it only in general terms and build the message on the supporting facts.
- The customer only agreed to promotional offers: frame this as an offer from the shop, not a reminder.
- Numbers may only come from: 1, 9, 25, 499, 2025, 2026.
- Never use: guaranteed weight loss, shred in 7 days, miracle transformation, fastest results.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Diya, Zen Yoga Studio here. Our First Month @ ₹499 offer is on right now. Your last visit was on 1 Apr 2026, 25 days ago. Thanks for your 9 visits since 1 Sep 2025. Reply YES and we'll find you a slot.

## 3 · Phase 3: AI writer

> Hi Diya, Zen Yoga Studio here—our First Month @ ₹499 offer is on right now. It’s been 25 days since your last visit on 1 Apr 2026, after your 9 visits since 1 Sep 2025. Reply YES and we’ll find you a slot.

**AI's rationale:** This keeps the offer timely and anchors the message on Diya’s last visit and visit history. It reduces booking effort to a single yes/no reply.

## 4 · Phase 4: validator

The AI's first version was **rejected** (doesn't say which shop is writing):

> Hi Diya, our First Month @ ₹499 offer is on right now. We noticed it’s been 25 days since your last visit on 1 Apr 2026, after your 9 visits since 1 Sep 2025. Reply YES and we’ll find you a slot.

It was sent back once with this feedback:

- Name the shop (Zen Yoga Studio) in the first sentence.

The rewrite (shown above) passed every check.

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