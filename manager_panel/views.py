import uuid

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from rest_framework.reverse import reverse_lazy
from unidecode import unidecode

from goods.models import Brand, Categories, Products, Stock
from django.db.models import Q
from .forms import BrandForm, CategoryForm, ProductForm, StockForm


# --------- List View ---------#

class CategoryListView(ListView):
    model = Categories
    template_name = "CRUD/category_list.html"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Categories.objects.filter(name__icontains=query)
        return super().get_queryset()

class BrandListView(ListView):
    model = Brand
    template_name = "CRUD/brand_list.html"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Brand.objects.filter(name__icontains=query)
        return super().get_queryset()

 # --------- Create View ---------#

class BrandCreateView(CreateView):
    model = Brand
    template_name = "CRUD/create_form.html"
    form_class = BrandForm
    success_url = reverse_lazy('manager_panel:brand_list')




 # --------- Update View ---------#

class BrandUpdateView(UpdateView):
    model = Brand
    template_name = "CRUD/create_form.html"
    form_class = BrandForm
    success_url = reverse_lazy('manager_panel:brand_list')


class StockListView(ListView):
    model = Stock
    template_name = "CRUD/stock_list.html"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Stock.objects.filter(product__name__icontains=query)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Products.objects.all()
        return context


class StockCreateView(CreateView):
    model = Stock
    template_name = "CRUD/create_form.html"
    form_class = StockForm
    success_url = reverse_lazy('manager_panel:stock_list')

class StockUpdateView(UpdateView):
    model = Stock
    template_name = "CRUD/create_form.html"
    form_class = StockForm
    success_url = reverse_lazy('manager_panel:stock_list')

class StockDeleteView(DeleteView):
    model = Stock
    success_url = reverse_lazy('manager_panel:stock_list')

 # --------- Delete View ---------#

class CategoryDeleteView(DeleteView):
    model = Categories
    success_url = reverse_lazy('manager_panel:category_list')

class BrandDeleteView(DeleteView):
    model = Brand
    success_url = reverse_lazy('manager_panel:brand_list')



 # --------- Detail View ---------#

def generate_article():
    return str(uuid.uuid4())[:8]


class ProductListView(ListView):
    model = Products
    template_name = "CRUD/product_list.html"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        brand_ids = self.request.GET.getlist('brands')  # Получаем список выбранных брендов
        price_min = self.request.GET.get('price_min')  # Минимальная цена
        price_max = self.request.GET.get('price_max')  # Максимальная цена

        queryset = Products.objects.all()

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if brand_ids:
            queryset = queryset.filter(brand_id__in=brand_ids)
        if query:
            queryset = queryset.filter(name__icontains=query)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Categories.objects.all()
        return context


class CategoryUpdateView(UpdateView):
    model = Categories
    form_class = CategoryForm
    success_url = reverse_lazy('manager_panel:category_list')

class CategoryCreateView(CreateView):
    model = Categories
    form_class = CategoryForm
    success_url = reverse_lazy('manager_panel:category_list')
    def form_valid(self, form):
        slug = slugify(unidecode(form.cleaned_data['name']))
        form.instance.slug = slug
        return super().form_valid(form)


class ProductCreateView(CreateView):
    model = Products
    form_class = ProductForm
    success_url = reverse_lazy('manager_panel:product_list')
    template_name = "CRUD/create_form.html"

    def form_valid(self, form):
        slug = slugify(unidecode(form.cleaned_data['name']))
        form.instance.slug = slug
        form.instance.article = generate_article()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Categories.objects.all()
        return context

class ProductUpdateView(UpdateView):
    model = Products
    form_class = ProductForm
    success_url = reverse_lazy('manager_panel:product_list')
    template_name = "CRUD/create_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Categories.objects.all()
        return context

class ProductDeleteView(DeleteView):
    model = Products
    success_url = reverse_lazy('manager_panel:product_list')

class ProductDetailView(DetailView):
    model = Products
    template_name = 'CRUD/product_detail.html'
