import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def attribute_radar(pokemon, poke_list):
    if poke_list == []:
        return attribute_radar(pokemon, ['Arceus'])

    # Atributos a serem mostrados
    categories = ['attack', 'defense', 'hp', 'sp_attack', 'sp_defense', 'speed']

    fig = go.Figure()
    max_list = []

    for p in poke_list:
        stats = pokemon.loc[pokemon['name'] == p, categories].squeeze()
        fig.add_trace(go.Scatterpolar(r=stats, theta=categories, fill='toself', name=p))
        max_list.append(max(stats))

    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, max(max_list)])),
                    title="Atributos da equipe",
                    legend_title="Equipe",
                    width=700, height=700)

    return fig

def capture_rate_quality_correlation(pokemon):
    fig = px.scatter(pokemon, x="how_good", y="capture_rate",
                 labels={
                     "how_good": "Soma dos atributos do pokémon",
                     "capture_rate": "Taxa de captura"},
                 title="Correlação da taxa de captura com a qualidade do pokémon", 
                 width=800, height=800)

    corr = np.corrcoef(pokemon['how_good'], pokemon['capture_rate'])[0,1]

    return fig, corr

def type_proportion(pokemon):
    # Não tá funcionando mudar de cor por algum motivo
    colors_dict = {'all':'lightgrey',
                'bug' : '#9c9c5e', 
                'dark' : 'black', 
                'dragon' : '#d62728', 
                'electric' : 'yellow', 
                'fairy' : 'pink', 
                'fighting' : '#636efa', 
                'fire' : '#e58606',
                'flying' : '#52c4ef',
                'ghost' : '#f2f2f2',
                'grass' : 'green',
                'ground' : '#8c564b',
                'ice' : 'lightblue',
                'none' : 'lightgrey',
                'normal' : '#f1e2cc',
                'poison' : '#620042',
                'psychic' : '#aa4499',
                'rock' : 'grey',
                'steel' : '#666666',
                'water' : 'teal'}

    fig = px.treemap(pokemon, path=[px.Constant("all"), 'type1', 'type2'], values='count',
                    title="Proporção de tipos (primário e secundário)",
                    color_discrete_map=colors_dict)

    return fig

def type_combination_correlation(pokemon):
    df = pokemon[~pokemon['type2'].isnull()][['type1', 'type2']]
    pokemon_types = df['type1'].unique()

    data = []
    for type1 in pokemon_types:
        arr = []
        for type2 in pokemon_types:
            arr.append(np.asarray([(df['type1'] == type1) & (df['type2'] == type2)]).sum())
        data.append(arr)

    fig = px.imshow(data, x=pokemon_types, y=pokemon_types,
                    labels=dict(x="Tipo secundário", y="Tipo primário", color="Quantidade"),
                    title='Correlação da combinação de tipos',
                    width=700, height=800
                )
    fig.update_xaxes(side="top")

    return fig

def type_proportion_evolution_cumulative(pokemon):
    types = np.unique(pokemon['type1'].values)
    gens = np.unique(pokemon['generation'].values)

    plot = go.Figure()

    for t in types:
        filteredbytype = pokemon.loc[pokemon['type1'] == t]
        numpergen = []
        for gen in gens:
            numpergen.append(len(filteredbytype.loc[filteredbytype['generation'] == gen]))
        plot.add_trace(go.Scatter(
            name = t,
            x = gens,
            y = np.cumsum(numpergen),
            stackgroup='one'
            ))
    
    plot.update_layout(
        title="Evolução da proporção de tipos acumulado",
        xaxis_title="Geração",
        yaxis_title="Número de pokémon",
        legend_title="Tipo de pokémon"
    )

    return plot

def type_proportion_evolution_absolute(pokemon):
    types = np.unique(pokemon['type1'].values)
    gens = np.unique(pokemon['generation'].values)

    plot = go.Figure()

    for t in types:
        filteredbytype = pokemon.loc[pokemon['type1'] == t]
        numpergen = []
        for gen in gens:
            numpergen.append(len(filteredbytype.loc[filteredbytype['generation'] == gen]))
        plot.add_trace(go.Scatter(
            name = t,
            x = gens,
            y = numpergen,
            stackgroup='one'
            ))
    
    plot.update_layout(
        title="Evolução da proporção de tipos por geração",
        xaxis_title="Geração",
        yaxis_title="Número de pokémon",
        legend_title="Tipo de pokémon"
    )

    return plot

def quality_histogram(pokemon):
    normal_pokemon = pokemon[pokemon['is_legendary'] == 0]
    legendary_pokemon = pokemon[pokemon['is_legendary'] == 1]

    x0 = normal_pokemon['how_good']
    x1 = legendary_pokemon['how_good']

    df = pd.DataFrame(dict(
        series=np.concatenate((["Regular"]*len(x0), ["Legendary"]*len(x1))), 
        data  =np.concatenate((x0,x1))
    ))

    fig = px.histogram(df, x="data", color="series", barmode="overlay",
                labels={"data": "Qualidade do pokémon",
                        "series": "Lendário?"},
                    title="Distribuição da qualidade dos pokémon")

    return fig

def general_type_chart(pokemon):
    coverage = pokemon[pokemon.type2=='none'][
        ['type1'] + [
                        col 
                        for col in pokemon.columns 
                        if 'against' in col
                    ]
    ].drop_duplicates().rename(columns={'type1':'type'})

    coverage = coverage.set_index('type').rename(columns={ c : c.split('_')[-1] for c in coverage.columns}).sort_index()

    fig = px.imshow(coverage, x=coverage.columns, y=coverage.columns,color_continuous_scale='RdBu_r',
                    labels=dict(x="Atacante", y="Defensor", color="Multiplicador"),
                    title='Typechart', text_auto=True,
                    width=700, height=800,
                )
    fig.update_traces(dict(showscale=False, 
                        coloraxis=None, 
                        colorscale='RdBu_r'), selector={'type':'heatmap'})

    fig.update_xaxes(side="top")
    return fig

def team_type_chart(pokemon, team):
    coverage_team = pokemon[pokemon.name.isin(team)][
        ['name'] + [
                        col 
                        for col in pokemon.columns 
                        if 'against' in col
                    ]
    ].drop_duplicates().rename(columns={'type1':'type'})

    coverage_team = coverage_team.set_index('name').rename(columns={ c : c.split('_')[-1] for c in coverage_team.columns}).sort_index()

    fig = px.imshow(coverage_team, x=coverage_team.columns, y=coverage_team.index,color_continuous_scale='RdBu_r',
                    labels=dict(x="Atacante", y="Defensor", color="Multiplicador"),
                    title='Typechart', text_auto=True,
                    width=800, height=400,
                )
    fig.update_traces(dict(showscale=False, 
                        coloraxis=None, 
                        colorscale='RdBu_r'), selector={'type':'heatmap'})

    fig.update_xaxes(side="top")
    return fig

def small_mulitples_all_atributtes(pokemon):
    fig = px.scatter_matrix(pokemon,
        dimensions=['speed','attack','sp_attack','defense','sp_defense','hp'],
        height=1000,
        width=1000
    )
    fig.update_traces(diagonal_visible=False)

    return fig

def radar_plot_teams_defense(pokemon, team1, team2):
    against_columns = [c for c in pokemon.columns if 'against' in c]

    df1 = pokemon[pokemon.name.isin(team1)][against_columns+['name']].set_index('name')
    df1 = df1.melt().groupby('variable', as_index=False).mean()

    df2 = pokemon[pokemon.name.isin(team2)][against_columns+['name']].set_index('name')
    df2 = df2.melt().groupby('variable', as_index=False).mean()

    df1['team'] = 1
    df2['team'] = 2

    dfzao = pd.concat([df1,df2])

    fig = px.line_polar(dfzao, r='value', theta='variable', color='team', line_close=True)
    return fig