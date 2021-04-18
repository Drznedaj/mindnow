from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.gis.geoip2 import GeoIP2
from .forms import CustomUserCreationForm, ShortLinkForm, LinkForm
from .models import ShortLink, Link
from random import choices


def get_redirect_link(shid):
    possible_links = Link.objects.filter(link_id=shid)
    weigths = possible_links.values_list("weigth", flat=True)
    link = choices(possible_links, weigths, k=1)

    return link[0].text


def redirect_func(request, id):
    short_link_id = id
    link = get_redirect_link(short_link_id)

    g = GeoIP2()

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")

    return redirect(link)


def dashboard(request):
    return render(
        request,
        "users/dashboard.html",
        {
            "all_links": ShortLink.objects.all(),
        },
    )


def register(request):

    if request.method == "GET":

        return render(request, "users/register.html", {"form": CustomUserCreationForm})

    elif request.method == "POST":

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect(reverse("dashboard"))


def create_url(request):

    if request.method == "GET":

        return render(
            request,
            "users/create.html",
            {"forms": ShortLinkForm},
        )

    elif request.method == "POST":

        form = ShortLinkForm(request.POST)

        if form.is_valid():

            candidate = form.save(commit=False)
            candidate.user = request.user
            candidate.save()
            return redirect(reverse("create"))

def edit_url(request, id):
    
    if request.method == "GET":

        return render(
            request,
            "users/edit.html",
            {"form": LinkForm, 'links':Link.objects.filter(link=id), "url": ShortLink.objects.get(id=id)},
        )

    elif request.method == "POST":

        form = LinkForm(request.POST)

        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.link = ShortLink.objects.get(id=id)
            candidate.save()
            return redirect("edit_url", id)

def delete_link(request, id):
    link = Link.objects.get(id=id)
    link_id = link.link.id
    link.delete()
    return redirect("edit_url", link_id)

def edit_link(request, id):

    link = Link.objects.get(id=id)
    
    if request.method == "GET":
        
        form = LinkForm(instance=link)

        return render(
            request,
            "users/edit_link.html",
            {"form": form, 'link':Link.objects.get(id=id), "url_id": link.link.id},
        )

    elif request.method == "POST":

        form = LinkForm(request.POST)

        if form.is_valid():
            form = LinkForm(request.POST, instance=link)
            form.save()
            return redirect("edit_url", link.link.id)
        else:
            return render(
                request,
                "users/edit_link.html",
                {"form": form, 'link':Link.objects.get(id=id), "url_id": link.link.id},
            )