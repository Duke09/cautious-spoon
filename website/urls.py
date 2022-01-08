from django.urls import path

from .views import *

app_name = "website"

urlpatterns = [
    path('', HomeView.as_view()),
    path('dashboard/', DashboardView.as_view()),
]
