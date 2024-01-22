import json
from typing import Dict, List

from utils.aws_utils import get_stored_parameter


def lambda_handler(event, context):
    """
    Lambda handler for triggering scheduled checking of quote currency balances on exchange.
    """
    print("Starting scheduled check of exchange quote currency balances")
    stored_param_input_key = "/SmartDcaTradeBot/Live/ScheduledBalanceChecker/input"
    raw_input = get_stored_parameter(stored_param_input_key)
    input_dict: List[Dict] = json.loads(raw_input)

    print(f"Required currency amount configuration from Parameter Store: {input_dict}")

    if input_dict is None or len(input_dict) == 0:
        raise ValueError(f"Input was empty for stored parameter: {stored_param_input_key}. It must be set as a list of dict "
                         f"e.g. [{'currency': 'USD', 'amount': 100}, {'currency': 'USDT', 'amount': 100}] ")
    states = []
    for entry in input_dict:
        input_keys = entry.keys()
        if 'currency' not in input_keys or 'amount' not in input_keys:
            raise ValueError(f"Found invalid input of {entry} for scheduled balance checker. It must be set as a list of dict "
                             f"e.g. [{'currency': 'USD', 'amount': 100}, {'currency': 'USDT', 'amount': 100}] ")
        states.append(
            {
                "state": {
                    "originalRequest": {
                        "quoteCurrency": entry['currency'],
                        "quoteAmount": float(entry['amount']),
                        "isTestnet": False
                    }
                }
            }
        )

    return states
