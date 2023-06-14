from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "update", "create"]
    list_display_links = ["id"]
    readonly_fields = ["update", "create"]
    search_fields = []


class RulesSingleInline(admin.StackedInline):
    fields = (
        ('title', 'rules'),
    )
    readonly_fields = ["update", "create"]
    model = RulesSingle


@admin.register(RulesBook)
class RulesBookAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    list_display_links = ["id", "title"]
    readonly_fields = ["update", "create"]
    search_fields = ["title", "user__user"]
    inlines = [RulesSingleInline]
