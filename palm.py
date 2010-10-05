from struct import *

'''
32s - name
H - attributes
H - version
I - creation_date
I - modification_date
I - last_backup_date
I - modification_number
I - appInfoID
I - sortInfoID
4s - type
4s - creator
I - uniqueIDseec
I - nextRecordListID
H - number_of_records
'''

HDR_FMT = '>32sHHIIIIII4s4sIIH'
REC_FMT = '>IB3s' # offset, attributes, info (actually 3 byte integer)

class Database():
    def __init__(self, filename):
        f = open(filename, 'rb')
        self.header = f.read(calcsize(HDR_FMT))
        (self.name, self.attributes, self.version, self.creation_date, 
                self.modification_date, self.last_backup_date,
                self.modification_number, self.appInfoID, self.sortInfoID, 
                self.type, self.creator, self.uniqueIDseed, 
                self.nextRecordListID, self.number_of_records
                ) = unpack(HDR_FMT, self.header)
        self.records = []
        for i in range(self.number_of_records):
            rec_info = unpack(REC_FMT, f.read(calcsize(REC_FMT)))
            offset = rec_info[0]
            flags = rec_info[1]
            (hi, lo) = unpack(">BH", rec_info[2])
            uid = hi*2**16+lo
            self.records.append((offset,flags,uid))
        
        data = f.read()
        self.records.append((f.tell(),0,0))
        f.close()

