from django.contrib import admin
from .models import Address
# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display=('billing_profile','address_type','address_line_1','city','country')
    list_filter=('billing_profile','address_type')
admin.site.register(Address,AddressAdmin)