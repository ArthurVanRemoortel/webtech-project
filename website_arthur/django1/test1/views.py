from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {
        'search_results': [[1, 2], [3, 4], [5, 6], [7], [8, 9]]
    }
    return render(request, 'index.html', context)


def venues(request):
    context = {}
    return render(request, 'venues.html', context)


def add_venue_form_test(request):
    context = {}
    return render(request, 'add_venue_form.html', context)


def add_event_form_test(request):
    context = {}
    return render(request, 'add_event_form.html', context)
