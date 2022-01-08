from django.urls import path


from .views import ProductView, ProductListAPI, ProductWebhookAPI

app_name = 'products'

urlpatterns = [
    path('product/', ProductView.as_view(), name="product_list"),
    path('create/', ProductWebhookAPI.as_view(), name='create_product'),
    path('update/<str:product_id>/', ProductWebhookAPI.as_view(), name='update_product'),
    path('delete/<str:product_id>/', ProductWebhookAPI.as_view(), name='delete_product'),
]