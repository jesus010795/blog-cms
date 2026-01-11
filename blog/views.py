from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from .models import Post, Category


class ListPostView(ListView):
    # model = Post
    queryset = Post.objects.published()
    context_object_name = "posts"


class DetailPostView(DetailView):
    # model = Post
    queryset = Post.objects.published()
    context_object_name = "post"


class PostByCategoryView(ListView):
    """
    Esta es una vista de posts,
    cuyo criterio de filtrado es una categoría.
    """

    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        """
        Obtiene el queryset de publicaciones filtradas por una categoría específica.

        - Recupera la categoría a partir del slug recibido en la URL.
        - Almacena la categoría en `self.category` para reutilizarla
          posteriormente en otros métodos de la vista.
        - Retorna únicamente los posts asociados a dicha categoría
          mediante la relación inversa ManyToMany.

        Returns:
            QuerySet: Lista de objetos Post pertenecientes a la categoría.
        """
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return self.category.posts.published().select_related("user")

    def get_context_data(self, **kwargs):
        """
        Amplía el contexto base de la vista para incluir información
        relacionada con la categoría activa.

        Esto permite que el template reutilizado (`post_list.html`)
        pueda mostrar elementos contextuales como:
        - Título de la categoría
        - Mensajes personalizados
        - Encabezados dinámicos

        La categoría se obtiene previamente en `get_queryset` y se mantiene
        como estado de la vista durante todo el ciclo de la request.
        """
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context
