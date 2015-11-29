# -*- coding: utf-8 -*-
import pandas as pd, json
import matplotlib, os

chemin = "../data/train.json"

json_data = open(chemin)
train = json.load(json_data)

""" SYNTAXE
train[0]
train[0]['cuisine']
train[0]['ingredients']
train[0]['ingredients'][0]
"""

# TOUT METTRE DANS DES CSV

def construire_db():
    print "prétraitement"
    enlever_virgules()
    print "cuisines"
    build_csv_cuisines()
    print "ingrédients"
    build_csv_ingredients()
    print "ingrédients - plats"
    build_relations_ingredients_plats()
    print "cuisines - plats"
    build_relations_plats_cuisines()
    

# TRAITEMENT DU JSON (on enlève les virgules des ingrédients)

def enlever_virgules():
    for plat in train:
        for i,ing in enumerate(plat['ingredients']):
            plat['ingredients'][i]=ing.replace(",","")
    
# TRAITEMENT DES INGREDIENTS

def liste_ingredients_from_json():
    N = len(train)
    i1 = [train[k]['ingredients'] for k in range(N)]
    i2 = matplotlib.cbook.flatten(i1)
    i3 = [i for i in i2]
    i3.sort()
    k=0
    a=0
    while k<len(i3)-1:
        if i3[k]==i3[k+1]:
            a = i3.pop(k)
        else:
            k=k+1
    return i3
        
def build_csv_ingredients():
    liste = liste_ingredients_from_json()
    header = ["id","nom"]
    T = [header]
    for i,ing in enumerate(liste):
        T.append([str(i+1),ing])
    ecrire_csv("data/ingredients_db.csv",T)
    
def download_ingredients_csv():
    D = download_csv("data/ingredients_db.csv")
    for d in D[1:]:
        d[0] = int(d[0])
        st = d[1]
        while len(d)>2:
            d[1] = d[1]+","+d.pop(2)        
    return D[0],D[1:]
    
# RELATIONS PLATS - INGREDIENTS

def id_by_name(nom,I):
    k0 = 0
    k1 = len(I)-1
    while I[k0][1]!=nom and k0<k1:
        km = (k0+k1)/2
        if I[km][1]>nom:
            k1=km-1
        elif I[km][1]<nom:
            k0=km+1
        else:
            k0=km
    if I[k0][1]!=nom:
        print nom
        return 1/0
    return I[k0][0]

def build_relations_ingredients_plats():
    H,I = download_ingredients_csv()
    T = [["id_plat","id_ingredient"]]
    for plat in train:
        #print plat['id'] #,plat['ingredients']
        for ing in plat['ingredients']:
            T.append([str(plat['id']),str(id_by_name(str(ing.encode('utf-8')),I))])
    ecrire_csv("data/ingredient_plat.csv",T)
    
# CUISINES

def build_csv_cuisines():
    CUISINES = []
    for plat in train:
        CUISINES.append(plat['cuisine'].encode('utf-8'))
    CUISINES.sort()
    remove_duplicates(CUISINES)
    header = ["id","nom"]
    T = [header]
    for i,c in enumerate(CUISINES):
        T.append([str(i+1),c])
    ecrire_csv("data/cuisines_db.csv",T)  
      
def download_cuisines_csv():
    D = download_csv("data/cuisines_db.csv")
    for d in D[1:]:
        d[0] = int(d[0])
    return D[0],D[1:]
    
# RELATIONS PLAT - CUISINE


def build_relations_plats_cuisines():
    H,C = download_cuisines_csv()
    T = [["id_plat","id_cuisine"]]
    for plat in train:
        T.append([str(plat['id']),str(id_by_name(str(plat['cuisine'].encode('utf-8')),C))])
    ecrire_csv("data/cuisine_plat.csv",T)
    
# FONCTIONS GENERALES

def remove_duplicates(tab):
    k=0
    a=0
    while k<len(tab)-1:
        if tab[k]==tab[k+1]:
            a = tab.pop(k)
        else:
            k=k+1
        
def download_csv(path):
    sep = ','
    T = []
    table = open(path,"r")
    db = table.read()
    table.close()
    erase = True
    while erase:
        k=0
        while k<len(db) and db[k]!='\n':
            k+=1
        k=min(k,len(db)-1)
        if (db[k]=='\n' and k<len(db)-1) or k==len(db)-1:
            line = db[:k+1]
            T.append([])
            cell = ""
            for i in line:
                if i!=sep and i!='\n':
                    cell+=i
                else:
                    T[-1].append(cell)
                    cell = ""
            if cell!="":
                T[-1].append(cell)
            db = db[k+1:]
        if len(db)==0:
            erase = False
    return T
    
def ecrire_csv(path,tableau):
    csv = ""
    sep = ","   # séparateur
    for ligne in tableau:
        L = ""
        for case in ligne:
            if L!="": L+=sep
            L+=case
        csv+=L+'\n'
    
    table = open(path,"w")
    table.write(csv.encode('utf-8'))
    table.close()
