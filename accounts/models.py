from django.db import models
from django.contrib.auth.models import User
from webtech.models import Venue, Event
from django.db.models.signals import post_save
# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	username = models.CharField(max_length=20) #set default as User' username
	bio = models.CharField(max_length=500, default='Please enter your bio!')
	website = models.URLField(default='')
	registered = models.DateTimeField(auto_now=True)
	bookmarked_venues = models.ManyToManyField(to=Venue)
	bookmarked_event = models.ManyToManyField(to=Event)
	owned_venues = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='owner',null=True)

	def __str__(self):
		return self.username



def create_profile(sender, **kwargs):
	if kwargs['created']:
		current_user = kwargs['instance']
		user_profile = UserProfile.objects.create(user=current_user, bio="Fill in your profile bio!", username=current_user.username)
#creates a userprofile when a user is made

post_save.connect(create_profile, sender=User)