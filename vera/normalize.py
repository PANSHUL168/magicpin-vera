"""Pure helpers that clean up raw context values.

Nothing here touches the store. Every function is defensive: odd input gives back
None or a safe default instead of raising, because the judge can push shapes we
have never seen.
"""

from __future__ import annotations

import copy
import re
from datetime import datetime, timedelta, timezone
from typing import Any

IST = timezone(timedelta(hours=5, minutes=30))

# =============================================================================
# NUMBERS
# =============================================================================


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def fmt_indian_int(value: float) -> str:
    """2410 -> '2,410', 124000 -> '1,24,000' (Indian digit grouping)."""
    n = int(round(value))
    sign = "-" if n < 0 else ""
    digits = str(abs(n))
    if len(digits) <= 3:
        return sign + digits
    head, tail = digits[:-3], digits[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    groups.insert(0, head)
    return sign + ",".join(groups + [tail])


def fmt_inr(amount: Any) -> str:
    """4999 -> '₹4,999'. Non-numbers come back unchanged, as text."""
    if not is_number(amount):
        return str(amount)
    amount = round(amount, 2)
    if float(amount).is_integer():
        return "₹" + fmt_indian_int(amount)
    return "₹" + fmt_indian_int(int(amount)) + f"{abs(amount) % 1:.2f}"[1:]


def pct_decimals(*fractions: float) -> int:
    """Decimals needed to show these fractions as percents: 1 if any is a small non-whole percent."""
    return int(any(abs(f * 100) < 10 and round(f * 100, 1) != round(f * 100) for f in fractions))


def fmt_pct(fraction: float, *, signed: bool = False, decimals: int | None = None) -> str:
    """Fraction to percent text: 0.021 -> '2.1%', 0.38 -> '38%', -0.05 -> '-5%'.

    The dataset stores every *_pct / ctr / delta value as a fraction, so this is
    the one place that multiplies by 100.
    """
    pct = fraction * 100
    if decimals is None:
        decimals = pct_decimals(fraction)
    text = f"{pct:.{decimals}f}"
    if float(text) == 0:
        text = text.lstrip("-")
    elif signed and pct > 0:
        text = "+" + text
    return text + "%"


def fmt_number(value: Any) -> str:
    """Counts and plain numbers: 2410 -> '2,410', 1.3 -> '1.3'."""
    if not is_number(value):
        return str(value)
    if float(value).is_integer():
        return fmt_indian_int(value)
    return f"{value:g}"


# =============================================================================
# DATES
# =============================================================================


def parse_dt(value: Any) -> datetime | None:
    """ISO text -> aware datetime. Accepts 'Z', '+05:30' and date-only values.

    Date-only values are Indian local dates, so they become midnight IST.
    Naive date-times are taken as UTC.
    """
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=IST if len(text) == 10 else timezone.utc)
    return dt


def iso_z(dt: datetime | None = None) -> str:
    """Aware datetime -> '2026-04-26T10:00:00.123Z' (current time if omitted)."""
    dt = (dt or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def fmt_date(value: Any, *, year: bool = True, weekday: bool = False) -> str | None:
    """'2026-05-12' -> '12 May 2026' (IST calendar)."""
    dt = parse_dt(value)
    if dt is None:
        return None
    d = dt.astimezone(IST)
    text = f"{d.day} {d:%b}" + (f" {d.year}" if year else "")
    return f"{d:%a} {text}" if weekday else text


def fmt_datetime(value: Any) -> str | None:
    """'2026-04-26T19:30:00+05:30' -> 'Sun 26 Apr, 7:30pm' (IST, weekday from the date itself).

    Midnight means "that day" in this data (e.g. stock_runs_out_iso), so it prints as a date.
    """
    dt = parse_dt(value)
    if dt is None:
        return None
    d = dt.astimezone(IST)
    if d.hour == 0 and d.minute == 0:
        return f"{d:%a} {d.day} {d:%b}"
    hour = d.hour % 12 or 12
    minutes = f":{d.minute:02d}" if d.minute else ""
    return f"{d:%a} {d.day} {d:%b}, {hour}{minutes}{'am' if d.hour < 12 else 'pm'}"


_MONTH_NUM = {m: i for i, m in enumerate(
    ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"), start=1)}


def months_in_range(label: Any) -> set[int]:
    """Seasonal-beat labels to month numbers: 'Nov-Feb' -> {11, 12, 1, 2}, 'Feb 14' -> {2}."""
    names = [n[:3].lower() for n in re.findall(r"[A-Za-z]{3,}", str(label or ""))]
    months = [_MONTH_NUM[n] for n in names if n in _MONTH_NUM]
    if not months:
        return set()
    start, end = months[0], months[-1]
    out, month = set(), start
    while True:
        out.add(month)
        if month == end:
            return out
        month = month % 12 + 1


_WEEKDAY_PREFIX = re.compile(r"^(mon|tue|wed|thu|fri|sat|sun)[a-z]*\.?,?\s+", re.I)


def check_slot_label(slot: Any) -> dict | None:
    """Compare a slot's human label with its ISO time.

    The seed labels carry wrong weekdays (e.g. 'Wed 5 Nov' for 2026-11-05, a
    Thursday), so we return a safe label with the weekday dropped when they
    disagree. Returns None when the slot has no usable label/ISO pair.
    """
    if not isinstance(slot, dict):
        return None
    label, dt = slot.get("label"), parse_dt(slot.get("iso"))
    if not isinstance(label, str) or dt is None:
        return None
    actual = dt.astimezone(IST).strftime("%a")
    match = _WEEKDAY_PREFIX.match(label.strip())
    ok = match is None or match.group(1).lower() == actual.lower()
    safe = label.strip() if ok else label.strip()[match.end():]
    return {"label": label, "iso": slot.get("iso"), "actual_weekday": actual,
            "weekday_ok": ok, "safe_label": safe}


# =============================================================================
# TEXT
# =============================================================================

_ACRONYMS = {"gbp", "ctr", "ors", "ipl", "cde", "dci", "ida", "jida", "hiit", "bp", "pt",
             "yoy", "aov", "gst", "otc", "seo", "sms", "upi", "emi", "faq", "bogo", "t2"}
_SPECIAL_CASE = {"rx": "Rx"}
# "may" is left out on purpose: it is also an ordinary English word.
_MONTH_WORDS = {m: m.title() for m in
                ("jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec")}
_MONTH_ALT = "jan|feb|mar|apr|may|jun|jul|aug|sept|sep|oct|nov|dec"
_UNIT_WORD = {"day": "day", "days": "day", "week": "week", "weeks": "week", "month": "month",
              "months": "month", "mo": "month", "year": "year", "years": "year", "yr": "year",
              "yrs": "year", "min": "minute", "mins": "minute", "hour": "hour", "hours": "hour",
              "hr": "hour", "hrs": "hour"}
_UNIT_RE = re.compile(r"(\d+)_?(days?|weeks?|months?|mo|years?|yrs?|mins?|hours?|hrs?)(?=_|\s|$)")
_MONTH_RANGE_RE = re.compile(rf"(?<![a-z])({_MONTH_ALT})_({_MONTH_ALT})(?![a-z])")
_CODE_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)+$")
_SHORT_DURATION_RE = re.compile(r"^(\d+)\s*([dhw])$")


def humanize(token: Any) -> str:
    """Snake-case codes to plain words.

    '6_month_cleaning' -> '6-month cleaning', 'seasonal_dip_apr_may' -> 'seasonal dip Apr-May',
    'unverified_gbp' -> 'unverified GBP'. The judge penalises internal jargon, so nothing
    snake_case should reach a message without passing through here.
    """
    if token is None:
        return ""
    text = str(token).strip()
    short = _SHORT_DURATION_RE.fullmatch(text)
    if short:
        n = int(short.group(1))
        unit = {"d": "day", "h": "hour", "w": "week"}[short.group(2)]
        return f"{n} {unit}{'' if n == 1 else 's'}"
    text = _UNIT_RE.sub(lambda m: f"{m.group(1)}-{_UNIT_WORD[m.group(2)]}", text)
    text = _MONTH_RANGE_RE.sub(lambda m: f"{m.group(1).title()}-{m.group(2).title()}", text)
    words = []
    raw_words = text.replace("_", " ").split()
    # 'skin prep program 30-day' reads better as '30-day skin prep program'
    if len(raw_words) > 1 and re.fullmatch(r"\d+-(day|week|month|year|minute|hour)", raw_words[-1]):
        raw_words = raw_words[-1:] + raw_words[:-1]
    for word in raw_words:
        low = word.lower()
        if low in _SPECIAL_CASE:
            words.append(_SPECIAL_CASE[low])
        elif low in _ACRONYMS:
            words.append(low.upper())
        elif word == low and low in _MONTH_WORDS:
            words.append(_MONTH_WORDS[low])
        else:
            words.append(word)
    return " ".join(words)


def looks_like_code(text: Any) -> bool:
    """True for lowercase snake-case tokens such as 'weekday_evening'."""
    return isinstance(text, str) and bool(_CODE_RE.fullmatch(text))


def offer_key(title: Any) -> str:
    """Loose key for matching offer titles: drops brackets, punctuation and ₹ formatting.

    'Senior Citizen 15% OFF (60+ age)' and 'Senior Citizen 15% OFF' give the same key.
    """
    text = str(title or "").lower()
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("₹", " rs ").replace(",", "")
    text = re.sub(r"[^a-z0-9%]+", " ", text)
    return " ".join(text.split())


_NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")


def number_tokens(text: Any) -> set[str]:
    """Numbers in text, normalised so '1,499', '3.0' and '3' compare sensibly: {'1499', '3'}."""
    tokens = set()
    for raw in _NUMBER_RE.findall(str(text or "")):
        cleaned = raw.replace(",", "")
        try:
            value = float(cleaned)
        except ValueError:
            continue
        tokens.add(str(int(value)) if value.is_integer() else f"{value:g}")
    return tokens


def fingerprint(text: Any) -> str:
    """Normalised text for exact-repeat checks (auto-replies, repeated bodies)."""
    cleaned = re.sub(r"[^a-z0-9ऀ-ॿ]+", " ", str(text or "").lower())
    return " ".join(cleaned.split())


# =============================================================================
# SIGNALS AND TRENDS
# =============================================================================

# Two formats exist in the data: 'stale_posts:22d' and 'dormant_with_vera_14d'.
_SIGNAL_RE = re.compile(r"^(?P<name>[a-z][a-z0-9_]*?)[:_](?P<value>\d+(?:\.\d+)?)(?P<unit>[a-z%]*)$")

SIGNAL_TEMPLATES = {
    "stale_posts": "last Google post was {value} days ago",
    "renewal_due_soon": "subscription renewal due in {value} days",
    "dormant_with_vera": "no message to Vera in {value} days",
    "engaged_in_last": "engaged with Vera in the last {value} hours",
    "ctr_below_peer_median": "CTR below the peer benchmark",
    "above_peer_ctr": "CTR above the peer benchmark",
    "above_peer_median_calls": "calls above the peer benchmark",
    "above_peer_calls": "calls above the peer benchmark",
    "unverified_gbp": "Google Business Profile not verified",
    "no_active_offers": "no active offers",
    "no_recent_post": "no recent Google post",
    "no_recent_conversation": "no recent conversation with Vera",
    "perf_dip_severe": "severe drop in performance",
    "perf_dip_post_expiry": "performance dropped after the subscription expired",
    "winback_eligible": "eligible for a win-back offer",
    "high_risk_adult_cohort": "sizeable high-risk adult patient group",
    "trial_ending_soon": "trial ending soon",
    "new_merchant": "new on magicpin",
    "delivery_not_set_up": "delivery not set up",
    "growing_views_7d": "views growing over the last 7 days",
    "seasonal_dip_apr_may": "seasonal dip expected in Apr-May",
}
_SIGNAL_UNITS = {"d": "days", "h": "hours", "w": "weeks", "pct": "%", "%": "%"}


def parse_signal(raw: Any) -> dict:
    """'stale_posts:22d' -> {'name': 'stale_posts', 'value': 22, 'unit': 'd', ...}."""
    text = str(raw or "").strip()
    match = _SIGNAL_RE.match(text)
    if match:
        value = float(match.group("value"))
        return {"raw": text, "name": match.group("name"),
                "value": int(value) if value.is_integer() else value,
                "unit": match.group("unit") or None}
    return {"raw": text, "name": text, "value": None, "unit": None}


def signal_display(signal: dict) -> str:
    template = SIGNAL_TEMPLATES.get(signal["name"])
    value = signal.get("value")
    if template and ("{value}" not in template or value is not None):
        return template.format(value=fmt_number(value)) if value is not None else template
    text = humanize(signal["name"])
    if value is not None:
        text += f" ({fmt_number(value)} {_SIGNAL_UNITS.get(signal.get('unit'), signal.get('unit') or '')})".rstrip()
    return text


_TREND_RE = re.compile(r"^(?P<label>.+?)_(?P<delta>[+-]\d+(?:\.\d+)?)$")


def parse_trend(text: Any) -> dict | None:
    """'ORS_demand_+40' -> {'label': 'ORS demand', 'delta': 0.4, 'display': 'ORS demand +40%'}.

    Unlike the numeric *_pct fields, these strings carry whole-number percents.
    """
    match = _TREND_RE.match(text.strip()) if isinstance(text, str) else None
    if not match:
        return None
    delta = float(match.group("delta")) / 100
    label = humanize(match.group("label"))
    return {"raw": text, "label": label, "delta": delta,
            "display": f"{label} {fmt_pct(delta, signed=True)}"}


# =============================================================================
# LANGUAGE AND NAMES
# =============================================================================

LANGUAGE_NAMES = {"en": "English", "hi": "Hindi", "mr": "Marathi", "ta": "Tamil", "te": "Telugu",
                  "kn": "Kannada", "bn": "Bengali", "gu": "Gujarati", "ml": "Malayalam",
                  "pa": "Punjabi", "or": "Odia", "ur": "Urdu"}
_LANGUAGE_CODES = {**{code: code for code in LANGUAGE_NAMES},
                   **{name.lower(): code for code, name in LANGUAGE_NAMES.items()},
                   "eng": "en", "hin": "hi", "hinglish": "hi"}


def language_code(value: Any) -> str | None:
    """'english' / 'EN' / 'Hindi' -> 'en' / 'en' / 'hi'."""
    return _LANGUAGE_CODES.get(value.strip().lower()) if isinstance(value, str) else None


def parse_language_pref(pref: Any) -> dict:
    """'hi-en mix' -> {'codes': ['hi', 'en'], 'mix': True}; 'english' -> {'codes': ['en'], 'mix': False}."""
    text = pref.strip().lower() if isinstance(pref, str) else ""
    codes: list[str] = []
    for token in re.split(r"[^a-z]+", text):
        code = language_code(token)
        if code and code not in codes:
            codes.append(code)
    mix = "mix" in text or "hinglish" in text or len(codes) > 1
    if mix and "en" not in codes:
        codes.append("en")
    return {"raw": pref, "codes": codes, "mix": mix}


_DEVANAGARI = re.compile(r"[ऀ-ॿ]")
_HINDI_WORDS = frozenset("""
    hai hain tha thi kya kyu kyun kaise kab kahan nahi nahin aap aapka aapki aapke tum mujhe
    mera meri mere hum hamara hamari humara karo karna kariye kijiye dijiye lijiye chahiye raha
    rahi rahe hoon ji bhai accha acha theek thik haan bilkul abhi sab bahut shukriya dhanyavad
    namaste batao bataiye wala wali liye yeh woh kuch koi gaya gayi diya karenge sakte sakta
    sakti chalega samajh baat kar karu karun karoon kitna kitne kitni lagega lagegi lagta hoga
    hogi hota hoti mein ko se ka ki ke toh bhi aur wapas arre arey wah achha aage bolo boliye
    dekho dekhiye jaldi zaroor kal aaj milega milegi chahta chahti bhejo bhejiye lekin matlab
    pehle baad yahan wahan sirf zyada thoda thodi pata kaam paise rupaye dukaan grahak roz sahi
""".split())


def detect_language(text: Any) -> str:
    """Rough per-message guess: 'hi' (Devanagari), 'hi-en' (Romanised Hindi mixed in), 'en'."""
    if not isinstance(text, str) or not text.strip():
        return "unknown"
    if _DEVANAGARI.search(text):
        return "hi"
    words = re.findall(r"[a-z]+", text.lower())
    if not words:
        return "unknown"
    hits = sum(1 for word in words if word in _HINDI_WORDS)
    return "hi-en" if hits >= 2 or (hits == 1 and len(words) <= 3) else "en"


_HONORIFICS = {"dr": "Dr.", "mr": "Mr.", "mrs": "Mrs.", "ms": "Ms.", "miss": "Miss",
               "smt": "Smt.", "shri": "Shri", "sri": "Sri", "prof": "Prof."}
_HONORIFIC_RE = re.compile(r"^(dr|mrs|mr|ms|miss|smt|shri|sri|prof)\b\.?\s*", re.I)


def split_honorific(name: Any) -> tuple[str | None, str]:
    """'Dr. Asha' -> ('Dr.', 'Asha'); 'Meera' -> (None, 'Meera').

    Generated dentists store 'Dr. Asha' as the first name while seeds store 'Meera';
    stripping here keeps 'Dr. {first_name}' from turning into 'Dr. Dr. Asha'.
    """
    text = name.strip() if isinstance(name, str) else ""
    match = _HONORIFIC_RE.match(text)
    if not match or not text[match.end():].strip():
        return None, text
    return _HONORIFICS[match.group(1).lower()], text[match.end():].strip()


_GUARDIAN_RE = re.compile(
    r"^(?P<child>[^()]+?)\s*\(\s*(?P<relation>parent|guardian|mother|father)\s*:\s*(?P<adult>[^)]+?)\s*\)\s*$",
    re.I)
_ANONYMOUS_HINTS = ("walk-in", "no profile", "anonymous")


def parse_person_name(raw: Any) -> dict:
    """Customer names as stored: 'Aanya (parent: Sneha)' means message Sneha about Aanya.

    Returns subject (who the visit is for), addressee (who reads the message),
    relation, honorific and bare_name; anonymous=True for '(walk-in, no profile)'.
    """
    text = raw.strip() if isinstance(raw, str) else ""
    if not text or text.startswith("(") or any(h in text.lower() for h in _ANONYMOUS_HINTS):
        return {"raw": raw, "anonymous": True, "subject": None, "addressee": None,
                "relation": None, "honorific": None, "bare_name": None}
    match = _GUARDIAN_RE.match(text)
    if match:
        adult = match.group("adult").strip()
        return {"raw": raw, "anonymous": False, "subject": match.group("child").strip(),
                "addressee": adult, "relation": match.group("relation").lower(),
                "honorific": None, "bare_name": adult}
    honorific, bare = split_honorific(text)
    return {"raw": raw, "anonymous": False, "subject": text, "addressee": text,
            "relation": None, "honorific": honorific, "bare_name": bare}


# =============================================================================
# PAYLOAD DISPLAY
# =============================================================================

_MONEY_KEYS = {"renewal_amount", "amount", "price", "fee", "lifetime_value"}
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T")


def _is_id_key(key: str | None) -> bool:
    return bool(key) and (key == "id" or key.endswith("_id") or key.endswith("_ids"))


def display_value(key: str | None, value: Any) -> Any:
    """One payload value as a merchant could read it (ids are left untouched)."""
    if isinstance(value, dict):
        if "iso" in value and "label" in value:
            checked = check_slot_label(value)
            if checked:
                return checked["safe_label"]
        return {k: display_value(k, v) for k, v in value.items()}
    if isinstance(value, list):
        return [display_value(key, v) for v in value]
    if _is_id_key(key):
        return value
    if is_number(value):
        if key and key.endswith("_pct"):
            signed = any(word in key for word in ("delta", "dip", "uplift", "change", "growth"))
            return fmt_pct(value, signed=signed)
        if key in _MONEY_KEYS:
            return fmt_inr(value)
        if key == "distance_km":
            return f"{fmt_number(value)} km"
        return fmt_number(value)
    if isinstance(value, str):
        trend = parse_trend(value)
        if trend:
            return trend["display"]
        if _DATETIME_RE.match(value) and parse_dt(value):
            return fmt_datetime(value)
        if _DATE_RE.match(value) and parse_dt(value):
            return fmt_date(value)
        if looks_like_code(value) or _SHORT_DURATION_RE.fullmatch(value):
            return humanize(value)
    return value


def humanize_payload(payload: Any) -> dict:
    """Trigger payload with codes, fractions, money and dates made readable."""
    return display_value(None, payload) if isinstance(payload, dict) else {}


# =============================================================================
# CANONICAL SHAPES PER SCOPE
# =============================================================================

DECLARED_ID_FIELD = {"category": "slug", "merchant": "merchant_id", "customer": "customer_id", "trigger": "id"}


def _fix(container: dict, key: str, kind: type, warnings: list[str], where: str) -> Any:
    """Force container[key] to a dict or list, noting anything we had to coerce."""
    value = container.get(key)
    if isinstance(value, kind):
        return value
    if value is not None:
        warnings.append(f"{where}.{key}: expected {kind.__name__}, got {type(value).__name__}")
    fixed: Any = {} if kind is dict else ([] if value is None else [value])
    container[key] = fixed
    return fixed


def _alias(container: dict, alias: str, canonical: str, warnings: list[str], where: str) -> None:
    """Accept the field names the briefs use when the data uses different ones."""
    if canonical not in container and alias in container:
        container[canonical] = container[alias]
        warnings.append(f"{where}.{alias} read as {where}.{canonical}")


def _turn_sort_key(turn: dict) -> datetime:
    return parse_dt(turn.get("ts")) or datetime.min.replace(tzinfo=timezone.utc)


def _category(p: dict, context_id: str, w: list[str]) -> None:
    p.setdefault("slug", context_id)
    p.setdefault("display_name", humanize(p["slug"]).title())
    voice = _fix(p, "voice", dict, w, "category")
    _alias(voice, "taboos", "vocab_taboo", w, "voice")
    for key in ("vocab_allowed", "vocab_taboo", "salutation_examples", "tone_examples"):
        _fix(voice, key, list, w, "voice")
    peer = _fix(p, "peer_stats", dict, w, "category")
    _alias(peer, "avg_reviews", "avg_review_count", w, "peer_stats")
    for key in ("offer_catalog", "digest", "patient_content_library", "seasonal_beats",
                "trend_signals", "regulatory_authorities", "professional_journals"):
        _fix(p, key, list, w, "category")
    for i, item in enumerate(p["digest"]):
        if isinstance(item, dict) and not item.get("id"):
            item["id"] = f"{p['slug']}_digest_{i + 1}"
            w.append(f"digest[{i}] had no id; assigned {item['id']}")


def _merchant(p: dict, context_id: str, w: list[str]) -> None:
    p.setdefault("merchant_id", context_id)
    _alias(p, "category", "category_slug", w, "merchant")
    identity = _fix(p, "identity", dict, w, "merchant")
    identity["languages"] = [x for x in _fix(identity, "languages", list, w, "identity") if isinstance(x, str)]
    _fix(p, "subscription", dict, w, "merchant")
    performance = _fix(p, "performance", dict, w, "merchant")
    _fix(performance, "delta_7d", dict, w, "performance")
    _fix(p, "customer_aggregate", dict, w, "merchant")
    for key in ("offers", "conversation_history", "signals", "review_themes"):
        _fix(p, key, list, w, "merchant")
    p["offers"] = [o for o in p["offers"] if isinstance(o, dict)]
    p["signals"] = [s for s in p["signals"] if isinstance(s, str)]
    p["review_themes"] = [r for r in p["review_themes"] if isinstance(r, dict)]
    p["conversation_history"] = sorted(
        (h for h in p["conversation_history"] if isinstance(h, dict)), key=_turn_sort_key)


def _customer(p: dict, context_id: str, w: list[str]) -> None:
    p.setdefault("customer_id", context_id)
    for key in ("identity", "relationship", "preferences", "consent"):
        _fix(p, key, dict, w, "customer")
    _fix(p["relationship"], "services_received", list, w, "relationship")
    _fix(p["consent"], "scope", list, w, "consent")
    p.setdefault("state", "unknown")


def _trigger(p: dict, context_id: str, w: list[str]) -> None:
    p.setdefault("id", context_id)
    payload = _fix(p, "payload", dict, w, "trigger")
    # challenge-brief §6 says triggers reference merchants via payload.merchant_id;
    # the dataset puts ids at the top level. Accept either.
    for key in ("merchant_id", "customer_id"):
        if not p.get(key) and payload.get(key):
            p[key] = payload[key]
            w.append(f"trigger.payload.{key} used as trigger.{key}")
        p.setdefault(key, None)
    if p.get("scope") not in ("merchant", "customer"):
        p["scope"] = "customer" if p.get("customer_id") else "merchant"
    p.setdefault("kind", "unknown")
    p.setdefault("source", "internal")
    try:
        p["urgency"] = min(5, max(1, int(p.get("urgency", 1))))
    except (TypeError, ValueError):
        w.append(f"trigger.urgency {p.get('urgency')!r} is not a number; using 1")
        p["urgency"] = 1
    if not p.get("suppression_key"):
        p["suppression_key"] = f"{p['kind']}:{p.get('merchant_id') or '-'}:{p['id']}"
    p.setdefault("expires_at", None)


_CANONICALIZERS = {"category": _category, "merchant": _merchant, "customer": _customer, "trigger": _trigger}


def canonicalize(scope: str, payload: dict, context_id: str) -> tuple[dict, list[str]]:
    """Deep-copied payload in the canonical shape downstream code relies on, plus warnings.

    Unknown fields are kept; missing containers become empty dicts/lists so readers
    never have to guard against KeyError or wrong types.
    """
    data = copy.deepcopy(payload)
    warnings: list[str] = []
    _CANONICALIZERS[scope](data, context_id, warnings)
    declared = data.get(DECLARED_ID_FIELD[scope])
    if declared != context_id:
        warnings.append(f"{scope} payload id {declared!r} differs from context_id {context_id!r}")
    return data, warnings
