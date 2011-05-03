#
# http://www.angelfire.com/ego2/idleloop/archives/mbp_file_format.txt
#

# FMT = '>4sIiIIIiIiBBBBiiiiII'
FMT = '>4sIiH2BIIiI8B4i2I'
TYPES = ('DATA', 'BKMK', 'PUBL', 'COVE', 'CATE', 'ABST',
         'GENR', 'TITL', 'AUTH')
TAGS = ('EBAR', 'EBVS', 'ADQM')

import glob
import struct
import palm

for f in (glob.glob("/media/Kindle/documents/*.mbp")):
    db = palm.Database(f)
    #print struct.unpack(FMT, db.records[0].data)
    print "\n\n%s" % f
    for rec in db.records:
        print "\nrecord %d" % rec.uid
        t = rec.data[:4]
        (l,) = struct.unpack(">I", rec.data[4:8])
        print ("%s %d" % (t, l))
        if len(rec.data) < 9:
            continue
        tag = rec.data[8:12]
        if tag in TAGS:
            if tag == 'EBAR':
                print 'EBAR: %d+%d' % (struct.unpack(">II", rec.data[12:20]))
            else:
                print tag
        elif t == 'DATA':
            try:
                print rec.data[8:].decode('utf-16be')
            except:
                print repr(rec.data)
