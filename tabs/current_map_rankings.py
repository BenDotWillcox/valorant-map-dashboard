import streamlit as st
import pandas as pd
from db_config import get_db_connection
from config import team_full_names, map_images



@st.cache_data(ttl=6000)  # Cache the results for 10 minutes
def fetch_display_elos():
    conn = get_db_connection()
    query = 'SELECT * FROM latest_elo_ratings'
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def show():
    st.markdown("<h1 class='title'>Valorant League Current Map Rankings</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>Ranking of teams by their latest Elo rating on each map.</h2>",
                unsafe_allow_html=True)

    # Fetch the latest Elo ratings from the database
    elo_df = fetch_display_elos()
    maps = elo_df['map'].unique()  # Get the unique map names

    # Create two rows for displaying the tables
    row1 = st.columns(4)
    row2 = st.columns(3)

    for idx, map_name in enumerate(maps):
        # Filter and sort the Elo ratings for the current map
        map_df = elo_df[elo_df['map'] == map_name].sort_values(by='elo_rating', ascending=False)
        map_df['elo_rating'] = map_df['elo_rating'].round().astype(int)  # Round Elo ratings to whole numbers
        map_df = map_df.reset_index(drop=True)
        map_df.index = map_df.index + 1
        map_df = map_df.rename(columns={'elo_rating': 'Elo Rating', 'team': 'Team'})
        map_df.index.name = 'Rank'

        # Replace team abbreviations with full names
        map_df['Team'] = map_df['Team'].apply(lambda abbr: team_full_names.get(abbr, abbr))

        # Display the image and table in the appropriate row and column
        if idx < 4:
            with row1[idx]:
                st.image(map_images[map_name], use_column_width=True)  # Display map image as title
                st.dataframe(map_df[['Team', 'Elo Rating']], use_container_width=True)
        elif idx - 4 < len(row2):  # Ensure idx - 4 is within the range of row2
            with row2[idx - 4]:
                st.image(map_images[map_name], use_column_width=True)  # Display map image as title
                st.dataframe(map_df[['Team', 'Elo Rating']], use_container_width=True)

