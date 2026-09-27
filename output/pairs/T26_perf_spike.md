# T26 · perf_spike → Padma (Zen Yoga Studio)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Hi Padma
> Calls are up 15% over the last 7 days, usually around 18—kids yoga post ne attention pakda lagta hai. Views are up 10%, and your 6.2% CTR is 38% above the 4.5% peer average, so let’s build on that curiosity. Want me to line up two more posts like the one that worked?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_024_perf_spike_zen`

```json
{
  "id": "trg_024_perf_spike_zen",
  "scope": "merchant",
  "kind": "perf_spike",
  "source": "internal",
  "merchant_id": "m_008_zenyoga_gym_chennai",
  "customer_id": null,
  "payload": {
    "metric": "calls",
    "delta_pct": 0.15,
    "window": "7d",
    "vs_baseline": 18,
    "likely_driver": "kids_yoga_post"
  },
  "urgency": 1,
  "suppression_key": "perf_spike:m_008:calls:2026-W17",
  "expires_at": "2026-05-03T00:00:00Z"
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

**Customer:** none (merchant-facing trigger)

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** merchant · **send as:** `vera` · **greeting:** Hi Padma · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"metric": "calls", "delta_pct": "+15%", "window": "7 days", "vs_baseline": "18", "likely_driver": "kids yoga post"}`

- **Data richness:** rich

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** none

<details><summary>All 39 facts</summary>

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

</details>

## 2 · Phase 2: writing brief

- **Family:** performance · **angle:** celebrate the jump and build on what caused it

- **Lead (why now):** calls +15% over the last 7 days (usually around 18), likely driven by kids yoga post

- **Supporting facts:**

  - views +10% over the last 7 days *(from merchant.performance.delta_7d.views_pct)*

  - CTR 6.2% vs 4.5% peer average, 38% above peers *(from merchant.performance.ctr vs category.peer_stats.avg_ctr)*

  - active offers: First Month @ ₹499; Free Body Composition Analysis *(from merchant.offers (status=active))*

- **Ask:** yes/no: Want me to line up two more posts like the one that worked?

- **Format:** pre-approved template (`vera_perf_spike_v1`)

- **Allowed numbers:** 4.5, 6.2, 7, 10, 15, 18, 38, 499

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Padma, owner of Zen Yoga Studio. Sent as: Vera, magicpin's merchant assistant.
Greeting: Hi Padma
Language: Mostly English; a little Hindi is fine.
Why now: calls +15% over the last 7 days (usually around 18), likely driven by kids yoga post
Supporting facts (use only these):
- views +10% over the last 7 days
- CTR 6.2% vs 4.5% peer average, 38% above peers
- active offers: First Month @ ₹499; Free Body Composition Analysis
Angle: celebrate the jump and build on what caused it. Levers: specificity, curiosity.
Ask, one only, as the last sentence (yes/no): Want me to line up two more posts like the one that worked?
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: energetic disciplined, coach to member.
- Category words you can use (vocabulary only, not facts about this business): footfall, membership churn, PT sessions, PR (personal record), 1RM, EMOM.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- Numbers may only come from: 4.5, 6.2, 7, 10, 15, 18, 38, 499.
- Never use: guaranteed weight loss, shred in 7 days, miracle transformation, fastest results.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Padma, your calls are up 15% over the last 7 days (usually around 18), likely thanks to your kids yoga post. Views +10% this week. Your CTR is 6.2% vs 4.5% for similar gyms. Want me to line up two more posts like the one that worked?

## 3 · Phase 3: AI writer

> Hi Padma
> Calls are up 15% over the last 7 days, usually around 18—kids yoga post ne attention pakda lagta hai. Views are up 10%, and your 6.2% CTR is 38% above the 4.5% peer average, so let’s build on that curiosity. Want me to line up two more posts like the one that worked?

**AI's rationale:** The message celebrates the recent call and view growth, anchors it in the kids yoga post, and highlights the 6.2% CTR versus the 4.5% peer average. It uses specificity and curiosity to support the suggested next step.

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