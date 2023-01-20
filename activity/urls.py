from django.urls import path, include
from . import views

urlpatterns = [
    path('activity-detail/<str:slug>/', views.activities_single),
    path('activities/', views.activities_collection),
]
