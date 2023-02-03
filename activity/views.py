from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Activity,ActivityCategory,ItineraryActivity,ActivityImage
from .serializers import Destination,DestinationSerializer,ActivityCategorySerializer,ActivitySerializer,ItineraryActivitySerializer,ActivityImageSerializer,ActivitySmallSerializer

@api_view(['GET'])
def activities_collection(request):
    if request.method == 'GET':
        activities = Activity.objects.all()
        serializer_activities = ActivitySmallSerializer(activities, many=True)
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

        return Response({"activities":serializer_activities.data,"activity_categories":serializer_activity_category.data})

@api_view(['GET'])
def activities_single(request,slug):
    if request.method == 'GET':
        activity = Activity.objects.get(slug=slug)
        serializer_activities = ActivitySerializer(activity)
        return Response(serializer_activities.data)

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
