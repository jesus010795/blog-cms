from django.contrib import admin
from .models import Category, Post, Author


@admin.action(description="Restaurar posts seleccionados")
def restore_posts(modeladmin, request, queryset):
    queryset.update(deleted_at=None)


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "status", "deleted_at", "is_featured"]
    list_filter = ("status", "deleted_at", "user")
    readonly_fields = ("created", "updated")
    prepopulated_fields = {"slug": ("title",)}
    actions = [restore_posts]
    search_fields = ["title", "content", "user__username"]

    def get_queryset(self, request):
        return Post.all_objects.all()


class CategoryModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


class AuthorModelAdmin(admin.ModelAdmin):
    list_display = ["user", "is_site_author", "get_posts_count", "created"]
    readonly_fields = ["created", "updated"]
    search_fields = ["user__username", "user__first_name", "user__last_name"]

    def get_posts_count(self, obj):
        return obj.get_posts_count()

    get_posts_count.short_description = "Posts publicados"


admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Author, AuthorModelAdmin)
