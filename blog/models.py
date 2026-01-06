from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificacion")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=60, verbose_name="Titulo")
    content = models.TextField(verbose_name="Contenido")
    user = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
    categories = models.ManyToManyField(
        Category,
        verbose_name="Categorias",
        related_name="posts",
    )
    image = models.ImageField(blank=True, null=True, verbose_name="Imagen destacada")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificacion")
    slug = models.SlugField(null=True)

    class Meta:
        verbose_name = "Publicacion"
        verbose_name_plural = "Publicaciones"
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
