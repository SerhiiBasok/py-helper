from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Модель користувача
class User(AbstractUser):
    pass

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username


# Профіль користувача з додатковою інформацією.
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=20,
        blank=True
    )
    bio = models.TextField(
        blank=True
    )
    categories = models.ManyToManyField(
        "categories.Category", related_name="profiles", blank=True
    )

    def __str__(self):
        return f"{self.user.username}`s profile"
