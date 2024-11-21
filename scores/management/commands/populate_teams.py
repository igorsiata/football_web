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
        url = f"{BASE_URL}/competitions/{league.api_id}/teams"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            teams = data.get("teams", [])
            for team in teams:
                team_to_save = Team(name=team['name'],
                                    tla=team['tla'],
                                    stadium=team['venue'],
                                    logo=team['crest'],
                                    api_id=team['id'])
                team_to_save.save()
                print(f"Team {team['name']}:{
                    team['id']} saved to the database.")
        else:
            print(f"Failed to retrieve league{league}. Status code: {
                response.status_code}")


class Command(BaseCommand):
    help = "Populate the database with data from the API"

    def handle(self, *args, **kwargs):
        populate_teams()
        self.stdout.write(self.style.SUCCESS(
            "Database populated successfully!"))
