import traceback
from typing import Dict

from ccxt import Exchange

from utils.exchanges import get_ccxt_exchange


def lambda_handler(event, context):
    """
    Lambda handler for placing orders on exchange.
    """
    print(f"Inside trade_executor function. Input values: {event}")
    state = event['state']
    original_request = state["originalRequest"]
    base_currency = original_request['baseCurrency']
    quote_currency = original_request['quoteCurrency']
    quote_amount = original_request['quoteAmount']
    is_test = original_request['isTestnet']

    try:
        exchange: Exchange = get_ccxt_exchange('kraken', is_test)
        raw_symbol = f"{base_currency}/{quote_currency}"
        all_tickers = dict(exchange.fetch_tickers())
        all_tickers_keys = list(all_tickers.keys())
        symbols = [x for x in all_tickers_keys if str(x).startswith(raw_symbol) and str(x).endswith(quote_currency)]
        symbol = symbols[0]
        if len(symbols) != 1:
            raise RuntimeError(f"Number of matching symbols must be 1 but was {len(symbols)}. Matching symbols: {symbols}")
        base_amount = get_amount_from_quote(quote_amount, symbol, all_tickers, exchange)
        print(f"Placing order for amount {base_amount} {base_currency} based on requested buy of {quote_amount} {quote_currency}")
        order = exchange.create_order(symbol=symbol, type='market', side='buy', amount=base_amount)
        print(f"Successfully created order on exchange: {order}")
        state['tradeStatus'] = 'success'
        state['order'] = order
    except Exception:
        print(f"Failed to place order. Exception: {traceback.format_exc()}")
        state['tradeStatus'] = 'failed'
        state['exception'] = traceback.format_exc()
    state['originalRequest'] = original_request
    return state


def get_amount_from_quote(quote_amount: float, symbol: str, all_tickers: Dict, exchange: Exchange) -> float:
    price = float(all_tickers[symbol]["last"])
    return float(exchange.amount_to_precision(symbol, float(quote_amount / price)))
