# flask_server.py
import sys
from flask import Flask, jsonify
import plotly.graph_objs as go
import json
# from tools.data_processing import haversine, enhance_dataframe
# from tools.data_loader import get_data_from_url, parse_gpx_to_dataframe, parse_gpx_file
from flask import Flask, request, jsonify
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px



app = Flask(__name__)

@app.route('/load_wydatki_2022', methods=['POST'])
def load_wydatki_2022():
    df = pd.read_csv('../data/wydatki_2022.csv')
    return df.to_json(orient='split')


@app.route('/sankey_all_to_grupa', methods=['POST'])
def sankey_all():
    data_json = json.loads(request.data)
    df = pd.read_json(data_json, orient='split')
    wydatki_df = df
    grouped_by_unit_and_group = wydatki_df.groupby(['Nazwa Jednostki', 'Grupa'])['PL'].sum().reset_index()

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
    fig_json = json.loads(fig1.to_json())
    return jsonify(fig_json)


@app.route('/sankey_grupa_to_paragraf', methods=['POST'])
def sankey_all():
    data_json = json.loads(request.data)
    df = pd.read_json(data_json, orient='split')
    wydatki_df = df

    grouped_by_group_and_paragraph = wydatki_df.groupby(['Grupa', 'Paragraf'])['PL'].sum().reset_index()

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




    fig_json = json.loads(fig1.to_json())
    return jsonify(fig_json)


if __name__ == "__main__":
    app.run(port=5000)

