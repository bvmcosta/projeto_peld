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
                            size= dataframe['concentracao_padronizada'],
                            color_discrete_sequence=["fuchsia"],
                            hover_name = dataframe['ponto'],
                            hover_data = {"concentracao_padronizada": True, "latitude": False, "longitude": False},
                            zoom=9.5, 
                            height=400,
                            width = 600)
    
    fig.update_layout(mapbox_style="open-street-map")
    
    fig.update_layout(mapbox_layers = [{"source": geojson_file, "color": "black", "type": "line", "visible": True}])
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show(config={'scrollZoom': True})

    return 
#-------------------------------------------------------------------------------------------------
path = './datasets/contaminantes_padronizados.csv'
geojson_path = './geojson/guadalupe.geojson'

df = load_data(path)
guadalupe = load_geojson(geojson_path)
#-------------------------------------------------------------------------------------------------
#CONFIGURANDO A BARRA LATERAL
with st.sidebar:

    st.markdown("<h4 style='text-align: left; color: black;'>Escolha o Ecossistema</h4>", unsafe_allow_html=True)
    eco = st.multiselect(label = '(Escolha até dois)',
                         options = list(df['ambiente'].unique()),
                         default = ['Mapa base'],
                         max_selections = 2)
    #-------------------------------------------------------------------------------------------------
    st.markdown("<h4 style='text-align: left; color: black;'>Escolha a matriz ambiental</h4>", unsafe_allow_html=True)
    matriz = st.multiselect(label = '(Escolha apenas uma)',
                            options = list(df['matriz'].unique()),
                            default = ['Matriz'],
                            max_selections = 1)
    #-------------------------------------------------------------------------------------------------
    st.markdown("<h4 style='text-align: left; color: black;'>Escolha a campanha de amostragem</h4>", unsafe_allow_html=True)
    campanha = st.multiselect(label = '(Escolha apenas uma)',
                              options = list(df['campanha'].unique()),
                              default = ['Mês/Ano'],
                              max_selections = 2)
    #-------------------------------------------------------------------------------------------------
    st.markdown("<h4 style='text-align: left; color: black;'>Escolha o grupo de contaminantes</h4>", unsafe_allow_html=True)
    grupo = st.multiselect(label = '(Escolha apenas um)',
                           options = list(df['grupo'].unique()),
                           default = ['Contaminantes'],
                           max_selections = 1)
    #-------------------------------------------------------------------------------------------------
    #Filtrando linhas no dataframe original
    df1 = df.loc[((df['ambiente'] == eco[0])|(df['ambiente'] == eco[1]))&
                 (df['matriz'] == matriz[0])&
                 (df['campanha'] == campanha[0])&
                 (df['grupo'] == grupo[0]), :]
    #-------------------------------------------------------------------------------------------------
    st.markdown("<h4 style='text-align: left; color: black;'>Escolha o analito</h4>", unsafe_allow_html=True)
    analito = st.multiselect(label = '(Escolha apenas um)',
                           options = list(df1['analito'].unique()),
                           max_selections = 1)
    st.markdown("<h5 style='text-align: justify; color: black;'><strong>Observação:</strong> A visualiação do mapa de contaminação e dataframe ocorre após seleção dos parâmetros acima solicitados.</h5>", unsafe_allow_html=True)
    #-------------------------------------------------------------------------------------------------
    df2 = df1.loc[df1['analito'] == analito[0], :]
#-------------------------------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: black;'>Mapa de Contaminação nos ecossistemas da APA de Guadalupe</h1>", unsafe_allow_html=True)

st.dataframe(df2)

#st.plotly_chart(create_map(df1, guadalupe))
