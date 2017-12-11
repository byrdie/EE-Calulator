import csv
import struct

def weapontohit_import():

    # Import the dbfamily file
    with open('../../data/dbweapontohit.dat', 'rb') as object_file:
        i = 0
        w2h = []  # array of attributes
        w2h_names = ['','c1','c2']

        # Read off the first 3 unused bytes
        object_file.read(4)

        num_fields = 9

        # try/catch to break out of double loop
        class break2(Exception):
            pass
        try:
            while True:
                flag = False
                w2h_i = []
                for j in range(num_fields):

                    if j == 0:
                        f_len = 100
                    else:
                        f_len = 4

                    datum = object_file.read(f_len)

                    if datum == b'':
                        raise break2

                    # special case to drop unused frames
                    # if field_types[j] == 2 and (datum[0] == 0 or datum[0] == 1 or datum[0] == 204):
                    #     flag = True
                    else:
                        if (j == 0):
                            datum = datum.decode('utf-8').replace('\x00', '')
                            w2h_names.append(datum)
                        elif(j < 3):
                            datum = int.from_bytes(datum, byteorder='little')
                        else:
                            pass
                            # datum = struct.unpack('f', datum)[0]
                            try:
                                datum = int.from_bytes(datum, byteorder='little') / 100
                            except ZeroDivisionError:
                                datum = ''

                    w2h_i.append(datum)

                if (flag == False):
                    w2h.append(w2h_i)

                i = i + 1

        except break2:
            pass


    with open('../../excel/weapontohit_export.csv', 'w') as family_file:
        export_writer = csv.writer(family_file, delimiter=',')

        export_writer.writerow(w2h_names)

        for i in range(len(w2h)):
            export_writer.writerow(w2h[i])

    return w2h