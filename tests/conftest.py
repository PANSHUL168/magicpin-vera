import subprocess
import sys
from pathlib import Path

import pytest

from vera.loader import load_dataset
from vera.store import ContextStore

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def brief_now() -> str:
    """The simulated 'now' the briefs' examples use (the local simulator sends wall-clock time)."""
    return "2026-04-26T10:30:00Z"


@pytest.fixture(scope="session")
def expanded_dir(tmp_path_factory) -> Path:
    """The deterministic 50/200/100 dataset, generated fresh for the test session."""
    out = tmp_path_factory.mktemp("expanded")
    subprocess.run([sys.executable, str(ROOT / "dataset" / "generate_dataset.py"),
                    "--seed-dir", str(ROOT / "dataset"), "--out", str(out)],
                   check=True, capture_output=True)
    return out


@pytest.fixture(scope="session")
def loaded_store(expanded_dir) -> ContextStore:
    """Shared by the whole session: read from it, never ingest into it."""
    store = ContextStore()
    report = load_dataset(store, expanded_dir)
    assert not report["rejected"]
    return store


@pytest.fixture(autouse=True)
def _no_reference_override(monkeypatch):
    monkeypatch.delenv("VERA_REFERENCE_NOW", raising=False)


@pytest.fixture(autouse=True)
def _offline_llm(monkeypatch, tmp_path):
    """Tests never call the real API: the AI writer is off unless a test installs a fake."""
    from vera import writer
    monkeypatch.setenv("VERA_LLM", "off")
    monkeypatch.setenv("VERA_AI_CACHE_FILE", str(tmp_path / "ai_messages.json"))
    writer.CACHE.clear()
    yield
    writer.CACHE.clear()
