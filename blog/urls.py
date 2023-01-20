from django.urls import path
from .views import post_list,post_single,post_list_slug

urlpatterns = [
    path('posts/', post_list, name='post_list'),
    path('posts-slug/', post_list_slug, name='post_list_slug'),
    path('post-single/<str:slug>/', post_single, name='post_single'),
]