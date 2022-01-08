from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.views.generic import TemplateView
from django.template.response import TemplateResponse


from flashbloom.utils import set_response
from orders.serialzers import CreateOrderSerialzer
from orders.models import Order

# Create your views here.
class OrderView(TemplateView):
    template_name = 'orders/order.html'

    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        ctx = {
            "orders":orders,
        }

        return TemplateResponse(
            request, self.template_name, ctx
        )

class CreateOrder(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateOrderSerialzer

    def post(self, request):
        print(f"Create Order data {request.data}")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return set_response(data={}, status=status.HTTP_200_OK)
        else:
            return set_response(error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)