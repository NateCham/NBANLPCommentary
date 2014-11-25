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

def insert_play(description):
    play = {}
    play['play_type'] = play_type(description.lower())


    if play['play_type'] == 'shot' or play['play_type'] == 'make' or play['play_type'] == 'miss':
        shot = re.search('(.*) (makes|misses) an? (.*) from (.*) (feet|foot) out\.', description)
        shot2 = re.search('(.*) (makes|misses) an? (.*)\.', description)
        dunk = re.search('(.*) dunks\.', description)
        dunks_from = re.search('(.*) dunks from (\d) (foot|feet) out\.', description)
        if shot:
            play['primary_player'] = shot.group(1)
            play['shot_made'] = shot.group(2)
            play['shot_type'] = shot.group(3).strip('shot').strip()
            play['shot_distance'] = shot.group(4)
        elif shot2:
            play['primary_player'] = shot2.group(1)
            play['shot_made'] = shot2.group(2)
            play['shot_type'] = shot2.group(3).strip('shot').strip()
        elif dunk:
            play['primary_player'] = dunk.group(1)
            play['shot_type'] = 'dunk'
            play['shot_made'] = 'made'
        elif dunks_from:
            play['primary_player'] = dunks_from.group(1)
            play['shot_type'] = 'dunk'
            play['shot_made'] = 'made'
            play['shot_distance'] = dunks_from.group(2)
        else:
            print(description)
    elif play['play_type'] == 'rebound':
        rebound = re.search('(.*) with an? (offensive|defensive) rebound\.', description)
        play['primary_player'] = rebound.group(1)
        play['rebound_type'] = rebound.group(2)
    elif play['play_type'] == 'foul':
        foul = re.search('(.*) foul committed by (.*)\.', description)
        if foul:
            play['foul_type'] = foul.group(1)
            play['primary_player'] = foul.group(2)
        else:
            print(description)
    elif play['play_type'] == 'timeout':
        timeout = re.search('(.*) take a (.*) timeout\.', description)
        official = re.search("Official's timeout\.", description)
        if timeout:
            play['team'] = timeout.group(1)
            play['timeout_type'] = timeout.group(2)
        elif official:
            play['timeout_type'] = 'official'
    elif play['play_type'] == 'substitution':
        sub = re.search('Substitution: (.*) in for (.*)\.', description)
        play['primary_player'] = sub.group(1)
        play['secondary_player'] = sub.group(2)
    elif play['play_type'] == 'free throw':
        free = re.search('(.*) (makes|misses) free throw (\d) of (\d)\.', description)
        technical = re.search('(.*) (makes|misses) free throw technical\.', description)
        special = re.search('(.*) (makes|misses) free throw (.*) (\d) of (\d)\.', description)
        if free:
            play['primary_player'] = free.group(1)
            play['shot_made'] = free.group(2)
        elif technical:
            play['primary_player'] = technical.group(1)
            play['shot_made'] = technical.group(2)
        elif special:
            play['primary_player'] = special.group(1)
            play['shot_made'] = special.group(2)
            play['shot_type'] = special.group(3)
        else:
            print(description)
        play['shot_type'] = 'free throw'
    elif play['play_type'] == 'steal':
        steal = re.search('(.*) steals the ball from (.*)\.', description)
        play['primary_player'] = steal.group(1)
        play['secondary_player'] = steal.group(2)
    elif play['play_type'] == 'turnover' or play['play_type'] == 'kick' or play['play_type'] == 'delay of game' or play['play_type'] == 'illegal assist' or play['play_type'] == 'violation':
        turnover = re.search('(.*) is charged with a turnover due to a (.*)\.', description)
        turnover2 = re.search('(.*) with a (.*) turnover', description)
        shot_clock = re.search('(.*) with a turnover: (.*)', description)
        kick = re.search('(.*) kicks the ball\. (.*) ball\.', description)
        delay = re.search('(.*) commit a delay of game violation\. (.*) ball\.', description)
        illegal_assist = re.search('(.*) with a illegal assist turnover', description)
        violation = re.search('(.*) with a lane violation', description)
        double_lane = re.search('Violation: Double Lane', description)
        if turnover:
            play['primary_player'] = turnover.group(1)
        elif turnover2:
            play['primary_player'] = turnover2.group(1)
            play['turnover_type'] = turnover2.group(2)
        elif shot_clock:
            play['team'] = shot_clock.group(1)
            play['turnover_type'] = shot_clock.group(2)
        elif kick:
            play['primary_player'] = kick.group(1)
            play['turnover_type'] = 'kick'
        elif delay:
            play['team'] = delay.group(1)
            play['turnover_type'] = 'delay of game'
        elif illegal_assist:
            play['primary_player'] = illegal_assist.group(1)
            play['turnover_type'] = 'illegal assist'
        elif violation:
            play['primary_player'] = violation.group(1)
            play['turnover_type'] = 'lane violation'
        elif double_lane:
            play['play_type'] = 'double lane violation'
        else:
            print(description)
    elif play['play_type'] == 'blocks':
        block = re.search("(.*) blocks a ([A-Z][\w'\.-]+ [A-Z][\w'\.-]+) .*\.", description)
        play['primary_player'] = block.group(1)
        play['secondary_player'] = block.group(2)
    elif play['play_type'] == 'jump ball':
        jump_ball = re.search('Jump Ball: (.*) vs\. (.*) -- (.*) gains possession\.', description)
        if jump_ball:
            play['primary_player'] = jump_ball.group(3)
    elif play['play_type'] == 'assist':
        assist = re.search('(.*) makes an? (.*)\. (.*) with the assist\.', description)
        dunk = re.search('(.*) dunks from (\d) (foot|feet) out. (.*) with the assist\.', description)
        other_dunk = re.search('(.*) dunks\. (.*) with the assist\.', description)
        if assist:
            play['primary_player'] = assist.group(1)
            play['shot_type'] = assist.group(2)
            play['secondary_player'] = assist.group(3)
        elif dunk:
            play['primary_player'] = dunk.group(1)
            play['shot_type'] = 'dunk'
            play['shot_distance'] = dunk.group(2) 
            play['secondary_player'] = dunk.group(4)
        elif other_dunk:
            play['primary_player'] = other_dunk.group(1)
            play['shot_type'] = 'dunk'
            play['secondary_player'] = other_dunk.group(2)
        else:
            print(description)
    elif play['play_type'] == 'ejected':
        ejected = re.search('(.*) ejected', description)
        play['primary_player'] = ejected.group(1)
    elif play['play_type'] != 'start' and play['play_type'] != 'end':
        print(description)

    return play 

def play_type(play_description):
    keywords = 'illegal assist|blocks|rebound|substitution|foul|timeout|free throw|steal|turnover|start|end|jump ball|assist|kick|delay of game|violation|ejected'
    shot = 'shot|make|miss|dunk'
    
    result = re.search(keywords, play_description)

    if result:
        return result.group(0)
    elif re.search(shot, play_description):
        return 'shot'
    else:
        return ''

def get_value(play, column):
    if column in play:
        return play[column]
    else:
        return None

def get_column_name(key):
    columns = {'quarter': 'quarter', 
               'minutes': 'time-minutes', 
               'seconds': 'time-seconds',
               'home_score': 'home-score',
               'away_score': 'visitor-score',
               'team': 'team',
               'description': 'textual-description',
               'play_type': 'play_type',
               'primary_player': 'primary_player', 
               'shot_type': 'shot_type',
               'shot_made': 'shot_made',
               'shot_distance': 'shot_distance',
               'x_coord': 'x-shot-coord',
               'y_coord': 'y-shot-coord',
               'timeout_type': 'timeout_type',
               'foul_type': 'foul_type',
               'rebound_type': 'rebound_type',
               'secondary_player': 'secondary_player',
               'turnover_type': 'turnover_type'
            }
    return columns[key]

def insert_into_db(data):
    with sqlite3.connect('foxsports.db') as conn:
        for play in data['pbp']['sports-scores']['nba-scores']['nba-playbyplay']['play']:

            insert = insert_play(play['textual-description'])
            insert.update(play)
            columns = ['quarter', 'minutes', 'seconds', 'home_score', 'away_score', 'description', 'play_type', 'primary_player', 'secondary_player', 'shot_made', 'shot_distance', 'x_coord', 'y_coord', 'timeout_type', 'foul_type', 'rebound_type', 'shot_type', 'turnover_type']
            insert_data = [get_value(insert, get_column_name(d)) for d in columns]

            conn.execute('INSERT INTO play_by_play (' + ','.join(columns) + ') VALUES (' + ','.join(['?'] * len(columns)) + ')', insert_data)

    

def parse(games_dir):
    for f in glob.glob(os.path.join(games_dir, '*.html')):
        #print(f)
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

"""
[play['quarter'], 
 play['time-minutes'], 
 play['time-seconds'], 
 play['home-score'], 
 play['visitor-score'],
 play['textual-description'],
 play_type,
 player,
 made,
 distance,
 play['x-shot-coord'],
 play['y-shot-coord']])
"""
