from django.contrib import admin

from apps.mailers.models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    autocomplete_fields = ("author",)
    list_display = (
        "id",
        "author",
        "status",
        "message",
        "created_at",
        "updated_at",
    )
    search_fields = ("campaign_name", "status", "email_content")
    list_filter = ("status", "country")
