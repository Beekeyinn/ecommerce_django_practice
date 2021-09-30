from django.contrib import admin
from .models import ObjectViewed
# Register your models here.

class ObjectViewedAdmin(admin.ModelAdmin):
    list_display = ('user','ip_address','content_type','object_id','content_object','timestamp')

admin.site.register(ObjectViewed,ObjectViewedAdmin)

