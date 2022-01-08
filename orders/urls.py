from django.urls import path

from .views import CreateOrder, OrderView

app_name = "orders"

urlpatterns = [
    path('create/', CreateOrder.as_view(), name="create_order"),
    path('orders/', OrderView.as_view(), name="order_list"),
]