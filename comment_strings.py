
"""
Start of game commentary
"""
game_start_lineup_comments = [
    ("The starting lineup for the %s %s is %s.", ('city', 'name', 'starters')),
    ("%s are starting tonight for the %s %s.", ('starters', 'city', 'name')),
    ("The %s %s are starting %s.", ('city', 'name', 'starters'))
]


assist_pair_avg_comments = [
    ("These two have been playing great together for %s games this season. They've linked up for an assist an average %0.1f times per game.", ['num_games', 'assist_avg']),
    ("These guys consistently make a good pair. %s games this season they've averaged %0.1f assists with each other per game.", ['num_games', 'assist_avg'])
]

"""
Shot commentary
"""

shot_first_comments = [
    ("That was %s with the first shot attempt of the game.", ['primary_player']),
    ("And there's the first shot attempt of the game.", []),
    ("That was the first shot of the game.", [])
]

shot_first_made_comments = [
    ("That %s shot marks the first basket of the game.", ['shot_type']),
    ("And there's the first basket of the game.", []),
    ("So the %s get the first points on the board.", ['name']),
    ("And the %s start the game up %s.", ['name', 'points_worth_str'])
]

make_comments = [
    ("%s's %s shot is good.", ['primary_player', 'shot_type']),
    ("%s makes the basket.", ['primary_player']),
    ("%s puts %s points on the board for the %s with a %s shot.", ['primary_player', 'points_worth_str', 'name', 'shot_type']),
    ("%s makes the %s shot for %s.", ['primary_player', 'shot_type', 'points_worth_str']),
    ("The %s-foot %s shot from %s is good.", ['shot_distance', 'shot_type', 'primary_player']),
    ("%s puts it in for %s.", ['primary_player', 'points_worth_str']),
    ("%s with the %s-foot %s pointer.", ['primary_player', 'shot_distance', 'points_worth_str']),
    ("%s gives the %s %s with that made %s shot.", ['primary_player', 'name', 'points_worth_str', 'shot_type'])
]

make_assist_comments = [
    ("After the assist from %s, %s's %s is good.", ['secondary_player', 'primary_player', 'shot_type']),
    ("%s makes the basket. %s with the assist.", ['primary_player', 'secondary_player']),
    ("%s passes it off to %s, who finishes it with a %s.", ['secondary_player', 'primary_player', 'shot_type']),
    ("%s puts %s points on the board for the %s with a %s. %s with the assist.", ['primary_player', 'points_worth_str', 'name', 'shot_type', 'secondary_player']),
    ("%s passes the ball to %s, who puts %s points on the board for the %s with a %s.", ['secondary_player', 'primary_player', 'points_worth_str', 'name', 'shot_type']),
    ("After the pass from %s, the %s-foot %s from %s is good.", ['secondary_player', 'shot_distance', 'shot_type', 'primary_player']),
    ("%s puts it up for %s. %s with the assist.", ['primary_player', 'points_worth_str', 'secondary_player'])
]

make_long_comments = [
    ("The long shot by %s is good!", ['primary_player']),
    ("%s with the %s-footer!", ['primary_player', 'shot_distance']),
    ("%s hits a long %s-footer.", ['primary_player', 'shot_distance']),
    ("The long %s-foot shot by %s is in!", ['shot_distance', 'primary_player']),
    ("%s hits the 3 from way outside!", ['primary_player']),
]

make_very_long_comments = [
    ("Are you kidding me?? %s's %s-footer hits for the very long 3-pointer.", ['primary_player', 'shot_distance']),
    ("%s makes the %s-foot shot! What!", ['primary_player', 'shot_distance']),
    ("%s drains the %s-footer!!! That was a very long distance shot.", ['primary_player', 'shot_distance'])
]

miss_comments = [
    ("%s misses the shot attempt.", ['primary_player']),
    ("%s misses a shot.", ['primary_player']),
    ("%s with the missed shot.", ['primary_player']),
    ("A missed attempt from %s.", ['primary_player']),
    ("A missed shot from %s.", ['primary_player'])
]

miss_nameless_comments = [
    ("The %s misses the shot attempt.", ['name']),
    ("The %s miss a shot.", ['name']),
    ("The %s with the missed shot.", ['name']),
    ("A missed attempt from the %s.", ['name']),
    ("A missed shot from the %s.", ['name'])
]

block_comments = [
    ("The shot is blocked.", []),
    ("%s swats it away!", ['secondary_player']),
    ("%s's shot is blocked by %s.", ['primary_player', 'secondary_player'])
]

assist_comments = [
    ("Shot is made. Nice assist from %s.", ['secondary_player']),
    ("%s hooks up with %s for the basket.", ['secondary_player', 'primary_player'])
]

fastbreak_12_comments = [
    ("%s with the quick fastbreak.", ['primary_player']),
    ("After the %s by %s, %s scores a fastbreak basket.", ['fastbreak_play', 'fastbreak_creator', 'primary_player'])
]
fastbreak_11_comments = [
    ("%s with the quick fastbreak.", ['primary_player']),
    ("Great play! %s with the %s and then finishes off the play with a %s.", ['primary_player', 'fastbreak_play', 'shot_type'])
]
fastbreak_123_comments = [
    ("%s with the quick fastbreak.", ['primary_player']),
    ("After the %s by %s, %s passes to %s who makes a %s for %s points.", ['fastbreak_play', 'fastbreak_creator', 'secondary_player', 'primary_player', 'shot_type', 'points_worth'])
]
fastbreak_121_comments = [
    ("%s with the quick fastbreak.", ['primary_player']),
    ("After the %s by %s, %s scores a fastbreak basket.", ['fastbreak_play', 'fastbreak_creator', 'primary_player'])
]
fastbreak_112_comments = [
    ("%s with the quick fastbreak.", ['primary_player']),
    ("After the %s by %s, %s scores a fastbreak basket.", ['fastbreak_play', 'fastbreak_creator', 'primary_player'])
]

shot_longest_comments = [
    ("Amazing! That %s-foot shot by %s was the longest shot made all season!", ['shot_distance', 'primary_player'])
]

shot_longest_player_comments = [
    ("Wow! At %s feet, that's %s's longest shot of this season.", ['shot_distance', 'primary_player'])
]


"""
Substitution commentary
"""
substitution_default_comments = [
    ("%s goes in for %s.", ['primary_player', 'secondary_player']),
    ("%s is coming out for %s.", ['secondary_player', 'primary_player']),
    ("%s for the %s is coming out for %s.", ['secondary_player', 'name', 'primary_player']),
    ("The %s sub in %s for %s.", ['name', 'primary_player', 'secondary_player'])
]

substitution_off_bench_comments = [
    ("%s comes off the bench for for %s.", ['primary_player', 'secondary_player']),
]

substitution_on_bench_comments = [
    ("%s returns to the bench. The starter, %s, comes back on the floor.", ['secondary_player', 'primary_player']),
]

substitution_bench_points_comments = [
    ("The %s bench has been doing great tonight, scoring %s of the team's %s points", ['name', 'bench_points', 'team_points']),
    ("The bench for the %s have been making a big impact this game. They've put in a total of %s points out of the team's %s.", ['name', 'bench_points', 'team_points']),
    ("Scoring %s of the team's %s, the %s bench are having a great showing tonight.", ['bench_points', 'team_points', 'name'])
]

"""
Steal commentary
"""
steal_default_comments = [
    ("%s with the steal.", ['primary_player']),
    ("%s steals the ball from %s.", ['primary_player', 'secondary_player']),
    ("%s with the pick.", ['primary_player'])
]


"""
Frethrow commentary
"""

free_throw_start_default_comments = [
    ("%s is %s of %s from the line tonight. He's shooting free throws now.", ['primary_player', 'free_throws_made', 'tot_free_throws']),
    ("%s is %s for %s in free throws tonight. He's shooting at the line now.", ['primary_player', 'free_throws_made', 'tot_free_throws'])
]

free_throw_default_comments = [
    ("%s", ['description'])
]

"""
Foul commentary
"""
foul_default_comments = [
    ("%s with the foul.", ['primary_player']),
    ("Foul called on %s.", ['primary_player']),
    ("There's a foul called on %s.", ['primary_player'])
]

foul_default_non_comments = [
    ("%s with the foul.", ['primary_player']),
    ("Foul called on %s.", ['primary_player']),
    ("There's a foul called on %s.", ['primary_player'])
]

foul_q1_comments = [
    ("He's got two fouls in the first quarter, probably should bench him soon.", []),
    ("Those two fouls in the first quarter could put him in early foul trouble.", []),
    ("He's got to watch his fouls now, with two fouls already in the first quarter.", [])
]

foul_q3_comments = [
    ("%s's fourth foul puts him in foul trouble with still over a quarter remaining.", ['primary_player'])
]

foul_q4_comments = [
    ("%s's has to watch out, one more slip up and he fouls out.", ['primary_player'])
]

foul_out_comments = [
    ("And he's gone. That's %s's last foul to give.", ['primary_player'])
]

"""
Rebound commentary
"""
rebound_default_comments = [
    ("%s with the rebound.", ['primary_player']),
    ("%s with the %s rebound.", ['primary_player', 'rebound_type']),
    ("%s rebounds the ball.", ['primary_player'])
]

"""
Jumpball commentary
"""
jumpball_default_comments = [
    ("A jumpball is called.", []),
    ("A jumpball is called in the %s's favor.", ['name'])
]

jumpball_first_comments = [
    ("And here's the tipoff to start the game. %s on the %s gains possesion.", ['primary_player', 'name'])
]

"""
Timeout commentary
"""
timeout_default_comments = [
    ("A timeout is called by the %s.", ['name']),
    ("The %s call a timeout.", ['name'])
]

timeout_team_losing_streak_comments = [
    ("It's been a sad last few games for the %s. They've lost %s of their last %s games.", ['team_name', 'num_lost', 'num_past_games'])
]

timeout_team_winning_streak_comments = [
    ("The %s have been on a great streak lately, winning %s of %s!", ['team_name', 'num_won', 'num_past_games']),
    ("The %s have been playing great these last few games. They've won %s of their last %s games.", ['team_name', 'num_won', 'num_past_games'])
]


"""
Start of game commentary
"""
game_start_first_default_comments = [
    ("The %s will be playing the %s here in %s.", ['away_team', 'home_team', 'home_city']),
    ("The matchup tonight is the %s %s playing at home against the %s %s.", ['home_city', 'home_team', 'away_city', 'away_team']),
    ("Tonights matchup we have the home team, the %s %s, playing the %s %s.", ['home_city', 'home_team', 'away_city', 'away_team']),
]

game_start_lineup_home_comments = [
    ("The starting lineup for the %s %s is %s.", ('home_city', 'home_team', 'home_starters')),
    ("%s are starting tonight for the %s %s.", ('home_starters', 'home_city', 'home_team')),
    ("The %s %s are starting %s.", ('home_city', 'home_team', 'home_starters')),
    ("The %s %s starting lineup for tonights game is %s.", ('home_city', 'home_team', 'home_starters')),
    ("The starters for the %s %s are %s.", ('home_city', 'home_team', 'home_starters'))
]

game_start_lineup_away_comments = [
    ("The starting lineup for the %s %s is %s.", ('away_city', 'away_team', 'away_starters')),
    ("%s are starting tonight for the %s %s.", ('away_starters', 'away_city', 'away_team')),
    ("The %s %s are starting %s.", ('away_city', 'away_team', 'away_starters')),
    ("The %s %s starting lineup for tonights game is %s.", ('away_city', 'away_team', 'away_starters')),
    ("The starters for the %s %s are %s.", ('away_city', 'away_team', 'away_starters'))
]
    
game_start_record_comments = [
    ("The %s are currently with a %s-%s record, while the %s stand with a %s-%s record", ('home_team', 'home_wins', 'home_losses', 'away_team', 'away_wins', 'away_losses')),
]


"""
End of game commentary
"""

game_end_first_default_comments = [
    ("Game over. The %s end the game with a %s to %s victory over the %s. That ends the night here in %s.", ['winner_team_name', 'winner_score', 'loser_score', 'loser_team_name', 'home_city'])
]
