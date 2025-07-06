from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TravelGuide, TravelGuideRegion
from .serializers import TravelGuideRegionSmallSerializer, TravelGuideSerializer, TravelGuideSmallSerializer, TravelGuideRegionSerializer
from bs4 import BeautifulSoup


@api_view(['GET'])
def guide_list(request):
    if request.method == 'GET':
        posts = TravelGuide.objects.all()
        serializer = TravelGuideSmallSerializer(posts, many=True)
        regions = TravelGuideRegion.objects.filter(
            guide_regions__isnull=False).distinct()
        regions_serializer = TravelGuideRegionSmallSerializer(
            regions, many=True)
        return Response({
            "guides": serializer.data,
            "regions": regions_serializer.data,
        })


@api_view(['GET'])
def guide_region(request, slug):
    if request.method == 'GET':
        try:
            posts = TravelGuideRegion.objects.get(slug=slug)
        except TravelGuideRegion.DoesNotExist:
            return Response({"error": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

        # Handle case where description is None
        if posts.description is not None:
            html_string = posts.description
            soup = BeautifulSoup(html_string, 'html.parser')
            toc_div = soup.find('div', class_='mce-toc')
            if toc_div is not None:
                toc_div.extract()
            updated_html_string = str(soup)  # Use soup instead of toc_div
        else:
            updated_html_string = ""

        serializer = TravelGuideRegionSerializer(posts)
        return Response({
            "data": serializer.data,
            "toc": updated_html_string,
        })


@api_view(['GET'])
def recent_guides(request):
    if request.method == 'GET':
        posts = TravelGuide.objects.all()[:5]
        posts_serializer = TravelGuideSerializer(posts, many=True)
        return Response({
            "recent_guides": posts_serializer.data,
        })
