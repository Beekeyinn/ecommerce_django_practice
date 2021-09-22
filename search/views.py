from products.models import Product
from django.shortcuts import render
from django.views.generic.list import ListView

# Create your views here.
class SearchProductList(ListView):
    # queryset = Product.objects.all()
    template_name = "search/view.html"

    # def get_context_data(self, **kwargs):
    #     context = super(ProductViewList,self).get_context_data(**kwargs)
    #     return context


    def get_queryset(self,*args, **kwargs):
        request = self.request
        query = request.GET.get('q',None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()