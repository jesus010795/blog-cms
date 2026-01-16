from django.urls import path


app_name = "pages"
urlpatterns = [
    path("<slug:slug>/", views.PageDetailView.as_view(), name="page_detail"),
]
