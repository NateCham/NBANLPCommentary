# NBA NLP - Final Project - CSC 582
# Commentary Generator - Main
# Jacob Bustamante

import sys, re, sqlite3, random

DEBUG = False

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
conn = sqlite3.connect('foxsports.db')
conn.row_factory = dict_factory


shot_first_comments = [
    ("Here's the first shot attempt of the game from %s.", ['primary_player'])
]

make_comments = [
    ("It's good.", []),
    ("He made a %s.", ['shot_type'])
]

miss_comments = [
    ("He misses it.", []),
    ("%s misses it.", ['primary_player'])
]

block_comments = [
    ("The shot is blocked.", []),
    ("%s swats it away!", ['secondary_player'])
]

assist_comments = [
    ("Shot is made. Nice assist from %s.", ['secondary_player']),
    ("%s hooks up with %s for the basket.", ['secondary_player', 'primary_player'])
]

def event_comment_from_list(comments, play):
    i = random.randint(0, len(comments) - 1)
    return comments[i][0] % tuple(play[key] for key in comments[i][1])
    

def event_shot(play):
    output = []
    
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as count FROM play_by_play "
                 "where game_id = " + str(play['game_id']) +
                 " and play_type in ('shot', 'assist', 'blocks')"
                 " and id < " + str(play['pbp_id']))
    shot_count = cursor.fetchone()['count']
    
    #print(play['play_type'])
    
    # First shot of the game
    if shot_count == 0:
        output.append(event_comment_from_list(shot_first_comments, play))
    
    if play['play_type'] == 'assist':
        output.append(event_comment_from_list(assist_comments, play))
    elif play['play_type'] == 'blocks':
        output.append(event_comment_from_list(block_comments, play))
    elif play['shot_made'] == 'makes':
        output.append(event_comment_from_list(make_comments, play))
    elif play['shot_made'] == 'misses':
        output.append(event_comment_from_list(miss_comments, play))
        
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
    output.extend(display_starting_lineup(1))

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
        return game_info

def get_game_plays(game_id):
    plays = []
    headers = ['play_by_play.id as pbp_id', 'event_description', 'detail_description', 'game_id', 'quarter', 'minutes', 'seconds', 'home_score', 'away_score', 'description', 'play_type', 'primary_player', 'secondary_player', 'shot_made', 'shot_distance', 'x_coord', 'y_coord', 'timeout_type', 'foul_type', 'rebound_type', 'shot_type', 'turnover_type']
    
    #with sqlite3.connect('foxsports.db') as conn:
    cursor = conn.cursor()
    #cursor.execute("SELECT " + ','.join(headers) + " FROM play_by_play where game_id = " + str(game_id))
    cursor.execute("SELECT " + ','.join(headers) + ", name, team.id as t_id FROM play_by_play JOIN team ON team.id = play_by_play.team_id where game_id = " + str(game_id))
    data = cursor.fetchall()
    print(data[0])
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
    for play in game_plays:
        if play['play_type'] in ['shot', 'assist', 'blocks']:
            game_time = (play['quarter'], play['minutes'], play['seconds'])
            parse_comment(event_shot(play), game_time)

if __name__ == '__main__':
    main()
    




