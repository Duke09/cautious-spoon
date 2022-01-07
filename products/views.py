from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status


from flashbloom.utils import set_response

from .serialzers import CreateProductSerialzer, ProductSerializer, ProductVariantSerializer, UpdateProductSerialzer
from .models import ProductVariants, Products

# Create your views here.
class ProductListAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer

    def get(self, request):
        products = Products.objects.all()
        serializer = self.serializer_class(products, many=True).data
        return set_response(data=serializer, status=status.HTTP_200_OK)


class ProductWebhookAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateProductSerialzer

    def post(self, request):
        print(f"Create Product Data {request.data}")

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return set_response(data={}, status=status.HTTP_200_OK)
        else:
            return set_response(error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, product_id):
        print(f"Update Product Data {request.data}")

        if not request.data.get('product_id') or not product_id:
            return set_response(error=f"Product id missing.", status=status.HTTP_204_NO_CONTENT)

        try:
            product = Products.objects.get(product_id=product_id)
        except Products.DoesNotExist:
            return set_response(error=f"Product with id {product_id} doesn't exist.", status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateProductSerialzer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return set_response(data={}, status=status.HTTP_200_OK)
        else:
            return set_response(error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        print(f"Delete Product Data {request.data}")
        
        if not request.data.get('product_id') or not product_id:
            return set_response(error=f"Product id missing.", status=status.HTTP_204_NO_CONTENT)

        try:
            product = Products.objects.get(product_id=product_id)
            variatns = ProductVariants.objects.filter(product=product)
            if variatns.exists():
                variatns.delete()
            product.delete()
        except Products.DoesNotExist:
            return set_response(error=f"Product with id {product_id} doesn't exist.", status=status.HTTP_404_NOT_FOUND)
        
        return set_response(data={}, status=status.HTTP_200_OK)
