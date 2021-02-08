from django.urls import path, include
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path("", PostList.as_view(), name="home"),
    path('category/<slug>/',
         GetCategory.as_view(), name="get_category"),
    path('tag/<slug>/',
         GetTag.as_view(), name="get_tag"),
    path('post/<slug>/', GetPost.as_view(), name="get_post"),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
]
