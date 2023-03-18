from rest_framework import serializers
from .models import Author, Category, Tag, Post,BlogContent
from bs4 import BeautifulSoup

class HTMLField(serializers.CharField):
    def to_representation(self, value):
        return str(BeautifulSoup(value, 'html.parser'))

    def to_internal_value(self, data):
        return data

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

class BlogContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogContent
        fields = ('id','order','title','description')
        depth = 1

class PostSerializer(serializers.ModelSerializer):
    blogcontent = BlogContentSerializer(many=True, read_only=True)
    blog_content = HTMLField()
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