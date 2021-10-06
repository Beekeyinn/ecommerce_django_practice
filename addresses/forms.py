from django import forms

from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line_1','address_line_2','city', 'country', 'state', 'postal_code']

        widgets = {
            'address_line_1' : forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':"Enter your Address 1..."
                }
            ),
            'address_line_2':forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':"Enter your Address 2 ..."
                }
            ),
            'city':forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':"Enter your City name...."
                }
            ),
            'country':forms.TextInput(
                attrs={
                    'class':"form-control",
                }
            ),
            'state':forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':"Enter your state name...."
                }
            ),
            'postal_code':forms.TextInput(
                attrs={
                    'class':"form-control",
                    'placeholder':"Enter your postal Code...."
                }
            ),
        }
