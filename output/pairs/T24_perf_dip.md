# T24 · perf_dip → Dr. Bharat (Bharat Dental Care)

**Final message** (sent as `vera`, written by **ai**, ask type `binary_yes_no`):

> Dr. Bharat, pichhle 7 din mein calls 50% down hain—usually around 12—and views bhi 22% gire hain. CTR 1.8% hai, peer average 3.0%, aur Google profile verified nahi hai; pehla quick fix verification hoga. Kya main is hafte ke liye do quick fixes bhej doon, 5 min mein?

Matches `submission.jsonl`: ✅

## 0 · Input (what the judge sends)

**Trigger** `trg_004_perf_dip_bharat`

```json
{
  "id": "trg_004_perf_dip_bharat",
  "scope": "merchant",
  "kind": "perf_dip",
  "source": "internal",
  "merchant_id": "m_002_bharat_dentist_mumbai",
  "customer_id": null,
  "payload": {
    "metric": "calls",
    "delta_pct": -0.5,
    "window": "7d",
    "vs_baseline": 12
  },
  "urgency": 4,
  "suppression_key": "perf_dip:m_002_bharat_dentist_mumbai:calls:2026-W17",
  "expires_at": "2026-05-10T00:00:00Z"
}
```

<details><summary>Merchant <code>m_002_bharat_dentist_mumbai</code> (full record)</summary>

```json
{
  "merchant_id": "m_002_bharat_dentist_mumbai",
  "category_slug": "dentists",
  "identity": {
    "name": "Bharat Dental Care",
    "city": "Mumbai",
    "locality": "Andheri West",
    "place_id": "ChIJ_ANDHERI_DENTIST_002",
    "verified": false,
    "languages": [
      "en",
      "hi",
      "mr"
    ],
    "owner_first_name": "Bharat",
    "established_year": 2010
  },
  "subscription": {
    "status": "active",
    "plan": "Pro",
    "days_remaining": 12,
    "renewed_at": "2025-04-26"
  },
  "performance": {
    "window_days": 30,
    "views": 980,
    "calls": 4,
    "directions": 18,
    "ctr": 0.018,
    "leads": 2,
    "delta_7d": {
      "views_pct": -0.22,
      "calls_pct": -0.5,
      "ctr_pct": -0.1
    }
  },
  "offers": [],
  "conversation_history": [
    {
      "ts": "2026-04-10T11:00:00Z",
      "from": "vera",
      "body": "Subscription expires in 16 days — Bharat Dental Care...",
      "engagement": "merchant_no_reply"
    }
  ],
  "customer_aggregate": {
    "total_unique_ytd": 220,
    "lapsed_180d_plus": 95,
    "retention_6mo_pct": 0.18
  },
  "signals": [
    "renewal_due_soon:12d",
    "perf_dip_severe",
    "unverified_gbp",
    "dormant_with_vera_14d",
    "no_active_offers"
  ],
  "review_themes": []
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

- **Audience:** merchant · **send as:** `vera` · **greeting:** Dr. Bharat · **language:** English with natural Hindi code-mix (Hinglish)

- **Event, made readable:** `{"metric": "calls", "delta_pct": "-50%", "window": "7 days", "vs_baseline": "12"}`

- **Data richness:** moderate

- **Digest item:** none

- **Slots:** none

- **Consent:** n/a (merchant-facing)

- **Warnings:** none

<details><summary>All 39 facts</summary>

- **identity**: Bharat Dental Care; Bharat; Andheri West, Mumbai; Google profile is not verified; in business since 2010
- **performance**: 980 profile views in the last 30 days; 4 calls in the last 30 days; 18 direction requests in the last 30 days; 2 leads in the last 30 days; 1.8% CTR over the last 30 days; views -22% over the last 7 days; calls -50% over the last 7 days; CTR -10% over the last 7 days
- **peer**: CTR 1.8% vs 3.0% peer average, 40% below peers; Profile views 980 vs 1,820 peer average, 46% below peers; Calls 4 vs 12 peer average, 67% below peers; Direction requests 18 vs 38 peer average, 53% below peers; 6-month retention 18% vs 42% peer average, 24 points below peers
- **customers**: 220 unique patients this year; 95 patients not seen in 180+ days; 6-month retention 18%
- **offers**: no active offers right now; category offers this merchant hasn't run: Dental Cleaning @ ₹299; Teeth Whitening @ ₹1,499; Root Canal @ ₹2,999 (single rooted); Aligner Consultation @ ₹499; Pediatric Dental Checkup @ ₹199
- **subscription**: Pro plan active, 12 days left
- **signals**: subscription renewal due in 12 days; severe drop in performance; Google Business Profile not verified; no message to Vera in 14 days; no active offers
- **category**: peer group: metro solo practices 2026; peers average a 4.4★ rating; peers average 62 reviews; peers post on Google every 14 days on average; peers have 9 photos on average
- **season**: Apr-Jun: school holiday window — pediatric appointments +50%
- **trends**: "clear aligners delhi" searches +62% year-on-year (age 28-45, skews female); "teeth whitening price" searches +41% year-on-year; "dental implants near me" searches +18% year-on-year (age 45-65, skews male); "kids first dental visit" searches +27% year-on-year (parents 25-40, skews female)

</details>

## 2 · Phase 2: writing brief

- **Family:** performance · **angle:** name the drop plainly, then offer a concrete fix

- **Lead (why now):** calls -50% over the last 7 days (usually around 12)

- **Supporting facts:**

  - views -22% over the last 7 days *(from merchant.performance.delta_7d.views_pct)*

  - CTR 1.8% vs 3.0% peer average, 40% below peers *(from merchant.performance.ctr vs category.peer_stats.avg_ctr)*

  - Google profile is not verified *(from merchant.identity.verified)*

- **Ask:** yes/no: Want two quick fixes you can try this week, drafted in 5 min?

- **Format:** pre-approved template (`vera_perf_dip_v1`)

- **Allowed numbers:** 1.8, 3, 5, 7, 12, 22, 40, 50

<details><summary>The prompt the AI receives</summary>

```text
Write one WhatsApp message.
To: Dr. Bharat, owner of Bharat Dental Care. Sent as: Vera, magicpin's merchant assistant.
Greeting: Dr. Bharat
Language: Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.
Why now: calls -50% over the last 7 days (usually around 12)
Supporting facts (use only these):
- views -22% over the last 7 days
- CTR 1.8% vs 3.0% peer average, 40% below peers
- Google profile is not verified
Angle: name the drop plainly, then offer a concrete fix. Levers: specificity, loss aversion, effort externalization.
Ask, one only, as the last sentence (yes/no): Kya main is hafte ke liye do quick fixes bhej doon, 5 min mein?
Format: first message in this chat window, so keep it template-shaped: greeting, 2-3 short sentences, then the ask.
Rules:
- Voice: peer clinical, respectful collegial.
- Category words you can use (vocabulary only, not facts about this business): fluoride varnish, scaling, caries, occlusion, bruxism, endodontic.
- One ask only, and make it the last sentence. No links. No preamble.
- Use only the facts listed here: no invented offers, prices, dates, names or statistics.
- Don't re-introduce Vera; speak as a peer, not a salesperson.
- Numbers may only come from: 1.8, 3, 5, 7, 12, 22, 40, 50.
- Never use: guaranteed, 100% safe, completely cure, miracle, best in city, doctor approved, FDA-approved.
```

</details>

**Plain message (fill-in-the-blanks writer):**

> Dr. Bharat, your calls are down 50% over the last 7 days (usually around 12). Views -22% this week. Your CTR is 1.8% vs 3.0% for similar clinics. Kya main is hafte ke liye do quick fixes bhej doon, 5 min mein?

## 3 · Phase 3: AI writer

> Dr. Bharat, pichhle 7 din mein calls 50% down hain—usually around 12—and views bhi 22% gire hain. CTR 1.8% hai, peer average 3.0%, aur Google profile verified nahi hai; pehla quick fix verification hoga. Kya main is hafte ke liye do quick fixes bhej doon, 5 min mein?

**AI's rationale:** Anchors on the call and view drop, then connects the below-peer CTR to the unverified Google profile. It offers a specific, low-effort fix while keeping the single yes/no ask exactly as requested.

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