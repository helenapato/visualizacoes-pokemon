import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def ability_radar(pokemon, poke_list):
    if poke_list == []:
        return ability_radar(pokemon, ['Arceus'])

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