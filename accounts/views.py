from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import VenueForm, EventForm, VenueBookmarkForm, EventBookmarkForm, RegistrationForm
from accounts.models import UserProfile

# Create your views here.

def home(request):
	current_user = request.user
	if current_user.is_authenticated:
		return redirect('/accounts/profile')
	else:
		return redirect('/accounts/login')

class Profile(View):
	def get(self, request, *args, **kwargs): #overriding get request
		forms = {
			'venue_form': VenueForm(),
			'event_form': EventForm(),

			'venue_bookmark_form': VenueBookmarkForm(),
			'event_bookmark_form': EventBookmarkForm(),
		} #make forms that'll be used either way
		context = {}
		current_user = request.user
		if current_user.is_authenticated: #retrieve the user's info to display
			current_user_profile = UserProfile.objects.get(user=current_user.id)
			context['profile'] = current_user_profile

			venue_bookmarks = current_user_profile.bookmarked_venues.all()
			event_bookmarks = current_user_profile.bookmarked_event.all()
			bookmarks = {'event_bookmarks': event_bookmarks, 'venue_bookmarks': venue_bookmarks}
			context = {**context, **forms, **bookmarks}
			return render(request, 'profile.html', context)
		else:
			return redirect('login')

	def post(self, request, *args, **kwargs): #if it's a post request it contains form data
		forms = {
			'venue_form': VenueForm(),
			'event_form': EventForm(),

			'venue_bookmark_form': VenueBookmarkForm(),
			'event_bookmark_form': EventBookmarkForm(),
		}
		context = {}
		current_user = request.user
		current_user_profile = UserProfile.objects.get(user=current_user.id)
		if 'addVenueBookmarkForm'in request.POST:
			v_b_form = VenueBookmarkForm(request.POST)
			raise Exception(v_b_form.is_valid())
			if v_b_form.is_valid():
				chosen_venue = form.cleaned_data['venue']
				raise Exception(chosen_venue)
				current_user_profile.bookmarked_venues.add(chosen_venue)
				current_user_profile.save()
				return redirect('profile')
			else:
				return redirect('profile')


def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('profile')

	else: #its a get
		form = RegistrationForm()
		args = {'form': form}
		return render(request, 'register.html', args)