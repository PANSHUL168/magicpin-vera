"""Facts about merchants, customers and categories, each with a display string and a source.

None of this depends on the trigger; the fact-sheet phase picks which facts a message
uses. `source` names the fields a fact came from, so later phases can check every
number in a message against the facts and cite provenance in the rationale.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from .normalize import (IST, LANGUAGE_NAMES, detect_language, fmt_date, fmt_inr, fmt_number,
                        fmt_pct, humanize, is_number, language_code, months_in_range, offer_key,
                        parse_dt, parse_language_pref, parse_person_name, parse_signal,
                        pct_decimals, signal_display, split_honorific)

CUSTOMER_NOUN = {"dentists": "patients", "gyms": "members", "salons": "clients",
                 "restaurants": "customers", "pharmacies": "customers"}


@dataclass
class Fact:
    key: str
    group: str
    value: Any
    display: str        # ready to quote; numbers formatted exactly as they should appear
    source: str         # dataset fields this came from

    def to_dict(self) -> dict:
        return asdict(self)


def customer_noun(category_slug: str | None) -> str:
    return CUSTOMER_NOUN.get(category_slug or "", "customers")


REVIEW_THEME_LABELS = {"delivery_late": "late delivery", "wait_time": "wait times",
                       "saturday_wait": "Saturday waits", "weekend_busy": "weekend crowding",
                       "morning_crowd": "morning crowding", "doctor_manner": "the doctor's manner"}


def review_theme_label(theme: Any) -> str:
    return REVIEW_THEME_LABELS.get(str(theme), humanize(theme))


def _slug(text: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(text).lower()).strip("_")


# =============================================================================
# PEER COMPARISONS
# =============================================================================


def _comparison(key: str, label: str, mine: float, peer: float, *, kind: str, source: str,
                higher_is_better: bool = True) -> Fact:
    """kind: 'rate' (small % like CTR, gap shown relative), 'share' (% like retention,
    gap in points) or 'count'."""
    ratio = mine / peer
    position = "above" if ratio > 1.05 else "below" if ratio < 0.95 else "in line with"
    if kind == "count":
        mine_text, peer_text = fmt_number(mine), fmt_number(peer)
    else:  # same precision on both sides: "2.1% vs 3.0%", not "2.1% vs 3%"
        decimals = pct_decimals(mine, peer)
        mine_text, peer_text = fmt_pct(mine, decimals=decimals), fmt_pct(peer, decimals=decimals)
    if position == "in line with":
        gap = "in line with peers"
    elif kind == "share":
        points = abs(round((mine - peer) * 100))
        gap = f"{points} point{'' if points == 1 else 's'} {position} peers"
    else:
        gap = f"{fmt_pct(abs(ratio - 1), decimals=0)} {position} peers"
    value = {"merchant": mine, "peer": peer, "ratio": round(ratio, 3), "position": position,
             "higher_is_better": higher_is_better}
    return Fact(key, "peer", value, f"{label} {mine_text} vs {peer_text} peer average, {gap}", source)


# =============================================================================
# MERCHANT
# =============================================================================

_PERF_LABELS = (("views", "profile views"), ("calls", "calls"),
                ("directions", "direction requests"), ("leads", "leads"))
_PEER_COUNTS = (("views", "avg_views_30d", "Profile views"), ("calls", "avg_calls_30d", "Calls"),
                ("directions", "avg_directions_30d", "Direction requests"))

# customer_aggregate has different keys per category; unknown keys fall back to humanize().
AGG_COUNT_LABELS = {
    "total_unique_ytd": "unique {noun} this year",
    "lapsed_180d_plus": "{noun} not seen in 180+ days",
    "lapsed_90d_plus": "{noun} not seen in 90+ days",
    "high_risk_adult_count": "high-risk adult {noun}",
    "delivery_orders_30d": "delivery orders in the last 30 days",
    "dine_in_orders_30d": "dine-in orders in the last 30 days",
    "total_active_members": "active members",
    "chronic_rx_count": "customers on chronic prescriptions",
}
AGG_SHARE_LABELS = {
    "retention_6mo_pct": "6-month retention",
    "retention_3mo_pct": "3-month retention",
    "retention_30d_pct": "30-day retention",
    "repeat_customer_pct": "repeat-customer share",
    "delivery_share_pct": "delivery share of orders",
    "monthly_churn_pct": "monthly churn",
    "trial_to_paid_pct": "trial-to-paid conversion",
}
# Service+price offers read as specific; flat discounts are the brief's anti-pattern.
_OFFER_TYPE_ORDER = {"service_at_price": 0, "free_service": 1, "free_trial": 2, "free_addon": 3,
                     "bogo": 4, "membership": 5, "percentage_discount": 9}


def merchant_facts(merchant: dict, category: dict | None) -> list[Fact]:
    facts: list[Fact] = []
    add = facts.append
    identity, perf = merchant["identity"], merchant["performance"]
    noun = customer_noun(merchant.get("category_slug"))
    peer = (category or {}).get("peer_stats", {})

    # --- identity ---
    if identity.get("name"):
        add(Fact("merchant_name", "identity", identity["name"], identity["name"], "merchant.identity.name"))
    honorific, first = split_honorific(identity.get("owner_first_name"))
    if first:
        add(Fact("owner_first_name", "identity", {"first_name": first, "honorific": honorific}, first,
                 "merchant.identity.owner_first_name"))
    place = ", ".join(x for x in (identity.get("locality"), identity.get("city")) if x)
    if place:
        add(Fact("location", "identity", {"locality": identity.get("locality"), "city": identity.get("city")},
                 place, "merchant.identity.locality, merchant.identity.city"))
    if isinstance(identity.get("verified"), bool):
        text = "Google profile is verified" if identity["verified"] else "Google profile is not verified"
        add(Fact("gbp_verified", "identity", identity["verified"], text, "merchant.identity.verified"))
    if is_number(identity.get("established_year")):
        year = identity["established_year"]
        add(Fact("established_year", "identity", year, f"in business since {year}",
                 "merchant.identity.established_year"))

    # --- performance ---
    window = perf["window_days"] if is_number(perf.get("window_days")) else 30
    for key, label in _PERF_LABELS:
        if is_number(perf.get(key)):
            add(Fact(f"{key}_{window}d", "performance", perf[key],
                     f"{fmt_number(perf[key])} {label} in the last {window} days", f"merchant.performance.{key}"))
    if is_number(perf.get("ctr")):
        add(Fact("ctr", "performance", perf["ctr"], f"{fmt_pct(perf['ctr'])} CTR over the last {window} days",
                 "merchant.performance.ctr"))
    for key, value in perf["delta_7d"].items():
        if is_number(value):
            metric = key[:-4] if key.endswith("_pct") else key
            label = "CTR" if metric == "ctr" else humanize(metric)
            add(Fact(f"{metric}_change_7d", "performance", value,
                     f"{label} {fmt_pct(value, signed=True)} over the last 7 days",
                     f"merchant.performance.delta_7d.{key}"))

    # --- vs peers (peer averages are 30-day figures, so counts need a 30-day window) ---
    if is_number(perf.get("ctr")) and is_number(peer.get("avg_ctr")) and peer["avg_ctr"]:
        add(_comparison("ctr_vs_peer", "CTR", perf["ctr"], peer["avg_ctr"], kind="rate",
                        source="merchant.performance.ctr vs category.peer_stats.avg_ctr"))
    if window == 30:
        for key, peer_key, label in _PEER_COUNTS:
            if is_number(perf.get(key)) and is_number(peer.get(peer_key)) and peer[peer_key]:
                add(_comparison(f"{key}_vs_peer", label, perf[key], peer[peer_key], kind="count",
                                source=f"merchant.performance.{key} vs category.peer_stats.{peer_key}"))

    # --- customers ---
    for key, value in merchant["customer_aggregate"].items():
        if not is_number(value):
            continue
        source = f"merchant.customer_aggregate.{key}"
        if key.endswith("_pct"):
            label = AGG_SHARE_LABELS.get(key, humanize(key[:-4]))
            add(Fact(key, "customers", value, f"{label} {fmt_pct(value)}", source))
            if is_number(peer.get(key)) and peer[key]:
                add(_comparison(f"{key}_vs_peer", label[:1].upper() + label[1:], value, peer[key],
                                kind="share", source=f"{source} vs category.peer_stats.{key}",
                                higher_is_better="churn" not in key))
        else:
            label = AGG_COUNT_LABELS.get(key, humanize(key)).format(noun=noun)
            add(Fact(key, "customers", value, f"{fmt_number(value)} {label}", source))

    # --- offers ---
    offers = merchant["offers"]
    active = [o for o in offers if str(o.get("status", "")).lower() == "active"]
    inactive = [o for o in offers if str(o.get("status", "")).lower() != "active"]
    if active:
        titles = [o.get("title", "?") for o in active]
        add(Fact("active_offers", "offers", titles, "active offers: " + "; ".join(titles),
                 "merchant.offers (status=active)"))
    else:
        add(Fact("no_active_offers", "offers", True, "no active offers right now", "merchant.offers"))
    if inactive:
        parts = []
        for offer in inactive:
            ended = fmt_date(offer.get("ended"))
            status = offer.get("status") or "inactive"
            parts.append(f"{offer.get('title', '?')} ({status}{', ended ' + ended if ended else ''})")
        add(Fact("past_offers", "offers", [o.get("title") for o in inactive], "past offers: " + "; ".join(parts),
                 "merchant.offers (status!=active)"))
    tried = {offer_key(o.get("title")) for o in offers}
    untried = [o for o in (category or {}).get("offer_catalog", [])
               if isinstance(o, dict) and o.get("title") and offer_key(o["title"]) not in tried]
    if untried:
        untried.sort(key=lambda o: _OFFER_TYPE_ORDER.get(o.get("type"), 6))
        titles = [o["title"] for o in untried]
        add(Fact("catalog_offers_not_run", "offers", titles,
                 "category offers this merchant hasn't run: " + "; ".join(titles[:5]),
                 "category.offer_catalog minus merchant.offers"))

    # --- subscription ---
    sub = merchant["subscription"]
    status = str(sub.get("status") or "unknown").lower()
    days_left = f", {fmt_number(sub['days_remaining'])} days left" if is_number(sub.get("days_remaining")) else ""
    if status == "active":
        text = f"{sub['plan'] + ' plan' if sub.get('plan') else 'subscription'} active{days_left}"
    elif status == "expired":
        ago = f" {fmt_number(sub['days_since_expiry'])} days ago" if is_number(sub.get("days_since_expiry")) else ""
        text = f"subscription expired{ago}"
    elif status == "trial":
        text = f"on a trial{days_left}"
    else:
        text = f"subscription status: {humanize(status)}"
    add(Fact("subscription", "subscription", dict(sub), text, "merchant.subscription"))

    # --- reviews ---
    for review in merchant["review_themes"]:
        theme = review_theme_label(review.get("theme"))
        count = review.get("occurrences_30d")
        text = (f"{fmt_number(count)} reviews in the last 30 days mention {theme}" if is_number(count)
                else f"reviews mention {theme}")
        sentiment = {"neg": "negative", "pos": "positive"}.get(review.get("sentiment"), review.get("sentiment"))
        if sentiment:
            text += f" ({sentiment})"
        if review.get("common_quote"):
            text += f': "{review["common_quote"]}"'
        add(Fact(f"review_theme_{_slug(review.get('theme'))}", "reviews", dict(review), text,
                 "merchant.review_themes"))

    # --- signals (internal flags; the display is plain words, never the raw code) ---
    for raw in merchant["signals"]:
        signal = parse_signal(raw)
        add(Fact(f"signal_{signal['name']}", "signals", signal, signal_display(signal), "merchant.signals"))
    return facts


def richness(merchant: dict) -> dict:
    """How much merchant-specific material there is. Generated merchants score 'sparse':
    no offers, history, signals or review themes."""
    present = {
        "offers": bool(merchant["offers"]),
        "conversation_history": bool(merchant["conversation_history"]),
        "signals": bool(merchant["signals"]),
        "review_themes": bool(merchant["review_themes"]),
        "customer_aggregate": len(merchant["customer_aggregate"]) > 1,
    }
    score = sum(present.values())
    return {"level": "rich" if score >= 4 else "moderate" if score >= 2 else "sparse",
            "score": score, "max": len(present),
            "present": [k for k, v in present.items() if v],
            "missing": [k for k, v in present.items() if not v]}


# =============================================================================
# CATEGORY
# =============================================================================

_NEUTRAL_SKEW = {"balanced", "none", "all", "mixed", "neutral"}


def category_facts(category: dict, merchant: dict | None, now: datetime) -> list[Fact]:
    facts: list[Fact] = []
    add = facts.append
    peer = category["peer_stats"]
    if peer.get("scope"):
        add(Fact("peer_group", "category", peer["scope"], f"peer group: {humanize(peer['scope'])}",
                 "category.peer_stats.scope"))
    benchmarks = (("avg_rating", "peer_avg_rating", "peers average a {}★ rating"),
                  ("avg_review_count", "peer_avg_reviews", "peers average {} reviews"),
                  ("avg_post_freq_days", "peer_post_frequency", "peers post on Google every {} days on average"),
                  ("avg_photos", "peer_avg_photos", "peers have {} photos on average"))
    for field_name, key, template in benchmarks:
        if is_number(peer.get(field_name)):
            add(Fact(key, "category", peer[field_name], template.format(fmt_number(peer[field_name])),
                     f"category.peer_stats.{field_name}"))

    month = now.astimezone(IST).month
    for beat in category["seasonal_beats"]:
        if isinstance(beat, dict) and month in months_in_range(beat.get("month_range")):
            add(Fact(f"season_{_slug(beat.get('month_range'))}", "season", dict(beat),
                     f"{beat.get('month_range')}: {beat.get('note')}", "category.seasonal_beats"))

    city = str(((merchant or {}).get("identity") or {}).get("city") or "").lower()
    for trend in category["trend_signals"]:
        if not isinstance(trend, dict) or not trend.get("query"):
            continue
        text = f'"{trend["query"]}" searches'
        if is_number(trend.get("delta_yoy")):
            text += f" {fmt_pct(trend['delta_yoy'], signed=True)} year-on-year"
        age, skew = trend.get("segment_age"), trend.get("skew")
        age_text = humanize(age) if age else ""
        details = [(f"age {age_text}" if age_text[:1].isdigit() else age_text)
                   if age_text and age_text.lower() not in ("all", "any") else None,
                   f"skews {humanize(skew)}" if skew and str(skew).lower() not in _NEUTRAL_SKEW else None]
        details = [d for d in details if d]
        if details:
            text += f" ({', '.join(details)})"
        local = bool(city) and city in trend["query"].lower()
        add(Fact(f"trend_{_slug(trend['query'])}", "trends", {**trend, "local": local}, text,
                 "category.trend_signals"))
    return facts


# =============================================================================
# CUSTOMER
# =============================================================================

CUSTOMER_STATE_LABELS = {"new": "new", "active": "active", "lapsed_soft": "recently lapsed",
                         "lapsed_hard": "lapsed for a long time", "churned": "churned"}


def _preference_fact(key: str, value: Any) -> Fact | None:
    if key in ("channel", "reminder_opt_in") or value in (None, "", [], {}):
        return None
    if key == "preferred_slots":
        text = f"prefers {humanize(value)} slots"
    elif key == "preferred_stylist":
        text = f"preferred stylist: {value}"
    elif key == "wedding_date":
        text = f"wedding on {fmt_date(value) or value}"
    elif key == "delivery_address":
        text = "delivery address saved" if value == "saved" else f"delivery address: {value}"
    elif key in ("family_size", "household_size"):
        text = f"household of {fmt_number(value)}"
    elif value is True:
        text = humanize(key)
    else:
        text = f"{humanize(key)}: {humanize(value) if isinstance(value, str) else value}"
    return Fact(f"customer_pref_{key}", "customer", value, text, f"customer.preferences.{key}")


def customer_facts(customer: dict, now: datetime) -> list[Fact]:
    facts: list[Fact] = []
    add = facts.append
    identity, rel = customer["identity"], customer["relationship"]
    prefs, consent = customer["preferences"], customer["consent"]

    person = parse_person_name(identity.get("name"))
    if not person["anonymous"]:
        add(Fact("customer_name", "customer", person, person["subject"], "customer.identity.name"))
        if person["relation"]:
            add(Fact("customer_guardian", "customer", person["addressee"],
                     f"{person['subject']} is a minor; messages go to their {person['relation']} {person['addressee']}",
                     "customer.identity.name"))
    band = identity.get("age_band")
    if band and band != "unknown":
        add(Fact("customer_age_band", "customer", band, f"age group {humanize(band)}", "customer.identity.age_band"))
    if identity.get("senior_citizen"):
        add(Fact("customer_senior", "customer", True, "senior citizen", "customer.identity.senior_citizen"))
    state = customer.get("state")
    add(Fact("customer_state", "customer", state,
             f"customer status: {CUSTOMER_STATE_LABELS.get(state, humanize(state))}", "customer.state"))

    visits = rel.get("visits_total")
    if is_number(visits):
        since = fmt_date(rel.get("first_visit"))
        add(Fact("customer_visits", "customer", visits,
                 f"{fmt_number(visits)} visit{'' if visits == 1 else 's'}" + (f" since {since}" if since else ""),
                 "customer.relationship.visits_total"))
    last = parse_dt(rel.get("last_visit"))
    if last:
        add(Fact("customer_last_visit", "customer", rel["last_visit"], f"last visit {fmt_date(last)}",
                 "customer.relationship.last_visit"))
        days = (now - last).days
        if days >= 0:  # the dataset's timelines disagree; never state a negative gap
            add(Fact("customer_days_since_last_visit", "customer", days, f"{days} days since the last visit",
                     "customer.relationship.last_visit vs now"))
    raw_services = [s for s in rel["services_received"] if isinstance(s, str)]
    services = [s for s in raw_services if re.search(r"[A-Za-z0-9]", s)]
    truncated = len(services) < len(raw_services)  # some seed lists end with a literal "..."
    if services:
        text = ", ".join(humanize(s) + (f" ×{n}" if n > 1 else "") for s, n in Counter(services).most_common())
        add(Fact("customer_services", "customer", {"services": services, "truncated": truncated},
                 f"services so far {'include' if truncated else 'are'}: {text}",
                 "customer.relationship.services_received"))
    if is_number(rel.get("lifetime_value")):
        add(Fact("customer_lifetime_value", "customer", rel["lifetime_value"],
                 f"{fmt_inr(rel['lifetime_value'])} spent so far", "customer.relationship.lifetime_value"))
    if rel.get("favourite_dish"):
        add(Fact("customer_favourite_dish", "customer", rel["favourite_dish"],
                 f"favourite dish: {rel['favourite_dish']}", "customer.relationship.favourite_dish"))
    conditions = rel.get("chronic_conditions")
    if isinstance(conditions, list) and conditions:
        add(Fact("customer_chronic_conditions", "customer_sensitive", conditions,
                 "chronic conditions on file: " + ", ".join(humanize(c) for c in conditions),
                 "customer.relationship.chronic_conditions"))
    for key, value in prefs.items():
        fact = _preference_fact(key, value)
        if fact:
            add(fact)

    scopes = [s for s in consent["scope"] if isinstance(s, str)]
    opted = fmt_date(consent.get("opted_in_at"))
    if scopes:
        text = "consented" + (f" on {opted}" if opted else "") + " to: " + ", ".join(humanize(s) for s in scopes)
    else:
        text = "no messaging consent on file"
    add(Fact("customer_consent", "consent", scopes, text, "customer.consent"))
    if isinstance(prefs.get("reminder_opt_in"), bool):
        add(Fact("customer_reminder_opt_in", "consent", prefs["reminder_opt_in"],
                 "opted in to reminders" if prefs["reminder_opt_in"] else "has NOT opted in to reminders",
                 "customer.preferences.reminder_opt_in"))
    return facts


# =============================================================================
# CONVERSATION HISTORY
# =============================================================================

INTENT_TAGS = {"intent_action", "intent_question", "intent_planning"}
_EPOCH = datetime.min.replace(tzinfo=timezone.utc)


def _hours_since(turn: dict | None, now: datetime) -> float | None:
    when = parse_dt(turn["ts"]) if turn else None
    if when is None:
        return None
    hours = (now - when).total_seconds() / 3600
    return round(hours, 1) if hours >= 0 else None


def _turn_view(turn: dict | None, hours: float | None, *, with_language: bool = False) -> dict | None:
    if not turn:
        return None
    view = {"ts": turn["ts"], "body": turn["body"], "engagement": turn["engagement"],
            "hours_ago": hours, "origin": turn["origin"]}
    if with_language:
        view["language"] = detect_language(turn["body"])
    return view


def history_summary(merchant: dict | None, live_turns: list | None, now: datetime) -> dict:
    """Pushed conversation_history merged with live turns from RuntimeState."""
    turns = [{"ts": h.get("ts"), "from": h.get("from"), "body": h.get("body") or "",
              "engagement": h.get("engagement"), "origin": "context"}
             for h in (merchant or {}).get("conversation_history", [])]
    turns += [{"ts": t.ts, "from": "vera" if t.sender == "bot" else t.sender, "body": t.body,
               "engagement": None, "origin": "live"}
              for t in live_turns or [] if t.meta.get("kind") != "auto_reply"]  # a bot's canned text isn't a reply
    turns.sort(key=lambda t: parse_dt(t["ts"]) or _EPOCH)

    vera = [t for t in turns if t["from"] == "vera"]
    merchant_turns = [t for t in turns if t["from"] == "merchant"]

    # A merchant request with no Vera turn after it is still waiting on us.
    open_requests = []
    for i, turn in enumerate(turns):
        if turn["from"] == "merchant" and turn["engagement"] in INTENT_TAGS \
                and not any(later["from"] == "vera" for later in turns[i + 1:]):
            prior = next((t for t in reversed(turns[:i]) if t["from"] == "vera"), None)
            open_requests.append({"ts": turn["ts"], "message": turn["body"], "engagement": turn["engagement"],
                                  "in_reply_to": prior["body"] if prior else None})

    # Trailing Vera messages nobody answered (feeds the brief's "stop after 3 unanswered nudges").
    streak = 0
    for turn in reversed(turns):
        if turn["from"] == "merchant" or turn["engagement"] == "merchant_replied":
            break
        if turn["from"] == "vera":
            streak += 1

    last_vera = vera[-1] if vera else None
    last_merchant = merchant_turns[-1] if merchant_turns else None
    hours_since_merchant = _hours_since(last_merchant, now)
    return {
        "turn_count": len(turns),
        "last_vera_message": _turn_view(last_vera, _hours_since(last_vera, now)),
        "last_merchant_message": _turn_view(last_merchant, hours_since_merchant, with_language=True),
        "open_requests": open_requests,
        "unanswered_streak": streak,
        # First outbound needs an approved template unless the merchant wrote in the last 24h.
        "session_window_open": hours_since_merchant is not None and hours_since_merchant <= 24,
        "recent_vera_bodies": [t["body"] for t in vera[-5:]],
        "engagement_tags": sorted({t["engagement"] for t in turns if t["engagement"]}),
    }


# =============================================================================
# LANGUAGE AND GREETINGS
# =============================================================================

_PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")
_GREETING_WORD_RE = re.compile(r"^(hi|hello|hey|dear|namaste)\s+", re.I)
_PERSON_FIELDS = {"first_name", "owner_first_name", "pharmacist_name", "chef_or_owner_first_name",
                  "doctor_name", "coach_name"}


def _is_person_template(template: str) -> bool:
    fields = _PLACEHOLDER_RE.findall(template)
    return bool(fields) and all(f in _PERSON_FIELDS or f.endswith("first_name") for f in fields)


def merchant_greeting(merchant: dict, category: dict | None) -> dict:
    """Fill the category's salutation template ('Dr. {first_name}', 'Hi {pharmacist_name}', ...)."""
    identity = merchant["identity"]
    honorific, first = split_honorific(identity.get("owner_first_name"))
    business = identity.get("name") or ""
    templates = [t for t in (category or {}).get("voice", {}).get("salutation_examples", []) if isinstance(t, str)]
    template = next((t for t in templates if first and _is_person_template(t)), None)
    if template is None and business:
        template = next((t for t in templates if _PLACEHOLDER_RE.search(t) and not _is_person_template(t)), None)
    if template:
        greeting = _PLACEHOLDER_RE.sub(
            lambda m: first if (m.group(1) in _PERSON_FIELDS or m.group(1).endswith("first_name")) else business,
            template)
    else:
        greeting = f"Hi {first}" if first else (f"Hi {business} team" if business else "Hi")
    address_as = _GREETING_WORD_RE.sub("", greeting).strip() or None
    if honorific in ("Dr.", "Prof.") and address_as == first:
        address_as = f"{honorific} {first}"
    return {"greeting": greeting, "address_as": address_as, "first_name": first or None,
            "honorific": honorific, "template": template, "about": None, "relation": None}


def customer_greeting(customer: dict, language_codes: list[str]) -> dict:
    person = parse_person_name(customer["identity"].get("name"))
    if person["anonymous"]:
        return {"greeting": "Hi", "address_as": None, "first_name": None, "honorific": None,
                "template": None, "about": None, "relation": None}
    address_as = person["addressee"]
    senior = bool(customer["identity"].get("senior_citizen"))
    hindi = "hi" in language_codes
    if senior and hindi and person["honorific"] in ("Mr.", "Mrs.", "Shri", "Smt."):
        address_as = f"{person['bare_name']} ji"
    return {"greeting": f"{'Namaste' if senior and hindi else 'Hi'} {address_as}", "address_as": address_as,
            "first_name": person["bare_name"], "honorific": person["honorific"], "template": None,
            "about": person["subject"] if person["relation"] else None, "relation": person["relation"]}


def language_profile(merchant: dict | None, category: dict | None, customer: dict | None,
                     audience: str) -> dict:
    """Who we're writing to, how to address them and which language mix to use."""
    slug = (merchant or {}).get("category_slug") or (category or {}).get("slug")
    code_mix = (category or {}).get("voice", {}).get("code_mix")
    base = {"audience": audience, "customer_noun": customer_noun(slug),
            "category_code_mix": humanize(code_mix) if code_mix else None}

    if audience == "customer" and customer:
        pref = parse_language_pref(customer["identity"].get("language_pref"))
        codes = pref["codes"] or ["en"]
        other = next((c for c in codes if c != "en"), None)
        if other and pref["mix"]:
            style, display = f"{other}-en", f"{LANGUAGE_NAMES[other]}-English mix" + (" (Hinglish)" if other == "hi" else "")
        elif other:
            style, display = other, LANGUAGE_NAMES[other]
        else:
            style, display = "en", "English"
        return {**base, **customer_greeting(customer, codes), "languages": codes, "style": style,
                "display": display, "code_mix": other if pref["mix"] else None, "regional_languages": [],
                "source": "customer.identity.language_pref"}

    raw = (merchant or {}).get("identity", {}).get("languages", [])
    codes = list(dict.fromkeys(c for c in (language_code(x) for x in raw) if c)) or ["en"]
    hindi = "hi" in codes
    greeting = merchant_greeting(merchant, category) if merchant else {
        "greeting": "Hi", "address_as": None, "first_name": None, "honorific": None,
        "template": None, "about": None, "relation": None}
    return {**base, **greeting, "languages": codes, "style": "hi-en" if hindi else "en",
            "display": "English with natural Hindi code-mix (Hinglish)" if hindi else "English",
            "code_mix": "hi" if hindi else None,
            "regional_languages": [c for c in codes if c not in ("en", "hi")],
            "source": "merchant.identity.languages"}
