from django.shortcuts import render,HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FAQ,FAQCategory,LegalDocument,FeaturedTour,TeamMember,Testimonial,SiteConfiguration,Affiliations,Partners,DestinationNavDropdown, OtherActivitiesNavDropdown, InnerDropdown, ClimbingNavDropdown, TreekingNavDropdown,NewsletterSubscription
from .serializers import FAQSerializer, LandingFeaturedTourSerializer, LandingTeamMemberSerializer,LegalDocumentSerializer,FeaturedTourSerializer,FAQCategorySerializer,TeamMemberSlugSerializer,TestimonialSerializer,TeamMemberSerializer,AffiliationsSerializer,PartnersSerializer,SiteConfigurationSerializer,DestinationNavDropdownSerializer, OtherActivitiesNavDropdownSerializer,NavbarOtherActivitiesSerializer, ClimbingNavDropdownSerializer, TreekingNavDropdownSerializer
from blog.models import Post
from blog.serializers import LandingPagePostSerializer, NavbarPostSerializer, PostSmallSerializer
from activity.models import ActivityCategory,Activity,ActivityEnquiry,ActivityBooking
from activity.serializers import ActivityCategorySerializer,ActivitySmallSerializer,ActivityCategory2Serializer, NavbarActivitySerializer
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from activity.serializers import ActivityBooking2Serializer
from datetime import date

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

            subject = "Contact Form Submission"
            email_from = "Hiking Bees <info@hikingbees.com>"
            
            # Create email body
            body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}\n"
            
            try:
                send_mail(subject, body, email_from, ["info@hikingbees.com"], fail_silently=False)
            except Exception as e:
                return Response({
                    "error": "An error occurred while sending the email",
                    "details": str(e)
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
        subject = "Enquiry About Activity"
        email = "Hiking Bees <info@hikingbees.com>"
        headers = {'Reply-To': request.POST["email"]}

        actt = Activity.objects.get(slug=request.POST["slug"])
        if request.POST["phone"]:
            chh = request.POST["phone"]
        else:
            chh = "No Number"

        neww = ActivityEnquiry.objects.create(activity=actt,name=request.POST["name"],email=request.POST["email"],message=request.POST["message"],phone=chh)
        neww.save()

        contex = {
            "name": request.POST["name"],
            "email": request.POST["email"],
            "phone": request.POST["phone"],
            "message": request.POST["message"],
            "activity": actt.activity_title,
            "slug": request.POST["slug"]
        }

        html_content = render_to_string("contactForm2.html", contex)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, "You have been sent a Contact Form Submission. Unable to Receive !", email, ["info@hikingbees.com"], headers=headers)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse("Sucess")
    else:
        return HttpResponse("Not post req")

@api_view(["POST"])
def PlanTripSubmit(request):
    if request.method == "POST":
        subject = "Customized Trip Enquiry"
        email = "Hiking Bees <info@hikingbees.com>"
        headers = {'Reply-To': request.POST["email"]}

        actt = Activity.objects.get(slug=request.POST["slug"])

        contex = {
            "name": request.POST["name"],
            "email": request.POST["email"],
            "phone": request.POST["phone"],
            "message": request.POST["message"],
            "noofpeople": request.POST["no_of_people"],
            "noofdays": request.POST["no_of_days"],
            "arrival": request.POST["arrival"],
            "departure": request.POST["departure"],
            "budget_from": request.POST["budget_from"],
            "budget_to": request.POST["budget_to"],
            "activity": actt.activity_title,
            "slug": request.POST["slug"]
        }

        html_content = render_to_string("ContactForm4.html", contex)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, "You have been sent a Contact Form Submission. Unable to Receive !", email, ["info@hikingbees.com"], headers=headers)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse("Sucess")
    else:
        return HttpResponse("Not post req")

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
                    booking_date=datetime.strptime(booking_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
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
                        new_booking.arrival_date = datetime.strptime(arrival_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                    if departure_date_str:
                        new_booking.departure_date = datetime.strptime(departure_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
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
                
                new_booking.save()

                # Try to send email, but don't fail if it doesn't work
                try:
                    subject = "Booking of Activity"
                    email = "Hiking Bees <info@hikingbees.com>"
                    headers = {'Reply-To': emaill}

                    contex = {
                        "name": name,
                        "email": emaill,
                        "phone": phone,
                        "message": message,
                        "total_price": total_price,
                        "no_of_guests": no_of_guests,
                        "booking_date": booking_date_str,
                        "activity": act.activity_title,
                        "slug": slug
                    }

                    html_content = render_to_string("contactForm3.html", contex)
                    text_content = strip_tags(html_content)

                    msg = EmailMultiAlternatives(subject, "You have been sent a Contact Form Submission. Unable to Receive !", email, ["info@hikingbees.com"], headers=headers)

                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
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
    return Response({'success': "Subscribed Sucessfully"},status=status.HTTP_200_OK)

@api_view(['GET'])
def legaldocuments(request):
    legal_documents = LegalDocument.objects.all()
    legal_documents_serializer = LegalDocumentSerializer(legal_documents, many=True)
    return Response({'legal_documents': legal_documents_serializer.data})

@api_view(['GET'])
def faq_list(request):
    faqs = FAQ.objects.all()
    serializer = FAQSerializer(faqs, many=True)
    
    faq_cats = FAQCategory.objects.all()
    serializer_cat = FAQCategorySerializer(faq_cats, many=True)
    
    return Response({'faqs': serializer.data,"faq_categories":serializer_cat.data})


@api_view(['GET'])
def navbar(request):
    if request.method == 'GET':
        destination_nav = DestinationNavDropdown.objects.get()
        destination_nav_serializer = DestinationNavDropdownSerializer(destination_nav)

        other_nav = OtherActivitiesNavDropdown.objects.get()
        other_nav_serializer = OtherActivitiesNavDropdownSerializer(other_nav)
        
        acy = ActivityCategory.objects.get(title="Peak Climbing")
        climb_nav = Activity.objects.filter(activity_category=acy)
        climb_nav_serializer = ActivitySmallSerializer(climb_nav,many=True)

        trek_nav = TreekingNavDropdown.objects.get()
        trek_nav_serializer = TreekingNavDropdownSerializer(trek_nav)

        # Add latest 4 posts
        latest_posts = Post.objects.all().order_by('-created_at')[:4]
        latest_posts_serializer = NavbarPostSerializer(latest_posts, many=True)
        
        return Response({
          "destination_nav":destination_nav_serializer.data,
          "other_activities_nav":other_nav_serializer.data,
          "climbing_nav":climb_nav_serializer.data,
          "trekking_nav":trek_nav_serializer.data,
          "latest_posts": latest_posts_serializer.data,
        })


@api_view(['GET'])
def landing_page(request):
    if request.method == 'GET':
        today = date.today()

        teammembers = TeamMember.objects.all()
        teammembers_serializer = LandingTeamMemberSerializer(teammembers,many=True)

        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial,many=True)
        
        hero_content = SiteConfiguration.objects.get()
        hero_content_serializer = SiteConfigurationSerializer(hero_content)

        posts = Post.objects.all()[:5]
        posts_serializer = LandingPagePostSerializer(posts,many=True)
        
        bookings = ActivityBooking.objects.filter(booking_date__gte=today).order_by('-booking_date')[:10]
        bookings_serializer = ActivityBooking2Serializer(bookings,many=True)

        activities = FeaturedTour.objects.get()
        serializer_activities = LandingFeaturedTourSerializer(activities)

        activity_category = ActivityCategory.objects.all()
        serializer_activity_category = ActivityCategory2Serializer(activity_category, many=True)
        
        affiliations = Affiliations.objects.all()
        serializer_affiliations = AffiliationsSerializer(affiliations, many=True)
        
        partners = Partners.objects.all()
        serializer_partners = PartnersSerializer(partners, many=True)
        
        return Response({
          "hero_content":hero_content_serializer.data,
          "recent_posts":posts_serializer.data,
          "featured_activities":serializer_activities.data["featured_tours"],
          "popular_activities":serializer_activities.data["popular_tours"],
          "best_selling_activities":serializer_activities.data["best_selling_tours"],
          "favourite_activities":serializer_activities.data["favourite_tours"],
          "banner_activity":serializer_activities.data["banner_tour"],
          "activity_categories":serializer_activity_category.data,
          "team_members":teammembers_serializer.data,
          "testimonials":testimonial_serializer.data,
          "affiliations":serializer_affiliations.data,
          "partners":serializer_partners.data,
          "bookings":bookings_serializer.data,
        })

@api_view(['GET'])
def all_bookings(request):
    if request.method == 'GET':
        bookings = ActivityBooking.objects.all().order_by('-booking_date')
        bookings_serializer = ActivityBooking2Serializer(bookings,many=True)
        
        return Response({
          "bookings":bookings_serializer.data,
        })


@api_view(['GET'])
def testimonials(request):
    if request.method == 'GET':
        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial,many=True)
        
        return Response({
          "testimonials":testimonial_serializer.data,
        })

@api_view(['GET'])
def teams_id(request):
    if request.method == 'GET':
        teammembers = TeamMember.objects.all()
        teammembers_serializer = TeamMemberSlugSerializer(teammembers,many=True)
        
        return Response({
          "team_members":teammembers_serializer.data,
        })

@api_view(['GET'])
def teams(request):
    if request.method == 'GET':
        teammembers = TeamMember.objects.all()
        teammembers_serializer = LandingTeamMemberSerializer(teammembers,many=True)
        
        return Response({
          "team_members":teammembers_serializer.data,
        })

@api_view(['GET'])
def teams_single(request,id):
    if request.method == 'GET':
        teammembers = TeamMember.objects.get(id=id)
        teammembers_serializer = TeamMemberSerializer(teammembers)
        
        return Response({
          "team_member":teammembers_serializer.data,
        })

@api_view(['GET'])
def teams_single_slug(request,slug):
    if request.method == 'GET':
        teammembers = TeamMember.objects.get(slug=slug)
        teammembers_serializer = TeamMemberSerializer(teammembers)
        
        return Response({
          "team_member":teammembers_serializer.data,
        })