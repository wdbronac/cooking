# -*- coding: utf-8 -*-
import pandas as pd, json
import export_json_csv as imp
import naive_bayes_gabriel as nbg

# Se placer dans le répertoire /code
# Ce code soumet une tentative de réponse
# Ce code charge naive_bayes_gabriel, ce qui prend un certain temps...

fichier = "../data"
chemin = fichier+"/test.json"
nom_soumission = "submission"
H,I = imp.download_ingredients_csv(fichier,"")
H,C = imp.download_cuisines_csv(fichier,"")

json_data = open(chemin)
test = json.load(json_data)

def trouver_id_ingredient(ing):
    for i in range(len(I)):
        if I[i][1]==ing.encode('utf-8'):
            return I[i][0] 
    return 0

def base_de_test():
    TEST = []
    for i in range(len(test)):
        idplat = test[i]['id']
        liste = []
        for ing in test[i]['ingredients']:
            ing_id = trouver_id_ingredient(ing)
            liste.append(ing_id)
        TEST.append([idplat]+[liste])
    return TEST
    
def cuisine_by_id(idcuisine):
    for i in range(len(C)):
        if C[i][0]==idcuisine: return C[i][1]
    
def submission(TEST):
    PREDICTIONS = [['id','cuisine']]
    for t in range(len(TEST)):
        if t%100==0: print t
        pred = nbg.trouver_cuisine(TEST[t][1])
        PREDICTIONS.append([str(TEST[t][0]),str(cuisine_by_id(pred))])
    return PREDICTIONS
    
def soumettre(P,fichier,nom):
    imp.ecrire_csv(fichier+"/"+nom+".csv",P)

############

TEST = base_de_test()
PREDICTIONS = submission(TEST)
soumettre(PREDICTIONS,fichier,nom_soumission)