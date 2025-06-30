from django.urls import path
from .views import guide_list, guide_region, recent_guides

urlpatterns = [
    path('guides/', guide_list, name='guide_list'),
    path('latest-guides/', recent_guides, name='recent_guides'),
    path('guide-region/<str:slug>/', guide_region, name='guide_region'),
]
