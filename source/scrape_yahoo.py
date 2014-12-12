# NBA NLP - Final Project - CSC 582
# Data Scraping  - Yahoo Sports
# Jacob Bustamante

import csv, re, os, sqlite3
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup as soup
from urllib.request import urlretrieve


class yahoo_game:
    game_date = ''
    home_team = ''
    away_team = ''
    season = ''
    game_type = ''
    game_time = ''
    commentary = []
    stats = {}
    
    def __init__(self, url, local=False):
        if local:
            game_datetime = datetime.strptime(url[:url.index('_')], '%Y%m%d');
            self.game_date = game_datetime.strftime('%Y-%m-%d')
            self.home_team = url[url.index('@')+1:url.index('.')]
            self.away_team = url[url.index('_')+1:url.index('@')]
            self.season = str(game_datetime.year if game_datetime.month > 8 else game_datetime.year - 1)
            self.game_type = 'Regular Season'
        else:
            pass
    
    def insert_string(self):
        self.game_info = (self.season, self.game_date, self.home_team, self.away_team, self.game_type)
        return 'INSERT INTO game (season, game_date, home_team, away_team, game_type) VALUES (' + ','.join(['?'] * len(self.game_info)) + ')'

class play:
    def __init__(self, quarter, time_string, event_string, game_id):
        self.data = {}
        self.data['game_id'] = game_id
        self.data['quarter'] = quarter
        self.data['minutes'] = int(time_string[:time_string.index(':')] if time_string[0] != ':' else 0)
        self.data['seconds'] = float(time_string[time_string.index(':') + 1:])
        self.data['description'] = event_string
        self.parse_event()
        self.data.update(parse_play_type(self.data))
    
    def parse_event(self):
        self.data['play_type'] = self.get_play_type(self.data['description'].lower())
        
    def get_play_type(self, play_description):
        #keywords = 'blocks|rebound|substitution|foul|timeout|free throw|steal|jump ball|assist|ejected|goaltending'
        keywords = 'jump ball|steals|rebound|foul|charge|enters game|timeout|block|technical|free throw'
        #shot = 'shot|make|miss|dunk'
        shot = 'dunk|dunks|misses|layup|makes'
        #turnover = 'kick|delay of game|violation|turnover|illegal assist'
        turnover = 'turnover|kicked|bad pass|delay of game'
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
            return 'NULL'
    
    def insert_string(self):
        columns = ['event_description', 'detail_description', 'game_id', 'quarter', 'minutes', 'seconds', 'home_score', 'away_score', 'description', 'play_type', 'primary_player', 'secondary_player', 'shot_made', 'shot_distance', 'x_coord', 'y_coord', 'timeout_type', 'foul_type', 'rebound_type', 'shot_type', 'turnover_type']
        self.insert_data = [self.data.get(self.get_column_name(d), '') for d in columns]
        return 'INSERT INTO play_by_play (' + ','.join(columns) + ') VALUES (' + ','.join(['?'] * len(columns)) + ')'
    
    def print_event(self):
        print(str(self.data['quarter']), str(self.data['minutes']) + ':' + str(self.data['seconds']), self.data['play_type'], self.data.get('primary_player',''), self.data['description'])
        
    def parsed(self):
        return self.data['play_type'] is not 'NULL'
    
    def get_column_name(self, key):
        columns = {
            'quarter': 'quarter', 
            'minutes': 'time-minutes', 
            'seconds': 'time-seconds',
            'home_score': 'home-score',
            'away_score': 'visitor-score',
            'team': 'team',
            #'description': 'textual-description',
            'description': 'description',
            'play_type': 'play_type',
            'primary_player': 'primary_player', 
            'event_description': 'event_description',
            'detail_description': 'detail_description',
            'shot_type': 'shot_type',
            'shot_made': 'shot_made',
            'shot_distance': 'shot_distance',
            'x_coord': 'x-shot-coord',
            'y_coord': 'y-shot-coord',
            'timeout_type': 'timeout_type',
            'foul_type': 'foul_type',
            'rebound_type': 'rebound_type',
            'secondary_player': 'secondary_player',
            'turnover_type': 'turnover_type',
            'game_id': 'game_id'
        }
        return columns[key]


def parse_play_type(data):
    play_type = data['play_type']
    description = data['description']
    
    shot_type = ['shot', 'make', 'miss']

    if play_type in shot_type:
        pass#data.update(parse_shot(description))
    elif play_type == 'rebound':
        pass#data.update(parse_rebound(description))
    elif play_type == 'foul':
        pass#data.update(parse_foul(description))
    elif play_type == 'timeout':
        pass#data.update(parse_timeout(description))
    elif play_type == 'substitution':
        pass#data.update(parse_substitution(description))
    elif play_type == 'free throw':
        pass#data.update(parse_free_throw(description))
    elif play_type == 'steal':
        pass#data.update(parse_steal(description))
    elif play_type == 'turnover':
        pass#data.update(parse_turnover(description))
    elif play_type == 'blocks':
        pass#data.update(parse_block(description))
    elif play_type == 'jump ball':
        pass#data.update(parse_jump_ball(description))
    elif play_type == 'assist':
        pass#data.update(parse_assist(description))
    elif play_type == 'ejected':
        pass#data.update(parse_ejection(description))
    elif play_type == 'quarter_break':
        pass
    
    return data


def scrape_play_by_play(raw, game_id):
    souped = soup(raw)
    
    # gets array of [time, event, time, event, time, event, ...]
    temp_dl = souped.find_all("dl")
    dd = max(temp_dl, key=len).find_all("dd")
    time_event = [(dd[i].text.strip(), dd[i+1].text.strip()) for i in range(0, len(dd), 2)]

    plays = []
    quarter = 1
    for i, p in enumerate(time_event):
        plays.append(play(quarter, p[0], p[1], game_id))
        if i < len(time_event) - 1 and int(p[0].split('.')[0].replace(':','')) < int(time_event[i+1][0].split('.')[0].replace(':','')):
            quarter += 1
    
    return plays


def parse_page(url, raw, local=False):
    game = yahoo_game(url, local)

    with sqlite3.connect('yahoo.db') as conn:
        cursor = conn.cursor()
        cursor.execute(game.insert_string(), game.game_info)
        game_id = cursor.lastrowid
        
        for play in scrape_play_by_play(raw, game_id):
            play.print_event()
            cursor.execute(play.insert_string(), play.insert_data)
    
    

def reset_sql():
    with sqlite3.connect('yahoo.db') as conn:
        cursor = conn.cursor()
        cursor.execute("delete from play_by_play")
        cursor.execute("delete from game")
        cursor.execute("delete from sqlite_sequence where name = 'game' or name = 'play_by_play'")
        
"""
def create_game_url_list():
    base_url = "http://sports.yahoo.com/nba/"
    
    csv = open("leagues_NBA_2014_games_games.csv").read().rstrip()
    games = [game.split(',') for game in csv.split('\n')]
    
    urls = []
    for game in games:
        date_string = datetime.strptime(game[0], '%a %b %d %Y').strftime('%Y%m%d')
        team_string = '-'.join(game[2].lower().split()) + '-' + '-'.join(game[4].lower().split())
        unique_string = team_string + '-' + date_string + team_id[game[4]]
        full_url = base_url + unique_string + '/'
        urls.append(full_url)
    
    return urls

def get_game_url_list():
    directory = "./webpages/yahoo/2013_season_urls.txt"
    url_list = list(map(lambda l: l.strip(), open(directory).readlines()))
    return url_list

def crawl_web_pages():
    urls = get_game_url_list()
    
    for url in urls:
        date_string = url[-11:-3]
        teams = ' '.join(url[28:-12].split('-')[:3])
        away = [team_abrvs[name] for name in team_abrvs if name.lower() in teams][0]
        home = team_abrvs[[name for name in team_id if team_id[name] == url[-3:-1]][0]]
        name = date_string + '_' + away + '@' + home + '.html'
        
        print("downloading:", name)
        urlretrieve(url, './webpages/yahoo/' + name)
        sleep(1)
"""

def main():
    reset_sql()
    
    directory = "./webpages/yahoo/"
    for game_file in os.listdir(directory)[:2]:
        if game_file[-5:] == '.html':
            file_name = directory + game_file
            with open(file_name) as open_file:
                raw = open_file.read()
            parse_page(game_file, raw, local=True)

if __name__ == '__main__':
    main()


team_id = {
    'Atlanta Hawks' : '01',
    'Boston Celtics' : '02',
    'Brooklyn Nets' : '17',
    'Charlotte Bobcats' : '30',
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
    'Memphis Grizzlies' : '29',
    'Miami Heat' : '14',
    'Milwaukee Bucks' : '15',
    'Minnesota Timberwolves' : '16',
    'New Orleans Pelicans' : '03',
    'New York Knicks' : '18',
    'Oklahoma City Thunder' : '25',
    'Orlando Magic' : '19',
    'Philadelphia 76ers' : '20',
    'Phoenix Suns' : '21',
    'Portland Trail Blazers' : '22',
    'Sacramento Kings' : '23',
    'San Antonio Spurs' : '24',
    'Toronto Raptors' : '28',
    'Utah Jazz' : '26',
    'Washington Wizards' : '27'
}

team_abrvs = {
    'Atlanta Hawks' : 'ATL',
    'Boston Celtics' : 'BOS',
    'Brooklyn Nets' : 'BKN',
    'Charlotte Bobcats' : 'CHA',
    'Chicago Bulls' : 'CHI',
    'Cleveland Cavaliers' : 'CLE',
    'Dallas Mavericks' : 'DAL',
    'Denver Nuggets' : 'DEN',
    'Detroit Pistons' : 'DET',
    'Golden State Warriors' : 'GS',
    'Houston Rockets' : 'HOU',
    'Indiana Pacers' : 'IND',
    'Los Angeles Clippers' : 'LAC',
    'Los Angeles Lakers' : 'LAL',
    'Memphis Grizzlies' : 'MEM',
    'Miami Heat' : 'MIA',
    'Milwaukee Bucks' : 'MIL',
    'Minnesota Timberwolves' : 'MIN',
    'New Orleans Pelicans' : 'NO',
    'New York Knicks' : 'NY',
    'Oklahoma City Thunder' : 'OKC',
    'Orlando Magic' : 'ORL',
    'Philadelphia 76ers' : 'PHI',
    'Phoenix Suns' : 'PHO',
    'Portland Trail Blazers' : 'POR',
    'Sacramento Kings' : 'SAC',
    'San Antonio Spurs' : 'SA',
    'Toronto Raptors' : 'TOR',
    'Utah Jazz' : 'UTA',
    'Washington Wizards' : 'WAS'
}
# game_date = datetime.strptime(game[0], '%a %b %d %Y').strftime('%Y%m%d')
# game = [date, Box Score, Away team, score, Home team, score, OT?, notes?]
# http://sports.yahoo.com/nba/chicago-bulls-miami-heat-2013102914/
    
"""
14|1|1|11|43|2|0||Udonis Haslem makes a dunk shot. Mario Chalmers with the assist.|Field Goal Made|Dunk Shot|assist|Udonis Haslem|Mario Chalmers|dunk|makes||0.2|0.3||||
27|1|1|9|42|2|5||Jimmy Butler makes a 3-point jump shot from 23 feet out. Joakim Noah with the assist.|Field Goal Made|Jump Shot|assist|Jimmy Butler|Joakim Noah|3-point jump|makes|23|23.3|1.4||||
163|1|2|7|38|29|20||Shane Battier makes a 3-point jump shot from 23 feet out. Ray Allen with the assist.|Field Goal Made|Jump Shot|assist|Shane Battier|Ray Allen|3-point jump|makes|23|-23.2|1.5||||

1|2013|2013-10-29|MIA|CHI|Regular Season
2|2013|2013-10-29|LAL|LAC|Regular Season

create table play_by_play (
  id integer not null primary key autoincrement,
  game_id integer references game(id),
  quarter integer,
  minutes integer,
  seconds integer,
  home_score integer,
  away_score integer,
  team text,
  description text,
  event_description text,
  detail_description text,
  play_type text default 'other', 
  primary_player text,
  secondary_player,
  shot_type text,
  shot_made text,
  shot_distance integer,
  x_coord real,
  y_coord real,
  rebound_type,
  foul_type,
  timeout_type,
  turnover_type
);

create table game (
  id integer primary key autoincrement,
  season text,
  game_date date,
  home_team text,
  away_team text,
  game_type text
);


db_columns = {
    'quarter': 'quarter', 
    'minutes': 'time-minutes', 
    'seconds': 'time-seconds',
    'home_score': 'home-score',
    'away_score': 'visitor-score',
    'team': 'team',
    'description': 'textual-description',
    'play_type': 'play_type',
    'primary_player': 'primary_player', 
    'event_description': 'event_description',
    'detail_description': 'detail_description',
    'shot_type': 'shot_type',
    'shot_made': 'shot_made',
    'shot_distance': 'shot_distance',
    'x_coord': 'x-shot-coord',
    'y_coord': 'y-shot-coord',
    'timeout_type': 'timeout_type',
    'foul_type': 'foul_type',
    'rebound_type': 'rebound_type',
    'secondary_player': 'secondary_player',
    'turnover_type': 'turnover_type',
    'game_id': 'game_id'
}
"""