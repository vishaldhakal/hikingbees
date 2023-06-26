from django.db import models
from tinymce import models as tinymce_models


class GuideAuthour(models.Model):
    name = models.CharField(max_length=200) 
    role = models.CharField(max_length=200,default="Travel Guide")
    phone = models.CharField(max_length=200)
    picture = models.FileField()
    about = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class TravelGuide(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=300)
    title = models.CharField(max_length=500)
    guide_duration_to_read = models.CharField(max_length=100,blank=True)
    thumbnail_image = models.FileField()
    thumbnail_image_alt_description = models.CharField(max_length=300)
    guide_content = tinymce_models.HTMLField(blank=True)
    guide = models.ForeignKey(GuideAuthour, on_delete=models.DO_NOTHING)
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()
    name = models.CharField(max_length=200) 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

