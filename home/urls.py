from django.urls import path, include
from . import views

urlpatterns = [
    path('testimonials/', views.testimonials),
    path('team-members/', views.teams),
]
