# db_config.py
import os
from sqlalchemy import create_engine

def get_db_connection():
    user = 'DB_USER'
    password = 'DB_PASSWORD'
    host = 'DB_HOST'
    port = 'DB_PORT'
    database = 'DB_NAME'

    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    return engine.connect()

