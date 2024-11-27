from django.http import Http404, HttpResponseForbidden
from django.views.generic import DetailView, ListView

from goods.utils import q_search
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Review, Products
from .forms import ReviewForm

from django.shortcuts import render, get_object_or_404, redirect


class CatalogView(ListView):
    model = Products
    # queryset = Products.objects.all().order_by("-id")
    template_name = "index-1.html"
    context_object_name = "goods"
    paginate_by = 20
    allow_empty = False
    # чтоб удобно передать в методы
    slug_url_kwarg = "category_slug"

    def get_queryset(self):
        category_slug = self.kwargs.get(self.slug_url_kwarg)
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")

        if category_slug == "all":
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != "default":
            goods = goods.order_by(order_by)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Каталог"
        context["slug_url"] = self.kwargs.get(self.slug_url_kwarg)
        return context

from django.contrib.auth.mixins import LoginRequiredMixin

class ProductView(DetailView):
    template_name = "goods/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_object(self, queryset=None):
        return Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(product=self.object).select_related("user")
        user_reviews = reviews.filter(user=self.request.user) if self.request.user.is_authenticated else None

        sort_by = self.request.GET.get('sort_by', 'newest')  # Фильтрация отзывов
        if sort_by == 'newest':
            reviews = reviews.order_by('-review_date')
        elif sort_by == 'rating_desc':
            reviews = reviews.order_by('-rating')
        elif sort_by == 'rating_asc':
            reviews = reviews.order_by('rating')
        elif sort_by == 'my_reviews' and user_reviews is not None:
            reviews = user_reviews

        context["reviews"] = reviews
        context["user_reviews"] = user_reviews
        context["sort_by"] = sort_by
        return context


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == "POST":
        review.delete()
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)


@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True}, status=200)
        return JsonResponse({"success": False, "errors": form.errors}, status=400)
    return JsonResponse({"success": False}, status=400)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return JsonResponse({"success": True}, status=201)
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    else:
        form = ReviewForm()
    return render(request, "add_review.html", {"form": form, "product": product})





def product_detail(request, product_slug):
    # Получаем продукт по slug или возвращаем 404, если не найден
    product = get_object_or_404(Products, slug=product_slug)
    return render(request, 'product_detail.html', {'product': product})
# def catalog(request, category_slug=None):

#     page = request.GET.get('page', 1)
#     on_sale = request.GET.get('on_sale', None)
#     order_by = request.GET.get('order_by', None)
#     query = request.GET.get('q', None)

#     if category_slug == "all":
#         goods = Products.objects.all()
#     elif query:
#         goods = q_search(query)
#     else:
#         goods = Products.objects.filter(category__slug=category_slug)
#         if not goods.exists():
#             raise Http404()

#     if on_sale:
#         goods = goods.filter(discount__gt=0)

#     if order_by and order_by != "default":
#         goods = goods.order_by(order_by)

#     paginator = Paginator(goods, 3)
#     current_page = paginator.page(int(page))

#     context = {
#         "title": "Home - Каталог",
#         "goods": current_page,
#         "slug_url": category_slug
#     }
#     return render(request, "goods/catalog.html", context)


# def product(request, product_slug):
#     product = Products.objects.get(slug=product_slug)

#     context = {"product": product}

#     return render(request, "goods/product.html", context)
