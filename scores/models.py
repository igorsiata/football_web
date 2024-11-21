from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import update_standings


class User(AbstractUser):
    can_edit = models.BooleanField(default=False)
    followed_teams = models.ManyToManyField('Team', related_name="followers")


class News(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=127)
    body = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="news_images/", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self, current_user=None):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "title": self.title,
            "body": self.body,
            "image_path": self.image.url if self.image else 'None',
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M")

        }


class Team(models.Model):
    name = models.CharField(max_length=127)
    tla = models.CharField(max_length=3)
    stadium = models.CharField(max_length=127)
    logo = models.CharField(max_length=127)
    api_id = models.IntegerField()

    def serialize(self):

        return {
            "id": self.id,
            "name": self.name,
            "stadium": self.stadium,
            "tla": self.tla,
            "api_id": self.api_id,
            "logo": self.logo

        }


class League(models.Model):
    name = models.CharField(max_length=127, unique=True)
    logo_link = models.CharField(max_length=255)
    code = models.CharField(max_length=15)
    teams = models.ManyToManyField(Team, related_name="leagues")
    api_id = models.IntegerField(blank=True, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "logo_link": self.logo_link,
            "api_id": self.api_id,
        }


class Standings(models.Model):
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name="standings")
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="standings")
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def serialize(self):
        return {
            "league": self.league.name,
            "team": self.team.serialize(),
            "games_played": self.games_played,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "golas_scored": self.goals_scored,
            "goals_conceded": self.goals_conceded,
            "points": self.points
        }

    class Meta:
        unique_together = ("league", "team")
        ordering = ["-points", "-goals_scored", "-wins"]


class Match(models.Model):
    home_team = models.ForeignKey(
        Team,
        related_name="home_matches",
        on_delete=models.CASCADE
    )
    away_team = models.ForeignKey(
        Team,
        related_name="away_matches",
        on_delete=models.CASCADE
    )
    score_home = models.IntegerField(null=True, blank=True)
    score_away = models.IntegerField(null=True, blank=True)
    league = models.ForeignKey(League,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,)
    date = models.DateTimeField()

    def serialize(self):
        return {
            "id": self.id,
            "home_team": self.home_team.serialize(),
            "away_team": self.away_team.serialize(),
            "score_home": self.score_home,
            "score_away": self.score_away,
            "date": self.date.strftime("%Y-%m-%d %H:%M")

        }

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.score_away is not None and self.score_home is not None:
            update_standings(self)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['home_team', 'away_team', 'date'], name='unique_match')
        ]
