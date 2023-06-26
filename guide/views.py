from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TravelGuide,GuideAuthour,TravelGuideRegion,TravelGuideCategory
from .serializers import TravelGuideSerializer,TravelGuideSlugSerializer,TravelGuideSmallSerializer,GuideAuthourSerializer,TravelGuideCategorySerializer,TravelGuideRegionSerializer
from bs4 import BeautifulSoup


@api_view(['GET'])
def guide_list(request):
    if request.method == 'GET':
        posts = TravelGuide.objects.all()
        serializer = TravelGuideSmallSerializer(posts, many=True)
        regions = TravelGuideRegion.objects.all()
        categories = TravelGuideCategory.objects.all()
        categories_serializer = TravelGuideCategorySerializer(categories, many=True)
        regions_serializer = TravelGuideRegionSerializer(regions, many=True)
        return Response({
            "guides":serializer.data,
            "regions":regions_serializer.data,
            "categories":categories_serializer.data,
        })

@api_view(['GET'])
def guide_list_slug(request):
    if request.method == 'GET':
        posts = TravelGuide.objects.all()
        serializer = TravelGuideSlugSerializer(posts, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def guide_single(request,slug):
    if request.method == 'GET':
        posts = TravelGuide.objects.get(slug=slug)
        html_string = posts.blog_content
        soup = BeautifulSoup(html_string, 'html.parser')
        toc_div = soup.find('div', class_='mce-toc')
        if toc_div is not None:
            toc_div.extract()
        updated_html_string = str(toc_div)
        serializer = TravelGuideSerializer(posts)
        return Response({
            "data":serializer.data,
            "toc":updated_html_string,
        })
    
@api_view(['GET'])
def recent_guides(request):
    if request.method == 'GET':
        posts = TravelGuide.objects.all()[:5]
        posts_serializer = TravelGuideSerializer(posts,many=True)
        return Response({
          "recent_guides":posts_serializer.data,
        })

