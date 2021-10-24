from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import EmailActivation, GuestEmail
from. forms import (UserChangeForm,UserCreationForm)
# Register your models here.
User = get_user_model()
class UserAdmin(UserAdmin):
    search_fields   =['email']
    
    add_form        = UserCreationForm
    form            = UserChangeForm

    list_display    = ('fullname','email','admin','staff','is_active')
    list_filter     = ('admin','staff','is_active')

    fieldsets       = (
        (None,{'fields':('email','password')}),
        ('Personal Info',{'fields':('fullname',)}),
        ('Permissions',{'fields':('is_active', 'admin', 'staff')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname','password1', 'password2'),
        }),
    )

    ordering = ('email',)
    filter_horizontal = ()
    class Meta:
        model       =   User

class GuestEmailAdmin(admin.ModelAdmin):
    search_fields=['email']
    class Meta:
        model=GuestEmail


class EmailActivationAdmin(admin.ModelAdmin):
    search_filter = ('email',)
    list_display = ['user','email','key','activated','forced_expired','expires','timestamp','updated']
    class Meta:
        model = EmailActivation



admin.site.register(GuestEmail,GuestEmailAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(EmailActivation,EmailActivationAdmin)
admin.site.unregister(Group)