from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import HeroSectionContent,TeamMember,Testimonial
from .serializers import HeroSectionContentSerializer,TestimonialSerializer,TeamMemberSerializer
from blog.models import Post
from blog.serializers import PostSerializer
from activity.models import ActivityCategory,Activity
from activity.serializers import ActivityCategorySerializer,ActivitySmallSerializer

@api_view(['GET'])
def testimonials(request):
    if request.method == 'GET':
        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial,many=True)
        
        return Response({
          "testimonials":testimonial_serializer.data,
        })

@api_view(['GET'])
def teams(request):
    if request.method == 'GET':
        teammembers = TeamMember.objects.all()
        teammembers_serializer = TeamMemberSerializer(teammembers,many=True)
        
        return Response({
          "team-members":teammembers_serializer.data,
        })

@api_view(['GET'])
def teams_single(request,id):
    if request.method == 'GET':
        teammembers = TeamMember.objects.get(id=id)
        teammembers_serializer = TeamMemberSerializer(teammembers)
        
        return Response({
          "team-member":teammembers_serializer.data,
        })