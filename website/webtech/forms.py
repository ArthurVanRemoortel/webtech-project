from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from .models import Venue


class EventFilterForm(forms.Form):
    event_title = forms.CharField(label='Event title', max_length=100, empty_value="Filter functionality (this is only a placeholder)")
    genres = forms.CharField(max_length=100)
    date = forms.DateField(
        widget=DatePickerInput(format='%d/%m/%Y')
    )
    city = forms.CharField(max_length=100)
    zip = forms.CharField(max_length=20)


class AddVenueForm(forms.Form):
    venue_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    venue_image = forms.ImageField()


class AddEventToVenueForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddEventToVenueForm, self).__init__(*args, **kwargs)
        #self.venues = venues

    event_name = forms.CharField(max_length=100)
    venue = forms.ChoiceField(
        choices=[(o.id, str(o.name)) for o in Venue.objects.all()]
    )
    artists = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.CharField(max_length=20)
    date = forms.DateField(
        widget=DatePickerInput(format='%d/%m/%Y')
    )
    official_page = forms.URLField()
    preview_links = forms.CharField(widget=forms.Textarea)
    event_image = forms.ImageField()



