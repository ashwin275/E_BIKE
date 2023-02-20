from django.conf import settings
from twilio.rest import Client


def sentOTP(mobile):
    
         
        account_sid = settings.ACCOUNT_SID
        auth_token =   settings.AUTH_TOKEN
        client = Client(account_sid,auth_token)
        verification = client.verify.services(settings.VERIFICATION_SID).verifications.create(to='+91'+mobile,channel='sms')
    

def check_otp(mobile,otp):
        account_sid = settings.ACCOUNT_SID
        auth_token =   settings.AUTH_TOKEN
        client = Client(account_sid,auth_token)

        verification_check = client.verify.services(settings.VERIFICATION_SID).verification_checks.create(to='+91'+mobile,code=otp)

        if(verification_check.status == 'approved'):
            return True
        else:
            return False

