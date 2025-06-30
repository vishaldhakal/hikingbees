from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import GuideAuthour, TravelGuide, TravelGuideCategory, TravelGuideRegion, RegionWeatherPeriod
from tinymce.widgets import TinyMCE
from django import forms


class GuideAuthourForm(forms.ModelForm):
    class Meta:
        model = GuideAuthour
        fields = '__all__'
        widgets = {
            'about': TinyMCE(),
        }


class TravelGuideForm(forms.ModelForm):
    class Meta:
        model = TravelGuide
        fields = '__all__'
        widgets = {
            'guide_content': TinyMCE(),
        }


class RegionWeatherPeriodAdmin(TabularInline):
    model = RegionWeatherPeriod
    fields = ('start_month', 'end_month', 'high_temp', 'low_temp')
    autocomplete_fields = ('region',)
    tab = True


class TravelGuideRegionForm(forms.ModelForm):

    class Meta:
        model = TravelGuideRegion
        fields = '__all__'
        widgets = {
            'description': TinyMCE(),
        }


class GuideAuthourAdmin(ModelAdmin):
    form = GuideAuthourForm
    list_display = ('name', 'role', 'phone', 'created_at')
    search_fields = ('name', 'role')
    date_hierarchy = 'created_at'


class TravelGuideRegionAdmin(ModelAdmin):
    form = TravelGuideRegionForm
    list_display = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RegionWeatherPeriodAdmin]
    autocomplete_fields = ('blogs', 'activities')
    filter_horizontal = ('blogs', 'activities')


class TravelGuideCategoryAdmin(ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)


class TravelGuideAdmin(ModelAdmin):
    form = TravelGuideForm
    list_display = ('title', 'name', 'guide', 'created_at')
    list_filter = ('guide_category', 'guide_region', 'guide')
    search_fields = ('title', 'name', 'meta_title')
    filter_horizontal = ('guide_category', 'guide_region')
    date_hierarchy = 'created_at'
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(GuideAuthour, GuideAuthourAdmin)
admin.site.register(TravelGuide, TravelGuideAdmin)
admin.site.register(TravelGuideCategory, TravelGuideCategoryAdmin)
admin.site.register(TravelGuideRegion, TravelGuideRegionAdmin)
