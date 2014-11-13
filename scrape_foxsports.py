import urllib
import glob
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import os
import sqlite3


teams = {
    'Atlanta Hawks' : '01',
    'Boston Celtics' : '02',
    'New Orleans Pelicans' : '03',
    'Chicago Bulls' : '04',
    'Cleveland Cavaliers' : '05',
    'Dallas Mavericks' : '06',
    'Denver Nuggets' : '07',
    'Detroit Pistons' : '08',
    'Golden State Warriors' : '09',
    'Houston Rockets' : '10',
    'Indiana Pacers' : '11',
    'Los Angeles Clippers' : '12',
    'Los Angeles Lakers' : '13',
    'Miami Heat' : '14',
    'Milwaukee Bucks' : '15',
    'Minnesota Timberwolves' : '16',
    'Brooklyn Nets' : '17',
    'New York Knicks' : '18',
    'Orlando Magic' : '19',
    'Philadelphia 76ers' : '20',
    'Phoenix Suns' : '21',
    'Portland Trail Blazers' : '22',
    'Sacramento Kings' : '23',
    'San Antonio Spurs' : '24',
    'Oklahoma City Thunder' : '25',
    'Utah Jazz' : '26',
    'Washington Wizards' : '27',
    'Toronto Raptors' : '28',
    'Memphis Grizzlies' : '29',
    'Charlotte Bobcats' : '30'
}


class Game:
    """A game between two teams on a date"""

    def __init__(self, game_date, home_team, away_team):
        self.game_date = game_date
        self.home_team = home_team
        self.away_team = away_team
        self.plays = {}

    def __repr__(self):
        return '{game_date: ' + self.game_date + ', home_team: ' + home_team + ', away_team: ' + away_team + '}'

class Play:

    def __init__(self, quarter, minutes, seconds, home_score, away_score, textual_description, x_coord, y_coord):
        self.quarter = quarter
        self.minutes = minutes
        self.seconds = seconds
        self.home_score = home_score
        self.away_score = away_score
        self.textual_description = textual_description
        self.x_coord = x_coord
        self.y_coord = y_coord

    def __repr__(self):
        return 'quarter: ' + self.quarter + ' minutes: ' + self.minutes + ' seconds: ' + self.seconds + ' home_score: ' + self.home_score + ' away_score: ' + self.away_score + '\n\ttextual_description: ' + self.textual_description 

def insert_into_db(data):
    with sqlite3.connect('foxsports.db') as conn:
        for play in data['pbp']['sports-scores']['nba-scores']['nba-playbyplay']['play']:
            conn.execute('INSERT INTO play_by_play (quarter, minutes, seconds, home_score, away_score, textual_description, play_type, x_coord, y_coord) VALUES (?,?,?,?,?,?,?,?)', 
                    [play['quarter'], 
                     play['time-minutes'], 
                     play['time-seconds'], 
                     play['home-score'], 
                     play['visitor-score'],
                     play['textual-description'],
                     play_type(play['textual-description']),
                     play['x-shot-coord'],
                     play['y-shot-coord']])

def play_type(play_description):
    return 'Rebound'
    

def parse(games_dir):
    for f in glob.glob(os.path.join(games_dir, '*.html')):
        print(f)
        with open(f, errors='ignore') as fi:
            soup = BeautifulSoup(fi)
            script = soup.find('script', text=re.compile('nba\.initialUpdate'))
            game_object = re.search(r'nba\.initialUpdate\s*=\s*({.*?})\s*;', script.string).group(1)
            data = json.loads(game_object)
            insert_into_db(data)


if __name__ == '__main__':
    full_schedule = 'leagues_NBA_2014_games_games.csv'
    base_url = 'http://www.foxsports.com/nba/gameTrax?gameId='
    games_dir = 'webpages/foxsports_gamepages/'
    games = []

    with open(full_schedule) as schedule:
        for line in schedule:
            game = line.split(',')
            game_date = datetime.strptime(game[0], '%a %b %d %Y').strftime('%Y%m%d')
            home_team = game[4]
            away_team = game[2]

            games.append(Game(game_date, home_team, away_team))

    #for g in games:
    #    game_url = g.game_date + teams[g.home_team]
    #    print('downloading: ' + g.game_date + ' - ' + g.away_team + ' @ ' + g.home_team)
    #    urllib.request.urlretrieve(base_url + game_url, games_dir + g.game_date + '_' + g.away_team + '@' + g.home_team + '.html')
    parse(games_dir)

