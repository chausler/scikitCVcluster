import sys
sys.path.append('..')
sys.path = ['/home/chris/programs/aa_scikits/scikit-learn'] + sys.path

from sklearn.cross_validation import KFold
import numpy as np
from sklearn.neighbors import RadiusNeighborsClassifier
try:
    from IPython.parallel import Client
    from IPython.parallel.error import RemoteError
except:
    Client = None
    print 'Failed to find IPython.parallel - No parallel processing available'


def classify(cv):
    train = cv[0]
    test = cv[1]
    gg = X[train]
    regr = clf(**clf_args)
    regr.fit(X[train], y[train])
    coef = None
    if return_coefs:
        try:
            coef = regr.coef_
        except:
            pass

    pred = regr.predict(X[test])
    return (pred, coef)
        #return (train, test)


class scikitCVcluster():

    def __init__(self):
        print 'hooraz' if Client else 'blag'
        rc = Client()
        self.dview = rc[:]
        self.lview = rc.load_balanced_view()
        self.lview.block = True
        if Client:
            print '%d engines found' % len(rc.ids)

    def CV(self, clf, X, y, folds=5, clf_args={}, clf_fit_args={},
           clf_pred_args={}, return_coefs=False):
        print clf, X, y, folds
        cv = KFold(len(X), k=folds, indices=True)#, shuffle=True)
        self.dview.push({'X': X, 'y': y, 'clf': clf, 'clf_args': clf_args,
                         'fit_args': clf_fit_args, 'pred_args': clf_pred_args,
                         'return_coefs' : return_coefs})
        pred = []
        print self.dview['clf']
        print self.dview['X']
        try:
            pred = self.dview.map(classify, cv)
        except RemoteError as e:
            e.print_traceback()
            print e
            if e.engine_info:
                print "e-info: " + str(e.engine_info)
            if e.ename:
                print "e-name:" + str(e.ename)

        preds = []
        coefs = []
        for (p, c) in pred:
            preds += p.tolist()
            coefs += [c]

        return np.array(preds), np.array(coefs)

if __name__ == "__main__":     
    from sklearn import neighbors
    from sklearn import datasets
    iris = datasets.load_iris()
    cv = scikitCVcluster()
    clf = neighbors.KNeighborsClassifier
    preds, _ = cv.CV(clf, iris.data, iris.target)
    print 'Accuracy: %.2f' % (np.sum(preds == iris.target) / (len(iris.target) * 1.))
