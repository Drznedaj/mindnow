from django.contrib import admin
from .models import ShortLink, Link

admin.site.register(ShortLink)
admin.site.register(Link)