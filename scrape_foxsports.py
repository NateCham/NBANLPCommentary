import urllib
import glob
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import os
import sqlite3
import insert_into_db


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

shot_adjectives = ['driving', 'finger roll', 'fade away', 'floating', 'step back', 'turnaround', 'alley oop', 'bank', 'putback', 'reverse', 'running', 'tip', 'slam']

shot_types = ['3-point', 'jump', 'layup', 'dunk', 'hook']

class Game:
    """A game between two teams on a date"""

    def __init__(self, game_date, home_team, away_team):
        self.game_date = game_date
        self.home_team = home_team
        self.away_team = away_team
        self.plays = {}

    def __repr__(self):
        return '{game_date: ' + self.game_date + ', home_team: ' + home_team + ', away_team: ' + away_team + '}'

def parse_shot(description):
    play = {}

    shot = re.search('(.*) (makes|misses) an? (.*) shot? from (\d+) (feet|foot) out\.', description)
    shot2 = re.search('(.*) (makes|misses) an? (.*) shot?\.', description)
    dunk = re.search('(.*) dunks\.', description)
    dunks_from = re.search('(.*) dunks from (\d) (foot|feet) out\.', description)
    if shot:
        play['primary_player'] = shot.group(1)
        play['shot_made'] = shot.group(2)
        play['shot_type'] = shot.group(3)
        play['shot_distance'] = shot.group(4)
    elif shot2:
        play['primary_player'] = shot2.group(1)
        play['shot_made'] = shot2.group(2)
        play['shot_type'] = shot2.group(3)
    elif dunk:
        play['primary_player'] = dunk.group(1)
        play['shot_type'] = 'dunk'
        play['shot_made'] = 'made'
    elif dunks_from:
        play['primary_player'] = dunks_from.group(1)
        play['shot_type'] = 'dunk'
        play['shot_made'] = 'made'
        play['shot_distance'] = dunks_from.group(2)

    return play

def parse_rebound(description):
    play = {}

    rebound = re.search('(.*) with an? (offensive|defensive) rebound\.', description)
    play['primary_player'] = rebound.group(1)
    play['rebound_type'] = rebound.group(2)

    return play

def parse_foul(description):
    play = {}

    foul = re.search('(.*) foul committed by (.*)\.', description)
    if foul:
        play['foul_type'] = foul.group(1)
        play['primary_player'] = foul.group(2)

    return play

def parse_timeout(description):
    play = {}

    timeout = re.search('(.*) take a (.*) timeout\.', description)
    official = re.search("Official's timeout\.", description)
    if timeout:
        play['team'] = timeout.group(1)
        play['timeout_type'] = timeout.group(2)
    elif official:
        play['timeout_type'] = 'official'

    return play

def parse_substitution(description):
    play = {}

    sub = re.search('Substitution: (.*) in for (.*)\.', description)
    play['primary_player'] = sub.group(1)
    play['secondary_player'] = sub.group(2)

    return play

def parse_free_throw(description):
    play = {}

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
    play['shot_type'] = 'free throw'

    return play

def parse_steal(description):
    play = {}

    steal = re.search('(.*) steals the ball from (.*)\.', description)
    play['primary_player'] = steal.group(1)
    play['secondary_player'] = steal.group(2)

    return play


def parse_turnover(description):
    play = {}

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
        #print(turnover.group(2))
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

    return play

def parse_jump_ball(description):
    play = {}

    jump_ball = re.search('Jump Ball: (.*) vs\. (.*) -- (.*) gains possession\.', description)
    if jump_ball:
        play['primary_player'] = jump_ball.group(3)

    return play

def parse_block(description):
    play = {}

    block = re.search("(.*) blocks a ([A-Z][\w'\.-]+ [A-Z][\w'\.-]+) .*\.", description)
    play['primary_player'] = block.group(1)
    play['secondary_player'] = block.group(2)

    return play

def parse_assist(description):
    play = {}

    assist = re.search('(.*) makes an? ([^\.]+) shot?\. (.*) with the assist\.', description)
    assist2 = re.search('(.*) makes an? (.*) shot? from (\d+) (feet|foot) out\. (.*) with the assist\.', description)
    dunk = re.search('(.*) dunks from (\d) (foot|feet) out. (.*) with the assist\.', description)
    other_dunk = re.search('(.*) dunks\. (.*) with the assist\.', description)
    if assist2:
        #print('assist2')
        play['primary_player'] = assist2.group(1)
        play['shot_type'] = assist2.group(2)
        play['shot_distance'] = assist2.group(3)
        play['secondary_player'] = assist2.group(5)
    elif assist:
        #print(description)
        #print('assist')
        play['primary_player'] = assist.group(1)
        play['shot_type'] = assist.group(2)
        play['secondary_player'] = assist.group(3)
    elif dunk:
        #print('dunk')
        play['primary_player'] = dunk.group(1)
        play['shot_type'] = 'dunk'
        play['shot_distance'] = dunk.group(2) 
        play['secondary_player'] = dunk.group(4)
    elif other_dunk:
        #print('other_dunk')
        play['primary_player'] = other_dunk.group(1)
        play['shot_type'] = 'dunk'
        play['secondary_player'] = other_dunk.group(2)

    play['shot_made'] = 'makes'
    return play

def parse_ejection(description):
    play = {}

    ejected = re.search('(.*) ejected', description)
    play['primary_player'] = ejected.group(1)

    return play


def insert_play(description):
    play = {}
    play['play_type'] = play_type(description.lower())
    shot_type = ['shot', 'make', 'miss']

    if play['play_type'] in shot_type:
        play.update(parse_shot(description))
    elif play['play_type'] == 'rebound':
        play.update(parse_rebound(description))
    elif play['play_type'] == 'foul':
        play.update(parse_foul(description))
    elif play['play_type'] == 'timeout':
        play.update(parse_timeout(description))
    elif play['play_type'] == 'substitution':
        play.update(parse_substitution(description))
    elif play['play_type'] == 'free throw':
        play.update(parse_free_throw(description))
    elif play['play_type'] == 'steal':
        play.update(parse_steal(description))
    elif play['play_type'] == 'turnover':
        play.update(parse_turnover(description))
    elif play['play_type'] == 'blocks':
        play.update(parse_block(description))
    elif play['play_type'] == 'jump ball':
        play.update(parse_jump_ball(description))
    elif play['play_type'] == 'assist':
        play.update(parse_assist(description))
    elif play['play_type'] == 'ejected':
        play.update(parse_ejection(description))
    elif play['play_type'] == 'quarter_break':
        dummy = 1
        #print(play['play_type'] + ' -- ' + description)

    return play 

def play_type(play_description):
    keywords = 'blocks|rebound|substitution|foul|timeout|free throw|steal|jump ball|assist|ejected|goaltending'
    shot = 'shot|make|miss|dunk'
    turnover = 'kick|delay of game|violation|turnover|illegal assist'
    quarter_break = 'start|end'
    
    result = re.search(keywords, play_description)

    if result:
        return result.group(0)
    elif re.search(turnover, play_description):
        return 'turnover'
    elif re.search(shot, play_description):
        return 'shot'
    elif re.search(quarter_break, play_description):
        return 'quarter_break'
    else:
        return ''

def get_player(p):
    player = {}
    player['first_name'] = p['name']['first-name']
    player['last_name'] = p['name']['last_name']
    player['weight'] = p['weight']['pounds']
    player['height'] = p['height']['inches']
    player['number'] = p['player-number']['number']
    player['experience'] = p['experience']['experience']
    player['school'] = p['school']['school']
    player['primary_position'] = p['primary-position']['name']
    player['foxsports-id'] = p['player-code']['global-id']
    player['team_code'] = p['team-code']['id']

def add_players(playerInfo):
    for p in playerInfo:
        get_player(p)

def parse(games_dir):
    for html_file in glob.glob(os.path.join(games_dir, '*.html')):
        with open(html_file, errors='ignore') as open_file:
            soup = BeautifulSoup(open_file)
            script = soup.find('script', text=re.compile('nba\.initialUpdate'))
            eastern_time = re.search(r'nba\.easternStartTime\s=\s({.*});', script.string).group(1)
            json_data = re.search(r'nba\.initialUpdate\s*=\s*({.*?})\s*;', script.string).group(1)
            json_object = json.loads(json_data)
            insert_into_db.insert_into_db(json_object)

def download_gamepages(games, games_dir):
    base_url = 'http://www.foxsports.com/nba/gameTrax?gameId='
    for g in games:
        game_url = g.game_date + teams[g.home_team]
        print('downloading: ' + g.game_date + ' - ' + g.away_team + ' @ ' + g.home_team)
        urllib.request.urlretrieve(base_url + game_url, games_dir + g.game_date + '_' + g.away_team + '@' + g.home_team + '.html')

if __name__ == '__main__':
    full_schedule = 'leagues_NBA_2014_games_games.csv'
    games_dir = 'webpages/foxsports_gamepages/'
    games = []

    with open(full_schedule) as schedule:
        for line in schedule:
            game = line.split(',')
            game_date = datetime.strptime(game[0], '%a %b %d %Y').strftime('%Y%m%d')
            home_team = game[4]
            away_team = game[2]

            games.append(Game(game_date, home_team, away_team))

    #download_gamepages(games, games_dir)
    parse(games_dir)
