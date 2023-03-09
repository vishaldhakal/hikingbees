from django.shortcuts import render,HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FAQ,FAQCategory,FeaturedTour,TeamMember,Testimonial,SiteConfiguration,Affiliations,Partners,DestinationNavDropdown, OtherActivitiesNavDropdown, InnerDropdown, ClimbingNavDropdown, TreekingNavDropdown
from .serializers import FAQSerializer,FeaturedTourSerializer,FAQCategorySerializer,TeamMemberSlugSerializer,TestimonialSerializer,TeamMemberSerializer,AffiliationsSerializer,PartnersSerializer,SiteConfigurationSerializer,DestinationNavDropdownSerializer, OtherActivitiesNavDropdownSerializer, ClimbingNavDropdownSerializer, TreekingNavDropdownSerializer
from blog.models import Post
from blog.serializers import PostSerializer
from activity.models import ActivityCategory,Activity,ActivityEnquiry,ActivityBooking
from activity.serializers import ActivityCategorySerializer,ActivitySmallSerializer
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@api_view(["POST"])
def ContactFormSubmission(request):
    if request.method == "POST":
        subject = "Contact Form Submission"
        email = "Hiking Bees <info@hikingbees.com>"
        headers = {'Reply-To': request.POST["email"]}
        contex = {
            "name": request.POST["name"],
            "email": request.POST["email"],
            "phone": request.POST["phone"],
            "message": request.POST["message"]
        }
        html_content = render_to_string("contactForm.html", contex)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, "You have been sent a Contact Form Submission. Unable to Receive !", email, ["info@hikingbees.com"], headers=headers)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse("Sucess")
    else:
        return HttpResponse("Not post req")

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
def BookingSubmission(request):
    if request.method == "POST":
        subject = "Booking of Activity"
        email = "Hiking Bees <info@hikingbees.com>"
        headers = {'Reply-To': request.POST["email"]}

        name = request.POST["name"]
        address = request.POST["address"]
        emaill = request.POST["email"]
        phone = request.POST["phone"]
        message = request.POST["message"]
        no_of_guests = request.POST["no_of_guests"]
        total_price = request.POST["total_price"]
        booking_date = request.POST["booking_date"]
        arrival_date = request.POST["arrival_date"]
        departure_date = request.POST["departure_date"]
        emergency_contact_name = request.POST["emergency_contact_name"]
        emergency_address = request.POST["emergency_address"]
        emergency_phone = request.POST["emergency_phone"]
        emergency_email = request.POST["emergency_email"]
        emergency_relationship = request.POST["emergency_relationship"]

        try:
            actt = Activity.objects.get(slug=request.POST["slug"])
        except:
            return HttpResponse("Muji Activity vetiyena")

        try:
            neww = ActivityBooking.objects.create(activity=actt,name=name,address=address,email=emaill,phone=phone,no_of_guests=no_of_guests,message=message,total_price=total_price,booking_date=booking_date,arrival_date=arrival_date,departure_date=departure_date,emergency_contact_name=emergency_contact_name,emergency_address=emergency_address,emergency_phone=emergency_phone,emergency_email=emergency_email,emergency_relationship=emergency_relationship)
            neww.save()
        except:
            return HttpResponse("Muji Activity Book Bhayena")

        contex = {
            "name": request.POST["name"],
            "email": request.POST["email"],
            "phone": request.POST["phone"],
            "message": request.POST["message"],
            "total_price": request.POST["total_price"],
            "no_of_guests": request.POST["no_of_guests"],
            "booking_date": request.POST["booking_date"],
            "activity": actt.activity_title,
            "slug": request.POST["slug"]
        }

        html_content = render_to_string("contactForm3.html", contex)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, "You have been sent a Contact Form Submission. Unable to Receive !", email, ["info@hikingbees.com"], headers=headers)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse("Sucess")
    else:
        return HttpResponse("Not post req")

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
        
        return Response({
          "destination_nav":destination_nav_serializer.data,
          "other_activities_nav":other_nav_serializer.data,
          "climbing_nav":climb_nav_serializer.data,
          "trekking_nav":trek_nav_serializer.data,
        })


@api_view(['GET'])
def landing_page(request):
    if request.method == 'GET':
        teammembers = TeamMember.objects.all()
        teammembers_serializer = TeamMemberSerializer(teammembers,many=True)

        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial,many=True)
        
        hero_content = SiteConfiguration.objects.get()
        hero_content_serializer = SiteConfigurationSerializer(hero_content)

        posts = Post.objects.all()[:6]
        posts_serializer = PostSerializer(posts,many=True)

        activities = FeaturedTour.objects.get()
        serializer_activities = FeaturedTourSerializer(activities)

        activity_category = ActivityCategory.objects.all()
        serializer_activity_category = ActivityCategorySerializer(activity_category, many=True)
        
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
          "activity_categories":serializer_activity_category.data,
          "team_members":teammembers_serializer.data,
          "testimonials":testimonial_serializer.data,
          "affiliations":serializer_affiliations.data,
          "partners":serializer_partners.data,
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
        teammembers_serializer = TeamMemberSerializer(teammembers,many=True)
        
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