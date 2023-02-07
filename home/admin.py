from django.contrib import admin
from .models import TeamMember,Testimonial,Affiliations,SiteConfiguration,Partners,TreekingNavDropdown,DestinationNavDropdown,OtherActivitiesNavDropdown,ClimbingNavDropdown,InnerDropdown
from solo.admin import SingletonModelAdmin


admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(DestinationNavDropdown, SingletonModelAdmin)
admin.site.register(ClimbingNavDropdown, SingletonModelAdmin)
admin.site.register(OtherActivitiesNavDropdown, SingletonModelAdmin)
admin.site.register(TreekingNavDropdown, SingletonModelAdmin)
admin.site.register(InnerDropdown)
admin.site.register(Affiliations)
admin.site.register(Partners)
admin.site.register(TeamMember)
admin.site.register(Testimonial)
