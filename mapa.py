import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Vestibular IFMG 2025",  page_icon="🗺️", layout="wide")

# Função para carregar os dados
def load_data():
    # Substitua o caminho pelos seus arquivos
    dados_df = pd.read_excel('./dados.xlsx')
    lat_lon_df = pd.read_csv('./latitude-longitude-cidades.csv')

    # Limpando e formatando os dados de coordenadas
    lat_lon_df[['id_municipio', 'uf', 'municipio', 'longitude', 'latitude']] = lat_lon_df['id_municipio;"uf";"municipio";"longitude";"latitude"'].str.split(';', expand=True)
    lat_lon_df['municipio'] = lat_lon_df['municipio'].str.replace('"', '')
    lat_lon_df['uf'] = lat_lon_df['uf'].str.replace('"', '')
    lat_lon_df['longitude'] = lat_lon_df['longitude'].astype(float)
    lat_lon_df['latitude'] = lat_lon_df['latitude'].astype(float)

    # Mesclando os dados das cidades com suas respectivas coordenadas geográficas
    merged_df = pd.merge(dados_df, lat_lon_df, left_on=['Cidade', 'uf'], right_on=['municipio', 'uf'], how='inner')

    return merged_df

# Carregando os dados
df = load_data()

# Criando o gráfico no Streamlit
st.title('📊 Análise Geográfica dos pedidos de acesso à informação')
st.write("Distribuição geográfica dos pedidos de acesso à informação em Minas Gerais entre 2012 a 2023.")


st.warning("Fonte: Dados disponibilizados pela Controladoria Geral da União atravpés da Plataforma Integrada de Ouvidoria e Acesso à Informação (Fala.BR)")

# Criando o gráfico Mapbox
fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    hover_name="Cidade",
    hover_data=["Registros"],
    color="Registros",
    size="Registros",
    zoom=5,
    height=600,
    size_max=30,
    color_continuous_scale=px.colors.cyclical.HSV
)

# Configurando o estilo do mapa
fig.update_layout(mapbox_style="carto-positron") 
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, 
                    height=700, 
                    mapbox_center={"lat": -19.91018, "lon": -43.92657})

fig.update_layout(showlegend=False)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)
