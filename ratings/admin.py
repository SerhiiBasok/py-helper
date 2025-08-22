from django.contrib import admin
from ratings.models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["rating", "profile", "comment", "created_at", "from_user"]
    list_filter = ["rating"]
    search_filter = ["rating"]

