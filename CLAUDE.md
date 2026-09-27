# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Starter kit plus our submission for the **magicpin AI Challenge**. "Vera" is a WhatsApp assistant for merchants. It composes messages from four context layers (category, merchant, trigger, optional customer) and handles multi-turn replies, and an LLM judge scores it. Git: the owner's **personal** GitHub, `PANSHUL168/magicpin-vera`. Always use the SSH alias `git@github-personal:...`, never `git@github.com:`, which signs in as their company account. Commits use the personal no-reply identity through an `includeIf` in `~/.gitconfig`. Railway auto-deploys `main`, so don't push during the judge's test window.

The bot is built as a pipeline, one phase at a time:

**contexts → fact sheet → LLM composer → validator (retry once) → template fallback**, plus reply handling.

**All five phases are done**: contexts, fact sheets, the AI writer (OpenAI `gpt-5.6-luna`), the validator with one retry, the plain-template fallback, and reply handling. `README.md` is the 1-page submission README. Still to do: deploy (see "Deploy" below).

`submission.jsonl` is generated, not hand-written.

**API budget is limited.** Tests and dev use a fake model (`VERA_LLM=off` is forced in `tests/conftest.py`). Only call the real API when asked, and report `llm.USAGE` afterwards. The key lives in `.env`, which is gitignored and set to mode 600; never print it or copy it anywhere.

## Which doc answers what

- `challenge-brief.md`: **what** to build. It covers the 4-context model, the `compose()` contract (§5, §7), the 5×10 rubric (§8), compulsion levers (§10), anti-patterns (§11) and open challenges (§12).
- `challenge-testing-brief.md`: **how** the bot is tested. It covers the HTTP contract, the judge lifecycle (warmup → 60-min tick window → mid-test context injection → replay), limits and penalties.
- `examples/api-call-examples.md`: exact request and response bodies for each endpoint and replay scenario.
- `examples/case-studies.md`: 10 scored examples showing the target voice per vertical. The judge checks similarity to these, so never reuse their body text (for example as few-shot outputs).
- `engagement-design.md`, `engagement-research.md`: magicpin internal background. The paths they cite (`agents/vera/...`, `vera-mcp/...`) do **not** exist here.

## Commands

```bash
# One-time setup (Homebrew Python blocks global pip installs)
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt

# Expanded dataset (deterministic): 50 merchants, 200 customers, 100 triggers, test_pairs.json (T01–T30)
python3 dataset/generate_dataset.py --seed-dir dataset --out dataset/expanded

# Tests (they generate their own copy of the expanded dataset)
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest tests/test_bundle.py::test_priya_recall_bundle -q

# Serve the bot; VERA_DEBUG=1 adds GET /debug/bundle/{trigger_id}?now=... and GET /debug/state
VERA_DEBUG=1 .venv/bin/uvicorn bot:app --port 8080

# Push the full warmup set (5/50/200, optionally all triggers) over HTTP and check healthz; no LLM key needed
.venv/bin/python scripts/local_warmup.py --with-triggers --check-versions

# Build a bundle for every trigger and list flags per test pair; --trigger ID dumps one bundle as JSON
.venv/bin/python scripts/audit_contexts.py

# Read the 30 test-pair messages (--brief adds each writing brief; --trigger ID or --all for others)
.venv/bin/python scripts/preview_messages.py --brief

# Regenerate the deliverable from bot.compose(); rerun after any phase 2+ change.
# Uses the AI writer (saved results make unchanged briefs free); --plain = no API calls
.venv/bin/python scripts/write_submission.py

# Plain vs AI side by side (--ai calls the API only for briefs not already saved)
.venv/bin/python scripts/preview_messages.py --ai --trigger trg_004_perf_dip_bharat

# Export every stage for the 30 test pairs to output/ (input -> briefing -> brief + plain -> AI -> checks),
# plus a tick demo and the pytest run. Never calls the API (reads saved AI results). --skip-tests = faster
.venv/bin/python scripts/export_outputs.py

# Play the 10 scripted reply scenarios through the HTTP app; transcripts go to output/conversations/.
# No API calls unless --ai, which saves AI replies to the cache (openers stay cached or plain)
.venv/bin/python scripts/simulate_conversations.py
.venv/bin/python scripts/simulate_conversations.py --ai intent_transition

# Bundled local judge (edit its CONFIGURATION constants first; see below)
python3 judge_simulator.py
```

The curl in `api-call-examples.md` posts the bare category JSON without the envelope, so a correct bot rejects it. Use `local_warmup.py` instead.

### judge_simulator.py

- It reads **no env vars or CLI args**, so the brief's `export BOT_URL=...` has no effect. Edit the CONFIGURATION constants at the top: `BOT_URL`, `LLM_PROVIDER`, `LLM_API_KEY`, `LLM_MODEL`, `TEST_SCENARIO`. The default model IDs are old (for example `claude-3-5-sonnet-20241022`), so set `LLM_MODEL` explicitly. From Python you can set `judge_simulator.BOT_URL` before building `JudgeSimulator`.
- To run one scenario, set `TEST_SCENARIO`:
  - `warmup`: pushes 5 categories and the first 5 merchants.
  - `phase2_short`: one tick with the first 3 seed triggers. **LLM-scored.**
  - `full_evaluation`: every seed trigger, in batches of 5. **LLM-scored.**
  - `auto_reply_hell`, `intent_transition`, `hostile`: reply checks.
  - `all` (the default): warmup plus the reply checks. It scores **no** compositions.
- The final "SCENARIO RESULTS" mostly reflects reachability. Read the per-turn `[PASS]/[FAIL]/[WARN]` lines. The intent and hostile checks are keyword heuristics.
- It always pushes `version: 1`. Re-running against the same bot process gives 409s that show as `[FAIL]`, so `POST /v1/teardown` or restart the bot between runs.
- To drive it from Python without an API key, build `JudgeSimulator` with a stub `LLMProvider` and set `judge.scorer = LLMScorer(judge.llm, judge.dataset)` before calling `_phase2_short()` or `_full()`. `run()` normally sets the scorer. Scores then come back as a meaningless 5.
- Reply checks use `conversation_id`s the bot never opened. Run standalone, they push no context at all. `auto_reply_hell` uses a new ID each turn with the same `merchant_id`; `RuntimeState` counts repeats per party for this reason.
- It never pushes customer contexts.
- It sends wall-clock `now` (see "Reference time" below).
- Its judge prompt omits most of the context (digest, peer_stats, customer_aggregate, history), so correct facts drawn from those can score as "fabricated" locally. Its 4th dimension, `decision_quality`, is the brief's "trigger relevance". Don't over-fit to local scores.
- Its `OpenAIProvider` sends `temperature` and `max_tokens`, which gpt-5 reasoning models reject; every score then silently falls back to 5s. Drive it from Python with a Responses API `LLMProvider` subclass instead of editing the file.
- **Measured on 2026-09-27** (10 messages from `full_evaluation`): the simulator reports about 31–32/50. With the full context shown to the same judge, the same messages score about 39.6/50. The gap is the blind spot, not the messages.
- The real judge compares each message with `examples/case-studies.md` for the same (category, merchant, trigger) tuple, and the seed triggers *are* those tuples. The cases score 44–50/50. What they reward: a concrete deliverable plus an effort cap in the ask, judgment ("skip X, do Y"), a real draft for planning intents, source citations, and no repetition (repetition caps a dimension at 5).

## Phase 1 architecture (`vera/`)

Data flows store → normalize → derive → bundle.

- **`store.py`**: `ContextStore.ingest(envelope) -> (status, body)` is the whole `/v1/context` contract.
  - Returns 400 for a bad envelope, 409 `stale_version` for the same or a lower version, and 200 otherwise.
  - Keyed on `(scope, context_id)`, with a fallback lookup by the id declared inside the payload.
  - A new version that omits a top-level key inherits it from the previous version, because api-call-examples 2.8 pushes a partial category. A key sent explicitly, even as `[]`, replaces.
  - Records are immutable. Each one keeps `data` (canonical), `changes` (vs the previous version), `changes_since_base` (vs the first version) and `item_first_seen`, which tells digest items and offers that arrived after warmup apart from the rest.
- **`normalize.py`**: pure helpers.
  - `canonicalize()` fills defaults, coerces types, and maps the briefs' field names onto the data's: `taboos`→`vocab_taboo`, `avg_reviews`→`avg_review_count`, `payload.merchant_id`→`merchant_id`.
  - Formatting helpers: fractions → `%`, Indian digit grouping and `₹`, IST dates, snake_case → plain words (`humanize`).
  - Parsers and checks: signals, trends, language preferences, names, slot labels.
- **`derive.py`**: lists of `Fact(key, group, value, display, source)` for merchant, category and customer, none of which depend on the trigger. Also the history summary (open merchant requests, unanswered streak, 24h window), a richness score, the greeting and the language profile. `display` is ready to quote. `source` names the dataset fields, for checking numbers and writing rationales.
- **`bundle.py`**: `build_bundle(store, trigger_id, now=, state=) -> ContextBundle` is the hand-off to phase 2.
  - Resolves references when read, so push order doesn't matter, and resolves digest items via `top_item_id`, `alert_id` or `digest_item_id`.
  - Sets `flags`, each with a reason in `warnings`: `placeholder_payload`, `consent_gap`, `state_conflict`, `time_inconsistent`, `slot_weekday_mismatch`, `sparse_merchant`, `open_merchant_request` (merchant-facing only), `merchant_not_active`, `category_not_relevant`, `expired`, `opted_out`, `suppression_key_used`, `incomplete`.
  - Flags inform later phases; they never block.
  - In anything a merchant or customer reads, use `payload_display` and `Fact.display`, never raw payload values. The judge takes a point off for internal jargon.
- **`state.py`**: `RuntimeState`, what the bot did and saw.
  - Conversations, opened on the fly for unknown ids.
  - Logs of sent bodies and used suppression keys.
  - Per-party opt-out, reply timestamps for the 24h window, and inbound-text repeat counts (the auto-reply signal).
  - `record_inbound()` does not count as a reply. Call `mark_replied()` only for real replies.
- **`loader.py`**: feeds dataset files (seed or expanded layout) through `store.ingest`. It's for offline tools only. **Never preload in the server**, or the judge's version-1 warmup pushes come back 409.

## Phase 2 architecture

Flow: bundle → `factsheet.build_fact_sheet()` → `templates.render()`. On the live path, `policy.plan_tick()` runs first to choose triggers.

- **`factsheet.py`**: the writing brief (`FactSheet`) for one trigger.
  - The 26 trigger kinds are grouped into 8 `FAMILIES`. Each kind has a `Recipe`: a lead builder (the "why now"), supporting-fact selector names in order of preference, an angle, persuasion levers, and an ask key into `ASKS`. Unknown kinds use `FAMILY_DEFAULTS`.
  - Each fact is a `Line` with `text` (for the brief), `source`, `key`, and `phrase` / `phrase_hi` (English or Hinglish wording that fits inside a message; empty means brief only).
  - Placeholder triggers get a generic lead plus anchor facts only.
  - Flags become `instructions`.
  - Special cases:
    - Consent that covers only promotions turns reminder kinds into an offer.
    - Kinds that don't fit the business, such as a medicine refill at a dental clinic, become a general visit note.
    - A festival uses the seasonal note for its own month.
    - Dormant merchants open with a category digest item, never a mention of the silence.
  - `allowed_numbers` lists every number the brief uses. `to_prompt()` is the phase 3 input.
- **`templates.py`**: the plain, AI-free message: greeting, lead, `render_support` supporting phrases (usually 2), then the ask as the last sentence. Customer messages open with "<shop> here." Hinglish is used when `language["hinglish"]` is set. This is the fallback writer for phase 3/4.
- **`policy.py`**: the tick choosing step.
  - Skips a trigger when data is missing, the recipient opted out, it was already sent, the category doesn't fit, there's no consent, or reminders are opted out.
  - Also skips after 3 unanswered messages, within the cooldown (`VERA_COOLDOWN_MINUTES`, default 30), or while a conversation is waiting.
  - Groups by recipient (the customer, for customer triggers) and keeps one per recipient, ranked by urgency, then earliest expiry, then id. Caps at 20.
  - Skipped triggers are not marked as used.
- **`compose.py`**: `compose(category, merchant, trigger, customer)` is the brief §7 contract, re-exported by `bot.py`. It is deterministic because it pins "now" to `DEFAULT_REFERENCE_NOW`, 2026-04-26T10:30Z. `compose_bundle()` is the live path.
- `bot.py /v1/tick` records every send in `RuntimeState` (conversation id `conv_<recipient>_<kind>[_n]`). With `VERA_DEBUG=1`, `GET /debug/sheet/{trigger_id}` shows the brief, the prompt and the rendered message.
- The simulator never pushes customers, so customer triggers show as "waiting for data" locally. That is correct behaviour.

## Phase 3 architecture (AI writer)

Flow: fact sheet → plain draft (`templates.render`) → `writer.write_ai()` rewrites it → validator (phase 4, retry once) → send. Any failure sends the plain draft instead.

- **`llm.py`**: a thin wrapper over the OpenAI Responses API. It uses a strict JSON schema `{body, rationale}`, `store=False` and `reasoning.effort` from `VERA_LLM_EFFORT` (default `low`), and counts tokens in `USAGE`.
  - `VERA_LLM=off` or a missing `OPENAI_API_KEY` turns calls off.
  - `VERA_LLM_MODEL` defaults to `gpt-5.6-luna`.
  - `VERA_LLM_TIMEOUT` is 8s by default; the scripts set 30.
  - `config.load_env()` reads `.env`, but real environment variables win.
- **`writer.py`**:
  - `INSTRUCTIONS` are the standing rules. `build_prompt()` is `sheet.to_prompt()` plus the plain draft.
  - The hard checks live in `validator.problems()` (see phase 4). `writer.problems` re-exports it.
  - Results, **rejections included**, are cached by a fingerprint of `PROMPT_VERSION` + model + instructions + prompt. The cache is in memory; `compose()` and the scripts also persist it to `.cache/ai_messages.json` (`VERA_AI_CACHE_FILE`). The live server never writes to disk, and teardown clears the cache.
  - Changing `INSTRUCTIONS`, `PROMPT_VERSION` or any brief wording invalidates saved results. Rerun `write_submission.py` afterwards so `compose()` still matches `submission.jsonl`; that costs about 30 calls.
- **`compose.py`**:
  - `compose_bundle()` handles one trigger.
  - `compose_many()` writes a tick's triggers in parallel threads with a `VERA_TICK_DEADLINE` cutoff (8s). Late ones go out plain, and their calls still finish and fill the cache.
  - `compose()` stays deterministic through the persisted cache, so ship `.cache/ai_messages.json` with the submission.
- **Measured:** about 840 input and 240 output tokens per message (roughly 100 of the output is reasoning). A live tick with 2 AI messages took 3.8s.
- **`checks.py`**: `run_checks(body, sheet)` is the report form of the validator: one row per hard rule, plus one advisory row (language). `export_outputs.py` uses it. `compose.bundle_from_dicts()` builds the exact briefing `compose()` uses.

## Phase 4 architecture (validator, retry once)

- **`validator.py`**: `problems(body, sheet, *, extra_numbers, mid_conversation, max_chars, context_text)` returns every reason not to send.
  - For all messages it rejects:
    - an empty body, or one over 600 characters
    - a number not in `allowed_numbers`
    - a link, a taboo word, a snake_case code or `{}` braces
    - more than one "?", or more than one "!" or emoji
    - a preamble or self-introduction ("hope you're well", "this is Vera")
    - a customer message that mentions Vera
    - **service words the brief doesn't back** (`unsupported_services`). These are category `vocab_allowed` terms that appear in the body but not in the brief's facts, names or the chat. Trade and metric words in `GENERIC_VOCAB` ("footfall", "covers", "MRP", ...) are exempt. This rule fixed T25, where a salon with no offers was pitched balayage and keratin.
  - First messages must also: name the shop (customer messages), address the reader by name, include a number when the brief has any, end with the ask, and not copy a case study (50% or more word-triple overlap).
  - `fixes(issues, sheet)` turns each problem into one instruction ("Remove 37: not in the brief. Numbers may only come from: ..."). `retry_prompt()` appends the rejected version and those instructions to the original prompt.
- **`writer.generate_checked()`**: the shared loop for first messages and replies: write, check, retry once with feedback, check again.
  - Both attempts are cached, with their problems. **Cached bodies are checked again when read**, so a new rule catches old saved results and retries them.
  - `deadline` is a `time.monotonic()` value: a retry starts only if about 1.2× the first call's duration still fits. `compose_many()` passes the tick deadline, and replies pass `VERA_REPLY_DEADLINE`.
  - Offline `compose()` has no deadline, so it always gets the same answer from the cache.
  - The returned message has `retried: True` when the second attempt was used. `STATS` counts `retried` and `retry_ok`.
- The invariant, tested in `test_validator.py`: every canonical pair's plain draft passes the validator, so the fallback is always sendable. Of the 100 expanded triggers, only `trg_011`'s plain draft fails, by repeating "in the last 30 days".
- Also rejected: a 4-word phrase said twice ("repeats itself"). `PROPOSAL_KINDS` (`active_planning_intent`) may propose new numbers in a draft plan (tiers, timings, ages), but never a new percentage.
- **Measured:** 1 retry among the 30 test pairs (T25), costing 1,053 input and 301 output tokens.

### Brief tuning after the judge runs (factsheet.py)

- `ASKS` offer concrete deliverables with effort caps ("a 1-page checklist, ready in 10 min"). Numbers in the ask text are automatically in `allowed_numbers`.
- `ipl_match_today` with `is_weeknight: false`:
  - the angle and ask change to "skip dine-in promos, run the existing offer as a delivery-only special"
  - `_sel_match_offer` marks an offer that doesn't run on the match day (`offer_days()` parses "(Tue-Thu)")
  - a rule says to quote Saturday data as Saturday data
- `curious_ask_due` anchors on `_sel_momentum`, their best positive 7-day change, instead of an outside trend.
- `active_planning_intent` asks for a concrete, editable starter version.
- `supply_alert`: the chronic-Rx count is the list to check, not the number affected.
- Untried catalog offers are worded as "not on their profile", not "never tried".
- The writer's `PROMPT_VERSION` is `v4`: judgment where the facts support it, keep the ask's deliverable and time estimate, English rationale, no promised outcomes the facts don't show, and outlines allowed when the Format line asks.
- Planning (`active_planning_intent`):
  - `_sel_history_said` adds Vera's last pushed chat message: a suggestion, never an approved offer. Its most concrete sentence goes into the plain draft too.
  - The Format line asks for a 2-4 line outline, and the validator allows 700 characters.
  - The ask offers the next deliverable (a Google post and WhatsApp).
- **Empty payloads** (the lead builder returns None) keep the recipe's own selectors except those in `_PAYLOAD_SELECTORS`; the old code jumped straight to generic anchors. `season` and `local_trend` anchors only join `_SEASONAL_KINDS`.
- `perf_dip` and `perf_spike` add `slump` or `momentum`: a real 7-day change, not the metric the trigger already reports.
- Customer kinds in `_RETURN_VISIT_KINDS` get a `last_visit` anchor, skipped on `state_conflict` or `time_inconsistent`.
- Visit counts under 2 are dropped. The validator doesn't demand a number in customer messages. Pharmacy lapsed customers get a pickup/delivery ask. Slot asks name the slots only once.
- `policy._rank` puts unexpired triggers first. It never blocks them, because the judge's clock may not match the data.
- Replies:
  - `STRONG_COMMIT`/`SOFT_COMMIT` split, so a soft yes inside a question is a question.
  - `NEGATED` ("do not go ahead") turns a yes into a decline.
  - "go ahead tomorrow" means commit with `detail["later"]`, and gets a fixed acknowledgement.
  - "not the first one" is not a slot pick.
  - `CANNED_STRONG` catches business-voice auto-replies even when they end in "?".
  - Repeated text containing "?" isn't treated as a bot.
  - `conversation_handlers.respond()` replays earlier turns' effects, so a STOP stays a STOP.
- **Measured** (full-context judge, 15 riskiest submission pairs): 34.9 before items 1-7, 35.9 after. Single samples swing ±3-5.

## Phase 5 architecture (replies)

Flow: `/v1/reply` → `responder.handle_reply()`, run in a thread → log the inbound → rebuild the conversation's brief → `replies.classify()` → `_decide()` → send, wait or end.

- **`replies.py`**: a rules-only classifier for English and Hinglish, matched on `fingerprint()` text. The order matters:
  1. empty
  2. opt_out
  3. auto_reply (canned patterns; skipped when the message starts like a yes or has a "?")
  4. the same text of 5 or more words repeated by the same party → auto_reply
  5. slot_pick
  6. hostile
  7. commit
  8. off_topic
  9. thanks
  10. later
  11. decline
  12. question
  13. a bare yes/ok → commit with `detail["weak"]`
  14. engaged
- **`responder.py`**:
  - Context: a conversation opened by `/v1/tick` rebuilds its trigger's fact sheet (slot labels come from `bundle.slots`). One the judge opened gets a stand-in sheet: the merchant's facts plus a dummy `conversation_followup` trigger. An unknown merchant gets no facts.
  - Rules, each counted **per party** (merchant or customer), not per conversation:
    - **Auto-reply:** the 1st gets one note to the owner, the 2nd a 24h wait, the 3rd and later an end. Auto-replies never call `mark_replied()`; a real reply resets the count.
    - **Opt-out:** end and mark the party opted out, so later ticks skip them. Only a question or a strong yes (not a bare "ok") brings them back.
    - **Hostile:** one apology, and an end on the second.
    - **Off-topic:** a fixed decline plus a steer back to our first message's ask; GST gets its own line.
    - **Busy:** wait 30 minutes, or 24h when they say "kal" or "tomorrow".
    - **Declines and thanks:** end.
  - **AI replies:** commit, question and engaged replies go to the AI. It gets the brief without the first-message lines, the last 8 turns, the goal and the language. The goal after a yes is to deliver the thing itself.
    - Checks: `validator.problems()` with `mid_conversation=True`, where numbers and service words already said in the chat are allowed, and one retry with feedback if time allows. No qualifying phrases after a yes. No internal jargon ("brief", "trigger", ...). No repeated body, and no reused sentence of 8 or more words.
    - The deadline is `VERA_REPLY_DEADLINE`, 8s by default; the script sets 30.
    - Replies are cached in `writer.CACHE` under `reply:<hash>`, including `REPLY_PROMPT_VERSION`. They go to disk only when `responder.CACHE_FILE` or the `cache_file=` argument is set (offline tools).
    - When the AI is off, late or rejected, the `FIXED` wording goes out: English or Hinglish, with customer versions. It picks the first variant not yet sent. A yes after a draft gets "going ahead with the draft above", and when every variant is used up it waits.
  - The CTA comes from the body (`_cta_of`: `CONFIRM`, `YES`, a closing "?", else none), so the label matches the text.
  - Language: each message is re-checked. Hindi or Hinglish replies get Hinglish, 3 or more English words get English, and anything shorter keeps the profile.
- **`conversation_handlers.respond(state, merchant_message)`**: the brief §7.4 offline contract. It builds a throwaway store and runtime state from the dicts and replays `state["turns"]`, then calls the same `handle_reply` with the disk cache.
- **`harness.py`**: 10 scripted scenarios run through the real HTTP app via TestClient. They cover a WhatsApp Business bot, a Hinglish assistant followed by the owner, intent transition, a join intent, hostility followed by GST, opt-out plus a later tick, a busy merchant, a language switch, a customer slot pick, and the simulator's own checks. `tests/test_conversations.py` runs them offline.
- **Measured:** about 750 input and 260 output tokens per AI reply, 1.7 to 6s each.

**Reference time**: `resolve_now()` uses `VERA_REFERENCE_NOW` if it is set, else the tick's `now`. The local simulator sends wall-clock time, which makes 21 of the 25 seed triggers look expired. Set `VERA_REFERENCE_NOW=2026-04-26T10:30:00Z` for local runs and unset it for the real test.

## Deploy

- `Dockerfile` (python:3.14-slim, `uvicorn bot:app --workers 1` on `$PORT`), `Procfile`, `.dockerignore` and `.railwayignore`. `.env` is excluded everywhere, so the key is never uploaded.
- The recommended host is Railway: `railway init`, `railway up`, set the variables, then `railway domain`.
- Set `OPENAI_API_KEY`, `TEAM_NAME`, `TEAM_MEMBERS` and `CONTACT_EMAIL` on the host. **Never set `VERA_REFERENCE_NOW` or `VERA_DEBUG` there.**
- It must be one worker: state lives in memory.
- After any test push to the deployed bot (e.g. `local_warmup.py --url ...`), **`POST /v1/teardown`**. Otherwise the judge's own version-1 pushes come back 409.

## Submission contracts

1. **Offline** (brief §7): `bot.py` exposes `compose(category, merchant, trigger, customer) -> {body, cta, send_as, suppression_key, rationale}`. It must be deterministic (temperature 0) and take under 30s per call. You also submit `submission.jsonl` (one line per `test_id`), a README of at most one page, and optionally `conversation_handlers.py` with `respond(state, merchant_message)`.
2. **Live** (testing brief): the FastAPI app in `bot.py`, served at a public URL. It exposes `/v1/context`, `/v1/tick`, `/v1/reply`, `/v1/healthz`, `/v1/metadata` and `/v1/teardown`. Metadata comes from the `TEAM_NAME`, `TEAM_MEMBERS`, `VERA_MODEL` and `CONTACT_EMAIL` env vars.

Conversation rules for phases 2–5:
- `/v1/tick` returns `actions[]`. The list may be empty; restraint is rewarded.
- A tick allows at most 20 actions and one per (merchant, conversation).
- Each action opens a new `conversation_id`.
- A missing `conversation_id`, `merchant_id`, `send_as`, `trigger_id`, `body`, `cta`, `suppression_key` or `rationale` means the action scores 0 and costs −2. Also send `template_name` and `template_params`.
- `/v1/reply` returns `send`, `wait` (plus `wait_seconds`) or `end`. Expected behavior (api-call-examples Phase 4):
  - Canned auto-reply: flag it once, then wait, then end.
  - Explicit commitment ("let's do it"): act at once, with no more qualifying questions.
  - Hostile or opt-out: end, or one line of apology.
  - Off-topic: decline and steer back.
  - After 3 unanswered nudges, exit.
  - Re-detect language each turn.
  - Never repeat a body within a conversation (−2).

## Dataset reality vs. the briefs (trust the JSON)

- **What ships**: only the seeds (`dataset/*_seed.json`: 10 merchants, 15 customers, 25 triggers) plus 5 full category files. The 50/200/100 layout exists only after running the generator. The simulator reads the seeds only.
- **Placeholder test pairs**: 13 of the 30 canonical test pairs have a placeholder payload (`{"placeholder": true, ...}`), mostly for generated merchants that have no offers, history, signals or review themes. Anchor on performance, peer and category facts, and invent nothing.
- **Conflicting test pairs**:
  - Consent doesn't cover the trigger in T03, T04, T08 and T29.
  - The trigger says "lapsed" but the customer is `active` or `churned` in T14 and T15.
  - T04 and T08 send on behalf of expired merchants.
- **Inconsistent timelines**:
  - Diwali `days_until: 188` implies a "now" of 2026-04-26.
  - Priya's `last_visit` of 2026-05-12 and her November slots imply November.
  - Prefer durations the payload gives; never state a negative gap.
- **Wrong weekdays in slot labels**: "Wed 5 Nov" is 2026-11-05, a Thursday. Use `safe_label`, which drops the weekday.
- **Units**:
  - Every numeric `*_pct`, `ctr` and `delta` field is a fraction (−0.5 means −50%).
  - Strings like `"ORS_demand_+40"` embed whole-number percents.
  - `ctr` is given as-is; don't recompute it from views, calls or directions.
- **Field names** differ from the briefs' schemas:
  - The data has `vocab_taboo` and `avg_review_count`.
  - `customer_aggregate` has no key shared across categories.
  - Signals come as `name:22d` or `name_14d`.
  - Salutation templates use `{first_name}`, `{pharmacist_name}` or `{chef_or_owner_first_name}`.
- **Names**:
  - Generated dentists store `owner_first_name: "Dr. Asha"`.
  - Children appear as `"Aanya (parent: Sneha)"`; message the parent.
  - `"(walk-in, no profile)"` is anonymous.
  - Two service lists end with a literal `"..."`.
- **IDs** in the briefs are shortened or wrong. Real IDs look like `m_001_drmeera_dentist_delhi` and `c_001_priya_for_m001`.

## Spec conflicts (resolve conservatively)

- **URLs in the body**: the brief (§5) allows them, but api-call-examples F.4 penalizes −3 per URL. Leave them out.
- **Latency**: the testing brief allows 30s, the api-call-examples table 10s (tick and reply), and the simulator waits 15s. Aim for under 10s, and run a tick's LLM calls in parallel.
- **Same-version push**: the testing brief calls it a no-op, but api-call-examples 1.5 expects 409. We return 409.

## Message rules the judge enforces (brief §5, §8, §11)

- `send_as` is `"vera"` for merchant-facing messages and `"merchant_on_behalf"` for customer-scope triggers.
- The first outbound to someone must be a template (`{{1}}`-style params). Free-form is fine within 24h of their reply; see `history.session_window_open`.
- Anchor on a verifiable fact from the contexts.
  - Use service+price ("Haircut @ ₹99"), not "X% off".
  - Research and compliance claims need a source citation.
- One CTA, in the last sentence:
  - Binary YES/STOP for action triggers.
  - None for pure information.
  - Multi-choice only for booking slots.
- Follow `category.voice` for tone, allowed vocabulary and taboos. Peer tone, no hype for clinical verticals, no preamble, no re-introduction.
- The `rationale` must describe what the message actually does.
- Never send payload data to non-LLM external APIs, and keep no state after teardown.
