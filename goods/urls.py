from django.urls import path

from goods import views
from goods.views import product_detail, add_review

app_name = 'goods'

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
    path("product/<int:product_id>/add_review/", views.add_review, name="add_review"),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:review_id>/update/', views.update_review, name='update_review'),

]
