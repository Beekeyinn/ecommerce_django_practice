from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import GuestEmail
from. forms import (UserChangeForm,UserCreationForm)
# Register your models here.
User = get_user_model()
class UserAdmin(UserAdmin):
    search_fields   =['email']
    
    add_form        = UserCreationForm
    form            = UserChangeForm

    list_display    = ('fullname','email','admin','staff','active')
    list_filter     = ('admin','staff','active')

    fieldsets       = (
        (None,{'fields':('email','password')}),
        ('Personal Info',{'fields':('fullname',)}),
        ('Permissions',{'fields':('active', 'admin', 'staff')})
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

admin.site.register(GuestEmail,GuestEmailAdmin)
admin.site.register(User,UserAdmin)
admin.site.unregister(Group)