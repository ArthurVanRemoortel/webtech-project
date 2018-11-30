from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import EventFilterForm, AddVenueForm, AddEventToVenueForm
# Create your views here.


def index(request):
    context = {
        'search_results': [[1, 2], [3, 4], [5, 6], [7, 0], [8, 9]]
    }
    if request.method == 'POST':
        form = EventFilterForm(request.POST)
        form.data = request.POST.copy()
        if form.is_valid():
            return HttpResponseRedirect('/map/')
    else:
        form = EventFilterForm()
    context['form'] = form
    return render(request, 'index.html', context)


def event_page(request):
    context = {}
    return render(request, 'event_page.html', context)


def venues(request):
    context = {}
    # Test
    context['form'] = EventFilterForm()
    return render(request, 'venues.html', context)


def add_venue_form_test(request):
    context = {}
    if request.method == 'POST':
        form = AddVenueForm(request.POST, request.FILES)
        print('add_venue_form_test Valid: ', form.is_valid())
        if form.is_valid():
            print(form.data)
    else:
        form = AddVenueForm()
    context['form'] = form
    return render(request, 'add_venue_form.html', context)


def add_event_form_test(request):
    context = {}
    if request.method == 'POST':
        form = AddEventToVenueForm(request.POST, request.FILES)
        print(form.data)
        print('add_event_form_test Valid: ', form.is_valid())
        if form.is_valid():
            print(form.data)
    else:
        form = AddEventToVenueForm()
    context['form'] = form

    return render(request, 'add_event_form.html', context)
