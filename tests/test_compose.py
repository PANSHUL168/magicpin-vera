import json
import subprocess
import sys
from pathlib import Path

import bot
from vera.compose import CONTRACT_KEYS, compose

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_compose_matches_the_brief_contract(expanded_dir):
    trigger = read(expanded_dir / "triggers" / "trg_003_recall_due_priya.json")
    merchant = read(expanded_dir / "merchants" / "m_001_drmeera_dentist_delhi.json")
    category = read(expanded_dir / "categories" / "dentists.json")
    customer = read(expanded_dir / "customers" / "c_001_priya_for_m001.json")
    result = compose(category, merchant, trigger, customer)
    assert tuple(result) == CONTRACT_KEYS
    assert result["send_as"] == "merchant_on_behalf" and result["body"].startswith("Hi Priya")
    assert compose(category, merchant, trigger, customer) == result  # deterministic


def test_compose_without_customer_for_merchant_triggers(expanded_dir):
    trigger = read(expanded_dir / "triggers" / "trg_001_research_digest_dentists.json")
    merchant = read(expanded_dir / "merchants" / "m_001_drmeera_dentist_delhi.json")
    category = read(expanded_dir / "categories" / "dentists.json")
    result = compose(category, merchant, trigger, None)
    assert result["send_as"] == "vera" and result["body"].startswith("Dr. Meera,")


def test_bot_exposes_compose():
    assert bot.compose is compose


def test_write_submission_produces_30_lines(expanded_dir, tmp_path):
    out = tmp_path / "submission.jsonl"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "write_submission.py"), "--dataset", str(expanded_dir),
                    "--out", str(out)], check=True, capture_output=True)
    lines = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert [line["test_id"] for line in lines] == [f"T{i:02d}" for i in range(1, 31)]
    assert all(set(line) == {"test_id", *CONTRACT_KEYS} and line["body"] for line in lines)
