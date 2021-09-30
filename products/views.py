from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.views.generic import ListView, DetailView

from django.db.models.query import QuerySet

from carts.models import Cart
from .models import Product

from analytics.mixin import ObjectViewedMixin
# Create your views here.

class ProductViewList(ListView):
    # queryset = Product.objects.all()
    template_name = "product/product_list.html"

    # def get_context_data(self, **kwargs):
    #     context = super(ProductViewList,self).get_context_data(**kwargs)
    #     return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj 
        return context

    def get_queryset(self,*args, **kwargs):
        request = self.request
        return Product.objects.all()
        
    

class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    # queryset = Product.objects.all()
    model           = Product
    template_name   = "product/product_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj 
        return context
    
    def get_object(self,*args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug,active=True)
        except Product.DoesNotExist:
            raise Http404("Product not Found.")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug,active=True)
            return qs.first()
        except:
            raise Http404('Uhhmmm..')
        return instance



# class ProductDetailList(DetailView):
#     model=Product
#     template_name = "product/product_detail.html"

#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     return context
    
#     def get_object(self,*args, **kwargs):
#         request = self.request
#         id = self.kwargs["id"]
#         instance = Product.objects.get_by_id(id)
#         if instance is None:
#             raise Http404("Product doesnot exist.")
#         return instance


# class ProductFeaturedListView(ListView):
#     template_name = "product/featured.html"

#     # def get_context_data(self, **kwargs):
#     #     context = super(ProductViewList,self).get_context_data(**kwargs)
#     #     return context


#     def get_queryset(self,*args, **kwargs):
#         request = self.request
        return Product.objects.features()


# class ProductFeaturedDetailList(DetailView):
#     model=Product
#     template_name = "product/featured_detail.html"

#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     return context
    
#     def get_object(self,*args, **kwargs):
#         request = self.request
#         id = self.kwargs["id"]
#         instance = Product.objects.get_by_id(id)
#         if instance is None:
#             raise Http404("Product doesnot exist.")
#         return instance


# --------------------- Function Based View ----------------------------

# def product_list_view(request):
#     queryset = Product.objects.all()
#     context={
#         'object_list':queryset,
#     }
#     return render(request,"product/product_list.html",context)


# def product_detail_view(request,id):
#     instance = Product.objects.get_by_id(id)
#     if instance is None:
#         raise Http404("Product doesnot exist.")
#     context={
#         'object_list':instance,
#     }
#     return render(request,"product/product_detail.html",context)