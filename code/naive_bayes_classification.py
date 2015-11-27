import numpy as np
import pandas as pd


#train = pd.read_json('../data/train.csv')
json_data=open('../data/train.csv').read()
data = json.loads(json_data)

#implement a prediction of the class with the naive bayes method


#Divides between the training set and the validation set

train = data[0: floor(9*len(train)/10)]
valid = data[train+1::]


#--------------------------------------building the model--------------------------------------------

#1: find all the cuisines
#2: find all the ingredients
#3: build an "empty" total_probs dictionary
#4: fill this dictionary thanks to the naive Bayes method

#constructs an empty dictionary
print 'building an empty dictionary of the cuisines and ingredients'
total_probs = dict 
for sample in train:
    if sample['cuisine'] not in total_probs.keys():    #if  the cuisine is not present yet in the total_probs dict
        total_probs[sample['cuisine'] ] = []  # Adds the new cuisine in the total_probs keys
    for ingredient in sample['ingredients']: 
        if ingredient is not in total_probs[0][:, 0]: #if the ingredient is not in the list of ingredients of the first entry of the dict
            for cuisine in total_probs.keys(): #append it to the list of ingredients of every entry of the dictionary
                total_probs[cuisine].append([ingredient, 0])


#Computes the matrix of the probabilities of the cuisine
nb_tot =len(train)
cuisine_probs = dict
for sample in train: 
    if sample['cuisine'] not in cuisine_probs.keys():
        cuisine_probs.append({sample['cuisine']: 1.0/nb_tot} 
    else: 
        cuisine_probs[sample['cuisine'] ]+=1.0/nb_tot


for cuisine in total_probs: 
    for ing_prob in cuisine:
        for sample in train: 
            total = 0
            found = 0
            if cuisine == train['cuisine']:
                total +=1
                if ing_prob[0] in train['ingredients']:
                    found +=1
        total_probs[cuisine][ing_prob[0]][1] = found/total


#then for every vector [ x1, x2, x3, x4], compute the score for each class, and label the vector with the most probable class.

#-------------------------------------------predicting the class---------------------------------------------------------
#echantillon à tester : {'id':1324134, 'ingredients': [baking powder, requin]}
#score has to be of this form:  score = {'tex_mex': 1, 'chines': 1} ----TODO: create it of this form---------
for cuisine in total_probs.keys(): 
    for ingredient in total_probs[cuisine]:  #total_probs has to be of the form {'tex mex':[['tomato sauce ',  0.8], ['pepper',  0.6] ], 'chinese':[['tomato sauce ', 0.3], ['pepper',  0.5] ]} here the probability is the prob of having 'pepper' knowing 'tex_mex' for instance
        if ingredient[0] in test_sample['ingredients']: #because the 0 elem contains the name of the ingredient and the 1 elem contains the probs to be or not to be in class C {
            score[cuisine] *= ingredient[1]
        else: 
            score[cuisine] *= (1-ingredient[1])
    score[cuisine] *= cuisine_probs[cuisine]

#return the cuisine the most probable for this ingredients
cuisine_more_prob = max(score.iterkeys(), key=(lamda key: score[key]))
