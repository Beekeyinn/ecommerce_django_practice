from django.urls import path
from .views import (
    ProductDetailSlugView,
    ProductViewList,
    # ProductFeaturedDetailList,
    # ProductDetailList,
    # ProductFeaturedListView,
    # product_detail_view,
    # product_list_view,
)
app_name="products"
urlpatterns = [
    path('',ProductViewList.as_view(),name="products"),
    path('<slug:slug>',ProductDetailSlugView.as_view(),name="detail"),
    # path('products_fbv/',product_list_view,name="products"),
    # path('product_detail/<int:id>',ProductDetailList.as_view(),name="products_detail"),
    # path('products_detail_fbv/<int:id>',product_detail_view,name="products_detail_fbv"),
    # path('featured/',ProductFeaturedListView.as_view(),name="featured"),
    # path('featured_detail/<int:id>',ProductFeaturedDetailList.as_view(),name="featured_detail"),
]
