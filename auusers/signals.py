from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from goodread.settings import EMAIL_HOST_USER

User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if instance.email and created:
        send_mail(
            subject="Welcome to goodreads-clone",
            message=f"Hi {instance.username}. Welcome to goodreads-clone. Enjoy the books and reviews",
            from_email=EMAIL_HOST_USER,
            recipient_list=[instance.email]
        )
