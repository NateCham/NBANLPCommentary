drop table if exists play_by_play;

create table play_by_play (
  id integer not null primary key autoincrement,
  game_id integer references game(id),
  quarter integer,
  minutes integer,
  seconds integer,
  home_score integer,
  away_score integer,
  team_id integer references team(id),
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
  rebound_type text,
  foul_type text,
  timeout_type text,
  turnover_type text,
  points_worth integer,
  p_player_id integer references player(foxsports_id),
  s_player_id integer references player(foxsports_id)
);

drop table if exists game;
create table game (
  id integer primary key autoincrement,
  season text,
  game_date date,
  home_team integer references team(id),
  away_team integer references team(id),
  game_type text,
  home_score integer,
  away_score integer,
  stadium integer references stadium(id),
  game_code integer
);

drop table if exists stadium;
create table stadium (
  id integer primary key autoincrement,
  name text,
  country text,
  state text,
  city text,
  fox_id integer,
  unique(name, city)
);


drop table if exists team;
create table team (
  id integer primary key,
  city text,
  alias text,
  name text,
  division text,
  unique(alias)
);

drop table if exists schedule;
create table schedule (
  id integer primary key autoincrement,
  game_date date,
  home_team_id integer not null references team(id),
  away_team_id integer not null references team(id),
  home_team_score integer,
  away_team_score integer,
  season text,
  game_id integer references game(id)
);

drop table if exists player;
create table player (
  id integer not null primary key autoincrement,
  first_name text,
  last_name text,
  weight integer,
  height integer,
  jersey_number integer,
  experience integer,
  school text,
  primary_position text,
  foxsports_id integer,
  team_id integer not null references team(id),
  unique(first_name, last_name, team_id)
);


drop table if exists division;
create table division (
  id integer not null primary key,
  name text not null,
  conference not null references conference(id)
);

drop table if exists conference;
create table conference (
  id integer not null primary key,
  name text not null
);
