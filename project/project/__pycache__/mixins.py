from django.conf import settings



class MessaHandler:
       

    phone_number =None
    otp = None
    def __init__(self,phone_number,otp):
        self.phone_number = phone_number
        self.otp =otp

    def send_otp_on(self):

        
        
