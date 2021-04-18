from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import ShortLink, Link


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class ShortLinkForm(ModelForm):
    class Meta:
        model = ShortLink
        fields = ["short_url_id"]


class LinkForm(ModelForm):
    class Meta:
        model = Link
        exclude = ["link"]
