from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from goodread.settings import EMAIL_HOST_USER

from books.models import Author
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


@receiver(pre_save, sender=User)
def create_author(sender, instance, **kwargs):
    if not instance._state.adding:
        print('this is an update')
        if instance.are_you_author:
            print("yeah. I'm author.")
            if not Author.objects.filter(author=instance).exists():
                Author.objects.create(author=instance)
    else:
        print('this is an insert')
