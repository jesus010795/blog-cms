from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    slug = models.SlugField(unique=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificacion")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["-name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:detail_category", kwargs={"slug": self.slug})


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
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Publicacion"
        verbose_name_plural = "Publicaciones"
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail_post", kwargs={"slug": self.slug})
