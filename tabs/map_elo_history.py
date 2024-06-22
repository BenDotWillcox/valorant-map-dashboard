import streamlit as st
import pandas as pd
from db_config import get_db_connection
import altair as alt
from config import team_full_names, regions_teams, team_colors, team_shapes

@st.cache_data(ttl=6000)
def fetch_elo_history():
    conn = get_db_connection()
    query = 'SELECT * FROM elo_rating_history'
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def show():
    st.markdown("<h1 class='title'>Valorant League Map Elo History</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>Visualize the Elo rating history of teams over time.</h2>", unsafe_allow_html=True)

    # Sidebar for parameter selection
    with st.sidebar:
        view_type = st.radio("Select view type", ("By Team", "By Map"))

        if view_type == "By Map":
            region = st.selectbox('Select a region', list(regions_teams.keys()))
            map_name = st.selectbox('Select a map', ['Abyss', 'Ascent', 'Bind', 'Breeze', 'Haven', 'Icebox', 'Lotus', 'Split', 'Sunset'])  # Add your map options here
            teams_in_region = regions_teams[region]
            selected_teams = st.multiselect('Select teams', teams_in_region, default=teams_in_region)
        else:  # By Team
            team_name = st.selectbox('Select a team', list(team_full_names.values()))
            maps = ['Abyss', 'Ascent', 'Bind', 'Breeze', 'Haven', 'Icebox', 'Lotus', 'Split', 'Sunset']  # Add your map options here
            selected_maps = st.multiselect('Select maps', maps, default=maps)

    # Fetch the Elo rating history from the database
    elo_history_df = fetch_elo_history()

    if view_type == "By Map":
        # Filter the Elo history based on the selected region, map, and teams
        filtered_elo_history = elo_history_df[
            (elo_history_df['map'] == map_name) &
            (elo_history_df['team'].isin(selected_teams))
            ]

        # Replace team abbreviations with full names for display
        filtered_elo_history['team'] = filtered_elo_history['team'].apply(lambda abbr: team_full_names.get(abbr, abbr))

        # Create a color scale based on the team colors
        color_scale = alt.Scale(domain=list(filtered_elo_history['team'].unique()),
                                range=[team_colors[team] for team in filtered_elo_history['team'].unique()])

        # Create a shape scale based on the team shapes
        shape_scale = alt.Scale(domain=list(filtered_elo_history['team'].unique()),
                                range=[team_shapes[team] for team in filtered_elo_history['team'].unique()])

        # Create a step line chart to visualize the Elo history
        line_chart = alt.Chart(filtered_elo_history).mark_line(strokeWidth=3, interpolate='step-after').encode(
            x=alt.X('timestamp:T', title='Match Date',
                    axis=alt.Axis(format='%b %d', labelFontSize=12, titleFontSize=14)),
            y=alt.Y('elo_rating:Q', title='Elo Rating', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
            color=alt.Color('team:N', scale=color_scale,
                            legend=alt.Legend(title="Teams", labelFontSize=12, titleFontSize=14, labelColor='#000000',
                                              titleColor='#000000')),
            tooltip=['timestamp:T', 'elo_rating:Q', 'team:N', 'opponent:N', 'score:N']
        ).properties(height=600,
                     title={'text': ' ', 'subtitle': map_name})  # Adjust the height as needed

        points_chart = alt.Chart(filtered_elo_history).mark_point(size=100).encode(
            x=alt.X('timestamp:T', title='Match Date',
                    axis=alt.Axis(format='%b %d', labelFontSize=12, titleFontSize=14)),
            y=alt.Y('elo_rating:Q', title='Elo Rating', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
            color=alt.Color('team:N', scale=color_scale,
                            legend=alt.Legend(title="Teams", labelFontSize=12, titleFontSize=14)),
            shape=alt.Shape('team:N', scale=shape_scale),  # Apply shape encoding
            tooltip=['timestamp:T', 'elo_rating:Q', 'team:N', 'opponent:N', 'score:N']
        ).properties(height=600)  # Adjust the height as needed

        # Combine the line and points charts
        chart = line_chart + points_chart

        st.altair_chart(chart.configure(background='#FFFFFF').configure_axisX(labelColor='#000000',
                                                                              titleColor='#000000').configure_axisY(
            labelColor='#000000', titleColor='#000000'), use_container_width=True)

    elif view_type == "By Team":
        # Map full team names back to abbreviations for filtering
        team_abbr = {v: k for k, v in team_full_names.items()}
        team_abbr_name = team_abbr[team_name]

        # Filter the Elo history based on the selected team and maps
        filtered_elo_history = elo_history_df[
            (elo_history_df['team'] == team_abbr_name) &
            (elo_history_df['map'].isin(selected_maps))
            ]

        # Create a color scale based on the map names
        color_scale = alt.Scale(domain=maps,
                                range=['#000000', '#1f77b4', '#ff7f0e', '#2ca02c', '#8c564b', '#e377c2', '#9467bd', '#7c7d7c', '#d62728'])

        # Create a step line chart to visualize the Elo history
        line_chart = alt.Chart(filtered_elo_history).mark_line(strokeWidth=3, interpolate='step-after').encode(
            x=alt.X('timestamp:T', title='Match Date',
                    axis=alt.Axis(format='%b %d', labelFontSize=12, titleFontSize=14)),
            y=alt.Y('elo_rating:Q', title='Elo Rating', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
            color=alt.Color('map:N', scale=color_scale,
                            legend=alt.Legend(title="Maps", labelFontSize=12, titleFontSize=14, labelColor='#000000',
                                              titleColor='#000000')),
            tooltip=['timestamp:T', 'elo_rating:Q', 'map:N', 'opponent:N', 'score:N']
        ).properties(height=600,
                     title={'text': ' ', 'subtitle': team_name})  # Adjust the height as needed

        points_chart = alt.Chart(filtered_elo_history).mark_point(size=100).encode(
            x=alt.X('timestamp:T', title='Match Date',
                    axis=alt.Axis(format='%b %d', labelFontSize=12, titleFontSize=14)),
            y=alt.Y('elo_rating:Q', title='Elo Rating', axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
            color=alt.Color('map:N', scale=color_scale,
                            legend=alt.Legend(title="Maps", labelFontSize=12, titleFontSize=14)),
            tooltip=['timestamp:T', 'elo_rating:Q', 'map:N', 'opponent:N', 'score:N']
        ).properties(height=600)  # Adjust the height as needed

        # Combine the line and points charts
        chart = line_chart + points_chart

        st.altair_chart(chart.configure(background='#FFFFFF').configure_axisX(labelColor='#000000',
                                                                              titleColor='#000000').configure_axisY(
            labelColor='#000000', titleColor='#000000'), use_container_width=True)


