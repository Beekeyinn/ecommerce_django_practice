from django.urls import path
from .views import EsewaPaymentRequest, EsewaVerification, KhaltiVerifyView, khalti_request_view

app_name = "billings"
urlpatterns = [
  path('Khalti_payment/',khalti_request_view, name='khalti'),
  path('Khalti_verify/',KhaltiVerifyView.as_view(), name='khaltiverify'),
  path('esewa_payment',EsewaPaymentRequest.as_view(),name='esewa_payment'),
  path('esewa_verification',EsewaVerification.as_view(),name='esewa_verify'),

]
