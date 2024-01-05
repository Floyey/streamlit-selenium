from functions import *

# Configurations de la page
streamlit.page_config('Dashboard')

st.title('How Long To Beat Dashboard')

# Afficher la sidebar
streamlit.show_sidebar()

value = st.text_input('Nom du jeu recherché')
if value:
    streamlit.show_games(value)
else:
    streamlit.show_games()
