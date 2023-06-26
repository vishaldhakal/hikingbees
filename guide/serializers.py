from rest_framework import serializers
from .models import GuideAuthour,TravelGuide,TravelGuideCategory,TravelGuideRegion
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup

class HTMLField(serializers.CharField):
    def to_representation(self, value):
        return str(BeautifulSoup(value, 'html.parser'))

    def to_internal_value(self, data):
        return data

class GuideAuthourSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideAuthour
        fields = '__all__'
        depth = 2

class TravelGuideCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelGuideCategory
        fields = '__all__'
        depth = 2

class TravelGuideRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelGuideRegion
        fields = '__all__'
        depth = 2

class TravelGuideSerializer(serializers.ModelSerializer):
    blog_content = serializers.SerializerMethodField()
    guide_regions = TravelGuideRegionSerializer(many=True)
    guide_categories = TravelGuideCategorySerializer(many=True)
    class Meta:
        model = TravelGuide
        fields = '__all__'
        depth = 2
        ordering = ['-created_at']
    
    def get_blog_content(self, obj):
        html_string = obj.guide_content
        soup = BeautifulSoup(html_string, 'html.parser')
        toc_div = soup.find('div', class_='mce-toc')
        if toc_div is not None:
            toc_div.extract()
        updated_html_string = str(soup)
        return mark_safe(updated_html_string)

class TravelGuideSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelGuide
        exclude = ['guide_content']
        depth = 1
        ordering = ['-created_at']

class TravelGuideSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelGuide
        fields = ('slug',)
        depth = 1