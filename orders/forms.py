from django import forms
from django.db.models import fields
from .models import Order
class PaymentMethods(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('payment_method',)