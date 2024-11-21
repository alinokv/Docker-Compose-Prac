from django.contrib import admin
from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin

from users.models import User, Role


# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email", "role"]
    search_fields = ["username", "first_name", "last_name", "email",]

    

    inlines = [CartTabAdmin, OrderTabulareAdmin]


admin.site.register(Role)