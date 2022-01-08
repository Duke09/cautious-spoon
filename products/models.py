import uuid
from django.db import models
from django.db.models.fields import URLField
from django.db.models.signals import pre_save

from utils.generators import number_generator,product_id_generator

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

    # def save(self, *args, **kwargs):
    #     if not self.product_id:
    #         self.product_id = uuid.uuid4()
    #     return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

def product_id_receiver(sender, instance, *args, **kwargs):
    if not instance.product_id:
        instance.product_id = product_id_generator(instance)
pre_save.connect(product_id_receiver, sender=Products)

class ProductVariants(models.Model):
    product = models.ForeignKey(Products, null=True, blank=True, on_delete=models.CASCADE)
    variant_title = models.CharField(null=True, blank=True, max_length=500)
    sku = models.CharField(null=True, blank=True, max_length=255)
    inventory_quantity = models.IntegerField(default=0, null=True, blank=True)
    image_url = URLField(blank=True, null=True)
    variant_price = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"{self.product.title[:3]}-{self.variant_title[:3]}-{number_generator(size=5)}"
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.product.title} - {self.variant_title}"

    class Meta:
        verbose_name = "Variant"
        verbose_name_plural = "Variants"
        default_related_name = 'product_variants'
