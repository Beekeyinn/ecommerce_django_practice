from django.urls import path
from .views import KhaltiVerifyView, khalti_request_view

app_name = "billings"
urlpatterns = [
  path('Khalti_payment/',khalti_request_view, name='khalti'),
  path('Khalti_verify/',KhaltiVerifyView.as_view(), name='khaltiverify'),
]
