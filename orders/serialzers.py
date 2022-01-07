from django.db import transaction
from rest_framework import serializers

from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order,
        fields = "__all__"


class CreateOrderSerialzer(OrderSerializer):
    order_items = serializers.ListField()

    def validate_order_id(self, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            order = None

        if order:
            raise serializers.ValidationError(f"Order with id {order_id} already exists")

        return order_id
            
    
    @transaction.atomic
    def create(self, validated_data):
        order_items = validated_data.get('order_items')

        if not order_items:
            raise serializers.ValidationError("Order Items are missing")

        order = Order.objects.create(
            order_id=validated_data.get('order_id'),
            order_created_by=validated_data.get('order_created_by'),
            customer_shop_name=validated_data.get('customer_shop_name'),
            customer_first_name=validated_data.get('customer_first_name'),
            customer_last_name=validated_data.get('customer_last_name'),
            customer_gst_no=validated_data.get('customer_gst_no'),
            is_discounted=validated_data.get('is_discounted'),
            discount_value=validated_data.get('discount_value'),
            discount_type=validated_data.get('discount_type'),
            total_quantity=validated_data.get('total_quantity'),
            subtotal_order_value=validated_data.get('subtotal_order_value'),
            gst_value=validated_data.get('gst_value'),
            tax_included=validated_data.get('tax_included'),
            tax_value=validated_data.get('tax_value'),
            total_order_value=validated_data.get('total_order_value'),
            is_cancelled=validated_data.get('is_cancelled'),
            is_hold=validated_data.get('is_hold'),
            is_fullfilled=validated_data.get('is_fullfilled'),
            is_delivered=validated_data.get('is_delivered'),
            paid=validated_data.get('paid'),
            payment_mode=validated_data.get('payment_mode'),
            transction_id=validated_data.get('transction_id'),
        )
        order.save()

        for order_item in order_items:
            order_item['order'] = order

        OrderItem.objects.bulk_create(
            [OrderItem(**order_item) for order_item in order_items])

        return order


