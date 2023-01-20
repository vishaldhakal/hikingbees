from .models import Activity,ActivityCategory,ItineraryActivity,ActivityImage,Destination
from rest_framework import serializers

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
        depth = 2

class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = '__all__'
        depth = 2

class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityImage
        fields = '__all__'

class ItineraryActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryActivity
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    activityitenary = ItineraryActivitySerializer(many=True, read_only=True)
    activityimage = ActivityImageSerializer(many=True,read_only=True)
    
    class Meta:
        model = Activity
        fields = '__all__'
        depth = 2

class ActivitySmallSerializer(serializers.ModelSerializer):
    activityimage = serializers.StringRelatedField(many=True,read_only=True)
    
    class Meta:
        model = Activity
        fields = ('slug', 'activity_title', 'activity_category','activity_location','activity_duration','activity_price','activityimage')
        depth = 1