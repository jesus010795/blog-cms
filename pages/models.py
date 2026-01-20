from django.db import models
from django.urls import reverse


# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titulo")
    content = models.TextField(verbose_name="Contenido")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion")
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    show_in_footer = models.BooleanField(
        default=False, verbose_name="Mostrar en el pie de pagina"
    )

    class Meta:
        verbose_name = "Pagina"
        verbose_name_plural = "Paginas"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("pages:page_detail", kwargs={"slug": self.slug})
