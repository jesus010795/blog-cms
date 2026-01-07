from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category


class ListPostView(ListView):
    model = Post
    context_object_name = "posts"


class DetailPostView(DetailView):
    model = Post
    context_object_name = "post"
