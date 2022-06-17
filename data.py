import pandas as pd

def read_data():
    # Dados de https://www.kaggle.com/datasets/rounakbanik/pokemon?resource=download
    pokemon = pd.read_csv('pokemon.csv')
    return pokemon

def process_data(pokemon):
    # O atributo capture_rate desse único pokémon tem um valor destoante dos demais, assim ele será removido
    pokemon.drop(labels=773, axis=0, inplace=True)
    pokemon.reset_index(inplace=True)

    # Atributo capture_rate estava no formato de string, foi convertido para int
    pokemon['capture_rate'] = pokemon['capture_rate'].astype(int)

    # Para os pokémon que não têm tipo secundário, esse campo estava preenchido com NaN, trocamos para string 'none'
    pokemon.loc[pokemon['type2'].isna(), ['type2']] = 'none'

    # Cálculo da "qualidade" do pokémon
    pokemon['how_good'] = pokemon['attack'] + pokemon['defense'] + pokemon['hp'] + pokemon['sp_attack'] + pokemon['sp_defense'] + pokemon['speed']

    # Utilizado no treemap para contar os pokémon
    pokemon['count'] = 1

    return pokemon

def read_process_data():
    pokemon = read_data()
    return process_data(pokemon)