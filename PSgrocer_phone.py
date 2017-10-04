from twilio.rest import Client
import certifi

class PS_Shopper_Phone:

    def __init__(self):
        # Your Account SID from twilio.com/console
        self.account_sid = "AC7df674e66c31920f936cd18a52525aff"
        # Your Auth Token from twilio.com/console
        self.auth_token  = "f23b2761ca8b7180f6fa135c91ec6ac4"
        # Set twilio number
        self.twilio_number = "+19472829832"

    def sendText(self, recipient, msg = "Testing Grocery App", debugg = False):
        #Connect to Twilio client
        client = Client(self.account_sid, self.auth_token)
        #Send Message
        message = client.messages.create(
            to = recipient,
            from_ = self.twilio_number,
            body = msg)

        if debugg:
            print(message.sid)
