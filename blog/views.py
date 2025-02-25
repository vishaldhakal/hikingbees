from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post,Tag,Category
from .serializers import LandingPagePostSerializer, NavbarPostSerializer, PostSerializer,PostSmallSerializer,TagSerializer,CategorySerializer,TagSmallSerializer,CategorySmallSerializer,PostSlugSerializer
from bs4 import BeautifulSoup
from django.db import models


@api_view(['GET'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        tags = Tag.objects.all()
        categories = Category.objects.all()
        serializer = PostSmallSerializer(posts, many=True)
        tag_serializer = TagSerializer(tags, many=True)
        categories_serializer = CategorySerializer(categories, many=True)
        return Response({
            "posts":serializer.data,
            "tags":tag_serializer.data,
            "categories":categories_serializer.data,
        })

@api_view(['GET'])
def post_list_slug(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSlugSerializer(posts, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def post_single(request, slug):
    if request.method == 'GET':
        post = Post.objects.get(slug=slug)
        # Get similar posts ranked by number of shared tags
        similar_posts = (
            Post.objects
            .filter(tags__in=post.tags.all())
            .exclude(id=post.id)
            .annotate(
                shared_tags=models.Count('tags', filter=models.Q(tags__in=post.tags.all()))
            )
            .order_by('-shared_tags', '-created_at')
        )[:5]
        
        post_serializer = PostSerializer(post)
        similar_posts_serializer = NavbarPostSerializer(similar_posts, many=True)
        
        return Response({
            "data": post_serializer.data,
            "similar_posts": similar_posts_serializer.data,
        })
    
@api_view(['GET'])
def recent_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()[:5]
        posts_serializer = LandingPagePostSerializer(posts,many=True)
        return Response({
          "recent_posts":posts_serializer.data,
        })

