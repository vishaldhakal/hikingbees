from django.urls import path, include
from . import views

urlpatterns = [
    path('landing-page/', views.landing_page),
    path('testimonials/', views.testimonials),
    path('team-members/', views.teams),
    path('team-members-id/', views.teams_id),
    path('navbar/', views.navbar),
    path('faqs/', views.faq_list),
    path('contact-form-submit/', views.ContactFormSubmission),
    path('enquiry-submit/', views.InquirySubmission),
    path('booking-submit/', views.BookingSubmission),
    path('team-single/<int:id>/', views.teams_single),
    path('tinymce/', include('tinymce.urls')),
    path('fb/', views.django_filebrowser, name='djangoFileBrowser'),
]
