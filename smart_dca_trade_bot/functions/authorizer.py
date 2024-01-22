from utils.aws_utils import get_stored_parameter


def lambda_handler(event, context):
    secret_name = "/SmartDcaTradeBot/Live/Authentication/apiKey"
    expected_api_key = get_stored_parameter(key_name=secret_name)

    try:
        provided_api_key = event['queryStringParameters']['api_key']
    except KeyError:
        # If api_key is not provided in the request
        print(f"Could not find API key on query params. Event: {event}. Context: {context}")
        return generate_policy(None, 'Deny', event['methodArn'])

    # Compare provided API key with the expected API key
    if provided_api_key == expected_api_key:
        print(f"API key matches expected API key. Request authenticated. Event: {event}. Context: {context}")
        return generate_policy(provided_api_key, 'Allow', event['methodArn'])
    else:
        print(f"API key passed was {provided_api_key} which did not match expected API key. Denying request. "
              f"Event: {event}. Context: {context}")
        return generate_policy(provided_api_key, 'Deny', event['methodArn'])


def generate_policy(principal_id, effect, resource):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
    }
