from django.urls import path, include
from . import views
from .views import activity_pdf_detail

urlpatterns = [
    path('activity-detail/<str:slug>/', views.activities_single),
    path('activities/', views.activities_collection),
    path('activities-slug/', views.activities_slug),
    path('activities-search/', views.activities_search),
    path('activitiy-categories-slug/', views.activities_cat_slug),
    path('activities-regions/', views.activities_regions),
    path('activities-region-slug/', views.activities_reg_slug),
    path('destinations-slug/', views.destination_slug),
    path('destinations/', views.destination_view),
    path('activitiy-categories/', views.activity_categories_collection),
    path('activities-all/<str:slug>/', views.activities_all),
    path('activities-region-wise/<str:slug>/', views.activities_all_region),
    path('activities-featured/', views.activities_featured),
    path('sign/', views.sign_view, name='sign_view'),
    path('activity-pdf/<str:slug>/', activity_pdf_detail, name='activity_pdf_detail'),
    path('video-reviews/', views.video_review_list, name='video-review-list'),
]
