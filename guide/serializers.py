from rest_framework import serializers

from activity.serializers import LandingActivitySmallSerializer
from blog.serializers import AuthorSmallSerializer, LandingPagePostSerializer
from .models import TravelGuide, TravelGuideRegion, RegionWeatherPeriod
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup


class HTMLField(serializers.CharField):
    def to_representation(self, value):
        return str(BeautifulSoup(value, 'html.parser'))

    def to_internal_value(self, data):
        return data


class RegionWeatherPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionWeatherPeriod
        fields = '__all__'


class RegionWeatherPeriodSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionWeatherPeriod
        fields = ['start_month', 'end_month', 'high_temp', 'low_temp']


class TravelGuideRegionSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelGuideRegion
        fields = ['title', 'slug', 'image',
                  'image_alt_description', 'description']


class TravelGuideRegionSerializer(serializers.ModelSerializer):
    weather_periods = RegionWeatherPeriodSmallSerializer(
        many=True, read_only=True)
    blogs = LandingPagePostSerializer(many=True, read_only=True)
    activities = LandingActivitySmallSerializer(many=True, read_only=True)

    class Meta:
        model = TravelGuideRegion
        fields = '__all__'


class TravelGuideSerializer(serializers.ModelSerializer):
    guide_content = serializers.SerializerMethodField()
    guide_region = TravelGuideRegionSerializer(many=True, read_only=True)

    class Meta:
        model = TravelGuide
        fields = '__all__'
        depth = 2
        ordering = ['-created_at']

    def get_guide_content(self, obj):
        html_string = obj.guide_content
        soup = BeautifulSoup(html_string, 'html.parser')
        toc_div = soup.find('div', class_='mce-toc')
        if toc_div is not None:
            toc_div.extract()
        updated_html_string = str(soup)
        return mark_safe(updated_html_string)


class TravelGuideSmallSerializer(serializers.ModelSerializer):
    guide = AuthorSmallSerializer(read_only=True)

    class Meta:
        model = TravelGuide
        exclude = ['guide_region']
        depth = 1
