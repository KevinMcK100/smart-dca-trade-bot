def lambda_handler(event, context):
    """
    Lambda handler for validating the incoming raw request.
    """

    # Function to check if a value can be converted to float
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    print(f"Inside request_validator function. Input Values: {event}")

    is_valid = (
            all(key in event for key in ['baseCurrency', 'quoteCurrency', 'quoteAmount', 'isTestnet'])
            and isinstance(event.get('baseCurrency'), str)
            and isinstance(event.get('quoteCurrency'), str)
            and is_float(event.get('quoteAmount'))
            and isinstance(event.get('isTestnet'), bool)
    )

    # Log the received values if valid
    if is_valid:
        print("Inside request_validator function. Valid request received.")
        print(f"base_currency: {event['baseCurrency']}")
        print(f"quote_currency: {event['quoteCurrency']}")
        print(f"quote_amount: {event['quoteAmount']}")
        print(f"is_testnet: {event.get('isTestnet')}")

    return {
        "originalRequest": event,
        "isValid": is_valid,
    }
