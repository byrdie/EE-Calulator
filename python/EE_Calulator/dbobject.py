import numpy as np
import csv
import struct

def object_import():

    # Import the field names and lengths for a dbobject entry
    with open('../../excel/dbobject_struct.csv') as struct_file:
        struct_stream = csv.reader(struct_file, delimiter=',')

        field_names = []
        field_lengths = []
        field_types = []
        for row in struct_stream:
            if row[0] == '':
                f_name = row[1]
            else:
                f_name = row[0]

            f_len = int(row[2])

            f_type = int(row[3])

            field_names.append(f_name)
            field_lengths.append(f_len)
            field_types.append(f_type)

    field_names.pop()
    L = field_lengths.pop() # Grab the total length of one line

    print(L)


    # Import the dbobject file
    with open('../../data/dbobjects.dat', 'rb') as object_file:
        i = 0
        obj = []     # array of attributes

        object_file.read(L + 4)

        # try/catch to break out of double loop
        class break2(Exception):
            pass
        try:
            while True:
                flag = False
                obj_i = []
                for j in range(len(field_lengths)):

                    f_name = field_names[j]
                    f_len = field_lengths[j]
                    datum = object_file.read(f_len)


                    if datum == b'':
                        raise break2

                    # special case to drop unused frames
                    if j == 0 and (datum[0] == 0 or datum[0] == 1 or datum[0] == 204):
                        flag = True
                    else:
                        if(field_types[j] == 1):
                            datum = int.from_bytes(datum, byteorder='little',signed=True)
                        elif (field_types[j] == 2):
                            datum = datum.decode(errors='ignore')
                            datum = datum.replace('\x00','')
                        elif field_types[j] == 3:
                            datum = struct.unpack('f',datum)[0]

                    obj_i.append(datum)

                if(flag == False):
                    obj.append(obj_i)

                i = i + 1

        except break2:
            pass


    with open('../../excel/object_export.csv', 'w') as export_file:
        export_writer = csv.writer(export_file, delimiter=',')

        export_writer.writerow(field_names)

        for i in range(len(obj)):
            export_writer.writerow(obj[i])

    return obj