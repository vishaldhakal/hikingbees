from rest_framework import serializers
from .models import TeamMember,Testimonial,SiteConfiguration,Affiliations,Partners,TreekingNavDropdown,DestinationNavDropdown,OtherActivitiesNavDropdown,ClimbingNavDropdown,InnerDropdown
from activity.serializers import ActivityCategorySerializer,ActivitySerializer,ActivityRegionSerializer,DestinationSerializer

class InnerDropdownSerializer(serializers.ModelSerializer):
    activity_region = ActivityRegionSerializer()
    activites = ActivitySerializer(many=True)

    class Meta:
        model = InnerDropdown
        fields = '__all__'

class DestinationNavDropdownSerializer(serializers.ModelSerializer):
    destinations = DestinationSerializer(many=True)

    class Meta:
        model = DestinationNavDropdown
        fields = '__all__'

class OtherActivitiesNavDropdownSerializer(serializers.ModelSerializer):
    activity_categories = ActivityCategorySerializer(many=True)

    class Meta:
        model = OtherActivitiesNavDropdown
        fields = '__all__'

class ClimbingNavDropdownSerializer(serializers.ModelSerializer):
    
    innerdropdowns = InnerDropdownSerializer(many=True)

    class Meta:
        model = ClimbingNavDropdown
        fields = '__all__'

class TreekingNavDropdownSerializer(serializers.ModelSerializer):

    innerdropdowns = InnerDropdownSerializer(many=True)

    class Meta:
        model = TreekingNavDropdown
        fields = '__all__'



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
