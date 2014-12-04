
-- player stats
select game_id, sum(case when event_description = 'Field Goal Made' then 1 else 0 end) as made, sum(case when event_description = 'Field Goal Missed' then 1 else 0 end) as missed, sum(case when event_description in ('Field Goal Made', 'Free Throw Made') then points_worth else 0 end) as points, primary_player from play_by_play where game_id = 1 and p_player_id = '399612';


-- Basic points stats per game for player
select 
  game.id, 
  play_by_play.quarter, 
  play_by_play.minutes,
  play_by_play.seconds,
  game.home_team, 
  game.away_team, 
  play_by_play.primary_player, 
  sum(case when shot_type not like '%3-point%'    and shot_made = 'makes'  then 1 else 0 end) as twos_made, 
  sum(case when shot_type not like '%3-point%'    and shot_made = 'misses' then 1 else 0 end) as twos_missed, 
  sum(case when shot_type like     '%3-point%'    and shot_made = 'makes'  then 1 else 0 end) as threes_made,
  sum(case when shot_type like     '%3-point%'    and shot_made = 'misses' then 1 else 0 end) as threes_missed,
  sum(case when shot_type like     '%free throw%' and shot_made = 'makes'  then 1 else 0 end) as made_free_throws, 
  sum(case when shot_type like     '%free throw%' and shot_made = 'misses' then 1 else 0 end) as missed_free_throws
from play_by_play join game on game.id = play_by_play.game_id 
where primary_player = 'Stephen Curry' group by game.id;


-- steal then fastbreak
select
  game.game_date,
  pbp1.game_id,
  pbp1.quarter,
  pbp1.minutes,
  pbp1.seconds,
  pbp2.minutes,
  pbp2.seconds,
  (pbp1.minutes * 60 + pbp1.seconds) - (pbp2.minutes * 60 + pbp2.seconds) as diff,
  pbp1.description,
  pbp2.description
from play_by_play as pbp1, play_by_play as pbp2
join game on game.id = pbp1.game_id
where pbp1.game_id = pbp2.game_id
  and pbp1.quarter = pbp2.quarter
  and (pbp1.minutes * 60 + pbp1.seconds) - (pbp2.minutes * 60 + pbp2.seconds) <= 6 
  and (pbp1.minutes * 60 + pbp1.seconds) > (pbp2.minutes * 60 + pbp2.seconds)
  and pbp1.play_type = 'steal'
  and (pbp2.play_type = 'shot' or pbp2.play_type = 'assist') -- use play_type = rebound as well
  and pbp2.shot_made = 'makes'
group by pbp2.description
order by game.game_date, pbp2.quarter, pbp2.minutes;


-- number of different kinds of baskets made/missed before date
select
    sum(case when shot_type not like '%3-point%'    and shot_made = 'makes'  then 1 else 0 end) as twos_made, 
    sum(case when shot_type like     '%3-point%'    and shot_made = 'makes'  then 1 else 0 end) as threes_made,
    sum(case when shot_type like     '%free throw%' and shot_made = 'makes'  then 1 else 0 end) as made_free_throws,
    sum(case when shot_type not like '%3-point%'    and shot_made = 'misses'  then 1 else 0 end) as twos_missed, 
    sum(case when shot_type like     '%3-point%'    and shot_made = 'misses'  then 1 else 0 end) as threes_missed,
    sum(case when shot_type like     '%free throw%' and shot_made = 'misses'  then 1 else 0 end) as missed_free_throws
from play_by_play join game on game.id = play_by_play.game_id
where game.game_date <= '2014-04-11' and primary_player = 'Stephen Curry';



-- points before date
select
  twos_made,
  threes_made,
  made_free_throws,
  (twos_made * 2 + threes_made * 3 + made_free_throws) as points
from (
  select
      sum(case when shot_type not like '%3-point%'    and shot_made = 'makes'  then 1 else 0 end) as twos_made, 
      sum(case when shot_type like     '%3-point%'    and shot_made = 'makes'  then 1 else 0 end) as threes_made,
      sum(case when shot_type like     '%free throw%' and shot_made = 'makes'  then 1 else 0 end) as made_free_throws
  from play_by_play join game on game.id = play_by_play.game_id
  where game.game_date <= '2014-04-11' and primary_player = 'Stephen Curry'
);

-- longest shot made
select
  quarter,
  minutes,
  seconds,
  max(shot_distance),
  description
from play_by_play
where shot_made = 'makes';

-- shots made over 50
select
  quarter,
  minutes,
  seconds,
  shot_distance,
  description
from play_by_play
where shot_made = 'makes' and shot_distance > 50;

-- players with most long shot attempts *need to include ties*
select
  count(primary_player) as long_shots,
  primary_player
from play_by_play
where shot_distance > 50
group by primary_player
order by count(primary_player) desc
limit 5;


-- number of field goals last 3 games (need more info)
select
  primary_player,
from play_by_play join game on game.id = play_by_play.game_id


-- 5 games before date including specific team
select * from schedule join game on schedule.game_id = game.id where (away_team_id = '4' or home_team_id = 'team_id') and game_date < 'date' order by game_date desc limit 5;

-- point totals for last 10 games for player
select first_name, last_name, sum(points_worth), game.game_date from player, play_by_play, game where play_by_play.game_id = game.id and play_by_play.p_player_id = player.foxsports_id and (event_description = 'Field Goal Made' or event_description = 'Free Throw Made') and player.last_name = 'Curry' and player.first_name = 'Stephen' group by game.id limit 10;

-- point average over last 10 games
select first_name, last_name, avg(points) from (select first_name, last_name, sum(case when (event_description = 'Field Goal Made' or event_description = 'Free Throw Made') then points_worth else 0 end) as points, game.game_date from player, play_by_play, game where play_by_play.game_id = game.id and play_by_play.p_player_id = player.foxsports_id and player.last_name = 'Curry' and player.first_name = 'Stephen' group by game.id limit 10);


-- max points per game
select max(game_points) from (select sum(case when event_description in ('Field Goal Made', 'Free Throw Made') then points_worth else 0 end) as game_points from play_by_play join player on p_player_id = foxsports_id where first_name = 'Stephen' and last_name = 'Curry' group by game_id);



-- number of double categories (points, assists, rebounds)
select 
  game_id, 
  points, 
  assists, 
  rebounds, 
  steals,
  (case when points >= 10 then 1 else 0 end) + (case when rebounds >= 10 then 1 else 0 end) + (case when assists >= 10 then 1 else 0 end) as double_cats

from (
  select 
    game_id, 
    sum(case when event_description in ('Field Goal Made', 'Free Throw Made') and primary_player = 'Stephen Curry' then points_worth else 0 end) as points, 
    sum(case when play_type = 'assist' and secondary_player = 'Stephen Curry' then 1 else 0 end) assists, 
    sum(case when play_type = 'rebound' and primary_player = 'Stephen Curry' then 1 else 0 end) rebounds,
    sum(case when play_type = 'steal' and primary_player = 'Stephen Curry' then 1 else 0 end) steals
  from play_by_play
  where (primary_player = 'Stephen Curry' or secondary_player = 'Stephen Curry') 
  group by game_id
);




select 
  game_id, 
  points, 
  assists, 
  rebounds,
  blocks,
  steals,
  (case when points >= 10 then 1 else 0 end) + (case when rebounds >= 10 then 1 else 0 end) + (case when assists >= 10 then 1 else 0 end) + (case when blocks >= 10 then 1 else 0 end) + (case when steals >= 10 then 1 else 0 end) as double_cats
from (
  select 
    game_id, 
    sum(case when event_description in ('Field Goal Made', 'Free Throw Made') and p_player_id = player.foxsports_id then points_worth else 0 end) as points, 
    sum(case when play_type = 'assist' and secondary_player = (player.first_name || ' ' || player.last_name) then 1 else 0 end) assists, 
    sum(case when play_type = 'rebound' and primary_player = (player.first_name || ' ' || player.last_name) then 1 else 0 end) rebounds,
    sum(case when play_type = 'steal' and primary_player = (player.first_name || ' ' || player.last_name) then 1 else 0 end) steals,
    sum(case when play_type = 'blocks' and primary_player = (player.first_name || ' ' || player.last_name) then 1 else 0 end) blocks
  from play_by_play, player
  where (player.first_name || ' ' || player.last_name) in (primary_player, secondary_player) and foxsports_id = '338365' 
  group by game_id
);
