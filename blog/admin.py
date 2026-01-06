from django.contrib import admin
from .models import Category, Post


class PostModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")


class CategoryModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")


admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
