import re
from django import forms
from orders.models import Address


class AddressForm(forms.Form):
    street = forms.CharField()
    city = forms.CharField()
    postal_code = forms.CharField()
    house_number = forms.CharField()

class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", "Самовывоз"),
            ("1", "Доставка"),
        ],
        widget=forms.RadioSelect
    )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", "Оплата картой"),
            ("1", "Оплата при получении"),
        ],
        widget=forms.RadioSelect
    )

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")

        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера")

        return data

    def clean(self):
        cleaned_data = super().clean()
        requires_delivery = cleaned_data.get('requires_delivery')
        delivery_address = cleaned_data.get('delivery_address')

        # Проверяем, чтобы адрес был пуст при самовывозе
        if requires_delivery == "0" and delivery_address:
            raise forms.ValidationError("При самовывозе адрес доставки должен быть пустым.")

        # Проверяем, чтобы адрес был указан при доставке
        if requires_delivery == "1" and not delivery_address:
            raise forms.ValidationError("При доставке необходимо указать адрес.")

        return cleaned_data

    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Введите ваше имя",
    #         }
    #     )
    # )

    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Введите вашу фамилию",
    #         }
    #     )
    # )

    # phone_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Номер телефона",
    #         }
    #     )
    # )

    # requires_delivery = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0", False),
    #         ("1", True),
    #     ],
    #     initial=0,
    # )

    # delivery_address = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             "class": "form-control",
    #             "id": "delivery-address",
    #             "rows": 2,
    #             "placeholder": "Введите адрес доставки",
    #         }
    #     ),
    #     required=False,
    # )

    # payment_on_get = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0", 'False'),
    #         ("1", 'True'),
    #     ],
    #     initial="card",
    # )