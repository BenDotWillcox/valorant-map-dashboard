import streamlit as st
from streamlit_option_menu import option_menu
from tabs import current_map_rankings, map_elo_history, team_win_probabilities

# Set up the Streamlit app configuration
st.set_page_config(page_title="Valorant League Data Visualization App", layout="wide")

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
load_css("styles.css")

# Create a horizontal navigation menu at the top of the screen
selected = option_menu(
    menu_title=None,  # No title for the menu
    options=["Current Map Rankings", "Map Elo History", "Team Win Probabilities"],  # Menu options
    icons=["list", "graph-up-arrow", "bar-chart"],  # Icons for the menu options
    menu_icon="cast",  # Menu icon
    default_index=0,  # Default selected menu option
    orientation="horizontal",  # Menu orientation
)

# Display the content for the selected tab
if selected == "Current Map Rankings":
    current_map_rankings.show()
elif selected == "Map Elo History":
    map_elo_history.show()
elif selected == "Team Win Probabilities":
    team_win_probabilities.show()





