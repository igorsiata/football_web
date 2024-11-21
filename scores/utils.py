from difflib import SequenceMatcher


def are_strings_simmilar(str1, str2):
    return SequenceMatcher(None, str1, str2) > 0.8


def update_standings(match):
    from .models import Standings

    home_standings, _ = Standings.objects.get_or_create(
        league=match.league, team=match.home_team
    )
    away_standings, _ = Standings.objects.get_or_create(
        league=match.league, team=match.away_team
    )
    home_standings.games_played += 1
    away_standings.games_played += 1

    home_standings.goals_scored += match.score_home
    away_standings.goals_scored += match.score_away
    home_standings. goals_conceded += match.score_away
    away_standings.goals_conceded += match.score_home

    if match.score_away > match.score_home:
        away_standings.wins += 1
        away_standings.points += 3
        home_standings.losses += 1
    elif match.score_home > match.score_away:
        home_standings.wins += 1
        home_standings.points += 3
        away_standings.losses += 1
    else:
        home_standings.draws += 1
        home_standings.points += 1
        away_standings.draws += 1
        away_standings.points += 1

    home_standings.save()
    away_standings.save()
