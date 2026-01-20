from .models import Page
from django.core.cache import cache


def footer_pages(request):
    pages = cache.get("footer_pages")
    if pages is None:
        pages = list(
            Page.objects.filter(is_active=True, show_in_footer=True).only(
                "title", "slug"
            )
        )
        cache.set("footer_pages", pages, 60 * 60)
    return {"footer_pages": pages}
