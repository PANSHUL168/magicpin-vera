from pathlib import Path

import pytest

from vera import harness

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("scenario", harness.SCENARIOS, ids=lambda s: s.name)
def test_scenario(scenario):
    result = harness.run_scenario(scenario, ROOT / "dataset")
    assert not result["problems"], result["problems"]
    assert result["passed"] == result["total"]
