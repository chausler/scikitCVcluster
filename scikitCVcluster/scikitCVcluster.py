import sys
sys.path.append('..')
#sys.path = ['/home/chris/programs/aa_scikits/scikit-learn'] + sys.path
from sklearn.cross_validation import KFold
import numpy as np
try:
    from IPython.parallel import Client
    from IPython.parallel.error import RemoteError
except:
    Client = None
    print 'Failed to find IPython.parallel - No parallel processing available'



print 'hooraz' if Client else 'blag'
rc = Client()
dview = rc[:]
print '%d engines found' % len(rc.ids)


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


def CV(clf, X, y, folds=5, clf_args={}, clf_fit_args={},
       clf_pred_args={}, return_coefs=False):

    cv = KFold(len(X), k=folds, indices=True)#, shuffle=True)
    dview.push({'X': X, 'y': y, 'clf': clf, 'clf_args': clf_args,
                     'fit_args': clf_fit_args, 'pred_args': clf_pred_args,
                     'return_coefs': return_coefs})
    pred = []
    try:
        pred = dview.map(classify, cv)
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
