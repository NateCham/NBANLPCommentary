import requests
import urllib3
import glob
import time
import urllib
from bs4 import BeautifulSoup
import os
from datetime import datetime

teams = {
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

class Game:
    """A game between two teams on a date"""

    def __init__(self, game_date, home_team, away_team):
        self.game_date = game_date
        self.home_team = home_team
        self.away_team = away_team

    def __repr__(self):
        return '{game_date: ' + self.game_date + ', home_team: ' + home_team + ', away_team: ' + away_team + '}'

class Play:
    """A play with a time, score, team, and play"""

    def __init__(self, qtr, time, score, team, play):
        self.quarter = qtr
        self.time = time
        self.score = score
        self.team = team
        self.play = play

    def __repr__(self):
        return '{quarter: ' + self.quarter + ', time: ' + self.time + ', score: ' + self.score + ', team: ' + self.team + ', play: ' + self.play + '}'

def parse(games):
    for f in glob.glob(os.path.join(games, '*.html')):
        print(f)
        with open(f, errors='ignore') as fi:
            soup = BeautifulSoup(fi)
            plays = soup.find('table', {'class' : 'data condensed stacked'})
            list_of_plays = plays.find_all('tr', {'align' : 'right'})

            all_plays = []

            for p in list_of_plays:
                play = p.find_all('td')
                if (len(play) == 4 and play[0].text != 'TIME'):
                    all_plays.insert(0, Play(quarter, play[0].text, play[1].text.strip(), play[2].text, play[3].text.strip()))
                elif (len(play) == 2):
                    all_plays.insert(0, Play(quarter, play[0].text, '', '', play[1].text))
                elif (len(play) == 1):
                    quarter = play[0].text.strip()

            all_plays[0].score = '0-0'
            for i in range(0, len(all_plays)):
                if all_plays[i].score == '':
                   all_plays[i].score = all_plays[i-1].score 
                print(all_plays[i])

if __name__ == "__main__":
    full_schedule = "/Users/natecham/Downloads/leagues_NBA_2014_games_games.csv"
    base_url = 'http://www.cbssports.com/nba/gametracker/playbyplay/'
    games_dir = '/Users/natecham/Desktop/nba_games/'
    games = []

    with open(full_schedule) as schedule:
        for line in schedule:
            game = line.split(',')
            game_date = datetime.strptime(game[0], '%a %b %d %Y').strftime('%Y%m%d')
            home_team = game[4]
            away_team = game[2]

            games.append(Game(game_date, home_team, away_team))
        

    for g in games:
        play_by_play = 'NBA_' + g.game_date + '_' + teams[g.away_team] + '@' + teams[g.home_team]
        #time.sleep(2)
        print("downloading: " + play_by_play)
        #urllib.request.urlretrieve(base_url + play_by_play, '/Users/natecham/Desktop/nba_games/' + play_by_play + '.html')
        #r = requests.get(base_url + play_by_play)

    parse(games_dir)
