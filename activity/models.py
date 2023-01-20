from django.db import models
from django_summernote.fields import SummernoteTextField

class Destination(models.Model):
     name = models.CharField(max_length=200)
     destination_detail = SummernoteTextField(blank=True)
     thumnail_image = models.ImageField(blank=True)
     thumnail_image_alt_description = models.CharField(max_length=200,default="Alt Description")

     def __str__(self) -> str:
          return self.name

class ActivityCategory(models.Model):
     name = models.CharField(max_length=200)
     description = SummernoteTextField(blank=True)
     thumnail_image = models.ImageField(blank=True)
     thumnail_image_alt_description = models.CharField(max_length=200,default="Alt Description")

     def __str__(self) -> str:
          return self.name

class Activity(models.Model):
    slug = models.CharField(max_length=200) 
    """ Auto Generate """
    activity_title = models.CharField(max_length=300)
    activity_category = models.ForeignKey(ActivityCategory,on_delete=models.DO_NOTHING)
    destination = models.ForeignKey(Destination,on_delete=models.DO_NOTHING)
    activity_location = models.CharField(max_length=300)
    contact_person_name = models.CharField(max_length=300)
    contact_person_phone = models.CharField(max_length=300)
    activity_duration = models.CharField(max_length=300)
    activity_price = models.CharField(max_length=300,default=0)
    activity_description = SummernoteTextField()
    activity_highlights = SummernoteTextField()
    """ List """
    activity_includes = SummernoteTextField()
    """ List """
    activity_excludes = SummernoteTextField()
    """ List """

    def __str__(self) -> str:
          return self.activity_title

class ActivityImage(models.Model):
    image = models.ImageField()
    image_alt_description = models.CharField(max_length=428,default="Image Description")
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='activityimage')

    def __str__(self) -> str:
          return self.image.url + ', '+self.image_alt_description
class ItineraryActivity(models.Model):
    activity_itineary_title = models.CharField(max_length=500)
    activity_itineary_description = models.TextField(max_length=128)
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name='activityitenary')

    def __str__(self) -> str:
          return self.activity_itineary_title
