from django.contrib import admin
from .models import Category, Post


@admin.action(description="Restaurar posts seleccionados")
def restore_posts(modeladmin, request, queryset):
    queryset.update(deleted_at=None)


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "deleted_at", "is_featured"]
    list_filter = ("status", "deleted_at")
    readonly_fields = ("created", "updated")
    prepopulated_fields = {"slug": ("title",)}
    actions = [restore_posts]

    def get_queryset(self, request):
        return Post.all_objects.all()


class CategoryModelAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
