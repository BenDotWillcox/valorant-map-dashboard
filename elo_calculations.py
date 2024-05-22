import numpy as np
import pandas as pd

# Elo update function using your initial method
def elo_update(win_elo, lose_elo, win_score, lose_score, k=1000, win=True):
    score_diff = win_score - lose_score
    if win:
        return win_elo + k * 0.15 * np.log(5.95 * np.sqrt(score_diff + 1)) * (1 - (1 / (1 + 10 ** ((lose_elo - win_elo) / 1000))))
    else:
        return lose_elo + k * 0.15 * np.log(5.95 * np.sqrt(score_diff + 1)) * (0 - (1 / (1 + 10 ** ((win_elo - lose_elo) / 1000))))

# Update Elo ratings based on match results in the provided DataFrame
def update_elo_ratings(df, elo_ratings, elo_update):
    new_elos = []

    for index, row in df.iterrows():
        winning_team = row['winning_team']
        losing_team = row['losing_team']
        timestamp = row['match_timestamp']

        # Old Elo ratings
        old_win_elo = elo_ratings[winning_team]
        old_lose_elo = elo_ratings[losing_team]

        # Update Elo ratings
        new_win_elo = elo_update(old_win_elo, old_lose_elo, row['winning_team_score'], row['losing_team_score'], win=True)
        new_lose_elo = elo_update(old_win_elo, old_lose_elo, row['winning_team_score'], row['losing_team_score'], win=False)

        # Save the updated ratings
        elo_ratings[winning_team] = new_win_elo
        elo_ratings[losing_team] = new_lose_elo

        # Add to the new DataFrame
        new_elos.append({'Team': winning_team, 'Timestamp': timestamp, 'Old_Elo_Rating': old_win_elo, 'New_Elo_Rating': new_win_elo,
                         'Opponent': losing_team, 'Score': f"{row['winning_team_score']}-{row['losing_team_score']}"})
        new_elos.append({'Team': losing_team, 'Timestamp': timestamp, 'Old_Elo_Rating': old_lose_elo, 'New_Elo_Rating': new_lose_elo,
                         'Opponent': winning_team, 'Score': f"{row['losing_team_score']}-{row['winning_team_score']}"})

    return pd.DataFrame(new_elos)

# Process all maps
def process_maps(df, maps):
    all_elos = []
    elo_history = []

    for map_name in maps:
        map_df = df[df['map'] == map_name].sort_values('match_timestamp')
        elo_ratings = {team: 1000 for team in set(df['winning_team']).union(set(df['losing_team']))}
        map_elos = update_elo_ratings(map_df, elo_ratings, elo_update)
        map_elos['Map'] = map_name
        all_elos.append(map_elos)

        # Add Elo history for the map
        for _, row in map_elos.iterrows():
            elo_history.append({
                'team': row['Team'],
                'map': map_name,
                'elo_rating': row['New_Elo_Rating'],
                'timestamp': row['Timestamp'],
                'opponent': row['Opponent'],
                'score': row['Score']
            })

    return pd.concat(all_elos, ignore_index=True), pd.DataFrame(elo_history)



