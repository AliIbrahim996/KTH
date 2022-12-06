from twilio.rest import Client
import random

from kitchenhome.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_MESSAGING_SERVICE_SID


def send_verification_code(phone_number):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    # Generate random code
    code = random.randint(1000, 9999)
    message = client.messages.create(
        messaging_service_sid=TWILIO_MESSAGING_SERVICE_SID,
        body='Your verification code is {}'.format(code),
        to=phone_number
    )
    if message.error_code == 'None':
        return code
    return message.error_code
