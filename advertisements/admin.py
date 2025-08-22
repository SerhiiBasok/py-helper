from django.contrib import admin
from advertisements.models import Advertisement, Application


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ["user"]
    list_filter = ["location", "price"]

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["user"]
    list_filter = ["status"]


