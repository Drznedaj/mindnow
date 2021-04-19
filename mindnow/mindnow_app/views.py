from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.gis.geoip2 import GeoIP2
from .forms import CustomUserCreationForm, ShortLinkForm, LinkForm
from .models import ShortLink, Link, StatisticLinkData
from random import choices, choice

"""
Does all of the logic for redirecting the user to linked pages
@param shid, short link id for getting all of links
@param country, country_code of the user
@return None if there are problems, string of the link otherwise
"""


def get_redirect_link(shid, country):

    possible_links = Link.objects.filter(link_id=shid)

    if not possible_links:
        return None

    weigths = possible_links.values_list("weigth", flat=True)
    countries = possible_links.values_list("country_code", flat=True)
    link = None

    if any(countries) and country in countries:
        possible_links = Link.objects.filter(link_id=shid, country_code=country)
        weigths = possible_links.values_list("weigth", flat=True)

    if 1.0 in weigths:
        for p in possible_links:
            if p.weigth == 1.0:
                link = p.text
                break
    elif all(weigths):
        link = choices(possible_links, weigths, k=1)
        link = link[0].text
    else:
        link = choice(possible_links)
        link = link.text

    return link


def save_client_data(_id, geo, ip, code):
    country = geo.country_name(ip)
    g = geo.city(ip)
    city = g["city"]
    continent_name = g["continent_name"]
    time_zone = g["time_zone"]
    is_in_european_union = g["is_in_european_union"]

    short_link = ShortLink.objects.get(id=_id)
    short_link.total_clicks += 1

    unique_ips = StatisticLinkData.objects.filter(ip=ip)

    if not unique_ips:
        short_link.unique_clicks +=1
        
    s = StatisticLinkData(ip=ip, country=country, country_code=code, city=city, link=short_link)

    short_link.save()
    s.save()


def redirect_func(request, _id):

    g = GeoIP2()
    
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")

    ip = "77.46.192.159"
    code = g.country_code(ip)
    # code = "BA"

    link = get_redirect_link(_id, code)

    save_client_data(_id, g, ip, code)

    if not link:
        return redirect(reverse("dashboard"))

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
            {
                "form": LinkForm,
                "links": Link.objects.filter(link=id),
                "url": ShortLink.objects.get(id=id),
            },
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
            {"form": form, "link": Link.objects.get(id=id), "url_id": link.link.id},
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
                {"form": form, "link": Link.objects.get(id=id), "url_id": link.link.id},
            )