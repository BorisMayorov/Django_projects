from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import *

# Create your views here.


class PostListView(ListView):

    template_name = 'blog\index.html'
    context_object_name = 'posts'

    def get_queryset(self):

        if self.kwargs:
            return Post.objects.filter(category__slug=self.kwargs['slug']).select_related('category')
        else:
            return Post.objects.all().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs:
            context["title"] = Category.objects.get(slug=self.kwargs['slug'])
        else:
            context["title"] = 'Home'
        return context


class PostDetailView(DetailView):

    template_name = 'blog\single.html'
    context_object_name = 'post'
    # model = Post
    queryset = Post.objects.all().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context["next_post"] = self.object.get_previous_by_created_at()
        except self.object.DoesNotExist:
            context["next_post"] = ''
        try:
            context["prev_post"] = self.object.get_next_by_created_at()
        except self.object.DoesNotExist:
            context["prev_post"] = ''
        context['title'] = self.object.title

        return context


class Search(ListView):
    template_name = 'blog\index.html'
    context_object_name = 'posts'

    def get_queryset(self):

        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Search results: ' + self.request.GET.get('s')
        return context

