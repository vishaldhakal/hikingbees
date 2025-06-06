from rest_framework import serializers

from activity.serializers import LandingActivitySmallSerializer
from .models import Author, Category, Tag, Post
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
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


class PostSerializer(serializers.ModelSerializer):
    blog_content = serializers.SerializerMethodField()
    related_activities = LandingActivitySmallSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'
        depth = 2
        ordering = ['-created_at']

    def get_blog_content(self, obj):
        html_string = obj.blog_content
        soup = BeautifulSoup(html_string, 'html.parser')
        toc_div = soup.find('div', class_='mce-toc')
        if toc_div is not None:
            toc_div.extract()
        updated_html_string = str(soup)
        return mark_safe(updated_html_string)


class PostSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['blog_content', 'related_activities']
        depth = 1
        ordering = ['-created_at']


class NavbarPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug')


class AuthorSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'picture', 'picture_alt_description')


class LandingPagePostSerializer(serializers.ModelSerializer):
    author = AuthorSmallSerializer()

    class Meta:
        model = Post
        fields = ('id', 'thumbnail_image', 'updated_at', 'created_at', 'blog_duration_to_read',
                  'slug', 'title', 'thumbnail_image_alt_description', 'author', 'meta_description')


class PostSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('slug',)
        depth = 1
