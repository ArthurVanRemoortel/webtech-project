from django.contrib import admin
from .models import UserProfile, VenueReview, EventReview

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(VenueReview)
admin.site.register(EventReview)