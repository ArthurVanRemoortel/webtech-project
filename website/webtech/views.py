from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import EventFilterForm, AddVenueForm, AddEventToVenueForm
from .models import Venue, Event, Genre, Artist, Preview


def index(request):
    all_events = Event.objects.all()
    search_results = []
    for i, item in enumerate(all_events):
        if i % 2 == 0:
            search_results.append([])
        search_results[-1].append(item)

    context = {
        'search_results': search_results
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
            venue_name = form.cleaned_data['venue_name']
            address = form.cleaned_data['address']
            description = form.cleaned_data['description']
            venue_image = form.cleaned_data['venue_image']
            venue_instance = Venue(name=venue_name, address_string=address, description=description, image=venue_image)
            venue_instance.save()
    else:
        form = AddVenueForm()
    context['form'] = form
    return render(request, 'add_venue_form.html', context)


def add_event_form_test(request):
    context = {}
    if request.method == 'POST':
        form = AddEventToVenueForm(request.POST, request.FILES)
        print('add_event_form_test Valid: ', form.is_valid())
        if form.is_valid():
            event_name = form.cleaned_data['event_name']
            venue = form.cleaned_data['venue']
            artists_raw = form.cleaned_data['artists']
            description = form.cleaned_data['description']
            price_strig = form.cleaned_data['price']
            price = 0 if "free" in price_strig.lower() else float(price_strig)
            event_image = form.cleaned_data['event_image']
            venue_object = Venue.objects.get(id=venue)
            event_instance = Event(name=event_name, venue=venue_object, description=description, price=price, image=event_image)
            event_instance.save()

            for artist in artists_raw.split(','):
                artist_instance = Artist(name=artist, last_fm_entry_exists=False)
                artist_instance.save()
                artist_instance.events.add(event_instance)

        else:
            print(form.data)
    else:
        form = AddEventToVenueForm() #venues=["Ancienne Belgique"]
    context['form'] = form

    return render(request, 'add_event_form.html', context)


def scrape(request):
    from .scripts.scrapers.flagey_scraper import FlageyScraper
    from .scripts.scrapers.ab_scraper import ABScraper
    from PIL import Image
    import requests
    from io import BytesIO
    from django.core.files.base import ContentFile

    Event.objects.all().delete()
    Preview.objects.all().delete()
    Genre.objects.all().delete()

    for scraper in [FlageyScraper(), ABScraper()]:
        print(f'Scraping {scraper.venue_name}')
        results = scraper.start_scrape(limit_results=False)
        venue = Venue.objects.get(name=scraper.venue_name)
        for event_dict in results:
            event_name = event_dict['event_title']
            response = requests.get(event_dict['event_image'])
            image = Image.open(BytesIO(response.content))
            file = BytesIO()
            image.save(file, 'JPEG')
            file.seek(0)
            image_name = event_dict['event_image'].split("/")[-1]
            if ".jpeg" not in image_name and ".jpg" not in  image_name and ".png" not in image_name:
                image_name += '.jpg'
            django_friendly_file = ContentFile(file.read(), image_name)
            description = event_dict['event_description']
            if description is None:
                description = ""
            event_object = Event(name=event_name,
                                 venue=venue,
                                 description=description,
                                 price=event_dict['event_price'],
                                 image=django_friendly_file, #event_dict['event_image'],
                                 official_page=event_dict['event_url'],
                                 datetime=event_dict['event_datetime']
                                 )
            event_object.save()

            for artist in []:
                artist_instance = Artist(name=artist, last_fm_entry_exists=False)
                artist_instance.save()
                artist_instance.events.add(event_object)

            for preview_url in event_dict['previews']:
                p = Preview(url=preview_url, type="youtube")
                p.save()
                event_object.previews.add(p)

            for genre in event_dict['event_tags']:
                g = Genre(name=genre)
                g.save()
                event_object.genres.add(g)

    return HttpResponse("Done")

