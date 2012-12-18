from scikitCVcluster import scikitCVcluster
from sklearn import neighbors
from sklearn import datasets
import numpy as np

iris = datasets.load_iris()
cv = scikitCVcluster()
cc = neighbors.KNeighborsClassifier
preds, _ = cv.CV(cc, iris.data, iris.target)
print preds
print 'Accuracy: %.2f' % (np.sum(preds == iris.target) / (len(iris.target) * 1.))
