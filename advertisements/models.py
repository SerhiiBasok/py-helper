from django.conf import settings
from django.db import models


class Advertisement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="advertisements",
    )
    title = models.CharField(
        max_length=255
    )
    price = models.PositiveIntegerField(
        default=0
    )
    location = models.CharField(
        max_length=255
    )
    categories = models.ManyToManyField(
        "categories.Category",
        related_name="advertisements"
    )
    description = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.title}"


class Application(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    message = models.TextField(
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accept"),
            ("rejected", "Rejected")
        ],
        default="pending"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "advertisement"], name="unique_advertisement"
            )
        ]

    """Прийняти заявку та закрити вакансію."""
    def accept(self):
        self.status = "accepted"
        self.save()
        self.advertisement.is_active = False
        self.advertisement.save()

    """Відхилити заявку."""
    def reject(self):
        self.status = "rejected"
        self.save()

    def __str__(self):
        return f"{self.advertisement.title} by {self.user.username}"
