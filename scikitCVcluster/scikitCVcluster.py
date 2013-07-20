"""
    Handles cross validation training of a classifier in parallel
    using Ipython.parallel
    requires libraries sklearn, numpy and Ipython
    @author: Chris Hausler
"""

from sklearn.cross_validation import KFold
import numpy as np
try:
    from IPython.parallel import Client
    from IPython.parallel.error import RemoteError
    from IPython.parallel.util import interactive
except:
    Client = None
    print 'Failed to find IPython.parallel - No parallel processing available'


print 'hooraz' if Client else 'blag'
rc = Client()
dview = rc[:]
print '%d engines found' % len(rc.ids)


@interactive
def classify(cv):
    """
    This method initialises the classifier and trains it on  the training data
    @return: prediction from the test data and the classifier coefficients 
        if required
    """
    train = cv[0]
    test = cv[1]
    regr = clf(**clf_args)
    regr.fit(X[train], y[train], **clf_fit_args)
    coef = None
    if return_coefs:
        try:
            coef = regr.coef_
        except:
            pass
    pred = regr.predict(X[test], **clf_pred_args)
    return (pred, coef)


def CV(clf, X, y, folds=5, shuffle=True, clf_args={}, clf_fit_args={},
       clf_pred_args={}, return_coefs=False):
    """
    @param clf: the classifier to use, must have methods fit and predict
    @param X: the training data. [samples, dimensions]
    @param y: the target data. [targets]
    @param folds: how many folds to use in the cross validation
    @param shuffle: whether or not to shuffle the samples for xval
    @param clf_args: arguments for initialising the classifier
    @param clf_fit_args: arguments for training the classifier
    @param clf_pred_args: arguments for predicting with the classifier
    @param return_coefs: bool, whether or not to return classifier coefficients
        the classifier must have the attribute coef_ for this
    @return: numpy arrays of the predictions and coefficients
    """
    cv = KFold(len(X), k=folds, indices=True, shuffle=shuffle)
    dview.push({'X': X, 'y': y, 'clf': clf, 'clf_args': clf_args,
                     'clf_fit_args': clf_fit_args, 'clf_pred_args': clf_pred_args,
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
