from carts.views import (cart_home, cart_update, checkout_done_view, checkout_home)
from django.urls import path

app_name = "Carts"
urlpatterns = [
    path('',cart_home, name="home"),
    path('update', cart_update, name="update"),
    path('checkout/',checkout_home, name="checkout"),
    path('checkout/success',checkout_done_view, name="success"),
]

