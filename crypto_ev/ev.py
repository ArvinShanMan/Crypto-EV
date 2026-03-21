from .models import TradeParameters


def expected_value_per_trade(params: TradeParameters) -> float:
    """Compute analytical expected value for one trade."""
    return params.win_rate * params.profit_per_win - (1 - params.win_rate) * params.loss_per_trade



def expected_value_over_series(params: TradeParameters) -> float:
    """Compute analytical expected value for a run of trades."""
    return expected_value_per_trade(params) * params.trades_per_run
