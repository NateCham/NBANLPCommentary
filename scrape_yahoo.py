# NBA NLP - Final Project - CSC 582
# Data Scraping  - Yahoo Sports
# Jacob Bustamante


"""
1) Get game URL list
   Iterate through each team's schedule page to get game URL list
   ex. http://sports.yahoo.com/nba/teams/lal/schedule/?season=2013_2
   30 teams - 82 games each (41home/41away) = 30 * 41 = 1230 games
   Keep url list to not duplicate a game
   NOTE: can possibly use inside hoops schedule to
   generate Yahoo's URL's since they are patterned, we just
   need the home team id yahoo uses

1.1) Remember to grab post-season as well

1.2) Build game database datastructure
     Can use Yahoo game URL string to get
     date - home - away - home_team_id


2) Get raw commentary
   Iterate through each game in game URL list and scrape commentary

2.1) Build team/player database datastructure as well
     Note: player-team relationships needed for Yahoo commentary
     
2.2) Possible player stats scrape
     Possibly grab stats / leaders / etcs.

"""


