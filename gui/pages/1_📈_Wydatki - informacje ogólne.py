import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
import json

from io import StringIO
import plotly.express as px


with st.spinner('Aktualizacja raportu..'):
    wydatki_df = pd.read_csv('../data/wydatki_2022.csv')
    # st.dataframe(wydatki)
    schools = wydatki_df['Nazwa Jednostki'].unique()
    school = st.selectbox('Wybierz szkołę', schools, help = 'Wybierz szkołę, aby zobaczyć wydatki')
    
    regon = wydatki_df[wydatki_df['Nazwa Jednostki'] == school]['Regon'].unique()[0]
    # st.write(regon)

    df_student_count = pd.read_csv('../data/uczniowie.csv')
    df_student_count = df_student_count[df_student_count['Regon'] == regon]
    student_count = df_student_count['Liczba uczniów'].values[0]

    df_stanin_sum = pd.read_csv('../data/staniny2022.csv')
    df_stanin_sum = df_stanin_sum[df_stanin_sum['Regon'] == regon]
    df_stanin_sum = df_stanin_sum['suma'].values[0]
    selected_school = wydatki_df[wydatki_df['Nazwa Jednostki'] == school]
    
    suma_ww = int(selected_school['WW'].sum())
    
    m2, m3, m4 , m5 = st.columns((1,1,1.4, 1.3))
    #

    m2.metric(label = 'Liczba uczniów', value = student_count, delta = '')
    m3.metric(label = 'Suma skali staninowej', value = df_stanin_sum, delta = '')
    m4.metric(label = 'Wydatki wykonane IV kwartał', value = str(suma_ww) + " zł", delta = '')
    m5.metric(label = 'Średnia wydatków na ucznia', value = str(round(suma_ww/student_count, 2)) + " zł", delta = '')

    # st.write('### Wydatki na poszczególne kategorie')
    
    

    tab1, tab2, = st.tabs(["Wartości bezwzględne", "Średnia na ucznia"])

    with tab1:
        ### wizualizacja przepływy do grup
        szkola_przeplywy = selected_school
        grouped_by_unit_and_group = szkola_przeplywy.groupby(['Nazwa Jednostki', 'Grupa'])['PL'].sum().reset_index()

        # Lista źródeł, celów i wartości
        source = []
        target = []
        value = []

        # Dodanie danych do list
        for index, row in grouped_by_unit_and_group.iterrows():
            source.append(row['Nazwa Jednostki'])
            target.append('Grupa ' + str(row['Grupa']))
            value.append(row['PL'])

        # Tworzenie wykresu Sankeya dla pierwszego scenariusza
        fig1 = go.Figure(data=[go.Sankey(
            node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=source + target
            ),
            link=dict(
            source=[source.index(i) for i in source],
            target=[len(source) + target.index(i) for i in target],
            value=value
            )
        )])

        fig1.update_layout(title_text="Wydatki środków przez jednostkę na daną kategorię", font_size=10)
        st.plotly_chart(fig1, use_container_width=False)
            
        ### wizualizacja przepływy z grup do paragrafów

        grouped_by_group_and_paragraph = szkola_przeplywy.groupby(['Grupa', 'Paragraf'])['PL'].sum().reset_index()

        # Lista źródeł, celów i wartości dla drugiego scenariusza
        source2 = []
        target2 = []
        value2 = []

        # Dodanie danych do list
        for index, row in grouped_by_group_and_paragraph.iterrows():
            source2.append('Grupa ' + str(row['Grupa']))
            target2.append('Paragraf ' + str(row['Paragraf']))
            value2.append(row['PL'])

        data_scenario2 = {
            "source": source2,
            "target": target2,
            "value": value2
        }

        source = source2
        target = target2
        value = value2

        # Tworzenie wykresu
        fig = go.Figure(data=[go.Sankey(
            node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=source + target
            ),
            link=dict(
            source=[source.index(i) for i in source],
            target=[len(source) + target.index(i) for i in target],
            value=value
            )
        )])
        fig.update_layout(title_text="Przepływ środków od kategorii do paragrafów", font_size=10)
        st.plotly_chart(fig, use_container_width=False)

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
        # 1. Słupkowy wykres sumy planowanych wydatków wg kategorii (Grupa)

        filtered_data_corrected = szkola_przeplywy
        top_paragraf = filtered_data_corrected.groupby('Paragraf').sum().sort_values(by='ZA', ascending=False).head(10)
        grouped_PL = filtered_data_corrected.groupby('Grupa').sum().reset_index()
        fig1 = px.bar(grouped_PL, x='Grupa', y='PL', title='Suma planowanych wydatków wg kategorii (Grupa)', labels={'Grupa': 'Grupa', 'PL': 'Planowane wydatki'})
        st.plotly_chart(fig1, use_container_width=False)

        # 2. Słupkowy wykres sumy wykonanych wydatków wg kategorii (Grupa)
        grouped_WW = filtered_data_corrected.groupby('Grupa').sum().reset_index()
        fig2 = px.bar(grouped_WW, x='Grupa', y='WW', title='Suma wykonanych wydatków wg kategorii (Grupa)', color_discrete_sequence=['skyblue'], labels={'Grupa': 'Grupa', 'WW': 'Wykonane wydatki'})
        st.plotly_chart(fig2, use_container_width=False)

        # 3. Wykres kołowy zatwierdzonych wydatków dla największych paragrafów
        fig3 = px.pie(top_paragraf, values='ZA', names=top_paragraf.index, title='Zatwierdzone wydatki dla 10 największych paragrafów')
        st.plotly_chart(fig3, use_container_width=False)

        grouped_difference = filtered_data_corrected.groupby('Grupa').sum()
        grouped_difference['Difference'] = grouped_difference['PL'] - grouped_difference['WW']
        heatmap_data = filtered_data_corrected.pivot_table(values='WW', index='Paragraf', columns='Grupa', aggfunc='sum', fill_value=0)
        # 4. Słupkowy wykres różnicy między planowanymi a wykonanymi wydatkami dla każdej kategorii (Grupa)
        fig4 = px.bar(grouped_difference.reset_index(), x='Grupa', y='Difference', title='Różnica między planowanymi a wykonanymi wydatkami dla każdej kategorii (Grupa)', color_discrete_sequence=['salmon'])
        # fig4.write_html("/mnt/data/plot4_roznica_wydatki.html")
        st.plotly_chart(fig4, use_container_width=False)
        custom_scale = [
        [0, 'white'],  # Dla najniższych wartości kolor biały
        [1, 'black']   # Dla najwyższych wartości kolor czarny
        ]
        # 6. Mapa cieplna (heatmap) dla kategorii (Grupa) i paragrafów (Paragraf) w odniesieniu do wykonanych wydatków
        fig6 = px.imshow(heatmap_data, color_continuous_scale=custom_scale,title='Mapa cieplna wykonanych wydatków dla kategorii (Grupa) i paragrafów (Paragraf)')
        # fig6.write_html("/mnt/data/plot6_heatmap_wydatki.html")
        st.plotly_chart(fig6, use_container_width=False)
        # 7. Słupkowy wykres zobowiązań dla każdej kategorii (Grupa)
        grouped_ZO = filtered_data_corrected.groupby('Grupa').sum().reset_index()
        fig7 = px.bar(grouped_ZO, x='Grupa', y='ZO', title='Suma zobowiązań wg kategorii (Grupa)', color_discrete_sequence=['lightgreen'])
        # fig7.write_html("/mnt/data/plot7_zobowiazania.html")
        st.plotly_chart(fig7, use_container_width=False)
    with tab2:

        ### wizualizacja przepływy do grup
        szkola_przeplywy = selected_school
        szkola_przeplywy['WW'] = szkola_przeplywy['WW']/student_count
        szkola_przeplywy['PL'] = szkola_przeplywy['PL']/student_count
        szkola_przeplywy['ZA'] = szkola_przeplywy['ZA']/student_count
        szkola_przeplywy['ZO'] = szkola_przeplywy['ZO']/student_count

        grouped_by_unit_and_group = szkola_przeplywy.groupby(['Nazwa Jednostki', 'Grupa'])['PL'].sum().reset_index()

        # Lista źródeł, celów i wartości
        source = []
        target = []
        value = []

        # Dodanie danych do list
        for index, row in grouped_by_unit_and_group.iterrows():
            source.append(row['Nazwa Jednostki'])
            target.append('Grupa ' + str(row['Grupa']))
            value.append(row['PL'])

        # Tworzenie wykresu Sankeya dla pierwszego scenariusza
        fig1 = go.Figure(data=[go.Sankey(
            node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=source + target
            ),
            link=dict(
            source=[source.index(i) for i in source],
            target=[len(source) + target.index(i) for i in target],
            value=value
            )
        )])

        fig1.update_layout(title_text="Wydatki środków przez jednostkę na daną kategorię", font_size=10)
        st.plotly_chart(fig1, use_container_width=False)
            
        ### wizualizacja przepływy z grup do paragrafów

        grouped_by_group_and_paragraph = szkola_przeplywy.groupby(['Grupa', 'Paragraf'])['PL'].sum().reset_index()

        # Lista źródeł, celów i wartości dla drugiego scenariusza
        source2 = []
        target2 = []
        value2 = []

        # Dodanie danych do list
        for index, row in grouped_by_group_and_paragraph.iterrows():
            source2.append('Grupa ' + str(row['Grupa']))
            target2.append('Paragraf ' + str(row['Paragraf']))
            value2.append(row['PL'])

        data_scenario2 = {
            "source": source2,
            "target": target2,
            "value": value2
        }

        source = source2
        target = target2
        value = value2

        # Tworzenie wykresu
        fig = go.Figure(data=[go.Sankey(
            node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=source + target
            ),
            link=dict(
            source=[source.index(i) for i in source],
            target=[len(source) + target.index(i) for i in target],
            value=value
            )
        )])
        fig.update_layout(title_text="Przepływ środków od kategorii do paragrafów", font_size=10)
        st.plotly_chart(fig, use_container_width=False)

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
        # 1. Słupkowy wykres sumy planowanych wydatków wg kategorii (Grupa)

        filtered_data_corrected = szkola_przeplywy
        top_paragraf = filtered_data_corrected.groupby('Paragraf').sum().sort_values(by='ZA', ascending=False).head(10)
        grouped_PL = filtered_data_corrected.groupby('Grupa').sum().reset_index()
        fig1 = px.bar(grouped_PL, x='Grupa', y='PL', title='Suma planowanych wydatków wg kategorii (Grupa)', labels={'Grupa': 'Grupa', 'PL': 'Planowane wydatki'})
        st.plotly_chart(fig1, use_container_width=False)

        # 2. Słupkowy wykres sumy wykonanych wydatków wg kategorii (Grupa)
        grouped_WW = filtered_data_corrected.groupby('Grupa').sum().reset_index()
        fig2 = px.bar(grouped_WW, x='Grupa', y='WW', title='Suma wykonanych wydatków wg kategorii (Grupa)', color_discrete_sequence=['skyblue'], labels={'Grupa': 'Grupa', 'WW': 'Wykonane wydatki'})
        st.plotly_chart(fig2, use_container_width=False)

        # 3. Wykres kołowy zatwierdzonych wydatków dla największych paragrafów
        fig3 = px.pie(top_paragraf, values='ZA', names=top_paragraf.index, title='Zatwierdzone wydatki dla 10 największych paragrafów')
        st.plotly_chart(fig3, use_container_width=False)

        grouped_difference = filtered_data_corrected.groupby('Grupa').sum()
        grouped_difference['Difference'] = grouped_difference['PL'] - grouped_difference['WW']
        heatmap_data = filtered_data_corrected.pivot_table(values='WW', index='Paragraf', columns='Grupa', aggfunc='sum', fill_value=0)
        # 4. Słupkowy wykres różnicy między planowanymi a wykonanymi wydatkami dla każdej kategorii (Grupa)
        fig4 = px.bar(grouped_difference.reset_index(), x='Grupa', y='Difference', title='Różnica między planowanymi a wykonanymi wydatkami dla każdej kategorii (Grupa)', color_discrete_sequence=['salmon'])
        # fig4.write_html("/mnt/data/plot4_roznica_wydatki.html")
        st.plotly_chart(fig4, use_container_width=False)
        custom_scale = [
        [0, 'white'],  # Dla najniższych wartości kolor biały
        [1, 'black']   # Dla najwyższych wartości kolor czarny
        ]
        # 6. Mapa cieplna (heatmap) dla kategorii (Grupa) i paragrafów (Paragraf) w odniesieniu do wykonanych wydatków
        fig6 = px.imshow(heatmap_data, color_continuous_scale=custom_scale,title='Mapa cieplna wykonanych wydatków dla kategorii (Grupa) i paragrafów (Paragraf)')
        # fig6.write_html("/mnt/data/plot6_heatmap_wydatki.html")
        st.plotly_chart(fig6, use_container_width=False)
        # 7. Słupkowy wykres zobowiązań dla każdej kategorii (Grupa)
        grouped_ZO = filtered_data_corrected.groupby('Grupa').sum().reset_index()
        fig7 = px.bar(grouped_ZO, x='Grupa', y='ZO', title='Suma zobowiązań wg kategorii (Grupa)', color_discrete_sequence=['lightgreen'])
        # fig7.write_html("/mnt/data/plot7_zobowiazania.html")
        st.plotly_chart(fig7, use_container_width=False)
    

