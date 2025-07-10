from django.contrib import admin

from .models import (
    TeamMember, Testimonial, LegalDocument, FeaturedTour, Affiliations,
    SiteConfiguration, Partners, TreekingNavDropdown, DestinationNavDropdown,
    OtherActivitiesNavDropdown, ClimbingNavDropdown, InnerDropdown, FAQ,
    FAQCategory, NewsletterSubscription, Enquiry
)
from tinymce.widgets import TinyMCE
from django import forms
from unfold.admin import ModelAdmin
from solo.admin import SingletonModelAdmin
from django.contrib.auth.models import User

# Create a base class that combines SingletonModelAdmin and Unfold's ModelAdmin


class UnfoldSingletonModelAdmin(SingletonModelAdmin, ModelAdmin):
    pass


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'
        widgets = {
            'about': TinyMCE(),
        }


class TeamMemberAdmin(ModelAdmin):
    form = TeamMemberForm
    list_display = ('name', 'role', 'type', 'email', 'order')
    list_filter = ('type',)
    search_fields = ('name', 'role', 'email')
    ordering = ('order', 'name')


class TestimonialAdmin(ModelAdmin):
    list_display = ('name', 'role', 'source', 'rating', 'created_at')
    list_filter = ('source', 'rating')
    search_fields = ('name', 'title', 'review')
    date_hierarchy = 'created_at'


class LegalDocumentAdmin(ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'description')


class FAQAdmin(ModelAdmin):
    list_display = ('question', 'category', 'active', 'created_at')
    list_filter = ('category', 'active')
    search_fields = ('question', 'answer')
    date_hierarchy = 'created_at'


class FAQCategoryAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class InnerDropdownAdmin(ModelAdmin):
    list_display = ('activity_region',)
    filter_horizontal = ('activites',)


class NewsletterSubscriptionAdmin(ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)


class EnquiryAdmin(ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date')
    search_fields = ('name', 'email', 'message')
    date_hierarchy = 'date'


class AffiliationsAdmin(ModelAdmin):
    list_display = ('name', 'link_to_website')
    search_fields = ('name',)


class PartnersAdmin(ModelAdmin):
    list_display = ('name', 'link_to_website')
    search_fields = ('name',)


class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')


# Register models with their respective admin classes
admin.site.register(SiteConfiguration, UnfoldSingletonModelAdmin)
admin.site.register(FeaturedTour, UnfoldSingletonModelAdmin)
admin.site.register(DestinationNavDropdown, UnfoldSingletonModelAdmin)
admin.site.register(ClimbingNavDropdown, UnfoldSingletonModelAdmin)
admin.site.register(OtherActivitiesNavDropdown, UnfoldSingletonModelAdmin)
admin.site.register(TreekingNavDropdown, UnfoldSingletonModelAdmin)
admin.site.register(InnerDropdown, InnerDropdownAdmin)
admin.site.register(Affiliations, AffiliationsAdmin)
admin.site.register(Partners, PartnersAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(FAQCategory, FAQCategoryAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(LegalDocument, LegalDocumentAdmin)
admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(User, UserAdmin)
