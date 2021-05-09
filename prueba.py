# -*- coding: utf-8 -*-
"""
Created on Sat May  8 20:11:16 2021

@author: Administrador
"""

import streamlit as st
import pandas as pd
from unidecode import unidecode
from Org_Reg import ORG_REG
from Mapas import ch_maps as cm
from Obtencion_Datos import Obtiene_Datos as od
import folium
from streamlit_folium import folium_static


# st.set_page_config(layout='wide')
@st.cache(allow_output_mutation=True)
def orga_reg():
    with st.spinner('Obteniendo datos...'):
        try:
            org_reg = pd.read_csv(ORG_REG().csvname)
        except FileNotFoundError:
            org_reg = ORG_REG().org_reg
    return org_reg

@st.cache(allow_output_mutation=True)
def obt_data():
    dt = od().data
    return dt

def no_acento(var):
    if type(var) == str:
        var = unidecode(var).lower()
    elif type(var) == list:
        var = [unidecode(x).lower().replace(' ', '') for x in var]
    else:
        var = var.str.lower()\
           .str.normalize('NFKD')\
           .str.encode('ascii', errors='ignore')\
           .str.decode('utf-8')\
           .str.replace(' ', '')
    return var

@st.cache
def ob_maps(reg):
    geo_comunas = cm()
    geo_comunas = geo_comunas.obt_polg(reg)
    return (geo_comunas)

st.write("""
# Mapa Paso a Paso
         """)

dt = obt_data()
o_reg = orga_reg()
regiones = o_reg['Región'].drop_duplicates().tolist()  
st.sidebar.header('Selecciona la región que quieras revisar')
reg_selec = st.sidebar.multiselect('Regiones', regiones)
procesar = st.sidebar.button('Ver Mapa')

if procesar:
    reg = no_acento(reg_selec)
    dt['com'] = no_acento(dt['COMUNA'])
    o_reg['Reg'] = no_acento(o_reg['Región'])
    o_reg['com'] = no_acento(o_reg['Nombre'])
    Comunas = o_reg[o_reg['Reg'].isin(reg)].loc[:, ('cod_comuna', 'Nombre',
                                              'Provincia', 'Región',
                                              'com', 'Latitud', 'Longitud')]
    datos = dt.merge(Comunas, how='inner', on='com')
    lat = datos['Latitud'].str.split('°').map(lambda x: x[0])
    lat = lat.str.replace('−', '-').astype(float)
    lon = datos['Longitud'].str.split('°').map(lambda x: x[0])
    lon = lon.str.replace('−', '-').astype(float)
    m = folium.Map(location=[lat.mean(), lon.mean()], zoom_start=8)
    datos = datos.astype({'Paso':'int16'})
    geo_comunas = ob_maps(reg)
    
    
    style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
    
    folium.Choropleth(
        geo_data = geo_comunas,
        name = 'choropleth',
        data = datos,
        style_function = style_function,
        columns = ['cod_comuna', 'Paso'],
        key_on = 'properties.COD_COMUNA',
        fill_color = 'RdBu',
        fill_opacy = 0.2,
        line_opacy = 0.2,
        legend_name = 'Estado',
        nan_fill_color = 'purple',       
        ).add_to(m)
    folium_static(m)
    st.dataframe(datos)
else:
    st.stop()
