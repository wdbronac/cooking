import csv
import pandas as pd
from multiprocessing import Pool
import naive_bayes_classification as NB


number_cores = 3

train, valid = NB.load_data('../data/train.json', 1.0)
test, valid = NB.load_data('../data/test.json', 1.0)

#ici c est juste pour avoir des fichiers pas trop gros pour tester le parralelisme
#train, valid1 = NB.load_data('../data/train.json', 0.1)
#test1, test = NB.load_data('../data/train.json', 0.99)

total_probs_init = NB.init_total_probs(train, overwrite = False)
total_probs, cuisine_probs = NB.build_model(train, total_probs_init, overwrite = False)


tabfin = [['id', 'cuisine']]
def predict(array): #it takes in arguments a numpyarray
    tabfin = []
    counter = 0.0
    done = 0
    for sample in array:
        l = float(len(array))
        percent = (int)(100*((float)(counter)/l))
        counter+=1
        if (percent)%10 == 0: 
            if done == 0:
                print `percent`+'%'
                done = 1
        else: done = 0
        cuisine_more_prob = NB.predict_class(sample, total_probs, cuisine_probs)
        tabfin.append([sample['id'], cuisine_more_prob])
    return tabfin


#dividing the testing dictionary
l = len(test)
arguments = []
for i in range(number_cores):
    arguments += [test[i*l/number_cores:(i+1)*l/number_cores]] #dividing the list of the samples to predict

#for i in range(number_cores): 
 #   print arguments[i] 

##computing the class for each array of sample
p = Pool(number_cores)
results = (p.map(predict, arguments))

##merging the results
tot_results = []
for i in range(len(results)):
    tot_results += results[i]
tab_tot_fin = tabfin + tot_results

##telling if the results are coherent (only if test owns a column with the true results, this was to test my program)
#print 'Computing empirical risk on the testation set.'
#total = 0.0
#good = 0.0
#counter = 0.0
#done = 0
#for idx, sample in enumerate(test):
#    l = float(len(test))
#    percent = (int)(100*((float)(counter)/l))
#    counter+=1
#    if (percent)%10 == 0: 
#        if done == 0:
#            print `percent`+'%'
#            done = 1
#    else: done = 0
#    total += 1.0
#    if tab_tot_fin[idx+1][1] == sample['cuisine']: # The +1 is because we dont take into account the first row
#        good +=1.0
#print '100% \nRisk computed.'
#result = 1.0-(good/total)
#
#print result


my_df = pd.DataFrame(tab_tot_fin)
my_df.to_csv('submission.csv', index=False, header=False)
