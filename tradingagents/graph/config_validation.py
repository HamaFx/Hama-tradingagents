from typing import Any, Dict


SUPPORTED_LLM_PROVIDERS = {
    "openai",
    "anthropic",
    "google",
    "xai",
    "openrouter",
    "ollama",
}

SUPPORTED_ANALYSTS = {"market", "social", "news", "fundamentals"}


def validate_tradingagents_config(config: Dict[str, Any]) -> None:
    """Validate TradingAgents configuration and raise helpful errors early."""
    required_keys = {
        "project_dir",
        "results_dir",
        "llm_provider",
        "deep_think_llm",
        "quick_think_llm",
        "max_debate_rounds",
        "max_risk_discuss_rounds",
        "max_recur_limit",
    }

    missing = sorted(key for key in required_keys if key not in config)
    if missing:
        raise ValueError(f"Missing required config key(s): {', '.join(missing)}")

    provider = str(config["llm_provider"]).lower()
    if provider not in SUPPORTED_LLM_PROVIDERS:
        supported = ", ".join(sorted(SUPPORTED_LLM_PROVIDERS))
        raise ValueError(f"Unsupported llm_provider '{provider}'. Supported: {supported}")

    _validate_positive_int(config, "max_debate_rounds")
    _validate_positive_int(config, "max_risk_discuss_rounds")
    _validate_positive_int(config, "max_recur_limit")

    if not str(config["deep_think_llm"]).strip():
        raise ValueError("'deep_think_llm' must be a non-empty string")

    if not str(config["quick_think_llm"]).strip():
        raise ValueError("'quick_think_llm' must be a non-empty string")

    if provider == "openai":
        reasoning_effort = config.get("openai_reasoning_effort")
        if reasoning_effort is not None:
            allowed = {"low", "medium", "high"}
            if reasoning_effort not in allowed:
                raise ValueError(
                    "'openai_reasoning_effort' must be one of: low, medium, high"
                )

    if provider == "google":
        thinking_level = config.get("google_thinking_level")
        if thinking_level is not None and not str(thinking_level).strip():
            raise ValueError("'google_thinking_level' must be a non-empty string when set")


def validate_selected_analysts(selected_analysts: list[str]) -> None:
    """Validate selected analyst sequence used for graph construction."""
    if not selected_analysts:
        raise ValueError("Trading Agents Graph Setup Error: no analysts selected!")

    if len(set(selected_analysts)) != len(selected_analysts):
        raise ValueError("selected_analysts must not contain duplicates")

    invalid = [a for a in selected_analysts if a not in SUPPORTED_ANALYSTS]
    if invalid:
        supported = ", ".join(sorted(SUPPORTED_ANALYSTS))
        raise ValueError(
            f"Unsupported analyst type(s): {', '.join(invalid)}. Supported: {supported}"
        )


def _validate_positive_int(config: Dict[str, Any], key: str) -> None:
    value = config.get(key)
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"'{key}' must be a positive integer")

