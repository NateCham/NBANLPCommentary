drop table if exists play_by_play;

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

/*
create table player (
  id integer not null primary key,
  first_name not null text,
  last_name not null text,
  team integer not null references team(id)
);

create table team (
  id integer not null primary key autoincrement,
  city text not null,
  name text not null,
  division not null integer
);

create table player (
  id integer,
  first_name text,
  last_name not null text,
  team integer not null references team(id)
);


create table division (
  id integer not null primary key,
  name text not null,
  conference not null references conference(id)
);

create table conference (
  id integer not null primary key,
  name text not null
);
*/
