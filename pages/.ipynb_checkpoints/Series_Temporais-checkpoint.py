#Importando bibliotecas de análise
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

#Importando biblioteca para aplicação web
import streamlit as st
#-----------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title = 'Temporal Series', layout = 'wide')

#Função para carregar arquivos csv
@st.cache_data
def load_data(path):

    df = pd.read_csv(path)

    return df
#-----------------------------------------------------------------------------------------------------------------------
#Temporal series of resident population and urban area of Tamandaré City
def urban_population(df):

    #Transformação dos dados nas séries temporais de populaçao residente e áreas
    df['year'] = pd.to_datetime(df['year'], format = '%d/%m/%Y', dayfirst = True)
    
    #Dados para o período de 1997 (após formação do município de Tamandaré) a 2021
    df = df.loc[df['resident_pop'].isnull() == False, :].copy()

    fig1, ax1 = plt.subplots(figsize = (3,2))
    ax1.plot(df['year'], df['resident_pop'], color = 'red')
    ax1.set_xlabel('Year', fontsize = 9, labelpad = 10)
    ax1.set_ylabel('Resident population', color = 'red', fontsize = 9, labelpad = 10)
    ax1.tick_params(axis= 'x', labelrotation = 90)
    ax1.tick_params(axis='both', which = 'major', labelsize=6)

    ax2 = ax1.twinx()

    ax2.plot(df['year'], df['urban_area'], color = 'black')
    ax2.set_ylabel('Urban area (ha)', fontsize = 9, rotation = -90, labelpad = 20)
    ax2.tick_params(axis='y', which = 'major', labelsize=6)
    

    return fig1
#-----------------------------------------------------------------------------------------------------------------------
#Temporal series of Atlantic Forest and mangrove areas
def forest_areas(df):

    #Transformação dos dados nas séries temporais de populaçao residente e áreas
    df['year'] = pd.to_datetime(df['year'], format = '%d/%m/%Y', dayfirst = True)

    fig2, ax3 = plt.subplots(figsize = (3, 2))
    ax3.plot(df['year'], df['atl_forest_area'], color = 'green')
    ax3.set_xlabel('Year', fontsize = 9, labelpad = 10)
    ax3.set_ylabel('Atlantic Forest (ha)', color = 'green', fontsize = 9, labelpad = 10)
    ax3.tick_params(axis = 'x', labelrotation = 90)
    ax3.tick_params(axis = 'both', which = 'major', labelsize = 6)

    ax4 = ax3.twinx()

    ax4.plot(df['year'], df['mang_area'], color = 'blue')
    ax4.set_ylabel('Mangroves (ha)', color = 'blue', fontsize = 9, rotation = -90, labelpad = 20)
    ax4.tick_params(axis = 'y', which = 'major', labelsize = 6)

    return fig2
#-----------------------------------------------------------------------------------------------------------------------
#Temporal series of agricultural and livestocks areas
def agricultural_livestock(df):

    #Transformação dos dados nas séries temporais de populaçao residente e áreas
    df['year'] = pd.to_datetime(df['year'], format = '%d/%m/%Y', dayfirst = True)

    fig3, ax5 = plt.subplots(figsize = (3, 2))
    ax5.plot(df['year'], df['agricultural_area'], color = 'gray')
    ax5.set_xlabel('Year', fontsize = 9, labelpad = 10)
    ax5.set_ylabel('Agricultural area (ha)', color = 'gray', fontsize = 9, labelpad = 10)
    ax5.tick_params(axis = 'x', labelrotation = 90)
    ax5.tick_params(axis = 'both', which = 'major', labelsize = 6)

    ax6 = ax5.twinx()

    ax6.plot(df['year'], df['livestock_area'], color = 'brown')
    ax6.set_ylabel('Livestock area (ha)', fontsize = 9, color = 'brown', rotation = -90, labelpad = 20)
    ax6.tick_params(axis = 'y', which = 'major', labelsize = 6)

    return fig3
#-----------------------------------------------------------------------------------------------------------------------
def effluent_outflow(df):

    df2 = df.loc[df['ete'] == 'Tamandare', :].copy()
    df2.columns = ['ete', 'mes', 'periodo', 'vazao']

    df2_seco = df2.loc[df['periodo'] == 'seco', :].copy()
    df2_seco = df2_seco.reset_index(drop=True)
    df2_seco.loc[6, :] = df2_seco.loc[0, :] 
    df2_seco.loc[7, :] = df2_seco.loc[1, :]
    df2_seco = df2_seco.drop([0,1], axis=0).reset_index(drop=True)
    df2_chuvoso = df2.loc[df2['periodo'] == 'chuvoso', :].copy()

    fig4, ax7 = plt.subplots(figsize = (3, 2))
    ax7.bar(df2_seco['mes'], df2_seco['vazao'], color='g', label = 'Dry Season')
    ax7.bar(df2_chuvoso['mes'], df2_chuvoso['vazao'], color='r', label = 'Wet Season')
    ax7.tick_params(axis= 'x', labelrotation = 90)
    ax7.legend(prop={'size': 6})
    ax7.set_xlabel('Month', fontsize = 8)
    ax7.set_ylabel('Effluent Outflow (m3/month)', fontsize = 8, labelpad = 10)
    ax7.set_ylim(68000,82000)
    ax7.set_yticks([68000, 72000, 76000, 80000, 84000])
    ax7.tick_params(axis = 'both', which = 'major', labelsize = 6)

    return fig4  
#-----------------------------------------------------------------------------------------------------------------------
def temporal_series_effluent(df):

    df3 = df.set_index('mes_ano')

    fig5, ax8 = plt.subplots(figsize = (12,4))
    #fig5.suptitle('Temporal series of effluent outflow and residential energy consumption')
    
    ax8.plot(df3.index, df3['vazao_ete'], color = 'red')
    ax8.set_xlabel('Month/Year', fontsize = 14)
    ax8.set_ylabel('Effluent outflow (m3/month)', fontsize = 11, labelpad = 10, color = 'red')
    ax8.tick_params(axis = 'x', rotation = 90, labelsize = 7)
    
    ax9 = ax8.twinx()
    
    ax9.plot(df3.index, df3['consumo_energia'], color = 'green')
    ax9.set_ylabel('Energy consumption (MWh)', color = 'green', fontsize = 12, rotation = -90, labelpad = 20)
    ax9.set_yticks([1000, 1400, 1800, 2200, 2600, 3000, 3400])
    ax9.tick_params(axis = 'y', which = 'major', labelsize = 10)
    

    return fig5
#-----------------------------------------------------------------------------------------------------------------------
#Carregando os dataframes e figuras
path1 = '../datasets/serie_temporal_uso_ocupacao_solo.csv'
path2 = '../datasets/serie_temporal_vazao_mensal_ete.csv'
path3 = '../datasets/serie_temporal_efluente_ete.csv'

df1 = load_data(path1)
df2 = load_data(path2)
df3 = load_data(path3)
fig1 = urban_population(df1)
fig2 = forest_areas(df1)
fig3 = agricultural_livestock(df1)
fig4 = effluent_outflow(df3)
fig5 = temporal_series_effluent(df2)
#-----------------------------------------------------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: black;'> Temporal series of land use and urban population</h1>", 
            unsafe_allow_html=True)
st.markdown("---------------------------------------------------------------------------------------------------------")

with st.container():
    
    st.markdown("<h5 style='text-align: center; color: black;'><strong>Introduction</strong></h5>",
                unsafe_allow_html=True)
    

st.markdown("---------------------------------------------------------------------------------------------------------")


col1, col2 = st.columns([0.5, 0.5], border = False, vertical_alignment="center")

with col1:
    
    st.markdown("<h5 style='text-align: center; color: black;'>Figure 1</h5>",
                unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: black;'>Temporal series of Atlantic Forest and Mangrove areas</h6>",
                unsafe_allow_html=True)
    st.pyplot(fig2, use_container_width = True)

with col2:
        
    with st.container(height = 300):
        
        st.markdown("<p style='text-align: justify'> From 1997 to 2024, the estimated resident population of Tamandaré city increased from 15,611 to 24,534 inhabitants (IBGE, 2025). Tamandaré is a tourist city, but there is no accurate estimate of the population growth during the tourism period (from December to February). </p>", unsafe_allow_html=True)
        
        st.markdown("<p><strong>Referências:</strong></p>", unsafe_allow_html=True)
        st.markdown("1. [IBGE, 2025](https://www.ibge.gov.br/)")

st.markdown("---------------------------------------------------------------------------------------------------------")

col3, col4 = st.columns([0.5, 0.5], border = False, vertical_alignment="center")

with col3:
    
    st.markdown("<h5 style='text-align: center; color: black;'>Figure 2</h5>",
                unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: black;'>Temporal series of agricultural and livestock areas</h6>",
                unsafe_allow_html=True)
    st.pyplot(fig3, use_container_width = True)

with col4:
        
    with st.container(height = 300):
        
        st.markdown("<p style='text-align: justify'> From 1997 to 2024, the estimated resident population of Tamandaré city increased from 15,611 to 24,534 inhabitants (IBGE, 2025). Tamandaré is a tourist city, but there is no accurate estimate of the population growth during the tourism period (from December to February). </p>", unsafe_allow_html=True)
        
        st.markdown("<p><strong>Referências:</strong></p>", unsafe_allow_html=True)
        st.markdown("1. [IBGE, 2025](https://www.ibge.gov.br/)")


st.markdown("---------------------------------------------------------------------------------------------------------")


col5, col6 = st.columns([0.5, 0.5], border = False, vertical_alignment="center")

with col5:
    
    st.markdown("<h5 style='text-align: center; color: black;'>Figure 3</h5>",
                unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: black;'>Temporal series of resident population and urban area</h6>",
                unsafe_allow_html=True)
    st.pyplot(fig1, use_container_width = True)

with col6:
        
    with st.container(height = 300):
        
        st.markdown("<p style='text-align: justify'> From 1997 to 2024, the estimated resident population of Tamandaré city increased from 15,611 to 24,534 inhabitants (IBGE, 2025). Tamandaré is a tourist city, but there is no accurate estimate of the population growth during the tourism period (from December to February). </p>", unsafe_allow_html=True)
        
        st.markdown("<p><strong>Referências:</strong></p>", unsafe_allow_html=True)
        st.markdown("1. [IBGE, 2025](https://www.ibge.gov.br/)")

st.markdown("---------------------------------------------------------------------------------------------------------")
col7, col8 = st.columns([0.5, 0.5], border = False, vertical_alignment="center")

with col7:
    
    st.markdown("<h5 style='text-align: center; color: black;'>Figure 4</h5>",
                unsafe_allow_html=True)
    st.markdown("<h6 style='text-align: center; color: black;'>Mean Monthly Effluent Outflow</h6>",
                unsafe_allow_html=True)
    st.pyplot(fig4, use_container_width = True)

with col8:
        
    with st.container(height = 300):
        
        st.markdown("<p style='text-align: justify'> From 1997 to 2024, the estimated resident population of Tamandaré city increased from 15,611 to 24,534 inhabitants (IBGE, 2025). Tamandaré is a tourist city, but there is no accurate estimate of the population growth during the tourism period (from December to February). </p>", unsafe_allow_html=True)
        
        st.markdown("<p><strong>Referências:</strong></p>", unsafe_allow_html=True)
        st.markdown("1. [IBGE, 2025](https://www.ibge.gov.br/)")

st.markdown("---------------------------------------------------------------------------------------------------------")

st.markdown("<h5 style='text-align: center; color: black;'>Figure 5</h5>",
                unsafe_allow_html=True)

st.markdown("<h6 style='text-align: center; color: black;'>Temporal series of residential energy conumption in Tamandaré city and effluent outflow from Tamandaré STP to Ariquindá River</h6>",
                unsafe_allow_html=True)

st.pyplot(fig5)
st.markdown("---------------------------------------------------------------------------------------------------------")








