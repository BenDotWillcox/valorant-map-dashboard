import pandas as pd
from db_config import get_db_connection
from elo_calculations import process_maps




# Fetch the latest Elo ratings
def fetch_latest_elos():
    conn = get_db_connection()
    query = 'SELECT * FROM latest_elo_ratings'
    df = pd.read_sql(query, conn)
    conn.close()

    # Create a dictionary of dictionaries to store Elo ratings by map and team
    elo_ratings = {}
    for _, row in df.iterrows():
        team = row['team']
        map_name = row['map']
        rating = row['elo_rating']

        if map_name not in elo_ratings:
            elo_ratings[map_name] = {}
        elo_ratings[map_name][team] = rating

    return elo_ratings


# Fetch new matches to process
def fetch_new_matches():
    conn = get_db_connection()
    query = '''
    SELECT * FROM valorant_game_data
    WHERE match_id NOT IN (SELECT match_id FROM processed_matches)
    ORDER BY match_timestamp
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# Save updated Elo ratings
def save_latest_elos(elo_ratings):
    conn = get_db_connection()
    latest_elo_df = []
    for map_name, ratings in elo_ratings.items():
        for team, rating in ratings.items():
            latest_elo_df.append({'team': team, 'elo_rating': rating, 'map': map_name})
    latest_elo_df = pd.DataFrame(latest_elo_df)
    latest_elo_df.to_sql('latest_elo_ratings', conn, if_exists='replace', index=False)
    conn.close()


# Save Elo rating history
def save_elo_history(elo_history):
    conn = get_db_connection()
    elo_history.to_sql('elo_rating_history', conn, if_exists='append', index=False)
    conn.close()


# Save processed matches
def save_processed_matches(match_ids):
    conn = get_db_connection()
    processed_df = pd.DataFrame({'match_id': match_ids})
    processed_df.to_sql('processed_matches', conn, if_exists='append', index=False)
    conn.close()


# Update Elo ratings based on new matches
def update_elos():
    elo_ratings = fetch_latest_elos()
    new_matches = fetch_new_matches()
    if new_matches.empty:
        return

    maps = new_matches['map'].unique()
    all_elos, elo_history = process_maps(new_matches, maps)

    # Update the elo_ratings dictionary with new ratings
    for _, row in all_elos.iterrows():
        map_name = row['Map']
        team = row['Team']
        new_elo = row['New_Elo_Rating']

        if map_name not in elo_ratings:
            elo_ratings[map_name] = {}
        elo_ratings[map_name][team] = new_elo

    save_latest_elos(elo_ratings)
    save_elo_history(elo_history)
    save_processed_matches(new_matches['match_id'].tolist())


# Fetch latest Elo ratings for display
def fetch_display_elos():
    conn = get_db_connection()
    query = 'SELECT * FROM latest_elo_ratings'
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# Call the update function (useful for testing)
if __name__ == '__main__':
    update_elos()

