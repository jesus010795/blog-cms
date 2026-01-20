from django.contrib import admin
from .models import Page


# Register your models here.
class PageModelAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created", "updated")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Page, PageModelAdmin)
