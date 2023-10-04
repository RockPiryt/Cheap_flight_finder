import os
from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

TWILIO_SID = os.getenv("account_sid_twilio")
TWILIO_AUTH_TOKEN = os.getenv("auth_token_twilio")
TWILIO_VIRTUAL_NUMBER = os.getenv("tel_twilio")
TWILIO_VERIFIED_NUMBER = os.getenv("tel_my")


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)