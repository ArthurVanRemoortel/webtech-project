from django.shortcuts import render, redirect
from accounts.models import UserProfile, EventReview, VenueReview
from webtech.models import Venue, Event, Genre, Artist, Preview
from webtech.forms import AddVenueForm, AddEventToVenueForm
from accounts.forms import RegistrationForm, VenueReviewForm, EventReviewForm
from django.views import View
from webtech.views import is_artist_on_lastfm

# Create your views here.
def home(request):
	current_user = request.user
	if current_user.is_authenticated:
		return redirect('/accounts/profile')
	else:
		return redirect('/accounts/login')

class PasswordChangeDoneView(View):
	template_name = 'accounts/profile.html'

class Profile(View):
	def get(self, request, *args, **kwargs):
		forms = {'e_form': EventReviewForm(),
		'v_form': VenueReviewForm(),
		'av_form': AddVenueForm(),
		'ae_form': AddEventToVenueForm(),}
		context = {}
		current_user = request.user
		if current_user.is_authenticated:
			current_user_profile = UserProfile.objects.get(user=current_user.id)
			event_reviews = EventReview.objects.filter(author=current_user.id)
			venue_reviews = VenueReview.objects.filter(author=current_user.id)
			context['profile'] = current_user_profile
			context['event_reviews'] = event_reviews
			context['venue_reviews'] = venue_reviews
			
			venue_bookmarks = current_user_profile.bookmarked_venues.all()
			event_bookmarks = current_user_profile.bookmarked_event.all()
			#raise Exception(venue_bookmarks) #empty for some reason
			bookmarks = {'e_b': event_bookmarks, 'v_b': venue_bookmarks}
			context = {**context, **forms, **bookmarks}
			return render(request, 'accounts/profile.html', context)
		else:
			return redirect('login')

	def post(self, request, *args, **kwargs):
		forms = {
			'e_form': EventReviewForm(),
			'v_form': VenueReviewForm(),
			'av_form': AddVenueForm(),
			'ae_form': AddEventToVenueForm(),}
		context = {}
		current_user = request.user
		if 'eventForm' in request.POST:
			event_review_form = EventReviewForm(request.POST)
			if event_review_form.is_valid():
				EventReview(event=event_review_form.cleaned_data['event'],
							text=event_review_form.cleaned_data['text']).save()
				return redirect('profile')
		if 'venueForm' in request.POST:
			venue_review_form = VenueReviewForm(request.POST)
			if venue_review_form.is_valid():
				venue = venue_review_form.cleaned_data['venue']
				text = venue_review_form.cleaned_data['text']

				venue_review = VenueReview(venue=venue, text=text, author=current_user)
				venue_review.save()
				return redirect('profile')
		if 'addVenueForm' in request.POST:
			add_venue_form = AddVenueForm(request.POST, request.FILES)
			if add_venue_form.is_valid():
				venue = Venue(
					name=add_venue_form.cleaned_data['venue_name'],
					address_string=add_venue_form.cleaned_data['address'],
					image=add_venue_form.cleaned_data['venue_image'],
					description=add_venue_form.cleaned_data['description'])
				
				UserProfile.objects.get(user=current_user.id)
				UserProfile.owned_venues.add(venue)
				venue.save()
				return redirect('profile')
		if 'newEventForm' in request.POST:
			add_event_to_venue_form = AddEventToVenueForm(request.POST, request.FILES)
			if add_event_to_venue_form.is_valid():
				price_strig = add_event_to_venue_form.cleaned_data['price']
				price = 0 if "free" in price_strig.lower() else float(price_strig)
				artists = add_event_to_venue_form.cleaned_data['artists']
				genres = add_event_to_venue_form.cleaned_data['genre']
				previews = add_event_to_venue_form.cleaned_data['preview_links']
				venue = add_event_to_venue_form.cleaned_data['venue']
				venue_object = Venue.objects.get(id=venue)
				event = Event(
					name=add_event_to_venue_form.cleaned_data['event_name'],
					venue=venue_object,
					description=add_event_to_venue_form.cleaned_data['description'],
					price=price,
					image=add_event_to_venue_form.cleaned_data['event_image'],
					official_page=add_event_to_venue_form.cleaned_data['official_page'],
					)

				event.datetime=add_event_to_venue_form.cleaned_data['date']
				event.save()
				for artist in artists.split(','):
					last_fm_exists = is_artist_on_lastfm(artist)
					artist_instance = Artist(name=artist, last_fm_entry_exists=last_fm_exists)
					artist_instance.save()
					artist_instance.events.add(event)
				for genre in genres.split(','):
					genre_instance = Genre(name=genre)
					genre_instance.save()
					event.genres.add(genre_instance)
				for preview in previews.split(','):
					preview_instance = Preview(url=preview,type="")
					preview_instance.save()
					event.previews.add(preview_instance)

				event.save()
			return redirect('profile')
		else:
			context = {**context, **forms}
			return render(request, 'accounts/profile.html', context)

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/accounts')
	else: #its a get
		form = RegistrationForm()
		args = {'form': form}
		return render(request, 'accounts/register.html', args)
