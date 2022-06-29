from styles import *
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

import data
import visualizations

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

pokemon = data.read_process_data()

vis_corr_capture_quality, corr = visualizations.capture_rate_quality_correlation(pokemon)

sidebar = html.Div(
    [
        html.H2("Visualizações"), html.Hr(),
        html.A("Pequenos múltiplos correlacionando todos os atributos", href="#small-multiples-all-atributtes-id"), html.Hr(),
        html.A("Histograma da qualidade dos pokémon", href="#quality-histogram-id"), html.Hr(),
        html.A("Correlação entre dificuldade de captura e qualidade do Pokémon", href="#scatter-capture-quality-id"), html.Hr(),
        html.A("Treemap da distribuição de tipos primário e secundário", href="#treemap-types-id"), html.Hr(),
        html.A("Mapa de calor da combinação de tipos", href="#heatmap-type-combination-id"), html.Hr(),
        html.A("Evolução da proporção de tipos", href="#stacked-area-type-evolution-id"), html.Hr(),
        html.A("Mapa de tipos", href="#general-type-chart-id"), html.Hr(),
        html.A("Radar de atributos", href="#attribute-radar-id"), html.Hr(),
        html.A("Mapa de tipos de uma equipe", href="#team-type-chart-id"), html.Hr(),
        html.A("Cobertura de defesa da equipe", href="#teams-defense-coverage-id"), html.Hr(),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    children=[
        html.H1(children='Visualizações Pokémon'),

        html.Div([
            html.H2(children='Pequenos múltiplos correlacionando todos os atributos'),
            dcc.Graph(
                id='small-multiples-all-atributtes',
                figure=visualizations.small_mulitples_all_atributtes(pokemon)
            ),
            html.P('''
                Cada pokémon possui 6 atributos de batalha. São eles: Velocidade, Ataque, Ataque Especial, 
                Defesa, Defesa Especial, Pontos de Vida. Eles são numéricos e quanto maiores, melhor. 
                
                Os gráficos de dispersão acima mostram a correlação entre cada um desses atributos com 
                todos os outros. Cada ponto é um pokémon.
            ''')
        ],
        id='small-multiples-all-atributtes-id'
        ),
   
        html.Div([
            html.H2(children='Histograma da qualidade dos pokémon'),
            dcc.Graph(
                id='quality-histogram',
                figure=visualizations.quality_histogram(pokemon)
            ),
            html.P('''Uma forma de medir aproximadamente a "qualidade" de um pokémon é calculando a 
            soma dos seus 6 atributos de batalha. 
            
            Existem dois tipos de pokémon, regulares e lendários. Lendários são pokémon exclusivos e 
            normalmente possuem limtações no uso competitivo.
            
            O gráfico acima mostra 2 histogramas de qualidade dos pokémon, ou seja, a quantidade de pokémon 
            cujos atributos de batalha têm como soma um determinado valor, que quanto maior, melhor. 
            Separamos os pokémon regulares e lendários entre histogramas azul e vermelho, respectivamente.'''),
        ],
            id="quality-histogram-id",
        ),
        
        html.Div([
            html.H2(children='Correlação entre dificuldade de captura e quão bom o Pokémon é'),
            dcc.Graph(
                id='scatter-capture-quality',
                figure=vis_corr_capture_quality
            ),
            html.P(f'''
                Pokémon precisam ser capturado e cada um deles possui uma dificuldade de captura 
                associada (taxa de captura, quanto mais alta mais fácil). 
                O gráfico de sipersão acima mostra a correlação entre a taxa de captura e a qualidade 
                de um pokémon (soma dos 6 atributos de batalha). 
                O coeficiente de correlação observado é {corr}.
            ''')
            ],  
            id="scatter-capture-quality-id",
        ),

        html.Div([
            html.H2(children='Treemap da distribuição de tipos primário e secundário'),
            dcc.Graph(
                id='treemap-types',
                figure=visualizations.type_proportion(pokemon)
            ),
            html.P('''
                Cada pokémon possuí um tipo primario obrigatório e um tipo secundário opcional. 
                O gráfico treemap acima mostra a proporção entre todos os tipos primários de pokémon. 
                Podemos clicar em cada quadrado para mostrar a proporção de tipos secundários 
                para aquele determinado tipo primário.
            ''')
            ],
            id="treemap-types-id",
        ),
        
        html.Div([
            html.H2(children='Mapa de calor da combinação de tipos'),
            dcc.Graph(
                id='heatmap-type-combination',
                figure=visualizations.type_combination_correlation(pokemon)
            ),
            html.P('''
                O gráfico acima considera todas as combinações possíveis de tipos (primário + secundário) 
                e visualiza a incidência através de um mapa de calor.
            ''')
            ],
            id="heatmap-type-combination-id",
        ),

        html.Div([
            html.H2(children='Evolução da proporção de tipos'),
            dcc.Graph(
                id='stacked-area-type-evolution-cumulative',
                figure=visualizations.type_proportion_evolution_cumulative(pokemon)
            ),
            dcc.Graph(
                id='stacked-area-type-evolution-absolute',
                figure=visualizations.type_proportion_evolution_absolute(pokemon)
            ),
            html.P('''
                Em cada geração uma nova leva de pokémon é adicionada, os gráficos acima mostram como 
                a proporção entre tipos se manteve com o passar das gerações. 
                O primeiro gráfico mostra os valores de forma acumulada, o seja cada geração é a soma 
                dela com todas as gerações anteriores; já o segundo gráfico mostra os valores mostra o 
                valor de forma absoluta, ou seja o valor mostrado é apenas a quantidade de pokémon 
                adicionada na geração em questão.
            ''')
            ],
            id="stacked-area-type-evolution-id",
        ),

        html.Div([
            html.H2(children='Mapa de tipos'),
            dcc.Graph(
                id='type-chart',
                figure=visualizations.general_type_chart(pokemon)
            ),
            html.P('''
                Os tipos de um pokémon interferem em como ele receberá e causará dano em batalhas. 
                Cada tipo de pokémon possui um multiplicador associado a todos os tipos de pokémon, 
                ou seja, cada tipo recebe dano diferentemente de cada outro tipo.
            ''')
            ],
            id='general-type-chart-id'
        ),

        html.Div([
            html.H2(children='Radar de atributos'),
            dcc.Dropdown(
                id='select-pokemon',
                options=pokemon['name'],
                value=['Bulbasaur','Chikorita','Chespin','Snivy','Charmander','Treecko'],
                multi=True
            ),
            dcc.Graph(
                id='attribute-radar-1',
                figure=visualizations.attribute_radar(pokemon, ['Bulbasaur','Chikorita','Chespin','Snivy','Charmander','Treecko'])
            ),
            dcc.Dropdown(
                id='select-pokemon-6',
                options=pokemon['name'],
                value=['Charmander','Squirtle','Pikachu','Pidgey','Gastly', 'Abra'],
                multi=True
            ),
            dcc.Graph(
                id='attribute-radar-2',
                figure=visualizations.attribute_radar(pokemon, ['Charmander','Squirtle','Pikachu','Pidgey','Gastly', 'Abra'])
            ),
            html.P('''
                O gráfico acima mostra os 6 atributos de batalha de 1 ou mais pokémon à sua escolha 
                em formato de radar. Nese tipo de visualização podemos perceber se os atributos de 
                batalha da equipe estão equilibrados. 
                "Vales" mostram deficiências em determinados atributos.
            ''')
            ],
            id='attribute-radar-id'
        ),
        
        html.Div([
            html.H2(children='Mapa de tipos de uma equipe'),
            dcc.Dropdown(
                id='select-pokemon2',
                options=pokemon['name'],
                value=['Bulbasaur','Chikorita','Chespin','Snivy','Charmander','Treecko'],
                multi=True
            ),
            dcc.Graph(
                id='team-type-chart-1',
                figure=visualizations.team_type_chart(pokemon, ['Bulbasaur','Chikorita','Chespin','Snivy','Charmander','Treecko'])
            ),
             dcc.Dropdown(
                id='select-pokemon5',
                options=pokemon['name'],
                value=['Charmander','Squirtle','Pikachu','Pidgey','Gastly', 'Abra'],
                multi=True
            ),
            dcc.Graph(
                id='team-type-chart-2',
                figure=visualizations.team_type_chart(pokemon, ['Charmander','Squirtle','Pikachu','Pidgey','Gastly', 'Abra'])
            ),
            html.P('''
                Mapa de tipo para uma equipe de pokémon específica. Informe os pokémon desejados e veja 
                qual é o multiplicador de dano recebido de cada um dos 18 tipos de pokémon.
            '''),
            ],
            id='team-type-chart-id'
        ),

        html.Div([
            html.H2(children='Cobertura de defesa da equipe'),
            html.Label('Equipe 1'),
            dcc.Dropdown(
                id='select-pokemon3',
                options=pokemon['name'],
                value=['Bulbasaur','Chikorita','Chespin','Snivy','Charmander','Treecko'],
                multi=True
            ),
            html.Label('Equipe 2'),
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
            html.P('''Forma inteligente de visualizar a cobrtura de defesa de uma equipe. 
            Calculamos cada valor através da média dos multiplicadores de dano recebido de cada um dos 
            18 tipos, para cada pokémon da equipe definida. 
            
            Equipes com tipos variados se mostram como escolhas mais seguras, menos picos(desvantagens 
            grandes) e menos vales(vantagens grandes).'''),
        ],
        id="teams-defense-coverage-id",
        ),
    ],
    style=CONTENT_STYLE
)

app.layout = html.Div([sidebar, content])

@app.callback(
    Output('attribute-radar-1', 'figure'),
    Input('select-pokemon', 'value'))
def update_attribute_radar(value):
    return visualizations.attribute_radar(pokemon, value)

@app.callback(
    Output('attribute-radar-2', 'figure'),
    Input('select-pokemon-6', 'value'))
def update_attribute_radar(value):
    return visualizations.attribute_radar(pokemon, value)

@app.callback(
    Output('team-type-chart-1', 'figure'),
    Input('select-pokemon2', 'value'))
def update_team_type_chart(value):
    return visualizations.team_type_chart(pokemon, value)

@app.callback(
    Output('team-type-chart-2', 'figure'),
    Input('select-pokemon5', 'value'))
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
