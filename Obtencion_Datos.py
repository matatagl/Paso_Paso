# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 20:51:28 2021

@author: Administrador
"""


import requests
from bs4 import BeautifulSoup
import ast
import pandas as pd

# url ='https://e.infogram.com/81277d3a-5813-46f7-a270-79d1768a70b2?parent_url'
# '=https%3A%2F%2Fwww.gob.cl%2Fcoronavirus%2Fpasoapaso%2F&src=embed#'

class Obtiene_Datos():
    """Obtiene los datos desde URL y los entrega como DataFrame"""
    def __init__(self):
        #Obtiene datos desde url
        url ='https://e.infogram.com/81277d3a-5813-46f7-a270-79d1768a70b2?parent_url'
        '=https%3A%2F%2Fwww.gob.cl%2Fcoronavirus%2Fpasoapaso%2F&src=embed#'
        self.url = url
        r = requests.get(url)
        dat_html = r.content
        dat_soup = BeautifulSoup(dat_html, features='lxml')
        #Busca todos los scripts en JS y su contenido, se pasan a una lista
        #de STR
        scr_list = [str(s) for s in dat_soup.find_all('script')]
        #Busca el index
        ind = [i for i, s in enumerate(scr_list) if 'Situación Comunal' in s]
        #Aisla data
        ind = ind[0]
        ini = scr_list[ind].find('[[["') + 2
        fin = scr_list[ind].find('"]]]') + 2
        #Crea lista de datos y los pasa a un DataFrame
        data_l_t = ast.literal_eval(scr_list[ind][ini:fin])
        columns = data_l_t[0]
        data_l = data_l_t[1:]
        data = pd.DataFrame(data=data_l, columns=columns)
        data['COMUNA'] = data['COMUNA'].str.title()
        data['COMUNA'] = data['COMUNA'].replace('Llaillay', 'LLay-llay')
        data['COMUNA'] = data['COMUNA'].replace('Calera', 'La calera')
        self.data = data