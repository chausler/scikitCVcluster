scikitCVcluster
================

You can use this module to perform cross validation in parralel using Ipython.parallel. Hooray for faster classifier training!

It is designed to work with scikit_learn style classifiers that have a .fit and .predict method
also, it requires that an ipython controller and engines are running. the easiest way to do this is to install ipython and then run
ipcluster start --n=1

increase the value of n to start more engines
