from django import forms
from django.contrib import admin
from django.utils import timezone
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin, StackedInline

from .models import *


class DestinationAdminForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = "__all__"
        widgets = {
            "destination_detail": TinyMCE(),
        }


class ActivityCategoryAdminForm(forms.ModelForm):
    class Meta:
        model = ActivityCategory
        fields = "__all__"
        widgets = {
            "content": TinyMCE(),
        }


class ActivityRegionAdminForm(forms.ModelForm):
    class Meta:
        model = ActivityRegion
        fields = "__all__"
        widgets = {
            "content": TinyMCE(),
        }


class ActivityAdminForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = "__all__"
        widgets = {
            "tour_description": TinyMCE(),
            "tour_highlights": TinyMCE(),
            "tour_includes": TinyMCE(),
            "tour_excludes": TinyMCE(),
            "additional_info": TinyMCE(),
            "add_on_description": TinyMCE(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # If this is a new instance
            self.instance.createdAt = timezone.now()


class ActivityTestimonialForm(forms.ModelForm):
    class Meta:
        model = ActivityTestimonial
        fields = "__all__"
        widgets = {
            "review": TinyMCE(),
        }


class ActivityFAQForm(forms.ModelForm):
    class Meta:
        model = ActivityFAQ
        fields = "__all__"
        widgets = {
            "answer": TinyMCE(),
        }


class ItineraryActivityForm(forms.ModelForm):
    class Meta:
        model = ItineraryActivity
        fields = "__all__"
        widgets = {
            "description": TinyMCE(),
        }


class ItineraryActivityInline(StackedInline):
    model = ItineraryActivity
    form = ItineraryActivityForm
    tab = True


class ActivityFAQInline(StackedInline):
    model = ActivityFAQ.activities.through
    extra = 1
    verbose_name = "Activity FAQ"
    verbose_name_plural = "Activity FAQs"
    autocomplete_fields = ["activityfaq"]
    tab = True


class ActivityImageInline(StackedInline):
    model = ActivityImage
    tab = True


class ActivityTestimonialImageInline(StackedInline):
    model = ActivityTestimonialImage
    tab = True


class AdditionalTilesForm(forms.ModelForm):
    class Meta:
        model = AdditionalTiles
        fields = "__all__"
        widgets = {
            "description": TinyMCE(),
        }


class AdditionalTilesInline(StackedInline):
    model = AdditionalTiles
    form = AdditionalTilesForm
    tab = True
    extra = 1


class ActivityPricingInline(StackedInline):
    model = ActivityPricing
    tab = True


class AddOnsInline(StackedInline):
    model = AddOns
    tab = True


class DestinationAdmin(ModelAdmin):
    form = DestinationAdminForm


class ActivityCategoryAdmin(ModelAdmin):
    form = ActivityCategoryAdminForm


class ActivityRegionAdmin(ModelAdmin):
    form = ActivityRegionAdminForm


class ActivityAdmin(ModelAdmin):
    form = ActivityAdminForm
    list_display = (
        "__str__",
        "price",
        "createdAt",
        "featured",
        "best_selling",
        "popular",
    )
    search_fields = ("activity_title", "location", "meta_title")
    list_filter = ("featured", "best_selling", "popular", "destination")

    inlines = [
        ItineraryActivityInline,
        ActivityImageInline,
        ActivityFAQInline,
        ActivityPricingInline,
        AddOnsInline,
        AdditionalTilesInline,
    ]

    fieldsets = (
        (
            "Basic Information",
            {
                "classes": ["tab"],
                "fields": [
                    ("activity_title", "slug"),
                    ("destination", "activity_category", "activity_region"),
                    ("price", "priceSale", "banner_text"),
                    ("popular", "best_selling", "featured"),
                    ("related_activities"),
                    ("pdf_url",),
                ],
            },
        ),
        (
            "Meta Information",
            {
                "classes": ["tab"],
                "fields": ["meta_title", "meta_description"],
            },
        ),
        (
            "Tour Details",
            {
                "classes": ["tab"],
                "fields": [
                    (
                        "heroImg",
                        "coverImg",
                    ),
                    ("location", "duration", "per_day_walk"),
                    (
                        "trip_grade",
                        "max_group_size",
                    ),
                    (
                        "best_time",
                        "ratings",
                    ),
                    (
                        "availableStart",
                        "availableEnd",
                    ),
                ],
            },
        ),
        (
            "Map & Chart",
            {
                "classes": ["tab"],
                "fields": [
                    "trek_map",
                    "altitude_chart",
                ],
            },
        ),
        (
            "Tour Description",
            {
                "classes": ["tab"],
                "fields": [
                    "tour_description",
                    "tour_highlights",
                    "tour_includes",
                    "tour_excludes",
                    "additional_info",
                    "add_on_description",
                ],
            },
        ),
    )


class ActivityTestimonialAdmin(ModelAdmin):
    form = ActivityTestimonialForm
    inlines = [ActivityTestimonialImageInline]


class ActivityFAQCategoryAdmin(ModelAdmin):
    list_display = ["name", "slug", "order", "active"]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["active"]
    ordering = ["order", "name"]


class ActivityFAQAdmin(ModelAdmin):
    form = ActivityFAQForm
    list_display = ["question", "category", "order", "active"]
    list_filter = ["category", "active"]
    search_fields = ["question", "answer"]
    filter_horizontal = ["activities"]
    ordering = ["order", "category"]


class ItineraryActivityAdmin(ModelAdmin):
    form = ItineraryActivityForm


# Register all models with their respective admin classes
admin.site.register(Destination, DestinationAdmin)
admin.site.register(ActivityCategory, ActivityCategoryAdmin)
admin.site.register(ActivityRegion, ActivityRegionAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ItineraryActivity, ItineraryActivityAdmin)
admin.site.register(ActivityImage, ModelAdmin)
admin.site.register(ActivityFAQCategory, ActivityFAQCategoryAdmin)
admin.site.register(ActivityFAQ, ActivityFAQAdmin)
admin.site.register(ActivityPricing, ModelAdmin)
admin.site.register(ActivityEnquiry, ModelAdmin)
admin.site.register(ActivityTestimonial, ActivityTestimonialAdmin)
admin.site.register(AddOns, ModelAdmin)
admin.site.register(ActivityBookingAddOn, ModelAdmin)
admin.site.register(VideoReview, ModelAdmin)
admin.site.register(Review, ModelAdmin)


class ActivityBookingAddOnInline(StackedInline):
    model = ActivityBookingAddOn
    tab = True


class ActivityBookingAdmin(ModelAdmin):
    list_display = (
        "__str__",
        "name",
        "booking_date",
        "is_private",
        "is_verified",
    )
    list_filter = ("is_private", "is_verified", "booking_date", "activity")
    inlines = [ActivityBookingAddOnInline]


admin.site.register(ActivityBooking, ActivityBookingAdmin)
