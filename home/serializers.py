from rest_framework import serializers
from .models import HeroSectionContent,TeamMember,Testimonial

class HeroSectionContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSectionContent
        fields = '__all__'
        depth = 2

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'
        depth = 2

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
        depth = 2
