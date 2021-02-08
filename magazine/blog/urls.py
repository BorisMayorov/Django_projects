from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('category/<str:slug>/', PostListView.as_view(), name='category'),
    path('post/<str:slug>/', cache_page(60*5)
         (PostDetailView.as_view()), name='post'),
    path('search/', Search.as_view(), name='search'),

]
