from django.contrib import admin
from .models import MetaTag

# Register your models here.
@admin.register(MetaTag)
class MetaTagAdmin(admin.ModelAdmin):
    list_display = ["id", "html_path"]
    list_display_links = ["id", "html_path"]
