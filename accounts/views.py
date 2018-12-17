from django.shortcuts import render, redirect
from accounts.models import UserProfile, EventReview, VenueReview
from webtech.models import Venue, Event
from accounts.forms import RegistrationForm, VenueReviewForm, EventReviewForm
from django.views import View

# Create your views here.
def home(request):
	current_user = request.user
	if current_user.is_authenticated:
		return redirect('/accounts/profile')
	else:
		return redirect('/accounts/login')

class Profile(View):

	def get(self, request, *args, **kwargs):
		forms = {'e_form': EventReviewForm(),
		'v_form': VenueReviewForm()}
		context = {}
		current_user = request.user
		if current_user.is_authenticated:
			current_user_profile = UserProfile.objects.get(user=current_user.id)
			current_user_reviews = VenueReview.objects.filter(author=current_user.id).union(EventReview.objects.filter(author=current_user.id))
			context['profile'] = current_user_profile
			context['reviews'] = current_user_reviews
			context = {**context, **forms}
			return render(request, 'accounts/profile.html', context)
		else:
			return redirect('login')

	def post(self, request, *args, **kwargs):
		forms = {'e_form': EventReviewForm(),
		'v_form': VenueReviewForm()}
		context = {}
		current_user = request.user
		if 'eventForm' in request.POST:
			event_review_form = EventReviewForm(request.POST)
			if event_review_form.is_valid():
				EventReview(event=event_review_form.cleaned_data['event'],
							text=event_review_form.cleaned_data['text']).save()
				# return render(request, 'accounts/profile.html', context)
				return redirect('profile')
		if 'venueForm' in request.POST:
			venue_review_form = VenueReviewForm(request.POST)
			if venue_review_form.is_valid():
				venue = venue_review_form.cleaned_data['venue']
				text = venue_review_form.cleaned_data['text']

				venue_review = VenueReview(venue=venue, text=text, author=current_user)
				venue_review.save()
				# return render(request, 'accounts/profile.html', context)
				return redirect('profile')
		else:
			context = {**context, **forms}
			return render(request, 'accounts/profile.html', context)



# def profile(request):
# 	args = {}
# 	current_user = request.user
# 	if current_user.is_authenticated:
# 		current_user_profile = UserProfile.objects.get(user=current_user.id)
# 		current_user_reviews = VenueReview.objects.filter(author=current_user.id)
# 		#current_user_reviews += EventReview.objects.filter(author=current_user.id) #queryset add operation
# 		args['profile'] = current_user_profile
# 		args['reviews'] = current_user_reviews
		
# 	else:
# 		return redirect('login')

# 	if request.method == 'POST':
# 		if 'eventForm' in request.POST:
# 			event_review_form = EventReviewForm(request.POST, request.FILES)
# 			args['erf'] = 'ya'
# 			if event_review_form.is_valid():
# 				event = event_review_form.cleaned_data['event']
# 				text = event_review_form.cleaned_data['text']

# 			event_review = EventReview(event=event, text=text)
# 			event_review.save()
# 		if 'venueForm' in request.POST:
# 			venue_review_form = VenueReviewForm(request.POST, request.FILES)
# 			if venue_review_form.is_valid():
# 				venue_id = venue_review_form.cleaned_data['venue']
# 				venue = Venue.objects.get(id=venue_id)
# 				text = venue_review_form.cleaned_data['text']

# 				venue_review = VenueReview(venue=venue, text=text, author=current_user)
# 				venue_review.save()
# 	# else:
# 	event_review_form = EventReviewForm()
# 	venue_review_form = VenueReviewForm()
# 	args['e_form'] = event_review_form
# 	args['v_form'] = venue_review_form
		
# 	return render(request, 'accounts/profile.html', args)

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