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


class PostQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)

    def published(self):
        return self.alive().filter(
            status=Post.Status.PUBLISHED, publish_at__lte=timezone.now()
        )

    def drafts(self):
        return self.filter(status=Post.Status.DRAFT)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db).alive()

    def published(self):
        return self.get_queryset().published()

    def dead(self):
        return PostQuerySet(self.model, using=self._db).dead()


class Post(models.Model):
    objects = PostManager()
    # all_objects = models.Manager()  # Manager por defecto

    class Status(models.TextChoices):
        DRAFT = "draft", "Borrador"
        PUBLISHED = "published", "Publicado"
        ARCHIVED = "archived", "Archivado"

    title = models.CharField(max_length=60, verbose_name="Titulo")
    content = models.TextField(verbose_name="Contenido")
    user = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
    categories = models.ManyToManyField(
        Category,
        verbose_name="Categorias",
        related_name="posts",
    )
    image = models.ImageField(blank=True, null=True, verbose_name="Imagen destacada")
    slug = models.SlugField(unique=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT
    )
    publish_at = models.DateTimeField(
        default=timezone.now, verbose_name="Fecha de publicacion"
    )
    deleted_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Fecha de eliminacion"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificacion")

    class Meta:
        verbose_name = "Publicacion"
        verbose_name_plural = "Publicaciones"
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail_post", kwargs={"slug": self.slug})

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields="deleted_at")

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])
