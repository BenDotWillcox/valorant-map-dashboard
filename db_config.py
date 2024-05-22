# db_config.py
import os
from sqlalchemy import create_engine

def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    engine = create_engine(database_url)
    return engine.connect()

