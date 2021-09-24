from addresses.views import checkout_address_create_view, checkout_address_use_view
from django.urls import path

app_name="Addresses"
urlpatterns = [
    path('checkout/address/create',checkout_address_create_view,name="checkout_address_create"),
    path('checkout/address/reuse',checkout_address_use_view,name="checkout_address_reuse"),
]
