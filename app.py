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
    '''),

    html.H2(children='Pequenos múltiplos correlacionando todos os atributos'),
    dcc.Graph(
        id='small-multiples-all-atributtes',
        figure=visualizations.small_mulitples_all_atributtes(pokemon)
    ),
    html.Div(children='''
        Texto explicando o gráfico acima.
    '''),

    html.H2(children='Mapa de tipos'),
    dcc.Graph(
        id='type-chart',
        figure=visualizations.general_type_chart(pokemon)
    ),
    
    html.H2(children='Mapa de tipos de uma equipe'),
    dcc.Dropdown(
        id='select-pokemon2',
        options=pokemon['name'],
        value=['Bulbasaur','Chikorita','Chespin','Snivy','Charmander','Treecko'],
        multi=True
    ),
    dcc.Graph(
        id='team-type-chart',
        figure=visualizations.team_type_chart(pokemon, ['Bulbasaur','Chikorita','Chespin','Snivy','Charmander','Treecko'])
    ),
    html.Div(children='''
        Texto explicando o gráfico acima.
    '''),

    html.H2(children='Cobertura de defesa da equipe'),
    html.Label('Team 1'),
    dcc.Dropdown(
        id='select-pokemon3',
        options=pokemon['name'],
        value=['Bulbasaur','Chikorita','Chespin','Snivy','Charmander','Treecko'],
        multi=True
    ),
    html.Label('Team 2'),
    dcc.Dropdown(
        id='select-pokemon4',
        options=pokemon['name'],
        value=['Charmander','Squirtle','Pikachu','Pidgey','Gastly', 'Abra'],
        multi=True
    ),
    dcc.Graph(
        id='teams-defense-coverage',
        figure=visualizations.radar_plot_teams_defense(pokemon, ['Bulbasaur','Chikorita','Chespin','Snivy','Charmander','Treecko'], ['Charmander','Squirtle','Pikachu','Pidgey','Gastly', 'Abra'])
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

@app.callback(
    Output('team-type-chart', 'figure'),
    Input('select-pokemon2', 'value'))
def update_team_type_chart(value):
    return visualizations.team_type_chart(pokemon, value)

@app.callback(
    Output('teams-defense-coverage', 'figure'),
    [Input('select-pokemon3', 'value'),
    Input('select-pokemon4', 'value')])
def update_team_type_chart(team1, team2):
    return visualizations.radar_plot_teams_defense(pokemon, team1, team2)

if __name__ == '__main__':
    app.run_server(debug=True)
