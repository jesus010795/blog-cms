from django.contrib import admin
from .models import Category, Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "deleted_at"]
    readonly_fields = ("created", "updated")
    prepopulated_fields = {"slug": ("title",)}


class CategoryModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
