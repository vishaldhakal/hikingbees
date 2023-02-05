from django.contrib import admin
from .models import TeamMember,Testimonial,Affiliations,SiteConfiguration,Partners
from solo.admin import SingletonModelAdmin


admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(Affiliations)
admin.site.register(Partners)
admin.site.register(TeamMember)
admin.site.register(Testimonial)
