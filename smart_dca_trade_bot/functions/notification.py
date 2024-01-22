import boto3
from botocore.exceptions import ClientError

from utils.aws_utils import get_stored_parameter


def lambda_handler(event, context):
    """
    Lambda handler for sending email notifications when events occur.
    """
    sender_email_address = get_stored_parameter("/SmartDcaTradeBot/Live/Notifications/senderEmailAddress")
    recipient_email_addresses = get_stored_parameter("/SmartDcaTradeBot/Live/Notifications/recipientEmailAddresses", True)

    ses_client = boto3.client('ses')
    email_subject = event.get('emailSubject', 'Smart DCA Trade Bot Notification')
    email_body = event.get('emailBody', 'No email body provided')
    additional_info = event.get('additionalInfo', '')

    email_body = f"Notification from Smart DCA Trade Bot.\n\n{email_body}\n\n{additional_info}"

    try:
        response = ses_client.send_email(
            Destination={'ToAddresses': recipient_email_addresses},
            Message={
                'Body': {'Text': {'Data': email_body}},
                'Subject': {'Data': email_subject}
            },
            Source=sender_email_address
        )
        print("Email sent! Message ID:", response['MessageId'])
    except ClientError as e:
        print("Error sending email:", e.response['Error']['Message'])

    return {"status": "Email sent"}
