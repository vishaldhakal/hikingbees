from django.urls import path, include
from . import views

urlpatterns = [
    path('activity-detail/<str:slug>/', views.activities_single),
    path('activities/', views.activities_collection),
    path('activitiy-categories/', views.activity_categories_collection),
    path('activities-all/<str:slug>/', views.activities_all),
    path('activities-region-wise/<str:slug>/', views.activities_all_region),
    path('activities-featured/', views.activities_featured),
]
