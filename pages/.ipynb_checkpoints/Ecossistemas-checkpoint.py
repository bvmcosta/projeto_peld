#Importando as bibliotecas
import numpy as np
import json
import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
#-------------------------------------------------------------------------------------------------
st.set_page_config(page_title = 'Ecossistemas', layout = 'wide')
#-------------------------------------------------------------------------------------------------
#DEFININDO AS FUNÇÕES
def load_data(path):

    df = pd.read_csv(path, encoding = 'latin-1')

    return df
#-------------------------------------------------------------------------------------------------
def load_geojson(geojson_files, apa):

    lista_ecossistemas = []

    lista_apa = []

    for file in geojson_files:

        with open(file, 'r') as f:

            file = json.load(f)
            lista_ecossistemas.append(file)

    for file in apa:

        with open(file, 'r', encoding = 'utf-8') as f:

            file = json.load(f)
            lista_apa.append(file)

    for ecossistema in lista_ecossistemas:

        if ecossistema['name'] == 'recifes':
    
            ecossistema['name'] = 'Recifes de Corais'

        elif ecossistema['name'] == 'rio_mamucabas':
    
            ecossistema['name'] = 'Sistema Estuarino dos Rios Mamucabas e Ilhetas'

        elif ecossistema['name'] == 'riacho_jacare':
    
            ecossistema['name'] = 'Riacho Jacaré'

        elif ecossistema['name'] == 'brejo':
    
            ecossistema['name'] = 'Rio Mamucabas'
    
        else: 

            ecossistema['name'] = 'Sistema Estuarino de Rio Formoso'

    return lista_ecossistemas, lista_apa
#-------------------------------------------------------------------------------------------------
def create_mapa_ecossistemas(lista1, lista2):

    mapa = folium.Map(location = [-8.718397, -35.035753],
                    tiles = 'OpenStreetMap',
                    zoom_start = 11,
                    width = 800, 
                    height = 200)

    folium.GeoJson(lista2[0],
                          style_function = lambda feature: {
                          "fillColor": "white",
                          "color": "purple",
                          "weight": 2},
                           zoom_on_click = True).add_to(mapa)

    for ecossistema in lista1:

        if ecossistema['name'] == 'Recifes de Corais':
            
            folium.GeoJson(ecossistema,
                          style_function = lambda feature: {
                          "fillColor": "gray",
                          "color": "black",
                          "weight": 0.5},
                          zoom_on_click = True).add_to(mapa)

        elif ecossistema['name'] == 'Riacho Jacaré':
            
            folium.GeoJson(ecossistema,
                          style_function = lambda feature: {
                          "fillColor": "gray",
                          "color": "black",
                          "weight": 0.5},
                          zoom_on_click = True).add_to(mapa)
        else:

            folium.GeoJson(ecossistema,
                          style_function = lambda feature: {
                          "fillColor": "gray",
                          "color": "black",
                          "weight": 0.5},
                          zoom_on_click = True).add_to(mapa)
           
    return mapa
#-------------------------------------------------------------------------------------------------
def insert_stations(mapa, df):

    marker_cluster = MarkerCluster().add_to(mapa)

    for row, value in df.iterrows():
        
        folium.Marker(location = (df.loc[row, 'latitude'], 
                                  df.loc[row, 'longitude']), 
                      popup = df.loc[row, 'descricao'],
                      icon = folium.Icon(color = df.loc[row, 'color'])
                     ).add_to(marker_cluster)

    return mapa
#-------------------------------------------------------------------------------------------------
path = './datasets/coordenadas_estacoes.csv'
eco = ['./geojson/recifes.geojson',
       './geojson/rio_mamucabas.geojson',
       './geojson/estuario_rio_formoso.geojson',
       './geojson/riacho_jacare.geojson',
       './geojson/brejo.geojson'
       ]

apa = ['./geojson/guadalupe.geojson']

lista_ecossistemas = load_geojson(eco, apa)[0]
lista_apa = load_geojson(eco, apa)[1]
df = load_data(path)
#-------------------------------------------------------------------------------------------------
#CONFIGURANDO A BARRA LATERAL

with st.sidebar:

    st.markdown("<h4 style='text-align: left; color: black;'>Escolha o Ecossistema</h4>", unsafe_allow_html=True)
    eco = st.multiselect(label = '',
                         options = ['Baía e Recifes de Corais',
                                    'Praia',
                                    'Estuário e Manguezal',
                                    'Rio'
                                    ],
                         default = ['Baía e Recifes de Corais'],
                         max_selections = 1)

    st.markdown("<h4 style='text-align: left; color: black;'>Escolha a fonte de poluição</h4>", unsafe_allow_html=True)
    fonte = st.multiselect(label = '',
                         options = ['Estação de Tratamento de Esgoto',
                                    'Marina',
                                    'Porto',
                                    'Cidade',
                                    'Assentamento Rural',
                                    'Zona de Reparo de Embarcações',
                                    'Aquicultura'
                                    ],
                         default = ['Estação de Tratamento de Esgoto'],
                         max_selections = 1)
#-------------------------------------------------------------------------------------------------
mapa = create_mapa_ecossistemas(lista_ecossistemas, lista_apa)

if eco[0] == np.nan:

    mapa = create_mapa_ecossistemas(lista_ecossistemas, lista_apa)

else:
    
    df = df.loc[(df['ambiente'] == eco[0])|(df['ambiente'] == fonte[0]), :]
    mapa = insert_stations(mapa, df)
#-------------------------------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: black;'>Ecossistemas no sítio PELD TAMS</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Localização das estações de amostragem e fontes de contaminação</h2>", unsafe_allow_html=True)

with st.container(border = True):

    st.markdown("<h4 style='text-align: left; color: black;'>Apresentação</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify'> A Área de Proteção Ambiental de Guadalupe ....</p>", unsafe_allow_html=True)

with st.container():

    st.markdown("<h5 style='text-align: center; color: black;'>Figura 3</h5>", unsafe_allow_html=True)
    st_folium(mapa, use_container_width = True)
    st.dataframe(df)


    





