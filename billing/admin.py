from django.contrib import admin
from .models import BillingProfile
# Register your models here.
class BillingProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(BillingProfile)