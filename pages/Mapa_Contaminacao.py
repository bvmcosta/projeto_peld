#Importando as bibliotecas
import plotly.express as px
import pandas as pd
import json
import numpy as np
import streamlit as st
#-------------------------------------------------------------------------------------------------
st.set_page_config(page_title = 'Mapa de Contaminação', layout = 'wide')
#-------------------------------------------------------------------------------------------------
#DEFININDO AS FUNÇÕES
def load_data(path):

    df = pd.read_csv(path, encoding = 'latin-1')
    
    df['concentracao'] = df['concentracao'].apply(lambda x: 0.0 if x == 'nd' 
                                                            else 0.03 if x == '<0.06' 
                                                            else x)
    
    df['concentracao'] = df['concentracao'].astype(np.float64)
    
    
    return df
#-------------------------------------------------------------------------------------------------
def load_geojson(geojson_file):

    with open(geojson_file, 'r', encoding = 'latin-1') as f:

        file = json.load(f)
    
    return file
#-------------------------------------------------------------------------------------------------
def create_map(dataframe, geojson_file):

    fig = px.scatter_mapbox(dataframe, lat = dataframe['latitude'].unique(), 
                            lon = dataframe['longitude'].unique(),
                            size= dataframe['concentracao'],
                            color_discrete_sequence=["fuchsia"],
                            hover_name = dataframe['ponto'],
                            hover_data = {"concentracao": False, "latitude": False, "longitude": False},
                            zoom=9.5, 
                            height=400,
                            width = 600)
    
    fig.update_layout(mapbox_style="open-street-map")
    
    fig.update_layout(mapbox_layers = [{"source": geojson_file, "color": "black", "type": "line", "visible": True}])
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show(config={'scrollZoom': True})

    return fig
#-------------------------------------------------------------------------------------------------
path = './datasets/contaminantes.csv'
geojson_path = './geojson/guadalupe.geojson'

df = load_data(path)
guadalupe = load_geojson(geojson_path)
#-------------------------------------------------------------------------------------------------
#CONFIGURANDO A BARRA LATERAL
with st.sidebar:

    st.markdown("<h4 style='text-align: left; color: black;'>Escolha o Ecossistema</h4>", unsafe_allow_html=True)
    eco = st.multiselect(label = '(Escolha até dois)',
                         options = ['Baía e Recifes de Corais',
                                    'Praia',
                                    'Estuário e Manguezal',
                                    'Rio',
                                    'Prado de Fanerógamas',
                                    'Mapa base'
                                    ],
                         default = ['Mapa base'],
                         max_selections = 2)
    #-------------------------------------------------------------------------------------------------
    st.markdown("<h4 style='text-align: left; color: black;'>Escolha a matriz ambiental</h4>", unsafe_allow_html=True)
    matriz = st.multiselect(label = '(Escolha apenas uma)',
                         options = ['Água',
                                    'Sedimento',
                                    'Organismos',
                                    'Matriz'
                                    ],
                         default = ['Matriz'],
                         max_selections = 1)
    #-------------------------------------------------------------------------------------------------
    st.markdown("<h4 style='text-align: left; color: black;'>Escolha a campanha de amostragem</h4>", unsafe_allow_html=True)
    campanha = st.multiselect(label = '(Escolha apenas uma)',
                         options = ['Agosto/2022',
                                    'Fevereiro/2023',
                                    'Janeiro/2024',
                                    'Mês/Ano'
                                    ],
                         default = ['Mês/Ano'],
                         max_selections = 2)
    #-------------------------------------------------------------------------------------------------
    st.markdown("<h4 style='text-align: left; color: black;'>Escolha o grupo de contaminantes</h4>", unsafe_allow_html=True)
    grupo = st.multiselect(label = '(Escolha apenas um)',
                         options = ['Hidrocarbonetos Alifáticos',
                                    'HPAs',
                                    'LABs',
                                    'LAS',
                                    'Biocidas',
                                    'Organoclorados',
                                    'Metais',
                                    'Contaminantes'
                                    ],
                         default = ['Contaminantes'],
                         max_selections = 1)
    #-------------------------------------------------------------------------------------------------
    #Filtrando linhas no dataframe original
    df1 = df.loc[(df['ambiente'] == eco[0])&
                 (df['matriz'] == matriz[0])&
                 (df['campanha'] == campanha[0])&
                 (df['grupo'] == grupo[0]), :]
    #-------------------------------------------------------------------------------------------------
    st.markdown("<h4 style='text-align: left; color: black;'>Escolha o analito</h4>", unsafe_allow_html=True)
    grupo = st.multiselect(label = '(Escolha apenas um)',
                         options = df1['analito'].unique(),
                         default = ['Contaminantes'],
                         max_selections = 1)
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#st.markdown("<h5 style='text-align: justify; color: black;'><strong>Observação:</strong> A visualiação das estações e fontes de poluição ocorre apenas após seleção dos parâmetros 'Ecossistema' e 'Fonte de poluição'</h5>", unsafe_allow_html=True)

#-------------------------------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: black;'>Mapa de Contaminação nos ecossistemas da APA de Guadalupe</h1>", unsafe_allow_html=True)

st.dataframe(df1)
st.plotly_chart(create_map(df1, guadalupe))
