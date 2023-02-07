from django.urls import path, include
from . import views

urlpatterns = [
    path('landing-page/', views.landing_page),
    path('testimonials/', views.testimonials),
    path('team-members/', views.teams),
    path('navbar/', views.navbar),
    path('team-single/<int:id>/', views.teams_single),
]
