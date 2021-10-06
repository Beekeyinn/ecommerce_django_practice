from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse

from accounts.models import GuestEmail
from carts.models import Cart
from addresses.models import Address
from billing.models import BillingProfile
from orders.forms import PaymentMethods
from products.models import Product
from orders.models import Order

from addresses.forms import AddressForm
from accounts.forms import GuestForm, LoginForm
# Create your views here.
def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # products =[]
    # for x in cart_obj.products.all():
    #     products.append({
    #         "name":x.name,
    #         "price":x.price,
    #     })
    products = [{"id":x.id,"name":x.title,"price":x.price,"url":x.get_absolute_url()}for x in cart_obj.products.all()]    # similar to above code
    data = {
        "products":products,
        "subTotal":cart_obj.subtotal,
        "total":cart_obj.total
    }
    return JsonResponse(data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request,"carts/home.html",{"cart":cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id' or None)
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("Carts:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            if cart_obj.total==0:
                print(f"cart_id = { request.session['cart_id'] }")
                Cart.objects.get(id= request.session['cart_id']).delete()
            added=False
        else:     
            cart_obj.products.add(product_obj)
            added=True
        count = cart_obj.products.count()
        request.session["cart_items"] = count
        if request.is_ajax():
            jsonData = {
                "added": added,
                "removed": not added,
                "cart_items": count
            }
            return JsonResponse(jsonData)
    return redirect("Carts:home")

def checkout_home(request):
    cart_obj, new_cart = Cart.objects.new_or_get(request)
    order_obj=None

    if new_cart or cart_obj.products.count()==0:
        return redirect('Carts:home')
    
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    method_form = PaymentMethods()

    billing_address_id = request.session.get("billing_address_id",None)
    shipping_address_id = request.session.get("shipping_address_id",None)


    billing_profile, billing_profile_created = BillingProfile.objects.get_or_new(request)
    address_qs = None
    # above logic
    # user = request.user
    # billing_profile=None
    # guest_email_id = request.session.get('guest_email_id')
    # if user.is_authenticated:
    #     # Logged in checkout
    #     billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user,email=user.email)
    # elif guest_email_id is not None:
    #     # Guest user checkout
    #     guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
    #     billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    # else:
    #     pass
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.get_or_new(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
        if billing_address_id or shipping_address_id:
            order_obj.save()
        
    if request.method == "POST":
        method = request.POST.get('payment_method')
        
        if method == 'Cash on Delivery':
            is_done = order_obj.check_done()
            if is_done:
                order_obj.payment_method = method
                order_obj.mark_shipped()
                request.session['cart_items'] = 0
                del request.session["cart_id"]
                return redirect("Carts:success")
        elif method == 'Khalti':
            return redirect(reverse('billings:khalti')+"?o_id="+str(order_obj.order_id))
        elif method == 'Esewa':
            return redirect(reverse('billings:esewa_payment') + "?o_id=" + str(order_obj.order_id))
        # order_qs = Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True)
        # if order_qs.count()==1:
        #     order_obj = order_qs.first()
        # else:
        #     # old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
        #     # if old_order_qs.exists():
        #     #     old_order_qs.update(active=False)  
        #     order_obj = Order.objects.create(billing_profile=billing_profile,cart=cart_obj)

    context = {
        "order":order_obj,
        "billing_profile":billing_profile,
        "login_form":login_form,
        "guest_form":guest_form,
        "address_form":address_form,
        "address_qs":address_qs,
        "method_form":method_form
    }
    return render(request,'carts/checkout.html',context)


def checkout_done_view(request):
    return render(request,'carts/checkout_done.html')