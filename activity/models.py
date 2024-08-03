from django.db import models
from tinymce import models as tinymce_models

class Destination(models.Model):
     meta_title = models.CharField(max_length=200,blank=True)
     meta_description = models.TextField(blank=True)
     order = models.IntegerField(blank=True)
     name = models.CharField(max_length=200)
     destination_small_detail = models.TextField(blank=True)
     destination_detail = tinymce_models.HTMLField(blank=True)
     thumnail_image = models.FileField(blank=True)
     thumnail_image_alt_description = models.CharField(max_length=200,default="Alt Description")

     def __str__(self) -> str:
          return self.name
     
     class Meta:
        ordering = ('order','name',)

     

class ActivityCategory(models.Model):
     meta_title = models.CharField(max_length=200,blank=True)
     meta_description = models.TextField(blank=True)
     content = tinymce_models.HTMLField(blank=True)
     title = models.CharField(max_length=200)
     destination = models.ForeignKey(Destination,on_delete=models.DO_NOTHING)
     subtitle = models.TextField()
     image = models.FileField(blank=True)
     slug = models.SlugField(blank=True)
     image_alt_description = models.CharField(max_length=200,default="Alt Description")

     def __str__(self) -> str:
          return self.title

class ActivityRegion(models.Model):
     title = models.CharField(max_length=200)
     meta_title = models.CharField(max_length=200,blank=True)
     meta_description = models.TextField(blank=True)
     activity_category = models.ManyToManyField(ActivityCategory)
     content = tinymce_models.HTMLField(blank=True)
     slug = models.SlugField(blank=True)
     image = models.FileField(blank=True)
     image_alt_description = models.CharField(max_length=200,default="Alt Description")

     def __str__(self) -> str:
          return self.title

class Activity(models.Model):
    meta_title = models.CharField(max_length=200,blank=True)
    meta_description = models.TextField(blank=True)
    activity_category = models.ManyToManyField(ActivityCategory)
    activity_region = models.ForeignKey(ActivityRegion,on_delete=models.DO_NOTHING)
    destination = models.ForeignKey(Destination,on_delete=models.DO_NOTHING)
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


    class Meta:
        ordering = ['createdAt']

    def __str__(self) -> str:
          strrr = "["
          if self.popular:
            strrr+=" Popular "
          if self.best_selling:
            strrr+=" Best Selling "
          if self.featured:
            strrr+=" Featured "
          
          strrr+="]"
          return self.activity_title + strrr

class ActivityTestimonial(models.Model):
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='testimonials')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=500,blank=True)
    review = tinymce_models.HTMLField(blank=True)
    rating = models.FloatField(default=5)

    def __str__(self) -> str:
        return self.name
    
class ActivityTestimonialImage(models.Model):
    image = models.FileField()
    activity_testimonial = models.ForeignKey(ActivityTestimonial,on_delete=models.CASCADE,related_name='images')

    def __str__(self) -> str:
          return self.image.url
            
class ActivityEnquiry(models.Model):
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='enquiries')
    name = models.CharField(max_length=400)
    email = models.CharField(max_length=400)
    phone = models.CharField(max_length=400,blank=True,default=" ")
    message = models.TextField()

    def __str__(self):
        return self.name

class ActivityBooking(models.Model):
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='bookings')
    name = models.CharField(max_length=400)
    address = models.CharField(max_length=400)
    email = models.CharField(max_length=400)
    phone = models.CharField(max_length=400,blank=True)
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
    emergency_contact_name = models.CharField(max_length=400,blank=True)
    emergency_address = models.CharField(max_length=400,blank=True)
    emergency_phone = models.CharField(max_length=400,blank=True)
    emergency_email = models.CharField(max_length=400,blank=True)
    emergency_relationship = models.CharField(max_length=400,blank=True)

    def __str__(self):
        return "Booking for " + self.activity.activity_title

class ActivityFAQ(models.Model):
    question = tinymce_models.HTMLField(blank=True)
    answer = tinymce_models.HTMLField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='faqs')
    
    def __str__(self):
        return self.question
class ActivityPricing(models.Model):
    group_size = models.CharField(max_length=500)
    price = models.FloatField(max_length=1000)
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='prices')
    
    def __str__(self):
        return self.group_size

class ActivityImage(models.Model):
    image = models.FileField()
    image_alt_description = models.CharField(max_length=428,default="Image Description")
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='gallery')

    def __str__(self) -> str:
          return self.image.url + ', '+self.image_alt_description

class ItineraryActivity(models.Model):
    day = models.IntegerField()
    title = models.CharField(max_length=100)
    trek_distance = models.CharField(max_length=100,blank=True)
    trek_duration = models.CharField(max_length=100,blank=True)
    highest_altitude = models.CharField(max_length=100,blank=True)
    meals = models.CharField(max_length=100,blank=True)
    description = tinymce_models.HTMLField(blank=True)
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='itinerary')

    class Meta:
        ordering = ['day']

    def __str__(self) -> str:
          return self.title
