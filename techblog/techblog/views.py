from .models import *
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, CommentForm
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from hitcount.views import HitCountDetailView
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class PostList(ListView):
    model = Post
    template_name = 'techblog/index.html'
    context_object_name = 'posts'
    pk_url_kwarg = 'post_id'
    extra_context = {'title': 'TechBlog'}
    queryset = Post.objects.select_related(
        'category',).prefetch_related('hit_count_generic',)

    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_posts"] = Post.objects.exclude(picture='').order_by(
            '-hit_count_generic__hits')[:3].select_related('category')
        return context


class GetCategory(ListView):
    template_name = 'techblog/category.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(
            slug=self.kwargs['slug'])
        return context


class GetTag(ListView):
    template_name = 'techblog/tag.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(
            slug=self.kwargs['slug'])
        return context


class GetPost(HitCountDetailView, FormMixin):

    template_name = 'techblog/single.html'
    model = Post
    context_object_name = 'post'
    count_hit = True
    form_class = CommentForm
    queryset = Post.objects.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post=self.object,
                                                     active=True).select_related('user')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.object
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('get_post', kwargs={'slug': self.object.slug})


def register(request):
    User._meta.get_field('email')._unique = True
    redirect_to = request.GET.get('next',)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have successfully registered.')
            return redirect(redirect_to)
        else:
            messages.error(request, 'Registration error.')
    else:
        form = UserRegisterForm()
    return render(request, 'techblog/register.html', {'form': form, })


def user_login(request):
    redirect_to = request.GET.get('next',)
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, f'Wellcome, {user.username}')
                return redirect(redirect_to)
        else:
            messages.error(request, 'Wrong login or password')
    else:
        form = UserLoginForm()
    return render(request, 'techblog/login.html', {'form': form})


def user_logout(request):
    redirect_to = request.GET.get('next',)
    logout(request)
    messages.info(request, 'You left site')
    return redirect(redirect_to)
