from django.conf import settings
from django.db import models


# Відгук користувача з коментарем і числовим рейтингом.
class Rating(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    profile = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name="reviews"
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, null=True, blank=True
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Rating {self.rating} by"
            f" {self.from_user.username if self.from_user else 'Anonymous'}"
            f" for {self.profile.user.username}"
        )
