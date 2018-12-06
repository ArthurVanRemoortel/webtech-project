from django.contrib import admin
from .models import Event, Venue, Artist, Genre, Preview

# Register your models here.
admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Preview)
