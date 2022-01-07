from django.urls import path


from .views import ProductWebhookAPI

app_name = 'products'

urlpatterns = [
    path('create/', ProductWebhookAPI.as_view(), name='create_product'),
    path('update/<str:product_id>/', ProductWebhookAPI.as_view(), name='update_product'),
    path('delete/<str:product_id>/', ProductWebhookAPI.as_view(), name='delete_product'),
]