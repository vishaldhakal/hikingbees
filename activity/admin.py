from django.contrib import admin
from .models import ActivityCategory,ActivityPricing,Activity,ItineraryActivity,ActivityImage,Destination,ActivityRegion,ActivityFAQ

class ItineraryActivityInline(admin.StackedInline):
    model = ItineraryActivity

class ActivityFAQInline(admin.StackedInline):
    model = ActivityFAQ

class ActivityImageInline(admin.StackedInline):
    model = ActivityImage

class ActivityPricingInline(admin.StackedInline):
    model = ActivityPricing

class ActivityAdmin(admin.ModelAdmin):
    inlines = [
        ItineraryActivityInline,
        ActivityImageInline,
        ActivityFAQInline,
        ActivityPricingInline,
    ]
    
admin.site.register(Destination)
admin.site.register(ActivityCategory)
admin.site.register(Activity,ActivityAdmin)
admin.site.register(ItineraryActivity)
admin.site.register(ActivityImage)
admin.site.register(ActivityFAQ)
admin.site.register(ActivityPricing)
admin.site.register(ActivityRegion)