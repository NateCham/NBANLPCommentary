drop table if exists play_by_play;

create table play_by_play (
  id integer not null primary key autoincrement,
  game integer references game(id),
  quarter integer,
  minutes integer,
  seconds integer,
  home_score integer,
  away_score integer,
  team text,
  description text,
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

/*
create table player (
  id integer not null primary key,
  first_name not null text,
  last_name not null text,
  team integer not null references team(id)
);

create table team (
  id integer not null primary key,
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

create table game (
  id integer primary key,
  played_on date not null,
  home_team integer not null references team(id),
  away_team integer not null references team(id),
  home_score integer not null,
  away_score integer not null
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
