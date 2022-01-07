from django.contrib import admin
from .models import Products, ProductVariants
# Register your models here.
class ProductVariantsAdmin(admin.TabularInline):
    model = ProductVariants


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductVariantsAdmin]