import streamlit as st
from sqlalchemy import create_engine

def get_db_connection():
    user = st.secrets["DB"]["DB_USER"]
    password = st.secrets["DB"]["DB_PASSWORD"]
    host = st.secrets["DB"]["DB_HOST"]
    port = st.secrets["DB"]["DB_PORT"]
    database = st.secrets["DB"]["DB_NAME"]

    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    return engine.connect()


