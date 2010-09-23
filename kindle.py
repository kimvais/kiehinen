'''
Copyright 2010 Kimmo Parviainen-Jalanko <k+kindle@77.fi>. All rights
reserved.
''' 

import simplejson as json
from debug import LOG
from struct import pack,unpack,calcsize

COLLNAME = "%s@en-US" 
#LOCALPATH = "/media/Kindle/documents"
LOCALPATH = "/home/kparviainen/py/kindle/test2"
KINDLEPATH = "/mnt/us/documents"
#JSONFILE = "/media/Kindle/system/collections.json"
JSONFILE = "/home/kparviainen/py/kindle/test2/collections.json"
MOBIHEADER_FMT = ">4s4I48x2I"
'''
http://wiki.mobileread.com/wiki/MOBI#Format

4s - MOBI
I - hlen
I - type
I - encoding
I - UID
48x - (I+40x+I) generator version + reserved + 1st non-book index
I - full name offset
I - full name length
I - locale
32x - 4I + 16x - uninteresting stuff
I - EXTH flags
32x - unknown
16x - 4I drm stuff
'''
EXTH_FMT = ">4x2I"
'''4x = "EXTH", I = hlen, I = record count'''


# JSON helper functions
def load_data():
    return json.loads(open(JSONFILE, 'r').read())

def save_data(kjd):
    open(JSONFILE, 'w').write(json.dumps(kjd))

# Kindle access
def read_palmdb(data):
    from PalmDB import PalmDatabase
    db = PalmDatabase.PalmDatabase()
    db.fromByteArray(data)
    return db

def get_books():
    supported_types = ('BOOKMOBI','TEXtREAd')
    import glob
    files =  glob.glob("%s/*" % LOCALPATH)
    for fn in files:
        d = open(fn).read()
        type = d[60:68]
        if type not in supported_types:
            LOG(1,"Unsupported file type %s for file %s" % (type,fn))
            continue
        db = read_palmdb(d) 
        rec0 = db.records[0].toByteArray(0)[1]
        LOG(5,repr(rec0))
        if type == 'BOOKMOBI':
            LOG(3,"%s is a MOBI book" % fn)
            id, hlen, mobitype, encoding, uid, nameoffs, namelen = unpack(
                    MOBIHEADER_FMT, rec0[16:16+calcsize(MOBIHEADER_FMT)])
            LOG(3,
            "id: %s, hlen %d, type %d, encoding %d, uid %d, offset %d, len %d" %
            (id, hlen, mobitype, encoding, uid, nameoffs, namelen))
            LOG(3,"Book name: %s" % rec0[nameoffs:nameoffs+namelen])
            if id != 'MOBI':
                LOG(0,"Mobi header missing!")
            if (0x40 & unpack(">I",rec0[128:132])[0]): # check for EXTH
                pass
                
        elif type == 'TEXtREAd':
            LOG(2,"%s is an older MOBI book" % fn)
        else:
            LOG(1,"%s is of unsupported format :(" % fn)

    filenames = [x.replace(LOCALPATH, KINDLEPATH) for x in files]
    return dict([(make_hash(x),x) for x in filenames])

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

