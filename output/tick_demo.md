# The choosing step on a real tick

The judge calls `/v1/tick` with three active triggers: two for Dr. Meera and one for her patient Priya. The bot sends at most one message per person, most urgent first.

## Tick 1 at 10:30

Available: `trg_001_research_digest_dentists, trg_002_compliance_dci_radiograph, trg_003_recall_due_priya`

**Sent** `trg_002_compliance_dci_radiograph` (urgency 4) to Dr. Meera, conversation `conv_m_001_drmeera_dentist_delhi_regulation_change`, written by AI:

> Dr. Meera, DCI ke 4 Nov 2026 circular ke hisaab se radiograph dose limit 15 Dec 2026 se revise ho rahi hai. IOPA exposure limit 1.5 mSv se 1.0 mSv hogi; E-speed film new limit pass karta hai, D-speed nahi, aur digital RVG unaffected hai. Dec 15 se pehle X-ray setup audit karke SOPs mein E-speed ya RVG document karna practical rahega. Kya main deadline se pehle ki 1-page checklist bana doon, 10 min mein ready?

**Sent** `trg_003_recall_due_priya` (urgency 3) to Priya, conversation `conv_c_001_priya_for_m001_recall_due`, written by AI:

> Hi Priya, Dr. Meera's Dental Clinic se reminder: aapka 6-month cleaning 12 Nov 2026 tak due hai. Weekday evening aapko suit karta hai, aur Dental Cleaning @ ₹299 available hai. 5 Nov, 6pm ke liye 1 ya 6 Nov, 5pm ke liye 2 reply kijiye, ya apna time bataiye.

**Held** `trg_001_research_digest_dentists`: trg_002_compliance_dci_radiograph ranked higher for m_001_drmeera_dentist_delhi

## Tick 2 at 10:35, same three triggers

Sent: 0 message(s).

- `trg_001_research_digest_dentists`: messaged 5 min ago (cooldown)
- `trg_002_compliance_dci_radiograph`: already sent (suppression key used)
- `trg_003_recall_due_priya`: already sent (suppression key used)
