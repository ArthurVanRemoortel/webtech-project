from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import EventFilterForm, AddVenueForm, AddEventToVenueForm, MapForm
from .models import Venue, Event, Genre, Artist, Preview


def index(request):
    context = {}
    search_results_events = []
    if request.method == 'POST':
        form = EventFilterForm(request.POST)
        form.data = request.POST.copy()
        if form.is_valid():
            event_title = form.cleaned_data['event_title']
            genres = form.cleaned_data['genres'].split(', ')
            date = form.cleaned_data['date']
            city = form.cleaned_data['city']
            zip = form.cleaned_data['zip']

            search_results_events = Event.objects.filter(name__contains=event_title)

    else:
        form = EventFilterForm()
        search_results_events = Event.objects.all()

    search_results = []
    for i, item in enumerate(search_results_events):
        if i % 2 == 0:
            search_results.append([])
        search_results[-1].append(item)
    context['search_results'] = search_results
    context['form'] = form
    return render(request, 'index.html', context)


def event_page(request, event_id):
    event = Event.objects.get(pk=event_id)
    context = {'event': event}
    return render(request, 'event_page.html', context)


def venue_page(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    context = {'venue': venue}
    return render(request, 'venue_page.html', context)


def map(request):
    context = {'form': MapForm()}
    return render(request, 'map.html', context)


# ----------- Testing --------------- #


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
    Venue.objects.all().delete()

    def django_image_from_url(url):
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        file = BytesIO()
        image.save(file, 'JPEG')
        file.seek(0)
        image_name = url.split("/")[-1]
        if ".jpeg" not in image_name and ".jpg" not in image_name and ".png" not in image_name:
            image_name += '.jpg'
        return ContentFile(file.read(), image_name)

    for scraper in [FlageyScraper(), ABScraper()]:
        print(f'Scraping {scraper.venue_name}')

        venue_object, _ = Venue.objects.get_or_create(
            name=scraper.venue_name,
            address_string=scraper.venue_addres,
            description=scraper.description,
            image=django_image_from_url(scraper.venue_image)
        )

        results = scraper.start_scrape(limit_results=False)
        for event_dict in results:
            event_name = event_dict['event_title']

            description = event_dict['event_description']
            if description is None:
                description = ""
            image = django_image_from_url(event_dict['event_image'])
            event_object = Event(name=event_name,
                                 venue=venue_object,
                                 description=description,
                                 price=event_dict['event_price'],
                                 image=image,
                                 official_page=event_dict['event_url'],
                                 datetime=event_dict['event_datetime']
                                 )
            event_object.save()

            # IMPORANT: !!! No artists are currently scraped from an event. For testing purposes only, one is made up.
            for artist in ["Charles Mingus"]:
                artist_instance, new = Artist.objects.get_or_create(name=artist, last_fm_entry_exists=True)
                artist_instance.events.add(event_object)

            for preview_url in event_dict['previews']:
                p, _ = Preview.objects.get_or_create(url=preview_url, type="youtube")
                event_object.previews.add(p)

            for genre in event_dict['event_tags']:
                g, _ = Genre.objects.get_or_create(name=genre)
                event_object.genres.add(g)

    return HttpResponse("Done")
