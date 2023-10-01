import streamlit as st
st.set_page_config(layout="wide")
import time
import numpy as np
import requests
import plotly.graph_objects as go
import pandas as pd
import json

from io import StringIO
import plotly.express as px


wydatki_df = pd.read_csv('../data/wydatki_2022.csv')
schools = wydatki_df['Nazwa Jednostki'].unique()

col1, col2 = st.columns(2, gap="large")

with col1:
    school_one = st.selectbox('Wybierz placówkę nr 1', schools, help = 'Wybierz szkołę, aby zobaczyć wydatki')
    regon = wydatki_df[wydatki_df['Nazwa Jednostki'] == school_one]['Regon'].unique()[0]
    # st.write(regon)

    df_student_count = pd.read_csv('../data/uczniowie.csv')
    df_student_count = df_student_count[df_student_count['Regon'] == regon]
    student_count = df_student_count['Liczba uczniów'].values[0]

    df_stanin_sum = pd.read_csv('../data/staniny2022.csv')
    df_stanin_sum = df_stanin_sum[df_stanin_sum['Regon'] == regon]
    df_stanin_sum = df_stanin_sum['suma'].values[0]
    selected_school = wydatki_df[wydatki_df['Nazwa Jednostki'] == school_one]
    suma_ww = int(selected_school['WW'].sum())
    
    m2, m3, m4 , m5 = st.columns((1,1,1.4, 1.3))
    
    m2.metric(label = 'Liczba uczniów', value = student_count, delta = '')
    m3.metric(label = 'Suma skali staninowej', value = df_stanin_sum, delta = '')
    m4.metric(label = 'Wydatki wykonane IV kwartał', value = str(suma_ww) + " zł", delta = '')
    m5.metric(label = 'Średnia wydatków na ucznia', value = str(round(suma_ww/student_count, 2)) + " zł", delta = '')
    ##
    szkola_przeplywy = selected_school
    st.write("Proporcje wydatków wykonanych (WW) na daną grupę")
    total_expenses_per_unit = szkola_przeplywy.groupby("Nazwa Jednostki").sum()[["PL", "ZA", "WW", "ZO"]]
    selected_unit = total_expenses_per_unit.index[0]
    pie_data = szkola_przeplywy[szkola_przeplywy["Nazwa Jednostki"] == selected_unit].groupby("Grupa").sum()["WW"]
    # Using the previously defined pie_data
    labels = pie_data.index
    values = pie_data.values

    # Creating the pie chart using plotly
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.3, title="Proporcje wydatków wykonanych (WW) dla"))
    st.plotly_chart(fig, use_container_width=False)
with col2:
    school_two = st.selectbox('Wybierz placówkę nr 2', schools, help = 'Wybierz szkołę, aby zobaczyć wydatki')
    regon = wydatki_df[wydatki_df['Nazwa Jednostki'] == school_two]['Regon'].unique()[0]
    # st.write(regon)

    df_student_count = pd.read_csv('../data/uczniowie.csv')
    df_student_count = df_student_count[df_student_count['Regon'] == regon]
    student_count = df_student_count['Liczba uczniów'].values[0]

    df_stanin_sum = pd.read_csv('../data/staniny2022.csv')
    df_stanin_sum = df_stanin_sum[df_stanin_sum['Regon'] == regon]
    df_stanin_sum = df_stanin_sum['suma'].values[0]
    selected_school = wydatki_df[wydatki_df['Nazwa Jednostki'] == school_two]
    suma_ww = int(selected_school['WW'].sum())
    
    m2, m3, m4 , m5 = st.columns((1,1,1.4, 1.3))
    #
    szkola_przeplywy = selected_school
    m2.metric(label = 'Liczba uczniów', value = student_count, delta = '')
    m3.metric(label = 'Suma skali staninowej', value = df_stanin_sum, delta = '')
    m4.metric(label = 'Wydatki wykonane IV kwartał', value = str(suma_ww) + " zł", delta = '')
    m5.metric(label = 'Średnia wydatków na ucznia', value = str(round(suma_ww/student_count, 2)) + " zł", delta = '')
    st.write("Proporcje wydatków wykonanych (WW) na daną grupę")
    total_expenses_per_unit = szkola_przeplywy.groupby("Nazwa Jednostki").sum()[["PL", "ZA", "WW", "ZO"]]
    selected_unit = total_expenses_per_unit.index[0]
    pie_data = szkola_przeplywy[szkola_przeplywy["Nazwa Jednostki"] == selected_unit].groupby("Grupa").sum()["WW"]
    # Using the previously defined pie_data
    labels = pie_data.index
    values = pie_data.values

    # Creating the pie chart using plotly
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.3, title="Proporcje wydatków wykonanych (WW) dla"))
    st.plotly_chart(fig, use_container_width=False)