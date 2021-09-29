from django.http import request
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView,FormView

from carts.models import Cart
from accounts.models import GuestEmail

from .forms import GuestForm, LoginForm, RegisterForm

# Create your views here.
def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        'title':"Login",
        'form':form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_url = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session["guest_email_id"] = new_guest_email.id 
        if is_safe_url(redirect_url, request.get_host()):
            return redirect(redirect_url)
        else:
            return redirect("/register")
    return redirect('/register')



class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_url = next_ or next_post or None

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request,email = email, password = password)
        if user is not None:
            login(request,user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_url, request.get_host()):
                return redirect(redirect_url)
            else:
                cart_obj, new_cart = Cart.objects.new_or_get(request)
                request.session["cart_items"] = cart_obj.products.count()
                return redirect("/")
        return super().form_invalid(form)

# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         'title':"Login",
#         'form':form
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_url = next_ or next_post or None
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request,username=username, password = password)
#         if user is not None:
#             login(request,user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_url, request.get_host()):
#                 return redirect(redirect_url)
#             else:
#                 cart_obj, new_cart = Cart.objects.new_or_get(request)
#                 request.session["cart_items"] = cart_obj.products.count()
#                 return redirect("/")
#         else:
#             print("error")

#     return render(request, "accounts/login.html",context)


class RegisterView(CreateView):
    form_class           = RegisterForm
    template_name   = 'accounts/register.html'
    success_url     = '/login/'

#  Above logic 
# User = get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context={
#         'title':"Register Page",    
#         'form':form,
#     }
#     if form.is_valid():
#         form.save()

#     return render(request, "accounts/register.html",context)
