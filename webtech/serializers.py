from .models import Event, Genre, Venue, VenueReview
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    # genres = serializers.ReadOnlyField(read_only=True)
    genres = serializers.StringRelatedField(many=True)
    class Meta:
        model = Event
        fields = ('id', 'name', 'description',
                  'price', 'official_page', 'datetime',
                  'image', 'genres')


class GenreSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())
    class Meta:
        model = Genre
        fields = ('name', )


class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venue
        fields = ('id', 'name', 'address_fr', 'address_nl', 'description',
                  'image', 'rating')


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VenueReview
        fields = ('score', 'text')


