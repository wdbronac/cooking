import os.path
import json
import numpy as np
import pandas as pd

def load_data(path, proportion):  #proportion = 1: all training set is used
    json_data=open(path)
    data = json.load(json_data)

    #implement a prediction of the class with the naive bayes method


    #Divides between the training set and the validation set

    train = data[0:(int)(proportion*len(data))]
    #valid = data[1001:2000]
    valid = data[len(train)::]
    return train, valid

#--------------------------------------building the model--------------------------------------------

#1: find all the cuisines
#2: find all the ingredients
#3: build an "empty" total_probs dictionary
#4: fill this dictionary thanks to the naive Bayes method

#constructs an empty dictionary
def init_total_probs(train, overwrite = False):
    if(overwrite == False and  os.path.isfile('total_probs_init.npy')): #if there is already an initial model and we do not want to overwrite it
            print 'Loading the initial total probabilities matrix...'
            total_probs_init = np.load('total_probs_init.npy').item()
            print 'Matrix loaded.\n\n'
            return total_probs_init
    print 'Building an empty dictionary of all the cuisines and ingredients.'
    total_probs_init = dict() 
    sample = train[0]
    ingredient = sample['ingredients'][0]# for the initialization of the array
    total_probs_init[sample['cuisine']] = np.array([[ingredient, 0]])
    counter = 0
    done = 0
    for sample in train[0::]:
        percent = (int)(100*((float)(counter)/len(train)))
        counter+=1
        if (percent)%10 == 0: 
            if done == 0:
                print `percent`+'%'
                done = 1
        else: done = 0
        if sample['cuisine'] not in total_probs_init.keys():    #if  the cuisine is not present yet in the total_probs_init dict
            total_probs_init[sample['cuisine'] ] = total_probs_init[total_probs_init.keys()[0]]  # Adds the new cuisine in the total_probs_init keys
        for ingredient in sample['ingredients']: 
            if ingredient not in total_probs_init[total_probs_init.keys()[0]][0:, 0]: #if the ingredient is not in the list of ingredients of the first entry of the dict
                for cuisine in total_probs_init.keys(): #append it to the list of ingredients of every entry of the dictionary
                    total_probs_init[cuisine] = np.append(total_probs_init[cuisine],[[ingredient, 0]], axis = 0)
    print '100% \nEmpty dictionary built.\n'
    print 'Saving it...'
    np.save('total_probs_init.npy', total_probs_init)
    print 'Saved.\n\n'
    return total_probs_init



#Computes the matrix of the probabilities of the cuisine

def build_model(train, total_probs, overwrite = False):
    print 'Computing the matrix of p(C):'   #TODO: I can optimize it by melting it with the previous step and I should not need to redo it every time but anyways I will do it later
    nb_tot =len(train)
    cuisine_probs = dict()
    for sample in train: 
        if sample['cuisine'] not in cuisine_probs.keys():
            cuisine_probs[sample['cuisine']]= 1.0/nb_tot
        else: cuisine_probs[sample['cuisine'] ]+=1.0/nb_tot
    print 'Matrix computed.\n\n'

    if(overwrite == False and  os.path.isfile('total_probs.npy')): #if there is already a model and we do not want to overwrite it
            print 'Loading the total probabilities matrix of p(xi knowing C)...'
            total_probs= np.load('total_probs.npy').item()
            print 'Matrix loaded.\n\n'
            return total_probs, cuisine_probs
    print 'Computing the matrix of p(xi knowing C):'  #TODO: save the model so that it doesn't need to be recomputed after
    counter = 0
    done = 0
    for cuisine in total_probs.keys(): 
        percent = (int)(100*((float)(counter)/len(total_probs.keys())))
        counter+=1
        if (percent)%10 == 0: 
            if done == 0:
                print `percent`+'%'
                done = 1
        else: done = 0
        for idx, ing_prob in enumerate(total_probs[cuisine]):
            total = 0.0
            found = 0.0
            for sample in train: 
                if cuisine == sample['cuisine']:
                    total +=1.0
                    if ing_prob[0] in sample['ingredients']:
                        found +=1.0
            total_probs[cuisine][idx,1] = (float)(found)/(float)(total)
    print 'Matrix computed.'
    print 'Saving it...'
    np.save('total_probs.npy', total_probs)
    print 'Saved.\n\n'
    return total_probs, cuisine_probs
#then for every vector [ x1, x2, x3, x4], compute the score for each class, and label the vector with the most probable class.

#-------------------------------------------predicting the class---------------------------------------------------------


def predict_class(sample, total_probs, cuisine_probs):
    #echantillon a tester : {'id':1324134, 'ingredients': [baking powder, requin]}
    #score has to be of this form:  score = {'tex_mex': 1, 'chines': 1} ----TODO: create it of this form---------
    
    #initiallize the score dictionary
    score = dict()
    for cuisine in total_probs.keys():
        score[cuisine]=1.0
    for cuisine in total_probs.keys(): 
        for ingredient in total_probs[cuisine]:  #total_probs has to be of the form {'tex mex':[['tomato sauce ',  0.8], ['pepper',  0.6] ], 'chinese':[['tomato sauce ', 0.3], ['pepper',  0.5] ]} here the probability is the prob of having 'pepper' knowing 'tex_mex' for instance
            if ingredient[0] in sample['ingredients']: #because the 0 elem contains the name of the ingredient and the 1 elem contains the probs to be or not to be in class C {
                score[cuisine] *= (float)(ingredient[1])
            else: 
                score[cuisine] *= (1.0-(float)(ingredient[1]))
        score[cuisine] *= cuisine_probs[cuisine]

    #return the cuisine the most probable for this ingredients
    cuisine_more_prob = max(score.iterkeys(), key=(lambda key: score[key]))
    return cuisine_more_prob

def test(valid, total_probs, cuisine_probs):
    print 'Computing empirical risk on the validation set.'
    total = 0.0
    good = 0.0
    counter = 0.0
    done = 0
    for sample in valid:
        l = float(len(valid))
        percent = (int)(100*((float)(counter)/l))
        counter+=1
        if (percent)%10 == 0: 
            if done == 0:
                print `percent`+'%'
                done = 1
        else: done = 0
        total += 1.0
        cuisine_more_prob =  predict_class(sample, total_probs, cuisine_probs)
        if str(cuisine_more_prob) == sample['cuisine']:
            good +=1.0
    result = good/total
    print 'The empirical risk is '+ `result`+'\n\n'
    return result




if  __name__ == '__main__':
    #launch the program with splitting the training set into test set and validation set, and computing the risk
    train, valid = load_data('../data/train.json', 0.9)
    total_probs_init = init_total_probs(train, overwrite = True)
    total_probs, cuisine_probs = build_model(train, total_probs_init, overwrite = True)
    result = test(valid, total_probs, cuisine_probs)
    print result
