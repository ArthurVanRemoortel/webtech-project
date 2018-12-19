from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from webtech.models import Venue, Event

import datetime, time

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	username = models.CharField(max_length=20) #set default as User' username
	bio = models.CharField(max_length=500, default='')
	website = models.URLField(default='')
	registered = models.DateTimeField(auto_now=True)
	# bookmarked_venues = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='bookmarked_by')
	# bookmarked_event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookmarked_by')
	bookmarked_venues = models.ManyToManyField(Venue)
	bookmarked_event = models.ManyToManyField(Event)
	owned_venues = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='owner')

	def __str__(self):
		return self.username


#creates UserProfile when a User is made
def create_profile(sender, **kwargs):
	if kwargs['created']:
		current_user = kwargs['instance']
		user_profile = UserProfile.objects.create(user=current_user, bio="Fill in your profile bio!", username=current_user.username)


post_save.connect(create_profile, sender=User)


class VenueReview(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)#, default=2) #2=admin's id
	venue = models.ForeignKey(Venue, on_delete=models.CASCADE, default=0) 
	text = models.TextField()

	def __str__(self):
		return self.venue.name


class EventReview(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	text = models.TextField()

	def __str__(self):
		return self.event.name