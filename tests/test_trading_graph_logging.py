import json

from tradingagents.graph.trading_graph import TradingAgentsGraph


def _sample_state():
    return {
        "company_of_interest": "NVDA",
        "trade_date": "2024-05-10",
        "market_report": "market",
        "sentiment_report": "sentiment",
        "news_report": "news",
        "fundamentals_report": "fundamentals",
        "investment_debate_state": {
            "bull_history": "bull",
            "bear_history": "bear",
            "history": "debate",
            "current_response": "Bull: buy",
            "judge_decision": "buy",
        },
        "trader_investment_plan": "plan",
        "risk_debate_state": {
            "aggressive_history": "agg",
            "conservative_history": "cons",
            "neutral_history": "neutral",
            "history": "risk",
            "judge_decision": "approved",
        },
        "investment_plan": "invest",
        "final_trade_decision": "BUY",
    }


def test_log_state_uses_results_dir(tmp_path):
    graph = TradingAgentsGraph.__new__(TradingAgentsGraph)
    graph.config = {"results_dir": str(tmp_path)}
    graph.ticker = "NVDA"
    graph.log_states_dict = {}

    graph._log_state("2024-05-10", _sample_state())

    log_path = (
        tmp_path
        / "NVDA"
        / "TradingAgentsStrategy_logs"
        / "full_states_log_2024-05-10.json"
    )
    assert log_path.exists()

    payload = json.loads(log_path.read_text(encoding="utf-8"))
    assert payload["2024-05-10"]["final_trade_decision"] == "BUY"
