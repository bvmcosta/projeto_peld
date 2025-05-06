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
@st.cache_data
def load_data(path):

    df = pd.read_csv(path, encoding = 'latin-1')
    
    return df
#-------------------------------------------------------------------------------------------------
@st.cache_data
def load_geojson(geojson_file):

    with open(geojson_file, 'r', encoding = 'latin-1') as f:

        file = json.load(f)
    
    return file
#-------------------------------------------------------------------------------------------------
def create_basemap(dataframe, geojson_file):

    fig = px.scatter_mapbox(dataframe,
                         lat = dataframe['latitude'],
                         lon = dataframe['longitude'],
                         mapbox_style = 'open-street-map', 
                         color_discrete_sequence=["white"], opacity = 0,
                         zoom=9.5, 
                         height = 500, 
                         width = 600)

    fig.update_layout(mapbox_layers = [{"source": geojson_file, "color": "black", "type": "line", "visible": True}])

    return fig
#-------------------------------------------------------------------------------------------------
def create_map(dataframe, geojson_file):

    fig = px.scatter_mapbox(dataframe,
                            mapbox_style = "open-street-map",
                            lat = dataframe['latitude'].unique(), 
                            lon = dataframe['longitude'].unique(),
                            size = dataframe['concentracao_padronizada'],
                            color_discrete_sequence = ["fuchsia"],
                            hover_name = dataframe['ponto'],
                            hover_data = {"concentracao_padronizada": True, "latitude": False, "longitude": False},
                            zoom=9.5, 
                            height=500,
                            width = 600)
    
    fig.update_layout(mapbox_layers = [{"source": geojson_file, "color": "black", "type": "line", "visible": True}])
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig
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
                              max_selections = 1)
    #-------------------------------------------------------------------------------------------------
    st.markdown("<h4 style='text-align: left; color: black;'>Escolha o grupo de contaminantes</h4>", unsafe_allow_html=True)
    grupo = st.multiselect(label = '(Escolha apenas um)',
                           options = list(df['grupo'].unique()),
                           default = ['Contaminantes'],
                           max_selections = 1)
    
    st.markdown("""<h5 style='text-align: justify; color: black;'><strong>Observação:</strong> 
                    A visualiação do mapa de contaminação e dataframe ocorre após seleção dos parâmetros acima solicitados.
                   </h5>
                """, 
                unsafe_allow_html=True)
#-------------------------------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: black;'>Mapa de Contaminação nos ecossistemas da APA de Guadalupe</h1>", unsafe_allow_html=True)

with st.container(border = True):

    st.markdown("<h4 style='text-align: left; color: black;'>Apresentação</h4>", unsafe_allow_html=True)
    st.markdown("""<p style='text-align: justify'> Entre agosto de 2022 e janeiro de 2024, a concentração de contaminantes orgânicos e/ou inorgânicos foi quantificada em diferentes matrizes ambientais (água, sedimento e organismos) para avaliar os impactos antrópicos na Área de Proteção Ambiental de Guadalupe.                      </p> Os seguintes grupos de poluentes orgânicos foram monitorados em amostras de sedimento:
    <ul>
    <li>Hidrocarbonetos Policíclicos Aromáticos (HPAs) - 33 analitos, incluindo os 16 HPAs prioritários da EPA (hpa_16) e os HPAs alquilados (hpa_33)</li>
    <li>Dicloro-Difenil-Tricloroetano (DDTs) e seus metabólitos (DDDs e DDEs)</li>
    <li>Bifenilas Policloradas (PCBs) com 1 a 10 átomos de cloro</li>
    <li>Alquilbenzeno lineares (LABs)</li>
    <li>Biocidas (DCOIT, Irgarol, Diclofluonida e Clorotalonil)</li> 
    </ul>
    
                """, 
    unsafe_allow_html=True)
#-------------------------------------------------------------------------------------------------
#Filtrando linhas no dataframe original
if len(eco) == 0:

    df1 = df.loc[df['ambiente'] == 'Mapa base', :]

elif len(eco) == 1:
    
    if eco[0] == 'Mapa base': 
        
        df1 = df.loc[df['ambiente'] == eco[0], :]

    else:
            
        df1 = df.loc[(df['ambiente'] == eco[0])&\
                     (df['matriz'] == matriz[0])&\
                     (df['campanha'] == campanha[0])&\
                     (df['grupo'] == grupo[0]), :]

else:

    df1 = df.loc[((df['ambiente'] == eco[0])|(df['ambiente'] == eco[1]))&\
                  (df['matriz'] == matriz[0])&\
                  (df['campanha'] == campanha[0])&\
                  (df['grupo'] == grupo[0]), :]
#-------------------------------------------------------------------------------------------------
with st.sidebar:       
    
        st.markdown("<h4 style='text-align: left; color: black;'>Escolha o analito</h4>", unsafe_allow_html=True)
        analito = st.multiselect(label = '(Escolha apenas um)',
                                 options = list(df1['analito'].unique()),
                                 default = list(df1['analito'].unique())[0],
                                 max_selections = 1)
        df2 = df1.loc[df1['analito'] == analito[0], :]
#-------------------------------------------------------------------------------------------------
if len(eco) == 0:

    map1 = create_basemap(df1, guadalupe)
    
    col1, col2 = st.columns([0.5, 0.5], border = True)

    with col1:
    
        st.markdown("<h5 style='text-align: center; color: black;'>Figura 4</h5>", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
                    (Mapa base da Área de Proteção Ambiental de Guadalupe)</h6>
                    """, unsafe_allow_html=True)
        
        st.plotly_chart(map1, config = {"scrollZoom": True}, use_container_width = True)
    
    with col2:
        
        st.markdown("<h5 style='text-align: center; color: black;'>Dataframe</h5>", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
                    (Atributos descritivos pontos de amostragem e dos contaminantes analisados.)</h6>
                    """, unsafe_allow_html=True)
        st.dataframe(df)
    
elif (len(eco) == 1)&(eco[0] == 'Mapa base'):

    map2 = create_basemap(df1, guadalupe)
    
    col1, col2 = st.columns([0.5, 0.5], border = True)

    with col1:
    
        st.markdown("<h5 style='text-align: center; color: black;'>Figura 4</h5>", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
                    (Mapa base da Área de Proteção Ambiental de Guadalupe)</h6>
                    """, unsafe_allow_html=True)
        
        st.plotly_chart(map2, config = {"scrollZoom": True}, use_container_width = True)
    
    with col2:
        
        st.markdown("<h5 style='text-align: center; color: black;'>Dataframe</h5>", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
                    (Atributos descritivos pontos de amostragem e dos contaminantes analisados.)</h6>
                    """, unsafe_allow_html=True)
        st.dataframe(df)

elif (len(eco) == 1)&(eco[0] != 'Mapa base'):

    map3 = create_map(df2, guadalupe)

    col1, col2 = st.columns([0.5, 0.5], border = True)

    with col1:
    
        st.markdown("<h5 style='text-align: center; color: black;'>Figura 4</h5>", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
                    (Pontos de amostragem na área de estudo representados por círculos com tamanhos proporcionais às concentrações)</h6>
                    """, unsafe_allow_html=True)
        
        st.plotly_chart(map3, config = {"scrollZoom": True}, use_container_width = True)
    
    with col2:
        
        st.markdown("<h5 style='text-align: center; color: black;'>Dataframe</h5>", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
                    (Atributos descritivos pontos de amostragem e dos contaminantes analisados.)</h6>
                    """, unsafe_allow_html=True)
        st.dataframe(df2)

else:

    map4 = create_map(df2, guadalupe)

    col1, col2 = st.columns([0.5, 0.5], border = True)

    with col1:
    
        st.markdown("<h5 style='text-align: center; color: black;'>Figura 4</h5>", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
                    (Pontos de amostragem na área de estudo representados por círculos com tamanhos proporcionais às concentrações)</h6>
                    """, unsafe_allow_html=True)
        
        st.plotly_chart(map4, config = {"scrollZoom": True}, use_container_width = True)
    
    with col2:
        
        st.markdown("<h5 style='text-align: center; color: black;'>Dataframe</h5>", unsafe_allow_html=True)
        st.markdown("""<h6 style='text-align: justify; color: black;'>
                    (Atributos descritivos pontos de amostragem e dos contaminantes analisados.)</h6>
                    """, unsafe_allow_html=True)
        st.dataframe(df2)
#-------------------------------------------------------------------------------------------------

