import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px

df = pd.read_csv("../data/wydatki_2022.csv")
df = df[['Nazwa Jednostki', 'Regon', 'Grupa',	'Paragraf',	'P4',	'PL'	,'ZA' ,'WW'	,'ZO']]

# Utwórz st.session_state, jeśli jeszcze nie istnieje
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = df

# Wyświetl AgGrid
grid_response = AgGrid(
    df, 
    height=400, 
    width='100%',
    data_return_mode='FILTERED'
)

# Aktualizuj st.session_state z przefiltrowaną ramką danych
if grid_response.get('data') is not None:
    st.session_state.filtered_data = pd.DataFrame(grid_response['data'])

# Wyświetl wykres
fig = px.bar(st.session_state.filtered_data, x='C', y=['A', 'B'], title='Przefiltrowane dane')
st.plotly_chart(fig)
