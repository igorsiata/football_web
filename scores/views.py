from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
import requests
from django.core.paginator import Paginator
from markdown2 import Markdown
from datetime import date, datetime, timedelta
from django.db.models import Q
from django.utils.dateparse import parse_date

from .models import *
from .forms import *
# Create your views here.


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "scores/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "scores/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "scores/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "scores/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "scores/register.html")


def home(request):
    return render(request, "scores/home.html")


def news(request):
    return render(request, "scores/news.html")


def results(request):
    matches_list = Match.objects.filter(
        date__lt=date.today()).order_by('-date')
    return render(request, "scores/results.html")


def upcoming(request):
    return render(request, "scores/home.html")


def load_news(request, page_num=1):

    news_list = News.objects.order_by('-timestamp')
    paginator = Paginator(news_list, 8)
    if paginator.num_pages >= page_num:
        page_obj = paginator.get_page(page_num)
    else:
        page_obj = []
    response_data = {
        "news": [news.serialize(current_user=request.user) for news in page_obj]
    }
    return JsonResponse(response_data, safe=False, status=201)


def add_news(request):
    if request.method == 'POST':
        news_form = NewsForm(request.POST, request.FILES)
        if news_form.is_valid():
            news = news_form.save(commit=False)
            news.creator = request.user
            news.save()
            return HttpResponseRedirect(reverse("news"))
        else:
            message = "error try again"
            return render(request, "scores/add_news.html", {
                "news_form": news_form,
                "message": message
            })
    news_form = NewsForm()
    return render(request, "scores/add_news.html", {
        "news_form": news_form
    })


def view_news(request, news_id):
    try:
        news = News.objects.get(id=news_id)
        response_data = {
            "title": news.title,
            "body": Markdown().convert(news.body)
        }
    except ObjectDoesNotExist:
        response_data = {
            "message": "Error - article not found"
        }

    return render(request, "scores/news_page.html", response_data)


def team_page(request, team_id):
    team = Team.objects.get(id=team_id)
    return render(request, "scores/team_page.html", {
        'team': team
    })


def load_matches(request):
    id = request.GET.get('id', None)
    match_date = request.GET.get('date', None)
    if id is not None:
        team = Team.objects.get(id=id)
        next_week = datetime.now() + timedelta(days=7)
        matches = Match.objects.filter(
            Q(home_team=team) | Q(away_team=team)).filter(date__lte=next_week).order_by("-date")
        response_data = {
            "matches": [match.serialize() for match in matches]
        }
    if match_date is not None:
        matches = Match.objects.filter(date__date=parse_date(match_date))
        matches_by_league = {}
        response_data = {
            "matches": {}
        }
        for league in League.objects.all():
            matches_by_league[league.name] = matches.filter(
                league=league)
            response_data["matches"][league.name] = [
                match.serialize() for match in matches_by_league[league.name]]
        print(response_data)
    return JsonResponse(response_data, safe=False, status=201)
