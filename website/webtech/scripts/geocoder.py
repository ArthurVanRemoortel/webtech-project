from django.contrib.gis.geos.point import Point
from geopy.geocoders import OpenCage


_opencage_api_key = '2effc381905143b7aa14e50ea7ff4fae'
_geocoder = OpenCage(_opencage_api_key)


class Geocoder:

    class Location:
        def __init__(self, location):
            self.point = Point(location.latitude, location.longitude)
            self.address_fr, self.address_nl = address_convert(location.address)
        def __iter__(self):
            return iter((self.address_fr, self.address_nl, self.point))

    def geocode(self, address):
        return self.Location(_geocoder.geocode(address))

    def reverse(self, point):
        return self.Location(_geocoder.reverse(point, exactly_one=True))


# using OpenCage geocoding, addresses in Brussels are returned as "French name - Dutch name"
def address_convert(address):
    print(address)
    street, town, country = address.split(', ')[-3:]
    postal_code = int(town[:4])
    if len(street.split(' - ')) > 1:
        street_fr, street_nl = street.split(' - ')
        # get street number
        street_fr += ' ' + street_nl.split(' ')[-1]
    else:
        street_fr = street_nl = street
    if len(town.split(' - ')) > 1:
        town_fr, town_nl = town.split(' - ')
        town_nl = str(postal_code) + ' ' + town_nl
    else:
        town_fr = town_nl = town
    # if location is in Brussels Capital Region, order will be correct
    # otherwise assume it's nearby town in Flemish Brabant, in which case the
    # the order has to be reversed
    if 1000 <= postal_code < 1300:
        return (street_fr + ', ' + town_fr, street_nl + ', ' + town_nl)
        return (street_nl + ', ' + town_nl, street_fr + ', ' + town_fr)



