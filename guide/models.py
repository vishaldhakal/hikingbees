from django.db import models
from solo.models import SingletonModel
from tinymce import models as tinymce_models
from blog.models import Post
from activity.models import Activity
from blog.models import Author


class RegionWeatherPeriod(models.Model):
    MONTH_CHOICES = [
        ("January", "January"), ("February",
                                 "February"), ("March", "March"), ("April", "April"),
        ("May", "May"), ("June", "June"), ("July", "July"), ("August", "August"),
        ("September", "September"), ("October",
                                     "October"), ("November", "November"), ("December", "December"),
    ]
    region = models.ForeignKey(
        'TravelGuideRegion', on_delete=models.CASCADE, related_name='weather_periods', null=True, blank=True)
    start_month = models.CharField(
        max_length=50, choices=MONTH_CHOICES, null=True, blank=True)
    end_month = models.CharField(
        max_length=50, choices=MONTH_CHOICES, null=True, blank=True)
    high_temp = models.IntegerField(
        help_text="High temperature (°C)", null=True, blank=True)
    low_temp = models.IntegerField(
        help_text="Low temperature (°C)", null=True, blank=True)

    def __str__(self):
        return f"{self.start_month} - {self.end_month} ({self.region.title})"


class TravelGuideRegion(models.Model):
    title = models.CharField(max_length=200)
    short_description = tinymce_models.HTMLField(null=True, blank=True)
    description = tinymce_models.HTMLField(null=True, blank=True)
    blogs = models.ManyToManyField(
        Post, related_name='guide_region', blank=True)
    activities = models.ManyToManyField(
        Activity, related_name='guide_region', blank=True)
    slug = models.SlugField(blank=True)
    image = models.FileField(blank=True)
    image_alt_description = models.CharField(
        max_length=200, default="Alt Description")

    def __str__(self) -> str:
        return self.title


class TravelGuide(SingletonModel):
    thumbnail_image = models.FileField(blank=True)
    thumbnail_image_alt_description = models.CharField(max_length=300)
    guide_content = tinymce_models.HTMLField(blank=True)
    guide_region = models.ManyToManyField(
        TravelGuideRegion, related_name='guide_regions')
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()

    def __str__(self):
        return self.meta_title
