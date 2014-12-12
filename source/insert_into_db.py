import sqlite3
import re
import scrape_foxsports


columns = ['points_worth', 'event_description', 'detail_description', 'game_id', 'quarter', 'minutes', 'team_id', 'seconds', 'home_score', 'away_score', 'description', 'play_type', 'primary_player', 'secondary_player', 'shot_made', 'shot_distance', 'x_coord', 'y_coord', 'timeout_type', 'foul_type', 'rebound_type', 'shot_type', 'turnover_type', 'p_player_id', 's_player_id']

def get_column_name(key):
    columns = {'quarter': 'quarter', 
               'minutes': 'time-minutes', 
               'seconds': 'time-seconds',
               'home_score': 'home-score',
               'away_score': 'visitor-score',
               'team_id': 'team_id',
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
               'game_id': 'game_id',
               'points_worth': 'points_worth',
               'p_player_id': 'primary_player_id',
               's_player_id': 'secondary_player_id'
            }
    return columns[key]

def get_player(p):
    player = {}
    player['first_name'] = p['name']['first-name']
    player['last_name'] = p['name']['last-name']
    #player['weight'] = p['weight']['pounds']
    #player['height'] = p['height']['inches']
    player['number'] = p['player-number']['number']
    #player['experience'] = p['experience']['experience']
    #player['school'] = p['school']['school']
    player['primary_position'] = p['primary-position']['name']
    player['foxsports_id'] = p['player-code']['global-id']
    player['team_id'] = p['team-code']['id']

    return player

def add_players(playerInfo):
    players = []
    for p in playerInfo:
        players.append(get_player(p))
    return players
    

def get_value(play, column):
    if column in play:
        return play[column]
    else:
        return None

def insert_into_db(data):
    team_id = data['gameInfo']['home-team']['team-code']['id']
    team_city = data['gameInfo']['home-team']['team-city']['city']
    team_alias = data['gameInfo']['home-team']['team-name']['alias'].upper()
    team_name = data['gameInfo']['home-team']['team-name']['name']

    team_info = [team_id, team_city, team_alias, team_name]
        
    home_team = data['gameInfo']['home-team']['team-code']['id']
    away_team = data['gameInfo']['visiting-team']['team-code']['id']
    season = data['gameInfo']['season']['season']
    game_date = data['gameInfo']['date']
    game_type = data['gameInfo']['gametype']['type']
    home_score = data['gameInfo']['home-team-score']['score']
    away_score = data['gameInfo']['visiting-team-score']['score']
    total_quarters = data['gameInfo']['total-quarters']['total']
    game_code = data['gameInfo']['gamecode']['code']
    
    game_info = [season, game_date, home_team, away_team, game_type, game_code]

    name = data['gameInfo']['stadium']['name']
    country = data['gameInfo']['stadium']['country']
    state = data['gameInfo']['stadium']['state']
    city = data['gameInfo']['stadium']['city']
    fox_id = data['gameInfo']['stadium']['id']
    stadium_info = [name, country, state, city, fox_id]
    

    with sqlite3.connect('foxsports.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO game (season, game_date, home_team, away_team, game_type, game_code) VALUES (' + ','.join(['?'] * len(game_info)) + ')', game_info)
        game_id = cursor.lastrowid

        schedule_info = [game_date, home_team, away_team, home_score, away_score, season, game_id]
        cursor.execute('INSERT INTO schedule (game_date, home_team_id, away_team_id, home_team_score, away_team_score, season, game_id) VALUES (' + ','.join(['?'] * len(schedule_info)) + ')', schedule_info)
        cursor.execute('INSERT OR IGNORE INTO team (id, city, alias, name) VALUES (' + ','.join(['?'] * len(team_info)) + ')', team_info)
        cursor.execute('INSERT OR IGNORE INTO stadium (name, country, state, city, fox_id) VALUES (' + ','.join(['?'] * len(stadium_info)) + ')', stadium_info)
        
        for p in add_players(data['playerInfo']):
            player_info = [p['first_name'], p['last_name'], p['number'], p['primary_position'], p['foxsports_id'], p['team_id']]
            #put dict to list function call here
            cursor.execute('INSERT OR IGNORE INTO player (first_name, last_name, jersey_number, primary_position, foxsports_id, team_id) VALUES (' + ','.join(['?'] * len(player_info)) + ')', player_info)
        for play in data['pbp']['sports-scores']['nba-scores']['nba-playbyplay']['play']:
            
            insert = scrape_foxsports.insert_play(play['textual-description'])
            insert.update(play)
            insert['points_worth'] = play['points-type']
            insert['event_description'] = play['event-description']
            insert['detail_description'] = play['detail-description']
            insert['game_id'] = game_id
            insert['team_id'] = play['global-team-code-1']
            insert['primary_player_id'] = play['global-player-id-1']
            insert['secondary_player_id'] = play['global-player-id-2']

            insert_data = [get_value(insert, get_column_name(d)) for d in columns]

            cursor.execute('INSERT INTO play_by_play (' + ','.join(columns) + ') VALUES (' + ','.join(['?'] * len(columns)) + ')', insert_data)
