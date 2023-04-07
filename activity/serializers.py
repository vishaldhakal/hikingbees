from .models import Activity,ActivityPricing,ActivityBooking,ActivityEnquiry,ActivityCategory,ItineraryActivity,ActivityImage,Destination,ActivityRegion,ActivityFAQ
from rest_framework import serializers

class ActivityEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityEnquiry
        fields = ('id',)
        depth = 1

class ActivityBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityBooking
        fields = ('id','no_of_guests','booking_date',)
        depth = 1

    def to_representation(self, instance):
        # Retrieve the default representation of the instance
        data = super().to_representation(instance)

        # Group activity bookings with the same booking date
        booking_date = data['booking_date']
        if booking_date in self.context.get('booking_dates', {}):
            self.context['booking_dates'][booking_date]['bookings'].append(data)
        else:
            self.context['booking_dates'][booking_date] = {
                'date': booking_date,
                'bookings': [data]
            }

        return None  # Return None to exclude this instance from the response

    def to_internal_value(self, data):
        # Override to_internal_value to exclude the 'bookings' key from the request data
        data.pop('bookings', None)
        return super().to_internal_value(data)
    
class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
        depth = 2

class ActivityRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRegion
        fields = '__all__'
        depth = 1

class ActivityRegionSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRegion
        fields = ('id','slug')
        depth = 1

class DestinationSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('name',)

class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = '__all__'
        depth = 2

class ActivityCategorySlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ('id','slug')

class ActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityImage
        fields = '__all__'

class ActivityPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityPricing
        fields = '__all__'

class ActivityFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityFAQ
        fields = '__all__'

class ItineraryActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryActivity
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    itinerary = ItineraryActivitySerializer(many=True, read_only=True)
    gallery = ActivityImageSerializer(many=True,read_only=True)
    faqs = ActivityFAQSerializer(many=True,read_only=True)
    enquiries = ActivityEnquirySerializer(many=True,read_only=True)
    bookings = ActivityBookingSerializer(many=True,read_only=True)
    prices = ActivityPricingSerializer(many=True,read_only=True)
    
    class Meta:
        model = Activity
        fields = '__all__'
        depth = 2

class ActivitySmallSerializer(serializers.ModelSerializer):
    destination = DestinationSerializerSmall()
    enquiries = ActivityEnquirySerializer(many=True,read_only=True)
    class Meta:
        model = Activity
        fields = ('id','slug', 'activity_title', 'activity_category','enquiries','location','duration','price','coverImg','ratings','popular','best_selling','destination','activity_region','priceSale')
        depth = 1

class ActivitySmallestSerializer(serializers.ModelSerializer):
    destination = DestinationSerializerSmall()
    class Meta:
        model = Activity
        fields = ('id','slug', 'activity_title','destination','duration','price','priceSale','trip_grade','max_group_size','best_time')
        depth = 1

class ActivitySlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id','slug')