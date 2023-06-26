from django.contrib import admin
from .models import GuideAuthour,TravelGuide,TravelGuideCategory,TravelGuideRegion

admin.site.register(GuideAuthour)
admin.site.register(TravelGuide)
admin.site.register(TravelGuideCategory)
admin.site.register(TravelGuideRegion)
