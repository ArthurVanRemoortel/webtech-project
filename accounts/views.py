from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import VenueForm, EventForm, VenueBookmarkForm, EventBookmarkForm, RegistrationForm, EditProfileForm
from accounts.models import UserProfile
from webtech.models import Venue, Event, Artist, Preview
from django.contrib.auth.models import User
from webtech.scripts.geocoder import Geocoder
from webtech.views import is_artist_on_lastfm


def home(request):
    current_user = request.user
    if current_user.is_authenticated:
        return redirect('/accounts/profile')
    else:
        return redirect('/accounts/login')


# steps for this view:
# -find out request type: get/post
# -if get, give all the info to display
# -if post, check which form the user is posting and write info to database
class Profile(View):
    def get(self, request, *args, **kwargs):
        forms = {
            'venue_form': VenueForm(),
            'event_form': EventForm(),

            'venue_bookmark_form': VenueBookmarkForm(),
            'event_bookmark_form': EventBookmarkForm(),
        }
        context = {}
        current_user = request.user
        if current_user.is_authenticated:  # retrieve the user's info to display
            current_user_profile = UserProfile.objects.get(user=current_user.id)
            context['profile'] = current_user_profile

            venue_bookmarks = current_user_profile.bookmarked_venues.all()
            event_bookmarks = current_user_profile.bookmarked_event.all()
            owned_venues = current_user_profile.owned_venues.all()
            info = {'event_bookmarks': event_bookmarks, 'venue_bookmarks': venue_bookmarks, 'owned_venues': owned_venues}

            context = {**context, **forms, **info}
            return render(request, 'profile.html', context)
        else:
            return redirect('login')

    # post:
    # -see which form
    # -see if it's valid
    # -if so, extract information, process information that requires this
    # -make obj, save to db
    # -redirect
    def post(self, request, *args, **kwargs):
        context = {}
        current_user = request.user
        current_user_profile = UserProfile.objects.get(user=current_user.id)
        if 'addVenueBookmark' in request.POST:
            v_b_form = VenueBookmarkForm(request.POST)
            if v_b_form.is_valid():
                chosen_venue = v_b_form.cleaned_data['venue']
                try:
                    current_user_profile.bookmarked_venues.add(chosen_venue)
                except IntegrityError:
                    pass  # in case it's already a bookmark: do nothing
                current_user_profile.save()
                return redirect('profile')
            else:
                return redirect('profile')
        if 'addEventBookmark' in request.POST:
            e_b_form = EventBookmarkForm(request.POST)
            if e_b_form.is_valid():
                chosen_event = e_b_form.cleaned_data['event']
                try:
                    current_user_profile.bookmarked_event.add(chosen_event)
                except IntegrityError:
                    pass  # in case it's already a bookmark: do nothing
                current_user_profile.save()
                return redirect('profile')
            else:
                return redirect('profile')
        if 'addVenueForm' in request.POST:
            a_v_form = VenueForm(request.POST, request.FILES)
            if a_v_form.is_valid():
                address = a_v_form.cleaned_data['address']
                address_fr, address_nl, point = Geocoder().geocode(address)
                # todo: update owned venues
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
                price_input = a_e_form.cleaned_data['price']
                venue_object = a_e_form.cleaned_data['venue']
                artists = a_e_form.cleaned_data['artists']
                genres = a_e_form.cleaned_data['genres']
                previews = a_e_form.cleaned_data['previews']

                event = Event(
                    name=a_e_form.cleaned_data['name'],
                    venue=venue_object,
                    description=a_e_form.cleaned_data['description'],
                    price=a_e_form.cleaned_data['price'],
                    official_page=a_e_form.cleaned_data['official_page'],
                    datetime=a_e_form.cleaned_data['date'],
                    image=a_e_form.cleaned_data['image'],
                )
                # todo: solve it not saving the time

                # order of saving objects is important here
                # id needs to be created (is done on save) etc..
                event.save()
                for artist in artists.split(','):
                    last_fm_exists = is_artist_on_lastfm(artist)
                    artist_instance = Artist(name=artist, last_fm_entry_exists=last_fm_exists)
                    artist_instance.save()
                    artist_instance.events.add(event)
                for genre in genres:
                    event.genres.add(genre)
                for preview in previews.split(','):
                    yt_check = check_preview_for_youtube(preview)
                    if yt_check is None:
                        # preview_instance = Preview(youtube_video_id=preview,type="")
                        pass
                    else:
                        preview_instance = Preview(youtube_video_id=yt_check, type="youtube")
                    preview_instance.save()
                    event.previews.add(preview_instance)

                return redirect('profile')

            else:
                # return redirect('profile')
                raise Exception(a_e_form.errors)
        else:
            raise Exception(request.POST)

class EditProfile(View):
	def get(self, request, *args, **kwargs):
		current_user = request.user
		if current_user.is_authenticated:
			current_user_profile = UserProfile.objects.get(user=current_user.id)
			context = {
				'profile': current_user_profile,
			}
			initial = {
				'username': current_user_profile.username,
				'bio': current_user_profile.bio,
				'website': current_user_profile.website,
			}
			forms = {
				'form':EditProfileForm(initial=initial),
			}
			context = {**context, **forms}
			return render(request, 'profile_edit.html', context)
		else:
			return redirect('login')
	def post(self, request, *args, **kwargs):
		current_user = request.user
		current_user_profile = UserProfile.objects.get(user=current_user.id)
		#todo: make modify owned venues en events form
		if 'editProfileForm' in request.POST:
			e_p_form = EditProfileForm(request.POST,instance=current_user_profile)
			if e_p_form.is_valid():
				e_p_form.save()
				return redirect('profile')
			else:
				return redirect('profile')
		else:
			return redirect('profile')

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
        else:
            # return redirect('')
            raise Exception(form.errors)
    else:  # its a get
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'register.html', args)


# cuts off the video ID if a preview is a youtube link
def check_preview_for_youtube(preview):
    watch_prefix = 'watch?v='
    if 'youtube.com/watch?v=' in preview:
        return preview[(preview.find(watch_prefix) + len(watch_prefix)):]
    else:
        return None