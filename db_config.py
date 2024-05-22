# db_config.py
import os
from sqlalchemy import create_engine

def get_db_connection():
    user = os.getenv('DB_USER')  # Database username
    password = os.getenv('DB_PASSWORD')  # Database password
    host = os.getenv('DB_HOST')  # Database host
    port = os.getenv('DB_PORT')  # Database port
    database = os.getenv('DB_NAME')  # Database name

    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    return engine.connect()
