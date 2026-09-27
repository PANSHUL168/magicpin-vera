# T28 · recall_due → Priya (Dr. Meera's Dental Clinic)

**Final message** (sent as `merchant_on_behalf`, written by **ai**, ask type `multi_choice_slot`):

> Hi Priya, Dr. Meera's Dental Clinic se reminder: aapka 6-month cleaning 12 Nov 2026 tak due hai. Weekday evening aapko suit karta hai, aur Dental Cleaning @ ₹299 available hai. 5 Nov, 6pm ke liye 1 ya 6 Nov, 5pm ke liye 2 reply kijiye, ya apna time bataiye.

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_003_recall_due_priya`

```json
{
  "id": "trg_003_recall_due_priya",
  "scope": "customer",
  "kind": "recall_due",
  "source": "internal",
  "merchant_id": "m_001_drmeera_dentist_delhi",
  "customer_id": "c_001_priya_for_m001",
  "payload": {
    "service_due": "6_month_cleaning",
    "last_service_date": "2026-05-12",
    "due_date": "2026-11-12",
    "available_slots": [
      {
        "iso": "2026-11-05T18:00:00+05:30",
        "label": "Wed 5 Nov, 6pm"
      },
      {
        "iso": "2026-11-06T17:00:00+05:30",
        "label": "Thu 6 Nov, 5pm"
      }
    ]
  },
  "urgency": 3,
  "suppression_key": "recall:c_001_priya_for_m001:6mo",
  "expires_at": "2026-11-30T00:00:00Z"
}
```

<details><summary>Merchant <code>m_001_drmeera_dentist_delhi</code> (full record)</summary>

```json
{
  "merchant_id": "m_001_drmeera_dentist_delhi",
  "category_slug": "dentists",
  "identity": {
    "name": "Dr. Meera's Dental Clinic",
    "city": "Delhi",
    "locality": "Lajpat Nagar",
    "place_id": "ChIJ_LAJPATNAGAR_DENTIST_001",
    "verified": true,
    "languages": [
      "en",
      "hi"
    ],
    "owner_first_name": "Meera",
    "established_year": 2018
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 82,
    "renewed_at": "2026-02-04"
  },
  "performance": {
    "window_days": 30,
    "views": 2410,
    "calls": 18,
    "directions": 45,
    "ctr": 0.021,
    "leads": 9,
    "delta_7d": {
      "views_pct": 0.18,
      "calls_pct": -0.05,
      "ctr_pct": 0.02
    }
  },
  "offers": [
    {
      "id": "o_meera_001",
      "title": "Dental Cleaning @ ₹299",
      "status": "active",
      "started": "2026-03-01"
    },
    {
      "id": "o_meera_002",
      "title": "Deep Cleaning @ ₹499",
      "status": "expired",
      "ended": "2026-02-28"
    }
  ],
  "conversation_history": [
    {
      "ts": "2026-04-24T10:12:00Z",
      "from": "vera",
      "body": "Profile audit done — your photos are 8/10, description complete, but Google posts are stale (last post 22 days ago). Want me to draft 3 posts you can review?",
      "engagement": "merchant_replied"
    },
    {
      "ts": "2026-04-24T10:18:00Z",
      "from": "merchant",
      "body": "Yes please, focus on whitening and aligners",
      "engagement": "intent_action"
    }
  ],
  "customer_aggregate": {
    "total_unique_ytd": 540,
    "lapsed_180d_plus": 78,
    "retention_6mo_pct": 0.38,
    "high_risk_adult_count": 124
  },
  "signals": [
    "stale_posts:22d",
    "ctr_below_peer_median",
    "high_risk_adult_cohort",
    "engaged_in_last_48h"
  ],
  "review_themes": [
    {
      "theme": "wait_time",
      "sentiment": "neg",
      "occurrences_30d": 3,
      "common_quote": "had to wait 30 min on Sunday afternoon"
    },
    {
      "theme": "doctor_manner",
      "sentiment": "pos",
      "occurrences_30d": 5,
      "common_quote": "Dr. Meera explains everything patiently"
    }
  ]
}
```

</details>

<details><summary>Category <code>dentists</code> (key fields)</summary>

```json
{
  "slug": "dentists",
  "voice": {
    "tone": "peer_clinical",
    "register": "respectful_collegial",
    "code_mix": "hindi_english_natural",
    "vocab_allowed": [
      "fluoride varnish",
      "scaling",
      "caries",
      "occlusion",
      "bruxism",
      "endodontic",
      "periodontal",
      "implant",
      "aligner",
      "veneer",
      "OPG",
      "IOPA",
      "RCT",
      "CAD/CAM",
      "zirconia",
      "PFM"
    ],
    "vocab_taboo": [
      "guaranteed",
      "100% safe",
      "completely cure",
      "miracle",
      "best in city",
      "doctor approved",
      "FDA-approved (use only when actually applicable)"
    ],
    "salutation_examples": [
      "Dr. {first_name}",
      "Doc"
    ],
    "tone_examples": [
      "Worth a look — JIDA Oct 2026 p.14",
      "This one likely affects your high-risk adult cohort",
      "If your case-mix is mostly cosmetic, may not be relevant"
    ]
  },
  "peer_stats": {
    "scope": "metro_solo_practices_2026",
    "avg_rating": 4.4,
    "avg_review_count": 62,
    "avg_views_30d": 1820,
    "avg_calls_30d": 12,
    "avg_directions_30d": 38,
    "avg_ctr": 0.03,
    "avg_photos": 9,
    "avg_post_freq_days": 14,
    "retention_6mo_pct": 0.42
  },
  "offer_catalog": [
    "Dental Cleaning @ ₹299",
    "Free Consultation",
    "Teeth Whitening @ ₹1,499",
    "Root Canal @ ₹2,999 (single rooted)",
    "Free Smile Analysis + Digital Scan",
    "Aligner Consultation @ ₹499",
    "Pediatric Dental Checkup @ ₹199",
    "Annual Family Dental Plan @ ₹4,999"
  ],
  "digest (titles)": [
    "3-month fluoride varnish recall outperforms 6-month for high-risk adult caries",
    "DCI revised radiograph dose limits effective 2026-12-15",
    "IDA Delhi: Digital impressions — 2026 state of the art",
    "Clear aligner consultations searches +62% YoY in metros",
    "Dentsply launches IPS e.max Press for zirconia crowns in India at ₹3,200/unit (Delhi labs)"
  ],
  "seasonal_beats": [
    {
      "month_range": "Nov-Feb",
      "note": "exam-stress bruxism spike — ortho consults rise 30% in 18-24 cohort"
    },
    {
      "month_range": "Oct-Dec",
      "note": "wedding whitening peak — bookings 2x baseline; ladies' segment dominant"
    },
    {
      "month_range": "Jan",
      "note": "new-year resolution surge — annual check-up bookings +40%"
    },
    {
      "month_range": "Apr-Jun",
      "note": "school holiday window — pediatric appointments +50%"
    }
  ]
}
```

</details>

<details><summary>Customer <code>c_001_priya_for_m001</code></summary>

```json
{
  "customer_id": "c_001_priya_for_m001",
  "merchant_id": "m_001_drmeera_dentist_delhi",
  "identity": {
    "name": "Priya",
    "phone_redacted": "<phone>",
    "language_pref": "hi-en mix",
    "age_band": "25-35"
  },
  "relationship": {
    "first_visit": "2025-11-04",
    "last_visit": "2026-05-12",
    "visits_total": 4,
    "services_received": [
      "cleaning",
      "cleaning",
      "whitening",
      "cleaning"
    ],
    "lifetime_value": 1696
  },
  "state": "lapsed_soft",
  "preferences": {
    "preferred_slots": "weekday_evening",
    "channel": "whatsapp",
    "reminder_opt_in": true
  },
  "consent": {
    "opted_in_at": "2025-11-04",
    "scope": [
      "recall_reminders",
      "appointment_reminders"
    ]
  }
}
```

</details>

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** customer · **send as:** `merchant_on_behalf` · **greeting:** Hi Priya · **language:** Hindi-English mix (Hinglish)

- **Event, made readable:** `{"service_due": "6-month cleaning", "last_service_date": "12 May 2026", "due_date": "12 Nov 2026", "available_slots": ["5 Nov, 6pm", "6 Nov, 5pm"]}`

- **Data richness:** rich

- **Digest item:** none

- **Slots:** Wed 5 Nov, 6pm → 5 Nov, 6pm; Thu 6 Nov, 5pm → 6 Nov, 5pm

- **Consent:** covered by consent: appointment_reminders, recall_reminders

- **Warnings:** 

  - time_inconsistent: payload.last_service_date 2026-05-12 is after now

  - time_inconsistent: customer last_visit 2026-05-12 is after now

  - slot_weekday_mismatch: slot labels name the wrong weekday for their dates; use safe_label

<details><summary>All 52 facts</summary>

- **identity**: Dr. Meera's Dental Clinic; Meera; Lajpat Nagar, Delhi; Google profile is verified; in business since 2018
- **performance**: 2,410 profile views in the last 30 days; 18 calls in the last 30 days; 45 direction requests in the last 30 days; 9 leads in the last 30 days; 2.1% CTR over the last 30 days; views +18% over the last 7 days; calls -5% over the last 7 days; CTR +2% over the last 7 days
- **peer**: CTR 2.1% vs 3.0% peer average, 30% below peers; Profile views 2,410 vs 1,820 peer average, 32% above peers; Calls 18 vs 12 peer average, 50% above peers; Direction requests 45 vs 38 peer average, 18% above peers; 6-month retention 38% vs 42% peer average, 4 points below peers
- **customers**: 540 unique patients this year; 78 patients not seen in 180+ days; 6-month retention 38%; 124 high-risk adult patients
- **offers**: active offers: Dental Cleaning @ ₹299; past offers: Deep Cleaning @ ₹499 (expired, ended 28 Feb 2026); category offers this merchant hasn't run: Teeth Whitening @ ₹1,499; Root Canal @ ₹2,999 (single rooted); Aligner Consultation @ ₹499; Pediatric Dental Checkup @ ₹199; Free Consultation
- **subscription**: Pro plan active, 82 days left
- **reviews**: 3 reviews in the last 30 days mention wait times (negative): "had to wait 30 min on Sunday afternoon"; 5 reviews in the last 30 days mention the doctor's manner (positive): "Dr. Meera explains everything patiently"
- **signals**: last Google post was 22 days ago; CTR below the peer benchmark; sizeable high-risk adult patient group; engaged with Vera in the last 48 hours
- **category**: peer group: metro solo practices 2026; peers average a 4.4★ rating; peers average 62 reviews; peers post on Google every 14 days on average; peers have 9 photos on average
- **season**: Apr-Jun: school holiday window — pediatric appointments +50%
- **trends**: "clear aligners delhi" searches +62% year-on-year (age 28-45, skews female); "teeth whitening price" searches +41% year-on-year; "dental implants near me" searches +18% year-on-year (age 45-65, skews male); "kids first dental visit" searches +27% year-on-year (parents 25-40, skews female)
- **customer**: Priya; age group 25-35; customer status: recently lapsed; 4 visits since 4 Nov 2025; last visit 12 May 2026; services so far are: cleaning ×3, whitening; ₹1,696 spent so far; prefers weekday evening slots
- **consent**: consented on 4 Nov 2025 to: recall reminders, appointment reminders; opted in to reminders

</details>

## 2 · Phase 2: writing brief

- **Family:** customer · **angle:** a friendly, useful reminder with an easy way to book

- **Lead (why now):** 6-month cleaning due by 12 Nov 2026

- **Supporting facts:**

  - available slots: 5 Nov, 6pm; 6 Nov, 5pm *(from trigger.payload slots (weekday checked))*

  - active offer: Dental Cleaning @ ₹299 *(from merchant.offers)*

  - prefers weekday evening slots *(from customer.preferences.preferred_slots)*

- **Ask:** pick a slot: Reply 1 for 5 Nov, 6pm or 2 for 6 Nov, 5pm, or tell us a time that suits you.

- **Format:** pre-approved template (`merchant_recall_due_v1`)

- **Allowed numbers:** 1, 2, 5, 6, 12, 299, 2026

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Priya, a customer of Dr. Meera's Dental Clinic. Sent as: Dr. Meera's Dental Clinic, on the shop's behalf (not Vera).
Greeting: Hi Priya
Language: Hindi-English mix (Hinglish), in Roman script.
Why now: 6-month cleaning due by 12 Nov 2026
Supporting facts (use only these):
- available slots: 5 Nov, 6pm; 6 Nov, 5pm
- active offer: Dental Cleaning @ ₹299
- prefers weekday evening slots
Angle: a friendly, useful reminder with an easy way to book. Levers: specificity, effort externalization, single binary commitment.
Ask, one only, as the last sentence (pick a slot): 5 Nov, 6pm ke liye 1 ya 6 Nov, 5pm ke liye 2 reply kijiye, ya apna time bataiye.
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: warm, clear and respectful, like the shop's front desk writing to a regular customer.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Write as Dr. Meera's Dental Clinic, not as Vera. No medical or guaranteed-result claims.
- Some dates in the data are after today: don't say how long ago anything happened.
- Use the slot labels exactly as listed here (their original weekdays were wrong).
- Name the slot times only once, in the ask.
- Numbers may only come from: 1, 2, 5, 6, 12, 299, 2026.
- Never use: guaranteed, 100% safe, completely cure, miracle, best in city, doctor approved, FDA-approved.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Hi Priya, Dr. Meera's Dental Clinic here. Aapka 6-month cleaning due hai (12 Nov 2026 tak). Dental Cleaning @ ₹299 available hai. Weekday evening slots aapke liye best rehte hain. 5 Nov, 6pm ke liye 1 ya 6 Nov, 5pm ke liye 2 reply kijiye, ya apna time bataiye.

## 3 · Phase 3: AI writer

> Hi Priya, Dr. Meera's Dental Clinic se reminder: aapka 6-month cleaning 12 Nov 2026 tak due hai. Weekday evening aapko suit karta hai, aur Dental Cleaning @ ₹299 available hai. 5 Nov, 6pm ke liye 1 ya 6 Nov, 5pm ke liye 2 reply kijiye, ya apna time bataiye.

**AI's rationale:** Anchors the reminder on the 12 Nov 2026 due date and the ₹299 cleaning offer. It uses her weekday-evening preference and makes booking a single binary choice.

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