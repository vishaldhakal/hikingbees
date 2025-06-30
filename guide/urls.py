from django.urls import path
from .views import guide_list, guide_region, guide_list_slug, recent_guides

urlpatterns = [
    path('guides/', guide_list, name='guide_list'),
    path('latest-guides/', recent_guides, name='recent_guides'),
    path('guides-slug/', guide_list_slug, name='guide_list_slug'),
    path('guide-region/<str:slug>/', guide_region, name='guide_region'),
]
