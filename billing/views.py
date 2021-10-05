from django.http.response import JsonResponse
from django.shortcuts import render
from orders.models import Order
from django.views import View
import requests
# Create your views here.

def khalti_request_view(request):
    o_id = request.GET.get('o_id')
    order_obj = Order.objects.get(order_id=o_id)
    context={
        'order':order_obj
    }
    return render(request,'billing/khalti_payment.html',context)

class KhaltiVerifyView(View):
    def post(self,request,*args, **kwargs):
        token = request.POST.get('token')
        amount = request.POST.get('amount')
        o_id = request.POST.get('order_id')

        
        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
        "token": token,
        "amount": amount
        }
        headers = {
        "Authorization": "Key test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"    
        }    # your merchant key(live or test) provided by khalti

        response = requests.post(url, payload, headers = headers)
        res = response.json()
        if res.get('idx'):
            success = True
            order_obj = Order.objects.get(order_id = o_id)
            if order_obj.check_done():
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']

        data = {
            'success':success
        }
        return JsonResponse(data)