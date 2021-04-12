from django.db import models
from django.contrib.auth.models import User


class ShortLink(models.Model):
    base_text = "http://mind.now/"
    short_url_id = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.base_text + self.short_url_id


class Link(models.Model):
    text = models.CharField(max_length=200)
    weigth = models.FloatField(default=1.0)
    link = models.ForeignKey(ShortLink, on_delete=models.CASCADE)

    def __str__(self):
        return self.text