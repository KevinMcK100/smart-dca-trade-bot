from typing import List

import boto3


def get_stored_parameter(key_name: str, is_string_list: bool = False) -> List[str] | str:
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name=key_name, WithDecryption=True)
    value = parameter['Parameter']['Value']
    return value.split(',') if is_string_list else value
