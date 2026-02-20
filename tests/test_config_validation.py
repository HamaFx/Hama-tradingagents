import pytest

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.config_validation import (
    validate_selected_analysts,
    validate_tradingagents_config,
)


def test_validate_tradingagents_config_accepts_default_config():
    validate_tradingagents_config(DEFAULT_CONFIG.copy())


def test_validate_tradingagents_config_rejects_unsupported_provider():
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "invalid-provider"

    with pytest.raises(ValueError, match="Unsupported llm_provider"):
        validate_tradingagents_config(config)


def test_validate_tradingagents_config_rejects_invalid_round_limits():
    config = DEFAULT_CONFIG.copy()
    config["max_debate_rounds"] = 0

    with pytest.raises(ValueError, match="max_debate_rounds"):
        validate_tradingagents_config(config)


def test_validate_selected_analysts_rejects_duplicates():
    with pytest.raises(ValueError, match="must not contain duplicates"):
        validate_selected_analysts(["market", "market"])


def test_validate_selected_analysts_rejects_invalid_values():
    with pytest.raises(ValueError, match="Unsupported analyst type"):
        validate_selected_analysts(["market", "macro"])
