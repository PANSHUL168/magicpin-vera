# T13 · customer_lapsed_hard → Rashmi (PowerHouse Fitness)

**Final message** (sent as `merchant_on_behalf`, written by **ai**, ask type `binary_yes_no`):

> Hi Rashmi, PowerHouse Fitness here. It’s been 57 days since your last visit, and we’d love to welcome you back. Since your focus is weight loss, you can use our 3 FREE Trial Classes in a weekday evening slot that suits you. Reply YES and we'll book a time that suits you.

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_015_winback_rashmi`

```json
{
  "id": "trg_015_winback_rashmi",
  "scope": "customer",
  "kind": "customer_lapsed_hard",
  "source": "internal",
  "merchant_id": "m_007_powerhouse_gym_bangalore",
  "customer_id": "c_010_rashmi_for_m007",
  "payload": {
    "days_since_last_visit": 57,
    "previous_focus": "weight_loss",
    "previous_membership_months": 5
  },
  "urgency": 3,
  "suppression_key": "winback:c_010_rashmi_for_m007",
  "expires_at": "2026-06-15T00:00:00Z"
}
```

<details><summary>Merchant <code>m_007_powerhouse_gym_bangalore</code> (full record)</summary>

```json
{
  "merchant_id": "m_007_powerhouse_gym_bangalore",
  "category_slug": "gyms",
  "identity": {
    "name": "PowerHouse Fitness",
    "city": "Bangalore",
    "locality": "HSR Layout",
    "place_id": "ChIJ_HSR_GYM_007",
    "verified": true,
    "languages": [
      "en",
      "hi",
      "kn"
    ],
    "owner_first_name": "Karthik",
    "established_year": 2020
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 95
  },
  "performance": {
    "window_days": 30,
    "views": 1480,
    "calls": 22,
    "directions": 48,
    "ctr": 0.052,
    "leads": 14,
    "delta_7d": {
      "views_pct": -0.3,
      "calls_pct": -0.35
    }
  },
  "offers": [
    {
      "id": "o_powerhouse_001",
      "title": "3 FREE Trial Classes",
      "status": "active",
      "started": "2026-01-01"
    }
  ],
  "conversation_history": [],
  "customer_aggregate": {
    "total_active_members": 245,
    "monthly_churn_pct": 0.1,
    "trial_to_paid_pct": 0.28
  },
  "signals": [
    "seasonal_dip_apr_may",
    "above_peer_ctr",
    "no_recent_post"
  ],
  "review_themes": [
    {
      "theme": "equipment_quality",
      "sentiment": "pos",
      "occurrences_30d": 7
    },
    {
      "theme": "morning_crowd",
      "sentiment": "neg",
      "occurrences_30d": 4
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

<details><summary>Customer <code>c_010_rashmi_for_m007</code></summary>

```json
{
  "customer_id": "c_010_rashmi_for_m007",
  "merchant_id": "m_007_powerhouse_gym_bangalore",
  "identity": {
    "name": "Rashmi",
    "phone_redacted": "<phone>",
    "language_pref": "english",
    "age_band": "30-40"
  },
  "relationship": {
    "first_visit": "2025-09-10",
    "last_visit": "2026-02-28",
    "visits_total": 22,
    "services_received": [
      "membership_x4",
      "PT_intro"
    ],
    "lifetime_value": 4490
  },
  "state": "lapsed_hard",
  "preferences": {
    "preferred_slots": "weekday_evening",
    "channel": "whatsapp",
    "reminder_opt_in": true,
    "training_focus": "weight_loss"
  },
  "consent": {
    "opted_in_at": "2025-09-10",
    "scope": [
      "renewal_reminders",
      "winback_offers"
    ]
  }
}
```

</details>

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** customer · **send as:** `merchant_on_behalf` · **greeting:** Hi Rashmi · **language:** English

- **Event, made readable:** `{"days_since_last_visit": "57", "previous_focus": "weight loss", "previous_membership_months": "5"}`

- **Data richness:** rich

- **Digest item:** none

- **Slots:** none

- **Consent:** covered by consent: winback_offers

- **Warnings:** none

<details><summary>All 51 facts</summary>

- **identity**: PowerHouse Fitness; Karthik; HSR Layout, Bangalore; Google profile is verified; in business since 2020
- **performance**: 1,480 profile views in the last 30 days; 22 calls in the last 30 days; 48 direction requests in the last 30 days; 14 leads in the last 30 days; 5.2% CTR over the last 30 days; views -30% over the last 7 days; calls -35% over the last 7 days
- **peer**: CTR 5.2% vs 4.5% peer average, 16% above peers; Profile views 1,480 vs 1,100 peer average, 35% above peers; Calls 22 vs 18 peer average, 22% above peers; Direction requests 48 vs 42 peer average, 14% above peers; Monthly churn 10% vs 8% peer average, 2 points above peers; Trial-to-paid conversion 28% vs 32% peer average, 4 points below peers
- **customers**: 245 active members; monthly churn 10%; trial-to-paid conversion 28%
- **offers**: active offers: 3 FREE Trial Classes; category offers this merchant hasn't run: First Month @ ₹499; Personal Training Demo @ ₹199; Annual Membership @ ₹14,999 (save ₹6,000); Couple/Family Plan @ ₹999/month; Yoga + Strength Combo @ ₹1,499/month
- **subscription**: Pro plan active, 95 days left
- **reviews**: 7 reviews in the last 30 days mention equipment quality (positive); 4 reviews in the last 30 days mention morning crowding (negative)
- **signals**: seasonal dip expected in Apr-May; CTR above the peer benchmark; no recent Google post
- **category**: peer group: metro neighbourhood gyms 2026; peers average a 4.5★ rating; peers average 56 reviews; peers post on Google every 12 days on average; peers have 16 photos on average
- **season**: Apr-Jun: lowest acquisition window — focus on retention, not acquisition
- **trends**: "gym near me" searches +5% year-on-year; "personal trainer cost" searches +38% year-on-year (age 30-50); "yoga classes near me" searches +42% year-on-year (age 25-55, skews female); "weight loss program" searches +28% year-on-year (age 30-50, skews female)
- **customer**: Rashmi; age group 30-40; customer status: lapsed for a long time; 22 visits since 10 Sep 2025; last visit 28 Feb 2026; 57 days since the last visit; services so far are: membership x4, PT intro; ₹4,490 spent so far; prefers weekday evening slots; training focus: weight loss
- **consent**: consented on 10 Sep 2025 to: renewal reminders, winback offers; opted in to reminders

</details>

## 2 · Phase 2: writing brief

- **Family:** customer · **angle:** warm, no pressure: give them an easy reason to come back

- **Lead (why now):** 57 days since last visit

- **Supporting facts:**

  - their focus: weight loss *(from trigger.payload.previous_focus / customer.preferences)*

  - active offer: 3 FREE Trial Classes *(from merchant.offers)*

  - prefers weekday evening slots *(from customer.preferences.preferred_slots)*

- **Ask:** yes/no: Reply YES and we'll book a time that suits you.

- **Format:** pre-approved template (`merchant_customer_lapsed_hard_v1`)

- **Allowed numbers:** 3, 57

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Rashmi, a customer of PowerHouse Fitness. Sent as: PowerHouse Fitness, on the shop's behalf (not Vera).
Greeting: Hi Rashmi
Language: English.
Why now: 57 days since last visit
Supporting facts (use only these):
- their focus: weight loss
- active offer: 3 FREE Trial Classes
- prefers weekday evening slots
Angle: warm, no pressure: give them an easy reason to come back. Levers: reciprocity, single binary commitment.
Ask, one only, as the last sentence (yes/no): Reply YES and we'll book a time that suits you.
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm, clear and respectful, like the shop's front desk writing to a regular customer.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Write as PowerHouse Fitness, not as Vera. No medical or guaranteed-result claims.
- Numbers may only come from: 3, 57.
- Never use: guaranteed weight loss, shred in 7 days, miracle transformation, fastest results.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Rashmi, PowerHouse Fitness here. It's been 57 days since your last visit, and we'd love to see you again. Our 3 FREE Trial Classes offer is on right now. We know weekday evening slots suit you best. Reply YES and we'll book a time that suits you.

## 3 · Phase 3: AI writer

> Hi Rashmi, PowerHouse Fitness here. It’s been 57 days since your last visit, and we’d love to welcome you back. Since your focus is weight loss, you can use our 3 FREE Trial Classes in a weekday evening slot that suits you. Reply YES and we'll book a time that suits you.

**AI's rationale:** Names PowerHouse Fitness in the first sentence and keeps the message warm, specific, and low-pressure. It anchors on 57 days, the weight-loss focus, and the 3 FREE Trial Classes, ending with one binary ask.

## 4 · Phase 4: validator

The AI's first version was **rejected** (doesn't say which shop is writing):

> Hi Rashmi, it’s been 57 days since your last visit, and we’d love to welcome you back. Since your focus is weight loss, you can use our 3 FREE Trial Classes in a weekday evening slot that suits you. Reply YES and we'll book a time that suits you.

It was sent back once with this feedback:

- Name the shop (PowerHouse Fitness) in the first sentence.

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