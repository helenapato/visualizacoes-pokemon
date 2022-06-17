# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

import data
import visualizations

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

pokemon = data.read_process_data()

app.layout = html.Div(children=[
    html.H1(children='Visualizações Pokémon'),

    html.H2(children='Histograma da qualidade dos pokémon'),

    dcc.Graph(
        id='quality-histogram',
        figure=visualizations.quality_histogram(pokemon)
    ),

    html.Div(children='''
        Texto explicando o gráfico acima.
    '''),

    html.H2(children='Radar de habilidades'),

    dcc.Dropdown(
        id='select-pokemon',
        options=pokemon['name'],
        value=['Arceus', 'Dialga', 'Zekrom', 'Palkia', 'Reshiram', 'Giratina'],
        multi=True
    ),

    dcc.Graph(
        id='ability-radar',
        figure=visualizations.ability_radar(pokemon, ['Arceus', 'Dialga', 'Zekrom', 'Palkia', 'Reshiram', 'Giratina'])
    ),
    html.Div(children='''
        Texto explicando o gráfico acima.
    ''')
])

@app.callback(
    Output('ability-radar', 'figure'),
    Input('select-pokemon', 'value'))
def update_ability_radar(value):
    return visualizations.ability_radar(pokemon, value)

if __name__ == '__main__':
    app.run_server(debug=True)
