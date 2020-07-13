from random import seed
import numpy as np

from sklearn.svm import SVC
import matplotlib.pyplot as plt

# fix randomness - DO NOT CHANGE/REMOVE THIS
seed(1234)
np.random.seed(1234)

data = np.load("task1/task1_A.npz")
X, y = data["X"], data["y"]

def plotSVC(ax, clf, title):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    h = .02
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
    plt.ylabel('First Feature')
    plt.xlabel('Second Feature')
    plt.xticks([], [])
    plt.yticks([], [])
    plt.title(title)

fignum = 1
for kernel in ('linear', 'sigmoid','poly', 'rbf'):
    clf = SVC(kernel=kernel)
    clf.fit(X, y)
    fig, ax = plt.subplots()
    title = kernel.capitalize() + " Kernel - Accuracy: " + str(round(clf.score(X,y),2))
    plotSVC(ax, clf, title)
    fignum = fignum + 1
    plt.show()

def custom_plt(fignum):
    plt.figure(fignum, figsize=(4, 3))
    plt.clf()

    plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=20,
                facecolors='none', zorder=10, edgecolors='k')
    plt.scatter(X[:, 0], X[:, 1], c=y, zorder=10, cmap=plt.cm.Paired,
                edgecolors='k')

    plt.axis('tight')
    x_min = -3
    x_max = 3
    y_min = -3
    y_max = 3

    XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
    Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])

    Z = Z.reshape(XX.shape)
    plt.figure(fignum, figsize=(5, 4))
    plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)
    plt.contour(XX, colors=['r'], linestyles=['-'],
                levels=[0])

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.title(kernel.capitalize()+" Kernel - Accuracy: "+ str(clf.score(X,y)))
    plt.xticks(())
    plt.xlabel('First Feature')
    plt.yticks(())
    plt.ylabel('Second Feature')
    fignum = fignum + 1
