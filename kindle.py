'''
Copyright 2010 Kimmo Parviainen-Jalanko <k+kindle@77.fi>. All rights
reserved.
''' 

import simplejson as json
import ebook
from debug import LOG
from ConfigParser import ConfigParser

# Set this to point to kindle, default for most modern Linuxes below
#KINDLEDIR = "/media/Kindle/"
#KINDLEDIR = "/home/kparviainen/py/kindle/test2/"
cp = ConfigParser()
cp.read('kiehinen.conf')

KINDLEDIR = cp.get('system','kindle_path')

BOOKPATH = KINDLEDIR + "documents/"
JSONFILE = KINDLEDIR + "system/collections.json"

KINDLE_INTERNAL_PATH = "/mnt/us/documents/"
COLLNAME = "%s@en-US" 

# JSON helper functions
def load_data():
    return json.loads(open(JSONFILE, 'r').read())

def save_data(kjd):
    open(JSONFILE, 'w').write(json.dumps(kjd))

# Kindle access
def get_books(progress_func=lambda: None):
    import glob
    ret = {}
    files =  glob.glob("%s/*" % BOOKPATH)
    tot = len(files)
    for c,fn in enumerate(files):
        progress_func(c+1,tot,fn)
        LOG(3,"\n - Processing file %s" % fn)
        key = make_hash(fn.replace(BOOKPATH, KINDLE_INTERNAL_PATH))
        val = ebook.Book(fn)
        if val:
            ret[key] = val
    return ret

# Collection functions
def update_ts(collection):
    from time import time
    collection['lastAccess'] = int(time()*1000)

def add_collection(kjd, collection):
    LOG(3,"Adding collection %s" % collection)
    time_ms = int(time.time()*1000)    
    new_item = {}
    cn = COLLNAME % collection
    if not ((cn) in kjd):
        kjd[cn] = {'items':[],'lastAccess':time_ms}
    else:
        LOG(1,"Collection %s already exists" % collection)
        update_ts(kjd[cn])

def delete_collection(kjd, collection):
    cn = COLLNAME % collection
    if cn in kjd:
        del kjd[cn]    
    else:
        LOG(1,'Collection %s does not exist' % collection)

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
        LOG(1,"Error. collection %s does not exist" % collection)
    else:
        kjd[cn]['items'].append(make_hash(name))
        update_ts(kjd[cn])

