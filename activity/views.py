from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Activity,ActivityCategory,ActivityBooking,Destination,ItineraryActivity,ActivityImage,ActivityRegion
from .serializers import ActivityCategorySlugSerializer,ActivityBookingSerializer,ActivitySmallestSerializer,ActivityRegionSlugSerializer,DestinationSerializerSmall,ActivitySlugSerializer,DestinationSerializer,ActivityCategorySerializer,ActivitySerializer,ItineraryActivitySerializer,ActivityImageSerializer,ActivitySmallSerializer,ActivityRegionSerializer
import json
from django.core import serializers
from django.db.models import DateField
from django.db.models.functions import Cast
from django.utils import timezone
from datetime import datetime, time

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
        serializer_activities = ActivitySmallestSerializer(activities, many=True)
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
def activities_single(request,slug):
    if request.method == 'GET':
        activity = Activity.objects.get(slug=slug)
        bookings = ActivityBooking.objects.filter(activity=activity)
        bookings = bookings.order_by('booking_date')
        grouped_bookings = []
        booking_dates = ActivityBooking.objects.annotate(
            booking_date_date=Cast('booking_date', output_field=DateField())
        ).values('booking_date_date').distinct()

        unique_dates = [booking['booking_date_date'] for booking in booking_dates]

        for datee in unique_dates:
            start_date = datetime.combine(datee, time.min)
            end_date = datetime.combine(datee, time.max)
            boki = ActivityBooking.objects.filter(booking_date__range=(start_date, end_date))
            grouped_bookings.append(ActivityBookingSerializer(boki, many=True).data)

        serializer_activities = ActivitySerializer(activity)
        return Response({"data":serializer_activities.data,"bookings":grouped_bookings})
    



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
