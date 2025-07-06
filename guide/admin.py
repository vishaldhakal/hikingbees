from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import TravelGuide, TravelGuideRegion, RegionWeatherPeriod
from tinymce.widgets import TinyMCE
from django import forms
from solo.admin import SingletonModelAdmin


class UnfoldSingletonModelAdmin(SingletonModelAdmin, ModelAdmin):
    pass


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
    tab = True


class TravelGuideRegionForm(forms.ModelForm):

    class Meta:
        model = TravelGuideRegion
        fields = '__all__'
        widgets = {
            'description': TinyMCE(),
            'short_description': TinyMCE(),
        }


class TravelGuideRegionAdmin(ModelAdmin):
    form = TravelGuideRegionForm
    list_display = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RegionWeatherPeriodAdmin]
    autocomplete_fields = ('blogs', 'activities')
    filter_horizontal = ('blogs', 'activities')


class TravelGuideAdmin(UnfoldSingletonModelAdmin):
    form = TravelGuideForm


admin.site.register(TravelGuide, TravelGuideAdmin)
admin.site.register(TravelGuideRegion, TravelGuideRegionAdmin)
