from django.db import models
from django.contrib.auth.models import User
from webtech.models import Venue, Event
# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	username = models.CharField(max_length=20) #set default as User' username
	bio = models.CharField(max_length=500, default='Please enter your bio!')
	website = models.URLField(default='')
	registered = models.DateTimeField(auto_now=True)
	bookmarked_venues = models.ManyToManyField(Venue)
	bookmarked_event = models.ManyToManyField(Event)
	owned_venues = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='owner')

	def __str__(self):
		return self.username