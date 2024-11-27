from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem, Address


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('users:profile')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    requires_delivery = form.cleaned_data['requires_delivery'] == "1"
                    delivery_address_id = form.cleaned_data.get('delivery_address')

                    delivery_address = None
                    if requires_delivery:
                        if not delivery_address_id:
                            messages.error(self.request, 'При доставке необходимо указать адрес.')
                            return redirect('orders:create_order')
                        try:
                            delivery_address = Address.objects.get(id=delivery_address_id, user=user)
                        except Address.DoesNotExist:
                            messages.error(self.request, 'Выбранный адрес доставки не существует.')
                            return redirect('orders:create_order')

                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=requires_delivery,
                        delivery_address=delivery_address,
                        payment_on_get=form.cleaned_data['payment_on_get'] == "1",
                    )

                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price = cart_item.product.sell_price()
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            self.request.session['stock_error_message'] = (
                                f'Недостаточное количество товара {name} на складе. В наличии: {product.quantity}.'
                            )
                            return redirect('orders:create_order')

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        product.quantity -= quantity
                        product.save()

                    cart_items.delete()
                    messages.success(self.request, 'Заказ оформлен!')
                    return redirect('users:profile')
        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect('orders:create_order')
        except Address.DoesNotExist:
            messages.error(self.request, 'Выбранный адрес доставки не существует.')
            return redirect('orders:create_order')


@csrf_exempt
def clear_stock_error(request):
    if request.method == 'POST' and 'stock_error_message' in request.session:
        del request.session['stock_error_message']
    return JsonResponse({'status': 'success'})


# @login_required
# def create_order(request):
#     if request.method == 'POST':
#         form = CreateOrderForm(data=request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     user = request.user
#                     cart_items = Cart.objects.filter(user=user)

#                     if cart_items.exists():
#                         # Создать заказ
#                         order = Order.objects.create(
#                             user=user,
#                             phone_number=form.cleaned_data['phone_number'],
#                             requires_delivery=form.cleaned_data['requires_delivery'],
#                             delivery_address=form.cleaned_data['delivery_address'],
#                             payment_on_get=form.cleaned_data['payment_on_get'],
#                         )
#                         # Создать заказанные товары
#                         for cart_item in cart_items:
#                             product=cart_item.product
#                             name=cart_item.product.name
#                             price=cart_item.product.sell_price()
#                             quantity=cart_item.quantity


#                             if product.quantity < quantity:
#                                 raise ValidationError(f'Недостаточное количество товара {name} на складе\
#                                                        В наличии - {product.quantity}')

#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity,
#                             )
#                             product.quantity -= quantity
#                             product.save()

#                         # Очистить корзину пользователя после создания заказа
#                         cart_items.delete()

#                         messages.success(request, 'Заказ оформлен!')
#                         return redirect('user:profile')
#             except ValidationError as e:
#                 messages.success(request, str(e))
#                 return redirect('orders:create_order')
#     else:
#         initial = {
#             'first_name': request.user.first_name,
#             'last_name': request.user.last_name,
#             }

#         form = CreateOrderForm(initial=initial)

#     context = {
#         'title': 'Home - Оформление заказа',
#         'form': form,
#         'order': True,
#     }
#     return render(request, 'orders/create_order.html', context=context)
