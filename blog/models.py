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

    def archived(self):
        return self.alive().filter(status=Post.Status.ARCHIVED)


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

    def archived(self):
        return self.get_queryset().archived()


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
        self.save(update_fields=["deleted_at", "status"])


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
        return self.filter(is_site_author=True).first()


class Author(models.Model):
    objects = AuthorManager()

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Autor",
        related_name="author_profile",
        blank=True,
        null=True,
    )
    bio = models.TextField(
        verbose_name="Biografia", blank=True, help_text="Descripcion corta del autor"
    )
    avatar = models.ImageField(blank=True, null=True, verbose_name="Foto de perfil")
    website = models.URLField(
        blank=True, verbose_name="Sitio web", help_text="Url complet (htpps://...)"
    )
    github = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="GitHub",
        help_text="Solo el nombre de usuario",
    )
    linkedin = models.URLField(blank=True, verbose_name="Linkedin")
    twitter = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Twitter",
        help_text="Solo el nombre de usuario",
    )
    is_site_author = models.BooleanField(
        default=False,
        verbose_name="Autor principal del sitio",
        help_text="Solo puede haber uno marcado como principal",
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificacion")

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ["-created"]

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def get_absolute_url(self):
        return reverse("blog:author_profile", kwargs={"pk": self.pk})

    def get_posts_count(self):
        return self.user.post_set.published().count()

    def save(self, *args, **kwargs):
        if self.is_site_author:
            Author.objects.filter(is_site_author=True).update(is_site_author=False)
        super().save(*args, **kwargs)
