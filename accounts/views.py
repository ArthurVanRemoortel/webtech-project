from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import VenueForm, EventForm, VenueBookmarkForm, EventBookmarkForm
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
		}
		context = {}
		current_user = request.user
		if current_user.is_authenticated:
			current_user_profile = UserProfile.objects.get(user=current_user.id)
			context['profile'] = current_user_profile

			venue_bookmarks = current_user_profile.bookmarked_venues.all()
			event_bookmarks = current_user_profile.bookmarked_event.all()
			bookmarks = {'event_bookmarks': event_bookmarks, 'venue_bookmarks': venue_bookmarks}
			context = {**context, **forms, **bookmarks}
			return render(request, 'profile.html', context)
		else:
			return redirect('login')