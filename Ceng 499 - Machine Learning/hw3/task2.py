from random import seed

# fix randomness - DO NOT CHANGE/REMOVE THIS
seed(1234)

def load_dataset(somefilename):
    dataset = list()
    returnlist = list()
    with open(somefilename, 'r') as file:
        dataset = [[line.strip()] for line in file]
    for line in dataset:
        feature_list = [float(x) for x in line[0].split(",")]
        returnlist.append((feature_list))
    return returnlist

def dataset_normalizer(somedataset):
    min_max = list()
    for i in range(len(somedataset[0])):
        val = [row[i] for row in somedataset]
        min_max.append([min(val), max(val)])
    for row in somedataset:
        for i in range(len(row)-1):
            row[i] = (row[i] - min_max[i][0]) / (min_max[i][1] - min_max[i][0])

def guess(row, coefficients):
    zero_coeff = coefficients[0]
    for i in range(len(row)-1):
        zero_coeff += coefficients[i + 1] * row[i]
    return zero_coeff
 
def s_gradient_descent_coeff(train, learning_rate, num_epochs):
    coef = [0.0 for i in range(len(train[0]))]
    for epoch in range(num_epochs):
        for row in train:
            error = (guess(row, coef) - row[-1])*2
            coef[0] -= learning_rate * error
            for i in range(len(row)-1):
                coef[i + 1] -= learning_rate * error * row[i]
    return coef

def s_gradient_descent_reg(train, test, learning_rate, num_epochs):
    predictions = list()
    coef = s_gradient_descent_coeff(train, learning_rate, num_epochs)
    for row in test:
        predictions.append(guess(row, coef))
    return predictions

def root_mean_square(actual, predicted):
    error = 0.0
    for i in range(len(actual)):
        error += ((predicted[i] - actual[i]) ** 2)
    mean_error = error / float(len(actual))
    return mean_error**(1/2)

def linear_regression(train_path, test_path, num_epochs, learning_rate):
    """
    Performs multivariate regression
    :param train_path: path of the training set, a string
    :param test_path: path of the test set, a string
    :param num_epochs: the number of epochs, an integer
    :param learning_rate: learning rate, a float
    :return: RMSE (Root Mean Square Error) of the test set
    """
    train_set = load_dataset(train_path)
    test_set = load_dataset(test_path)
    dataset_normalizer(train_set)
    dataset_normalizer(test_set)
    scores = list()
    test_copy = list(test_set)
    for row in test_set:
        row_copy = list(row)
        row_copy[-1] = None
    predicted = s_gradient_descent_reg(train_set, test_set, learning_rate, num_epochs)
    actual = [row[-1] for row in test_copy]
    rms = root_mean_square(actual, predicted)
    scores.append(rms)
    return sum(scores)/float(len(scores))

# rmse = linear_regression('train_set.txt', 'test_set.txt', 1000, 0.001)
# print('RMSE = {} for {}'.format(rmse,'test_set.txt'))