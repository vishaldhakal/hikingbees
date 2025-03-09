from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post,Tag,Category
from .serializers import LandingPagePostSerializer, NavbarPostSerializer, PostSerializer,PostSmallSerializer,TagSerializer,CategorySerializer,TagSmallSerializer,CategorySmallSerializer,PostSlugSerializer
from bs4 import BeautifulSoup
from django.db import models
from rest_framework.pagination import PageNumberPagination
class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
def post_list(request):
    if request.method == 'GET':
        # Initialize paginator
        paginator = CustomPagination()
        
        # Get all posts and paginate them
        posts = Post.objects.all()
        paginated_posts = paginator.paginate_queryset(posts, request)
        
        # Serialize paginated posts
        posts_serializer = LandingPagePostSerializer(paginated_posts, many=True)

        # Get and serialize tags and categories
        tags = Tag.objects.all()
        categories = Category.objects.all()
        
        tag_serializer = TagSerializer(tags, many=True)
        categories_serializer = CategorySerializer(categories, many=True)

        return Response({
            "posts": posts_serializer.data,
            "tags": tag_serializer.data,
            "categories": categories_serializer.data,
            "total_pages": paginator.page.paginator.num_pages,
            "current_page": paginator.page.number,
            "total_items": paginator.page.paginator.count,
        })

@api_view(['GET'])
def post_list_slug(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSlugSerializer(posts, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def post_single(request,slug):
    if request.method == 'GET':
        posts = Post.objects.get(slug=slug)
        html_string = posts.blog_content
        soup = BeautifulSoup(html_string, 'html.parser')
        toc_div = soup.find('div', class_='mce-toc')
        if toc_div is not None:
            toc_div.extract()
        updated_html_string = str(toc_div)
        similar_posts = ( Post.objects .filter(tags__in=posts.tags.all()) .exclude(id=posts.id) .annotate( shared_tags=models.Count('tags', filter=models.Q(tags__in=posts.tags.all())) ) .order_by('-shared_tags', '-created_at') )[:5]
        serializer = PostSerializer(posts)
        similar_posts_serializer = NavbarPostSerializer(similar_posts, many=True)

        return Response({
            "data":serializer.data,
            "toc":updated_html_string,
            "similar_posts":similar_posts_serializer.data,
        })
    
@api_view(['GET'])
def recent_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()[:5]
        posts_serializer = LandingPagePostSerializer(posts,many=True)
        return Response({
          "recent_posts":posts_serializer.data,
        })

