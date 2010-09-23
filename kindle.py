'''
Copyright 2010 Kimmo Parviainen-Jalanko <k+kindle@77.fi>. All rights
reserved.
''' 

import simplejson as json

COLLNAME = "%s@en-US" 
#LOCALPATH = "/media/Kindle/documents"
LOCALPATH = "/home/kparviainen/py/kindle/testdata"
KINDLEPATH = "/mnt/us/documents"
JSONFILE = "/media/Kindle/system/kjd.json"
COLLFILE = "/media/Kindle/system/collections.json"

# JSON helper functions
def load_data():
    return json.loads(open(COLLFILE, 'r').read())

def save_data(kjd):
    open(COLLFILE, 'w').write(json.dumps(kjd))

# Kindle access
def read_palmdb(data):
    from PalmDB import PalmDatabase
    db = PalmDatabase.PalmDatabase()
    db.fromByteArray(data)
    return db

def get_books():
    import glob
    files =  glob.glob("%s/*" % LOCALPATH)
    for fn in files:
        d = open(fn).read()
        type = d[60:68]
        if type == 'BOOKMOBI':
            print "%s is a MOBI book" % fn
            db = read_palmdb(d) 
            mobiheader = db.records[0].toByteArray(0)[1][:242]
        elif type == 'TEXtREAd':
            print "%s is an older MOBI book" % fn
        else:
            print "%s is of unsupported format :(" % fn

    filenames = [x.replace(LOCALPATH, KINDLEPATH) for x in files]
    return dict([(make_hash(x),x) for x in filenames])

# Collection functions
def update_ts(collection):
    from time import time
    collection['lastAccess'] = int(time()*1000)

def add_collection(kjd, collection):
    print "Adding collection %s" % collection
    time_ms = int(time.time()*1000)    
    new_item = {}
    cn = COLLNAME % collection
    if not ((cn) in kjd):
        kjd[cn] = {'items':[],'lastAccess':time_ms}
    else:
        print "Collection %s already exists" % collection
        update_ts(kjd[cn])

def delete_collection(kjd, collection):
    cn = COLLNAME % collection
    if cn in kjd:
        del kjd[cn]    
    else:
        print 'Collection %s does not exist' % collection

# Item functions
def make_hash(s):
    '''
    Calculates a SHA1 hash, prepended with * from filename prefixed 
    by the path to documents folder on Kindle 2.x and 3.0.x
    '''
    from hashlib import sha1
    return "*%s" % sha1(s).hexdigest()

def add_item(kjd, collection, name):
    cn = COLLNAME % collection
    if not ((cn) in kjd):
        print "Error. collection %s does not exist" % collection
    else:
        kjd[cn]['items'].append(make_hash(name))
        update_ts(kjd[cn])

