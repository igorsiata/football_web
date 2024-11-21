from django.core.management.base import BaseCommand
from scores.models import *

import requests

API_KEY = 'a63ee23a43e04fc78cd8bde71c49ad39'
BASE_URL = "https://api.football-data.org/v4"


def populate_teams():

    headers = {
        "X-Auth-Token": API_KEY
    }
    leagues = League.objects.all()
    for league in leagues:
        # TODO now
        url = f"{BASE_URL}/competitions/{league.api_id}/matches?status=SCHEDULED"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            matches = data.get("matches", [])
            for match in matches:
                home_team = match['homeTeam']['id']
                away_team = match['awayTeam']['id']

                date = match['utcDate']
                score_home = match['score']['fullTime']['home']
                score_away = match['score']['fullTime']['away']
                match_to_save, created = Match.objects.get_or_create(
                    home_team=Team.objects.get(api_id=home_team),
                    away_team=Team.objects.get(api_id=away_team),
                    score_home=score_home,
                    score_away=score_away,
                    league=league,
                    date=date
                )
                if created:
                    print(f"Match {match_to_save} saved to the database.")
                elif (match_to_save.score_away == None or match_to_save == None) and score_home != None and score_away != None:
                    match_to_save.score_away = score_away
                    match_to_save.score_home = score_home
                    print(
                        f"Match {match_to_save} updated")
                else:
                    print(
                        f"Match {match_to_save} aleready exists in database.")
        else:
            print(f"Failed to retrieve league{league}. Status code: {
                response.status_code}")


class Command(BaseCommand):
    help = "Populate the database with data from the API"

    def handle(self, *args, **kwargs):
        populate_teams()
        self.stdout.write(self.style.SUCCESS(
            "Database populated successfully!"))
