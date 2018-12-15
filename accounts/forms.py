from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import VenueReview, EventReview

class RegistrationForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = [
			'username', 
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
			]
	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save() #runs sql query

		return user

class VenueReviewForm(forms.ModelForm):
	class Meta:
		model = VenueReview
		fields = ['author', 'venue', 'text']

class EventReviewForm(forms.ModelForm):
	class Meta:
		model = EventReview
		fields = ['event', 'text']

