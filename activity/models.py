from django.db import models
from django_summernote.fields import SummernoteTextField

class Destination(models.Model):
     name = models.CharField(max_length=200)
     destination_small_detail = models.TextField(blank=True)
     destination_detail = SummernoteTextField(blank=True)
     thumnail_image = models.FileField(blank=True)
     thumnail_image_alt_description = models.CharField(max_length=200,default="Alt Description")

     def __str__(self) -> str:
          return self.name

class ActivityCategory(models.Model):
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
     activity_category = models.ManyToManyField(ActivityCategory)
     slug = models.SlugField(blank=True)
     image = models.FileField(blank=True)
     image_alt_description = models.CharField(max_length=200,default="Alt Description")

     def __str__(self) -> str:
          return self.title

class Activity(models.Model):
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
    tour_description = SummernoteTextField()
    tour_highlights = SummernoteTextField()
    tour_includes = SummernoteTextField()
    tour_excludes = SummernoteTextField()
    createdAt = models.DateTimeField(auto_created=True)
    availableStart = models.DateTimeField()
    availableEnd = models.DateTimeField()

    class Meta:
        ordering = ['createdAt']

    def __str__(self) -> str:
          return self.activity_title

class ActivityFAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
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
    description = models.TextField()
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='itinerary')

    class Meta:
        ordering = ['day']

    def __str__(self) -> str:
          return self.title
