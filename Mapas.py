# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 14:11:17 2021

@author: Administrador
"""


import json

class ch_maps():
    def __init__(self):
        reg = {'aricayparinacota': 'arica_y_parinacota.json',
               'tarapaca': 'tarapaca.json', 'antofagasta': 'antofagasta.json',
               'atacama': 'atacama.json', 'coquimbo': 'coquimbo.json',
               'valparaiso': 'valparaiso.json', "lib.gral.bernardoo'higgins":
               'b_ohiggins.json', 'maule': 'maule.json', 'nuble': 
               'bio_bio.json', 'biobio': 'bio_bio.json', 'laaraucania':
               'araucania.json', 'losrios': 'los_rios.json', 'loslagos':
               'los_lagos.json', 'aysendelgral.c.ibanezdelcampo':
               'ayse_gral_ibanez_campo.json', 'magallanesyantarticachilena':
               'magallanes_antartica.json', 'metropolitanadesantiago':
                   'metropolitana.json'}
        self.reg = reg

    def obt_polg(self, lista):
        fnms = []
        i = 0
        for li in lista:
            fnms.append(self.reg[li])
        self.fnms = fnms
        for fname in self.fnms:
            if i == 0:
                ma = json.load(open(f'Map/{fname}', 'r'))
                i += 1
            else:
                tam = json.load(open(f'Map/{fname}', 'r'))
                for ta in tam['features']:
                    ma['features'].append(ta)
        self.polg = ma
        return self.polg