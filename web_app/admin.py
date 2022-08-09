from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class UserModelAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_admin', 'last_login')
    search_fields = ('email', 'name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    ordering = ('-date_joined',)
    fieldsets = ()
    list_filter = ('is_admin', 'is_active')


class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


class CartModelAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ()
    fieldsets = ()
    list_filter = ()


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'food', 'quantity')
    search_fields = ('cart',)
    readonly_fields = ()

    filter_horizontal = ()
    ordering = ('-date_added',)
    fieldsets = ()
    list_filter = ()


class OrderModelAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'total_price', 'date_ordered', 'is_pending', 'is_confirmed', 'is_cooking', 'is_onTheWay',
        'is_delivered')
    search_fields = ('user',)
    readonly_fields = ('total_price', 'date_ordered')

    filter_horizontal = ()
    ordering = ('-date_ordered',)
    fieldsets = ()
    list_filter = ()


admin.site.register(UserModel, UserModelAdmin)
admin.site.register(ProfileModel, ProfileModelAdmin)

admin.site.register(CategoryModel)
admin.site.register(FoodModel)

admin.site.register(CartModel, CartModelAdmin)
admin.site.register(CartItem, CartItemAdmin)

admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(OrderItem)

admin.site.register(FeedbackModel)
