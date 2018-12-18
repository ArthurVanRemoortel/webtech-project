from .serializers import EventSerializer, VenueSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Venue, Event, Genre, Artist, Preview, VenueReview


@api_view(['GET'])
def event_list(request):
    """
    List all events.
    """
    if request.method == 'GET':
        print(request.query_params.get('genre', None))
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def event_detail(request, pk):
    """
    Retrieve single event.
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def venue_list(request):
    """
    List all events.
    """
    if request.method == 'GET':
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def venue_detail(request, pk):
    """
    Retrieve single event.
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)