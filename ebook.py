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
    ("huff/cdic_record",112,"I"),
    ("huff/cdic_count",116,"I"),
    ("datp_record",120,"I"),
    ("datp_count",124,"I"),
    ("exth_flags",128,"I"),
    ("unknowni@132",132,"32s"),
    ("unknown@164",164,"I"),
    ("drm_offs",168,"I"),
    ("drm_count",172,"I"),
    ("drm_size",176,"I"),
    ("drm_flags",180,"I"),
    ("unknown@184",184,"I"),
    ("unknown@188",188,"I"),
    ("unknown@192",192,"H"),
    ("last_image_record",194,"H"),
    ("unknown@196",196,"I"),
    ("fcis_record",200,"I"),
    ("unknown@204",204,"I"),
    ("flis_record",208,"I"),
    ("unknown@212",212,"I"),
    ("extra_data_flags",242,"H")
    )

EXTH_FMT = ">4x2I"
'''4x = "EXTH", I = hlen, I = record count'''

EXTH_RECORD_TYPES = {
        1 : 'drm server id',
        2 : 'drm commerce id',
        3 : 'drm ebookbase book id',
        100 : 'author', # list
        101 : 'publisher', # list
        102 : 'imprint',
        103 : 'description',
        104 : 'isbn', # list
        105 : 'subject', # list
        106 : 'publication date',
        107 : 'review',
        108 : 'contributor', # list
        109 : 'rights',
        110 : 'subjectcode', # list
        111 : 'type',
        112 : 'source',
        113 : 'asin',
        114 : 'version number', # int
        115 : 'sample', # int (or bool)?
        116 : 'start reading',
        117 : 'adult',
        118 : 'retail price',
        119 : 'retail price currency',
        201 : 'cover offset', # int
        202 : 'thumbnail offset', # int
        203 : 'has fake cover', # bool?
        208 : 'watermark',
        209 : 'tamper proof keys',
        401 : 'clipping limit', # int
        402 : 'publisher limit',
        404 : 'ttsflag',
        501 : 'cde type',
        502 : 'last update time',
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
            LOG(4,"field: %s, fmt: %s, @ [%d:%d], data: %s" % (
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
            LOG(3,"EXTH header: %s" % repr(exth))

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
        LOG(4,"pos: %d, EXTH header len: %d, record count: %d" % (
            pos, hlen, count ))
        pos = end
        while n < count:
            end = pos+calcsize(">2I")
            t,l = unpack(">2I",data[pos:end])
            v = data[end:pos+l]
            if l-8 == 4:
                v = unpack(">I",v)[0]
            if t in EXTH_RECORD_TYPES:
                rec = EXTH_RECORD_TYPES[t]
                LOG(4,"EXTH record '%s' @%d+%d: '%s'" % (
                    rec, pos, l-8, v))
                if rec not in ret:
                    ret[rec] = [v]
                else:
                    ret[rec].append(v)

            else:
                LOG(4,"Found an unknown EXTH record type %d @%d+%d: '%s'" %
                        (t,pos,l-8,repr(v)))
            pos +=l
            n += 1
    return ret

