from django import forms
from django.contrib.auth.models import User
from webtech.models import Venue, Event

class VenueForm(forms.ModelForm):
	address = forms.CharField()
	class Meta:
		model = Venue
		fields = ['name', 'description','image',]

class EventForm(forms.ModelForm):
	previews = forms.CharField()
	class Meta:
		model = Event
		fields = ['name', 'venue', 'description', 'price', 'official_page', 'genres', 'image', 'datetime']

class VenueBookmarkForm(forms.Form):
	venue = forms.ChoiceField(
        choices=[(o.id, str(o.name)) for o in Venue.objects.all()]
    )

class EventBookmarkForm(forms.Form):
	event = forms.ChoiceField(
		choices=[(o.id, str(o.name)) for o in Event.objects.all()]
		)