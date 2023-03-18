from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post,Tag,Category,BlogContent
from .serializers import PostSerializer,PostSmallSerializer,TagSerializer,CategorySerializer,TagSmallSerializer,CategorySmallSerializer,PostSlugSerializer

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
def post_single(request,slug):
    if request.method == 'GET':
        posts = Post.objects.get(slug=slug)
        serializer = PostSerializer(posts)
        return Response(serializer.data)