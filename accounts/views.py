from django.shortcuts import render, redirect
from accounts.models import UserProfile, EventReview, VenueReview
from webtech.models import Venue, Event
from accounts.forms import RegistrationForm, VenueReviewForm, EventReviewForm

# Create your views here.
def home(request):
	current_user = request.user
	if current_user.is_authenticated:
		return redirect('/accounts/profile')
	else:
		return redirect('/accounts/login')


def profile(request):
	current_user = request.user
	if current_user.is_authenticated:
		current_user_profile = UserProfile.objects.get(user=current_user.id)
		current_user_reviews = VenueReview.objects.filter(author=current_user.id)
	else:
		return redirect('login')


	if request.method == 'POST':
		event_review_form = EventReviewForm(request.POST, request.FILES) #change form if this doesnt work
		venue_review_form = VenueReviewForm(request.POST, request.FILES)
		if event_review_form.is_valid():
			event_id = event_review_form.cleaned_data['event']
			event = Event.objects.get(id=event_id)
			text = event_review_form.cleaned_data['text']

			event_review = EventReview(event=event, text=text)
			event_review.save()
		if venue_review_form.is_valid():
			venue_id = venue_review_form.cleaned_data['venue']
			venue = Venue.objects.get(id=venue_id)
			text = venue_review_form.cleaned_data['text']

			venue_review = VenueReview(venue=venue, text=text, author=current_user)
			venue_review.save()
	else:
		event_review_form = EventReviewForm()
		venue_review_form = VenueReviewForm()


	args = {
		'profile': current_user_profile,
		'reviews': current_user_reviews,
		'e_form' : event_review_form,
		'v_form' : venue_review_form,
	}

	return render(request, 'accounts/profile.html', args)

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

# def add_event_review_modal(request):
# 	