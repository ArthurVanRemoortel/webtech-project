from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from webtech.models import Venue, Event
from accounts.models import UserProfile
from bootstrap_datepicker_plus import DateTimePickerInput


# class EditVenueForm(forms.ModelForm):


class EditProfileForm(forms.ModelForm):
	bio = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = UserProfile
		fields = ['username', 'bio', 'website']

class VenueForm(forms.ModelForm):
	address = forms.CharField()
	class Meta:
		model = Venue
		fields = ['name', 'description','image',]

class EventForm(forms.ModelForm):
	previews = forms.CharField()
	artists = forms.CharField()
	date = forms.DateField(
        widget=DateTimePickerInput(format='%d/%m/%Y %H:%M'),
        input_formats=['%d/%m/%Y %H:%M'],
    )
	class Meta:
		model = Event
		fields = ['name', 'venue', 'description', 'price', 'official_page', 'genres', 'image',]

class VenueBookmarkForm(forms.Form):
    venue = forms.ChoiceField()
    def __init__(self, choices, *args, **kwargs):
        super(VenueBookmarkForm, self).__init__()
        self.fields['venue'] = forms.ChoiceField(choices=choices)

class EventBookmarkForm(forms.Form):
    event = forms.ChoiceField()
    def __init__(self, choices, *args, **kwargs):
        super(EventBookmarkForm, self).__init__()
        self.fields['event'] = forms.ChoiceField(choices=choices)

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(label='Email')
	first_name = forms.CharField(label='First name')
	last_name = forms.CharField(label='Last name')
