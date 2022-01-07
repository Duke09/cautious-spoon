from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status

from flashbloom.utils import set_response
from orders.serialzers import CreateOrderSerialzer

# Create your views here.
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