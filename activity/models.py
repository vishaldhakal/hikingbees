from django.db import models
from tinymce import models as tinymce_models


class Destination(models.Model):
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    order = models.IntegerField(blank=True)
    name = models.CharField(max_length=200)
    destination_small_detail = models.TextField(blank=True)
    destination_detail = tinymce_models.HTMLField(blank=True)
    thumnail_image = models.FileField(blank=True)
    thumnail_image_alt_description = models.CharField(
        max_length=200, default="Alt Description"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = (
            "order",
            "name",
        )


class ActivityCategory(models.Model):
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    content = tinymce_models.HTMLField(blank=True)
    title = models.CharField(max_length=200)
    destination = models.ForeignKey(Destination, on_delete=models.DO_NOTHING)
    subtitle = models.TextField()
    image = models.FileField(blank=True)
    slug = models.SlugField(blank=True)
    image_alt_description = models.CharField(max_length=200, default="Alt Description")

    def __str__(self) -> str:
        return self.title


class ActivityRegion(models.Model):
    title = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    activity_category = models.ManyToManyField(ActivityCategory)
    content = tinymce_models.HTMLField(blank=True)
    slug = models.SlugField(blank=True)
    image = models.FileField(blank=True)
    image_alt_description = models.CharField(max_length=200, default="Alt Description")
    order = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Activity(models.Model):
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    activity_category = models.ManyToManyField(ActivityCategory)
    activity_region = models.ForeignKey(ActivityRegion, on_delete=models.DO_NOTHING)
    destination = models.ForeignKey(Destination, on_delete=models.DO_NOTHING)
    activity_title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=100)
    price = models.FloatField()
    heroImg = models.FileField()
    ratings = models.FloatField()
    coverImg = models.FileField()
    location = models.CharField(max_length=500)
    duration = models.CharField(max_length=500)
    trip_grade = models.CharField(max_length=500)
    max_group_size = models.CharField(max_length=500)
    best_time = models.CharField(max_length=500)
    priceSale = models.FloatField()
    popular = models.BooleanField()
    best_selling = models.BooleanField()
    featured = models.BooleanField(default=False)
    tour_description = tinymce_models.HTMLField()
    tour_highlights = tinymce_models.HTMLField()
    tour_includes = tinymce_models.HTMLField()
    tour_excludes = tinymce_models.HTMLField()
    createdAt = models.DateTimeField(auto_created=True)
    availableStart = models.DateTimeField()
    availableEnd = models.DateTimeField()
    trek_map = models.FileField(blank=True)
    altitude_chart = models.FileField(blank=True)
    additional_info = tinymce_models.HTMLField(blank=True)
    banner_text = models.CharField(max_length=120, blank=True, null=True)
    pdf_url = models.CharField(max_length=120, blank=True, null=True)
    related_activities = models.ManyToManyField("self", blank=True, symmetrical=True)
    per_day_walk = models.CharField(max_length=120, blank=True, null=True)
    add_on_description = tinymce_models.HTMLField(null=True, blank=True)

    class Meta:
        ordering = ["createdAt"]

    def __str__(self) -> str:
        strrr = "["
        if self.popular:
            strrr += " Popular "
        if self.best_selling:
            strrr += " Best Selling "
        if self.featured:
            strrr += " Featured "

        strrr += "]"
        return self.activity_title + strrr


class ActivityTestimonial(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="testimonials"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=500, blank=True)
    review = tinymce_models.HTMLField(blank=True)
    rating = models.FloatField(default=5)

    def __str__(self) -> str:
        return self.name


class ActivityTestimonialImage(models.Model):
    image = models.FileField()
    activity_testimonial = models.ForeignKey(
        ActivityTestimonial, on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self) -> str:
        return self.image.url


class ActivityEnquiry(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="enquiries"
    )
    name = models.CharField(max_length=400)
    email = models.CharField(max_length=400)
    phone = models.CharField(max_length=400, blank=True, default=" ")
    message = models.TextField()

    def __str__(self):
        return self.name


class AddOns(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="add_ons_bookings"
    )
    name = models.CharField(max_length=400)
    subtitle = models.CharField(max_length=400, null=True, blank=True)
    price = models.FloatField()
    unit = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.name} - {self.price}"


class ActivityBooking(models.Model):
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="bookings"
    )
    name = models.CharField(max_length=400)
    address = models.CharField(max_length=400)
    email = models.CharField(max_length=400)
    phone = models.CharField(max_length=400, blank=True)
    message = models.TextField(blank=True)
    no_of_guests = models.IntegerField()
    total_price = models.FloatField()
    is_private = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    booking_date = models.DateTimeField()
    arrival_date = models.DateTimeField(null=True)
    departure_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    emergency_contact_name = models.CharField(max_length=400, blank=True)
    emergency_address = models.CharField(max_length=400, blank=True)
    emergency_phone = models.CharField(max_length=400, blank=True)
    emergency_email = models.CharField(max_length=400, blank=True)
    emergency_relationship = models.CharField(max_length=400, blank=True)
    add_ons = models.ManyToManyField(AddOns, through="ActivityBookingAddOn", blank=True)

    def __str__(self):
        return "Booking for " + self.activity.activity_title


class ActivityBookingAddOn(models.Model):
    booking = models.ForeignKey(
        ActivityBooking, on_delete=models.CASCADE, related_name="booking_addons"
    )
    addon = models.ForeignKey(AddOns, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.booking.name} - {self.addon.name} x{self.quantity}"


class AdditionalTiles(models.Model):
    title = models.CharField(max_length=255)
    description = tinymce_models.HTMLField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="additional_tiles"
    )

    def __str__(self):
        return self.title


class ActivityFAQCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "FAQ Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class ActivityFAQ(models.Model):
    category = models.ForeignKey(
        ActivityFAQCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faqs",
    )
    question = models.TextField()
    answer = tinymce_models.HTMLField()
    activities = models.ManyToManyField(Activity, related_name="faqs", blank=True)
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Activity FAQs"
        ordering = ["category__order", "order", "created_at"]

    def __str__(self):
        return self.question


class ActivityPricing(models.Model):
    group_size = models.CharField(max_length=500)
    price = models.FloatField(max_length=1000)
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="prices"
    )

    def __str__(self):
        return self.group_size


class ActivityImage(models.Model):
    image = models.FileField()
    image_alt_description = models.CharField(
        max_length=428, default="Image Description"
    )
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="gallery"
    )

    def __str__(self) -> str:
        return self.image.url + ", " + self.image_alt_description


class ItineraryActivity(models.Model):
    day = models.IntegerField()
    title = models.CharField(max_length=100)
    trek_distance = models.CharField(max_length=100, blank=True)
    trek_duration = models.CharField(max_length=100, blank=True)
    highest_altitude = models.CharField(max_length=100, blank=True)
    meals = models.CharField(max_length=100, blank=True)
    description = tinymce_models.HTMLField(blank=True)
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="itinerary"
    )
    image_1 = models.FileField(upload_to="itinerary_images/", blank=True, null=True)
    image_1_alt_description = models.CharField(max_length=428, null=True, blank=True)
    image_2 = models.FileField(upload_to="itinerary_images/", blank=True, null=True)
    image_2_alt_description = models.CharField(max_length=428, null=True, blank=True)
    image_3 = models.FileField(upload_to="itinerary_images/", blank=True, null=True)
    image_3_alt_description = models.CharField(max_length=428, null=True, blank=True)
    image_4 = models.FileField(upload_to="itinerary_images/", blank=True, null=True)
    image_4_alt_description = models.CharField(max_length=428, null=True, blank=True)

    class Meta:
        ordering = ["day"]

    def __str__(self) -> str:
        return self.title


class VideoReview(models.Model):
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, null=True, blank=True)
    thumbnail_image = models.FileField(null=True, blank=True)
    thumbnail_image_alt_description = models.CharField(
        max_length=428, default="Image Description", null=True, blank=True
    )
    video_url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    trip_advisor_review = models.IntegerField(null=True, blank=True)
    google_review = models.IntegerField(null=True, blank=True)
    google_rating = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Trip Advisor: {self.trip_advisor_review} - Google: {self.google_review} - Google Rating: {self.google_rating}"
