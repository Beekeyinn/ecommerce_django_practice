from addresses.views import checkout_address_create_view
from django.urls import path

app_name="Addresses"
urlpatterns = [
    path('checkout/address/create',checkout_address_create_view,name="shipping_address")
]
