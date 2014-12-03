# NBA NLP - Final Project - CSC 582
# Commentary Generator - Main
# Jacob Bustamante

import sys, re, sqlite3, random
import comment_strings


DEBUG = False

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
conn = sqlite3.connect('foxsports.db')
conn.row_factory = dict_factory


def event_comment_from_list(comments, play):
    i = random.randint(0, len(comments) - 1)
    return comments[i][0] % tuple(play[key] for key in comments[i][1])
    


bid_shot_counts = {'bid_shot_default':0, 'bid_shot_fastbreak':0, 'bid_shot_first':0, 'bid_shot_longest':0}

def bid_shot_fastbreak(play):
    if play['play_index'] - 1 <= 0 or play['shot_made'] != 'makes':
        return (0, "fastbreak!", 'bid_shot_fastbreak')
    
    last_play = game_plays[play['play_index'] - 1]
    
    if (last_play['minutes'] * 60 + last_play['seconds']) - (play['minutes'] * 60 + play['seconds']) <= 5:
        if last_play['play_type'] == 'steal':
            play['fastbreak_creator'] = last_play['primary_player']
            play['fastbreak_play'] = 'steal'
        elif last_play['play_type'] == 'blocks':
            play['fastbreak_creator'] = last_play['secondary_player']
            play['fastbreak_play'] = 'block'
        elif last_play['play_type'] == 'rebound' and last_play['rebound_type'] == 'defensive':
            play['fastbreak_creator'] = last_play['primary_player']
            play['fastbreak_play'] = 'rebound'
        else:
            return (0, "fastbreak!", 'bid_shot_fastbreak')
            
        if play['play_type'] == 'assist':
            if play['fastbreak_creator'] == play['secondary_player']:
                return (0.75, event_comment_from_list(comment_strings.fastbreak_112_comments, play), 'bid_shot_fastbreak')
            elif play['fastbreak_creator'] == play['primary_player']:
                return (0.8, event_comment_from_list(comment_strings.fastbreak_121_comments, play), 'bid_shot_fastbreak')
            else:
                return (0.9, event_comment_from_list(comment_strings.fastbreak_123_comments, play), 'bid_shot_fastbreak')
        else:
            if play['primary_player'] == play['fastbreak_creator']:
                return (0.8, event_comment_from_list(comment_strings.fastbreak_11_comments, play), 'bid_shot_fastbreak')
            else:
                return (0.7, event_comment_from_list(comment_strings.fastbreak_12_comments, play), 'bid_shot_fastbreak')
    else:
        return (0, "fastbreak!", 'bid_shot_fastbreak')
   
    return (1, "fastbreak!", 'bid_shot_fastbreak')

def bid_shot_first(play):
    if play['quarter'] == 1:
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) as count FROM play_by_play "
                     "where game_id = " + str(play['game_id']) +
                     " and play_type in ('shot', 'assist', 'blocks')"
                     " and id < " + str(play['pbp_id']))
        shot_count = cursor.fetchone()['count']
        
        # First shot of the game
        if shot_count == 0:
            return (0.9, event_comment_from_list(comment_strings.shot_first_comments, play), 'bid_shot_first')
    
    return (0, "", 'bid_shot_first')

def bid_shot_longest(play):
    if play['event_description'] != 'Field Goal Made' or not play['shot_distance']:
        return (0, "", 'bid_shot_longest')
    
    cursor = conn.cursor()
    cursor.execute("SELECT max(shot_distance) as max_shot FROM play_by_play "
                   "WHERE event_description = 'Field Goal Made' AND id < " + str(play['pbp_id']))
    max_shot_distance = cursor.fetchone()['max_shot']
    
    cursor.execute("SELECT max(shot_distance) as max_shot FROM play_by_play "
                   "WHERE event_description = 'Field Goal Made' AND id < " + str(play['pbp_id']) +
                   " AND p_player_id = '" + str(play['p_player_id']) + "'")
    max_player_shot_distance = cursor.fetchone()['max_shot']
    
    if max_shot_distance and play['shot_distance'] > 30 and play['shot_distance'] > max_shot_distance:
        return (1, event_comment_from_list(comment_strings.shot_longest_comments, play), 'bid_shot_longest')
    elif max_player_shot_distance and play['shot_distance'] > 30 and play['shot_distance'] > max_player_shot_distance:
        return (1, event_comment_from_list(comment_strings.shot_longest_player_comments, play), 'bid_shot_longest')
    else:
        return (0, "", 'bid_shot_longest')
    
def bid_shot_default(play):
    return (0.25, play['description'], 'bid_shot_default')


def event_shot(play):
    global game_plays
    
    output = []
    
    # bids are (bid_number, comment, bid_function_name)
    max_bid = max([globals()[bid_function](play) for bid_function in bid_shot_counts.keys()])
    bid_shot_counts[max_bid[2]] += 1
    
    output.append(max_bid[1])
    return output


def display_starting_lineup(game_id):
    cursor = conn.cursor()
    cursor.execute("select city, name, group_concat(first_name || ' ' || last_name, ', ') as starters "
                   "from play_by_play join player on p_player_id = foxsports_id join team on play_by_play.team_id = team.id where game_id = " + str(game_id) + " and description = 'Starting Lineup' group by play_by_play.team_id;")
    lineups = cursor.fetchall()
    
    comments = [
        ("The starting lineup for the %s %s is %s.", ('city', 'name', 'starters')),
        ("%s are starting tonight for the %s %s.", ('starters', 'city', 'name'))
    ]
    
    output = []
    for l in lineups:
        i = random.randint(0, len(comments) - 1)
        output.append(comments[i][0] % tuple(l[key] for key in comments[i][1]))
    
    return output

def event_game_start():
    global DEBUG, game_info, game_plays
    
    output = []
    output.append("The " + game_info['away_team'] + " are playing the " + game_info['home_team'] + ".")
    output.extend(display_starting_lineup(game_info['game_id']))

    return output


def parse_comment(output_comments, game_time):
    time_string = str(game_time[0]) + " " + str(game_time[1]) + ':' + str(game_time[2])
    
    if output_comments:
        print(time_string)
        for comment in output_comments:
            print(comment)
        print()
    

def get_game_info(game_id):
    headers = ['season', 'game_date', 'home_team', 'away_team', 'game_type']
    
    with sqlite3.connect('foxsports.db') as conn:
        cursor = conn.cursor();
        cursor.execute("SELECT season, game_date, t1.name, t2.name, game_type "
                       "FROM game JOIN team as t1 "
                       " ON home_team = t1.id JOIN team as t2 "
                       " ON away_team = t2.id "
                       "WHERE game.id = " + str(game_id))
        data = cursor.fetchone()
    
    if not data:
        return None
    else:
        game_info = dict(zip(headers, data))
        game_info['game_id'] = game_id
        return game_info

def get_game_plays(game_id):
    plays = []
    headers = ['play_by_play.id as pbp_id', 'event_description', 'detail_description', 'game_id', 'quarter', 'minutes', 'seconds', 'home_score', 'away_score', 'description', 'play_type', 'primary_player', 'secondary_player', 'shot_made', 'shot_distance', 'x_coord', 'y_coord', 'timeout_type', 'foul_type', 'rebound_type', 'shot_type', 'turnover_type', 'points_worth', 'p_player_id', 's_player_id']
    
    #with sqlite3.connect('foxsports.db') as conn:
    cursor = conn.cursor()
    #cursor.execute("SELECT " + ','.join(headers) + " FROM play_by_play where game_id = " + str(game_id))
    cursor.execute("SELECT " + ','.join(headers) + ", name, team.id as t_id FROM play_by_play JOIN team ON team.id = play_by_play.team_id where game_id = " + str(game_id))
    data = cursor.fetchall()
    
    if not data:
        return None
    #plays = [dict(zip(headers, play)) for play in data]
    
    return data



def main():
    global DEBUG, game_info, game_plays
    
    if len(sys.argv) > 2:
        if sys.argv[2] == 'debug':
            DEBUG = True
    if len(sys.argv) > 1:
        game_id = sys.argv[1]
    else:
        game_id = 0
    
    if DEBUG:
        print('game_id:', game_id)
    
    
    
    game_info = get_game_info(game_id)
    if not game_info:
        print('game_id',game_id,'not found')
    game_plays = get_game_plays(game_id)


    # Start game
    parse_comment(event_game_start(), (0,0,0))
    for play_index, play in enumerate(game_plays):
        play['play_index'] = play_index
        if play['play_type'] in ['shot', 'assist', 'blocks']:
            game_time = (play['quarter'], play['minutes'], play['seconds'])
            parse_comment(event_shot(play), game_time)

if __name__ == '__main__':
    main()
    




