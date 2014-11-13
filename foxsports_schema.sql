create table play_by_play (
  id integer not null primary key autoincrement,
  game integer references game(id),
  quarter integer,
  minutes integer,
  seconds integer,
  home_score integer,
  away_score integer,
  team integer,
  textual_description text,
  play_type text check( play_type in ('R', 'B', 'S', 'A', 'O') ) not null default 'O',
  primary_player text,
  x_coord real,
  y_coord real
);

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
