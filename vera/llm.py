"""Thin wrapper around the OpenAI Responses API (phase 3's only network dependency).

Settings (environment or .env):
    OPENAI_API_KEY    required for any call
    VERA_LLM          "off" disables every call; the bot then uses the plain writer (tests run this way)
    VERA_LLM_MODEL    default gpt-5.6-luna
    VERA_LLM_EFFORT   reasoning effort, default "low" (hidden reasoning tokens are billed as output)
    VERA_LLM_TIMEOUT  seconds per call, default 8 (the live tick budget); scripts raise it
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from collections import Counter
from dataclasses import dataclass

from .config import load_env

load_env()
log = logging.getLogger("vera.llm")

DEFAULT_MODEL = "gpt-5.6-luna"
USAGE: Counter[str] = Counter()     # calls and tokens this process has spent, for reporting
_lock = threading.Lock()
_client = None


class LLMError(Exception):
    """Any failure: disabled, timeout, API error, incomplete or unreadable output."""


@dataclass
class LLMResult:
    data: dict
    model: str
    input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    seconds: float


def enabled() -> bool:
    return os.getenv("VERA_LLM", "on").lower() != "off" and bool(os.getenv("OPENAI_API_KEY"))


def model_name() -> str:
    return os.getenv("VERA_LLM_MODEL", DEFAULT_MODEL)


def _get_client():
    global _client
    with _lock:
        if _client is None:
            from openai import OpenAI
            _client = OpenAI(timeout=float(os.getenv("VERA_LLM_TIMEOUT", "8")), max_retries=1)
        return _client


def complete_json(instructions: str, prompt: str, schema: dict, *, name: str,
                  max_output_tokens: int = 1200) -> LLMResult:
    """One Responses API call constrained to a JSON schema. Raises LLMError on any failure."""
    if not enabled():
        raise LLMError("LLM disabled (VERA_LLM=off or no OPENAI_API_KEY)")
    import openai

    started = time.perf_counter()
    try:
        response = _get_client().responses.create(
            model=model_name(),
            instructions=instructions,
            input=prompt,
            reasoning={"effort": os.getenv("VERA_LLM_EFFORT", "low")},
            text={"format": {"type": "json_schema", "name": name, "schema": schema, "strict": True},
                  "verbosity": "low"},
            max_output_tokens=max_output_tokens,
            store=False,  # don't keep merchant data on OpenAI's side (testing brief §11)
        )
    except openai.OpenAIError as exc:
        raise LLMError(f"{type(exc).__name__}: {exc}") from exc

    usage = response.usage
    details = getattr(usage, "output_tokens_details", None)
    result = LLMResult(data={}, model=response.model, input_tokens=getattr(usage, "input_tokens", 0) or 0,
                       output_tokens=getattr(usage, "output_tokens", 0) or 0,
                       reasoning_tokens=getattr(details, "reasoning_tokens", 0) or 0,
                       seconds=time.perf_counter() - started)
    with _lock:
        USAGE.update(calls=1, input_tokens=result.input_tokens, output_tokens=result.output_tokens,
                     reasoning_tokens=result.reasoning_tokens)
    log.info("llm %s: %d in / %d out (%d reasoning) tokens, %.1fs", result.model, result.input_tokens,
             result.output_tokens, result.reasoning_tokens, result.seconds)

    if response.status != "completed":
        reason = getattr(getattr(response, "incomplete_details", None), "reason", None)
        raise LLMError(f"response {response.status}" + (f" ({reason})" if reason else ""))
    try:
        result.data = json.loads(response.output_text)
    except (TypeError, ValueError) as exc:
        raise LLMError(f"unreadable output: {exc}") from exc
    if not isinstance(result.data, dict):
        raise LLMError("output is not a JSON object")
    return result
