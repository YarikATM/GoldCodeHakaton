from django.shortcuts import render
from .models import Shipments


# Create your views here.

def main_page(request):
    shipments = Shipments.objects.all().order_by('time')
    return render(request, 'GoldCode/main_page.html', {'shipments': shipments})
