from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, get_user_model
from django.forms import widgets
from django.http import request
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from accounts.models import EmailActivation

User = get_user_model()

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'admin', 'staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class GuestForm(forms.Form):
    email = forms.EmailField()


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class':"form-control",
                'placeholder':"Enter Your Email........"
            }
        )
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'class':"form-control",
                'placeholder':"Your Password........"
            }
        )
    )

    

class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
                'class':"form-control",
                'placeholder':"password"
            }))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
                'class':"form-control",
                'placeholder':"password"
            }))

    class Meta:
        model = User
        fields = ('fullname', 'email',)
        
        labels = {
            'fullname': _('Full Name'),
            'email':_('Email Address')
        }

        widgets = {
            'fullname': forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':"Enter your full name...."
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':"Enter your email address...."
                }
            )
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active=False
        # obj,is_created = EmailActivation.objects.create(user=user)
        # obj.send_activation()
        
        if commit:
            user.save()
        return user


class EmailReactivationForm(forms.Form):
    email = forms.EmailField(label='Email Address',widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Your email....'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link =  reverse('register')

            msg = f"""This email does not Exists. would you like to <a href='{register_link}' class="nav-link">register</a>"""
            raise forms.ValidationError(mark_safe(msg))
        return email