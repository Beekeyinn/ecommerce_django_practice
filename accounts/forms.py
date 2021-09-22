from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class GuestForm(forms.Form):
    email = forms.EmailField()


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':"form-control",
                'placeholder':"Enter Your Email"
            }
        )
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'class':"form-control",
                'placeholder':"password"
            }
        )
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':"form-control",
                'placeholder':"Enter Your Email"
            }
        )
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"Enter Your Email Address...."
            }
        )
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'class':"form-control",
                'placeholder':"password"
            }
        )
    )

    confirm_Password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':"form-control",
                'placeholder':"password"
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        queryset = User.objects.filter(username=username)
        if queryset.exists():
            raise forms.ValidationError("Invalid Username or already exists")
        return username


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError(" Email Address must be G mail. ")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        confPassword = self.cleaned_data.get("confirm_Password")
        if confPassword != password:
            raise forms.ValidationError("Password must match.")
        return data