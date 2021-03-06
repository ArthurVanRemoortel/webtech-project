from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from .models import Venue
from django.forms.widgets import NumberInput
from django.core.validators import MaxValueValidator, MinValueValidator


class EventFilterForm(forms.Form):
    """
    The form used to filter events on the home page.
    """
    event_title = forms.CharField(label='Event title', max_length=100, required=False)
    genres = forms.CharField(max_length=100, required=False)
    date = forms.DateField(input_formats=['%d/%m/%Y'],
        widget=DatePickerInput(format='%d/%m/%Y'), required=False)
    zip = forms.IntegerField(validators=[MaxValueValidator(9999), MinValueValidator(1000)], required=False)
    range = forms.CharField(max_length=20, required=False)
    distance_unit = forms.ChoiceField(
        choices=[(0, "m"), (1, "km")],
        required=False
    )

    # Would be hidden fields and automatically fillen in using AJAX and geolocation.
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())


class AddVenueForm(forms.Form):
    """
    Form used to create a venue linked to a user account.
    """
    venue_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    venue_image = forms.ImageField()


class AddEventToVenueForm(forms.Form):
    """
    Form used to create an events linked a venue.
    """
    def __init__(self, *args, **kwargs):
        super(AddEventToVenueForm, self).__init__(*args, **kwargs)

    event_name = forms.CharField(max_length=100)
    venue = forms.ModelChoiceField(queryset=Venue.objects.all())
    artists = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    genres = forms.CharField(max_length=150)
    price = forms.CharField(max_length=20)
    date = forms.DateField(
        widget=DatePickerInput(format='%d/%m/%Y'),
        input_formats=['%d/%m/%Y'],
    )
    official_page = forms.URLField()
    preview_links = forms.CharField(widget=forms.Textarea)
    event_image = forms.ImageField()


class ReviewForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    score = forms.IntegerField(widget=NumberInput(attrs={'type': 'range'}),
                               validators=[MaxValueValidator(10), MinValueValidator(0)])


class MapForm(forms.Form):
    """
    Filters used on the map page.
    """
    search_string = forms.CharField()
    show_bookmarked_venues = forms.BooleanField(widget=forms.CheckboxInput)
    show_bookmarked_events = forms.BooleanField(widget=forms.CheckboxInput)

