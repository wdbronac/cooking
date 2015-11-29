# -*- coding: utf-8 -*-
import export_json_csv as imp, math

# Se placer dans le répertoire /code

# Ce code établit un modèle sur une proportion PROP des données
# Les données restantes sont utilisées pour un test

PROP = 0.99


print "Téléchargement des données..."
fichier = '../data'
H,C = imp.download_cuisines_csv(fichier,"")
H,I = imp.download_ingredients_csv(fichier,"")
CP = imp.download_csv2('../data/cuisine_plat.csv')
IP = imp.download_csv2('../data/ingredient_plat.csv')

def transformation_matrice_str_to_int(M):
    for i in range(len(M)):
        for j in range(len(M[0])):
            M[i][j] = int(M[i][j])

transformation_matrice_str_to_int(CP[1:])
transformation_matrice_str_to_int(IP[1:])

IP2 = zip(*IP)

# On coupe en train/test

# TRAINING DATA

N = int(len(CP)*PROP)
CP_test = CP[N:]
CP = CP[:N]

# TESTING DATA  (long à calculer)

print "calcul de l'ensemble des tests (",len(CP_test),")"

for k in range(len(CP_test)):
    if k%25==0: print k
    plat = CP_test[k][0]
    ingredients_k = []
    for i in range(len(IP)):
        if IP[i][0]==plat:
            ingredients_k.append(IP[i][1])
    CP_test[k].append(ingredients_k)


# NB de plats par cuisine

print "calculs préliminaires..."

def nb_plats_cuisine(CP,c):     # Calcule le nombre de plats dans une cuisine c
    compteur = 0
    for cp in CP[1:]:
        if cp[1]==c:
            compteur+=1
    return compteur

CUISINES_TOT = {}   # contient les Nb plats par cuisine
for c in C:
    CUISINES_TOT[c[0]] = nb_plats_cuisine(CP,c[0])
    
# NB d'ingrédients par plat
# Ceci présuppose que le fichier csv est ordonné :

COMPLEXITES_PLATS = {}  # nb d'ingrédients par plat
k=1
while k<len(IP)-1:
    k2=k
    while k2<len(IP)-1 and IP[k2][0]==IP[k][0]:
        k2+=1
    if k2 == len(IP)-1:
        k2+=1
    COMPLEXITES_PLATS[IP[k][0]]= k2-k
    k=k2
     
# Proba conditionnelle

def cuisine_du_plat(p):     # trouve la cuisine associée au plat d'id p
                            # ne rend rien si on n'a pas l'info
    for i in range(1,len(CP)):
        if CP[i][0]==p:
            return CP[i][1]

def ajout_cuisine_IP2():    # cette fonction ajoute une colonne à IP2 : les cuisines
    print "start calcul"
    IP22 = ["id_cuisine"]
    plat=1
    cuisine = cuisine_du_plat(plat)
    for i in range(1,len(IP2[0])):
        if i%20000==0:
            print i
        p = IP2[0][i]
        if p!=plat:
            plat=p
            cuisine = cuisine_du_plat(plat)
        IP22.append(cuisine)
    IP2.append(IP22)
    
ajout_cuisine_IP2()


# Calcul de IC (matrice ingrédient-cuisine)
IC = []     # 20 lignes (cuisines) / 6715 colonnes (nb de fois que l'ingrédient apparait)

def construction_IC():
    for cuis in C:
        print cuis
        c = cuis[0]
        ing = [0 for i in range(len(I)+1)]
        for i in range(1,len(IP2[0])):
            if IP2[2][i]==c:
                ing[IP2[1][i]]+=1
        IC.append(ing)
        
construction_IC()
    
NC = []    # nb d'ingrédients par cuisine (vecteur de taille 20)
for cuis in C:
    c = cuis[0]
    NC.append(sum(IC[c-1]))
    
PIC = [[C[i][1] for i in range(len(C))]]    # proba ingrédient sachant cuisine : PIC[ingredient][cuisine]
for i in range(1,len(I)+1):
    probs = []
    for j in range(len(C)):
        c = C[j][0]
        probs.append(float(IC[c-1][i])/NC[c-1])
    PIC.append(probs)

CONST_CUIS = []     # produits des 1-P(i|cuisine) : constante pour chaque cuisine
                    # (vecteur de taille 20)
for cuis in C:
    c = cuis[0]-1
    CON = 1.0
    for i in range(1,len(I)+1):
        CON*= (1-PIC[i][c])
    CONST_CUIS.append(CON)

def proba_cuisine_sachant_ingredients(c,ingredients):
    Pcuisine = NC[c-1] # ou CUISINES_TOT[c]
    const_cuisine = CONST_CUIS[c-1]
    P = Pcuisine/const_cuisine
    p=0
    for i in ingredients:
        if i<len(PIC) and i>0: p=PIC[i][c-1]/(1-PIC[i][c-1])
        if p==0: p = 10**(-6)
        P*=p
    return P
    
def argmax(tableau):     # pour un tableau non vide, rend l'index d'un max
    maxi = tableau[0]
    ind = 0
    for i,t in enumerate(tableau):
        if t>maxi:
            maxi=t
            ind = i
    return ind
    
def procuste(chaine,n=6):
    if len(chaine)<n:
        return chaine+(n-len(chaine))*" "
    elif len(chaine)>n:
        return chaine[:n]
    else:
        return chaine
    
def afficher_matrice(mat,n=6):
    pr = ""
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            pr+=procuste(str(math.trunc(mat[i][j]*10**4)/10**4),n)+"  "
        pr+="\n"
    print pr

def trouver_cuisine(ingredients):   # cette fonction rend l'estimation pour la cuisine
    # ingredients est la liste des ids des ingrédients
    probs = [proba_cuisine_sachant_ingredients(c,ingredients) for c in range(len(C))]
    mp = max(probs)
    probs = [p/mp for p in probs]
    #afficher_matrice([probs])
    return argmax(probs)

# pour tester la fonction : le premier plat (bonne réponse : 7)
#ingredients_test = [5223,957,3034,2885,4570,4912,5406,2879,2549]
#trouver_cuisine(ingredients_test)

def evaluate_model(set_ingredients):    # prend en argument une liste d'éléments de la forme
    # [id_plat,id_cuisine, listes d'ingrédients]
    CONFUSION = [[0 for i in range(21)] for j in range(21)]
    for i in range(len(set_ingredients)):
        if i%100==0: print i
        c1 = set_ingredients[i][1]
        c2 = trouver_cuisine(set_ingredients[i][2])
        CONFUSION[c1][c2]+=1
    return CONFUSION                    # rend la matrice de confusion
    
def analyse_confusion(MC):  # on analyse la matrice de confusion (evaluate_model)
    afficher_matrice(MC,2)
    diag = [MC[i][i] for i in range(len(MC))]
    err = [sum(MC[i][j] for j in range(len(MC)) if i!=j) for i in range(len(MC))]
    B,M = sum(diag),sum(err)
    print "Bien classés : ",B, " => ",float(B)/(B+M)*100,"%"
    print "Mal classés : ",M, " => ",float(M)/(B+M)*100,"%"
    return diag, B, err, M 
    
CONFUSION = evaluate_model(CP_test)
analyse_confusion(CONFUSION)