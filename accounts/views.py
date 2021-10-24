from django.contrib import messages
from django.http import request
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.contrib.auth import authenticate, login

from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic.edit import FormMixin
from django.views.generic import CreateView,FormView,DetailView,View
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.utils.safestring import mark_safe

from carts.models import Cart
from accounts.models import GuestEmail,EmailActivation

from .forms import EmailReactivationForm, GuestForm, LoginForm, RegisterForm
from .signal import user_logged_in

# Create your views here.

# @login_required
# def account_home_view(request):
#     context={}
#     return render(request, 'accounts/home.html',context)


class AccountHomeView(LoginRequiredMixin,DetailView):
    template_name='accounts/home.html'
    
    def get_object(self):
        return self.request.user
    

class AccountEmailActivationView(FormMixin ,View):
    success_url = '/login/'
    form_class = EmailReactivationForm
    def get(self,request, key,*args, **kwargs):
        qs = EmailActivation.objects.filter(key__iexact=key)
        confirm_qs = qs.confirmable()
        if confirm_qs.count()==1:
            obj = confirm_qs.first()
            obj.activate()
            messages.success(request,"Your email has been Activated. please login")
            return redirect('login')
        else:
            activated_qs = qs.filter(activated=True)
            if qs.exists():
                reset_link = reverse("password_reset")
                msg = f"""Your email has already been activated. 
                        Do you need to <a href="{reset_link}" class="list-group-item-action text-decoration-none"> reset your password?</a>"""
                messages.success(request,mark_safe(msg))
                return redirect('login')
        context={
            'form':self.get_form()
        }
        return render(request, 'registration/activation-error.html',context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self,form):
        request=self.request
        msg = """Activation link is send to your email address. Please check your email """
        messages.success(request, msg)
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        print(user)
        new_activation = EmailActivation.objects.create(user=user,email = email)
        new_activation.send_activation()
        return super().form_valid(form)

    def form_invalid(self, form):
        context={'form':form}
        return render(self.request, 'registration/activation-error.html',context)

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
            if not user.is_active:
                messages.error(request,"This user is inactive.")
                return super().form_invalid(form)
            login(request,user)
            user_logged_in.send(user.__class__,instance=user,request=request)
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
