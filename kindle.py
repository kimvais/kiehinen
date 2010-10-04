'''
Copyright 2010 Kimmo Parviainen-Jalanko <k+kindle@77.fi>. All rights
reserved.
''' 

import simplejson as json
import glob
import ebook
from debug import LOG
from time import time
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
    try:
        return json.load(open(JSONFILE, 'r'))
    except IOError:
        LOG(2,"File %s not found" % JSONFILE)
        return dict()

def save_data(kjd):
    open(JSONFILE, 'w').write(json.dumps(kjd))

# Kindle access
def get_books(progress_func=lambda: None):
    ret = {}
    files =  glob.glob("%s/*" % BOOKPATH)
    for c,fn in enumerate(files):
        progress_func(c)
        LOG(3,"\n - Processing file #%d: %s" % (c,fn))
        key = make_hash(fn.replace(BOOKPATH, KINDLE_INTERNAL_PATH))
        val = ebook.Book(fn)
        if val.is_a_book:
            ret[key] = val
    return ret

def get_bookcount():
    return len(glob.glob("%s/*" % BOOKPATH))

# Collection functions
def update_ts(collection):
    collection['lastAccess'] = int(time()*1000)

def add_collection(kjd, collection):
    time_ms = int(time()*1000)    
    new_item = {}
    cn = COLLNAME % collection
    LOG(3,"Adding collection %s" % cn)
    if not ((cn) in kjd):
        kjd[cn] = {'items':[],'lastAccess':time_ms}
    else:
        LOG(1,"Collection %s already exists" % collection)
        update_ts(kjd[cn])

def delete_collection(kjd, collection):
    cn = COLLNAME % collection
    LOG(3,"Deleting collection %s" % cn)
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

def add_item(kjd, collection, hash):
    cn = COLLNAME % collection
    if not ((cn) in kjd):
        LOG(1,"Error. collection %s does not exist" % collection)
    else:
        if hash in kjd[cn]['items']:
            LOG(1,"%s was already in %s" % (hash,cn))
        else:
            kjd[cn]['items'].append(hash)
            update_ts(kjd[cn])

def remove_item(kjd, collection, hash):
    cn = COLLNAME % collection
    if not ((cn) in kjd):
        LOG(1,"Error. collection %s does not exist" % collection)
    else:
        if hash not in kjd[cn]['items']:
            return
        else:
            kjd[cn]['items'].remove(hash)
            update_ts(kjd[cn])

def get_books_in_collection(kjd, collection):
    return kjd[COLLNAME % collection]['items']
