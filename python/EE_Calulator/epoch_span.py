import csv

def epoch_span():

    with open('../../excel/epoch_span.csv', 'r') as epoch_file:

        epoch_stream = csv.reader(epoch_file, delimiter=',')

        epoch = []

        i = 0
        for row in epoch_stream:

            if i > 0:
                start_epoch = row[1]
                end_epoch = row[2]

                if start_epoch == '':

                    start_epoch = 0
                    end_epoch = 0

                start_epoch = int(start_epoch)
                end_epoch = int(end_epoch)

                epoch_i = [start_epoch, end_epoch]

                epoch.append(epoch_i)

            i = i + 1

    return epoch