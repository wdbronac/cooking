#implement a prediction of the class with the naive bayes method


def train_naive_bayes(training_set, classes_total):
    '''training_set should be an np.array of this form : [ [[0, 0, 1, 0][1, 0, 0, 1]...][indian]


    '''


    #for every class C, compute the probability to have parameter x1, and x2, and x3...


    #then for every vector [ x1, x2, x3, x4], compute the score for each class, and label the vector with the most probable class.
