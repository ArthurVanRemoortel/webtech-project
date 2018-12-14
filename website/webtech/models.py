from django.contrib.gis.db import models
from django.db.models.functions import Length


class Venue(models.Model):
    name = models.TextField()
    address_string = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.TextField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='images')
    official_page = models.TextField()
    previews = models.ManyToManyField('Preview')
    datetime = models.DateTimeField()
    genres = models.ManyToManyField('Genre')

    def short_genres_list(self):
        characters_len = 0
        passed_genres = []
        for genre_obj in self.genres.all().order_by(Length('name').asc()):
            if len(passed_genres) < 3 and len(genre_obj.name) + characters_len < 20:
                characters_len += len(genre_obj.name)
                passed_genres.append(genre_obj.name)
            else:
                break
        return passed_genres

    def __str__(self):
        return self.name


class Preview(models.Model):
    url = models.TextField()
    type = models.CharField(max_length=20)


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.TextField()
    events = models.ManyToManyField(Event)
    last_fm_entry_exists = models.BooleanField(False)

    def __str__(self):
        return self.name


class VenueReview(models.Model):
    #author = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.TextField()



