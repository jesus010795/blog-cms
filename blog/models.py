from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db import models


class CategoryQuerySet(models.QuerySet):
    def main(self):
        return self.order_by("name")

    def categories_for_home(self):
        return self.main()[:4]


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def main(self):
        return self.get_queryset().main()

    def categories_for_home(self):
        return self.get_queryset().categories_for_home()


class Category(models.Model):
    objects = CategoryManager()
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

    def popular(self):
        # Por ahora: orden arbitrario (luego métricas reales)
        return self.published().order_by("-created")

    def drafts(self):
        return self.filter(status=Post.Status.DRAFT)

    def for_home_latest(self):
        return self.published()[:3]

    def for_home_popular(self):
        return self.popular()[:5]

    def featured(self):
        return self.published().filter(is_featured=True)

    def for_home_featured(self):
        return self.featured().first()


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db).alive()

    def published(self):
        return self.get_queryset().published()

    def dead(self):
        return PostQuerySet(self.model, using=self._db).dead()

    def popular(self):
        return self.get_queryset().popular()

    def for_home_latest(self):
        return self.get_queryset().for_home_latest()

    def for_home_popular(self):
        return self.get_queryset().for_home_popular()

    def for_home_featured(self):
        return self.get_queryset().for_home_featured()


class Post(models.Model):
    objects = PostManager()
    all_objects = models.Manager()  # Manager por defecto

    class Status(models.TextChoices):
        DRAFT = "draft", "Borrador"
        PUBLISHED = "published", "Publicado"
        ARCHIVED = "archived", "Archivado"
        DELETED = "deleted", "Eliminado"

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
    is_featured = models.BooleanField(default=False, verbose_name="Destacado en Home")
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
        self.status = self.Status.DELETED
        self.save(update_fields=["deleted_at", "status"])

    def restore(self):
        self.deleted_at = None
        self.status = self.Status.DRAFT
        self.save(update_fields=["deleted_at"])


class StaticPageManager(models.Manager):
    def by_slug(self, slug):
        return self.get(slug=slug)


class StaticPage(models.Model):
    slug = models.SlugField(unique=True)
    content = models.TextField()

    objects = StaticPageManager()

    class Meta:
        verbose_name = "Pagina estatica"
        verbose_name_plural = "Paginas estaticas"
        ordering = ["slug"]

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("static_page", kwargs={"slug": self.slug})


class AuthorManager(models.Manager):
    def site_author(self):
        return self.first()


class Author(models.Model):
    ...
    objects = AuthorManager()
