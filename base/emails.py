from django.core.mail import send_mail
from django.conf import settings
import uuid
import traceback

def send_account_activation_email(email, email_token):
    try:
        subject = 'Your account needs to be verified'
        email_from = settings.EMAIL_HOST_USER
        message = f'Hi, click on the link to activate your account: http://127.0.0.1:8000/accounts/activate/{email_token}'
        send_mail(subject, message, email_from, [email], fail_silently=False)
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")
        traceback.print_exc()
