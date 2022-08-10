from django.shortcuts import render
from django.http import HttpResponse
from . models import * 

# Create your views here.

def room(request):
    standard_suite = Room.objects.get(standard_suite=True)
    luxury_suite = Room.objects.get(luxury_suite=True)
    deluxe_suite = Room.objects.get(deluxe_suite=True)
    royal_suite = Room.objects.get(royal_suite=True)

    context = {
        'standard_suite': standard_suite,
        'luxury_suite': luxury_suite,
        'deluxe_suite': deluxe_suite,
        'royal_suite': royal_suite
    }

    return render(request, 'index.html', context)