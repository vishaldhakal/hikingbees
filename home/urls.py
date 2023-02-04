from django.urls import path, include
from . import views

urlpatterns = [
    path('landing-page/', views.landing_page),
    path('testimonials/', views.testimonials),
]
