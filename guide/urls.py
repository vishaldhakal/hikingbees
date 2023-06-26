from django.urls import path
from .views import guide_list,guide_single,guide_list_slug,recent_guides

urlpatterns = [
    path('guides/', guide_list, name='guide_list'),
    path('latest-guides/', recent_guides, name='recent_guides'),
    path('guides-slug/', guide_list_slug, name='guide_list_slug'),
    path('guide-single/<str:slug>/', guide_single, name='guide_single'),
]