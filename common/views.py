from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

def access_denied_view(request):
    return render(request,'access_denied.html')