from django.contrib.gis.db import models


class Venue(models.Model):
    name = models.CharField(max_length=50)
    address_string = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)
    price = models.FloatField()
    image = models.ImageField(upload_to='images')
    official_page = models.CharField(max_length=300)
    previews = models.ManyToManyField('Preview')
    datetime = models.DateTimeField()
    genres = models.ManyToManyField('Genre')

    def shorten_description(self):
        if len(self.description) > 283:
            return self.description[:280]+"..."
        else:
            return self .description

    def short_genres_list(self):
        characters_len = 0
        passed_genres = []
        for genre_obj in self.genres.all():
            if len(passed_genres) < 4 and len(genre_obj.name) + characters_len < 20:
                characters_len += len(genre_obj.name)
                passed_genres.append(genre_obj.name)
            else:
                break
        return passed_genres

    def __str__(self):
        return self.name


class Preview(models.Model):
    url = models.CharField(max_length=200)
    type = models.CharField(max_length=20)


class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=50)
    events = models.ManyToManyField(Event)
    last_fm_entry_exists = models.BooleanField(False)

    def __str__(self):
        return self.name

