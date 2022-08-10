from django.contrib import admin
from . models import *
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','room_type', 'slug', 'room_pix']
    prepopulated_fields = {'slug':('room_type',)}

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id','category', 'tag', 'room_no', 'slug', 'room_img', 'rate', 'amenity', 'standard_suite', 'luxury_suite', 'deluxe_suite', 'royal_suite', 'min_guest', 'max_guest', 'available', 'created_at', 'updated_at']
    prepopulated_fields = {'slug':('tag',)}
    list_editable = ['available']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Room, RoomAdmin)