from ccxt import Exchange

from utils.exchanges import get_ccxt_exchange, get_free_balance_for_currency


def lambda_handler(event, context):
    """
    Lambda handler for fetching the current value of quoteCurrency assets on the exchange.
    """
    print(f"Inside check_account_balance function. Input Values: {event}")
    state = event['state']
    original_request = state["originalRequest"]
    quote_currency = original_request['quoteCurrency']
    is_test = original_request['isTestnet']
    exchange: Exchange = get_ccxt_exchange('kraken', is_test)
    free_balance = get_free_balance_for_currency(exchange, quote_currency, is_test)
    state['accountBalance'] = free_balance
    state['originalRequest'] = original_request

    return state
