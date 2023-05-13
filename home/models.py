from django.db import models
from solo.models import SingletonModel
from activity.models import Activity,ActivityCategory,Destination,ActivityRegion
from tinymce import models as tinymce_models

class NewsletterSubscription(models.Model):
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.email
    
class LegalDocument(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.FileField()
    image_alt_description = models.CharField(max_length=300)

    def __str__(self):
        return self.title
    
class FAQCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE)
    question = models.TextField(max_length=500)
    answer = models.TextField(max_length=1000)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.question

class DestinationNavDropdown(SingletonModel):
    destinations = models.ManyToManyField(Destination,blank=True)

    def __str__(self) -> str:
        return "Destinations Nav Config"
class OtherActivitiesNavDropdown(SingletonModel):
    activity_categories = models.ManyToManyField(ActivityCategory,blank=True)

    def __str__(self) -> str:
        return "Destinations Nav Config"

class InnerDropdown(models.Model):
    activity_region = models.ForeignKey(ActivityRegion,on_delete=models.DO_NOTHING)
    activites = models.ManyToManyField(Activity,blank=True)

    def __str__(self) -> str:
        return self.activity_region.title
class ClimbingNavDropdown(SingletonModel):
    innerdropdowns = models.ManyToManyField(InnerDropdown,blank=True)

    def __str__(self) -> str:
        return "Climbing Nav Config"

class TreekingNavDropdown(SingletonModel):
    innerdropdowns = models.ManyToManyField(InnerDropdown,blank=True)

    def __str__(self) -> str:
        return "Treeking Nav Config"

class FeaturedTour(SingletonModel):
    featured_tours = models.ManyToManyField(Activity,blank=True,limit_choices_to={'featured': True},related_name="featured_tours")
    popular_tours = models.ManyToManyField(Activity,blank=True,limit_choices_to={'popular': True},related_name="popular_tours")
    best_selling_tours = models.ManyToManyField(Activity,blank=True,limit_choices_to={'best_selling': True},related_name="best_selling_tours")
    favourite_tours = models.ManyToManyField(Activity,blank=True,related_name="favourite_tours")
    banner_tour = models.ManyToManyField(Activity,blank=True,related_name="banner_tour")

    def __str__(self) -> str:
        return "Featured, Popular and Best Selling Tours"

class SiteConfiguration(SingletonModel):
    meta_title = models.CharField(max_length=200,default="Meta Title Landing Page")
    meta_description = models.TextField(default="Meta Description Landing Page")
    hero_title_line1 = models.CharField(max_length=328,default="Line 1")
    hero_title_line2 = models.CharField(max_length=328,default="Line 2")
    hero_title_line3 = models.CharField(max_length=328,default="Line 3")
    hero_section_subtitle = models.TextField(default="Discover The Best Hiking Trails And Bee-Watching Spots On Your Next Adventure. Book A Trip Now")
    hero_section_image = models.FileField(blank=True)

    def __str__(self):
        return "Site Configuration"
    class Meta:
        verbose_name = "Site Configuration"

class TeamMember(models.Model):
    TEAM_CHOICES = (
    ("Executive Team", "Executive Team"),
    ("Representative", "Representative"),
    ("Trekking Guides", "Trekking Guides"),
    ("Tour Guide", "Tour Guide"),
    )
    order = models.IntegerField(blank=True)
    name = models.CharField(max_length=200,blank=True)
    role = models.CharField(max_length=200,blank=True)
    photo = models.FileField(blank=True)
    about = tinymce_models.HTMLField(blank=True)
    type = models.CharField(max_length=300,choices=TEAM_CHOICES,default="Representative")
    email = models.CharField(max_length=200) 
    facebook = models.URLField(max_length=200,blank=True) 
    instagram = models.URLField(max_length=200,blank=True)
    linkedin = models.URLField(max_length=200,blank=True)
    twitter = models.URLField(max_length=200,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ('order','name',)

class Testimonial(models.Model):

    SOURCE_CHOICES = (
    ("Trip Advisor", "Trip Advisor"),
    ("Trust Pilot", "Trust Pilot"),
    ("Google", "Google"),
    ("Others", "Others"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200,blank=True)
    avatar = models.FileField(blank=True)
    role = models.CharField(max_length=200,blank=True)
    title = models.CharField(max_length=500,blank=True)
    source = models.CharField(max_length=200,choices=SOURCE_CHOICES,default="Others")
    review = models.TextField(blank=True)
    rating = models.FloatField(default=5)

    def __str__(self) -> str:
        return self.name

class Affiliations(models.Model):
    name = models.CharField(max_length=200)
    link_to_website = models.URLField(blank=True)
    image = models.FileField()

    def __str__(self) -> str:
        return self.name
class Partners(models.Model):
    name = models.CharField(max_length=200)
    link_to_website = models.URLField(blank=True)
    image = models.FileField()

    def __str__(self) -> str:
        return self.name

class Enquiry(models.Model):
    name = models.CharField(max_length=500,blank=True)
    phone = models.CharField(max_length=500,blank=True)
    email = models.CharField(max_length=500,blank=True)
    message = models.CharField(max_length=500,blank=True)
    date = models.DateTimeField(auto_now_add=True)
