#Importando as bibliotecas
import json
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
#-------------------------------------------------------------------------------------------------
st.set_page_config(page_title = 'PELD TAMS', layout = 'wide')
#-------------------------------------------------------------------------------------------------
#DEFININDO AS FUNÇÕES
def load_geojson(municipios, ucs):

    lista_municipios = []

    lista_ucs = []

    for file in municipios:

        with open(file, 'r', encoding = 'utf-8') as f:

            file = json.load(f)
            lista_municipios.append(file)

    for file in ucs:

        with open(file, 'r', encoding = 'utf-8') as f:

            file = json.load(f)
            lista_ucs.append(file)

    for uc in lista_ucs:

        if uc['name'] == 'apacc':
    
            uc['name'] = 'APA Costa dos Corais'
    
        elif uc['name'] == 'guadalupe':
    
            uc['name'] = 'APA de Guadalupe'
        
        elif uc['name'] == 'pnmft':
    
            uc['name'] = 'Parque Nacional Marinho do Forte de Tamandaré'
        
        elif uc['name'] == 'saltinho':
    
            uc['name'] = 'Reserva Biológica de Saltinho'
    
        elif uc['name'] == 'apa_serrambi':
    
            uc['name'] = 'APA Recifes de Serrambi'
    
        elif uc['name'] == 'zpvmt':

            uc['name'] = 'Zona de Proteção da Vida Marinha de Tamandaré'

        else: 

            uc['name'] = 'APA de Sirinhaém'

    return lista_municipios, lista_ucs 
#-------------------------------------------------------------------------------------------------
def create_mapa_municipios(lista):

    mapa = folium.Map(location = [-8.691356, -35.138558],
                    tiles = 'OpenStreetMap',
                    zoom_start = 8.4,
                    width = 800, 
                    height = 200)

    folium.GeoJson(lista_municipios[0], style_function = lambda feature: {
        "fillColor": "#FFFFFF",
        "color": "black",
        "weight": 2
    }, zoom_on_click = True).add_to(mapa)

    recife = """
    <h2>Recife</h2><br>
    <p><strong>Área total:</strong><br> 219 km<sup>2<sup></p>
    <p><strong>Área urbana:</strong> 143 km<sup>2<sup></p>
    <p><strong>População residente:</strong> 1.488.920 pessoas</p>
    <p><strong>Referência:</strong><a href="https://cidades.ibge.gov.br/brasil/pe/recife/panorama"> IBGE Cidades</a></p> </p>  
    """
    folium.GeoJson(lista_municipios[1], style_function = lambda feature: {
            "fillColor": "gray",
            "color": "black",
            "weight": 2
        }, popup = folium.Popup(recife), parse_html=True, max_width = 100, zoom_on_click = True).add_to(mapa)

    sirinhaem = """
    <h2>Sirinhaém</h2><br>
    <p><strong>Área total:</strong><br> 374 km<sup>2<sup></p>
    <p><strong>Área urbana:</strong> 5 km<sup>2<sup></p>
    <p><strong>População residente:</strong> 37.596 pessoas</p>
    <p><strong>Referência:</strong><a href="https://cidades.ibge.gov.br/brasil/pe/sirinhaem/panorama"> IBGE Cidades</a></p> </p>  
    """
    
    folium.GeoJson(lista_municipios[2], style_function = lambda feature: {
            "fillColor": "blue",
            "color": "black",
            "weight": 2
        }, popup = folium.Popup(sirinhaem), parse_html=True, max_width = 100, zoom_on_click = True).add_to(mapa)

    tamandare = """
    <h2>Tamandaré</h2><br>
    <p><strong>Área total:</strong><br> 214 km<sup>2<sup></p>
    <p><strong>Área urbana:</strong> 7 km<sup>2<sup></p>
    <p><strong>População residente:</strong> 23.561 pessoas</p>
    <p><strong>Referência:</strong><a href="https://cidades.ibge.gov.br/brasil/pe/tamandare/panorama"> IBGE Cidades</a></p> </p>  
    """
    
    folium.GeoJson(lista_municipios[3], style_function = lambda feature: {
            "fillColor": "blue",
            "color": "black",
            "weight": 2
        }, popup = folium.Popup(tamandare), parse_html=True, max_width = 100, zoom_on_click = True).add_to(mapa)

    rio_formoso = """
    <h2>Rio Formoso</h2><br>
    <p><strong>Área total:</strong><br> 227 km<sup>2<sup></p>
    <p><strong>Área urbana:</strong> 3 km<sup>2<sup></p>
    <p><strong>População residente:</strong> 20.009 pessoas</p>
    <p><strong>Referência:</strong><a href="https://cidades.ibge.gov.br/brasil/pe/rio-formoso/panorama"> IBGE Cidades</a></p> </p>  
    """
    
    folium.GeoJson(lista_municipios[4], style_function = lambda feature: {
            "fillColor": "blue",
            "color": "black",
            "weight": 2}, popup = folium.Popup(rio_formoso), parse_html=True, max_width = 100, zoom_on_click = True).add_to(mapa)

    barreiros = """
    <h2>Barreiros</h2><br>
    <p><strong>Área total:</strong><br> 233 km<sup>2<sup></p>
    <p><strong>Área urbana:</strong> 6 km<sup>2<sup></p>
    <p><strong>População residente:</strong> 40.121 pessoas</p>
    <p><strong>Referência:</strong><a href="https://cidades.ibge.gov.br/brasil/pe/barreiros/panorama"> IBGE Cidades</a></p> </p>  
    """
    
    folium.GeoJson(lista_municipios[5], style_function = lambda feature: {
            "fillColor": "blue",
            "color": "black",
            "weight": 2
        }, popup = folium.Popup(barreiros), parse_html=True, max_width = 100, zoom_on_click = True).add_to(mapa)

    sao_jose = """
    <h2>São José da Coroa Grande</h2><br>
    <p><strong>Área total:</strong><br> 69 km<sup>2<sup></p>
    <p><strong>Área urbana:</strong> 4 km<sup>2<sup></p>
    <p><strong>População residente:</strong> 18.825 pessoas</p>
    <p><strong>Referência:</strong><a href="https://cidades.ibge.gov.br/brasil/pe/sao-jose-da-coroa-grande/panorama"> IBGE Cidades</a></p> </p>  
    """
    
    folium.GeoJson(lista_municipios[6], style_function = lambda feature: {
            "fillColor": "blue",
            "color": "black",
            "weight": 2}, popup = folium.Popup(sao_jose), parse_html=True, max_width = 100, zoom_on_click = True).add_to(mapa)
    
    return mapa
#-------------------------------------------------------------------------------------------------
def create_mapa_ucs(lista):

    mapa = folium.Map(location = [-8.718397, -35.035753],
                    tiles = 'OpenStreetMap',
                    zoom_start = 9.5,
                    width = 800, 
                    height = 200)

    for uc in lista:

        if uc['name'] == 'APA Costa dos Corais':
            
            folium.GeoJson(uc,
                          style_function = lambda feature: {
                          "fillColor": "white",
                          "color": "green",
                          "weight": 2},
                          zoom_on_click = True).add_to(mapa)
            
        elif uc['name'] == 'APA Recifes de Serrambi':
            
            folium.GeoJson(uc,
                          style_function = lambda feature: {
                          "fillColor": "white",
                          "color": "blue",
                          "weight": 2},
                          zoom_on_click = True).add_to(mapa)
            
        elif uc['name'] == 'APA de Guadalupe':

             folium.GeoJson(uc,
                          style_function = lambda feature: {
                          "fillColor": "white",
                          "color": "purple",
                          "weight": 2},
                           zoom_on_click = True).add_to(mapa)

        elif uc['name'] == 'APA de Sirinhaém':

             folium.GeoJson(uc,
                          style_function = lambda feature: {
                          "fillColor": "white",
                          "color": "brown",
                          "weight": 2},
                           zoom_on_click = True).add_to(mapa)

        elif uc['name'] == 'Parque Nacional Marinho do Forte de Tamandaré':

             folium.GeoJson(uc,
                          style_function = lambda feature: {
                          "fillColor": "white",
                          "color": "yellow",
                          "weight": 3},
                           zoom_on_click = True).add_to(mapa)

        elif uc['name'] == 'Reserva Biológica de Saltinho':

             folium.GeoJson(uc,
                          style_function = lambda feature: {
                          "fillColor": "white",
                          "color": "black",
                          "weight": 2},
                           zoom_on_click = True).add_to(mapa)

        elif uc['name'] == 'Zona de Proteção da Vida Marinha de Tamandaré':

             folium.GeoJson(uc,
                          style_function = lambda feature: {
                          "fillColor": "white",
                          "color": "red",
                          "weight": 2,
                          "dashArray": "10,10"},
                           zoom_on_click = True).add_to(mapa)
        
        else:

            folium.GeoJson(uc,
                          style_function = lambda feature: {
                          "fillColor": "white",
                          "color": "black",
                          "weight": 3},
                          zoom_on_click = True).add_to(mapa)
           
    return mapa
#-------------------------------------------------------------------------------------------------
municipios = ['geojson/pernambuco.geojson',
              'geojson/recife.geojson',
              'geojson/sirinhaem.geojson',
              'geojson/tamandare.geojson',
              'geojson/rio_formoso.geojson',
              'geojson/barreiros.geojson',
              'geojson/sao_jose.geojson']

ucs        = ['geojson/apacc.geojson', 
              'geojson/guadalupe.geojson',
              'geojson/pnmft.geojson',
              'geojson/saltinho.geojson',
              'geojson/apa_serrambi.geojson',
              'geojson/zpvmt.geojson',
              'geojson/apa_sirinhaem.geojson',
              
             ]

lista_municipios = load_geojson(municipios, ucs)[0]
lista_ucs = load_geojson(municipios, ucs)[1]

mapa_municipios = create_mapa_municipios(lista_municipios)
#-------------------------------------------------------------------------------------------------
#CONFIGURANDO A BARRA LATERAL
with st.sidebar:

    st.markdown("<h4 style='text-align: left; color: black;'>Escolha a Unidade de Conservação</h4>", unsafe_allow_html=True)
    ucs = list(st.multiselect(label = '(Escolha apenas uma)', 
                   options = ['APA Costa dos Corais',
                              'APA de Guadalupe',
                              'APA de Sirinhaém',
                              'APA Recifes de Serrambi',
                              'Parque Nacional Marinho do Forte de Tamandaré',
                              'Reserva Biológica de Saltinho',
                              'Zona de Proteção da Vida Marinha de Tamandaré'
                             ],
                  default = ['APA Costa dos Corais',
                              'APA de Guadalupe',
                              'APA de Sirinhaém',
                              'APA Recifes de Serrambi',
                              'Parque Nacional Marinho do Forte de Tamandaré',
                              'Reserva Biológica de Saltinho',
                              'Zona de Proteção da Vida Marinha de Tamandaré'])
             )    
#-------------------------------------------------------------------------------------------------
selecao = []

for uc in lista_ucs:

    if uc['name'] in ucs:

        selecao.append(uc)

mapa_ucs = create_mapa_ucs(selecao)
#-------------------------------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: black;'>Pesquisa Ecológica de Longa Duração Tamandaré Sustentável (PELD TAMS)</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Mapa de contaminação no sítio do PELD TAMS</h2>", unsafe_allow_html=True)

with st.container(border = True):

    st.markdown("<h4 style='text-align: left; color: black;'>Apresentação</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify'> O sítio PELD TAMS está localizado no litoral sul do Estado de Pernambuco (nordeste do Brasil) a 105 km da cidade de Recife. O sítio PELD TAMS está submetido a influências antrópicas a partir das cidades de Sirinhaém, Tamandaré, Rio Formoso, Barreiros e São José da Coroa Grande, contendo ecossistemas marinhos, estuarinos e dulcícolas. Esses ecossistemas registram o impacto antrópico da contaminação em matrizes ambientais como água, sedimento e biota.</p>", unsafe_allow_html=True)

col2, col3 = st.columns([0.5, 0.5], border = True, vertical_alignment="top")

with col2:
    
    st.markdown("<h5 style='text-align: center; color: black;'>Figura 1</h5>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center'> Litoral do Estado de Pernambuco destacando as cidades de Recife, Sirinhaém, Rio Formoso, Tamandaré, Barreiros e São José da Coroa Grande. </p>", unsafe_allow_html=True)
    
    st_folium(mapa_municipios, use_container_width = True)

with col3:
    
    st.markdown("<h5 style='text-align: center; color: black;'>Figura 2</h5>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center'> Unidades de Conservação federal, estadual e municipal no litoral sul de Pernambuco. </p>", unsafe_allow_html=True)
    st_folium(mapa_ucs, use_container_width = True)

