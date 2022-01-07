import uuid
from django.db import models
from django.db.models.fields import URLField
from django.db.models.fields.json import JSONField

# Create your models here.
class Products(models.Model):
    title = models.CharField(null=True, blank=True, max_length=500)
    product_id = models.CharField(null=True, blank=True, max_length=120)
    handle = models.CharField(null=True, blank=True, max_length=500)
    vendor = models.CharField(null=True, blank=True, max_length=500)
    product_type = models.CharField(null=True, blank=True, max_length=500)
    tags = models.CharField(null=True, blank=True, max_length=1024)
    taxable = models.BooleanField(default=False, blank=True, null=True)
    tax_slab = models.CharField(max_length=120, blank=True, null=True)
    draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = uuid.uuid4()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

class ProductVariants(models.Model):
    product = models.ForeignKey(Products, null=True, blank=True, on_delete=models.CASCADE)
    variant_title = models.CharField(null=True, blank=True, max_length=500)
    sku = models.CharField(null=True, blank=True, max_length=255)
    inventory_quantity = models.IntegerField(default=0, null=True, blank=True)
    image_url = URLField(blank=True, null=True)
    variant_price = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.product.title} - {self.variant_title}"

    class Meta:
        verbose_name = "Variant"
        verbose_name_plural = "Variants"
