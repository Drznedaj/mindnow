from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class ShortLink(models.Model):
    base_text = "http://mind.now/"
    short_url_id = models.CharField(max_length=5)
    total_clicks = models.IntegerField(default=0)
    unique_clicks = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.base_text + self.short_url_id


class Link(models.Model):
    text = models.CharField(max_length=200)
    weigth = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        blank=True,
        null=True,
    )
    country_code = models.CharField(max_length=2, blank=True, null=True)
    link = models.ForeignKey(ShortLink, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class StatisticLinkData(models.Model):
    country_code = models.CharField(max_length=2)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    ip = models.CharField(max_length=15)
    continent_name = models.CharField(max_length=100)
    time_zone = models.CharField(max_length=100)
    is_in_european_union = models.BooleanField(default=False)
    time = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)
    link = models.ForeignKey(ShortLink, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip + " " + self.country + " from: " + self.city
