from debug import LOG
from struct import unpack,pack,calcsize

MOBI_HDR_FIELDS = (
    ("id",16,"4s"),
    ("header_len",20,"I"),
    ("mobi_type",24,"I"),
    ("encoding",28,"I"),
    ("UID",32,"I"),
    ("generator_version",36,"I"),
    ("reserved",40,"40s"),
    ("first_nonbook_idx",80,"I"),
    ("full_name_offs",84,"I"),
    ("full_name_len",88,"I"),
    ("locale",92,"I"),
    ("input_lang",96,"I"),
    ("output_lang",100,"I"),
    ("format_version",104,"I"),
    ("first_image_idx",108,"I"),
    ("unknown",112,"16s"),
    ("exth_flags",128,"I"),
    ("unknown2",132,"36s"),
    ("drm_offs",168,"I"),
    ("drm_count",172,"I"),
    ("drm_size",174,"I"),
    ("drm_flags",176,"I"),
    ("extra_data_flags",242,"H")
    )

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

def parse_palmdb(data):
    from PalmDB import PalmDatabase
    db = PalmDatabase.PalmDatabase()
    db.fromByteArray(data)
    return db

def read(fn):
    d = open(fn).read()
    encodings = {
            1252: 'cp1252',
            65001: 'utf-8'
            }
    supported_types = ('BOOKMOBI','TEXtREAd')
    ptype = d[60:68]
    if ptype not in supported_types:
        LOG(1,"Unsupported file type %s" % (ptype))
        return None

    db = parse_palmdb(d) 
    rec0 = db.records[0].toByteArray(0)[1]
    
    #LOG(5,repr(rec0))
    if ptype == 'BOOKMOBI':
        LOG(3,"This is a MOBI book")
        mobiheader = {}
        for field,pos,fmt in MOBI_HDR_FIELDS:
            end = pos + calcsize(fmt)
            if (end > len(rec0) or 
                ("header_len" in mobiheader 
                    and end > mobiheader["header_len"])):
                    continue
            LOG(3,"field: %s, fmt: %s, @ [%d:%d], data: %s" % (
                field, fmt, pos, end, repr(rec0[pos:end])))
            (mobiheader[field],) = unpack(">%s" % fmt,rec0[pos:end])

        LOG(3, "mobiheader: %s" % repr(mobiheader))

        # Get and decode the book name
        pos = mobiheader['full_name_offs']
        end = pos + mobiheader['full_name_len']
        name = rec0[pos:end].decode(encodings[mobiheader['encoding']])

        LOG(2,"Book name: %s" % name)
        if mobiheader['id'] != 'MOBI':
            LOG(0,"Mobi header missing!")
        if (0x40 & mobiheader['exth_flags']): # check for EXTH
            exth = parse_exth(rec0,mobiheader['header_len']+16)

    elif ptype == 'TEXtREAd':
        LOG(2,"This is an older MOBI book")

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
    return ret

