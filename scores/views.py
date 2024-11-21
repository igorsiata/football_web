from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from django.core.paginator import Paginator
from markdown2 import Markdown
from datetime import date, datetime, timedelta
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

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
    return render(request, "scores/results.html")


def leagues(request):
    leagues = League.objects.all()
    return render(request, "scores/leagues_list.html", {
        "leagues": leagues
    })


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
    is_followed = team in request.user.followed_teams.all()
    return render(request, "scores/team_page.html", {
        'team': team,
        "is_followed": is_followed
    })


def load_matches(request):
    id = request.GET.get('id', None)
    match_date = request.GET.get('date', None)
    max_num = request.GET.get('max', None)
    if id is not None:
        team = Team.objects.get(id=id)
        next_week = datetime.now() + timedelta(days=7)
        matches = Match.objects.filter(
            Q(home_team=team) | Q(away_team=team)).filter(date__lte=next_week).order_by("-date")
        if max_num is not None:
            max_num = int(max_num)
            response_data = {
                "matches": [match.serialize() for match in matches][:max_num]
            }
        else:
            response_data = {
                "matches": [match.serialize() for match in matches]
            }
    if match_date is not None:
        matches = Match.objects.filter(date__date=parse_date(match_date))
        matches_by_league = {}
        response_data = {
            "matches": {},
            "leagues": {}
        }
        for league in League.objects.all():
            matches_by_league[league.name] = matches.filter(
                league=league)
            response_data["matches"][league.name] = [
                match.serialize() for match in matches_by_league[league.name]]
            response_data["leagues"][league.name] = league.serialize()
    return JsonResponse(response_data, safe=False, status=201)


def league_page(request, league_code):
    league = League.objects.get(code=league_code)
    standings = [
        team.serialize for team in Standings.objects.filter(league=league).order_by("-points")]
    return render(request, "scores/league_page.html", {
        "league": league.serialize(),
        'standings': standings
    })


def profile(request):
    followed_teams = [team.serialize()
                      for team in request.user.followed_teams.all()]
    return render(request, "scores/profile.html", {
        "followed_teams": followed_teams
    })


@login_required
@csrf_protect
def toggle_follow(request, team_id):
    try:
        team_to_follow = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return JsonResponse({"error": "team not found"}, status=404)
    if request.method == 'PUT':
        if team_to_follow not in request.user.followed_teams.all():
            request.user.followed_teams.add(team_to_follow)
            return JsonResponse({"status": "followed"}, status=200)
        else:
            request.user.followed_teams.remove(team_to_follow)
            return JsonResponse({"status": "unfollowed"}, status=200)
    return JsonResponse({"error": "invalid method"}, status=405)


def search(request):
    if request.method == "POST":

        query = request.POST["search_query"]
        results_teams = []
        results_leagues = []
        print(query)
        for team in Team.objects.all():
            if query.lower() in team.name.lower():
                results_teams.append(team.serialize())
        for league in League.objects.all():
            if query.lower() in league.name.lower():
                results_leagues.append(league.serialize())
        return render(request, "scores/search_results.html", {
            "query": query,
            "teams": results_teams,
            "leagues": results_leagues
        })
