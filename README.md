# Football scores website
## Quick overview
This website is designed for football fans. It provides scores, standings and also recent news from football world. In provided database ony 5 leagues are present but you can easly add other.

## Distinctiveness and Complexity
This project integrates features like interactive functionality, dynamic page generation, and external API integration. By combining user interactivity, advanced backend logic, and dynamic content, this project offers a feature-rich, personalized platform for football fans.
This project integrates a third-party API to populate and maintain a live database of leagues, teams, and matches. Intuitive navigation (clicking team and beeing redirected to its page) makes moving around site easy. This project combines a lot of things that i have learned over cs50 web course and extends it.


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
### Following
You can follow your favourite teams. On your profile page followed teams will be displayed with upcoming match and two recent matches.

## Custom commands
Utilized api from https://www.football-data.org to populate my database. Created custom commands in "scores/management/commands" to populate database with and update database based on results: 
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
* toggle follow: use PUT method to add or remove team from followed list
* search: search for all teams and leagues containing query as substring
### Models
* User: default with field can edit for users who can add articles and results of matches
* News
* Team
* League
* Standing
* Match: info about match score and date. Score can be empty if match hasn't been plyed yet. When match is saved and score is valid updates standings using utils.update_standings
### Scripts
* news.js: displaying articles and implementing infinite scroll
* loadMatch.js: export function for rendering matches from template match_template.html.
* results.js: functionlaity for switch date buttons. function loadMatchByDate loads matches for certain date, adds header for different leagues.
* teamPage.js: calls loadMatchByTeam with team id fetched from url as argument, function loadMatchByTeam loads matches for certain team. Adds follow button functionality.
* profilePage: displays followed teams and add functionality of follow and unfollow.
* followTeam: export function for follow button.


## How to run
Type ```python manage.py runserver```. Important: 
* Install packages from requirements.txt
* Use provided database or populate yours with custom commands.
* In order for images to display you have to have internet connection.

