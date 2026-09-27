"""Phase 2: turn one trigger's ContextBundle into a writing brief (a FactSheet).

The brief says what to lead with, which 2-3 facts back it up, the angle, the single
ask and what to avoid. There is no AI here: phase 3 writes from the brief, and
templates.render() turns it into a plain message on its own (the fallback).

Every trigger kind has a Recipe: a lead builder (the "why now"), supporting-fact
selectors in order of preference, an angle, persuasion levers and an ask. Kinds we
have never seen use their family's default recipe.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Callable

from .bundle import ContextBundle
from .derive import AGG_SHARE_LABELS, Fact, review_theme_label
from .normalize import (IST, LANGUAGE_NAMES, fmt_date, fmt_datetime, fmt_inr, fmt_number, fmt_pct, humanize,
                        is_number, months_in_range, number_tokens, parse_dt, pct_decimals)
from .state import RuntimeState

# =============================================================================
# FAMILIES
# =============================================================================

FAMILIES = {
    "news": ("research_digest", "regulation_change", "cde_opportunity", "supply_alert", "category_seasonal"),
    "performance": ("perf_dip", "perf_spike", "seasonal_perf_dip", "milestone_reached"),
    "account": ("renewal_due", "winback_eligible", "dormant_with_vera", "gbp_unverified"),
    "event": ("festival_upcoming", "ipl_match_today", "competitor_opened"),
    "followup": ("active_planning_intent", "curious_ask_due"),
    "reviews": ("review_theme_emerged",),
    "customer": ("recall_due", "appointment_tomorrow", "chronic_refill_due", "customer_lapsed_soft",
                 "customer_lapsed_hard", "trial_followup", "wedding_package_followup"),
}
KIND_FAMILY = {kind: family for family, kinds in FAMILIES.items() for kind in kinds}

BUSINESS_NOUN = {"dentists": "clinics", "gyms": "gyms", "salons": "salons", "restaurants": "restaurants",
                 "pharmacies": "pharmacies"}
ASK_ITEM = {"dentists": "treatment", "gyms": "class", "salons": "service", "restaurants": "dish",
            "pharmacies": "product"}
LOCAL_GREETING = {"ta": "Vanakkam", "te": "Namaskaram", "kn": "Namaskara"}
CTA_LABELS = {"binary_yes_no": "yes/no", "binary_confirm_cancel": "confirm", "open_ended": "open question",
              "multi_choice_slot": "pick a slot", "none": "no ask"}

# Asks per recipe: (cta, English, Hinglish or ""). Hinglish is used only where the audience's
# language calls for it. Vera speaks as a woman in the reference chats ("kar sakti hoon").
ASKS = {
    "research": ("binary_yes_no", "Want me to pull the key points into a WhatsApp for your {noun}, ready in 5 min?",
                 "Kya main key points nikaal ke aapke {noun} ke liye WhatsApp draft kar doon, 5 min mein ready?"),
    "regulation": ("binary_yes_no", "Want a 1-page checklist of what to change before the deadline, ready in 10 min?",
                   "Kya main deadline se pehle ki 1-page checklist bana doon, 10 min mein ready?"),
    "cde": ("binary_yes_no", "Want me to send you the registration details?",
            "Kya main registration details bhej doon?"),
    "supply": ("binary_yes_no", "Want me to draft the note for affected customers plus a replacement-pickup plan?",
               "Kya main affected customers ke liye note aur replacement-pickup plan draft kar doon?"),
    "seasonal_demand": ("binary_yes_no", "Want a quick shelf-and-offer plan for this, ready in 10 min?",
                        "Kya main iske liye ek quick shelf aur offer plan bana doon, 10 min mein ready?"),
    "perf_dip": ("binary_yes_no", "Want two quick fixes you can try this week, drafted in 5 min?",
                 "Kya main is hafte ke liye do quick fixes bhej doon, 5 min mein?"),
    "perf_spike": ("binary_yes_no", "Want me to line up two more posts like the one that worked?",
                   "Kya main isi tarah ke do aur posts plan kar doon?"),
    "seasonal_dip": ("binary_yes_no", "Want me to draft a retention challenge to keep your current {noun} coming in?",
                     "Kya main aapke current {noun} ko engaged rakhne ke liye ek retention challenge draft kar "
                     "doon?"),
    "milestone": ("binary_yes_no", "Want me to draft a 2-line review request for your happy {noun}?",
                  "Kya main aapke happy {noun} ke liye 2-line review request draft kar doon?"),
    "renewal": ("binary_yes_no", "Want me to line up the renewal so nothing pauses? Just reply YES.",
                "Kya main renewal line up kar doon taaki kuch ruke nahi? Bas YES reply kijiye."),
    "winback": ("binary_yes_no", "Want me to walk you through restarting in 3 steps?",
                "Kya main 3 steps mein restart karne ka process bata doon?"),
    "dormant": ("binary_yes_no", "Want me to show how this could work for your business, in 2 min?",
                "Kya main 2 min mein bataun ki yeh aapke liye kaise kaam kar sakta hai?"),
    "gbp": ("binary_yes_no", "Want me to send the verification steps here, one by one?",
            "Kya main verification ke steps yahin ek-ek karke bhej doon?"),
    "festival": ("binary_yes_no", "Want me to draft a festive offer, a Google post and a WhatsApp blast for you?",
                 "Kya main aapke liye festive offer, Google post aur WhatsApp blast draft kar doon?"),
    "ipl": ("binary_yes_no", "Want me to draft a match-night post and an Insta story around your current offer?",
            "Kya main aapke current offer par match-night post aur Insta story draft kar doon?"),
    "competitor": ("binary_yes_no", "Want me to draft a Google post on what sets you apart, ready in 10 min?",
                   "Kya main ek Google post draft kar doon jo dikhaye ki aap alag kyun hain, 10 min mein ready?"),
    "planning": ("binary_yes_no", "Want me to turn this into a Google post and a WhatsApp you can share, ready in 10 min?",
                 "Kya main ise Google post aur share karne layak WhatsApp mein badal doon, 10 min mein ready?"),
    "curious": ("open_ended", "Tell me the most asked-for {item} this week, and I'll turn it into a Google post "
                "plus a ready WhatsApp reply for price questions.",
                "Is hafte kis {item} ki sabse zyada demand rahi? Bataiye, main uska Google post aur price ke "
                "sawaalon ke liye ek ready WhatsApp reply bana doongi."),
    "reviews": ("binary_yes_no", "Want me to draft a reply to these reviews and a short fix note for your team?",
                "Kya main in reviews ka reply aur team ke liye ek short fix note draft kar doon?"),
    "general": ("binary_yes_no", "Want me to help with this?",
                "Kya main isme help karoon?"),
    # customer-facing (sent as the shop)
    "appointment": ("binary_confirm_cancel", "Reply YES to confirm, or let us know if you need to reschedule.",
                    "Confirm karne ke liye YES reply kijiye, ya reschedule ke liye bataiye."),
    "lapsed": ("binary_yes_no", "Reply YES and we'll book a time that suits you.",
               "YES reply kijiye, hum aapke liye convenient time book kar denge."),
    "wedding": ("binary_yes_no", "Reply YES and we'll book your first session.",
                "YES reply kijiye, hum aapka pehla session book kar denge."),
    "customer_general": ("binary_yes_no", "Reply YES if you'd like us to set this up.",
                         "Agar aap chahein toh YES reply kijiye."),
}

# Merchant-facing event wording for triggers whose payload carries no details.
_GENERIC_EVENT = {
    "perf_dip": "your recent numbers show a dip",
    "perf_spike": "your recent numbers show a jump",
    "seasonal_perf_dip": "your numbers are in the usual seasonal dip",
    "milestone_reached": "you've hit a milestone worth marking",
    "renewal_due": "your subscription renewal is coming up",
    "winback_eligible": "your subscription is paused",
    "gbp_unverified": "your Google profile isn't verified yet",
    "festival_upcoming": "the festival season is coming up",
    "ipl_match_today": "there's an IPL match on today",
    "competitor_opened": "a new competitor has opened nearby",
    "review_theme_emerged": "a pattern is showing up in your recent reviews",
    "category_seasonal": "the seasonal demand shift is starting",
    "active_planning_intent": "picking up the plan you asked about",
    "regulation_change": "there's a regulation update for your category",
    "supply_alert": "there's a product alert for your category",
    "cde_opportunity": "there's a training opportunity coming up",
}
# Customer-facing openers for the same case: (English, Hinglish).
_GENERIC_CUSTOMER = {
    "recall_due": ("it's time for your next visit", "aapki agli visit ka time ho gaya hai"),
    "appointment_tomorrow": ("a quick reminder that your appointment with us is tomorrow",
                             "yaad dila dein, kal aapka appointment hai"),
    "chronic_refill_due": ("your regular medicines are due for a refill", "aapki regular dawaiyon ka refill due hai"),
    "customer_lapsed_soft": ("we'd love to see you again soon", "hum aapko jald hi phir se dekhna chahenge"),
    "customer_lapsed_hard": ("we'd love to see you again soon", "hum aapko jald hi phir se dekhna chahenge"),
    "trial_followup": ("thanks for trying us out", "humein try karne ke liye shukriya"),
    "wedding_package_followup": ("we're ready to help with your wedding prep", "aapki wedding prep ke liye hum ready hain"),
}
_NEUTRAL_CUSTOMER = ("a quick note from us", "aapke liye ek chhota sa update")
# Trigger kinds whose news item comes from the category digest when the trigger names none.
_TOPIC_DIGEST_KINDS = {"research_digest": ("research", "trend", "tech"), "regulation_change": ("compliance",),
                       "cde_opportunity": ("cde",), "supply_alert": ("alert", "supply")}


# =============================================================================
# DATA SHAPES
# =============================================================================


@dataclass
class Line:
    """One fact as the brief states it, plus wording that can sit inside a message."""

    text: str               # the fact, as the writer should understand it
    source: str             # dataset fields it came from
    key: str                # stable id: a fact key, "digest:<id>" or "payload:<field>"
    phrase: str = ""        # English clause for templates.py ("" = brief only, not rendered)
    phrase_hi: str = ""     # Hinglish clause, for audiences that want it


@dataclass(frozen=True)
class Recipe:
    lead: Callable[["_Context"], Line | None]
    support: tuple[str, ...]            # selector names, in order of preference
    angle: str
    levers: tuple[str, ...]
    ask: str                            # key into ASKS (customer asks are built from slots)
    related: tuple[str, ...] = ()       # digest search terms for the "related_digest" selector
    related_kinds: tuple[str, ...] = ()  # digest kinds for the same selector
    related_field: str = "summary"      # which part of that digest item to use: "summary" or "actionable"
    render_support: int = 2             # supporting facts the plain template shows (the brief keeps all)


@dataclass
class _Context:
    bundle: ContextBundle
    recipe: Recipe
    digest: dict | None                 # the news item this message is about, if any
    digest_picked: bool = False         # the trigger named none; we took the category's current one


@dataclass
class FactSheet:
    trigger_id: str
    kind: str
    family: str
    audience: str                       # "merchant" or "customer"
    send_as: str                        # "vera" or "merchant_on_behalf"
    merchant_id: str | None
    customer_id: str | None
    recipient_id: str | None
    sender_name: str | None             # the shop's name (customer messages open with it)
    greeting: str
    address_as: str | None
    language: dict                      # {"style", "instruction", "hinglish"}
    lead: Line
    support: list[Line]
    angle: str
    levers: list[str]
    ask: dict                           # {"cta", "text", "text_hi", "intent"}
    template: dict                      # {"required", "name"}
    instructions: list[str]
    avoid: list[str]
    allowed_numbers: list[str]
    suppression_key: str
    urgency: int
    flags: list[str]
    notes: list[str] = field(default_factory=list)   # what we adapted and why (feeds the rationale)
    render_support: int = 2                          # supporting facts the plain template shows
    vocabulary: list[str] = field(default_factory=list)  # category words; the validator's service check (not prompted)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_prompt(self) -> str:
        """The brief as plain text for the phase 3 writer."""
        if self.audience == "customer":
            to = f"{self.address_as or 'a customer'}, a customer of {self.sender_name}"
            sender = f"{self.sender_name}, on the shop's behalf (not Vera)"
        else:
            to = f"{self.address_as or 'the owner'}, owner of {self.sender_name}"
            sender = "Vera, magicpin's merchant assistant"
        ask_text = self.ask["text_hi"] if self.language.get("hinglish") and self.ask.get("text_hi") else self.ask["text"]
        form = ("first message in this chat window, so keep it template-shaped: greeting, "
                "2-3 short sentences, then the ask" if self.template["required"] else "free-form reply allowed")
        if self.kind == "active_planning_intent":
            form = ("an editable outline: greeting and one short line of context, then 2-4 short lines starting "
                    "with '- ', then the ask")
        lines = [
            "Write one WhatsApp message.",
            f"To: {to}. Sent as: {sender}.",
            f"Greeting: {self.greeting}",
            f"Language: {self.language['instruction']}",
            f"Why now: {self.lead.text}",
            "Supporting facts (use only these):",
            *[f"- {line.text}" for line in self.support],
            f"Angle: {self.angle}. Levers: {', '.join(humanize(lever) for lever in self.levers)}.",
            f"Ask, one only, as the last sentence ({CTA_LABELS.get(self.ask['cta'], self.ask['cta'])}): "
            f"{ask_text}",
            f"Format: {form}.",
            "Rules:",
            *[f"- {rule}" for rule in self.instructions],
            f"- Numbers may only come from: {', '.join(self.allowed_numbers) or 'none'}.",
        ]
        if self.avoid:
            lines.append(f"- Never use: {', '.join(self.avoid)}.")
        return "\n".join(lines)


# =============================================================================
# SMALL HELPERS
# =============================================================================

_ISO_DATE_IN_TEXT = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
_SENTENCE_END = re.compile(r"(?<!\bDr)(?<!\bMr)(?<!\bMs)(?<!\bvs)(?<!\b[A-Z])\.\s+")


def _pretty(text: Any) -> str:
    """Dataset prose tidied for messages: ISO dates become '15 Dec 2026', no trailing full stop."""
    out = _ISO_DATE_IN_TEXT.sub(lambda m: fmt_date(m.group(0)) or m.group(0), str(text or "")).strip()
    return out[:-1] if out.endswith(".") else out


def _first_sentence(text: Any) -> str:
    return _SENTENCE_END.split(_pretty(text), maxsplit=1)[0].strip()


def _join_words(items: list[str], conjunction: str = "and") -> str:
    items = [humanize(i) for i in items]
    return items[0] if len(items) == 1 else f"{', '.join(items[:-1])} {conjunction} {items[-1]}"


def _payload(b: ContextBundle) -> dict:
    return b.trigger["payload"]


def _shown(b: ContextBundle, key: str) -> str | None:
    """A payload value as display text, or None if it isn't plain text."""
    value = b.payload_display.get(key)
    return value if isinstance(value, str) and value else None


def _slug(b: ContextBundle) -> str | None:
    return (b.merchant or {}).get("category_slug") or (b.category or {}).get("slug")


def _verb(noun: str) -> str:
    return "are" if noun.endswith("s") else "is"


def _active_offer_titles(b: ContextBundle) -> list[str]:
    return [o["title"] for o in (b.merchant or {}).get("offers", [])
            if str(o.get("status", "")).lower() == "active" and o.get("title")]


def _category_digest(b: ContextBundle, *, kinds: tuple[str, ...] = (), terms: tuple[str, ...] = (),
                     exclude: set[str] | None = None) -> dict | None:
    fresh = set(b.fresh.get("new_digest_items", []))
    items = [d for d in (b.category or {}).get("digest", [])
             if isinstance(d, dict) and d.get("title") and d.get("id") not in (exclude or set())]
    items.sort(key=lambda d: d.get("id") not in fresh)  # items pushed mid-test first (judge bonus)
    if terms:
        pattern = re.compile(r"\b(" + "|".join(re.escape(t) for t in terms) + r")", re.I)
        items = [d for d in items if pattern.search(f"{d.get('title', '')} {d.get('summary', '')}")]
    for kind in kinds or (None,):
        for item in items:
            if kind is None or item.get("kind") == kind:
                return item
    return None


def _metric_label(metric: str) -> tuple[str, bool]:
    """Label for 'your {label} is/are ...' and whether it's plural."""
    known = {"ctr": ("CTR", False), "views": ("profile views", True), "calls": ("calls", True),
             "directions": ("direction requests", True)}
    if metric in known:
        return known[metric]
    return AGG_SHARE_LABELS.get(metric, humanize(metric)), False


def _phrase_for(b: ContextBundle, fact: Fact) -> str:
    """A derived fact worded to sit inside a message."""
    value = fact.value
    if fact.group == "peer" and isinstance(value, dict) and "merchant" in value:
        metric = fact.key[: -len("_vs_peer")]
        mine, peer = value["merchant"], value["peer"]
        if metric == "ctr" or metric.endswith("_pct"):
            decimals = pct_decimals(mine, peer)
            mine_text, peer_text = fmt_pct(mine, decimals=decimals), fmt_pct(peer, decimals=decimals)
        else:
            mine_text, peer_text = fmt_number(mine), fmt_number(peer)
        label, plural = _metric_label(metric)
        return (f"your {label} {'are' if plural else 'is'} {mine_text} vs {peer_text} "
                f"for similar {BUSINESS_NOUN.get(_slug(b), 'businesses')}")
    if fact.group == "customers" and is_number(value):
        if fact.key.endswith("_pct"):
            return f"your {_metric_label(fact.key)[0]} is {fmt_pct(value)}"
        verb = "you've had" if "orders" in fact.key else "you have"
        return f"{verb} {fact.display}"
    if fact.key == "gbp_verified":
        return "your Google profile is verified" if value else "your Google profile isn't verified yet"
    if fact.key == "active_offers" and isinstance(value, list) and value:
        if len(value) == 1:
            return f"your {value[0]} offer is live"
        return f"your {', '.join(value[:-1])} and {value[-1]} offers are live"
    if fact.group == "season" and isinstance(value, dict):
        return f"the usual {value.get('month_range')} pattern: {value.get('note')}"
    if fact.group == "trends" and isinstance(value, dict) and is_number(value.get("delta_yoy")):
        delta = value["delta_yoy"]
        return (f'searches for "{value["query"]}" are {"up" if delta >= 0 else "down"} '
                f"{fmt_pct(abs(delta))} year-on-year")
    if fact.group == "reviews" and isinstance(value, dict):
        count = value.get("occurrences_30d")
        theme = review_theme_label(value.get("theme"))
        text = f"{fmt_number(count)} reviews in the last 30 days mention {theme}" if is_number(count) \
            else f"reviews mention {theme}"
        return text + (f' ("{value["common_quote"]}")' if value.get("common_quote") else "")
    return fact.display


def _line(b: ContextBundle, fact: Fact | None) -> Line | None:
    return Line(fact.display, fact.source, fact.key, _phrase_for(b, fact)) if fact else None


def _first_fact(b: ContextBundle, *keys: str) -> Line | None:
    for key in keys:
        line = _line(b, b.fact(key))
        if line:
            return line
    return None


def _peer_extreme(b: ContextBundle, *, best: bool) -> Line | None:
    """Strongest above-peer (best) or weakest below-peer comparison; CTR wins ties of kind."""
    def goodness(f: Fact) -> float:
        ratio = f.value["ratio"]
        return ratio if f.value.get("higher_is_better", True) else (1 / ratio if ratio else 0.0)

    peers = [f for f in b.facts_in("peer") if isinstance(f.value, dict) and "ratio" in f.value]
    if best:
        picks = sorted((f for f in peers if goodness(f) > 1.05),
                       key=lambda f: (f.key != "ctr_vs_peer", -goodness(f)))
    else:
        picks = sorted((f for f in peers if goodness(f) < 0.95),
                       key=lambda f: (f.key != "ctr_vs_peer", goodness(f)))
    return _line(b, picks[0]) if picks else None


# =============================================================================
# SUPPORTING-FACT SELECTORS
# =============================================================================


def _sel_digest_summary(ctx: _Context) -> Line | None:
    item = ctx.digest
    if not item or not item.get("summary"):
        return None
    text = _pretty(item["summary"])
    phrase = text if len(text) <= 120 else _first_sentence(text)   # keep plain messages short
    return Line(text, f"category.digest[{item['id']}].summary", f"digest:{item['id']}:summary", phrase)


def _sel_digest_actionable(ctx: _Context) -> Line | None:
    item = ctx.digest
    if not item or not item.get("actionable"):
        return None
    text = _pretty(item["actionable"])
    return Line(text, f"category.digest[{item['id']}].actionable", f"digest:{item['id']}:actionable",
                f"the practical takeaway: {text[:1].lower()}{text[1:]}")


def _sel_cohort(ctx: _Context) -> Line | None:
    """The customer group a research item is about, e.g. 124 high-risk adult patients."""
    segment = (ctx.digest or {}).get("patient_segment")
    if not isinstance(segment, str):
        return None
    wanted = {t for t in re.split(r"[^a-z]+", segment.lower()) if len(t) > 2} - {"adult", "adults"}
    for fact in ctx.bundle.facts_in("customers"):
        if wanted and wanted <= set(fact.key.split("_")):
            return _line(ctx.bundle, fact)
    return None


def _sel_related_digest(ctx: _Context) -> Line | None:
    """A category digest item that backs this trigger up (e.g. IPL match-day order data)."""
    recipe, exclude = ctx.recipe, {ctx.digest["id"]} if ctx.digest else set()
    item = _category_digest(ctx.bundle, terms=recipe.related, exclude=exclude) if recipe.related else None
    if item is None and recipe.related_kinds:
        item = _category_digest(ctx.bundle, kinds=recipe.related_kinds, exclude=exclude)
    if not item:
        return None
    source, title = _pretty(item.get("source")), _pretty(item["title"])
    if recipe.related_field == "actionable" and item.get("actionable"):
        action = _pretty(item["actionable"])
        return Line(f"{title} ({source}): {action}", f"category.digest[{item['id']}].actionable",
                    f"digest:{item['id']}", f"the practical takeaway: {action[:1].lower()}{action[1:]}")
    first = _first_sentence(item.get("summary"))
    text = f"{title} ({source})" + (f": {first}" if first else "")
    return Line(text, f"category.digest[{item['id']}]", f"digest:{item['id']}",
                f"{first} ({source})" if first else f"{title} ({source})")


def _sel_untried_offer(ctx: _Context) -> Line | None:
    """Catalog offers the merchant hasn't run; one matching the message's news item comes first."""
    fact = ctx.bundle.fact("catalog_offers_not_run")
    if not fact:
        return None
    topic = f"{(ctx.digest or {}).get('title', '')} {(ctx.digest or {}).get('summary', '')}".lower()
    topic_words = {w for w in re.split(r"[^a-z]+", topic) if len(w) >= 5}
    ranked = sorted(fact.value, key=lambda t: -len(topic_words & set(re.split(r"[^a-z]+", t.lower()))))
    titles = ranked[:2]
    return Line(f"popular category offers not on their profile: {'; '.join(titles)}", fact.source, fact.key,
                f'one idea from the category catalog: a "{titles[0]}" offer')


def _sel_performance(ctx: _Context, metric: str) -> Line | None:
    fact = next((f for f in ctx.bundle.facts_in("performance")
                 if f.key.startswith(f"{metric}_") and f.key.endswith("d") and "change" not in f.key), None)
    return _line(ctx.bundle, fact)


def _sel_review(ctx: _Context, sentiment: str) -> Line | None:
    fact = next((f for f in ctx.bundle.facts_in("reviews")
                 if isinstance(f.value, dict) and f.value.get("sentiment") == sentiment), None)
    return _line(ctx.bundle, fact)


def _sel_unverified(ctx: _Context) -> Line | None:
    fact = ctx.bundle.fact("gbp_verified")
    return _line(ctx.bundle, fact) if fact and fact.value is False else None


def _sel_local_trend(ctx: _Context) -> Line | None:
    fact = next((f for f in ctx.bundle.facts_in("trends") if f.value.get("local")), None)
    return _line(ctx.bundle, fact)


def _sel_slots(ctx: _Context) -> Line | None:
    labels = [s["safe_label"] for s in ctx.bundle.slots]
    if not labels:
        return None
    return Line("available slots: " + "; ".join(labels), "trigger.payload slots (weekday checked)", "payload:slots")


def _offer_line(title: str, key: str) -> Line:
    return Line(f"active offer: {title}", "merchant.offers", key, f"{title} is available",
                f"{title} available hai")


def _sel_matching_offer(ctx: _Context) -> Line | None:
    """The shop's active offer for the service this message is about (e.g. cleaning -> ₹299 cleaning)."""
    b = ctx.bundle
    words: set[str] = set()
    for key in ("service_due", "next_step_window_open", "intent_topic"):
        words |= {w for w in re.split(r"[^a-z]+", (_shown(b, key) or "").lower()) if len(w) > 3}
    if b.trigger["kind"] == "wedding_package_followup":
        words |= {"bridal", "wedding"}
    words -= {"month", "program", "window", "open", "package"}
    for title in _active_offer_titles(b):
        if words & set(re.split(r"[^a-z]+", title.lower())):
            return _offer_line(title, "offer:matching")
    return None


def _sel_first_offer(ctx: _Context) -> Line | None:
    titles = _active_offer_titles(ctx.bundle)
    if not titles:
        return None
    return Line(f"active offer: {titles[0]}", "merchant.offers", "offer:first",
                f"our {titles[0]} offer is on right now", f"abhi hamara {titles[0]} offer chal raha hai")


def _sel_applicable_offers(ctx: _Context) -> Line | None:
    """Delivery and (for seniors) senior-citizen offers in one line, e.g. for a refill."""
    b = ctx.bundle
    senior = bool((b.customer or {}).get("identity", {}).get("senior_citizen"))
    titles = [t for t in _active_offer_titles(b) if "delivery" in t.lower() or (senior and "senior" in t.lower())]
    if not titles:
        return None
    if len(titles) == 1:
        return Line(f"active offer: {titles[0]}", "merchant.offers", "offer:applicable",
                    f"{titles[0]} applies", f"{titles[0]} lagu hai")
    return Line(f"active offers: {'; '.join(titles)}", "merchant.offers", "offer:applicable",
                f"{_join_plain(titles, 'and')} both apply", f"{_join_plain(titles, 'aur')} dono lagu hain")


def _join_plain(items: list[str], conjunction: str) -> str:
    return items[0] if len(items) == 1 else f"{', '.join(items[:-1])} {conjunction} {items[-1]}"


def _sel_reach(ctx: _Context) -> Line | None:
    """Views and calls as one line: '720 profile views and 14 calls in the last 30 days'."""
    b = ctx.bundle
    found = {}
    for metric in ("views", "calls"):
        fact = next((f for f in b.facts_in("performance")
                     if f.key.startswith(f"{metric}_") and f.key.endswith("d") and "change" not in f.key), None)
        if fact:
            found[metric] = fact
    if not found:
        return None
    days = next(iter(found.values())).key.split("_")[-1][:-1]
    parts = [f"{fmt_number(found['views'].value)} profile views"] if "views" in found else []
    parts += [f"{fmt_number(found['calls'].value)} calls"] if "calls" in found else []
    text = f"{' and '.join(parts)} in the last {days} days"
    return Line(text, "merchant.performance.views, calls", "performance:reach", f"you've had {text}")


def _sel_event_season(ctx: _Context) -> Line | None:
    """The category's seasonal note for the event's month (Diwali on 31 Oct -> the Oct-Dec note)."""
    b = ctx.bundle
    when = parse_dt(_payload(b).get("date"))
    if when is None:
        return None
    month = when.astimezone(IST).month
    for beat in (b.category or {}).get("seasonal_beats", []):
        if isinstance(beat, dict) and month in months_in_range(beat.get("month_range")):
            text = f"{beat.get('month_range')}: {beat.get('note')}"
            return Line(text, "category.seasonal_beats", f"season:{beat.get('month_range')}",
                        f"the usual {beat.get('month_range')} pattern: {beat.get('note')}")
    return None


def _sel_customer_visits(ctx: _Context) -> Line | None:
    b = ctx.bundle
    fact = b.fact("customer_visits")
    if not fact or not is_number(fact.value) or fact.value < 2:  # "thanks for your 1 visit" reads as filler
        return None
    count = f"{fmt_number(fact.value)} visits"
    since = fmt_date((b.customer or {}).get("relationship", {}).get("first_visit"))
    return Line(fact.display, fact.source, fact.key, f"thanks for your {count}" + (f" since {since}" if since else ""),
                (f"{since} se ab tak " if since else "") + f"{count} ke liye shukriya")


def _sel_last_visit(ctx: _Context) -> Line | None:
    """When they last came in: the concrete "why now" for a check-in, unless the records disagree about it."""
    b = ctx.bundle
    last, days = b.fact("customer_last_visit"), b.fact("customer_days_since_last_visit")
    if (not last or b.has("state_conflict") or b.has("time_inconsistent")
            or b.trigger["kind"] not in _RETURN_VISIT_KINDS):  # an appointment reminder is about tomorrow
        return None
    date = fmt_date((b.customer or {}).get("relationship", {}).get("last_visit"))
    if not date:
        return None
    ago = int(days.value) if days and is_number(days.value) and days.value > 0 else None
    return Line(last.display + (f" ({ago} days ago)" if ago else ""), last.source, last.key,
                f"your last visit was on {date}" + (f", {ago} days ago" if ago else ""),
                f"aapki last visit {date} ko thi" + (f", {ago} din pehle" if ago else ""))


def _sel_offer_containing(ctx: _Context, word: str) -> Line | None:
    title = next((t for t in _active_offer_titles(ctx.bundle) if word in t.lower()), None)
    if not title:
        return None
    return Line(f"active offer: {title}", "merchant.offers", f"offer:{word}", f"{title} applies",
                f"{title} lagu hai")


def _sel_senior_offer(ctx: _Context) -> Line | None:
    if not (ctx.bundle.customer or {}).get("identity", {}).get("senior_citizen"):
        return None
    return _sel_offer_containing(ctx, "senior")


def _sel_preferred_slot(ctx: _Context) -> Line | None:
    fact = ctx.bundle.fact("customer_pref_preferred_slots")
    if not fact or not isinstance(fact.value, str):
        return None
    slot = humanize(fact.value)
    return Line(fact.display, fact.source, fact.key, f"we know {slot} slots suit you best",
                f"{slot} slots aapke liye best rehte hain")


def _sel_customer_focus(ctx: _Context) -> Line | None:
    b = ctx.bundle
    prefs = (b.customer or {}).get("preferences", {})
    focus = _payload(b).get("previous_focus") or prefs.get("training_focus") or prefs.get("health_focus")
    if not isinstance(focus, str):
        return None
    return Line(f"their focus: {humanize(focus)}", "trigger.payload.previous_focus / customer.preferences",
                "customer:focus")


def _sel_delivery_saved(ctx: _Context) -> Line | None:
    if _payload(ctx.bundle).get("delivery_address_saved") is not True:
        return None
    return Line("delivery address saved", "trigger.payload.delivery_address_saved", "payload:delivery_address_saved")


def _sel_trial_done(ctx: _Context) -> Line | None:
    when = _shown(ctx.bundle, "trial_completed")
    if not when:
        return None
    return Line(f"trial completed on {when}", "trigger.payload.trial_completed", "payload:trial_completed",
                f"your trial with us was on {when}", f"aapka trial {when} ko hua tha")


SELECTORS: dict[str, Callable[[_Context], Line | None]] = {
    "digest_summary": _sel_digest_summary,
    "digest_actionable": _sel_digest_actionable,
    "cohort": _sel_cohort,
    "related_digest": _sel_related_digest,
    "active_offers": lambda ctx: _first_fact(ctx.bundle, "active_offers"),
    "match_offer": lambda ctx: _sel_match_offer(ctx),
    "history_said": lambda ctx: _sel_history_said(ctx),
    "last_visit": _sel_last_visit,
    "slump": lambda ctx: _sel_slump(ctx),
    "momentum": lambda ctx: _sel_momentum(ctx),
    "untried_offer": _sel_untried_offer,
    "members": lambda ctx: _first_fact(ctx.bundle, "total_active_members", "total_unique_ytd"),
    "churn": lambda ctx: _first_fact(ctx.bundle, "monthly_churn_pct_vs_peer", "monthly_churn_pct"),
    "chronic_rx": lambda ctx: _first_fact(ctx.bundle, "chronic_rx_count"),
    "delivery": lambda ctx: _first_fact(ctx.bundle, "delivery_orders_30d", "delivery_share_pct"),
    "peer_gap": lambda ctx: _peer_extreme(ctx.bundle, best=False),
    "peer_strength": lambda ctx: _peer_extreme(ctx.bundle, best=True),
    "peer_reviews": lambda ctx: _first_fact(ctx.bundle, "peer_avg_reviews"),
    "season": lambda ctx: _line(ctx.bundle, next(iter(ctx.bundle.facts_in("season")), None)),
    "local_trend": _sel_local_trend,
    "stale_posts": lambda ctx: _first_fact(ctx.bundle, "signal_stale_posts", "signal_no_recent_post"),
    "unverified": _sel_unverified,
    "views": lambda ctx: _sel_performance(ctx, "views"),
    "calls": lambda ctx: _sel_performance(ctx, "calls"),
    "positive_review": lambda ctx: _sel_review(ctx, "pos"),
    "slots": _sel_slots,
    "matching_offer": _sel_matching_offer,
    "first_offer": _sel_first_offer,
    "delivery_offer": lambda ctx: _sel_offer_containing(ctx, "delivery"),
    "senior_offer": _sel_senior_offer,
    "applicable_offers": _sel_applicable_offers,
    "preferred_slot": _sel_preferred_slot,
    "customer_focus": _sel_customer_focus,
    "customer_visits": _sel_customer_visits,
    "delivery_saved": _sel_delivery_saved,
    "trial_done": _sel_trial_done,
    "reach": _sel_reach,
    "event_season": _sel_event_season,
}
# Used when a recipe's own selectors find fewer than two facts (sparse or placeholder triggers).
# peer_gap only joins recipes that use loss aversion: a milestone shouldn't point at weak numbers.
_MERCHANT_ANCHORS = ("peer_gap", "peer_strength", "season", "local_trend", "untried_offer", "active_offers",
                     "members")
_CUSTOMER_ANCHORS = ("last_visit", "first_offer", "preferred_slot", "customer_visits")
# Customer kinds where "when did they last come in" is the reason for writing.
_RETURN_VISIT_KINDS = frozenset({"customer_lapsed_soft", "customer_lapsed_hard", "recall_due", "chronic_refill_due",
                                 "trial_followup"})
# Only these kinds take a seasonal note or category trend as filler; elsewhere it reads as a tangent
# (a competitor message drifting into IPL advice).
_SEASONAL_KINDS = frozenset({"festival_upcoming", "category_seasonal", "seasonal_perf_dip", "ipl_match_today",
                             "research_digest", "curious_ask_due"})


# =============================================================================
# LEADS (the "why now")
# =============================================================================


def _lead_research(ctx: _Context) -> Line | None:
    item = ctx.digest
    if not item:
        return None
    title, source = _pretty(item["title"]), _pretty(item.get("source"))
    bits = [f"{fmt_number(item['trial_n'])}-patient trial" if is_number(item.get("trial_n")) else "", source]
    detail = ", ".join(x for x in bits if x)
    return Line(title + (f" ({detail})" if detail else ""), f"category.digest[{item['id']}]",
                f"digest:{item['id']}", f"new in {source}: {title}" if source else f"new research: {title}")


def _lead_regulation(ctx: _Context) -> Line | None:
    item = ctx.digest
    if not item:
        return None
    title, source = _pretty(item["title"]), _pretty(item.get("source"))
    deadline = fmt_date(_payload(ctx.bundle).get("deadline_iso"))
    text = title + (f" (deadline {deadline})" if deadline and deadline not in title else "")
    return Line(text + (f"; source: {source}" if source else ""), f"category.digest[{item['id']}]",
                f"digest:{item['id']}", f"heads-up: {text}" + (f" ({source})" if source else ""))


def _lead_cde(ctx: _Context) -> Line | None:
    item = ctx.digest
    if not item:
        return None
    credits = _payload(ctx.bundle).get("credits", item.get("credits"))
    details = [fmt_datetime(item.get("date")) if item.get("date") else None,
               f"{fmt_number(credits)} CDE credits" if is_number(credits) else None,
               _shown(ctx.bundle, "fee")]
    details = [d for d in details if d]
    title = _pretty(item["title"])
    return Line(title + (f" ({'; '.join(details)})" if details else ""), f"category.digest[{item['id']}]",
                f"digest:{item['id']}", title + (f", {', '.join(details)}" if details else ""))


def _lead_supply(ctx: _Context) -> Line | None:
    payload, item = _payload(ctx.bundle), ctx.digest
    molecule = payload.get("molecule")
    batches = [x for x in payload.get("affected_batches") or [] if isinstance(x, str)]
    if not molecule and not item:
        return None
    what = humanize(molecule) + (f" batches {', '.join(batches)}" if batches else "") if molecule \
        else _pretty(item["title"])
    kind = "voluntary recall" if item and "voluntary" in str(item.get("title", "")).lower() else "recall"
    maker = f" from {payload['manufacturer']}" if payload.get("manufacturer") else ""
    source = _pretty(item.get("source")) if item else ""
    text = f"{kind}: {what}{maker}" + (f" ({source})" if source else "")
    return Line(text, "trigger.payload + category.digest", f"digest:{item['id']}" if item else "payload:molecule",
                f"urgent: {kind} on {what}{maker}" + (f", per {source}" if source else ""))


def _lead_category_seasonal(ctx: _Context) -> Line | None:
    trends = [t for t in ctx.bundle.payload_display.get("trends") or [] if isinstance(t, str)]
    season = _shown(ctx.bundle, "season")
    if not trends and not season:
        return None
    listed = ", ".join(trends)
    return Line((f"{season}: " if season else "") + listed, "trigger.payload.season, trends", "payload:trends",
                f"the {season} demand shift is here: {listed}" if season else f"demand is shifting: {listed}")


def _metric_move(ctx: _Context) -> tuple[str, float, str] | None:
    payload = _payload(ctx.bundle)
    if not is_number(payload.get("delta_pct")):
        return None
    return humanize(payload.get("metric") or "numbers"), payload["delta_pct"], _shown(ctx.bundle, "window") or "few days"


def _lead_perf(ctx: _Context) -> Line | None:
    move = _metric_move(ctx)
    if not move:
        return None
    metric, delta, window = move
    payload = _payload(ctx.bundle)
    text = f"{metric} {fmt_pct(delta, signed=True)} over the last {window}"
    phrase = f"your {metric} {_verb(metric)} {'up' if delta > 0 else 'down'} {fmt_pct(abs(delta))} over the last {window}"
    if is_number(payload.get("vs_baseline")):
        text += f" (usually around {fmt_number(payload['vs_baseline'])})"
        phrase += f" (usually around {fmt_number(payload['vs_baseline'])})"
    if payload.get("likely_driver"):
        text += f", likely driven by {humanize(payload['likely_driver'])}"
        phrase += f", likely thanks to your {humanize(payload['likely_driver'])}"
    return Line(text, "trigger.payload.metric, delta_pct, window", "payload:delta_pct", phrase)


def _lead_seasonal_dip(ctx: _Context) -> Line | None:
    move = _metric_move(ctx)
    if not move:
        return None
    metric, delta, window = move
    expected = _payload(ctx.bundle).get("is_expected_seasonal") is True
    note = _shown(ctx.bundle, "season_note")
    text = (f"{metric} {fmt_pct(delta, signed=True)} over the last {window}"
            + ("; flagged as the expected seasonal dip" if expected else "") + (f" ({note})" if note else ""))
    phrase = (f"your {metric} {_verb(metric)} {'down' if delta < 0 else 'up'} {fmt_pct(abs(delta))} over the last "
              f"{window}" + (", but that's the expected seasonal dip" if expected else ""))
    return Line(text, "trigger.payload.metric, delta_pct, is_expected_seasonal, season_note", "payload:delta_pct",
                phrase)


def _lead_milestone(ctx: _Context) -> Line | None:
    payload = _payload(ctx.bundle)
    now_value, goal = payload.get("value_now"), payload.get("milestone_value")
    if not (is_number(now_value) and is_number(goal)):
        return None
    label = "reviews" if payload.get("metric") == "review_count" else humanize(payload.get("metric"))
    if now_value >= goal:
        return Line(f"reached {fmt_number(goal)} {label}", "trigger.payload.value_now, milestone_value",
                    "payload:milestone", f"you've crossed {fmt_number(goal)} {label}")
    gap = fmt_number(goal - now_value)
    return Line(f"{fmt_number(now_value)} {label}, {gap} away from {fmt_number(goal)}",
                "trigger.payload.value_now, milestone_value", "payload:milestone",
                f"you're at {fmt_number(now_value)} {label}, just {gap} away from {fmt_number(goal)}")


def _lead_renewal(ctx: _Context) -> Line | None:
    b = ctx.bundle
    payload, sub = _payload(b), (b.merchant or {}).get("subscription", {})
    days, source = payload.get("days_remaining"), "trigger.payload.days_remaining, plan, renewal_amount"
    if not is_number(days):
        if str(sub.get("status")).lower() != "active" or not is_number(sub.get("days_remaining")):
            return None
        days, source = sub["days_remaining"], "merchant.subscription"
    plan = payload.get("plan") or sub.get("plan")
    plan_text = f"{plan} plan" if plan else "subscription"
    amount = f" ({fmt_inr(payload['renewal_amount'])})" if is_number(payload.get("renewal_amount")) else ""
    return Line(f"{plan_text} renews in {fmt_number(days)} days{amount}", source, "payload:days_remaining",
                f"your {plan_text} is up for renewal in {fmt_number(days)} days{amount}")


def _lead_winback(ctx: _Context) -> Line | None:
    b = ctx.bundle
    payload, sub = _payload(b), (b.merchant or {}).get("subscription", {})
    days = payload.get("days_since_expiry", sub.get("days_since_expiry"))
    if not is_number(days):
        return None
    dip, lapsed, noun = payload.get("perf_dip_pct"), payload.get("lapsed_customers_added_since_expiry"), \
        b.language.get("customer_noun", "customers")
    text = f"subscription lapsed {fmt_number(days)} days ago"
    phrase = f"it's been {fmt_number(days)} days since your subscription paused"
    if is_number(dip):
        text += f"; performance {fmt_pct(dip, signed=True)} since"
        phrase += f", and performance is {'down' if dip < 0 else 'up'} {fmt_pct(abs(dip))} since then"
    if is_number(lapsed):
        text += f"; {fmt_number(lapsed)} more {noun} lapsed since"
        phrase += f", with {fmt_number(lapsed)} more {noun} lapsing"
    return Line(text, "trigger.payload.days_since_expiry, perf_dip_pct, lapsed_customers_added_since_expiry",
                "payload:days_since_expiry", phrase)


def _lead_dormant(ctx: _Context) -> Line | None:
    """Re-open with something useful from the category; never with "you've gone quiet"."""
    item = _category_digest(ctx.bundle, kinds=("trend", "tech"))
    if not item:
        return None
    ctx.digest = item  # later selectors (e.g. the offer idea) can match it
    title, source = _pretty(item["title"]), _pretty(item.get("source"))
    return Line(f"{title} ({source})", f"category.digest[{item['id']}]", f"digest:{item['id']}",
                f"thought you'd want to see this: {title} ({source})")


def _lead_gbp(ctx: _Context) -> Line | None:
    payload = _payload(ctx.bundle)
    if payload.get("verified") is not False:
        return None
    path, uplift = _shown(ctx.bundle, "verification_path"), payload.get("estimated_uplift_pct")
    text = "Google profile not verified" + (f"; verification via {path}" if path else "") + \
        (f"; estimated uplift {fmt_pct(uplift, signed=True)}" if is_number(uplift) else "")
    phrase = "your Google profile still isn't verified"
    if path and is_number(uplift):
        phrase += f", and verifying it ({path}) comes with an estimated {fmt_pct(uplift)} uplift"
    return Line(text, "trigger.payload.verified, verification_path, estimated_uplift_pct", "payload:verified", phrase)


def _lead_festival(ctx: _Context) -> Line | None:
    payload = _payload(ctx.bundle)
    name = payload.get("festival")
    if not isinstance(name, str):
        return None
    date, days = _shown(ctx.bundle, "date"), payload.get("days_until")
    when = (f" on {date}" if date else "") + (f", {fmt_number(days)} days away" if is_number(days) else "")
    return Line(f"{name}{when}", "trigger.payload.festival, date, days_until", "payload:festival",
                f"{name} is coming up{when}")


def _lead_ipl(ctx: _Context) -> Line | None:
    payload = _payload(ctx.bundle)
    match = payload.get("match")
    if not isinstance(match, str):
        return None
    venue, when = payload.get("venue"), _shown(ctx.bundle, "match_time_iso")
    text = match + (f" at {venue}" if venue else "") + (f", {when}" if when else "") + \
        ("; not a weeknight match" if payload.get("is_weeknight") is False else "")
    phrase = f"{match} is on" + (f" at {venue}" if venue else "") + " today" + (f" ({when})" if when else "")
    return Line(text, "trigger.payload.match, venue, match_time_iso, is_weeknight", "payload:match", phrase)


_WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
_DAY_RANGE_RE = re.compile(r"\b(mon|tue|wed|thu|fri|sat|sun)[a-z]*\s*[-–/]\s*(mon|tue|wed|thu|fri|sat|sun)[a-z]*\b", re.I)


def offer_days(title: str) -> set[int] | None:
    """Weekdays (0 = Monday) an offer title limits itself to, e.g. '(Tue-Thu)'; None when it runs every day."""
    if m := _DAY_RANGE_RE.search(title):
        start, end = _WEEKDAYS.index(m.group(1).lower()), _WEEKDAYS.index(m.group(2).lower())
        return {d % 7 for d in range(start, end + 1 if end >= start else end + 8)}
    low = title.lower()
    if "weekday" in low:
        return {0, 1, 2, 3, 4}
    if "weekend" in low:
        return {5, 6}
    return None


def _match_day(ctx: _Context) -> datetime | None:
    when = parse_dt(_payload(ctx.bundle).get("match_time_iso"))
    return when.astimezone(IST) if when else None


def _sel_match_offer(ctx: _Context) -> Line | None:
    """The live offer, marked as not running today when its days exclude the match day."""
    line = _first_fact(ctx.bundle, "active_offers")
    fact, day = ctx.bundle.fact("active_offers"), _match_day(ctx)
    titles = [t for t in (fact.value if fact and isinstance(fact.value, list) else []) if isinstance(t, str)]
    if not line or not day or not titles or any(offer_days(t) is None or day.weekday() in offer_days(t)
                                                for t in titles):
        return line
    weekday, names = day.strftime("%A"), " and ".join(titles)
    return Line(f"{line.text} (doesn't run on {weekday}, the match day)", line.source, line.key,
                f"your {names} doesn't run on {weekday}, so there's no offer live tonight",
                f"aapka {names} {weekday} ko nahi chalta, toh aaj raat koi offer live nahi hai")


def _changes_7d(ctx: _Context) -> list[Fact]:
    """7-day changes, minus the metric the trigger itself already reports (no saying it twice)."""
    covered = _payload(ctx.bundle).get("metric")
    facts = [ctx.bundle.fact(f"{m}_change_7d") for m in ("calls", "views", "ctr") if m != covered]
    return [f for f in facts if f and is_number(f.value)]


def _week_line(ctx: _Context, fact: Fact | None) -> Line | None:
    """A 7-day change worded "this week", so it doesn't echo a lead that already says "over the last 7 days"."""
    line = _line(ctx.bundle, fact)
    if not line:
        return None
    return Line(line.text, line.source, line.key, line.phrase.replace("over the last 7 days", "this week"),
                line.phrase_hi)


def _sel_momentum(ctx: _Context) -> Line | None:
    """Their best positive 7-day change, the local signal a check-in or a jump can lean on."""
    rising = [f for f in _changes_7d(ctx) if f.value > 0]
    return _week_line(ctx, max(rising, key=lambda f: f.value)) if rising else None


def _sel_slump(ctx: _Context) -> Line | None:
    """Their worst 7-day drop, what a dip message should name."""
    falling = [f for f in _changes_7d(ctx) if f.value < 0]
    return _week_line(ctx, min(falling, key=lambda f: f.value)) if falling else None


def _sel_history_said(ctx: _Context) -> Line | None:
    """Vera's last message in the pushed chat history: an earlier suggestion or data point the plan can build on."""
    history = (ctx.bundle.merchant or {}).get("conversation_history") or []
    said = next((h.get("body") for h in reversed(history) if h.get("from") == "vera" and h.get("body")), None)
    if not isinstance(said, str):
        return None
    # the plain draft quotes its most concrete sentence (numbers, no question) so the fallback shows the plan too
    sentences = [x.strip(" —-") for x in re.split(r"(?<=[.!?])\s+|\s+—\s+", said) if x.strip()]
    concrete = max((x for x in sentences if "?" not in x and re.search(r"\d", x)),
                   key=lambda x: len(re.findall(r"\d+", x)), default="")
    phrase = re.sub(r"^(i )?suggest(ed)?\s+", "as suggested earlier: ", concrete.rstrip("."), flags=re.I)
    return Line(f'earlier in this chat Vera said (a suggestion, not something they have approved): "{said}"',
                "merchant.conversation_history", "history:vera_said", phrase)


def _weekend_match(ctx: _Context) -> bool:
    return ctx.bundle.trigger["kind"] == "ipl_match_today" and _payload(ctx.bundle).get("is_weeknight") is False


def _lead_competitor(ctx: _Context) -> Line | None:
    payload = _payload(ctx.bundle)
    name = payload.get("competitor_name")
    if not isinstance(name, str):
        return None
    distance, opened, offer = _shown(ctx.bundle, "distance_km"), _shown(ctx.bundle, "opened_date"), \
        payload.get("their_offer")
    where = (f" {distance} away" if distance else " nearby") + (f" on {opened}" if opened else "")
    return Line(f"{name} opened{where}" + (f", offering {offer}" if offer else ""),
                "trigger.payload.competitor_name, distance_km, opened_date, their_offer", "payload:competitor",
                f"{name} opened{where}" + (f" with {offer}" if offer else ""))


def _lead_planning(ctx: _Context) -> Line | None:
    b = ctx.bundle
    topic, said = _shown(b, "intent_topic"), _payload(b).get("merchant_last_message")
    if topic:
        return Line(f"merchant wants a plan for: {topic}" + (f' (their last message: "{said}")' if said else ""),
                    "trigger.payload.intent_topic, merchant_last_message", "payload:intent_topic",
                    f"here's a first cut of your {topic} plan")
    if b.history["open_requests"]:
        request = b.history["open_requests"][-1]
        return Line(f'merchant asked: "{request["message"]}"', "merchant.conversation_history",
                    "history:open_request", "picking up where we left off")
    return None


def _lead_curious(ctx: _Context) -> Line | None:
    ask = _shown(ctx.bundle, "ask_template")
    return Line("weekly check-in question" + (f": {ask}" if ask else ""),
                "trigger.payload.ask_template" if ask else "trigger.kind", "payload:ask_template",
                "quick question for this week")


def _lead_review(ctx: _Context) -> Line | None:
    payload = _payload(ctx.bundle)
    if not payload.get("theme"):
        return None
    label, count = review_theme_label(payload["theme"]), payload.get("occurrences_30d")
    counted = f"{fmt_number(count)} reviews in the last 30 days" if is_number(count) else "recent reviews"
    quote, trend = payload.get("common_quote"), payload.get("trend")
    text = f"{counted} mention {label}" + (f" ({trend})" if trend else "") + (f': "{quote}"' if quote else "")
    phrase = f"{counted} mention {label}" + (", and it's rising" if trend == "rising" else "") + \
        (f', like "{quote}"' if quote else "")
    return Line(text, "trigger.payload.theme, occurrences_30d, trend, common_quote", "payload:theme", phrase)


def _lead_recall(ctx: _Context) -> Line | None:
    service, due = _shown(ctx.bundle, "service_due"), _shown(ctx.bundle, "due_date")
    if not service:
        return None
    return Line(f"{service} due" + (f" by {due}" if due else ""), "trigger.payload.service_due, due_date",
                "payload:service_due", f"your {service} is due" + (f" by {due}" if due else ""),
                f"aapka {service} due hai" + (f" ({due} tak)" if due else ""))


def _lead_appointment(ctx: _Context) -> Line | None:
    english, hinglish = _GENERIC_CUSTOMER["appointment_tomorrow"]
    return Line("appointment tomorrow (the trigger gives no time)", "trigger.kind", "payload:kind", english, hinglish)


def _lead_refill(ctx: _Context) -> Line | None:
    medicines = [m for m in _payload(ctx.bundle).get("molecule_list") or [] if isinstance(m, str)]
    if not medicines:
        return None
    when = _shown(ctx.bundle, "stock_runs_out_iso")
    names, names_hi = _join_words(medicines), _join_words(medicines, "aur")
    return Line(f"refill due: {names}" + (f"; stock runs out {when}" if when else ""),
                "trigger.payload.molecule_list, stock_runs_out_iso", "payload:molecule_list",
                f"your {names} will run out" + (f" on {when}" if when else " soon"),
                f"aapki dawaiyan ({names_hi})" + (f" {when} ko" if when else " jald") + " khatam ho jayengi")


def _lead_lapsed(ctx: _Context) -> Line | None:
    b = ctx.bundle
    days = _payload(b).get("days_since_last_visit")
    if b.has("state_conflict") or not is_number(days):
        return None
    days_text = fmt_number(days)
    return Line(f"{days_text} days since last visit", "trigger.payload.days_since_last_visit",
                "payload:days_since_last_visit",
                f"it's been {days_text} days since your last visit, and we'd love to see you again",
                f"aapki last visit ko {days_text} din ho gaye, hum aapko phir se dekhna chahenge")


def _lead_trial(ctx: _Context) -> Line | None:
    b = ctx.bundle
    when = _shown(b, "trial_date")
    if not when:
        return None
    child = b.language.get("about")
    if child:
        return Line(f"{child}'s trial class on {when}", "trigger.payload.trial_date", "payload:trial_date",
                    f"thanks for bringing {child} to the trial class on {when}",
                    f"{child} ko {when} ki trial class mein laane ke liye shukriya")
    return Line(f"trial class on {when}", "trigger.payload.trial_date", "payload:trial_date",
                f"thanks for coming to the trial class on {when}",
                f"{when} ki trial class mein aane ke liye shukriya")


def _lead_wedding(ctx: _Context) -> Line | None:
    b = ctx.bundle
    date, days, step = _shown(b, "wedding_date"), _payload(b).get("days_to_wedding"), \
        _shown(b, "next_step_window_open")
    if not date:
        return None
    count = fmt_number(days) if is_number(days) else None
    text = f"wedding on {date}" + (f", {count} days away" if count else "") + (f"; next step: {step}" if step else "")
    phrase = (f"{count} days to go until your wedding on {date}" if count else f"your wedding on {date} is coming up") \
        + (f", so it's a good time to start the {step}" if step else "")
    phrase_hi = f"aapki wedding {date} ko hai" + (f", {count} din baaki hain" if count else "") + \
        (f", {step} shuru karne ka yeh sahi time hai" if step else "")
    return Line(text, "trigger.payload.wedding_date, days_to_wedding, next_step_window_open",
                "payload:wedding_date", phrase, phrase_hi)


def _lead_general(ctx: _Context) -> Line | None:
    """Unknown trigger kinds: state what the payload says, in plain words."""
    b = ctx.bundle
    pairs = [(k, v) for k, v in b.payload_display.items()
             if k != "placeholder" and not k.endswith("id") and isinstance(v, (str, int, float)) and v != ""]
    if not pairs:
        return None
    detail = "; ".join(f"{humanize(k)}: {v}" for k, v in pairs[:4])
    return Line(f"{humanize(b.trigger['kind'])}: {detail}", "trigger.payload", "payload:general",
                f"a quick update on {humanize(b.trigger['kind'])} ({detail})")


# =============================================================================
# RECIPES
# =============================================================================

_CUSTOMER_LEVERS = ("specificity", "effort_externalization", "single_binary_commitment")

RECIPES: dict[str, Recipe] = {
    # news
    "research_digest": Recipe(_lead_research, ("digest_summary", "cohort", "digest_actionable"),
                              "share the finding as a peer and tie it to their own patients or customers",
                              ("specificity", "curiosity", "reciprocity"), "research"),
    "regulation_change": Recipe(_lead_regulation, ("digest_summary", "digest_actionable"),
                                "flag the change early and make compliance feel easy",
                                ("specificity", "loss_aversion", "effort_externalization"), "regulation"),
    "cde_opportunity": Recipe(_lead_cde, ("digest_summary", "digest_actionable"),
                              "a useful, low-effort professional opportunity", ("specificity", "curiosity"), "cde",
                              render_support=1),
    "supply_alert": Recipe(_lead_supply, ("digest_summary", "chronic_rx", "digest_actionable"),
                           "urgent but calm: protect their customers and offer to do the legwork; the chronic-Rx "
                           "count is the list to check for these batches, not the number affected",
                           ("specificity", "loss_aversion", "effort_externalization"), "supply"),
    "category_seasonal": Recipe(_lead_category_seasonal, ("related_digest", "active_offers", "untried_offer"),
                                "get ahead of the seasonal shift", ("specificity", "loss_aversion"),
                                "seasonal_demand", related=("summer", "seasonal", "demand shift"),
                                related_field="actionable"),
    # performance
    "perf_dip": Recipe(_lead_perf, ("slump", "peer_gap", "stale_posts", "unverified", "untried_offer"),
                       "name the drop plainly, then offer a concrete fix",
                       ("specificity", "loss_aversion", "effort_externalization"), "perf_dip"),
    "perf_spike": Recipe(_lead_perf, ("momentum", "peer_strength", "active_offers", "members"),
                         "celebrate the jump and build on what caused it", ("specificity", "curiosity"),
                         "perf_spike"),
    "seasonal_perf_dip": Recipe(_lead_seasonal_dip, ("season", "peer_strength", "members", "churn"),
                                "reassure first (the dip is seasonal), then point to keeping current customers",
                                ("specificity", "loss_aversion", "effort_externalization"), "seasonal_dip"),
    "milestone_reached": Recipe(_lead_milestone, ("peer_reviews", "positive_review", "peer_strength"),
                                "celebrate and help them over the line",
                                ("specificity", "social_proof", "effort_externalization"), "milestone"),
    # account
    "renewal_due": Recipe(_lead_renewal, ("reach", "peer_strength"),
                          "show what the plan is delivering before it lapses",
                          ("specificity", "loss_aversion", "single_binary_commitment"), "renewal"),
    "winback_eligible": Recipe(_lead_winback, ("peer_gap", "members", "untried_offer"),
                               "show what they're missing since pausing, without guilt",
                               ("specificity", "loss_aversion"), "winback"),
    "dormant_with_vera": Recipe(_lead_dormant, ("peer_strength", "local_trend", "untried_offer"),
                                "re-open with something genuinely useful; never mention the silence",
                                ("reciprocity", "curiosity", "loss_aversion"), "dormant"),
    "gbp_unverified": Recipe(_lead_gbp, ("reach", "peer_strength"), "an easy fix with a clear upside",
                             ("specificity", "loss_aversion", "effort_externalization"), "gbp"),
    # outside events
    "festival_upcoming": Recipe(_lead_festival, ("event_season", "active_offers", "untried_offer"),
                                "plan early for the festival with a concrete offer",
                                ("specificity", "loss_aversion"), "festival",
                                related=("festive", "festival", "diwali")),
    "ipl_match_today": Recipe(_lead_ipl, ("season", "related_digest", "match_offer"),
                              "use the match timing, with data on how match days really perform",
                              ("specificity", "curiosity"), "ipl", related=("ipl",)),
    "competitor_opened": Recipe(_lead_competitor, ("active_offers", "peer_strength", "positive_review"),
                                "stay calm and competitive: lean on their strengths, not on price",
                                ("specificity", "loss_aversion", "social_proof"), "competitor",
                                related=("compet",)),
    # follow-ups
    "active_planning_intent": Recipe(_lead_planning, ("history_said", "active_offers", "delivery", "members"),
                                     "they already said yes: answer 'what would it look like' with a concrete, "
                                     "editable outline in the message itself. Build it on what Vera suggested earlier "
                                     "in the chat when there is one (it's a suggestion, not something they approved, "
                                     "so call prices 'proposed'), plus the listed facts; add structure, timings or "
                                     "ordering steps that fit the idea; use listed offers only if they fit. Never "
                                     "invent facts: no statistics, percentages, named customers, offices or "
                                     "buildings; end by offering the next deliverable; no qualifying questions",
                                     ("effort_externalization", "single_binary_commitment"), "planning"),
    "curious_ask_due": Recipe(_lead_curious, ("momentum", "active_offers"),
                              "ask one easy question anchored on their own momentum this week, and offer to turn the "
                              "answer into content while the interest is there",
                              ("asking_the_merchant", "reciprocity", "curiosity"), "curious", render_support=1),
    # reviews
    "review_theme_emerged": Recipe(_lead_review, ("positive_review", "related_digest", "delivery"),
                                   "flag the pattern early and offer to handle the reply",
                                   ("specificity", "loss_aversion", "effort_externalization"), "reviews",
                                   related=("complaint",)),
    # customer-facing
    "recall_due": Recipe(_lead_recall, ("slots", "matching_offer", "preferred_slot"),
                         "a friendly, useful reminder with an easy way to book", _CUSTOMER_LEVERS, "slots"),
    "appointment_tomorrow": Recipe(_lead_appointment, ("preferred_slot",), "a short, clear confirmation",
                                   ("single_binary_commitment",), "appointment"),
    "chronic_refill_due": Recipe(_lead_refill, ("delivery_saved", "applicable_offers"),
                                 "precise and respectful: make the refill effortless", _CUSTOMER_LEVERS, "refill"),
    "customer_lapsed_soft": Recipe(_lead_lapsed, ("customer_focus", "first_offer", "preferred_slot"),
                                   "warm, no pressure: give them an easy reason to come back",
                                   ("reciprocity", "single_binary_commitment"), "lapsed"),
    "customer_lapsed_hard": Recipe(_lead_lapsed, ("customer_focus", "first_offer", "preferred_slot"),
                                   "warm, no pressure: give them an easy reason to come back",
                                   ("reciprocity", "single_binary_commitment"), "lapsed"),
    "trial_followup": Recipe(_lead_trial, ("slots", "first_offer"), "build on the trial with an easy next step",
                             ("effort_externalization", "single_binary_commitment"), "slots"),
    "wedding_package_followup": Recipe(_lead_wedding, ("trial_done", "matching_offer", "preferred_slot"),
                                       "timely and personal: the next step before the wedding",
                                       ("specificity", "loss_aversion"), "wedding"),
}
# For kinds we've never seen, by family (unknown customer-scope kinds use "customer").
FAMILY_DEFAULTS: dict[str, Recipe] = {
    "news": RECIPES["research_digest"],
    "performance": RECIPES["perf_dip"],
    "account": Recipe(_lead_general, ("peer_gap", "views", "untried_offer"), "a clear, useful account update",
                      ("specificity", "loss_aversion"), "general"),
    "event": Recipe(_lead_general, ("season", "active_offers", "untried_offer"), "connect the event to their business",
                    ("specificity", "curiosity"), "general"),
    "followup": RECIPES["curious_ask_due"],
    "reviews": RECIPES["review_theme_emerged"],
    "customer": Recipe(_lead_general, ("first_offer", "preferred_slot"), "a short, relevant note from the shop",
                       ("single_binary_commitment",), "customer_general"),
    "general": Recipe(_lead_general, ("peer_gap", "peer_strength", "active_offers", "untried_offer"),
                      "a clear update tied to their own numbers", ("specificity",), "general"),
}


# Customer-facing kinds that only make sense for some categories. The generated data assigns
# kinds to random merchants (e.g. a dental clinic with a medicine-refill trigger).
_KIND_CATEGORIES = {"chronic_refill_due": {"pharmacies"}, "wedding_package_followup": {"salons"}}
_MISMATCH_RECIPE = Recipe(lambda ctx: Line(f"{humanize(ctx.bundle.trigger['kind'])} (doesn't fit this business)",
                                           "trigger.kind", "payload:kind", *_GENERIC_CUSTOMER["recall_due"]),
                          ("first_offer", "preferred_slot", "customer_visits"), "a short, relevant note from the shop",
                          ("single_binary_commitment",), "lapsed")


def family_of(kind: str, audience: str) -> str:
    return KIND_FAMILY.get(kind) or ("customer" if audience == "customer" else "general")


# =============================================================================
# ASSEMBLY
# =============================================================================


def _language(b: ContextBundle) -> tuple[dict, str]:
    """Language instruction plus the greeting to use."""
    lang = b.language
    greeting = lang.get("greeting") or "Hi"
    if b.audience == "customer":
        style = lang.get("style") or "en"
        other = style.split("-")[0]
        instructions = {"hi-en": "Hindi-English mix (Hinglish), in Roman script.",
                        "hi": "Simple Hindi in Roman script; everyday English words are fine.",
                        "en": "English."}
        instruction = instructions.get(style)
        if instruction is None:
            name = LANGUAGE_NAMES.get(other, other)
            instruction = f"{name}-English mix is their preference; clear English with a {name} greeting is fine."
            if other in LOCAL_GREETING and lang.get("address_as"):
                greeting = f"{LOCAL_GREETING[other]} {lang['address_as']}"
        return {"style": style, "instruction": instruction, "hinglish": style in ("hi-en", "hi")}, greeting
    code_mix = (b.category or {}).get("voice", {}).get("code_mix") or ""
    if "hi" not in lang.get("languages", []):
        return {"style": "en", "instruction": "English.", "hinglish": False}, greeting
    if code_mix == "english_primary_some_hindi":
        return {"style": "en", "instruction": "Mostly English; a little Hindi is fine.", "hinglish": False}, greeting
    return {"style": "hi-en", "instruction": "Natural Hindi-English mix (Hinglish) is welcome; plain English is fine too.",
            "hinglish": True}, greeting


def _consent_offer_framing(b: ContextBundle) -> bool:
    """Consent covers promotions only: turn reminder-style kinds into an offer from the shop."""
    consent = b.consent or {}
    return (b.audience == "customer" and b.has("consent_gap") and "promotional_offers" in consent.get("scopes", [])
            and b.trigger["kind"] != "appointment_tomorrow" and bool(_active_offer_titles(b)))


def _fallback_lead(ctx: _Context) -> Line:
    b, kind = ctx.bundle, ctx.bundle.trigger["kind"]
    if b.audience == "customer":
        english, hinglish = _NEUTRAL_CUSTOMER if b.has("state_conflict") else \
            _GENERIC_CUSTOMER.get(kind, _NEUTRAL_CUSTOMER)
        return Line(f"{humanize(kind)} (the trigger gives no details)", "trigger.kind", "payload:kind", english, hinglish)
    return Line(f"{humanize(kind)} (the trigger gives no details)", "trigger.kind", "payload:kind",
                _GENERIC_EVENT.get(kind, f"a quick update on {humanize(kind)}"))


# Selectors that read the trigger's own payload or news item; useless when the payload has no details.
_PAYLOAD_SELECTORS = frozenset({"digest_summary", "digest_actionable", "cohort", "match_offer", "event_season",
                                "delivery_saved", "trial_done"})


def _pick_support(ctx: _Context, lead: Line, limit: int = 3, *, payload_missing: bool = False) -> list[Line]:
    """The recipe's own facts first (minus payload-based ones when the payload is empty), then generic anchors.
    Keeping the kind's own choices is what keeps a detail-less competitor alert about their strengths."""
    b = ctx.bundle
    names = [n for n in ctx.recipe.support if not payload_missing or n not in _PAYLOAD_SELECTORS]
    anchors = _CUSTOMER_ANCHORS if b.audience == "customer" else tuple(
        a for a in _MERCHANT_ANCHORS if (a != "peer_gap" or "loss_aversion" in ctx.recipe.levers)
        and (a not in ("season", "local_trend") or b.trigger["kind"] in _SEASONAL_KINDS))
    picked: list[Line] = []
    seen = {lead.key, lead.text}
    for name in names + [a for a in anchors if a not in names]:
        if len(picked) >= limit or (name in anchors and name not in names and len(picked) >= 2):
            break
        line = SELECTORS[name](ctx)
        if line and line.key not in seen and line.text not in seen:
            picked.append(line)
            seen |= {line.key, line.text}
    return picked


def _ask(ctx: _Context, support: list[Line]) -> dict:
    b = ctx.bundle
    noun = b.language.get("customer_noun") or "customers"
    item = ASK_ITEM.get(_slug(b) or "", "service")
    if ctx.recipe.ask == "slots":
        labels = [s["safe_label"] for s in b.slots]
        if len(labels) >= 2:
            return {"cta": "multi_choice_slot",
                    "text": f"Reply 1 for {labels[0]} or 2 for {labels[1]}, or tell us a time that suits you.",
                    "text_hi": f"{labels[0]} ke liye 1 ya {labels[1]} ke liye 2 reply kijiye, ya apna time bataiye."}
        if labels:
            return {"cta": "binary_yes_no", "text": f"Reply YES to book {labels[0]}, or tell us a time that suits you.",
                    "text_hi": f"{labels[0]} book karne ke liye YES reply kijiye, ya apna time bataiye."}
        return {"cta": "binary_yes_no", "text": "Reply YES and we'll find you a slot.",
                "text_hi": "Slot ke liye YES reply kijiye."}
    if ctx.recipe.ask == "refill":
        saved = any(line.key == "payload:delivery_address_saved" for line in support)
        return {"cta": "binary_confirm_cancel",
                "text": "Reply CONFIRM and we'll " + ("deliver to your saved address." if saved else "get it ready."),
                "text_hi": "CONFIRM reply kijiye, hum " + ("saved address par deliver kar denge." if saved
                                                          else "ready kar denge.")}
    if ctx.recipe.ask == "lapsed" and _slug(b) == "pharmacies":
        return {"cta": "binary_yes_no", "text": "Reply YES and we'll get your next order ready for pickup or home delivery.",
                "text_hi": "YES reply kijiye, hum aapka agla order pickup ya home delivery ke liye ready kar denge."}
    if ctx.recipe.ask == "ipl" and _weekend_match(ctx):
        return {"cta": "binary_yes_no",
                "text": "Want me to draft a delivery-only match-night special, with a banner and an Insta story?",
                "text_hi": "Kya main aaj raat ke liye delivery-only match special, banner aur Insta story ke saath, "
                           "draft kar doon?"}
    cta, english, hinglish = ASKS[ctx.recipe.ask]
    return {"cta": cta, "text": english.format(noun=noun, item=item), "text_hi": hinglish.format(noun=noun, item=item)}


def _instructions(ctx: _Context, fallback_lead: bool, notes: list[str]) -> list[str]:
    b = ctx.bundle
    voice = (b.category or {}).get("voice", {})
    rules = []
    if b.audience == "customer":
        rules.append("Voice: warm, clear and respectful, like the shop's front desk writing to a regular customer.")
    elif voice.get("tone"):
        rules.append(f"Voice: {humanize(voice['tone'])}, {humanize(voice.get('register', ''))}.".replace(", .", "."))
    vocab = [v for v in voice.get("vocab_allowed", []) if isinstance(v, str)][:6]
    if vocab and b.audience == "merchant":
        rules.append(f"Category words you can use (vocabulary only, not facts about this business): "
                     f"{', '.join(vocab)}.")
    rules.append("One ask only, and make it the last sentence. No links. No preamble.")
    rules.append("Use only the facts listed here: no invented offers, prices, dates, names or statistics.")
    if b.audience == "customer":
        rules.append(f"Write as {(b.merchant or {}).get('identity', {}).get('name', 'the shop')}, not as Vera. "
                     "No medical or guaranteed-result claims.")
    else:
        rules.append("Don't re-introduce Vera; speak as a peer, not a salesperson.")
    if fallback_lead or b.has("placeholder_payload"):
        rules.append(f"The trigger ({humanize(b.trigger['kind'])}) gives no details: mention it only in general terms "
                     "and build the message on the supporting facts.")
    if b.has("consent_gap"):
        scopes = ", ".join(humanize(s) for s in (b.consent or {}).get("scopes", []))
        if _consent_offer_framing(b):
            rules.append(f"The customer only agreed to {scopes}: frame this as an offer from the shop, not a reminder.")
        else:
            rules.append(f"The customer only agreed to {scopes or 'nothing on file'}: keep it to a brief, "
                         "non-promotional note about their own booking.")
    if b.has("reminders_opted_out"):
        rules.append("The customer hasn't opted in to reminders: avoid reminder wording.")
    if b.has("state_conflict"):
        rules.append("The records disagree about when they last visited: don't mention how long they've been away.")
    if b.has("time_inconsistent"):
        rules.append("Some dates in the data are after today: don't say how long ago anything happened.")
    if b.has("slot_weekday_mismatch"):
        rules.append("Use the slot labels exactly as listed here (their original weekdays were wrong).")
    if b.has("merchant_not_active"):
        status = str((b.merchant or {}).get("subscription", {}).get("status", "inactive"))
        rules.append(f"Their subscription is {status}: don't promise platform features as if it were active.")
    if b.has("category_not_relevant"):
        rules.append("This event mainly targets other categories: connect it to this business only through the facts.")
    if b.has("sparse_merchant"):
        rules.append("There's little merchant-specific data: lean on the comparisons and category facts listed.")
    if any("doesn't fit" in note for note in notes):
        rules.append(f"This trigger type ({humanize(b.trigger['kind'])}) doesn't fit a {_slug(b)} business: "
                     "keep it to a general, friendly visit note.")
    last_topic = _shown(b, "last_topic")
    if b.trigger["kind"] == "dormant_with_vera" and last_topic:
        rules.append(f"Don't reopen the last topic ({last_topic}) or mention how long they've been quiet.")
    if _weekend_match(ctx):
        day = _match_day(ctx)
        rules.append("This is a weekend match, not a weeknight one: steer them away from dine-in promos and toward "
                     "delivery for tonight.")
        related = SELECTORS["related_digest"](ctx)  # the match-day data the brief will quote
        digest_text = " ".join([related.text if related else "",
                                *(str(d.get("summary", "")) + " " + str(d.get("title", "")) for d in b.digest_items)])
        if day and "saturday" in digest_text.lower() and day.strftime("%A") != "Saturday":
            rules.append(f"The order data is about Saturday matches and this match is on a {day.strftime('%A')}: "
                         "quote it as Saturday data (both are weekend matches), not as a figure for today.")
    if ctx.recipe.ask == "slots" and len(b.slots) >= 2:
        rules.append("Name the slot times only once, in the ask.")
    if any(d.get("fresh") for d in b.digest_items):
        rules.append("This news item arrived during the test window: you can call it new.")
    rules.extend(f"Note: {note}" for note in notes if note.startswith("digest item"))
    return rules


def _avoid(b: ContextBundle) -> list[str]:
    taboos = [re.sub(r"\s*\([^)]*\)", "", t).strip() for t in (b.category or {}).get("voice", {}).get("vocab_taboo", [])
              if isinstance(t, str)]
    return [t for t in taboos if t]


def build_fact_sheet(bundle: ContextBundle, *, state: RuntimeState | None = None) -> FactSheet:
    """The writing brief for one trigger. Deterministic: same bundle in, same sheet out."""
    b = bundle
    kind = b.trigger["kind"]
    family = family_of(kind, b.audience)
    recipe = RECIPES.get(kind) or FAMILY_DEFAULTS[family]
    notes: list[str] = []
    slug = _slug(b)
    if kind in _KIND_CATEGORIES and slug and slug not in _KIND_CATEGORIES[kind]:
        recipe = _MISMATCH_RECIPE
        notes.append(f"a {humanize(kind)} trigger doesn't fit a {slug} business, so it's a general visit note")

    digest = b.digest_items[0]["item"] if b.digest_items else None
    picked = False
    if digest is None and kind in _TOPIC_DIGEST_KINDS:
        digest = _category_digest(b, kinds=_TOPIC_DIGEST_KINDS[kind])
        picked = digest is not None
        if picked:
            notes.append(f"digest item {digest['id']} taken from the category's current digest "
                         "(the trigger named none)")
    ctx = _Context(bundle=b, recipe=recipe, digest=digest, digest_picked=picked)

    lead = None
    if _consent_offer_framing(b):
        offer = _sel_first_offer(ctx)
        if offer:
            lead = offer
            notes.append("consent covers promotional offers only, so the message is framed as an offer")
    lead = lead or recipe.lead(ctx)
    fallback = lead is None
    if fallback:
        lead = _fallback_lead(ctx)
        notes.append("the trigger has no usable details, so the message leans on merchant and category facts")
    support = _pick_support(ctx, lead, payload_missing=fallback)
    language, greeting = _language(b)
    ask = _ask(ctx, support)
    ask["intent"] = f"{CTA_LABELS.get(ask['cta'], ask['cta'])}: {ask['text']}"

    merchant_id = b.trigger.get("merchant_id") or (b.merchant or {}).get("merchant_id")
    customer_id = b.trigger.get("customer_id") if b.audience == "customer" else None
    recipient = customer_id if b.audience == "customer" else merchant_id
    sender = (b.merchant or {}).get("identity", {}).get("name")
    if b.audience == "customer":
        window_open = bool(state and customer_id and state.session_window_open(customer_id, b.now))
    else:
        window_open = bool(b.history.get("session_window_open"))

    numbers: set[str] = set()
    for line in [lead, *support]:
        for text in (line.text, line.phrase, line.phrase_hi):
            numbers |= number_tokens(text)
    for text in (ask["text"], ask["text_hi"], greeting, sender,
                 (b.merchant or {}).get("identity", {}).get("locality")):
        numbers |= number_tokens(text)

    return FactSheet(
        trigger_id=b.trigger_id,
        kind=kind,
        family=family,
        audience=b.audience,
        send_as=b.send_as,
        merchant_id=merchant_id,
        customer_id=customer_id,
        recipient_id=recipient,
        sender_name=sender,
        greeting=greeting,
        address_as=b.language.get("address_as"),
        language=language,
        lead=lead,
        support=support,
        angle=("a weekend match: the category's IPL guidance says match-night promos work Tue-Thu, not weekends, "
               "so skip dine-in promos tonight; propose running their existing offer as a delivery-only special for "
               "the match, as an exception for them to approve (it normally runs Tue-Thu)" if _weekend_match(ctx)
               else recipe.angle),
        levers=list(recipe.levers),
        ask=ask,
        template={"required": not window_open,
                  "name": f"{'vera' if b.audience == 'merchant' else 'merchant'}_{kind}_v1"},
        instructions=_instructions(ctx, fallback, notes),
        avoid=_avoid(b),
        allowed_numbers=sorted(numbers, key=lambda n: (float(n), n)),
        suppression_key=b.trigger["suppression_key"],
        urgency=b.trigger["urgency"],
        flags=list(b.flags),
        notes=notes,
        render_support=recipe.render_support,
        vocabulary=[v for v in ((b.category or {}).get("voice", {}).get("vocab_allowed") or []) if isinstance(v, str)],
    )
