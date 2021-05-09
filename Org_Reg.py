# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 12:17:13 2021

@author: Administrador
"""


#Obtención de datos de organización regional Chile
import requests
from bs4 import BeautifulSoup
import pandas as pd

class ORG_REG():

    def __init__(self):
        self.csvname = 'org_reg.csv'
        r = requests.get('https://es.wikipedia.org/wiki/Anexo:'
                         'Comunas_de_Chile')
        # print(r.content)
        soup = BeautifulSoup(r.content, features='html5lib')
        tabla = soup.find('div', class_='mw-parser-output')
        
        #Columnas y Cabecera
        A, B, C, D, E, F, G, H, I, J = [], [], [], [], [], [], [], [], [], []
        K, L = [], []
        
        l_dat = [B, C, D, E, F, G, H, I, J, K, L]
        #Cabecera
        for cab in tabla.find_all('th'):
            c_ab = cab.text.strip('\n')
            A.append(c_ab)
        A[0] = 'cod_comuna'
        #Columnas
        for dat in tabla.find_all('tr'):
            dat_c = dat.find_all('td')
            if len(dat_c) == 12:
                B.append(dat_c[0].text.strip('\n'))
                C.append(dat_c[1].text.strip('\n'))
                D.append(dat_c[2].text.strip('\n'))
                E.append(dat_c[3].text.strip('\n'))
                F.append(dat_c[4].text.strip('\n'))
                G.append(dat_c[5].text.strip('\n'))
                H.append(dat_c[6].text.strip('\n'))
                I.append(dat_c[7].text.strip('\n'))
                J.append(dat_c[8].text.strip('\n') + '|' + 
                         dat_c[9].text.strip('\n'))
                K.append(dat_c[10].text.strip('\n'))
                L.append(dat_c[11].text.strip('\n'))
        
        #Diccionario
        z_iterador = zip(A, l_dat)
        dic = dict(z_iterador)
        
        #Dataframe
        org_reg = pd.DataFrame(dic)
        dat_str = org_reg[['Nombre', 'Provincia', 'Región']]
        #Dejar en MAYUSCULAS
        dat_str = dat_str.apply(lambda x: x.astype(str).str.title())
        #Quitar acentos
        # dat_str = dat_str.apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))
        org_reg[['Nombre', 'Provincia', 'Región']] = dat_str
        org_reg.to_csv(self.csvname, index=False)
        self.org_reg = org_reg
        self.cab = A