from django.urls import path, include

from .views import (
    CategoryCreateView, CategoryListView, ProductListView, StockListView, BrandListView, ProductUpdateView, ProductCreateView, BrandCreateView, BrandUpdateView,
    BrandDeleteView, StockCreateView, StockUpdateView, StockDeleteView, CategoryUpdateView,
    CategoryDeleteView, ProductDeleteView
)
app_name = 'manager_panel'

urlpatterns = [
    path('category_create/', CategoryCreateView.as_view(), name='category_create'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('category_update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),

    path('product_list/', ProductListView.as_view(), name='product_list'),
    # path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('product_update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    path('stock_list/', StockListView.as_view(), name='stock_list'),
    path('stock_create/', StockCreateView.as_view(), name='stock_create'),
    path('stock_update/<int:pk>/', StockUpdateView.as_view(), name='stock_update'),
    path('stock_delete/<int:pk>/', StockDeleteView.as_view(), name='stock_delete'),

    path('brand_list/', BrandListView.as_view(), name='brand_list'),
    path('brand_create/', BrandCreateView.as_view(), name='brand_create'),
    path('brand_update/<int:pk>/', BrandUpdateView.as_view(), name='brand_update'),
    path('brand_delete/<int:pk>/', BrandDeleteView.as_view(), name='brand_delete'),
]