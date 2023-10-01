import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
import plotly.express as px

# Dwie przykładowe ramki danych
df1 = pd.DataFrame({
    'A': range(1, 11),
    'B': range(10, 0, -1),
    'C': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
})

df2 = pd.DataFrame({
    'A': range(11, 21),
    'B': range(20, 10, -1),
    'C': ['k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']
})

# Inicjalizacja st.session_state dla przefiltrowanych ramek danych
if 'filtered_data1' not in st.session_state:
    st.session_state.filtered_data1 = df1

if 'filtered_data2' not in st.session_state:
    st.session_state.filtered_data2 = df2

# Wyświetl pierwszy AgGrid
st.write("Filtruj pierwszą ramkę danych:")
grid_response1 = AgGrid(df1, height=400, width='100%', data_return_mode='FILTERED')
if grid_response1.get('data') is not None:
    st.session_state.filtered_data1 = pd.DataFrame(grid_response1['data'])

# Wyświetl drugi AgGrid
st.write("Filtruj drugą ramkę danych:")
grid_response2 = AgGrid(df2, height=400, width='100%', data_return_mode='FILTERED')
if grid_response2.get('data') is not None:
    st.session_state.filtered_data2 = pd.DataFrame(grid_response2['data'])

# Wyświetl wykres w oparciu o obie przefiltrowane ramki danych
combined_df = pd.concat([st.session_state.filtered_data1, st.session_state.filtered_data2], axis=0)
fig = px.bar(combined_df, x='C', y=['A', 'B'], title='Przefiltrowane dane z obu ramek danych')
st.plotly_chart(fig)
