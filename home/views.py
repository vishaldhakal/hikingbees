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
def landing_page(request):
    if request.method == 'GET':
        herosection_content = HeroSectionContent.objects.all()[:1]
        herosection_content_serializer = HeroSectionContentSerializer(herosection_content)
        
        testimonial = Testimonial.objects.all()[:1]
        testimonial_serializer = TestimonialSerializer(testimonial)
        
        teammembers = TeamMember.objects.all()[:1]
        teammembers_serializer = TeamMemberSerializer(teammembers)
        
        posts = Post.objects.all()[:3]
        posts_serializer = PostSerializer(posts)
        
        activity_categories = ActivityCategory.objects.all()[:3]
        activity_categories_serializer = ActivityCategorySerializer(activity_categories)
        
        return Response({
          "hero_section":herosection_content_serializer.data,
          "testimonials":testimonial_serializer.data,
          "team_members":teammembers_serializer.data,
          "activity_categories":activity_categories_serializer.data,
          "posts":posts_serializer.data,
        })

@api_view(['GET'])
def testimonials(request):
    if request.method == 'GET':
        testimonial = Testimonial.objects.all()[:1]
        testimonial_serializer = TestimonialSerializer(testimonial)
        
        return Response({
          "testimonials":testimonial_serializer.data,
        })