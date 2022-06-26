# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output

import data
import visualizations

app = Dash(__name__)

pokemon = data.read_process_data()

vis_corr_capture_quality, corr = visualizations.capture_rate_quality_correlation(pokemon)

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

    html.H2(children='Gráfico de dispersão - Correlação entre dificuldade de captura e quão bom o Pokémon é'),
    dcc.Graph(
        id='scatter-capture-quality',
        figure=vis_corr_capture_quality
    ),
    html.Div(children=f'''
        Texto explicando o gráfico acima. Coeficiente de correlação: {corr}.
    '''),

    html.H2(children='Treemap da distribuição de tipos primário e secundário'),
    dcc.Graph(
        id='treemap-types',
        figure=visualizations.type_proportion(pokemon)
    ),
    html.Div(children='''
        Texto explicando o gráfico acima.
    '''),

    html.H2(children='Mapa de calor da combinação de tipos'),
    dcc.Graph(
        id='heatmap-type-combination',
        figure=visualizations.type_combination_correlation(pokemon)
    ),
    html.Div(children='''
        Texto explicando o gráfico acima.
    '''),

    html.H2(children='Evolução da proporção de tipos'),
    dcc.Graph(
        id='stacked-area-type-evolution-cumulative',
        figure=visualizations.type_proportion_evolution_cumulative(pokemon)
    ),
    dcc.Graph(
        id='stacked-area-type-evolution-absolute',
        figure=visualizations.type_proportion_evolution_absolute(pokemon)
    ),
    html.Div(children='''
        Texto explicando o gráfico acima.
    '''),

    html.H2(children='Radar de atributos'),
    dcc.Dropdown(
        id='select-pokemon',
        options=pokemon['name'],
        value=['Arceus', 'Dialga', 'Zekrom', 'Palkia', 'Reshiram', 'Giratina'],
        multi=True
    ),
    dcc.Graph(
        id='attribute-radar',
        figure=visualizations.attribute_radar(pokemon, ['Arceus', 'Dialga', 'Zekrom', 'Palkia', 'Reshiram', 'Giratina'])
    ),
    html.Div(children='''
        Texto explicando o gráfico acima.
    ''')
])

@app.callback(
    Output('attribute-radar', 'figure'),
    Input('select-pokemon', 'value'))
def update_attribute_radar(value):
    return visualizations.attribute_radar(pokemon, value)

if __name__ == '__main__':
    app.run_server(debug=True)
