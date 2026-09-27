# Vera: magicpin AI Challenge submission

Vera writes WhatsApp messages to merchants (and, on their behalf, to customers) from four contexts: category, merchant, trigger and optional customer. It then handles the replies. Each message is anchored on a verifiable fact, explains why it's being sent now, and ends with one low-friction ask.

## How a message is made

1. **Contexts** (`vera/store.py`, `bundle.py`). `/v1/context` stores versioned pushes: the same or an older version gets 409, and a partial update inherits the keys it omits. The trigger, merchant, category and customer are then joined and cleaned into a *briefing*:
   - fractions become %, prices become ₹ with Indian digit grouping, dates are IST, and internal codes become plain words
   - peer comparisons are computed
   - data problems get flags: consent gaps, stale or contradictory dates, wrong slot weekdays, placeholder payloads
2. **Writing brief** (`factsheet.py`). The 26 trigger kinds form 8 families, and each kind picks:
   - a *why now* lead
   - the supporting facts that make its point
   - an angle, such as "weekend IPL match: skip dine-in promos, push delivery"
   - one ask that offers a concrete deliverable, such as "a 1-page checklist, ready in 10 min"

   Every number the message may use is listed.
3. **AI writer** (`writer.py`, OpenAI `gpt-5.6-luna`, strict JSON, low reasoning effort). It rewrites a plain, fact-correct draft into natural English or Hinglish, following the category voice.
4. **Validator, one retry** (`validator.py`). A message that fails a check is sent back once with specific feedback. The checks cover:
   - numbers not in the brief, links, taboo words, internal codes
   - more than one question, repetition, preamble or self-introduction
   - services the business doesn't list, such as a salon with no keratin offer
   - a missing name, number or final ask
   - copying a case study
5. **Fallback** (`templates.py`). If the AI is off, late (8s budget per tick) or fails twice, the plain draft goes out. Every plain draft passes the validator.

**Choosing what to send** (`policy.py`). Vera sends at most one message per recipient per tick. It skips expired, already-sent or out-of-consent triggers, opted-out parties, recipients with 3 unanswered messages, and anyone inside a 30-min cooldown. Restraint over spam.

**Replies** (`replies.py`, `responder.py`). A rules-first classifier (English and Hinglish) handles each kind of reply:
- **Merchant's own auto-reply:** one note for the owner, then wait 24h, then end. Counted per merchant across conversations.
- **Stop:** end and remember the opt-out.
- **Hostile:** one apology, then end.
- **Off-topic (e.g. GST):** a polite decline, then back to the original ask.
- **"Let's do it":** deliver the thing now, with no more qualifying questions.
- **Slot pick:** booked.

The AI writes the real answers under the same checks. The language is re-detected every turn, and Vera never repeats itself in a conversation.

## Run it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
OPENAI_API_KEY=... .venv/bin/uvicorn bot:app --port 8080     # without a key: plain templates only
.venv/bin/python -m pytest -q                                   # 210 tests, no API calls
.venv/bin/python scripts/write_submission.py                    # regenerate submission.jsonl (cached, deterministic)
.venv/bin/python scripts/simulate_conversations.py              # 10 scripted reply scenarios -> output/conversations/
```

To deploy, use the `Dockerfile` (one worker; state is in memory by design) and set `OPENAI_API_KEY`, `TEAM_NAME`, `TEAM_MEMBERS` and `CONTACT_EMAIL`. `compose()` in `bot.py` is the offline contract. It's deterministic because AI results are cached in `.cache/ai_messages.json`, which ships with the submission. `conversation_handlers.respond()` is the multi-turn contract.

## Choices worth knowing

- **Facts over flair.** Numbers come only from the contexts, and research and compliance claims carry their source. Planning drafts may propose quantities and timings, but never statistics.
- **Judgment, not templating.** For example: a weekend IPL match gets "skip the promo, push delivery"; a seasonal dip gets "save ad spend, focus on retention"; a recall gets "check the chronic-Rx list for these batches".
- **Data conflicts are handled, not ignored.** Examples: consent that covers only promotions, "lapsed" customers who are actually active, slot labels with the wrong weekday, and dates after "today".
- **Privacy.** Payloads go only to the LLM, and `/v1/teardown` wipes all state.
