from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "update", "create"]
    list_display_links = ["id", "user"]
    readonly_fields = ["update", "create"]
    search_fields = ["user__username"]


class RulesSingleInline(admin.StackedInline):
    fields = (
        ('title', 'rules'),
    )
    readonly_fields = ["update", "create"]
    model = RulesSingle


@admin.register(RulesBook)
class RulesBookAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user"]
    list_display_links = ["id", "title"]
    readonly_fields = ["update", "create"]
    search_fields = ["title", "user__user__username"]
    inlines = [RulesSingleInline]
