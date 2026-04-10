from django.core.mail import send_mail
from django.conf import settings
import threading # creating new thread for email sending, this take little time to send


def send_custom_mail(subject, message, recipient_list):
    def send():
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False
        )
    threading.Thread(target=send).start()