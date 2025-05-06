#Importando as bibliotecas
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
@st.cache_data
def load_data(path):

    df = pd.read_csv(path, encoding = 'latin-1')

    return df
#-------------------------------------------------------------------------------------------------
@st.cache_data
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
def create_mapa_base(apa, ecossistemas):

    mapa = folium.Map(location = [-8.718397, -35.035753],
                    tiles = 'OpenStreetMap',
                    zoom_start = 9.5,
                    width = 800, 
                    height = 200)
    
    folium.GeoJson(apa[0],
                          style_function = lambda feature: {
                          "fillColor": "white",
                          "color": "purple",
                          "weight": 2},
                           zoom_on_click = True).add_to(mapa)
    
    for ecossistema in ecossistemas:
            
        folium.GeoJson(ecossistema,
                          style_function = lambda feature: {
                          "fillColor": "gray",
                          "color": "black",
                          "weight": 0.5},
                          zoom_on_click = True).add_to(mapa)

    return mapa
#-------------------------------------------------------------------------------------------------
def create_mapa_ecossistemas(lista2, lista1, df):

    mapa = folium.Map(location = [-8.718397, -35.035753],
                    tiles = 'OpenStreetMap',
                    zoom_start = 11,
                    width = 800, 
                    height = 200)

    marker_cluster = MarkerCluster().add_to(mapa)

    folium.GeoJson(lista2[0],
                          style_function = lambda feature: {
                          "fillColor": "white",
                          "color": "purple",
                          "weight": 2},
                           zoom_on_click = True).add_to(mapa)

    for ecossistema in lista1:
           
        folium.GeoJson(ecossistema,
                          style_function = lambda feature: {
                          "fillColor": "gray",
                          "color": "black",
                          "weight": 0.5},
                          zoom_on_click = True).add_to(mapa)

    for row, value in df.iterrows():
        
        folium.Marker(location = (df.loc[row, 'latitude'], 
                                  df.loc[row, 'longitude']), 
                      popup = df.loc[row, 'descricao'],
                      icon = folium.Icon(color = df.loc[row, 'color'])
                     ).add_to(marker_cluster)
           
    return mapa
#-------------------------------------------------------------------------------------------------
def insert_stations(mapa, df):

    for row, value in df.iterrows():
        
        folium.Marker(location = (df.loc[row, 'latitude'], 
                                  df.loc[row, 'longitude']), 
                      popup = df.loc[row, 'descricao'],
                      icon = folium.Icon(color = df.loc[row, 'color'])
                     ).add_to(mapa)
           
    return mapa
#-------------------------------------------------------------------------------------------------
estacoes = './datasets/estacoes_amostragem.csv'
fontes = './datasets/fontes_poluicao.csv'

eco = ['./geojson/recifes.geojson',
       './geojson/rio_mamucabas.geojson',
       './geojson/estuario_rio_formoso.geojson',
       './geojson/riacho_jacare.geojson',
       './geojson/brejo.geojson'
       ]

apa = ['./geojson/guadalupe.geojson']

lista_ecossistemas = load_geojson(eco, apa)[0]
lista_apa = load_geojson(eco, apa)[1]
df1 = load_data(estacoes)
df2 = load_data(fontes)
#-------------------------------------------------------------------------------------------------
#CONFIGURANDO A BARRA LATERAL

with st.sidebar:

    st.markdown("<h4 style='text-align: left; color: black;'>Escolha o Ecossistema</h4>", unsafe_allow_html=True)
    eco = st.multiselect(label = '(Escolha apenas um)',
                         options = ['Baía e Recifes de Corais',
                                    'Praia',
                                    'Estuário e Manguezal',
                                    'Rio',
                                    'Prado de Fanerógamas',
                                    'Mapa base'
                                    ],
                         default = ['Mapa base'],
                         max_selections = 1)

    st.markdown("<h4 style='text-align: left; color: black;'>Escolha a fonte de poluição</h4>", unsafe_allow_html=True)
    fonte = st.multiselect(label = '(Escolha apenas uma)',
                         options = ['Estação de Tratamento de Esgoto',
                                    'Ponto de Lançamento',
                                    'Aquicultura',
                                    'Porto',
                                    'Assentamento rural',
                                    'Área desmatada',
                                    'Área urbana',
                                    'Marina',
                                    'Mapa base'
                                    ],
                         default = ['Mapa base'],
                         max_selections = 1)

    st.markdown("<h5 style='text-align: justify; color: black;'><strong>Observação:</strong> A visualiação das estações e fontes de poluição ocorre apenas após seleção dos parâmetros 'Ecossistema' e 'Fonte de poluição'</h5>", unsafe_allow_html=True)
#-------------------------------------------------------------------------------------------------
if (eco[0] == 'Mapa base')&(fonte[0] == 'Mapa base'):
    
    mapa1 = create_mapa_base(lista_apa, lista_ecossistemas)

elif (eco[0] != 'Mapa base')&(fonte[0] == 'Mapa base'):

    df1 = df1.loc[(df1['ambiente'] == eco[0]), :]
    mapa2 = create_mapa_ecossistemas(lista_apa, lista_ecossistemas, df1)

else:

    df1 = df1.loc[(df1['ambiente'] == eco[0]), :]
    df2 = df2.loc[(df2['fonte'] == fonte[0]), :]
    mapa2 = create_mapa_ecossistemas(lista_apa, lista_ecossistemas, df1)
    mapa3 = insert_stations(mapa2, df2)
#-------------------------------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: black;'>Ecossistemas no sítio PELD TAMS</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Localização das estações de amostragem e fontes de contaminação</h2>", unsafe_allow_html=True)

with st.container(border = True):

    st.markdown("<h4 style='text-align: left; color: black;'>Apresentação</h4>", unsafe_allow_html=True)
    st.markdown("""<p style='text-align: justify'> Entre 2020 e 2025, os impactos antrópicos sobre ecossistemas marinhos, estuarinos e dulcícolas foram avaliados em ambientes
    localizados na Área de Proteção Ambiental de Guadalupe.</p>
                """, 
    unsafe_allow_html=True)

with st.container():

    st.markdown("<h5 style='text-align: center; color: black;'>Figura 3</h5>", unsafe_allow_html=True)
    
    if (eco[0] == 'Mapa base')&(fonte[0] == 'Mapa base'):
        
        st_folium(mapa1, use_container_width = True)
    
    elif (eco[0] != 'Mapa base')&(fonte[0] == 'Mapa base'):
        
        st_folium(mapa2, use_container_width = True)
    
    else:

        st_folium(mapa3, use_container_width = True)

with st.container():
    
    st.markdown("<h5 style='text-align: center; color: black;'>Tabela de identificação das estações de amostragem</h5>", unsafe_allow_html=True)
    st.dataframe(df1)

    st.markdown("<h5 style='text-align: center; color: black;'>Tabela de identificação das fontes de contaminação</h5>", unsafe_allow_html=True)
    st.dataframe(df2)



    





