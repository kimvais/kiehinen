'''
Copyright 2010 Kimmo Parviainen-Jalanko <k+kindle@77.fi>. All rights
reserved.
''' 

import simplejson as json
from debug import LOG
from struct import pack,unpack,calcsize

COLLNAME = "%s@en-US" 
#LOCALPATH = "/media/Kindle/documents"
LOCALPATH = "/home/kparviainen/py/kindle/testdata"
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
    import glob
    files =  glob.glob("%s/*" % LOCALPATH)
    for fn in files:
        LOG(3,"\n - Processing file %s" % fn)
        read_book(fn)
    filenames = [x.replace(LOCALPATH, KINDLEPATH) for x in files]
    return dict([(make_hash(x),x) for x in filenames])

def read_book(fn):
    d = open(fn).read()
    encodings = {
            1252: 'cp1252'
            }
    supported_types = ('BOOKMOBI','TEXtREAd')
    ptype = d[60:68]
    if ptype not in supported_types:
        LOG(1,"Unsupported file type %s" % (ptype))
        return None

    db = read_palmdb(d) 
    rec0 = db.records[0].toByteArray(0)[1]
    
    #LOG(5,repr(rec0))
    if ptype == 'BOOKMOBI':
        LOG(3,"This is a MOBI book")
        id, hlen, mobitype, encoding, uid, nameoffs, namelen = unpack(
                MOBIHEADER_FMT, rec0[16:16+calcsize(MOBIHEADER_FMT)])
        LOG(3,
        "id: %s, hlen %d, type %d, encoding %d, uid %d, offset %d, len %d" %
        (id, hlen, mobitype, encoding, uid, nameoffs, namelen))

        # Get and decode the book name
        name = rec0[nameoffs:nameoffs+namelen].decode(encodings[encoding])

        LOG(3,"Book name: %s" % name)
        if id != 'MOBI':
            LOG(0,"Mobi header missing!")
        if (0x40 & unpack(">I",rec0[128:132])[0]): # check for EXTH
            parse_exth(rec0,hlen+16)

    elif ptype == 'TEXtREAd':
        LOG(2,"This is an older MOBI book")

            
EXTH_FMT = ">4x2I"
'''4x = "EXTH", I = hlen, I = record count'''

EXTH_RECORD_TYPES = {
        1 : 'drm server id',
        2 : 'drm commerce id',
        3 : 'drm ebookbase book id',
        100 : 'author',
        101 : 'publisher',
        102 : 'imprint',
        103 : 'description',
        104 : 'isbn',
        105 : 'subject',
        106 : 'publishingdate',
        107 : 'review',
        108 : 'contributor',
        109 : 'rights',
        110 : 'subjectcode',
        111 : 'type',
        112 : 'source',
        113 : 'asin',
        114 : 'version number',
        115 : 'sample',
        116 : 'start reading',
        118 : 'retail price',
        119 : 'retail price currency',
        201 : 'cover offset',
        202 : 'thumbnail offset',
        203 : 'has fake cover',
        208 : 'watermark',
        209 : 'tamper proof keys',
        401 : 'clipping limit',
        402 : 'publisher limit',
        404 : 'ttsflag',
        502 : 'cde type',
        503 : 'updated title'
        }

def parse_exth(data,pos):
    ret = {}
    n = 0
    if (pos != data.find('EXTH')):
        LOG(0,"EXTH header not found where it should be @%d" % pos)
        return None
    else:
        end = pos+calcsize(EXTH_FMT)
        (hlen, count) = unpack(EXTH_FMT, data[pos:end])
        LOG(3,"pos: %d, EXTH header len: %d, record count: %d" % (
            pos, hlen, count ))
        pos = end
        while n < count:
            end = pos+calcsize(">2I")
            t,l = unpack(">2I",data[pos:end])
            v = data[end:pos+l]
            if l-8 == 4:
                v = unpack(">I",v)[0]
            if t in EXTH_RECORD_TYPES:
                LOG(2,"EXTH record '%s' @%d+%d: '%s'" % (
                    EXTH_RECORD_TYPES[t], pos, l-8, v))
                ret[t] = v
            else:
                LOG(3,"Found an unknown EXTH record type %d @%d+%d: '%s'" %
                        (t,pos,l-8,repr(v)))
            pos +=l
            n += 1
    

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

