"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from ecommerce import settings

from django.contrib.auth.views import LogoutView
from .views import about_page, contact_page, homepage
from accounts.views import LoginView,RegisterView,guest_register_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage, name="homepage"),
    path('about/',about_page,name="about"),
    path('contact/',contact_page,name="contact"),
    path('login/',LoginView.as_view(),name="login"),
    path('register/',RegisterView.as_view(),name="register"),
    path('logout',LogoutView.as_view(), name="logout"),
    path('register/guest',guest_register_view,name="guest_register"),
    path('products/',include('products.urls', namespace="products")),
    path('search/',include('search.urls', namespace="Search")),
    path('cart/',include('carts.urls', namespace="Carts")),
    path('accounts/',include('accounts.urls', namespace='Accounts')),
    path('accounts/',include('accounts.password.urls')),
    path('',include('addresses.urls',namespace="Addresses")),
    path('billing/',include('billing.urls',namespace="billings")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
