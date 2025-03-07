from django.urls import path
from .views import PostListView,post_single,post_list_slug,recent_posts

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('latest-posts/', recent_posts, name='recent_posts'),
    path('posts-slug/', post_list_slug, name='post_list_slug'),
    path('post-single/<str:slug>/', post_single, name='post_single'),
]