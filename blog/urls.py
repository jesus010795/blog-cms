from django.urls import path
from .views import ListPostView, DetailPostView, PostByCategoryView

app_name = "blog"
urlpatterns = [
    path("", ListPostView.as_view(), name="list_posts"),
    path("<slug:slug>/", DetailPostView.as_view(), name="detail_post"),
    path("category/<slug:slug>/", PostByCategoryView.as_view(), name="detail_category"),
]
