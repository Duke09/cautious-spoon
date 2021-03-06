from django.db import transaction
from rest_framework import serializers

from .models import Products, ProductVariants


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariants,
        fields = "__all__"


class CreateProductSerialzer(ProductSerializer):
    variants = serializers.ListField()

    def validate_product_id(self, product_id):
        try:
            product = Products.objects.get(product_id=product_id)
        except Products.DoesNotExist:
            product = None

        if product:
            raise serializers.ValidationError(f"Product with id {product_id} already exists")

        return product_id
            
    
    @transaction.atomic
    def create(self, validated_data):
        product_id = validated_data.get('product_id')
        variants = validated_data.get('variants')

        if not variants:
            raise serializers.ValidationError("Variants is missing")

        product = Products.objects.create(
            title=validated_data.get('title'),
            product_id=product_id,
            handle=validated_data.get('handle'),
            vendor=validated_data.get('vendor'),
            product_type=validated_data.get('product_type'),
            tags=validated_data.get('tags'),
            taxable=validated_data.get('taxable'),
            tax_slab=validated_data.get('tax_slab'),
            draft=validated_data.get('draft'),
        )
        product.save()

        for variant in variants:
            variant['product'] = product

        ProductVariants.objects.bulk_create(
            [ProductVariants(**variant) for variant in variants])

        return product


class UpdateProductSerialzer(ProductSerializer):

    def update(self, product, validated_data):
        variants = validated_data.get('variants')
        
        product.title=validated_data.get('title')
        product.handle=validated_data.get('handle')
        product.vendor=validated_data.get('vendor')
        product.product_type=validated_data.get('product_type')
        product.tags=validated_data.get('tags')
        product.taxable=validated_data.get('taxable')
        product.tax_slab=validated_data.get('tax_slab')
        product.draft=validated_data.get('draft')
        product.save()

        if variants:
            for variant in variants:
                variant['product'] = product
            ProductVariants.objects.bulk_update(
                [ProductVariants(**variant) for variant in variants])

        return product