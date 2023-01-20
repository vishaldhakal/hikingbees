from rest_framework import serializers
from .models import Author, Category, Tag, Post

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        depth = 2

class CategorySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_name',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 2

class TagSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_name',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        depth = 2

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        depth = 2

class PostSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        depth = 1

class PostSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('slug',)
        depth = 1