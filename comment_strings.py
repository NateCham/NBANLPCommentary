
"""
Start of game commentary
"""
game_start_lineup_comments = [
    ("The starting lineup for the %s %s is %s.", ('city', 'name', 'starters')),
    ("%s are starting tonight for the %s %s.", ('starters', 'city', 'name'))
]


"""
Shot commentary
"""

shot_first_comments = [
    ("That was %s with the first shot attempt of the game.", ['primary_player'])
]

shot_first_made_comments = [
    ("That %s marks the first basket of the game.", ['shot_type']),
    ("And there's the first basket of the game.", [])
]

make_comments = [
    ("%s's %s shot is good.", ['primary_player', 'shot_type']),
    ("%s makes the basket.", ['primary_player'])
]

make_long_comments = [
    ("The long shot by %s is good!", ['primary_player']),
    ("%s with the %s-footer!", ['primary_player', 'shot_distance'])
]

make_very_long_comments = [
    ("Are you kidding me?? %s's %s-footer hits for the very long 3-pointer.", ['primary_player', 'shot_distance']),
    ("%s makes the %s-foot shot! wow!", ['primary_player', 'shot_distance'])
]

miss_comments = [
    ("%s misses the bottom of the net.", ['primary_player']),
    ("%s misses a shot.", ['primary_player'])
]

block_comments = [
    ("The shot is blocked.", []),
    ("%s swats it away!", ['secondary_player'])
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

"""
Steal commentary
"""
steal_default_comments = [
    ("%s with the steal.", ['primary_player']),
    ("%s steals the ball from %s.", ['primary_player', 'secondary_player']),
    ("%s with the pick.", ['primary_player'])
]

"""
Foul commentary
"""
foul_default_comments = [
    ("%s with the foul.", ['primary_player'])
]

foul_default_non_comments = [
    ("%s with the foul.", ['primary_player'])
]

foul_q1_comments = [
    ("He's got two fouls in the first quarter, probably should bench him soon.", [])
]

foul_q3_comments = [
    ("%s fourth foul puts him in foul trouble with over still over a quarter remaining.", ['primary_player'])
]

foul_q4_comments = [
    ("%s has to watch out, one more slip up and he fouls out.", ['primary_player'])
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
End of game commentary
"""

game_end_first_default_comments = [
    ("The %s end the game with a %s to %s victory over the %s.", ['winner_team_name', 'winner_score', 'loser_score', 'loser_team_name'])
]
