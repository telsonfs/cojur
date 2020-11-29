from os import listdir
import pandas as pd
import json
import re


def open_complete_json():
    path ='Lexml/acervo_2010_2020/acervo_2010_2020.json'

    with open(path, 'r') as data_file:
        data = json.load(data_file)

    print(data.keys())

    # df = pd.read_json(path)

    # df.to_csv('complete.csv', sep='\t')

def features_select():
    path = 'data/federal/json/'
    arqs = listdir(path)


    columns_delete = ['facet-tipoDocumento', 'urn', 'localidade', 'facet-localidade', 'autoridade', 'facet-autoridade', 'type']

    for arq in arqs:
        entities = []
        df = pd.read_json(f'{path}{arq}')
        df.drop(columns= columns_delete, axis= 1, inplace= True)
        titles = df['title']
        for title in titles:
            if isinstance(title, list):
                entities.append(title[0].split(',')[0])
            else: 
                if ',' in title:
                    entities.append(title.split(',')[0])
                else:
                    entities.append(title[:len(title) - 14])

        df['entity_legal'] = entities
        save_name = arq.split('.')[0]
        df.to_csv(f'data/{save_name}.csv', sep='\t')

def mesclar():
    path = 'data/leis_csv/'
    arqs = listdir(path)

    arr_df = [] 

    for arq in arqs:
        arr_df.append(pd.read_csv(f'{path}{arq}', sep = '\t'))
    df = pd.concat(arr_df)
    df.to_csv('data/legislacao.csv', sep='\t')

def search_relation_entity():
    df = pd.read_csv('data/legislacao.csv', sep = '\t')
    tipo_documento = df.tipoDocumento.value_counts()

    print(f'tipos de leis: {tipo_documento}')