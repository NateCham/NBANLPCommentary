CREATE TABLE IF NOT EXISTS Play_by_play(
  player_id_1 INTEGER,
  player_id_2 INTEGER,
  x_shot_coord FLOAT,
  y_shot_coord FLOAT,
  time_quarter INTEGER,
  time_minute INTEGER,
  time_seconds DECIMAL,
  event_description VARCHAR(50),
  textual_description VARCHAR(255),
  points_earned INTEGER,
  home_team_score INTEGER,
  away_team_score INTEGER,
  shot_type VARCHAR(30),
  shot_distance INTEGER,
  shot_made BOOLEAN,
  shot_blocked BOOLEAN
);

CREATE TABLE IF NOT EXISTS Player(
  player_id INTEGER AUTO_INCREMENT,
  last_name VARCHAR(40),
  first_name VARCHAR(40),
  current_team INTEGER,
  age INTEGER,
  height_inches INTEGER,
  weight_pounds INTEGER,
  college VARCHAR(50),
  position VARCHAR(50),
  place_depth_chart INTEGER,
  jersey_number INTEGER,
  injured BOOLEAN,
  return_from_injury VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS Team(
  team_id INTEGER AUTO_INCREMENT,
  name VARCHAR(30),
  city VARCHAR(30),
  arena VARCHAR(50),
  schedule_id INTEGER
);

CREATE TABLE IF NOT EXISTS Schedule(
  home_team_id INTEGER,
  away_team_id INTEGER,
  home_team_score INTEGER,
  away_team_score INTEGER,
  start_time DATETIME
);

