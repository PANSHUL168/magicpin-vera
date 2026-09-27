# T09 · competitor_opened → Dr. Meera (Dr. Meera's Dental Clinic)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Dr. Meera, Smile Studio 1.3 km door 8 Apr 2026 ko khula hai, Dental Cleaning @ ₹199 ke saath. Aapka Dental Cleaning @ ₹299 offer live hai, aur 18 calls vs 12 peer average ke saath 5 recent reviews mein patients ne aapke patient explanations ko appreciate kiya hai. Kya main ek Google post draft kar doon jo dikhaye ki aap alag kyun hain, 10 min mein ready?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_023_competitor_opened_dentist`

```json
{
  "id": "trg_023_competitor_opened_dentist",
  "scope": "merchant",
  "kind": "competitor_opened",
  "source": "external",
  "merchant_id": "m_001_drmeera_dentist_delhi",
  "customer_id": null,
  "payload": {
    "competitor_name": "Smile Studio",
    "distance_km": 1.3,
    "their_offer": "Dental Cleaning @ ₹199",
    "opened_date": "2026-04-08"
  },
  "urgency": 2,
  "suppression_key": "competitor:m_001:smile_studio",
  "expires_at": "2026-06-08T00:00:00Z"
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

**Customer:** none (merchant-facing trigger)

## 1 · Phase 1: briefing (join, clean, compare, warn)

- **Audience:** merchant · **send as:** `vera` · **greeting:** Dr. Meera · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"competitor_name": "Smile Studio", "distance_km": "1.3 km", "their_offer": "Dental Cleaning @ ₹199", "opened_date": "8 Apr 2026"}`

- **Data richness:** rich

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** 

  - open_merchant_request: merchant is waiting on: Yes please, focus on whitening and aligners

<details><summary>All 42 facts</summary>

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

</details>

## 2 · Phase 2: writing brief

- **Family:** event · **angle:** stay calm and competitive: lean on their strengths, not on price

- **Lead (why now):** Smile Studio opened 1.3 km away on 8 Apr 2026, offering Dental Cleaning @ ₹199

- **Supporting facts:**

  - active offers: Dental Cleaning @ ₹299 *(from merchant.offers (status=active))*

  - Calls 18 vs 12 peer average, 50% above peers *(from merchant.performance.calls vs category.peer_stats.avg_calls_30d)*

  - 5 reviews in the last 30 days mention the doctor's manner (positive): "Dr. Meera explains everything patiently" *(from merchant.review_themes)*

- **Ask:** yes/no: Want me to draft a Google post on what sets you apart, ready in 10 min?

- **Format:** pre-approved template (`vera_competitor_opened_v1`)

- **Allowed numbers:** 1.3, 5, 8, 10, 12, 18, 30, 50, 199, 299, 2026

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Dr. Meera, owner of Dr. Meera's Dental Clinic. Sent as: Vera, magicpin's merchant assistant.
Greeting: Dr. Meera
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: Smile Studio opened 1.3 km away on 8 Apr 2026, offering Dental Cleaning @ ₹199
Supporting facts (use only these):
- active offers: Dental Cleaning @ ₹299
- Calls 18 vs 12 peer average, 50% above peers
- 5 reviews in the last 30 days mention the doctor's manner (positive): "Dr. Meera explains everything patiently"
Angle: stay calm and competitive: lean on their strengths, not on price. Levers: specificity, loss aversion, social proof.
Ask, one only, as the last sentence (yes/no): Kya main ek Google post draft kar doon jo dikhaye ki aap alag kyun hain, 10 min mein ready?
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: peer clinical, respectful collegial.
- Category words you can use (vocabulary only, not facts about this business): fluoride varnish, scaling, caries, occlusion, bruxism, endodontic.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- Numbers may only come from: 1.3, 5, 8, 10, 12, 18, 30, 50, 199, 299, 2026.
- Never use: guaranteed, 100% safe, completely cure, miracle, best in city, doctor approved, FDA-approved.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Dr. Meera, Smile Studio opened 1.3 km away on 8 Apr 2026 with Dental Cleaning @ ₹199. Your Dental Cleaning @ ₹299 offer is live. Your calls are 18 vs 12 for similar clinics. Kya main ek Google post draft kar doon jo dikhaye ki aap alag kyun hain, 10 min mein ready?

## 3 · Phase 3: AI writer

> Dr. Meera, Smile Studio 1.3 km door 8 Apr 2026 ko khula hai, Dental Cleaning @ ₹199 ke saath. Aapka Dental Cleaning @ ₹299 offer live hai, aur 18 calls vs 12 peer average ke saath 5 recent reviews mein patients ne aapke patient explanations ko appreciate kiya hai. Kya main ek Google post draft kar doon jo dikhaye ki aap alag kyun hain, 10 min mein ready?

**AI's rationale:** The message acknowledges the nearby low-price competitor but anchors on stronger evidence: above-peer calls and five positive reviews about Dr. Meera’s manner. It uses specificity and social proof rather than recommending a price response.

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