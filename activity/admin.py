from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from .models import *
from tinymce.widgets import TinyMCE
from django import forms
from django.utils import timezone

class DestinationAdminForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'
        widgets = {
            'destination_detail': TinyMCE(),
        }

class ActivityCategoryAdminForm(forms.ModelForm):
    class Meta:
        model = ActivityCategory
        fields = '__all__'
        widgets = {
            'content': TinyMCE(),
        }

class ActivityRegionAdminForm(forms.ModelForm):
    class Meta:
        model = ActivityRegion
        fields = '__all__'
        widgets = {
            'content': TinyMCE(),
        }

class ActivityAdminForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        widgets = {
            'tour_description': TinyMCE(),
            'tour_highlights': TinyMCE(),
            'tour_includes': TinyMCE(),
            'tour_excludes': TinyMCE(),
            'additional_info': TinyMCE(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # If this is a new instance
            self.instance.createdAt = timezone.now()

class ActivityTestimonialForm(forms.ModelForm):
    class Meta:
        model = ActivityTestimonial
        fields = '__all__'
        widgets = {
            'review': TinyMCE(),
        }

class ActivityFAQForm(forms.ModelForm):
    class Meta:
        model = ActivityFAQ
        fields = '__all__'
        widgets = {
            'question': TinyMCE(),
            'answer': TinyMCE(),
        }

class ItineraryActivityForm(forms.ModelForm):
    class Meta:
        model = ItineraryActivity
        fields = '__all__'
        widgets = {
            'description': TinyMCE(),
        }

class ItineraryActivityInline(StackedInline):
    model = ItineraryActivity
    form = ItineraryActivityForm

class ActivityFAQInline(StackedInline):
    model = ActivityFAQ
    form = ActivityFAQForm

class ActivityImageInline(StackedInline):
    model = ActivityImage

class ActivityTestimonialImageInline(StackedInline):
    model = ActivityTestimonialImage

class ActivityPricingInline(StackedInline):
    model = ActivityPricing

class DestinationAdmin(ModelAdmin):
    form = DestinationAdminForm

class ActivityCategoryAdmin(ModelAdmin):
    form = ActivityCategoryAdminForm

class ActivityRegionAdmin(ModelAdmin):
    form = ActivityRegionAdminForm

class ActivityAdmin(ModelAdmin):
    form = ActivityAdminForm
    inlines = [
        ItineraryActivityInline,
        ActivityImageInline,
        ActivityFAQInline,
        ActivityPricingInline,
    ]
    list_display = (
        "__str__",
        "price",
        "createdAt",
        "featured",
        "best_selling",
        "popular",
    )
    list_filter = ("featured","best_selling","popular","destination")

    fieldsets = (
        ("Basic Information", {
            "fields": (
                ("activity_title", "slug"),
                ("destination", "activity_category", "activity_region"),
                ("price", "priceSale"),
                ("popular", "best_selling", "featured"),
            )
        }),
        ("Meta Information", {
            "fields": (
                "meta_title",
                "meta_description"
            )
        }),
        ("Tour Details", {
            "fields": (
                "heroImg",
                "coverImg",
                "location",
                "duration",
                "trip_grade",
                "max_group_size",
                "best_time",
                "ratings",
                "availableStart",
                "availableEnd",
                "trek_map",
                "altitude_chart",
            )
        }),
        ("Tour Description", {
            "fields": (
                "tour_description",
                "tour_highlights",
                "tour_includes",
                "tour_excludes",
                "additional_info",
            )
        }),
    )

class ActivityTestimonialAdmin(ModelAdmin):
    form = ActivityTestimonialForm
    inlines = [ActivityTestimonialImageInline]

class ActivityFAQAdmin(ModelAdmin):
    form = ActivityFAQForm

class ItineraryActivityAdmin(ModelAdmin):
    form = ItineraryActivityForm

# Register all models with their respective admin classes
admin.site.register(Destination, DestinationAdmin)
admin.site.register(ActivityCategory, ActivityCategoryAdmin)
admin.site.register(ActivityRegion, ActivityRegionAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ItineraryActivity, ItineraryActivityAdmin)
admin.site.register(ActivityImage, ModelAdmin)
admin.site.register(ActivityFAQ, ActivityFAQAdmin)
admin.site.register(ActivityPricing, ModelAdmin)
admin.site.register(ActivityEnquiry, ModelAdmin)
admin.site.register(ActivityTestimonial, ActivityTestimonialAdmin)

class ActivityBookingAdmin(ModelAdmin):
    list_display = (
        "__str__",
        "name",
        "booking_date",
        "is_private",
        "is_verified",
    )
    list_filter = ("is_private", "is_verified", "booking_date","activity")

admin.site.register(ActivityBooking, ActivityBookingAdmin)