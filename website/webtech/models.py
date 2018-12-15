from django.contrib.gis.db import models
from django.db.models.functions import Length
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

class Venue(models.Model):
    name = models.TextField()
    address_string = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name

    def average_score(self):
        return int(round(VenueReview.objects.filter(venue=self.pk).aggregate(Avg('score'))['score__avg'], 0))

    def get_score_image_url(self):
        avg_score = self.average_score()
        return f"/media/images/assets/score{avg_score}.png"


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
    text = models.TextField()
    score = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)])
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, related_name='reviews')
    date = models.DateField()

    def get_score_image_url(self):
        return f"/media/images/assets/score{self.score}.png"

    def __str__(self):
        return f"{self.score}: {self.text[:10]}..."




