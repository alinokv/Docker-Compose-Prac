from django import forms
from goods.models import Brand, Categories, Products, Stock

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['category', 'brand', 'name', 'description', 'price', 'image', 'quantity']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['cell_number', 'product']
