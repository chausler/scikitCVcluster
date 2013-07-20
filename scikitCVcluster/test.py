from scikitCVcluster import CV
from sklearn import neighbors
from sklearn import datasets
import numpy as np


iris = datasets.load_iris()
cc = neighbors.KNeighborsClassifier
preds, _ = CV(cc, iris.data, iris.target)
print preds
print 'Accuracy: %.2f' % (np.sum(preds == iris.target)
                          / (len(iris.target) * 1.))
