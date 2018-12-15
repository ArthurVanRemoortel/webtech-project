from datetime import datetime
from htmldom import htmldom
from django.contrib.gis.geos.point import Point
import pytz


brussels_time = pytz.timezone('Europe/Brussels')


class LastfmScraper:

    class LastfmVenue:
        def __init__(self, name, location):
            self.name = name
            self.point = location.point
            self.address_fr = location.address_fr
            self.address_nl = location.address_nl

    class LastfmEvent:
        def __init__(self, name, venue, image, official_page, datetime):
            self.name = name
            self.venue = venue
            self.image = image
            self.official_page = official_page
            self.datetime = datetime

    class LastfmArtist:
        def __init__(self, name):
            self.name = name
            self.events = []
        def add(self, event):
            self.events.append(event)

    def __init__(self, geocoder):
        ab = self.LastfmVenue('Ancienne Belgique', geocoder.geocode('Anspachlaan 110, Brussels, 1000, Belgium'))
        botanique = self.LastfmVenue('Botanique', geocoder.geocode('Rue Royale 236, Brussels, 1210, Belgium'))
        self.geocoder = geocoder
        self.venue_dict = {ab.name: ab, botanique.name: botanique}
        self.events = []
        self.artist_dict = {}

        url_base = 'https://www.last.fm'
        url = 'https://www.last.fm/events?location_0=Brussels,+Belgium&location_1=50.8503396&radius=10000&location_2=4.351710300000036'
        for event in htmldom.HtmlDom(url).createDom().find('div.events-list-item-event--title'):
            link = url_base + event.children().attr('href')
            event_dom = htmldom.HtmlDom(link).createDom()
            name = event_dom.find('h1.header-title').text().strip()
            artists = self.get_or_create_artists(event_dom)
            img_link = self.get_img_link(event_dom)
            official_page = self.get_official_page(event_dom)
            dt = self.get_datetime(event_dom)
            lastfm_venue = self.get_or_create_venue(event_dom)
            lastfm_event = self.LastfmEvent(name, lastfm_venue, img_link, official_page, dt)
            self.events.append(lastfm_event)
            for artist in artists:
                artist.add(lastfm_event)

        self.venues = self.venue_dict.values()
        self.artists = self.artist_dict.values()
        for x in self.events:
            print(x.name)

    def get_or_create_venue(self, dom):
        venue_info = dom.find('p.event-detail-address')
        name = venue_info.find('strong').text()
        venue = self.venue_dict.get(name)
        if venue:
            return venue
        else:
            address = ', '.join(x.getText() for x in venue_info.children().last().find('span').toList())
            location = self.geocoder.geocode(address)
            venue = self.LastfmVenue(name, location)
            self.venue_dict[name] = venue
            return venue

    def get_or_create_artists(self, dom):
        artist_dom = dom.find('ol.grid-items')
        artists = [x.getText() for x in artist_dom.find('div.grid-items-item-details').find('a').toList()]
        for artist in artists:
            if not self.artist_dict.get(artist):
                self.artist_dict[artist] = self.LastfmArtist(artist)
        return [self.artist_dict.get(artist) for artist in artists]

    def get_img_link(self, dom):
        img_link = dom.find('div#event-poster-full-width').find('img').attr('src') + '.jpg'
        return img_link if img_link[0] != '/' else ''

    def get_official_page(self, dom):
        try:
            return dom.find('a.event-detail-long-link').last().text().strip()
        except AttributeError:
            return ''

    def get_datetime(self, dom):
        ymd = dom.find('p.qa-event-date span').attr('content').split('T')[0]
        year, month, day = (int(x) for x in ymd.split('-'))
        try:
            time = dom.find('p.qa-event-date span').children().last().text()
            hour, minute = (int(x) for x in time[:-2].split(':'))
            if time[-2:] == 'pm':
                hour += 12
            # important to use .astimezone(...) to get CET offset
            # and not datetime(..., tzinfo=...) which get BST offset for some reason
            return datetime(year, month, day, hour, minute).astimezone(brussels_time)
        except:
            return datetime(year, month, day).astimezone(brussels_time)


#dom = htmldom.HtmlDom(url).createDom()
#
#events = dom.find("div.events-list-item-event--title")
#
#
#
#
#def scrape(geocoder):
#    for event in events:
#        link = url_base + event.children().attr('href')
#        event_dom = htmldom.HtmlDom(link).createDom()
#        name = event_dom.find('h1.header-title').text().strip()
#        artists = [x.getText() for x in event_dom.find('p.header-title-secondary').find('a').toList()]
#        tmp = event_dom.find('p.event-detail-address')
#        venue_name = tmp.find('strong').text()
#        location_info = geocoder.geocode(', '.join(x.getText() for x in tmp.children().last().find('span').toList()))
#        point = Point(location_info.point.latitude, location_info.point.longitude)
#        address = location_info.address
#        img_link = event_dom.find('div#event-poster-full-width').find('img').attr('src') + '.jpg'
#        if img_link[0] == '/': # on last.fm this means no poster for event
#            img_link = ''
#        try:
#            evt_link = event_dom.find('a.event-detail-long-link').last().text().strip()
#        except AttributeError:
#            evt_link = ''
#        (year,month,day) = [int(x) for x in event_dom.find('p.qa-event-date span').attr('content').split('T')[0].split('-')]
#        try:
#            (hour, minute) = time_convert(event_dom.find('p.qa-event-date span').children().last().text())
#            dt = datetime(year, month, day, hour, minute, tzinfo=cet)
#        except:
#            dt = datetime(year, month, day, tzinfo=cet)
#        venueEntry = Venue.objects.filter(name=venue_name)
#        if venueEntry.exists():
#            venueEntry = venueEntry.first()
#        else:
#            venueEntry = Venue(name=venue_name, coordinates=coordinates)
#            venueEntry.save()
#        eventEntry = Event(
#                name=name,
#                venue=venueEntry,
#                official_page=evt_link,
#                datetime=dt,
#                )
#        eventEntry.save()
#        for artist in artists:
#            artistEntry = Artist.objects.filter(name=artist)
#            if artistEntry.exists():
#                artistEntry = artistEntry.first()
#            else:
#                artistEntry = Artist(name=artist)
#                artistEntry.save()
#            artistEntry.events.add(eventEntry)
#
