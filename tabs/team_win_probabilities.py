import streamlit as st
import pandas as pd
from db_config import get_db_connection
from config import team_full_names, team_colors, team_logos, map_images

@st.cache_data(ttl=6000)
def fetch_display_elos():
    conn = get_db_connection()
    query = 'SELECT * FROM latest_elo_ratings'
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def calculate_win_probability(elo1, elo2):
    prob1 = 1 / (1 + 10 ** ((elo2 - elo1) / 1000))
    prob2 = 1 / (1 + 10 ** ((elo1 - elo2) / 1000))
    return prob1, prob2

def calculate_bo3_match_win_probability(map_probs):
    prob_team1 = (
            (map_probs[0][0] * map_probs[1][0]) +
            (map_probs[0][0] * map_probs[1][1] * map_probs[2][0]) +
            (map_probs[0][1] * map_probs[1][0] * map_probs[2][0])
    )
    return prob_team1, 1 - prob_team1

def calculate_bo5_match_win_probability(map_probs):
    prob_team1 = (
            (map_probs[0][0] * map_probs[1][0] * map_probs[2][0]) +
            (map_probs[0][0] * map_probs[1][0] * map_probs[2][1] * map_probs[3][0]) +
            (map_probs[0][0] * map_probs[1][0] * map_probs[2][1] * map_probs[3][1] * map_probs[4][0]) +
            (map_probs[0][0] * map_probs[1][1] * map_probs[2][0] * map_probs[3][0]) +
            (map_probs[0][0] * map_probs[1][1] * map_probs[2][0] * map_probs[3][1] * map_probs[4][0]) +
            (map_probs[0][0] * map_probs[1][1] * map_probs[2][1] * map_probs[3][0] * map_probs[4][0]) +
            (map_probs[0][1] * map_probs[1][0] * map_probs[2][0] * map_probs[3][0]) +
            (map_probs[0][1] * map_probs[1][0] * map_probs[2][0] * map_probs[3][1] * map_probs[4][0]) +
            (map_probs[0][1] * map_probs[1][0] * map_probs[2][1] * map_probs[3][0] * map_probs[4][0]) +
            (map_probs[0][1] * map_probs[1][1] * map_probs[2][0] * map_probs[3][0] * map_probs[4][0])
    )
    return prob_team1, 1 - prob_team1

def show():
    st.markdown("<h1 class='title'>Team Win Probabilities</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>Select two teams to view their win probabilities on each map. Based on our Elo ratings</h2>", unsafe_allow_html=True)

    # Fetch the latest Elo ratings from the database
    elo_df = fetch_display_elos()

    # Sidebar for team selection
    with st.sidebar:
        team1 = st.selectbox('Select Team 1', list(team_full_names.values()), key='team1')
        team2 = st.selectbox('Select Team 2', list(team_full_names.values()), key='team2')

    # Map full team names back to abbreviations
    team_abbr = {v: k for k, v in team_full_names.items()}
    team1_abbr = team_abbr[team1]
    team2_abbr = team_abbr[team2]

    # Filter Elo ratings for the selected teams
    team1_elos = elo_df[elo_df['team'] == team1_abbr]
    team2_elos = elo_df[elo_df['team'] == team2_abbr]

    # Ensure we have the same maps in both DataFrames
    maps = set(team1_elos['map']).intersection(set(team2_elos['map']))

    # Create a DataFrame to store the probabilities
    prob_list = []
    for map_name in maps:
        team1_elo = team1_elos[team1_elos['map'] == map_name]['elo_rating'].values[0]
        team2_elo = team2_elos[team2_elos['map'] == map_name]['elo_rating'].values[0]
        prob1, prob2 = calculate_win_probability(team1_elo, team2_elo)

        if prob1 > prob2:
            prob_list.append({'Map': map_name, 'Team': team1_abbr, 'Win Probability': f'{prob1:.2%}'})
        else:
            prob_list.append({'Map': map_name, 'Team': team2_abbr, 'Win Probability': f'{prob2:.2%}'})

    prob_df = pd.DataFrame(prob_list)

    # Add the full team name and logo HTML to the DataFrame
    try:
        prob_df['Team'] = prob_df['Team'].apply(
            lambda abbr: f'<img src="{team_logos[abbr]}" style="width: 60px; height: 60px;"> {team_full_names[abbr]}')
    except KeyError as e:
        st.error(f"KeyError: {e} - The 'Team' column is missing in prob_df.")

    prob_df['Map'] = prob_df['Map'].apply(lambda map_name: f'<img src="{map_images[map_name]}" style="width: 100%;">')

    # Display the team logos above the table
    team1_logo_html = f'<img src="{team_logos[team1_abbr]}" style="width: 100px; height: 100px;">'
    team2_logo_html = f'<img src="{team_logos[team2_abbr]}" style="width: 100px; height: 100px;">'
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            {team1_logo_html} <span style="font-size: 30px; font-weight: bold;">vs</span> {team2_logo_html}
        </div>
    """, unsafe_allow_html=True)

    # Custom CSS for styling the table
    st.markdown(f"""
        <style>
        .custom-table {{
            width: 80%;  /* Reduce the table width to 80% */
            border-collapse: collapse;
            margin: auto;  /* Center the table */
        }}
        .custom-table th, .custom-table td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;  /* Center headers and data */
        }}
        .custom-table th {{
            background-color: #131B61;  /* Custom color for the header */
            font-size: 24px;  /* Increase header font size */
        }}
        .custom-table td {{
            font-size: 20px;  /* Increase data font size */
            height: 60px;  /* Adjust this value to set the desired row height */
        }}
        .custom-table tr:nth-child(even) {{
            background-color: #000000;  /* Lighter gray for even rows */
        }}
        .custom-table tr:nth-child(odd) {{
            background-color: #131B61;  /* Darker gray for odd rows */
        }}
        .custom-table td.map-column {{
            width: 150px;  /* Adjust this value to set the desired column width */
        }}
        .custom-table td.team-column, .custom-table td.win-probability-column {{
            text-align: center;  /* Center the data in the Team and Win Probability columns */
        }}
        </style>
    """, unsafe_allow_html=True)

    # Create the HTML table with the map column class
    html_table = prob_df.to_html(index=False, escape=False, classes='custom-table')
    html_table = html_table.replace('<td>', '<td class="map-column">')  # Add the map-column class to the map cells
    html_table = html_table.replace('<th>Team</th>', '<th class="team-column">Team</th>')  # Center the Team header
    html_table = html_table.replace('<th>Win Probability</th>', '<th class="win-probability-column">Win Probability</th>')  # Center the Win Probability header

    st.markdown(html_table, unsafe_allow_html=True)

    # Match predictor
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 class='title'>Match Predictor</h1>", unsafe_allow_html=True)

    # Check if both teams have played all maps
    team1_played_all_maps = len(set(team1_elos['map'])) == len(map_images)
    team2_played_all_maps = len(set(team2_elos['map'])) == len(map_images)

    selected_maps = []

    if team1_played_all_maps and team2_played_all_maps:
        # Sidebar for match predictor
        with st.sidebar:
            bo_type = st.selectbox('Select Match Type (Best of 3 or 5)', ['BO3', 'BO5'], key='bo_type')
            manual_map_selection = st.checkbox('Manual Map Selection', key='manual_map_selection')

            if manual_map_selection:
                for i in range(1, (3 if bo_type == 'BO3' else 5) + 1):
                    selected_maps.append(st.selectbox(f'Select Map {i}', list(maps), key=f'map_{i}'))

        if not manual_map_selection:
            map_probs = {}
            for map_name in maps:
                team1_elo = team1_elos[team1_elos['map'] == map_name]['elo_rating'].values[0]
                team2_elo = team2_elos[team2_elos['map'] == map_name]['elo_rating'].values[0]
                prob1, prob2 = calculate_win_probability(team1_elo, team2_elo)
                map_probs[map_name] = (prob1, prob2)

            if bo_type == 'BO3':
                if len(map_probs) < 3:
                    st.warning("Not enough maps to produce optimal map pool. Please use manual map selection.")
                    manual_map_selection = True
                else:
                    # Team 1 bans the map they have the lowest winning % for
                    ban1 = min(map_probs, key=lambda x: map_probs[x][0])
                    map_probs.pop(ban1)

                    # Team 2 bans the map they have the lowest winning % for
                    ban2 = min(map_probs, key=lambda x: map_probs[x][1])
                    map_probs.pop(ban2)

                    # Team 1 picks the map they have the highest win % for (this becomes map 1)
                    pick1 = max(map_probs, key=lambda x: map_probs[x][0])
                    map_probs.pop(pick1)

                    # Team 2 picks the map they have the highest win % for (this becomes map 2)
                    pick2 = max(map_probs, key=lambda x: map_probs[x][1])
                    map_probs.pop(pick2)

                    # Team 1 bans the map they have the worst win % for
                    ban3 = min(map_probs, key=lambda x: map_probs[x][0])
                    map_probs.pop(ban3)

                    # Team 2 bans the map they have the worst win % for
                    ban4 = min(map_probs, key=lambda x: map_probs[x][1])
                    map_probs.pop(ban4)

                    # The final remaining map becomes map 3
                    pick3 = list(map_probs.keys())[0]

                    selected_maps = [pick1, pick2, pick3]

                    # Build the optimal selection description
                    optimal_selection_desc = f"{team1} ban {ban1}, {team2} ban {ban2}, " \
                                             f"{team1} pick {pick1}, {team2} pick {pick2}, " \
                                             f"{team1} ban {ban3}, {team2} ban {ban4}, " \
                                             f"and the final map is {pick3}."

                    # Display the optimal selection description
                    st.markdown("<h4 class='subtitle3'>Map pool with optimal selections (If both teams picked optimally to their win percentages on each map):", unsafe_allow_html=True)
                    st.markdown(f"""<h4 class='subtitle3'>{optimal_selection_desc}""", unsafe_allow_html=True)

            elif bo_type == 'BO5':
                if len(map_probs) < 5:
                    st.warning("Not enough maps to produce optimal map pool. Please use manual map selection.")
                    manual_map_selection = True
                else:
                    # Team 1 bans the map they have the lowest winning % for
                    ban1 = min(map_probs, key=lambda x: map_probs[x][0])
                    map_probs.pop(ban1)

                    # Team 2 bans the map they have the lowest winning % for
                    ban2 = min(map_probs, key=lambda x: map_probs[x][1])
                    map_probs.pop(ban2)

                    # Team 1 picks the map they have the highest win % for (this becomes map 1)
                    pick1 = max(map_probs, key=lambda x: map_probs[x][0])
                    map_probs.pop(pick1)

                    # Team 2 picks the map they have the highest win % for (this becomes map 2)
                    pick2 = max(map_probs, key=lambda x: map_probs[x][1])
                    map_probs.pop(pick2)

                    # Team 1 picks the map they have the highest win % for (this becomes map 3)
                    pick3 = max(map_probs, key=lambda x: map_probs[x][0])
                    map_probs.pop(pick3)

                    # Team 2 picks the map they have the highest win % for (this becomes map 4)
                    pick4 = max(map_probs, key=lambda x: map_probs[x][1])
                    map_probs.pop(pick4)

                    # The final remaining map becomes map 5
                    pick5 = list(map_probs.keys())[0]

                    selected_maps = [pick1, pick2, pick3, pick4, pick5]

                    # Build the optimal selection description
                    optimal_selection_desc = f"{team1} ban {ban1}, {team2} ban {ban2}, " \
                                             f"{team1} pick {pick1}, {team2} pick {pick2}, " \
                                             f"{team1} pick {pick3}, {team2} pick {pick4}, " \
                                             f"and the final map is {pick5}."

                    # Display the optimal selection description
                    st.markdown("<h4 class='subtitle3'>Map pool with optimal selections (If both teams picked optimally to their win percentages on each map):", unsafe_allow_html=True)
                    st.markdown(f"""<h4 class='subtitle3'>{optimal_selection_desc}""", unsafe_allow_html=True)

        # Calculate win probabilities for each selected map
        map_probs = []
        for map_name in selected_maps:
            team1_elo = team1_elos[team1_elos['map'] == map_name]['elo_rating'].values[0]
            team2_elo = team2_elos[team2_elos['map'] == map_name]['elo_rating'].values[0]
            prob1, prob2 = calculate_win_probability(team1_elo, team2_elo)
            map_probs.append((prob1, prob2))

        # Collect rows in a list and create DataFrame in one go
        rows = []
        for i, map_name in enumerate(selected_maps):
            prob1, prob2 = map_probs[i]
            rows.append({'Map': map_name, f'{team1} Win Probability': f'{prob1:.2%}', f'{team2} Win Probability': f'{prob2:.2%}'})

        match_prob_df = pd.DataFrame(rows)
        match_prob_df = match_prob_df.reset_index(drop=True)
        match_prob_df.index = match_prob_df.index + 1
        match_prob_df.index.name = '#'

        # Calculate overall match win probabilities
        if bo_type == 'BO3':
            win_prob_team1, win_prob_team2 = calculate_bo3_match_win_probability(map_probs)
        else:
            win_prob_team1, win_prob_team2 = calculate_bo5_match_win_probability(map_probs)

        st.markdown(f"""<h2 class='subtitle'>Match win probabilities for {team1} vs {team2}:</h2>""", unsafe_allow_html=True)
        st.markdown(f"""<h4 class='subtitle2'>{team1}: {win_prob_team1:.2%}</h4>""", unsafe_allow_html=True)
        st.markdown(f"""<h4 class='subtitle2'>{team2}: {win_prob_team2:.2%}</h4>""", unsafe_allow_html=True)

        # Display the match probabilities table using st.table
        st.table(match_prob_df)

    else:
        # Sidebar for manual map selection only
        with st.sidebar:
            bo_type = st.selectbox('Select Match Type', ['BO3', 'BO5'], key='manual_bo_type')
            st.warning("Not enough maps to produce optimal map pool. Please use manual map selection.")

            for i in range(1, (3 if bo_type == 'BO3' else 5) + 1):
                selected_maps.append(st.selectbox(f'Select Map {i}', list(maps), key=f'manual_map_{i}'))

        # Calculate win probabilities for each selected map
        map_probs = []
        for map_name in selected_maps:
            team1_elo = team1_elos[team1_elos['map'] == map_name]['elo_rating'].values[0]
            team2_elo = team2_elos[team2_elos['map'] == map_name]['elo_rating'].values[0]
            prob1, prob2 = calculate_win_probability(team1_elo, team2_elo)
            map_probs.append((prob1, prob2))

        # Collect rows in a list and create DataFrame in one go
        rows = []
        for i, map_name in enumerate(selected_maps):
            prob1, prob2 = map_probs[i]
            rows.append({'Map': map_name, f'{team1} Win Probability': f'{prob1:.2%}', f'{team2} Win Probability': f'{prob2:.2%}'})

        match_prob_df = pd.DataFrame(rows)
        match_prob_df = match_prob_df.reset_index(drop=True)
        match_prob_df.index = match_prob_df.index + 1
        match_prob_df.index.name = '#'

        # Calculate overall match win probabilities
        if bo_type == 'BO3':
            win_prob_team1, win_prob_team2 = calculate_bo3_match_win_probability(map_probs)
        else:
            win_prob_team1, win_prob_team2 = calculate_bo5_match_win_probability(map_probs)

        st.markdown(f"""<h2 class='subtitle'>Match win probabilities for {team1} vs {team2}:</h2>""", unsafe_allow_html=True)
        st.markdown(f"""<h4 class='subtitle2'>{team1}: {win_prob_team1:.2%}</h4>""", unsafe_allow_html=True)
        st.markdown(f"""<h4 class='subtitle2'>{team2}: {win_prob_team2:.2%}""", unsafe_allow_html=True)

        # Display the match probabilities table using st.table
        st.table(match_prob_df)























