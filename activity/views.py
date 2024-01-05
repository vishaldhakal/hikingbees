from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Activity,ActivityCategory,ActivityBooking,Destination,ActivityTestimonial,ItineraryActivity,ActivityImage,ActivityRegion
from .serializers import ActivityCategorySlugSerializer,ActivityTestimonialSerializer,ActivityBookingSerializer,ActivityRegionSlugSerializer,DestinationSerializerSmall,ActivitySlugSerializer,DestinationSerializer,ActivityCategorySerializer,ActivitySerializer,ItineraryActivitySerializer,ActivityImageSerializer,ActivitySmallSerializer,ActivityRegionSerializer,ActivityRegionSmallSerializer
import json
from django.core import serializers
from django.db.models import DateField
from django.db.models.functions import Cast
from django.utils import timezone
from datetime import datetime, time
import hashlib
import hmac
from django.utils.encoding import force_bytes
import base64

sentence_array = [
    "घर/जग्गा नामसारीको सिफारिस गरी पाऊँ",
    "मोही लगत कट्टाको सिफारिस पाउं",
    "घर कायम सिफारीस पाउं",
    "अशक्त सिफारिस",
    "छात्रबृत्तिको लागि सिफारिस पाऊँ",
    "आदिवासी जनजाति प्रमाणित गरी पाऊँ",
    "अस्थायी बसोबासको सिफारिस पाऊँ",
    "स्थायी बसोबासको सिफारिस गरी पाऊँ",
    "आर्थिक अवस्था कमजोर सिफारिस पाऊँ",
    "नयाँ घरमा विद्युत जडान सिफारिस पाऊँ",
    "धारा जडान सिफारिस पाऊँ",
    "दुबै नाम गरेको ब्यक्ति एक्कै हो भन्ने सिफारिस पाऊँ",
    "ब्यवसाय बन्द सिफारिस पाऊँ",
    "व्यवसाय ठाउँसारी सिफारिस पाऊँ",
    "कोर्ट–फिमिनाहा सिफारिस पाऊँ",
    "नाबालक सिफारिस पाऊँ",
    "चौपाया सिफारिस पाऊँ",
    "संस्था दर्ता गरी पाऊँ",
    "विद्यालय ठाउँसारी सिफारिस पाऊँ",
    "विद्यालय संचालन/कक्षा बृद्धिको सिफारिस पाऊँ",
    "जग्गा दर्ता सिफारिस पाऊँ",
    "संरक्षक सिफारिस पाऊँ",
    "बाटो कायम सिफारिस पाऊँ",
    "जिवित नाता प्रमाणित गरी पाऊँ",
    "मृत्यु नाता प्रमाणित गरी पाऊँ",
    "निःशुल्क स्वास्थ्य उपचारको लागि सिफारिस पाऊँ",
    "संस्था दर्ता सिफारिस पाऊँ",
    "घर बाटो प्रमाणित गरी पाऊँ",
    "चारकिल्ला प्रमाणित गरि पाउ",
    "जन्म मिति प्रमाणित गरि पाउ",
    "बिवाह प्रमाणित गरि पाऊँ",
    "घर पाताल प्रमाणित गरी पाऊँ",
    "हकदार प्रमाणित गरी पाऊँ",
    "अबिवाहित प्रमाणित गरी पाऊँ",
    "जग्गाधनी प्रमाण पूर्जा हराएको सिफारिस पाऊँ",
    "व्यवसाय दर्ता गरी पाऊँ",
    "मोही नामसारीको लागि सिफारिस गरी पाऊँ",
    "मूल्याङ्कन गरी पाऊँ",
    "तीन पुस्ते खोली सिफारिस गरी पाऊँ",
    "पुरानो घरमा विद्युत जडान सिफारिस पाऊँ",
    "सामाजिक सुरक्षा भत्ता नाम दर्ता सम्बन्धमा",
    "बहाल समझौता",
    "कोठा खोली पाऊँ",
    "अपाङ्ग सिफारिस पाऊँ",
    "नापी नक्सामा बाटो नभएको फिल्डमा बाटो भएको सिफारिस",
    "धारा नामसारी सिफारिस पाऊँ",
    "विद्युत मिटर नामसारी सिफारिस",
    "फोटो टाँसको लागि तीन पुस्ते खोली सिफारिस पाऊ",
    "कोठा बन्द सिफारिस पाऊँ",
    "अस्थाई टहराको सम्पत्ति कर तिर्न सिफारिस गरी पाऊँ",
    "औषधि उपचार बापत खर्च पाउँ भन्ने सम्वन्धमा",
    "नागरिकता र प्रतिलिपि सिफारिस",
    "अंग्रेजीमा सिफारिस"
]

SECRET_KEY = 'wXuq97YlFNPM2OU2i/Y1bGukJuY0LUl6u9nAg1Y91uQ='

@api_view(['POST'])
def sign_view(request):
    try:
        # Get the signed field names from the request
        signed_field_names = request.data.get('signed_field_names', '').split(',')

        # Create a list of field values
        field_values = [f"{item}={request.data.get(item, '')}" for item in signed_field_names]

        # Join the field values with a comma
        field_values_joined = ",".join(field_values)

        # Create a SHA-256 HMAC hash using the secret key
        hash_obj = hmac.new(force_bytes(SECRET_KEY), msg=force_bytes(field_values_joined), digestmod=hashlib.sha256)
        hash_value = base64.b64encode(hash_obj.digest()).decode('utf-8').strip()

        # Log the details (you may want to replace this with your actual logging mechanism)
        print({
            'request_body': request.data,
            'fieldValues': field_values,
            'fieldValuesJoined': field_values_joined,
            'hash': hash_value,
        })

        # Return the hash in the response
        return Response({'hash': hash_value})

    except Exception as e:
        # Handle exceptions appropriately
        return Response({'error': str(e)})
    
@api_view(['GET'])
def activities_collection(request):
    if request.method == 'GET':

        act_cat = request.GET.get("category","All")
        act_reg = request.GET.get("region","All")
        act_des = request.GET.get("destination","All")

        activities = Activity.objects.all()
        serializer_activities = ActivitySmallSerializer(activities, many=True)
        
        activities_cat = ActivityCategory.objects.all()
        serializer_activities_cat = ActivityCategorySerializer(activities_cat, many=True)
        
        activities_reg = ActivityRegion.objects.all()
        serializer_activities_reg = ActivityRegionSerializer(activities_reg, many=True)
        
        destinations = Destination.objects.all()
        serializer_destinations = DestinationSerializer(destinations, many=True)
        
        return Response({
            "activities":serializer_activities.data,
            "categories":serializer_activities_cat.data,
            "regions":serializer_activities_reg.data,
            "destinations":serializer_destinations.data,
        })

@api_view(['GET'])
def activities_slug(request):
    if request.method == 'GET':
        activities = Activity.objects.all()
        serializer_activities = ActivitySlugSerializer(activities, many=True)
        return Response(serializer_activities.data)

@api_view(['GET'])
def activities_search(request):
    if request.method == 'GET':
        activities = Activity.objects.all()
        serializer_activities = ActivitySmallSerializer(activities, many=True)
        return Response(serializer_activities.data)

@api_view(['GET'])
def activities_cat_slug(request):
    if request.method == 'GET':
        activities = ActivityCategory.objects.all()
        serializer_activities = ActivityCategorySlugSerializer(activities, many=True)
        return Response(serializer_activities.data)

@api_view(['GET'])
def activities_reg_slug(request):
    if request.method == 'GET':
        activities = ActivityRegion.objects.all()
        serializer_activities = ActivityRegionSlugSerializer(activities, many=True)
        return Response(serializer_activities.data)

@api_view(['GET'])
def destination_slug(request):
    if request.method == 'GET':
        activities = Destination.objects.all()
        serializer_activities = DestinationSerializerSmall(activities, many=True)
        return Response(serializer_activities.data)

@api_view(['GET'])
def activities_featured(request):
    if request.method == 'GET':
        activities = Activity.objects.all()[0:6]
        serializer_activities = ActivitySmallSerializer(activities, many=True)
        return Response(serializer_activities.data)

@api_view(['GET'])
def activities_all(request,slug):
    if request.method == 'GET':

        act_cat = request.GET.get("category","All")
        capp = slug.capitalize()
        deatt = Destination.objects.get(name=capp)

        if act_cat == "All":
            activities = Activity.objects.filter(destination=deatt)
        else:
            act_category = ActivityCategory.objects.get(slug=act_cat)
            activities = Activity.objects.filter(activity_category=act_category,destination=deatt)

        serializer_activities = ActivitySmallSerializer(activities, many=True)

        activity_category = ActivityCategory.objects.all()
        serializer_activity_category = ActivityCategorySerializer(activity_category, many=True)
        
        serializer_destination = DestinationSerializer(deatt)

        return Response({"activities":serializer_activities.data,"activity_categories":serializer_activity_category.data,"destination_details":serializer_destination.data})

@api_view(['GET'])
def activities_all_region(request,slug):
    if request.method == 'GET':

        act_region = request.GET.get("region","All")
        
        act_category = ActivityCategory.objects.get(slug=slug)
        
        act_categoriess = ActivityCategory.objects.all()

        if act_region == "All":
            activities = Activity.objects.filter(activity_category=act_category)
        else:
            act_regionn = ActivityRegion.objects.get(slug=act_region)
            activities = Activity.objects.filter(activity_category=act_category,activity_region=act_regionn)
        
        acts = ActivitySmallSerializer(activities,many=True)

        print(activities)
        activity_region = ActivityRegion.objects.filter(activity_category=act_category)
        serializer_activity_region = ActivityRegionSerializer(activity_region, many=True)

        return Response({"activities":acts.data,"activity_regions":serializer_activity_region.data})



@api_view(['GET'])
def activities_regions(request):
    if request.method == 'GET':
        activities = ActivityRegion.objects.all()
        serializer_activities = ActivityRegionSmallSerializer(activities, many=True)
        return Response(serializer_activities.data)

@api_view(['GET'])
def activities_single(request,slug):
    if request.method == 'GET':
        today = timezone.now().date()
        activity = Activity.objects.get(slug=slug)
        bookings = ActivityBooking.objects.filter(activity=activity,booking_date__gte=today)
        testimonials = ActivityTestimonial.objects.filter(activity=activity)
        testimonials_ser = ActivityTestimonialSerializer(testimonials,many=True)
        bookings = bookings.order_by('booking_date')
        grouped_bookings = []
        booking_dates = ActivityBooking.objects.filter(is_verified=True,is_private=False).annotate(
            booking_date_date=Cast('booking_date', output_field=DateField())
        ).values('booking_date_date').distinct()

        unique_dates = [booking['booking_date_date'] for booking in booking_dates]

        for datee in unique_dates:
            start_date = datetime.combine(datee, time.min)
            end_date = datetime.combine(datee, time.max)
            boki = ActivityBooking.objects.filter(booking_date__range=(start_date, end_date),is_verified=True,is_private=False)
            grouped_bookings.append(ActivityBookingSerializer(boki, many=True).data)

        serializer_activities = ActivitySerializer(activity)
        return Response({"data":serializer_activities.data,"bookings":grouped_bookings,"dates":unique_dates,"testimonials":testimonials_ser.data})
    



@api_view(['GET'])
def activity_categories_collection(request):
    if request.method == 'GET':
        activity_category = ActivityCategory.objects.all()
        serializer_activity_category = ActivityCategorySerializer(activity_category, many=True)
        return Response(serializer_activity_category.data)

@api_view(['GET'])
def activity_itenaries_collection(request):
    if request.method == 'GET':
        activity_itenaries = ItineraryActivity.objects.all()
        serializer_activity_itenaries = ItineraryActivitySerializer(activity_itenaries, many=True)
        return Response(serializer_activity_itenaries.data)

@api_view(['GET'])
def activity_images_collection(request):
    if request.method == 'GET':
        activity_images = ActivityImage.objects.all()
        serializer_activity_images = ActivityImageSerializer(activity_images, many=True)
        return Response(serializer_activity_images.data)
