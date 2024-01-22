from typing import Dict

import ccxt
from ccxt import Exchange

from utils.aws_utils import get_stored_parameter


def get_ccxt_exchange(exchange: str, is_test: bool) -> Exchange:

    if exchange not in ccxt.exchanges:
        raise ValueError(f"Exchange {exchange} is not a valid CCXT change. Choose one from: {ccxt.exchanges}")

    if exchange.lower() == 'kraken':
        env = "Demo" if is_test else "Live"
        api_key_name = f"/SmartDcaTradeBot/{env}/KrakenAuthentication/apiKey"
        private_key_name = f"/SmartDcaTradeBot/{env}/KrakenAuthentication/privateKey"
        auth_params = {'apiKey': get_stored_parameter(api_key_name), 'secret': get_stored_parameter(private_key_name)}
        if is_test:
            # There is no testnet environment for Kraken spot exchange right now so we are forced to use the Futures version here
            ccxt_exchange = ccxt.krakenfutures(auth_params)
        else:
            ccxt_exchange = ccxt.kraken(auth_params)
        ccxt_exchange.set_sandbox_mode(is_test)
    else:
        raise ValueError(f"Exchange {exchange} is a valid CCXT exchange but is not yet supported in this bot. Please update code to add it")

    return ccxt_exchange


def get_free_balance_for_currency(exchange: Exchange, currency: str, is_test: bool) -> float:

    def get_balance(balances: Dict):
        print(f"All balances data from exchange: {balances}")
        try:
            if is_test:
                return float(balances['info']['accounts']['cash']['balances'][currency.lower()])
            else:
                return float(balances[currency]["free"])
        except KeyError as ke:
            raise RuntimeError(f"Currency {currency} not found on exchange", ke)

    print(f"About to call {exchange.name} exchange")
    all_balances = exchange.fetch_balance()

    return get_balance(all_balances)
