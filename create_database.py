import sqlite3
import os

def create_db(games_dir):
    db_filename = 'foxsports.db'
    schema_filename = 'foxsports_schema.sql'

    if not os.path.exists(db_filename):
        with sqlite3.connect(db_filename) as conn:
            print('Creating schema')
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)

if __name__ == '__main__':
    games_dir = 'webpages/foxsports_gamepages/'

    create_db(games_dir)
