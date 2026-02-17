from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.config_validation import validate_tradingagents_config
from tradingagents.llm_clients.factory import create_llm_client
from tradingagents.llm_clients.openai_client import OpenAIClient
from tradingagents.llm_clients.validators import validate_model


def test_openclaw_provider_is_valid_config():
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "openclaw"
    validate_tradingagents_config(config)


def test_factory_maps_openclaw_to_openai_compatible_client():
    client = create_llm_client(provider="openclaw", model="openclaw-chat")
    assert isinstance(client, OpenAIClient)


def test_openclaw_accepts_any_model_name():
    assert validate_model("openclaw", "custom/model-name") is True
