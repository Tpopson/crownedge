from django.contrib import admin
from . models import *
# Register your models here.

class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'keyword', 'description', 'logo', 'carousel', 'carousel2', 'carousel3', 'carousel4', 'banner','favicon', 'mobile', 'mobile2', 'address', 'email', 'website', 'about', 'about2', 'copyright_year']


class TalkToUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'message', 'email', 'created', 'cleared', 'admin_note', 'status']


admin.site.site_header = 'Crownedge Hotel'
admin.site.site_title = 'Crownedge Hotel Admin'
admin.site.index_title = 'Crownedge Hotel Admin site'



admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(TalkToUs, TalkToUsAdmin)
