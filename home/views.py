from django.shortcuts import render, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FAQ, Enquiry, FAQCategory, LegalDocument, FeaturedTour, TeamMember, Testimonial, SiteConfiguration, Affiliations, Partners, DestinationNavDropdown, OtherActivitiesNavDropdown, InnerDropdown, ClimbingNavDropdown, TreekingNavDropdown, NewsletterSubscription
from .serializers import FAQSerializer, LandingFeaturedTourSerializer, LandingTeamMemberSerializer, LegalDocumentSerializer, FeaturedTourSerializer, FAQCategorySerializer, TeamMemberSlugSerializer, TestimonialSerializer, TeamMemberSerializer, AffiliationsSerializer, PartnersSerializer, SiteConfigurationSerializer, DestinationNavDropdownSerializer, OtherActivitiesNavDropdownSerializer, NavbarOtherActivitiesSerializer, ClimbingNavDropdownSerializer, TreekingNavDropdownSerializer
from blog.models import Post
from blog.serializers import LandingPagePostSerializer, NavbarPostSerializer, PostSmallSerializer
from activity.models import ActivityBookingAddOn, ActivityCategory, Activity, ActivityEnquiry, ActivityBooking, Destination
from activity.serializers import ActivityCategorySerializer, ActivitySmallSerializer, ActivityCategory2Serializer, NavbarActivitySerializer
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from activity.serializers import ActivityBooking2Serializer
from datetime import date
import json
import requests
import os
from dotenv import load_dotenv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")


def validate_name(name):
    """
    Validates the name field.
    Returns True if name is valid, False otherwise.
    """
    if not name or not isinstance(name, str):
        return False
    if len(name.strip()) < 2:
        return False
    return True


def validate_email(email):
    """
    Validates the email field.
    Returns True if email is valid, False otherwise.
    """
    if not email or not isinstance(email, str):
        return False
    if '@' not in email or '.' not in email:
        return False
    if len(email.split('@')[0]) < 1 or len(email.split('@')[1].split('.')[0]) < 1:
        return False
    return True


def validate_phone(phone):
    """
    Validates the phone field.
    Returns True if phone is valid, False otherwise.
    """
    if not phone:
        return True  # Phone is optional
    if not isinstance(phone, str):
        return False
    # Remove any non-digit characters
    phone_digits = ''.join(filter(str.isdigit, phone))
    if len(phone_digits) < 10:
        return False
    return True


def send_brevo_email(name, email, phone, message):
    """Helper function to send email via Brevo API"""
    try:
        # Configure API client
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration))

        # Render email template
        email_html = render_to_string("contact_email.html", {
            "name": name,
            "email": email,
            "phone": phone or "Not provided",
            "message": message
        })

        # Prepare email request
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": "info@hikingbees.com"},
                {"email": email}],
            sender={"email": "info@hikingbees.com", "name": "Hiking Bees"},
            subject=f"New Contact Form Submission from {name}",
            html_content=email_html,
            reply_to={"email": email, "name": name}
        )

        # Send email
        api_instance.send_transac_email(send_smtp_email)
        return True, None

    except ApiException as e:
        return False, f"Brevo API error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


@api_view(["POST"])
def ContactFormSubmission(request):
    if request.method == "POST":
        try:
            # Get data from either POST or request.data (for JSON)
            data = request.POST or request.data

            # Get required fields
            name = data.get("name", "").strip()
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            message = data.get("message", "").strip()

            # Validate all fields
            if not validate_name(name) or not validate_email(email) or not validate_phone(phone):
                return Response({
                    "error": "Validation failed",
                    "message": "Please check your input fields"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Send email using Brevo
            success, error = send_brevo_email(name, email, phone, message)

            # Create enquiry record
            enquiry = Enquiry.objects.create(
                name=name, email=email, phone=phone, message=message)
            enquiry.save()

            if not success:
                return Response({
                    "error": "Failed to send email",
                    "details": error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "message": "Contact form submitted successfully",
                "data": {
                    "name": name,
                    "email": email,
                    "phone": phone or "Not provided"
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": "An error occurred while processing your request",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "error": "Method not allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
def InquirySubmission(request):
    if request.method == "POST":
        try:
            # Handle both multipart and form-urlencoded data
            data = request.POST or request.data

            # Safely get form data with defaults
            user_email = data.get("email")
            name = data.get("name")
            phone = data.get("phone", "No Number")
            message = data.get("message")
            slug = data.get("slug")

            if not all([user_email, name, message, slug]):
                return Response({
                    "error": "Missing required fields"
                }, status=status.HTTP_400_BAD_REQUEST)
            try:
                actt = Activity.objects.get(slug=slug)
            except Activity.DoesNotExist:
                return Response({
                    "error": "Activity not found"
                }, status=status.HTTP_404_NOT_FOUND)

            # Create enquiry record
            neww = ActivityEnquiry.objects.create(
                activity=actt,
                name=name,
                email=user_email,
                message=message,
                phone=phone
            )
            neww.save()

            try:
                success, error = send_inquiry_brevo(
                    name=name,
                    email=user_email,
                    phone=phone,
                    message=message,
                    activity_title=actt.activity_title,
                    slug=slug
                )
                if not success:
                    return Response({
                        "error": "Failed to send email",
                        "details": error
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({
                    "error": "Failed to send email",
                    "details": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "message": "Inquiry submitted successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": "An error occurred",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "error": "Method not allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def send_plan_trip_brevo(name, email, phone, message, no_of_people, no_of_days, arrival, departure, budget_from, budget_to, activity_title, slug):
    """Helper function to send email via Brevo API"""
    try:
        # Configure API client
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration))

        # Render email template
        email_html = render_to_string("plan_trip_email.html", {
            "name": name,
            "email": email,
            "phone": phone or "Not provided",
            "message": message,
            "no_of_people": no_of_people,
            "no_of_days": no_of_days,
            "arrival": arrival,
            "departure": departure,
            "budget_from": budget_from,
            "budget_to": budget_to,
            "activity_title": activity_title,
            "slug": slug
        })

        # Prepare email request
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": "info@hikingbees.com"},
                {"email": email}],
            sender={"email": "info@hikingbees.com", "name": "Hiking Bees"},
            subject=f"New Trip Plan Submission from {name}",
            html_content=email_html,
            reply_to={"email": email, "name": name}
        )

        # Send email
        api_instance.send_transac_email(send_smtp_email)
        return True, None

    except ApiException as e:
        return False, f"Brevo API error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


@api_view(["POST"])
def PlanTripSubmit(request):
    if request.method == "POST":
        try:
            # Get data from either POST or request.data
            data = request.POST or request.data
            actt = Activity.objects.get(slug=data.get("slug", "").strip())

            # Get required fields
            name = data.get("name", "").strip()
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            message = data.get("message", "").strip()
            no_of_people = data.get("no_of_people", "").strip()
            no_of_days = data.get("no_of_days", "").strip()
            arrival = data.get("arrival", "").strip()
            departure = data.get("departure", "").strip()
            budget_from = data.get("budget_from", "").strip()
            budget_to = data.get("budget_to", "").strip()
            slug = data.get("slug", "").strip()
            activity_title = actt.activity_title

            # Validate required fields
            if not validate_name(name) or not validate_email(email) or not validate_phone(phone):
                return Response({
                    "error": "Validation failed",
                    "message": "Please check your input fields"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Replace EmailJS with Brevo
            success, error = send_plan_trip_brevo(
                name, email, phone, message, no_of_people, no_of_days,
                arrival, departure, budget_from, budget_to,
                activity_title, slug
            )

            if not success:
                return Response({
                    "error": "Failed to send email",
                    "details": error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "message": "Trip plan submitted successfully",
                "data": {
                    "name": name,
                    "email": email,
                    "activity": actt.activity_title
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": "An error occurred while processing your request",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        "error": "Method not allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def send_booking_brevo(name, email, phone, message, total_price, no_of_guests, booking_date, activity_title, slug):
    """Helper function to send booking confirmation email via Brevo API"""
    try:
        # Configure API client
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration))

        # Render email template
        email_html = render_to_string("booking_email.html", {
            "name": name,
            "email": email,
            "phone": phone or "Not provided",
            "message": message,
            "total_price": total_price,
            "no_of_guests": no_of_guests,
            "booking_date": booking_date,
            "activity": activity_title,
            "slug": slug
        })

        # Prepare email request
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": "info@hikingbees.com"},
                {"email": email}],
            sender={"email": "info@hikingbees.com", "name": "Hiking Bees"},
            subject=f"Booking Confirmation for {activity_title}",
            html_content=email_html,
            reply_to={"email": email, "name": name}
        )

        # Send email
        api_instance.send_transac_email(send_smtp_email)
        return True, None

    except ApiException as e:
        return False, f"Brevo API error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


@api_view(["POST"])
def BookingSubmission(request):
    if request.method == "POST":
        try:
            # Handle both multipart and form-urlencoded data
            data = request.POST or request.data

            # Get all form data first
            name = data.get("name", "")
            emaill = data.get("email", "")
            address = data.get("address", "")
            phone = data.get("phone", "")
            message = data.get("message", "")
            no_of_guests = int(data.get("no_of_guests", "0"))
            total_price = float(data.get("total_price", "0.0"))
            booking_date_str = data.get("booking_date", "")
            arrival_date_str = data.get("arrival_date", "")
            private_booking = data.get("private_booking", "False")
            departure_date_str = data.get("departure_date", "")
            slug = data.get("slug", "")

            # Create booking first
            try:
                act = Activity.objects.get(slug=slug)
                new_booking = ActivityBooking.objects.create(
                    activity=act,
                    name=name,
                    address=address,
                    email=emaill,
                    no_of_guests=no_of_guests,
                    total_price=total_price,
                    booking_date=datetime.strptime(
                        booking_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                )

                # Set optional fields
                if private_booking == "True":
                    new_booking.is_private = True
                if phone:
                    new_booking.phone = phone
                if message:
                    new_booking.message = message

                # Handle dates
                try:
                    if arrival_date_str:
                        new_booking.arrival_date = datetime.strptime(
                            arrival_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                    if departure_date_str:
                        new_booking.departure_date = datetime.strptime(
                            departure_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                except ValueError:
                    pass  # Skip if date parsing fails

                # Set emergency contact info
                emergency_contact_name = data.get("emergency_contact_name", "")
                emergency_address = data.get("emergency_address", "")
                emergency_phone = data.get("emergency_phone", "")
                emergency_email = data.get("emergency_email", "")
                emergency_relationship = data.get("emergency_relationship", "")
                if emergency_contact_name:
                    new_booking.emergency_contact_name = emergency_contact_name
                if emergency_address:
                    new_booking.emergency_address = emergency_address
                if emergency_phone:
                    new_booking.emergency_phone = emergency_phone
                if emergency_email:
                    new_booking.emergency_email = emergency_email
                if emergency_relationship:
                    new_booking.emergency_relationship = emergency_relationship

                # Handle add-ons
                addons_data = data.get('booking_addons', [])
                if isinstance(addons_data, str):
                    # If it's a string (from form data), try to parse it as JSON
                    try:
                        addons_data = json.loads(addons_data)
                    except json.JSONDecodeError:
                        addons_data = []

                for addon in addons_data:
                    try:
                        addon_id = addon.get('id')
                        quantity = addon.get('quantity', 0)
                        if addon_id and quantity > 0:
                            ActivityBookingAddOn.objects.create(
                                booking=new_booking,
                                addon_id=addon_id,
                                quantity=quantity
                            )
                    except Exception as e:
                        print(f"Failed to add addon: {str(e)}")
                        # Continue with other addons even if one fails

                new_booking.save()

                # Try to send email, but don't fail if it doesn't work
                try:
                    success, error = send_booking_brevo(
                        name=name,
                        email=emaill,
                        phone=phone,
                        message=message,
                        total_price=total_price,
                        no_of_guests=no_of_guests,
                        booking_date=booking_date_str,
                        activity_title=act.activity_title,
                        slug=slug
                    )
                    if not success:
                        print(f"Email sending failed: {error}")
                except Exception as e:
                    print(f"Email sending failed: {str(e)}")
                    # Continue anyway since booking was saved

                return Response({
                    "message": "Booking created successfully",
                    "booking_id": new_booking.id
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({
                    "error": f"Failed to create booking: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({
                "error": f"Request processing failed: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "error": "Method not allowed"
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def Newsletter(request):
    emaill = request.POST.get("email")
    nsss = NewsletterSubscription.objects.create(email=emaill)
    nsss.save()
    """ subject = "Newsletter Subscribed" """

    """ body = f"Newsletter Subscribed by {emaill}\n" """

    """ send_mail(subject, body, "info@hikingbees.com",  [emaill,"info@hikingbees.com"], fail_silently=False) """
    return Response({'success': "Subscribed Sucessfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def legaldocuments(request):
    legal_documents = LegalDocument.objects.all()
    legal_documents_serializer = LegalDocumentSerializer(
        legal_documents, many=True)
    return Response({'legal_documents': legal_documents_serializer.data})


@api_view(['GET'])
def faq_list(request):
    faqs = FAQ.objects.all()
    serializer = FAQSerializer(faqs, many=True)

    faq_cats = FAQCategory.objects.all()
    serializer_cat = FAQCategorySerializer(faq_cats, many=True)

    return Response({'faqs': serializer.data, "faq_categories": serializer_cat.data})


@api_view(['GET'])
def navbar(request):
    if request.method == 'GET':
        destination_nav = DestinationNavDropdown.objects.get()
        destination_nav_serializer = DestinationNavDropdownSerializer(
            destination_nav)

        other_nav = OtherActivitiesNavDropdown.objects.get()
        other_nav_serializer = OtherActivitiesNavDropdownSerializer(other_nav)

        acy = ActivityCategory.objects.get(title="Peak Climbing")
        climb_nav = Activity.objects.filter(activity_category=acy)
        climb_nav_serializer = ActivitySmallSerializer(climb_nav, many=True)

        trek_nav = TreekingNavDropdown.objects.get()
        trek_nav_serializer = TreekingNavDropdownSerializer(trek_nav)

        # Add latest 4 posts
        latest_posts = Post.objects.all().order_by('-created_at')[:4]
        latest_posts_serializer = NavbarPostSerializer(latest_posts, many=True)

        return Response({
            "destination_nav": destination_nav_serializer.data,
            "other_activities_nav": other_nav_serializer.data,
            "climbing_nav": climb_nav_serializer.data,
            "trekking_nav": trek_nav_serializer.data,
            "latest_posts": latest_posts_serializer.data,
        })


@api_view(['GET'])
def landing_page(request):
    if request.method == 'GET':
        today = date.today()

        teammembers = TeamMember.objects.all()
        teammembers_serializer = LandingTeamMemberSerializer(
            teammembers, many=True)

        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial, many=True)

        hero_content = SiteConfiguration.objects.get()
        hero_content_serializer = SiteConfigurationSerializer(hero_content)

        posts = Post.objects.all()[:5]
        posts_serializer = LandingPagePostSerializer(posts, many=True)

        bookings = ActivityBooking.objects.filter(
            booking_date__gte=today).order_by('-booking_date')[:10]
        bookings_serializer = ActivityBooking2Serializer(bookings, many=True)

        activities = FeaturedTour.objects.get()
        serializer_activities = LandingFeaturedTourSerializer(activities)

        activity_category = ActivityCategory.objects.all()
        serializer_activity_category = ActivityCategory2Serializer(
            activity_category, many=True)

        affiliations = Affiliations.objects.all()
        serializer_affiliations = AffiliationsSerializer(
            affiliations, many=True)

        partners = Partners.objects.all()
        serializer_partners = PartnersSerializer(partners, many=True)

        return Response({
            "hero_content": hero_content_serializer.data,
            "recent_posts": posts_serializer.data,
            "featured_activities": serializer_activities.data["featured_tours"],
            "popular_activities": serializer_activities.data["popular_tours"],
            "best_selling_activities": serializer_activities.data["best_selling_tours"],
            "favourite_activities": serializer_activities.data["favourite_tours"],
            "banner_activity": serializer_activities.data["banner_tour"],
            "activity_categories": serializer_activity_category.data,
            "team_members": teammembers_serializer.data,
            "testimonials": testimonial_serializer.data,
            "affiliations": serializer_affiliations.data,
            "partners": serializer_partners.data,
            "bookings": bookings_serializer.data,
        })


@api_view(['GET'])
def all_bookings(request):
    if request.method == 'GET':
        bookings = ActivityBooking.objects.all().order_by('-booking_date')
        bookings_serializer = ActivityBooking2Serializer(bookings, many=True)

        return Response({
            "bookings": bookings_serializer.data,
        })


@api_view(['GET'])
def testimonials(request):
    if request.method == 'GET':
        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial, many=True)

        return Response({
            "testimonials": testimonial_serializer.data,
        })


@api_view(['GET'])
def teams_id(request):
    if request.method == 'GET':
        teammembers = TeamMember.objects.all()
        teammembers_serializer = TeamMemberSlugSerializer(
            teammembers, many=True)

        return Response({
            "team_members": teammembers_serializer.data,
        })


@api_view(['GET'])
def teams(request):
    if request.method == 'GET':
        teammembers = TeamMember.objects.all()
        teammembers_serializer = LandingTeamMemberSerializer(
            teammembers, many=True)

        return Response({
            "team_members": teammembers_serializer.data,
        })


@api_view(['GET'])
def teams_single(request, id):
    if request.method == 'GET':
        teammembers = TeamMember.objects.get(id=id)
        teammembers_serializer = TeamMemberSerializer(teammembers)

        return Response({
            "team_member": teammembers_serializer.data,
        })


@api_view(['GET'])
def teams_single_slug(request, slug):
    if request.method == 'GET':
        teammembers = TeamMember.objects.get(slug=slug)
        teammembers_serializer = TeamMemberSerializer(teammembers)

        return Response({
            "team_member": teammembers_serializer.data,
        })


def send_inquiry_brevo(name, email, phone, message, activity_title, slug):
    """Helper function to send inquiry confirmation email via Brevo API"""
    try:
        # Configure API client
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration))

        # Render email template
        email_html = render_to_string("inquiry_email.html", {
            "name": name,
            "email": email,
            "phone": phone or "Not provided",
            "message": message,
            "activity": activity_title,
            "slug": slug
        })

        # Prepare email request
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": "info@hikingbees.com"},
                {"email": email}],
            sender={"email": "info@hikingbees.com", "name": "Hiking Bees"},
            subject=f"Inquiry About {activity_title}",
            html_content=email_html,
            reply_to={"email": email, "name": name}
        )

        # Send email
        api_instance.send_transac_email(send_smtp_email)
        return True, None

    except ApiException as e:
        return False, f"Brevo API error: {str(e)}"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


@api_view(['GET'])
def sitemap(request):
    if request.method == 'GET':
        # Get all posts and their slugs
        posts = Post.objects.all()
        post_slugs = [{'slug': post.slug} for post in posts]
        activities = Activity.objects.all()
        activity_slugs = [{'slug': activity.slug} for activity in activities]
        activity_categories = ActivityCategory.objects.all()
        activity_category_slugs = [{'slug': activity_category.slug}
                                   for activity_category in activity_categories]
        destinations = Destination.objects.all()
        destination_slugs = [{'slug': destination.name}
                             for destination in destinations]

        return Response({
            "posts": post_slugs,
            "activity": activity_slugs,
            "activity_category": activity_category_slugs,
            "destination": destination_slugs
        }, status=status.HTTP_200_OK)
