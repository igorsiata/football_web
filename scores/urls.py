from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("news", views.news, name="news"),
    path("results", views.results, name="results"),
    path("upcoming", views.upcoming, name="upcoming"),
    path("load_news/<int:page_num>", views.load_news, name="load_news"),
    path("add_news", views.add_news, name="add_news"),
    path("news/<int:news_id>", views.view_news, name="view_news"),
    path("teams/<int:team_id>", views.team_page, name="team_page"),
    path("load_matches", views.load_matches, name="load_matches"),
]
