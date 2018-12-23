from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.functions import Length
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from decimal import Decimal

from .scripts.geocoder import Geocoder


class Venue(models.Model):
    name = models.CharField(max_length=50)
    point = models.PointField()
    address_fr = models.TextField(default='')
    address_nl = models.TextField(default='')
    description = models.TextField()
    image = models.ImageField(upload_to='images/uploaded')

    def save(self, *args, **kwargs):
        if not (self.address_fr and self.address_nl):
            geocoder = Geocoder()
            location = geocoder.reverse(self.point)
            self.address_fr = location.address_fr
            self.address_nl = location.address_nl
        super(Venue, self).save(*args, **kwargs)

    def toJson(self):
        return str({
            'id': self.id,
            'name': self.name,
            'address': self.address_nl,
            'latlng': [self.point.x, self.point.y],
            }).replace("'", '"')

    def __str__(self):
        return self.name

    @property
    def rating(self):
        return int(round(VenueReview.objects.filter(venue=self.pk).aggregate(Avg('score'))['score__avg'], 0))

    def get_score_image_url(self):
        return "/media/images/assets/score{}.png".format(self.rating)


class Event(models.Model):
    name = models.CharField(max_length=200)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, related_name='events')
    description = models.TextField(default='')
    price = models.DecimalField(decimal_places=2, max_digits=7, null=True)
    official_page = models.CharField(max_length=200, default='')
    previews = models.ManyToManyField('Preview', related_name='events')
    datetime = models.DateTimeField()
    genres = models.ManyToManyField('Genre', related_name='events')
    image = models.ImageField(upload_to='images/uploaded')

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

    def save(self, *args, **kwargs):
        if self.price and type(self.price) != Decimal:
            self.price = Decimal(self.price).quantize(Decimal("0.00"))
        super(Event, self).save(*args, **kwargs)

    def toJson(self):
        return str({
            'id': self.id,
            'name': self.name,
            'venue': self.venue.name,
            'latlng': [self.venue.point.x, self.venue.point.y],
            'artists': [{'id': x['id'], 'name': x['name']} for x in self.artists.values()],
            'date': self.datetime.strftime('%h %-d'),
            'time': self.datetime.strftime('%H:%M'),
            'weekday': self.datetime.strftime('%a'),
            }).replace("'", '"')

    def __str__(self):
        return self.name


class Preview(models.Model):
    youtube_video_id = models.TextField()
    type = models.CharField(max_length=20)

    @property
    def youtube_embeddable_link(self):
        print(f'https://www.youtube.com/embed/{self.youtube_video_id}')
        return f'https://www.youtube.com/embed/{self.youtube_video_id}'

    def __str__(self):
        return "{}: {}".format(self.type, self.youtube_video_id)


class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100)
    events = models.ManyToManyField('Event', related_name='artists')
    last_fm_entry_exists = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class VenueReview(models.Model):
    text = models.TextField()
    score = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)])
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, related_name='reviews')
    date = models.DateField()

    def get_score_image_url(self):
        return "/media/images/assets/score{}.png".format(self.score)

    def __str__(self):
        return "{}: {}...".format(self.score, self.text[:15])

