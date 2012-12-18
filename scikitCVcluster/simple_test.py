
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
    return x * cv


def simple_test():

    dview.push({'x':5})
    try:
        pred = dview.map(classify, range(10), block=True)
    except RemoteError as e:
        e.print_traceback()
        print e
        if e.engine_info:
            print "e-info: " + str(e.engine_info)
        if e.ename:
            print "e-name:" + str(e.ename)

    print pred