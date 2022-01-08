from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'website/home.html'

class DashboardView(TemplateView):
    template_name = 'website/dashboard.html'