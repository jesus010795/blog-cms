from .models import Author
from django.core.cache import cache


def site_author(request):
    author = cache.get("site_author")

    if author is None:
        author = Author.objects.site_author()
        cache.set("site_author", author, 60 * 60)

    return {"site_author": author}
