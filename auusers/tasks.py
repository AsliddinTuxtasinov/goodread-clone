from django.core.mail import send_mail

from goodread.settings import EMAIL_HOST_USER
from goodread.celery import app


@app.task
def send_email(subject, message, resipiend_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=resipiend_list
    )
