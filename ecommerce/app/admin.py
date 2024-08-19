from django.contrib import admin
from .models import Product, Order, Comment, Category, WishList, Cart, OrderItem, CartItem, WishItem
from django.contrib import admin
from .models import UserAccount

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')
    ordering = ('email',)


# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(WishList)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(WishItem)

# admin.site.register(UserAccount, UserAccountAdmin)