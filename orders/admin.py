from django.contrib import admin
from django.contrib.admin.options import TabularInline

from .models import Order, OrderItem
# Register your models here.
# admin.site.register(Order)
# admin.site.register(OrderItem)


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]