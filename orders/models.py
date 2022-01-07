import uuid
from django.db import models

# Create your models here.
class Order(models.Model):
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    PAYMENT_MODE = (
        (CASH, "Casg"),
        (BANK_TRANSFER, "Bank Transfer")
    )
    FIXED = "fixed"
    PERCENTAGE = "percentage"
    DISCOUNT_TYPE = (
        (FIXED, "Fixed"),
        (PERCENTAGE, "Percentage")
    )

    order_id = models.CharField(max_length=500)
    customer_shop_name = models.CharField(max_length=500, blank=True, null=True)
    customer_first_name = models.CharField(max_length=500, blank=True, null=True)
    customer_last_name = models.CharField(max_length=500, blank=True, null=True)
    customer_gst_no = models.CharField(max_length=500, blank=True, null=True)
    is_discounted = models.BooleanField(default=False)
    discount_value = models.CharField(max_length=500, blank=True, null=True)
    discount_type = models.CharField(max_length=500, blank=True, null=True, choices=DISCOUNT_TYPE)
    total_quantity = models.IntegerField(blank=True, null=True)
    subtotal_order_value = models.IntegerField(blank=True, null=True)
    gst_value = models.IntegerField(blank=True, null=True)
    total_order_value = models.IntegerField(blank=True, null=True)
    is_cancelled = models.BooleanField(default=False)
    is_hold = models.BooleanField(default=False)
    is_fullfilled = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=500, blank=True, null=True, choices=PAYMENT_MODE)
    transction_id = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = uuid.uuid4()
        return super().save(*args, **kwargs)

    def __str__(self):
        name = f"{self.customer_first_name} {self.customer_last_name}"
        if self.customer_shop_name:
            name = self.customer_shop_name
        return f"Order: {self.order_id} - Shop/Customer: {name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=500, blank=True, null=True)
    variant_id = models.CharField(max_length=500, blank=True, null=True)
    variant_sku = models.CharField(max_length=500, blank=True, null=True)
    variant_image = models.URLField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True, default=0)
    variant_price = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Order: {self.order_id} - Product: {self.product_id} - Variant: {self.variant_id}"