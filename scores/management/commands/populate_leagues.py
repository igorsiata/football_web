from django.core.management.base import BaseCommand
from scores.models import *

import requests

API_KEY = 'a63ee23a43e04fc78cd8bde71c49ad39'
BASE_URL = "https://api.football-data.org/v4"


def populate_competitions():
    url = f"{BASE_URL}/competitions"
    headers = {
        "X-Auth-Token": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        competitions = data.get("competitions", [])

        for competition in competitions:
            if competition['code'] not in ["BL1", "PD", "FL1", "SA", "PL"]:
                continue
            print(competition)
            league = League(name=competition['name'],
                            logo_link=competition['emblem'],
                            code=competition['code'],
                            api_id=competition['id'])
            league.save()
            print(f"Competition {competition['name']}:{
                  competition['id']} saved to the database.")
    else:
        print(f"Failed to retrieve competitions. Status code: {
              response.status_code}")


class Command(BaseCommand):
    help = "Populate the database with data from the API"

    def handle(self, *args, **kwargs):
        populate_competitions()
        self.stdout.write(self.style.SUCCESS(
            "Database populated successfully!"))
