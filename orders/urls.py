from django.urls import path

from orders import views
from orders.views import clear_stock_error

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
    path('clear_stock_error/', clear_stock_error, name='clear_stock_error'),
]