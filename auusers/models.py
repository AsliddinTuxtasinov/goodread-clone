from django.contrib.auth.models import AbstractUser
from django.db import models


class CostumUser(AbstractUser):
    profile_picture = models.ImageField(default='default-profile-picture.png', upload_to="picture/")
    are_you_author = models.BooleanField(default=False, blank=True)
