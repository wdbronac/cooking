# -*- coding: utf-8 -*-
import export_json_csv as imp


H,C = imp.download_cuisines_csv()
H,I = imp.download_ingredients_csv()

#IP = imp.download_csv('../data/ingredient_plat.csv')
CP = imp.download_csv('../data/cuisine_plat.csv')
for cp in CP[1:]:
    cp[1] = int(cp[1])
    
# NB de plats par cuisine

def nb_plats_cuisine(CP,c):
    compteur = 0
    for cp in CP[1:]:
        if cp[1]==c:
            compteur+=1
    return compteur

CUISINES_TOT = {}   # contient les N(cuisine)
for c in C:
    CUISINES_TOT[c[0]] = nb_plats_cuisine(CP,c[0])
    
# NB d'ingrédients par plat
        
COMPLEXITES_PLATS = {}
for p in 
        
def p_i_sachant_c(i,c):
    somme = 0
    for cp in CP[1:]:
        if cp[1]==c:
            somme += 1/
    return somme/CUISINES_TOT[c]