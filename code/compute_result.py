import naive_bayes_classification as NB
import export_json_csv as exp



train, valid = NB.load_data('../data/train.json', 1.0)
total_probs_init = NB.init_total_probs(train, overwrite = False)
total_probs, cuisine_probs = NB.build_model(train, total_probs_init, overwrite = False)

test, valid = NB.load_data('../data/train.json', 1.0)

tabfin = [['id', 'cuisine']]
for sample in test: 
    cuisine_more_prob = NB.predict_class(sample, total_probs, cuisine_probs)
    tabfin.append([sample['id'], cuisine_more_prob)

exp.ecrire_csv("submission1.csv"



