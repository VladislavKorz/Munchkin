from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "date_sent"]
    list_display_links = ["id", "name", "email", "date_sent"]

