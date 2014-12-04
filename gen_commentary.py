# NBA NLP - Final Project - CSC 582
# Commentary Generator - Main
# Jacob Bustamante, Nate Chamness

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


"""
Game local variabls
"""
# Ejection / Foul out dictionary
# Key = player name (or possibly id?)
# Value = ejection|foul out|other?
ejections = {}


"""
Substitution commentary bid functions
"""
bid_substitution_counts = {'bid_substitution_default':0}
bid_substitution_meta_counts = {'bid_substitution_meta_default':0}

def bid_substitution_default(play):
    return (0.25, event_comment_from_list(comment_strings.substitution_default_comments, play), 'bid_substitution_default')

def bid_substitution_meta_default(play):
    return (0, "", 'bid_substitution_meta_default')

def event_substitution(play):
    output = []
    #print(play)
    max_bid = max([globals()[bid_function](play) for bid_function in bid_substitution_counts.keys()])
    bid_substitution_counts[max_bid[2]] += 1
    output.append(max_bid[1])
    
    max_bid_meta = max([globals()[bid_function](play) for bid_function in bid_substitution_meta_counts.keys()])
    if max_bid_meta[0] > 0:
        bid_substitution_meta_counts[max_bid_meta[2]] += 1
        output.append(max_bid_meta[1])
    
    return output


"""
Steal commentary bid functions
"""
bid_steal_counts = {'bid_steal_default':0}
bid_steal_meta_counts = {'bid_steal_meta_default':0}

def bid_steal_default(play):
    return (0.25, event_comment_from_list(comment_strings.steal_default_comments, play), 'bid_steal_default')

def bid_steal_meta_default(play):
    return (0, "", 'bid_steal_meta_default')

def event_steal(play):
    output = []
    
    max_bid = max([globals()[bid_function](play) for bid_function in bid_steal_counts.keys()])
    bid_steal_counts[max_bid[2]] += 1
    output.append(max_bid[1])
    
    max_bid_meta = max([globals()[bid_function](play) for bid_function in bid_steal_meta_counts.keys()])
    if max_bid_meta[0] > 0:
        bid_steal_meta_counts[max_bid_meta[2]] += 1
        output.append(max_bid_meta[1])
    
    return output


"""
Rebound commentary bid functions
"""
bid_rebound_counts = {'bid_rebound_default':0}
bid_rebound_meta_counts = {'bid_rebound_meta_default':0}

def bid_rebound_default(play):
    return (0.25, event_comment_from_list(comment_strings.rebound_default_comments, play), 'bid_rebound_default')

def bid_rebound_meta_default(play):
    return (0, "", 'bid_rebound_meta_default')

def event_rebound(play):
    output = []
    
    max_bid = max([globals()[bid_function](play) for bid_function in bid_rebound_counts.keys()])
    bid_rebound_counts[max_bid[2]] += 1
    output.append(max_bid[1])
    
    max_bid_meta = max([globals()[bid_function](play) for bid_function in bid_rebound_meta_counts.keys()])
    if max_bid_meta[0] > 0:
        bid_rebound_meta_counts[max_bid_meta[2]] += 1
        output.append(max_bid_meta[1])
    
    return output
    

"""
Foul commentary bid functions
"""
bid_foul_counts = {'bid_foul_default':0, 'bid_foul_trouble':0}
bid_foul_meta_counts = {'bid_foul_meta_default':0}

def bid_foul_trouble(play):
    if 'player_foul_count' not in play:
        return (0, "", 'bid_foul_trouble')
    
    if play['player_foul_count'] == 6:
        return (1, event_comment_from_list(comment_strings.foul_out_comments, play), 'bid_foul_trouble')
    elif play['quarter'] == 1 and play['player_foul_count'] == 2:
        return (1, event_comment_from_list(comment_strings.foul_q1_comments, play), 'bid_foul_trouble')
    elif play['quarter'] == 3 and play['player_foul_count'] == 4:
        return (1, event_comment_from_list(comment_strings.foul_q3_comments, play), 'bid_foul_trouble')
    elif play['quarter'] == 4 and play['player_foul_count'] == 5:
        return (1, event_comment_from_list(comment_strings.foul_q4_comments, play), 'bid_foul_trouble')
    else:
        return (0, "", 'bid_foul_trouble')

def bid_foul_default(play):
    if 'player_foul_count' not in play:
        return (0.25, event_comment_from_list(comment_strings.foul_default_non_comments, play), 'bid_foul_default')
    return (0.25, event_comment_from_list(comment_strings.foul_default_comments, play), 'bid_foul_default')

def bid_foul_out_contribution(play):
    pass

def bid_foul_meta_default(play):
    return (0, "", 'bid_foul_meta_default')

def event_foul(play):
    output = []
    
    if play['p_player_id']:
        cursor = conn.cursor();
        cursor.execute("select count(*) as foul_count "
                       "from play_by_play "
                       "where event_description = 'Foul' "
                       " and (detail_description like 'Personal%' or detail_description like 'Shooting%' or detail_description like 'Offensive%' or detail_description like 'Loose Ball') "
                       " and game_id = " + str(play['game_id']) + " "
                       " and id <= " + str(play['pbp_id']) + " "
                       " and p_player_id = " + str(play['p_player_id']) + " "
                       "group by p_player_id")
        
        foul_count = cursor.fetchone()
        if foul_count:
            play['player_foul_count'] = foul_count['foul_count']
    else:
        play['player_foul_count'] = 0
    
    max_bid = max([globals()[bid_function](play) for bid_function in bid_foul_counts.keys()])
    bid_foul_counts[max_bid[2]] += 1
    output.append(max_bid[1])
    
    max_bid_meta = max([globals()[bid_function](play) for bid_function in bid_foul_meta_counts.keys()])
    if max_bid_meta[0] > 0:
        bid_foul_meta_counts[max_bid_meta[2]] += 1
        output.append(max_bid_meta[1])
    
    return output
    

"""
Shot commentary bid functions
includes both shot and meta shot commentary
"""
bid_shot_counts = {'bid_shot_default':0, 'bid_shot_make':0, 'bid_shot_fastbreak':0}
bid_shot_meta_counts = {'bid_shot_meta_default':0, 'bid_shot_first':0, 'bid_shot_longest':0}
    

"""
Normal shot bids
""" 
def bid_shot_default(play):
    return (0.25, play['description'], 'bid_shot_default')

def bid_shot_make(play):
    if play['shot_made'] != 'makes':
        return (0, "", 'bid_shot_make')
    
    if play['shot_distance'] and play['shot_distance'] >= 70:
        return (1, event_comment_from_list(comment_strings.make_long_comments, play), 'bid_shot_make')
    elif play['shot_distance'] and play['shot_distance'] >= 40:
        return (1, event_comment_from_list(comment_strings.make_very_long_comments, play), 'bid_shot_make')
    return (0.3, event_comment_from_list(comment_strings.make_comments, play), 'bid_shot_make')


def bid_shot_fastbreak(play):
    if play['play_index'] - 1 <= 0 or play['shot_made'] != 'makes':
        return (0, "", 'bid_shot_fastbreak')
    
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
            return (0, "", 'bid_shot_fastbreak')
            
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
        return (0, "", 'bid_shot_fastbreak')


"""
Meta shot bids
"""
def bid_shot_meta_default(play):
    return (0, "", 'bid_shot_meta_default')

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
            if play['shot_made'] == 'makes':
                return (0.9, event_comment_from_list(comment_strings.shot_first_made_comments, play), 'bid_shot_first')
            else:
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


def event_shot(play):
    global game_plays
    
    output = []
    
    # bids are (bid_number, comment, bid_function_name)
    max_bid = max([globals()[bid_function](play) for bid_function in bid_shot_counts.keys()])
    bid_shot_counts[max_bid[2]] += 1
    output.append(max_bid[1])
    
    max_bid_meta = max([globals()[bid_function](play) for bid_function in bid_shot_meta_counts.keys()])
    if max_bid_meta[0] > 0:
        bid_shot_meta_counts[max_bid_meta[2]] += 1
        output.append(max_bid_meta[1])
    
    return output


"""
Start of game commentary bid functions
"""

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


"""
End of game commentary bid functions
"""
bid_end_first_counts = {'bid_game_end_first_default':0}

def bid_game_end_first_default(game_info):
    global game_plays
    
    return (.25, event_comment_from_list(comment_strings.game_end_first_default_comments, game_info), 'bid_game_end_first_default')
    

def event_game_end():
    global DEBUG, game_info, game_plays
    
    output = []
    max_bid_first = max([globals()[bid_function](game_info) for bid_function in bid_end_first_counts.keys()])
    bid_end_first_counts[max_bid_first[2]] += 1
    output.append(max_bid_first[1])
    
    return output


"""
Other functions
"""

def event_comment_from_list(comments, play):
    i = random.randint(0, len(comments) - 1)
    return comments[i][0] % tuple(play[key] for key in comments[i][1])
    

# all comments are pushed through here to have a central output interface
def parse_comment(output_comments, game_time):
    time_string = "Q" + str(game_time[0]) + " " + str(game_time[1]) + ':' + str(game_time[2])
    
    if output_comments:
        print(time_string)
        for comment in output_comments:
            print(comment)
        print()
    

def get_game_info(game_id):
    headers = ['season', 'game_date', 'home_team', 'away_team', 'game_type', 'home_score', 'away_score', 'game_code', 'stadium']
    
    
    cursor = conn.cursor();
    cursor.execute("SELECT season, game_date, t1.name as home_team, t2.name as away_team, game_type, home_score, away_score, game_code, stadium "
                   "FROM game JOIN team as t1 "
                   " ON home_team = t1.id JOIN team as t2 "
                   " ON away_team = t2.id "
                   "WHERE game.id = " + str(game_id))
    game_info = cursor.fetchone()
    
    if not game_info:
        return None
    
    cursor.execute("SELECT home_team_score, away_team_score "
                   "FROM schedule "
                   "WHERE game_id = " + str(game_id))
    game_info.update(cursor.fetchone())
    
    # get winner / loser
    if game_info['home_team_score'] > game_info['away_team_score']:
        game_info['winner_team_name'] = game_info['home_team']
        game_info['winner_score'] = game_info['home_team_score']
        game_info['loser_team_name'] = game_info['away_team']
        game_info['loser_score'] = game_info['away_team_score']
    else:
        game_info['winner_team_name'] = game_info['away_team']
        game_info['winner_score'] = game_info['away_team_score']
        game_info['loser_team_name'] = game_info['home_team']
        game_info['loser_score'] = game_info['home_team_score']
    
    game_info['game_id'] = game_id
    return game_info

def get_game_plays(game_id):
    plays = []
    headers = ['play_by_play.id as pbp_id', 'event_description', 'detail_description', 'game_id', 'quarter', 'minutes', 'seconds', 'home_score', 'away_score', 'description', 'play_type', 'primary_player', 'secondary_player', 'shot_made', 'shot_distance', 'x_coord', 'y_coord', 'timeout_type', 'foul_type', 'rebound_type', 'shot_type', 'turnover_type', 'points_worth', 'p_player_id', 's_player_id']
    
    cursor = conn.cursor()
    cursor.execute("SELECT " + ','.join(headers) + ", name, team.id as t_id FROM play_by_play JOIN team ON team.id = play_by_play.team_id where game_id = " + str(game_id))
    data = cursor.fetchall()
    
    return data



def main():
    global DEBUG, game_info, game_plays
    
    if len(sys.argv) > 2 and sys.argv[2] == 'debug':
        DEBUG = True
    if len(sys.argv) > 1:
        game_id = sys.argv[1]
    else:
        game_id = 0
    
    game_info = get_game_info(game_id)
    game_plays = get_game_plays(game_id)
    
    if not game_info:
        print('game_id',game_id,'not found')
        return
    if DEBUG:
        print('game_id:', game_id)
        print(game_info)


    """
    Start game commentary loop
    """
    # Game start commentary
    parse_comment(event_game_start(), (1,12,0))
    
    # Main game loop
    for play_index, play in enumerate(game_plays):
        play['play_index'] = play_index
        game_time = (play['quarter'], play['minutes'], play['seconds'])
        
        if play['play_type'] in ['shot', 'assist', 'blocks']:
            parse_comment(event_shot(play), game_time)
        elif play['event_description'] == "Foul":
            parse_comment(event_foul(play), game_time)
        elif play['play_type'] == "rebound":
            parse_comment(event_rebound(play), game_time)
        elif play['play_type'] == "steal":
            parse_comment(event_steal(play), game_time)
        elif play['play_type'] == "substitution":
            parse_comment(event_substitution(play), game_time)
        elif DEBUG:
            print("UNPARSED PLAY_TYPE:", play['play_type'])
    
    # End game commentary
    parse_comment(event_game_end(), (4,0,0))


if __name__ == '__main__':
    main()
    




