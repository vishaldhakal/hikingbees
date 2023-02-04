from django.db import models

class HeroSectionContent(models.Model):
    hero_section_title = models.CharField(max_length=328,default="Welcome to Hiking Bees : Your Ultimate Guide to Exploring the Great Outdoors")
    hero_section_subtitle = models.CharField(max_length=328,default="Discover The Best Hiking Trails And Bee-Watching Spots On Your Next Adventure. Book A Trip Now")
    hero_section_image = models.ImageField(blank=True)

    def __str__(self) -> str:
        return "Hero Section"


class TeamMember(models.Model):
    name = models.CharField(max_length=200,blank=True)
    role = models.CharField(max_length=200,blank=True)
    photo = models.ImageField(blank=True)
    facebook = models.URLField(max_length=200,blank=True) 
    instagram = models.URLField(max_length=200,blank=True)
    linkedin = models.URLField(max_length=200,blank=True)
    twitter = models.URLField(max_length=200,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Testimonial(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200,blank=True)
    avatar = models.ImageField(blank=True)
    role = models.CharField(max_length=200,blank=True)
    review = models.TextField(blank=True)
    rating = models.FloatField(default=5)

    def __str__(self) -> str:
        return self.name

