from django.urls import path, include
from . import views

urlpatterns = [
    path('landing-page/', views.landing_page),
    path('all-bookings/', views.all_bookings),
    path('testimonials/', views.testimonials),
    path('legaldocuments/', views.legaldocuments),
    path('team-members/', views.teams),
    path('team-members-id/', views.teams_id),
    path('navbar/', views.navbar),
    path('faqs/', views.faq_list),
    path('contact-form-submit/', views.ContactFormSubmission),
    path('enquiry-submit/', views.InquirySubmission),
    path('plan-trip-submit/', views.PlanTripSubmit),
    path('booking-submit/', views.BookingSubmission),
    path('newsletter-submit/', views.Newsletter),
    path('team-single/<int:id>/', views.teams_single),
]
