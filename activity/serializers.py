from .models import Activity, ActivityTestimonialImage, ActivityPricing, ActivityBooking, ActivityEnquiry, ActivityCategory, ItineraryActivity, ActivityImage, Destination, ActivityRegion, ActivityFAQ, ActivityTestimonial, AddOns, ActivityBookingAddOn, Review, VideoReview, AdditionalTiles
from rest_framework import serializers


class ActivityEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityEnquiry
        fields = ('id',)
        depth = 1


class ActivityTestimonialImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityTestimonialImage
        fields = ('image',)
        depth = 1


class ActivityTestimonialSerializer(serializers.ModelSerializer):
    images = ActivityTestimonialImageSerializer(many=True)

    class Meta:
        model = ActivityTestimonial
        exclude = ('activity',)
        depth = 1


class ActivitySmallestSer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('activity_title', 'priceSale', 'slug',)
        depth = 1


class ActivityBooking2Serializer(serializers.ModelSerializer):
    activity = ActivitySmallestSer(read_only=True)

    class Meta:
        model = ActivityBooking
        fields = ('id', 'no_of_guests', 'booking_date', 'activity')
        depth = 1


class ActivityBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityBooking
        fields = ('id', 'no_of_guests', 'booking_date',)
        depth = 1


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
        depth = 2


class DestinationSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('id', 'name', 'thumnail_image',
                  'thumnail_image_alt_description')


class ActivityRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRegion
        fields = '__all__'
        depth = 1


class ActivityRegionSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRegion
        fields = ['id', 'title', 'slug', 'image', 'image_alt_description']
        depth = 1


class ActivityRegionSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRegion
        fields = ('id', 'slug')
        depth = 1


class LandingActivityRegionSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRegion
        fields = ['id', 'title', 'slug']
        depth = 1


class DestinationSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('name',)


class ActivityCategory2Serializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ('id', 'title', 'image', 'image_alt_description',
                  'subtitle', 'slug')
        depth = 2


class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = '__all__'
        depth = 2


class ActivityCategorySerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = '__all__'


class ActivityCategorySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ('id', 'title', 'slug')


class NavbarActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ('id', 'title', 'image', 'image_alt_description', 'slug')
        depth = 2


class LandingActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ('id', 'title', 'slug')


class ActivityCategorySlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ('id', 'slug')


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
    images = serializers.SerializerMethodField()

    class Meta:
        model = ItineraryActivity
        fields = [
            'id', 'day', 'title', 'trek_distance', 'trek_duration',
            'highest_altitude', 'meals', 'description', 'images'
        ]

    def get_images(self, obj):
        images = []
        for i in range(1, 5):  # For image_1 to image_4 as per the model
            image_field = f'image_{i}'
            image = getattr(obj, image_field, None)
            if image:
                alt_description = getattr(
                    obj, f'image_{i}_alt_description', '')
                images.append({
                    'url': self.context['request'].build_absolute_uri(image.url) if hasattr(self.context.get('request'), 'build_absolute_uri') and image.url else image.url,
                    'description': alt_description or ''
                })
        return images


class AddOnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOns
        fields = ('id', 'name', 'subtitle', 'price', 'unit')


class AdditionalTilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalTiles
        fields = '__all__'


class AdditionalTilesSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalTiles
        fields = ('id', 'title', 'description')


class LandingActivitySmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('id', 'slug', 'activity_title', 'duration', 'price',
                  'heroImg', 'coverImg', 'priceSale', 'ratings', 'banner_text')


class ActivitySerializer(serializers.ModelSerializer):
    itinerary = ItineraryActivitySerializer(many=True, read_only=True)
    gallery = ActivityImageSerializer(many=True, read_only=True)
    faqs = ActivityFAQSerializer(many=True, read_only=True)
    additional_tiles = AdditionalTilesSmallSerializer(
        many=True, read_only=True)
    enquiries = ActivityEnquirySerializer(many=True, read_only=True)
    testimonials = ActivityTestimonialSerializer(many=True, read_only=True)
    prices = ActivityPricingSerializer(many=True, read_only=True)
    add_ons_bookings = AddOnsSerializer(many=True, read_only=True)
    related_activities = LandingActivitySmallSerializer(
        many=True, read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'
        depth = 2


class ActivitySmallSerializer(serializers.ModelSerializer):
    destination = DestinationSerializerSmall()
    enquiries = ActivityEnquirySerializer(many=True, read_only=True)

    class Meta:
        model = Activity
        fields = ('id', 'slug', 'activity_title', 'activity_category', 'enquiries', 'location', 'duration', 'price',
                  'coverImg', 'ratings', 'popular', 'best_selling', 'destination', 'activity_region', 'priceSale', 'banner_text')
        depth = 1


class ActivitySearchSerializers(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ('id', 'slug', 'activity_title', 'duration', 'best_time',
                  'max_group_size', 'trip_grade', 'price', 'priceSale')


class LandingFavouriteActivitySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'slug', 'activity_title', 'heroImg',
                  'coverImg', 'location', 'banner_text')


class LandingBannerActivitySmallSerializer(serializers.ModelSerializer):
    activity_category = LandingActivityCategorySerializer(many=True)
    activity_region = LandingActivityRegionSmallSerializer()
    destination = DestinationSerializerSmall()

    class Meta:
        model = Activity
        fields = ('id', 'slug', 'activity_title', 'activity_category', 'location', 'duration',
                  'heroImg', 'coverImg', 'price', 'priceSale', 'ratings', 'activity_region', 'destination')
        depth = 1


class ActivitySmallestSerializer(serializers.ModelSerializer):
    destination = DestinationSerializerSmall()

    class Meta:
        model = Activity
        fields = ('id', 'slug', 'activity_title', 'destination', 'duration', 'price',
                  'priceSale', 'trip_grade', 'max_group_size', 'best_time', 'banner_text')
        depth = 1


class ClimbingActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'slug', 'activity_title', 'coverImg')


class ActivitySlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'slug')


class NavbarActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'slug', 'activity_title', 'coverImg')


class NavbarActivitySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'slug', 'activity_title')


class VideoReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoReview
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
