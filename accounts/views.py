from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import VenueForm, EventForm, VenueBookmarkForm, EventBookmarkForm, RegistrationForm
from accounts.models import UserProfile
from webtech.models import Venue, Event
from django.contrib.auth.models import User
from webtech.scripts.geocoder import Geocoder

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
		if 'addVenueBookmark'in request.POST:
			v_b_form = VenueBookmarkForm(request.POST)
			# raise Exception(v_b_form.is_valid())
			if v_b_form.is_valid():
				chosen_venue = v_b_form.cleaned_data['venue']
				current_user_profile.bookmarked_venues.add(chosen_venue)
				current_user_profile.save()
				return redirect('profile')
			else:
				return redirect('profile')
		if 'addEventBookmark' in request.POST:
			e_b_form = EventBookmarkForm(request.POST)
			if e_b_form.is_valid():
				chosen_event = e_b_form.cleaned_data['event']
				current_user_profile.bookmarked_event.add(chosen_event)
				current_user_profile.save()
				return redirect('profile')
			else:
				return redirect('profile')
		if 'addVenueForm' in request.POST:
			a_v_form = VenueForm(request.POST, request.FILES)
			if a_v_form.is_valid():
				address = a_v_form.cleaned_data['address']
				address_fr, address_nl, point = Geocoder().geocode(address)
				#update owned venues
				venue = Venue(
					name=a_v_form.cleaned_data['name'],
					point=point,
					address_fr=address_fr,
					address_nl=address_nl,
					description=a_v_form.cleaned_data['description'],
					image=a_v_form.cleaned_data['image'],
					)
				venue.save()
				return redirect('profile')
			else:
				return redirect('profile')
		if 'addEventForm' in request.POST:
			a_e_form = EventForm(request.POST, request.FILES)
			if a_e_form.is_valid():
				price_input = add_event_to_venue_form.cleaned_data['price']
				price = 0 if "free" in price_input.lower() else float(price_input)
				venue = add_event_to_venue_form.cleaned_data['venue']
				venue_object = Venue.objects.get(id=venue)
				artists = add_event_to_venue_form.cleaned_data['artists']
				genres = add_event_to_venue_form.cleaned_data['genres']
				previews = add_event_to_venue_form.cleaned_data['preview_links']

				event = Event(
						name=a_v_form.cleaned_data['name'],
						venue=venue_object,
						description=a_v_form.cleaned_data['description'],
						price=a_v_form.cleaned_data['price'],
						official_page=a_v_form.cleaned_data['official_page'],
						datetime=a_v_form.cleaned_data['datetime'],
						image=a_v_form.cleaned_data['image'],
					)

				for artist in artists.split(','):
					last_fm_exists = is_artist_on_lastfm(artist)
					artist_instance = Artist(name=artist, last_fm_entry_exists=last_fm_exists)
					artist_instance.events.add(event)
				for genre in genres.split(','):
					genre_instance = Genre(name=genre)
					event.genres.add(genre_instance)
				for preview in previews.split(','):
					preview_instance = Preview(url=preview,type="")
					event.previews.add(preview_instance)

				artist_instance.save()
				genre_instance.save()
				preview_instance.save()
				event.save()
		else:
			raise Exception(request.POST)


def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['password1'] == form.cleaned_data['password2']:
				password = form.cleaned_data['password1']
			user = User(
			username=form.cleaned_data['username'],
			email=form.cleaned_data['email'],
			first_name=form.cleaned_data['first_name'],
			last_name=form.cleaned_data['last_name'],
			password=password,
				)
			user.save()
			return redirect('logout')
	else: #its a get
		form = RegistrationForm()
		args = {'form': form}
		return render(request, 'register.html', args)