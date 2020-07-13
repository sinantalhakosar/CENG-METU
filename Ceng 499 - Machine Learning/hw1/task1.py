import sys

import pickle
import gzip
import numpy as np
np.random.seed(1234)

with gzip.open(sys.argv[1], 'rb') as f:
    X, y = pickle.load(f,encoding ='latin1')
with gzip.open(sys.argv[2], 'rb') as f:
    tX, ty = pickle.load(f,encoding ='latin1')
class Neural_Network(object):
    def __init__(self,n_in,n_hidden,n_out):
        self.inputSize = n_in
        self.outputSize = n_out
        self.hiddenSize = n_hidden
        self.W1 = np.random.randn(int(self.hiddenSize), int(self.inputSize))*0.01
        self.b1 = np.zeros((int(self.hiddenSize), 1))
        self.W2 = np.random.randn(int(self.outputSize), int(self.hiddenSize))*0.01
        self.b2 = np.zeros((int(self.outputSize), 1))

    def sigmoid(self, s):
        return 1/(1+np.exp(-s))
    
    def hiddenActivation(self,s):
        return np.where((s<=-1), 0, (np.where(s<1,(s+1)/2,1)))
    
    def hiddenActivationDerivative(self,s,dx):
        return dx*(np.where((s<=-1), 0, (np.where(s<1,0.5,0))))

    def forward(self, X):
        self.Z1 = self.W1.dot(X.T) + self.b1
        self.A1 = self.hiddenActivation(self.Z1)
        self.Z2 = self.W2.dot(self.A1) + self.b2
        self.A2 = self.sigmoid(self.Z2)
        return self.A2

    def sigmoidPrime(self, s,dx):
        return dx * (s * (1 - s))

    def backward(self, X, y,o):
        m = X.shape[0]
        self.dZ2 = self.sigmoidPrime(self.A2,-2 * (np.subtract(y,self.A2)))
        self.dW2 = (1/m) * np.dot(self.dZ2, self.A1.T)
        self.db2 = (1 / m) * np.sum(self.dZ2, axis=1, keepdims=True)

        self.dZ1 = self.hiddenActivationDerivative(self.A1,np.dot(self.W2.T, self.dZ2))
        self.dW1 = (1 / m) * np.dot(self.dZ1, X)
        self.db1 = (1 / m) * np.sum(self.dZ1, axis=1, keepdims=True)

    def train(self, X, Y, epochs=int(sys.argv[3]), learning_rate=1):
        m = X.shape[0]
        for e in range(epochs):
            o = self.forward(X)
            loss = str(np.mean(np.square(Y - o)))
            self.backward(X, Y,o)

            self.W1 -= learning_rate * self.dW1
            self.b1 -= learning_rate * self.db1
            self.W2 -= learning_rate * self.dW2
            self.b2 -= learning_rate * self.db2

            if e % epochs == 0 or e == epochs-1 or True:
                print("Loss at epoch ",  e+1, " = ", loss)
    def predict(self, X):
        self.forward(X)
        return np.round(self.A2).astype(np.int)

def show_predictions(model, X, Y):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))
    X_temp = np.c_[xx.flatten(), yy.flatten()]
    Z = model.predict(X_temp)
    
nn = Neural_Network(np.size(X,1),((np.size(X,1)+1)/2)+1,1)
nn.train(X, y)

show_predictions(nn, tX, ty)
nn_predictions = nn.predict(tX)
print("Accuracy : ", np.sum(nn_predictions == ty) / ty.shape[0])

