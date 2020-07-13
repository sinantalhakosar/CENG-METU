import random
random.seed(1234)  # fix randomness

def normalize_data(somedataset):
    returnlist = list()
    for line in somedataset:
        somelist = [float(x) for x in line[0].split(",")[:-1]]
        somelist.append(line[0].split(",")[-1])
        returnlist.append(somelist)
    return returnlist

def load_dataset(somefilename):
    dataset = list()
    with open(somefilename, 'r') as file:
        dataset = [[line.strip()] for line in file]
    return normalize_data(dataset)

def euclidean_distance(record_1, record_2):
    distance = .0
    for i in range(len(record_1)-1):
        distance += (record_1[i] - record_2[i])**2
    return distance**(1/2)


def classification(k,train_dataset, test_row):
    distances = []
    for train_row in train_dataset:
        dist = euclidean_distance(test_row,train_row)
        distances.append((train_row,dist))
    distances.sort(key=lambda x: x[1])
    neighbours = []
    for i in range(k):
        neighbours.append(distances[i][0][-1])
    #output_values = [row[-1] for row in neigbours]
    prediction = max(set(neighbours),key=neighbours.count)
    return prediction


def cvs(train_set, n_folds):
    set_split = []
    set_copy = list(train_set)
    fold_size = int(len(train_set)/n_folds)
    for _ in range(n_folds):
        fold = []
        while len(fold) < fold_size:
            index = random.randrange(len(set_copy))
            fold.append(set_copy.pop(index))
        set_split.append(fold)
    return set_split

def calculate_accuracy(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual))*100.

def alg_eval(k,dataset, n_folds):
    folds = cvs(dataset,n_folds)
    scores = []
    for fold in folds:
        train_set = list(folds)
        train_set.remove(fold)
        train_set = sum(train_set,[])
        scores.append(kNN(k,train_set,fold))
    return scores



def kNN(k, train_set, test_set):
    """
    the unweighted k-NN algorithm using Euclidean distance as the metric

    :param k: the k value, i.e, how many neighbors to consider
    :param train_set: training set, a list of lists where each nested list is a training instance
    :param test_set: test set, a list of lists where each nested list is a test instance
    :return: percent accuracy for the test set, e.g., 78.42
    """
    predictions = []
    fold = list(test_set)
    #print(len(test_set))
    for row in test_set:
        row_copy = list(row)
        row_copy[-1] = None
        #fold.append(row_copy)
    for i,test in enumerate(fold):
        prediction = classification(k,train_set,test)
       # print(i)
        predictions.append(prediction)
    actual = [row[-1] for row in test_set]
    return_accuracy = calculate_accuracy(actual, predictions)
    #print("k: {} | test accuracy: {}".format(k,return_accuracy))
    return return_accuracy
    


def find_best_k(train_set, test_set, num_folds):
    """
    finds the best k value by using K-fold cross validation. Try at least 10 different k values. Possible choices
    can be: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19. Besides the return value, as a side effect, print each k value and
    the corresponding validation accuracy to the screen as a tuple. As an example,
    (1, 78.65)
    (3, 79.12)
    ...
    (19, 76.99)

    :param train_set: training set, a list of lists where each nested list is a training instance
    :param test_set: test set, a list of lists where each nested list is a test instance
    :param num_folds: the K value in K-fold cross validation
    :return: a tuple, best k value and percent accuracy for the test set using the best k value, e.g., (3, 80.06)
    """
    k_list = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    k_values = []
    for k in k_list:
        scores = alg_eval(k,train_set, num_folds)
        k_values.append((k,sum(scores)/float(len(scores))))
        print((k,sum(scores)/float(len(scores))))
    best_score_knn = kNN(max(k_values,key=lambda x:x[1])[0],train_set,test_set)
    return max(k_values,key=lambda x:x[1])[0],best_score_knn


# train_dataset = load_dataset('task1_train.txt')
# test_dataset = load_dataset('task1_test.txt')


# k = 3
# test_accuracy = kNN(k,train_dataset,test_dataset)
# print("k: {} | test accuracy: {}".format(k,test_accuracy))

# num_folds = 5
# best_k, test_accuracy = find_best_k(train_dataset,test_dataset,num_folds)
# print("best k is: {} | test accuracy: {}".format(best_k,test_accuracy))

