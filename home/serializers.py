from rest_framework import serializers
from .models import TeamMember,Testimonial,SiteConfiguration,Affiliations,Partners

class SiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'
        depth = 1
class AffiliationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliations
        fields = '__all__'
        depth = 2

class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
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
