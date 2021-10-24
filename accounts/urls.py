from django.urls import path
from django.contrib.auth import views as auth_views


from .views import AccountEmailActivationView, AccountHomeView
from django.contrib.auth.views import LogoutView
app_name="Accounts"
urlpatterns = [
    path('',AccountHomeView.as_view(),name='account'),
    path('email/confirm/<slug:key>/',AccountEmailActivationView.as_view(),name="email_activate"),    
]
