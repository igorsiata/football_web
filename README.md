# Football scores website
## Quick overview
This website is designed for football fans. It provides scores, standings and also recent news from football world. In provided database ony 5 leagues are present but you can easly add other. Users with presmissions can add news and update scores of matches.

## Distinctiveness and Complexity

## Functionalities
### Scores display
When you visit "/results" or click results in navbar, scores page will show. You can select date of your interest and see matches that were played or are scheduled on this day. To render matches i use html template and script "static/scores/scripts/loadMatch.js" handles fetching data from django database and displying match result.
### Leagues
Leagues view will let you browse all leagues, if you click on league you will be redirected to page that displays this league standings.
### Team page
When you click team in league standings table or in scores display you will be redirected to team page that displays next match and all finished matches of this team.
### News page
When you visist "/news" you will see latest articles. You can scroll down and if you reach bottom of the page new set of articles will show, utilized pagination for each set of articles. When you click on article you will be redirected to article content, content is written in markdown and uses markdowntohtml to display. If user has permission "can_edit" he can write new article, you can add images that are saved into "scores/media".
### Search
You can search for team or league in top right corner. It will show all records that contains querry as substrion, not case sensitive.

## Custom commands
Utilized api from https://www.football-data.org to populate my database. Created custom commands in "scores/management/sommands" to populate database with: 
* leagues: ```python manage.py populate_leagues```
* teams: ```python manage.py populate_teams```
* matches played: ```python manage.py populate_matches```
* matches scheduled: ```python manage.py populate_matches_scheduled```

## Structure description
### Views
* Login and register view
* Default views for each page
* Loading news utilizing pagination
* Adding news
* Displaying article utilizing Markdown().convert() to display nicly styled articles
* loading matches: geting matches from database based on querry. Can get all matches from certain date grouped by league. Also can get past matches of team and all sheduled in next 7 day.
* league_page: displaying league standings of asked league ordered by points desceding
### Models
* User: default with field can edit for users who can add articles and results of matches
* News
* Team
* League
* Standing
* Match: info about match score and date. Score can be empty if match hasn't been plyed yet. When match is saved and score is valid updates standings using utils.update_standings
### Scripts
* news.js: displaying articles and implementing infinite scroll
* loadMatch.js: rendering matches from template match_template.html. Also export two functions loadMatchByDate that loads matches for certain date, adds header for different leagues, loadMatchByTeam loads matches of certain team.
* results.js: functionlaity for switch date buttons
* teamPage.js: calls loadMatchByTeam with team id fetched from url as argument


## How to run
Type ```python manage.py runserver```. Important: 
* Use provided database or populate yours with custom commands.
* In order for images to display you have to have internet connection.

