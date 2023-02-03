from django.contrib import admin
from .models import ActivityCategory,Activity,ItineraryActivity,ActivityImage,Destination,ActivityRegion

class ItineraryActivityInline(admin.StackedInline):
    model = ItineraryActivity

class ActivityImageInline(admin.StackedInline):
    model = ActivityImage

class ActivityAdmin(admin.ModelAdmin):
    inlines = [
        ItineraryActivityInline,
        ActivityImageInline,
    ]
    
admin.site.register(Destination)
admin.site.register(ActivityCategory)
admin.site.register(Activity,ActivityAdmin)
admin.site.register(ItineraryActivity)
admin.site.register(ActivityImage)
admin.site.register(ActivityRegion)